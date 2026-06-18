"""Radio propagation: ray tracing and voxel coverage grid.

The model implements the formulas described in ``report/report.tex``:

- distance ``d`` and log-distance path loss ``L(d)``;
- received power ``P_r = P_t + G_t + G_r - L_total``;
- per-material extra losses ``L_obs = sum(alpha_i * l_i)`` (here applied as a
  fixed reflection/transmission loss when a ray hits a surface);
- direct + reflected superposition: each ray contributes power to every voxel
  it traverses, multiple rays sum incoherently (power addition).

The result is a 3D voxel grid of received power in dBm. A horizontal slice of
that grid is used to render the top-down coverage map.
"""

from __future__ import annotations

import hashlib
import pickle
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pyvista as pv

from .osm_parser import OSMData, Tower, UAV_FLIGHT_ALTITUDE_M, UAV_JAM_POWER_DBM


TX_POWER_DBM = 46.0
TX_ANTENNA_GAIN_DB = 15.0
RX_ANTENNA_GAIN_DB = 0.0
PATH_LOSS_REF_DB = 32.0  # L(d0) at d0 = 1 m, ~ free space at 900 MHz
PATH_LOSS_REF_DISTANCE_M = 1.0
PATH_LOSS_EXPONENT = 2.6  # urban-ish n
NOISE_FLOOR_DBM = -100.0
BACKGROUND_JAM_POWER_DBM: float | None = None
RAY_INITIAL_OFFSET_M = 0.5
RAY_MIN_SEGMENT_M = 1.0
RAY_POWER_CUTOFF_DBM = -130.0

REFLECTION_LOSS_DB = {
    "building": 8.0,
    "ferry": 3.0,
    "boundary": 14.0,
}
DEFAULT_REFLECTION_LOSS_DB = 10.0

WAVE_SOURCE_HEIGHT_RATIO = 0.9
MAX_COVERAGE_CACHE_ITEMS = 128
COVERAGE_CACHE_VERSION = 7
COVERAGE_CACHE_DIR = Path(__file__).resolve().parent.parent / ".cache" / "coverage"
MAX_STATIC_RAY_CACHE_ITEMS = 16


@dataclass
class CoverageGrid:
    """Voxel grid of received signal power, accumulated linearly."""

    origin_xyz: tuple[float, float, float]
    voxel_size_m: float
    shape: tuple[int, int, int]
    power_linear: np.ndarray  # mW, summed across rays
    bounds_xyz: tuple[float, float, float, float, float, float]
    jam_power_linear: np.ndarray | None = None

    def power_dbm(self) -> np.ndarray:
        with np.errstate(divide="ignore"):
            return 10.0 * np.log10(np.maximum(self.power_linear, 1e-15))

    def snr_db(self) -> np.ndarray:
        denominator_mw: float | np.ndarray = _dbm_to_mw(NOISE_FLOOR_DBM)
        if BACKGROUND_JAM_POWER_DBM is not None:
            denominator_mw += _dbm_to_mw(BACKGROUND_JAM_POWER_DBM)
        if self.jam_power_linear is not None:
            denominator_mw = denominator_mw + self.jam_power_linear
        with np.errstate(divide="ignore"):
            return 10.0 * np.log10(
                np.maximum(self.power_linear, 1e-15) / np.maximum(denominator_mw, 1e-15)
            )

    def power_slice_at_z(self, z_m: float) -> np.ndarray:
        z_index = int(np.clip(
            np.floor((z_m - self.origin_xyz[2]) / self.voxel_size_m),
            0,
            self.shape[2] - 1,
        ))
        return self.power_dbm()[:, :, z_index]

    def quality_slice_at_z(self, z_m: float) -> np.ndarray:
        z_index = int(np.clip(
            np.floor((z_m - self.origin_xyz[2]) / self.voxel_size_m),
            0,
            self.shape[2] - 1,
        ))
        return self.snr_db()[:, :, z_index]


@dataclass(frozen=True)
class RaySegment:
    """One straight part of a traced ray with the power used for drawing it."""

    start: np.ndarray
    end: np.ndarray
    direction: np.ndarray
    start_path_m: float
    reflection_loss_db: float
    power_dbm: float


@dataclass
class _ReflectorScene:
    """Combined reflector mesh with a per-cell material id array."""

    mesh: pv.PolyData
    cell_material_ids: np.ndarray
    material_names: list[str]

    def material_for_cell(self, cell_index: int) -> str:
        if cell_index < 0 or cell_index >= self.cell_material_ids.shape[0]:
            return "building"
        material_id = int(self.cell_material_ids[cell_index])
        if 0 <= material_id < len(self.material_names):
            return self.material_names[material_id]
        return "building"


_STATIC_RAY_CACHE: dict[tuple, list[list[RaySegment]]] = {}
_STATIC_RAY_CACHE_ORDER: list[tuple] = []


def _dbm_to_mw(power_dbm: float) -> float:
    return 10.0 ** (power_dbm / 10.0)


def _tower_center_xy(tower: Tower) -> tuple[float, float]:
    xs = [x for x, _ in tower.footprint]
    ys = [y for _, y in tower.footprint]
    return sum(xs) / len(xs), sum(ys) / len(ys)


def _tower_source_xyz(tower: Tower) -> np.ndarray:
    cx, cy = _tower_center_xy(tower)
    return np.array((cx, cy, tower.height_m * WAVE_SOURCE_HEIGHT_RATIO), dtype=np.float64)


def _scene_geometry_digest(data: OSMData) -> str:
    """Compact signature of geometry that affects ray tracing."""

    buildings_sig = tuple(
        (
            float(round(float(building.height_m), 3)),
            building.kind,
            tuple(
                (float(round(float(x), 3)), float(round(float(y), 3)))
                for x, y in building.footprint
            ),
        )
        for building in data.buildings
    )
    boundary_sig = tuple(
        (float(round(float(x), 3)), float(round(float(y), 3)))
        for x, y in data.boundary_xy
    )
    payload = repr((buildings_sig, boundary_sig)).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _fibonacci_sphere_directions(count: int) -> np.ndarray:
    """Roughly uniform unit vectors on a sphere via the Fibonacci lattice."""

    if count <= 0:
        return np.zeros((0, 3), dtype=np.float64)

    indices = np.arange(count, dtype=np.float64) + 0.5
    phi = np.arccos(1.0 - 2.0 * indices / count)
    golden_angle = np.pi * (1.0 + 5.0 ** 0.5)
    theta = golden_angle * indices
    sin_phi = np.sin(phi)
    return np.stack(
        (sin_phi * np.cos(theta), sin_phi * np.sin(theta), np.cos(phi)),
        axis=1,
    )


def _gather_reflectors(
    data: OSMData,
    buildings_mesh: pv.MultiBlock | None,
    ferry_mesh: pv.MultiBlock | None,
    boundary_mesh: pv.PolyData | None,
) -> _ReflectorScene | None:
    """Merge all reflectors into one mesh with a per-cell material id array."""

    parts: list[pv.PolyData] = []
    cell_material_ids: list[np.ndarray] = []
    material_names: list[str] = ["building", "ferry", "boundary"]
    name_to_id = {name: idx for idx, name in enumerate(material_names)}

    def _add(block: pv.MultiBlock | None, material: str) -> None:
        if block is None or block.n_blocks == 0:
            return
        for sub in block:
            if sub is None or sub.n_points == 0:
                continue
            triangulated = sub.triangulate()
            if triangulated.n_points == 0 or triangulated.n_cells == 0:
                continue
            parts.append(triangulated)
            cell_material_ids.append(
                np.full(triangulated.n_cells, name_to_id[material], dtype=np.int32)
            )

    _add(buildings_mesh, "building")
    _add(ferry_mesh, "ferry")

    if boundary_mesh is not None and boundary_mesh.n_points > 0:
        triangulated = boundary_mesh.triangulate()
        if triangulated.n_points > 0 and triangulated.n_cells > 0:
            parts.append(triangulated)
            cell_material_ids.append(
                np.full(triangulated.n_cells, name_to_id["boundary"], dtype=np.int32)
            )

    if not parts:
        return None

    merged = parts[0].copy()
    for part in parts[1:]:
        merged = merged.merge(part)

    return _ReflectorScene(
        mesh=merged,
        cell_material_ids=np.concatenate(cell_material_ids),
        material_names=material_names,
    )


def _path_loss_db(distance_m: float) -> float:
    if distance_m <= PATH_LOSS_REF_DISTANCE_M:
        return PATH_LOSS_REF_DB
    return PATH_LOSS_REF_DB + 10.0 * PATH_LOSS_EXPONENT * np.log10(
        distance_m / PATH_LOSS_REF_DISTANCE_M
    )


def _path_loss_db_array(distance_m: np.ndarray) -> np.ndarray:
    distances = np.maximum(distance_m, PATH_LOSS_REF_DISTANCE_M)
    return PATH_LOSS_REF_DB + 10.0 * PATH_LOSS_EXPONENT * np.log10(
        distances / PATH_LOSS_REF_DISTANCE_M
    )


def _voxel_indices_along_segment(
    grid_origin: np.ndarray,
    voxel_size: float,
    grid_shape: tuple[int, int, int],
    point_a: np.ndarray,
    point_b: np.ndarray,
) -> np.ndarray:
    """Return indices of voxels touched along ``[a, b]`` via uniform sampling."""

    segment_length = float(np.linalg.norm(point_b - point_a))
    if segment_length < 1e-6:
        return np.zeros((0, 3), dtype=np.int64)

    sample_count = max(2, int(np.ceil(segment_length / (voxel_size * 0.5))))
    ts = np.linspace(0.0, 1.0, sample_count)
    samples = point_a + ts[:, None] * (point_b - point_a)
    indices = np.floor((samples - grid_origin) / voxel_size).astype(np.int64)
    grid_shape_array = np.array(grid_shape, dtype=np.int64)
    valid_mask = np.all((indices >= 0) & (indices < grid_shape_array), axis=1)
    if not np.any(valid_mask):
        return np.zeros((0, 3), dtype=np.int64)
    return np.unique(indices[valid_mask], axis=0)


def _accumulate_segment_power(
    start: np.ndarray,
    end: np.ndarray,
    direction: np.ndarray,
    segment_start_path_m: float,
    reflection_loss_db: float,
    segment_power_dbm: float,
    transmit_dbm: float,
    grid_origin: np.ndarray,
    voxel_size: float,
    grid_shape: tuple[int, int, int],
    power_grid: np.ndarray,
    line_segments: list[tuple[np.ndarray, np.ndarray, float]],
) -> None:
    segment_distance = float(np.linalg.norm(end - start))
    if segment_distance < RAY_MIN_SEGMENT_M:
        return

    voxel_idx = _voxel_indices_along_segment(
        grid_origin, voxel_size, grid_shape, start, end
    )
    if voxel_idx.shape[0] > 0:
        voxel_centers = grid_origin + (voxel_idx.astype(np.float64) + 0.5) * voxel_size
        segment_offsets_m = np.clip(
            (voxel_centers - start) @ direction,
            0.0,
            segment_distance,
        )
        voxel_path_m = np.maximum(
            segment_start_path_m + segment_offsets_m,
            RAY_MIN_SEGMENT_M,
        )
        voxel_rx_dbm = (
            transmit_dbm
            - _path_loss_db_array(voxel_path_m)
            - reflection_loss_db
        )
        valid_mask = voxel_rx_dbm >= RAY_POWER_CUTOFF_DBM
        if np.any(valid_mask):
            rx_linear_mw = 10.0 ** (voxel_rx_dbm[valid_mask] / 10.0)
            valid_voxel_idx = voxel_idx[valid_mask]
            power_grid[
                valid_voxel_idx[:, 0], valid_voxel_idx[:, 1], valid_voxel_idx[:, 2]
            ] += rx_linear_mw

    line_segments.append((start.copy(), end.copy(), segment_power_dbm))


def _reflect_direction(direction: np.ndarray, normal: np.ndarray) -> np.ndarray:
    return direction - 2.0 * np.dot(direction, normal) * normal


def _closest_hit(
    reflectors: _ReflectorScene,
    origin: np.ndarray,
    direction: np.ndarray,
    max_distance: float,
    cell_normals: np.ndarray,
) -> tuple[float, np.ndarray, np.ndarray, str] | None:
    """Find the nearest ray-mesh hit on the combined reflector scene."""

    end_point = origin + direction * max_distance
    try:
        points, indices = reflectors.mesh.ray_trace(
            origin.tolist(),
            end_point.tolist(),
            first_point=False,
        )
    except Exception:
        return None
    if len(points) == 0:
        return None

    deltas = points - origin
    distances = np.linalg.norm(deltas, axis=1)
    valid_mask = distances > 1e-3
    if not np.any(valid_mask):
        return None

    valid_distances = distances[valid_mask]
    valid_points = points[valid_mask]
    valid_indices = np.array(indices)[valid_mask]
    nearest_local = int(np.argmin(valid_distances))
    nearest_distance = float(valid_distances[nearest_local])
    nearest_point = valid_points[nearest_local]
    nearest_cell = int(valid_indices[nearest_local])

    if 0 <= nearest_cell < cell_normals.shape[0]:
        normal = cell_normals[nearest_cell].astype(np.float64)
    else:
        normal = np.array((0.0, 0.0, 1.0), dtype=np.float64)
    normal_length = float(np.linalg.norm(normal))
    if normal_length < 1e-6:
        normal = np.array((0.0, 0.0, 1.0), dtype=np.float64)
    else:
        normal = normal / normal_length

    material = reflectors.material_for_cell(nearest_cell)
    return nearest_distance, nearest_point, normal, material


def _trace_ray_segments(
    source_xyz: np.ndarray,
    direction: np.ndarray,
    reflectors: _ReflectorScene | None,
    cell_normals: np.ndarray,
    max_bounces: int,
    grid_max_distance: float,
) -> list[RaySegment]:
    """Trace one ray with up to ``max_bounces`` reflections."""

    segments: list[RaySegment] = []
    transmit_dbm = TX_POWER_DBM + TX_ANTENNA_GAIN_DB + RX_ANTENNA_GAIN_DB
    cumulative_path_m = 0.0
    cumulative_reflection_loss_db = 0.0
    origin = source_xyz + direction * RAY_INITIAL_OFFSET_M
    current_dir = direction

    for _bounce_index in range(max_bounces + 1):
        if reflectors is None:
            hit = None
        else:
            hit = _closest_hit(
                reflectors, origin, current_dir, grid_max_distance, cell_normals
            )
        if hit is None:
            segment_end = origin + current_dir * grid_max_distance
            segment_distance = grid_max_distance
        else:
            segment_distance, hit_point, hit_normal, hit_material = hit
            segment_end = hit_point

        if segment_distance < RAY_MIN_SEGMENT_M:
            break

        start_path_m = max(cumulative_path_m, RAY_MIN_SEGMENT_M)
        start_rx_dbm = (
            transmit_dbm
            - _path_loss_db(start_path_m)
            - cumulative_reflection_loss_db
        )
        if start_rx_dbm < RAY_POWER_CUTOFF_DBM:
            break

        mid_path_m = cumulative_path_m + segment_distance * 0.5
        loss_db = _path_loss_db(max(mid_path_m, RAY_MIN_SEGMENT_M))
        rx_dbm = transmit_dbm - loss_db - cumulative_reflection_loss_db

        segments.append(
            RaySegment(
                start=origin.copy(),
                end=segment_end.copy(),
                direction=current_dir.copy(),
                start_path_m=cumulative_path_m,
                reflection_loss_db=cumulative_reflection_loss_db,
                power_dbm=rx_dbm,
            )
        )

        if hit is None:
            return segments

        cumulative_path_m += segment_distance
        material_loss = REFLECTION_LOSS_DB.get(hit_material, DEFAULT_REFLECTION_LOSS_DB)
        cumulative_reflection_loss_db += material_loss

        current_dir = _reflect_direction(current_dir, hit_normal)
        # Push origin slightly off the surface to avoid self-hits
        origin = hit_point + current_dir * RAY_INITIAL_OFFSET_M

    return segments


def _accumulate_ray_segments(
    segments: list[RaySegment],
    grid_origin: np.ndarray,
    voxel_size: float,
    grid_shape: tuple[int, int, int],
    power_grid: np.ndarray,
    line_segments: list[tuple[np.ndarray, np.ndarray, float]],
) -> None:
    transmit_dbm = TX_POWER_DBM + TX_ANTENNA_GAIN_DB + RX_ANTENNA_GAIN_DB
    for segment in segments:
        _accumulate_segment_power(
            segment.start,
            segment.end,
            segment.direction,
            segment.start_path_m,
            segment.reflection_loss_db,
            segment.power_dbm,
            transmit_dbm,
            grid_origin,
            voxel_size,
            grid_shape,
            power_grid,
            line_segments,
        )


def _grid_bounds_for_data(data: OSMData) -> tuple[float, float, float, float, float, float]:
    if data.boundary_xy:
        xs = [x for x, _ in data.boundary_xy]
        ys = [y for _, y in data.boundary_xy]
        minx, maxx = min(xs), max(xs)
        miny, maxy = min(ys), max(ys)
    else:
        minx, miny, maxx, maxy = data.bounds_xy

    z_min = 0.0
    tower_max_height = max(
        (tower.height_m for tower in data.towers if tower.enabled),
        default=120.0,
    )
    z_max = max(120.0, tower_max_height + 30.0)
    return (minx, maxx, miny, maxy, z_min, z_max)


def _uav_position_xyz(data: OSMData) -> tuple[float, float, float] | None:
    if not data.uav_enabled or not data.uav_active:
        return None

    if data.boundary_xy:
        xs = [x for x, _ in data.boundary_xy]
        ys = [y for _, y in data.boundary_xy]
        minx, maxx = min(xs), max(xs)
        miny, maxy = min(ys), max(ys)
    else:
        minx, miny, maxx, maxy = data.bounds_xy

    margin_m = 80.0
    progress = float(np.clip(data.uav_progress, 0.0, 1.0))
    x = minx - margin_m + progress * ((maxx - minx) + margin_m * 2.0)
    y = (miny + maxy) * 0.5
    return (x, y, UAV_FLIGHT_ALTITUDE_M)


def _compute_uav_jam_grid(
    data: OSMData,
    grid_origin: np.ndarray,
    voxel_size: float,
    grid_shape: tuple[int, int, int],
) -> np.ndarray | None:
    uav_position = _uav_position_xyz(data)
    if uav_position is None:
        return None

    ix, iy, iz = np.indices(grid_shape, dtype=np.float64)
    x = grid_origin[0] + (ix + 0.5) * voxel_size
    y = grid_origin[1] + (iy + 0.5) * voxel_size
    z = grid_origin[2] + (iz + 0.5) * voxel_size
    ux, uy, uz = uav_position
    distance_m = np.sqrt((x - ux) ** 2 + (y - uy) ** 2 + (z - uz) ** 2)
    jam_dbm = UAV_JAM_POWER_DBM - _path_loss_db_array(distance_m)
    return 10.0 ** (jam_dbm / 10.0)


def coverage_signature(data: OSMData) -> tuple:
    """Cheap signature so we can detect when recompute is needed."""

    towers_sig = tuple(
        (
            tower.name,
            float(round(_tower_center_xy(tower)[0], 3)),
            float(round(_tower_center_xy(tower)[1], 3)),
            float(round(float(tower.height_m), 3)),
            tower.enabled,
        )
        for tower in data.towers
    )
    return (
        float(round(float(data.voxel_size_m), 3)),
        int(data.ray_count),
        int(data.ray_max_bounces),
        bool(data.ferry_enabled),
        float(round(float(data.ferry_progress % 1.0), 3)) if data.ferry_enabled else None,
        bool(data.uav_enabled),
        bool(data.uav_active) if data.uav_enabled else None,
        float(round(float(data.uav_progress), 3))
        if data.uav_enabled and data.uav_active
        else None,
        towers_sig,
        _scene_geometry_digest(data),
    )


def _static_ray_signature(data: OSMData) -> tuple:
    towers_sig = tuple(
        (
            tower.name,
            float(round(_tower_center_xy(tower)[0], 3)),
            float(round(_tower_center_xy(tower)[1], 3)),
            float(round(float(tower.height_m), 3)),
            tower.enabled,
        )
        for tower in data.towers
    )
    return (
        int(data.ray_count),
        int(data.ray_max_bounces),
        tuple(float(round(value, 3)) for value in data.bounds_xy),
        tuple(float(round(value, 3)) for value in (data.view_bounds_xy or ())),
        towers_sig,
        _scene_geometry_digest(data),
    )


def _store_static_ray_cache(signature: tuple, rays: list[list[RaySegment]]) -> None:
    if signature in _STATIC_RAY_CACHE:
        _STATIC_RAY_CACHE[signature] = rays
        return

    _STATIC_RAY_CACHE[signature] = rays
    _STATIC_RAY_CACHE_ORDER.append(signature)
    while len(_STATIC_RAY_CACHE_ORDER) > MAX_STATIC_RAY_CACHE_ITEMS:
        oldest = _STATIC_RAY_CACHE_ORDER.pop(0)
        _STATIC_RAY_CACHE.pop(oldest, None)


def _segment_intersects_bounds(
    segment: RaySegment,
    bounds_xyz: tuple[float, float, float, float, float, float],
) -> bool:
    xmin, xmax, ymin, ymax, zmin, zmax = bounds_xyz
    segment_min = np.minimum(segment.start, segment.end)
    segment_max = np.maximum(segment.start, segment.end)
    return (
        segment_max[0] >= xmin
        and segment_min[0] <= xmax
        and segment_max[1] >= ymin
        and segment_min[1] <= ymax
        and segment_max[2] >= zmin
        and segment_min[2] <= zmax
    )


def _ray_may_hit_ferry(
    segments: list[RaySegment],
    ferry_bounds_xyz: tuple[float, float, float, float, float, float] | None,
) -> bool:
    if ferry_bounds_xyz is None:
        return False
    return any(_segment_intersects_bounds(segment, ferry_bounds_xyz) for segment in segments)


def _mesh_bounds_xyz(mesh: object | None) -> tuple[float, float, float, float, float, float] | None:
    if mesh is None:
        return None
    if hasattr(mesh, "n_points") and int(getattr(mesh, "n_points")) == 0:
        return None
    if hasattr(mesh, "n_blocks") and int(getattr(mesh, "n_blocks")) == 0:
        return None
    bounds = getattr(mesh, "bounds", None)
    if bounds is None:
        return None
    xmin, xmax, ymin, ymax, zmin, zmax = (float(value) for value in bounds)
    if not all(np.isfinite((xmin, xmax, ymin, ymax, zmin, zmax))):
        return None
    return xmin, xmax, ymin, ymax, zmin, zmax


def _trace_static_rays(
    data: OSMData,
    static_reflectors: _ReflectorScene | None,
    static_cell_normals: np.ndarray,
    directions: np.ndarray,
    grid_max_distance: float,
) -> list[list[RaySegment]]:
    signature = _static_ray_signature(data)
    cached = _STATIC_RAY_CACHE.get(signature)
    if cached is not None:
        return cached

    rays: list[list[RaySegment]] = []
    for tower in data.towers:
        if not tower.enabled:
            continue
        source_xyz = _tower_source_xyz(tower)
        for direction in directions:
            rays.append(
                _trace_ray_segments(
                    source_xyz,
                    direction.astype(np.float64),
                    static_reflectors,
                    static_cell_normals,
                    int(data.ray_max_bounces),
                    grid_max_distance,
                )
            )

    _store_static_ray_cache(signature, rays)
    return rays


def compute_coverage(
    data: OSMData,
    buildings_mesh: pv.MultiBlock | None,
    ferry_mesh: pv.MultiBlock | None,
    boundary_mesh: pv.PolyData | None,
) -> tuple[CoverageGrid, list[tuple[np.ndarray, np.ndarray, float]]]:
    """Run ray tracing and return the voxel grid and ray segments for drawing."""

    minx, maxx, miny, maxy, zmin, zmax = _grid_bounds_for_data(data)
    voxel_size = max(float(data.voxel_size_m), 1.0)
    grid_shape = (
        max(1, int(np.ceil((maxx - minx) / voxel_size))),
        max(1, int(np.ceil((maxy - miny) / voxel_size))),
        max(1, int(np.ceil((zmax - zmin) / voxel_size))),
    )
    grid_origin = np.array((minx, miny, zmin), dtype=np.float64)
    grid_diagonal = float(
        ((maxx - minx) ** 2 + (maxy - miny) ** 2 + (zmax - zmin) ** 2) ** 0.5
    )

    static_reflectors = _gather_reflectors(data, buildings_mesh, None, boundary_mesh)
    full_reflectors = _gather_reflectors(data, buildings_mesh, ferry_mesh, boundary_mesh)

    def _cell_normals_for(reflectors: _ReflectorScene | None) -> np.ndarray:
        if reflectors is None:
            return np.zeros((0, 3), dtype=np.float64)
        normals_array = reflectors.mesh.cell_normals
        return (
            np.array(normals_array, dtype=np.float64)
            if normals_array is not None and len(normals_array) > 0
            else np.zeros((0, 3), dtype=np.float64)
        )

    static_cell_normals = _cell_normals_for(static_reflectors)
    full_cell_normals = _cell_normals_for(full_reflectors)

    ray_count = max(1, int(data.ray_count))
    directions = _fibonacci_sphere_directions(ray_count)
    power_grid = np.zeros(grid_shape, dtype=np.float64)
    line_segments: list[tuple[np.ndarray, np.ndarray, float]] = []

    static_rays = _trace_static_rays(
        data,
        static_reflectors,
        static_cell_normals,
        directions,
        grid_diagonal,
    )
    ferry_bounds_xyz = _mesh_bounds_xyz(ferry_mesh)
    static_ray_index = 0

    for tower in data.towers:
        if not tower.enabled:
            continue
        source_xyz = _tower_source_xyz(tower)
        for direction in directions:
            static_segments = static_rays[static_ray_index]
            static_ray_index += 1
            if _ray_may_hit_ferry(static_segments, ferry_bounds_xyz):
                segments = _trace_ray_segments(
                    source_xyz,
                    direction.astype(np.float64),
                    full_reflectors,
                    full_cell_normals,
                    int(data.ray_max_bounces),
                    grid_diagonal,
                )
            else:
                segments = static_segments
            _accumulate_ray_segments(
                segments,
                grid_origin,
                voxel_size,
                grid_shape,
                power_grid,
                line_segments,
            )

    coverage = CoverageGrid(
        origin_xyz=tuple(grid_origin.tolist()),
        voxel_size_m=voxel_size,
        shape=grid_shape,
        power_linear=power_grid,
        bounds_xyz=(minx, maxx, miny, maxy, zmin, zmax),
        jam_power_linear=_compute_uav_jam_grid(
            data,
            grid_origin,
            voxel_size,
            grid_shape,
        ),
    )
    return coverage, line_segments


def coverage_is_fresh(data: OSMData) -> bool:
    return (
        data.coverage_grid is not None
        and data.coverage_signature == coverage_signature(data)
    )


def activate_cached_coverage(data: OSMData, signature: tuple | None = None) -> bool:
    """Make the cached coverage for ``signature`` current, if present."""

    key = coverage_signature(data) if signature is None else signature
    cached = data.coverage_cache.get(key)
    if cached is None:
        return False

    data.coverage_grid = cached
    data.coverage_signature = key
    return True


def coverage_is_cached(data: OSMData, signature: tuple | None = None) -> bool:
    key = coverage_signature(data) if signature is None else signature
    return key in data.coverage_cache


def _coverage_cache_path(signature: tuple) -> Path:
    key = repr((COVERAGE_CACHE_VERSION, signature)).encode("utf-8")
    digest = hashlib.sha256(key).hexdigest()
    return COVERAGE_CACHE_DIR / f"{digest}.pkl"


def persistent_coverage_exists(signature: tuple) -> bool:
    return _coverage_cache_path(signature).exists()


def load_persistent_coverage(data: OSMData, signature: tuple | None = None) -> bool:
    """Load a coverage result from disk into the in-memory cache if available."""

    key = coverage_signature(data) if signature is None else signature
    cache_path = _coverage_cache_path(key)
    if not cache_path.exists():
        return False

    try:
        with cache_path.open("rb") as cache_file:
            coverage_result = pickle.load(cache_file)
    except (OSError, pickle.PickleError, EOFError):
        return False

    store_coverage_result(data, key, coverage_result, persist=False)
    return True


def store_coverage_result(
    data: OSMData,
    signature: tuple,
    coverage_result: object,
    persist: bool = True,
) -> None:
    """Store a computed coverage result and keep the cache bounded."""

    data.coverage_grid = coverage_result
    data.coverage_signature = signature
    if signature in data.coverage_cache:
        data.coverage_cache[signature] = coverage_result
        if persist:
            _store_persistent_coverage(signature, coverage_result)
        return

    data.coverage_cache[signature] = coverage_result
    data.coverage_cache_order.append(signature)
    while len(data.coverage_cache_order) > MAX_COVERAGE_CACHE_ITEMS:
        oldest = data.coverage_cache_order.pop(0)
        data.coverage_cache.pop(oldest, None)

    if persist:
        _store_persistent_coverage(signature, coverage_result)


def _store_persistent_coverage(signature: tuple, coverage_result: object) -> None:
    cache_path = _coverage_cache_path(signature)
    try:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        with cache_path.open("wb") as cache_file:
            pickle.dump(coverage_result, cache_file, protocol=pickle.HIGHEST_PROTOCOL)
    except OSError:
        return


def update_coverage_signature(data: OSMData) -> None:
    data.coverage_signature = coverage_signature(data)


def invalidate_coverage(data: OSMData) -> None:
    data.coverage_grid = None
    data.coverage_signature = ()
    data.coverage_cache.clear()
    data.coverage_cache_order.clear()
