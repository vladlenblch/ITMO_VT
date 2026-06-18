"""Build PyVista meshes from projected OSM features."""

from __future__ import annotations

import numpy as np
import pyvista as pv

from .osm_parser import Building, OSMData, Tower, UAV_FLIGHT_ALTITUDE_M
from .radio import (
    CoverageGrid,
    NOISE_FLOOR_DBM,
    RAY_POWER_CUTOFF_DBM,
    WAVE_SOURCE_HEIGHT_RATIO,
    activate_cached_coverage,
    compute_coverage,
    coverage_is_fresh,
    coverage_signature,
    load_persistent_coverage,
    store_coverage_result,
)


GROUND_MARGIN_M = 20.0
GROUND_Z = 0.0
CONTOUR_Z = 0.25
BOUNDARY_WALL_HEIGHT_M = 400.0
MIN_BUILDING_FOOTPRINT_AREA_M2 = 35.0
TOWER_RESOLUTION = 48
TOWER_CONCRETE_HEIGHT_M = 100.0
TOWER_BASE_DIAMETER_M = 10.3
TOWER_PLATFORM_DIAMETER_M = 17.6
TOWER_MAST_DIAMETER_M = 2.0
FERRY_LENGTH_M = 320.0
FERRY_WIDTH_M = 48.0
FERRY_HULL_HEIGHT_M = 18.0
FERRY_SUPERSTRUCTURE_HEIGHT_M = 77.0
FERRY_SUPERSTRUCTURE_WIDTH_RATIO = 0.78
FERRY_SUPERSTRUCTURE_LENGTH_RATIO = 0.7
FERRY_DRAFT_M = 12.0
FERRY_BOW_TAPER_M = 60.0
WAVE_SPACING_M = 45.0
WAVE_RESOLUTION = 96
WAVE_PLANE_ANGLES_DEG = (10.0, 24.0, 38.0, 52.0, 66.0, 80.0)
WAVE_MESH_PREFIX = "tower_waves_"
COVERAGE_SLICE_RENDER_OFFSET_M = 0.5
UAV_PATH_MARGIN_M = 80.0
UAV_BODY_LENGTH_M = 24.0
UAV_BODY_WIDTH_M = 8.0
UAV_BODY_HEIGHT_M = 4.0
UAV_ARM_LENGTH_M = 34.0
UAV_ROTOR_RADIUS_M = 5.0


def _polygon_area(footprint: list[tuple[float, float]]) -> float:
    if len(footprint) < 3:
        return 0.0
    area = 0.0
    for i, (x1, y1) in enumerate(footprint):
        x2, y2 = footprint[(i + 1) % len(footprint)]
        area += x1 * y2 - x2 * y1
    return abs(area) * 0.5


def _polygon_to_polydata(footprint: list[tuple[float, float]]) -> pv.PolyData | None:
    """Convert a 2D polygon footprint to a flat PyVista polygon at raised ground."""

    if len(footprint) < 3:
        return None
    points = np.array([(x, y, GROUND_Z) for x, y in footprint], dtype=np.float32)
    n = len(points)
    faces = np.concatenate(([n], np.arange(n, dtype=np.int64)))
    return pv.PolyData(points, faces=faces)


def _build_buildings_mesh(buildings: list[Building]) -> pv.MultiBlock:
    """Extrude each footprint vertically into a solid block."""

    block = pv.MultiBlock()
    for i, building in enumerate(buildings):
        if _polygon_area(building.footprint) < MIN_BUILDING_FOOTPRINT_AREA_M2:
            continue
        base = _polygon_to_polydata(building.footprint)
        if base is None:
            continue
        solid = base.extrude((0.0, 0.0, building.height_m), capping=True)
        block.append(solid, name=f"building_{i}")
    return block


def _tower_center(tower: Tower) -> tuple[float, float]:
    xs = [x for x, _ in tower.footprint]
    ys = [y for _, y in tower.footprint]
    return sum(xs) / len(xs), sum(ys) / len(ys)


def _max_wave_radius(
    center: tuple[float, float, float],
    bounds_xy: tuple[float, float, float, float],
) -> float:
    cx, cy, cz = center
    minx, miny, maxx, maxy = bounds_xy
    return max(
        ((cx - x) ** 2 + (cy - y) ** 2 + (cz - z) ** 2) ** 0.5
        for x, y in ((minx, miny), (maxx, miny), (maxx, maxy), (minx, maxy))
        for z in (GROUND_Z, BOUNDARY_WALL_HEIGHT_M)
    )


def _point_inside_box(
    point: tuple[float, float, float],
    bounds_xy: tuple[float, float, float, float],
) -> bool:
    x, y, z = point
    minx, miny, maxx, maxy = bounds_xy
    return minx <= x <= maxx and miny <= y <= maxy and GROUND_Z <= z <= BOUNDARY_WALL_HEIGHT_M


def _point_inside_wave_lobe(
    point: tuple[float, float, float],
    center: tuple[float, float, float],
    radial_axis: np.ndarray,
) -> bool:
    dx = point[0] - center[0]
    dy = point[1] - center[1]
    forward_offset = dx * radial_axis[0] + dy * radial_axis[1]
    return forward_offset >= -1e-5 and point[2] <= center[2] + 1e-5


def _bounds_center(bounds_xy: tuple[float, float, float, float]) -> tuple[float, float]:
    minx, miny, maxx, maxy = bounds_xy
    return (minx + maxx) / 2.0, (miny + maxy) / 2.0


def _horizontal_unit_vector(dx: float, dy: float) -> np.ndarray:
    length = (dx * dx + dy * dy) ** 0.5
    if length < 1e-6:
        return np.array((1.0, 0.0, 0.0), dtype=np.float32)
    return np.array((dx / length, dy / length, 0.0), dtype=np.float32)


def _opposite_tower_center(
    tower: Tower,
    tower_center_xy: tuple[float, float],
    perimeter_tower_centers: list[tuple[Tower, tuple[float, float]]],
    fallback_center_xy: tuple[float, float],
) -> tuple[float, float]:
    other_centers = [
        center_xy
        for other_tower, center_xy in perimeter_tower_centers
        if other_tower is not tower
    ]
    if not other_centers:
        return fallback_center_xy

    return max(
        other_centers,
        key=lambda center_xy: (
            (center_xy[0] - tower_center_xy[0]) ** 2
            + (center_xy[1] - tower_center_xy[1]) ** 2
        ),
    )


def _perimeter_tower_index(tower: Tower) -> str | None:
    name = tower.name or ""
    if not name.startswith("perimeter_tower_"):
        return None
    suffix = name.removeprefix("perimeter_tower_")
    return suffix if suffix else None


def _build_tilted_wave_ring(
    center: tuple[float, float, float],
    radius: float,
    radial_axis: np.ndarray,
    angle_deg: float,
) -> list[tuple[float, float, float]]:
    angle_rad = np.deg2rad(angle_deg)
    vertical_axis = np.array((0.0, 0.0, -1.0), dtype=np.float32)
    tangent_axis = np.array((-radial_axis[1], radial_axis[0], 0.0), dtype=np.float32)
    sloped_axis = (
        np.cos(angle_rad) * vertical_axis
        + np.sin(angle_rad) * radial_axis
    )
    sloped_axis /= np.linalg.norm(sloped_axis)

    center_vector = np.array(center, dtype=np.float32)
    angles = np.linspace(0.0, 2.0 * np.pi, WAVE_RESOLUTION, endpoint=False)
    return [
        tuple(
            center_vector
            + radius * np.cos(angle) * tangent_axis
            + radius * np.sin(angle) * sloped_axis
        )
        for angle in angles
    ]


def _build_frustum_mesh(
    center_xy: tuple[float, float],
    z_min: float,
    z_max: float,
    bottom_radius: float,
    top_radius: float,
    resolution: int = TOWER_RESOLUTION,
) -> pv.PolyData:
    """Build a capped vertical frustum or cylinder mesh."""

    cx, cy = center_xy
    angles = np.linspace(0.0, 2.0 * np.pi, resolution, endpoint=False)
    bottom = [
        (cx + np.cos(angle) * bottom_radius, cy + np.sin(angle) * bottom_radius, z_min)
        for angle in angles
    ]
    top = [
        (cx + np.cos(angle) * top_radius, cy + np.sin(angle) * top_radius, z_max)
        for angle in angles
    ]
    points = np.array(bottom + top, dtype=np.float32)

    faces: list[int] = []
    for i in range(resolution):
        j = (i + 1) % resolution
        faces.extend((4, i, j, resolution + j, resolution + i))
    faces.extend((resolution, *range(resolution - 1, -1, -1)))
    faces.extend((resolution, *range(resolution, resolution * 2)))

    return pv.PolyData(points, faces=np.array(faces, dtype=np.int64))


def _build_box_mesh(
    center: tuple[float, float, float],
    size: tuple[float, float, float],
) -> pv.PolyData:
    cx, cy, cz = center
    sx, sy, sz = (value / 2.0 for value in size)
    points = np.array(
        [
            (cx - sx, cy - sy, cz - sz),
            (cx + sx, cy - sy, cz - sz),
            (cx + sx, cy + sy, cz - sz),
            (cx - sx, cy + sy, cz - sz),
            (cx - sx, cy - sy, cz + sz),
            (cx + sx, cy - sy, cz + sz),
            (cx + sx, cy + sy, cz + sz),
            (cx - sx, cy + sy, cz + sz),
        ],
        dtype=np.float32,
    )
    faces = np.array(
        [
            4, 0, 1, 2, 3,
            4, 4, 7, 6, 5,
            4, 0, 4, 5, 1,
            4, 1, 5, 6, 2,
            4, 2, 6, 7, 3,
            4, 3, 7, 4, 0,
        ],
        dtype=np.int64,
    )
    return pv.PolyData(points, faces=faces)


def _build_clipped_box_mesh(
    center: tuple[float, float, float],
    size: tuple[float, float, float],
    clip_y_bounds: tuple[float, float],
) -> pv.PolyData | None:
    cx, cy, cz = center
    sx, sy, sz = size
    clip_y_min, clip_y_max = clip_y_bounds
    visible_y_min = max(cy - sy / 2.0, clip_y_min)
    visible_y_max = min(cy + sy / 2.0, clip_y_max)
    if visible_y_min >= visible_y_max:
        return None

    return _build_box_mesh(
        (cx, (visible_y_min + visible_y_max) / 2.0, cz),
        (sx, visible_y_max - visible_y_min, sz),
    )


def _intersect_footprint_at_y(
    first: tuple[float, float],
    second: tuple[float, float],
    y_limit: float,
) -> tuple[float, float]:
    x1, y1 = first
    x2, y2 = second
    if abs(y2 - y1) < 1e-9:
        return second
    ratio = (y_limit - y1) / (y2 - y1)
    return (x1 + (x2 - x1) * ratio, y_limit)


def _clip_footprint_y_side(
    footprint: list[tuple[float, float]],
    y_limit: float,
    keep_above: bool,
) -> list[tuple[float, float]]:
    if not footprint:
        return []

    clipped: list[tuple[float, float]] = []
    previous = footprint[-1]
    previous_inside = previous[1] >= y_limit if keep_above else previous[1] <= y_limit

    for current in footprint:
        current_inside = current[1] >= y_limit if keep_above else current[1] <= y_limit
        if current_inside:
            if not previous_inside:
                clipped.append(_intersect_footprint_at_y(previous, current, y_limit))
            clipped.append(current)
        elif previous_inside:
            clipped.append(_intersect_footprint_at_y(previous, current, y_limit))

        previous = current
        previous_inside = current_inside

    return clipped


def _clip_footprint_y_bounds(
    footprint: list[tuple[float, float]],
    clip_y_bounds: tuple[float, float],
) -> list[tuple[float, float]]:
    clip_y_min, clip_y_max = clip_y_bounds
    clipped = _clip_footprint_y_side(footprint, clip_y_min, keep_above=True)
    return _clip_footprint_y_side(clipped, clip_y_max, keep_above=False)


def _build_prism_mesh(
    footprint: list[tuple[float, float]],
    z_bottom: float,
    z_top: float,
) -> pv.PolyData | None:
    if len(footprint) < 3:
        return None

    bottom = [(x, y, z_bottom) for x, y in footprint]
    top = [(x, y, z_top) for x, y in footprint]
    points = np.array(bottom + top, dtype=np.float32)

    n = len(footprint)
    faces: list[int] = []
    faces.extend((n, *range(n - 1, -1, -1)))
    faces.extend((n, *range(n, 2 * n)))
    for i in range(n):
        j = (i + 1) % n
        faces.extend((4, i, j, n + j, n + i))

    return pv.PolyData(points, faces=np.array(faces, dtype=np.int64))


def _build_cylinder_mesh(
    center_xy: tuple[float, float],
    z_min: float,
    z_max: float,
    radius: float,
    resolution: int = TOWER_RESOLUTION,
) -> pv.PolyData:
    return _build_frustum_mesh(center_xy, z_min, z_max, radius, radius, resolution)


def _build_tower_visual_meshes(towers: list[Tower]) -> dict[str, pv.MultiBlock]:
    """Build a stylized communication tower: base, platform, steel mast."""

    enabled = pv.MultiBlock()
    disabled = pv.MultiBlock()

    for i, tower in enumerate(towers):
        if len(tower.footprint) < 3:
            continue

        block = enabled if tower.enabled else disabled
        center = _tower_center(tower)
        total_height = max(tower.height_m, TOWER_CONCRETE_HEIGHT_M)
        concrete_height = min(TOWER_CONCRETE_HEIGHT_M, total_height * 0.35)
        mast_top = total_height
        mast_radius = TOWER_MAST_DIAMETER_M / 2.0

        block.append(
            _build_cylinder_mesh(
                center,
                GROUND_Z,
                4.0,
                TOWER_BASE_DIAMETER_M * 0.62,
            ),
            name=f"tower_{i}_base_plinth",
        )
        block.append(
            _build_frustum_mesh(
                center,
                4.0,
                concrete_height,
                TOWER_BASE_DIAMETER_M / 2.0,
                TOWER_BASE_DIAMETER_M * 0.38,
            ),
            name=f"tower_{i}_concrete_shaft",
        )
        block.append(
            _build_cylinder_mesh(
                center,
                concrete_height - 2.2,
                concrete_height + 2.2,
                TOWER_PLATFORM_DIAMETER_M / 2.0,
            ),
            name=f"tower_{i}_main_platform",
        )
        block.append(
            _build_cylinder_mesh(
                center,
                concrete_height + 2.2,
                concrete_height + 12.0,
                TOWER_BASE_DIAMETER_M * 0.42,
            ),
            name=f"tower_{i}_equipment_drum",
        )

        mast_start = concrete_height + 3.0
        if mast_top > mast_start + 10.0:
            block.append(
                _build_cylinder_mesh(
                    center,
                    mast_start,
                    mast_top - 10.0,
                    mast_radius,
                    resolution=32,
                ),
                name=f"tower_{i}_steel_mast",
            )
            block.append(
                _build_frustum_mesh(
                    center,
                    mast_top - 10.0,
                    mast_top,
                    mast_radius,
                    mast_radius * 0.35,
                    resolution=32,
                ),
                name=f"tower_{i}_top_antenna",
            )

        for level in (155.0, 226.0, 297.0, 350.0):
            if mast_start < level < mast_top - 5.0:
                block.append(
                    _build_cylinder_mesh(
                        center,
                        level - 0.7,
                        level + 0.7,
                        mast_radius * 2.2,
                        resolution=32,
                    ),
                    name=f"tower_{i}_antenna_ring_{int(level)}",
                )

    return {
        "tower_enabled": enabled,
        "tower_disabled": disabled,
    }


def build_tower_meshes(towers: list[Tower]) -> dict[str, pv.MultiBlock]:
    """Build only tower meshes for interactive updates."""

    return _build_tower_visual_meshes(towers)


def _build_ferry_hull_mesh(
    center_xy: tuple[float, float],
    length_m: float,
    width_m: float,
    z_bottom: float,
    z_top: float,
    bow_taper_m: float,
    clip_y_bounds: tuple[float, float],
) -> pv.PolyData:
    """Build a tapered ferry hull as a closed prism.

    The bow narrows along +Y, the stern is flat. The hull stays a single solid
    so that future ray/wave reflection treats it like any other building.
    """

    cx, cy = center_xy
    half_w = width_m / 2.0
    half_l = length_m / 2.0
    bow_y = cy + half_l
    stern_y = cy - half_l
    taper_y = bow_y - max(bow_taper_m, 1.0)

    bottom = [
        (cx - half_w, stern_y, z_bottom),
        (cx + half_w, stern_y, z_bottom),
        (cx + half_w, taper_y, z_bottom),
        (cx, bow_y, z_bottom),
        (cx - half_w, taper_y, z_bottom),
    ]
    clipped = _clip_footprint_y_bounds([(x, y) for x, y, _ in bottom], clip_y_bounds)
    mesh = _build_prism_mesh(clipped, z_bottom, z_top)
    return mesh if mesh is not None else pv.PolyData()


def build_ferry_meshes(data: OSMData) -> dict[str, pv.MultiBlock]:
    if (
        not data.ferry_enabled
        or data.ferry_path_x is None
        or data.ferry_path_y_bounds is None
        or data.ferry_clip_y_bounds is None
    ):
        return {"ferry_body": pv.MultiBlock()}

    y_min, y_max = data.ferry_path_y_bounds
    clip_y_bounds = data.ferry_clip_y_bounds
    travel_span = (y_max - y_min) + FERRY_LENGTH_M
    ferry_center_y = (
        y_min - FERRY_LENGTH_M / 2.0 + (data.ferry_progress % 1.0) * travel_span
    )
    ferry_center = (data.ferry_path_x, ferry_center_y)

    body = pv.MultiBlock()

    hull_top_z = FERRY_HULL_HEIGHT_M - FERRY_DRAFT_M
    hull = _build_ferry_hull_mesh(
        ferry_center,
        FERRY_LENGTH_M,
        FERRY_WIDTH_M,
        -FERRY_DRAFT_M,
        hull_top_z,
        FERRY_BOW_TAPER_M,
        clip_y_bounds,
    )
    if hull.n_points > 0:
        body.append(hull, name="ferry_hull")

    superstructure_length = FERRY_LENGTH_M * FERRY_SUPERSTRUCTURE_LENGTH_RATIO
    superstructure_width = FERRY_WIDTH_M * FERRY_SUPERSTRUCTURE_WIDTH_RATIO
    superstructure_center = (
        data.ferry_path_x,
        ferry_center_y - FERRY_LENGTH_M * 0.05,
        hull_top_z + FERRY_SUPERSTRUCTURE_HEIGHT_M / 2.0,
    )
    superstructure = _build_clipped_box_mesh(
        superstructure_center,
        (
            superstructure_width,
            superstructure_length,
            FERRY_SUPERSTRUCTURE_HEIGHT_M,
        ),
        clip_y_bounds,
    )
    if superstructure is not None:
        body.append(superstructure, name="ferry_superstructure")

    bridge_center = (
        data.ferry_path_x,
        ferry_center_y + FERRY_LENGTH_M * 0.18,
        hull_top_z + FERRY_SUPERSTRUCTURE_HEIGHT_M + 6.0,
    )
    bridge = _build_clipped_box_mesh(
        bridge_center,
        (superstructure_width * 0.55, superstructure_length * 0.18, 12.0),
        clip_y_bounds,
    )
    if bridge is not None:
        body.append(bridge, name="ferry_bridge")

    return {"ferry_body": body}


def _uav_position(data: OSMData) -> tuple[float, float, float] | None:
    if not data.uav_enabled or not data.uav_active:
        return None
    bounds = _bounds_from_points(data.boundary_xy) if data.boundary_xy else None
    if bounds is None:
        minx, miny, maxx, maxy = data.bounds_xy
    else:
        minx, miny, maxx, maxy = bounds
    progress = float(np.clip(data.uav_progress, 0.0, 1.0))
    x = minx - UAV_PATH_MARGIN_M + progress * (
        (maxx - minx) + UAV_PATH_MARGIN_M * 2.0
    )
    y = (miny + maxy) * 0.5
    return (x, y, UAV_FLIGHT_ALTITUDE_M)


def build_uav_meshes(data: OSMData) -> dict[str, pv.MultiBlock]:
    position = _uav_position(data)
    body = pv.MultiBlock()
    if position is None:
        return {"uav_body": body}

    x, y, z = position
    fuselage = _build_box_mesh(
        (x, y, z),
        (UAV_BODY_LENGTH_M, UAV_BODY_WIDTH_M, UAV_BODY_HEIGHT_M),
    )
    body.append(fuselage, name="uav_fuselage")

    arm_x = _build_box_mesh(
        (x, y, z),
        (UAV_ARM_LENGTH_M, 1.4, 1.2),
    )
    body.append(arm_x, name="uav_arm_x")
    arm_y = _build_box_mesh(
        (x, y, z),
        (1.4, UAV_ARM_LENGTH_M, 1.2),
    )
    body.append(arm_y, name="uav_arm_y")

    for dx in (-UAV_ARM_LENGTH_M / 2.0, UAV_ARM_LENGTH_M / 2.0):
        for dy in (-UAV_ARM_LENGTH_M / 2.0, UAV_ARM_LENGTH_M / 2.0):
            rotor = pv.Cylinder(
                center=(x + dx, y + dy, z + 1.2),
                direction=(0.0, 0.0, 1.0),
                radius=UAV_ROTOR_RADIUS_M,
                height=0.35,
                resolution=32,
            )
            body.append(rotor, name="uav_rotor")

    return {"uav_body": body}


def build_wave_meshes(data: OSMData) -> dict[str, pv.PolyData]:
    wave_meshes: dict[str, pv.PolyData] = {}
    if not data.boundary_xy:
        return wave_meshes

    boundary_bounds = _bounds_from_points(data.boundary_xy)
    if boundary_bounds is None:
        return wave_meshes

    boundary_center = _bounds_center(boundary_bounds)
    perimeter_tower_centers = [
        (tower, _tower_center(tower))
        for tower in data.towers
        if (tower.name or "").startswith("perimeter_tower_")
    ]
    for tower in data.towers:
        tower_index = _perimeter_tower_index(tower)
        if not tower.enabled or tower_index is None:
            continue

        wave_front_radius = data.tower_wave_phases_m.get(tower_index, data.wave_phase_m)
        if wave_front_radius <= 0.5:
            continue

        points: list[tuple[float, float, float]] = []
        lines: list[int] = []
        tower_center_xy = _tower_center(tower)
        center = (
            tower_center_xy[0],
            tower_center_xy[1],
            tower.height_m * WAVE_SOURCE_HEIGHT_RATIO,
        )
        target_center_xy = _opposite_tower_center(
            tower,
            tower_center_xy,
            perimeter_tower_centers,
            boundary_center,
        )
        radial_axis = _horizontal_unit_vector(
            target_center_xy[0] - tower_center_xy[0],
            target_center_xy[1] - tower_center_xy[1],
        )
        max_radius = _max_wave_radius(center, boundary_bounds)
        radius = wave_front_radius
        if radius > max_radius:
            radius -= (
                np.ceil((radius - max_radius) / WAVE_SPACING_M)
                * WAVE_SPACING_M
            )
        while radius > 0.5:
            for angle_deg in WAVE_PLANE_ANGLES_DEG:
                ring = _build_tilted_wave_ring(
                    center,
                    radius,
                    radial_axis,
                    angle_deg,
                )
                point_indexes: list[int | None] = []
                for point in ring:
                    if (
                        _point_inside_box(point, boundary_bounds)
                        and _point_inside_wave_lobe(point, center, radial_axis)
                    ):
                        point_indexes.append(len(points))
                        points.append(point)
                    else:
                        point_indexes.append(None)
                for i, start_index in enumerate(point_indexes):
                    end_index = point_indexes[(i + 1) % WAVE_RESOLUTION]
                    if start_index is not None and end_index is not None:
                        lines.extend((2, start_index, end_index))
            radius -= WAVE_SPACING_M

        if points:
            wave_meshes[f"{WAVE_MESH_PREFIX}{tower_index}"] = pv.PolyData(
                np.array(points, dtype=np.float32),
                lines=np.array(lines, dtype=np.int64),
            )

    return wave_meshes


def _ensure_coverage_cached(data: OSMData) -> tuple[CoverageGrid, list[tuple[np.ndarray, np.ndarray, float]]]:
    """Compute (or reuse cached) ray tracing results for the current scene."""

    if coverage_is_fresh(data) and data.coverage_grid is not None:
        cached = data.coverage_grid
        if isinstance(cached, tuple):
            return cached  # type: ignore[return-value]

    signature = coverage_signature(data)
    if activate_cached_coverage(data, signature) and isinstance(data.coverage_grid, tuple):
        return data.coverage_grid  # type: ignore[return-value]
    if load_persistent_coverage(data, signature) and isinstance(data.coverage_grid, tuple):
        return data.coverage_grid  # type: ignore[return-value]

    buildings_mesh = _build_buildings_mesh(data.buildings)
    ferry_meshes = build_ferry_meshes(data)
    ferry_mesh = ferry_meshes.get("ferry_body")
    boundary_mesh = _build_boundary_walls_mesh(data.boundary_xy)

    coverage, line_segments = compute_coverage(
        data,
        buildings_mesh if buildings_mesh.n_blocks > 0 else None,
        ferry_mesh if ferry_mesh is not None and ferry_mesh.n_blocks > 0 else None,
        boundary_mesh if boundary_mesh.n_points > 0 else None,
    )
    coverage_result = (coverage, line_segments)
    store_coverage_result(data, signature, coverage_result)
    return coverage_result


def compute_coverage_result(
    data: OSMData,
) -> tuple[tuple, tuple[CoverageGrid, list[tuple[np.ndarray, np.ndarray, float]]]]:
    """Compute coverage for the current data state and return its cache key."""

    signature = coverage_signature(data)
    buildings_mesh = _build_buildings_mesh(data.buildings)
    ferry_meshes = build_ferry_meshes(data)
    ferry_mesh = ferry_meshes.get("ferry_body")
    boundary_mesh = _build_boundary_walls_mesh(data.boundary_xy)
    coverage, line_segments = compute_coverage(
        data,
        buildings_mesh if buildings_mesh.n_blocks > 0 else None,
        ferry_mesh if ferry_mesh is not None and ferry_mesh.n_blocks > 0 else None,
        boundary_mesh if boundary_mesh.n_points > 0 else None,
    )
    return signature, (coverage, line_segments)


def build_ray_meshes(data: OSMData) -> dict[str, pv.PolyData]:
    """Trace antenna rays and return a colored line mesh per tower."""

    if not any(tower.enabled for tower in data.towers):
        return {"radio_rays": pv.PolyData()}

    _coverage, line_segments = _ensure_coverage_cached(data)
    if not line_segments:
        return {"radio_rays": pv.PolyData()}

    points: list[tuple[float, float, float]] = []
    lines: list[int] = []
    scalars: list[float] = []
    for start, end, power_dbm in line_segments:
        index = len(points)
        points.append(tuple(start))
        points.append(tuple(end))
        lines.extend((2, index, index + 1))
        scalars.append(power_dbm)

    poly = pv.PolyData(
        np.array(points, dtype=np.float32),
        lines=np.array(lines, dtype=np.int64),
    )
    poly.cell_data["power_dbm"] = np.array(scalars, dtype=np.float32)
    return {"radio_rays": poly}


def build_coverage_slice_mesh(data: OSMData) -> dict[str, pv.PolyData]:
    """Build a flat colored slice of the voxel coverage grid at fixed Z."""

    if not any(tower.enabled for tower in data.towers):
        return {"coverage_slice": pv.PolyData()}

    coverage, _segments = _ensure_coverage_cached(data)
    return build_coverage_slice_mesh_for_grid(coverage, data.coverage_slice_z_m)


def build_coverage_slice_mesh_for_grid(
    coverage: CoverageGrid,
    z_m: float,
) -> dict[str, pv.PolyData]:
    """Build a flat colored slice from an already computed coverage grid."""

    z_target = float(z_m)
    minx, maxx, miny, maxy, zmin, zmax = coverage.bounds_xyz
    z_target = float(
        np.clip(
            z_target,
            zmin,
            zmax,
        )
    )
    slice_quality_db = coverage.quality_slice_at_z(z_target)
    render_z = z_target
    if np.isclose(render_z, zmin):
        render_z += COVERAGE_SLICE_RENDER_OFFSET_M

    nx, ny = slice_quality_db.shape
    voxel = coverage.voxel_size_m
    points: list[tuple[float, float, float]] = []
    faces: list[int] = []
    cell_values: list[float] = []
    for ix in range(nx):
        for iy in range(ny):
            x0 = minx + ix * voxel
            y0 = miny + iy * voxel
            x1 = x0 + voxel
            y1 = y0 + voxel
            base = len(points)
            points.extend(
                [
                    (x0, y0, render_z),
                    (x1, y0, render_z),
                    (x1, y1, render_z),
                    (x0, y1, render_z),
                ]
            )
            faces.extend((4, base, base + 1, base + 2, base + 3))
            cell_values.append(float(slice_quality_db[ix, iy]))

    poly = pv.PolyData(
        np.array(points, dtype=np.float32),
        faces=np.array(faces, dtype=np.int64),
    )
    poly.cell_data["quality_snr_db"] = np.array(cell_values, dtype=np.float32)
    return {"coverage_slice": poly}


def coverage_power_range_dbm() -> tuple[float, float]:
    """Common min/max in dBm for ray colors."""

    return (max(RAY_POWER_CUTOFF_DBM, NOISE_FLOOR_DBM - 10.0), -40.0)


def coverage_quality_range_db() -> tuple[float, float]:
    """Common min/max in dB for the coverage quality map."""

    return (0.0, 60.0)


def _build_contour_mesh(contour_xy: list[tuple[float, float]]) -> pv.PolyData:
    if len(contour_xy) < 2:
        return pv.PolyData()

    points = np.array([(x, y, CONTOUR_Z) for x, y in contour_xy], dtype=np.float32)
    lines: list[int] = []
    for i in range(len(points)):
        lines.extend((2, i, (i + 1) % len(points)))
    return pv.PolyData(points, lines=np.array(lines, dtype=np.int64))


def _build_boundary_walls_mesh(boundary_xy: list[tuple[float, float]]) -> pv.PolyData:
    if len(boundary_xy) < 2:
        return pv.PolyData()

    points: list[tuple[float, float, float]] = []
    faces: list[int] = []
    for i, (x1, y1) in enumerate(boundary_xy):
        x2, y2 = boundary_xy[(i + 1) % len(boundary_xy)]
        start_index = len(points)
        points.extend(
            [
                (x1, y1, GROUND_Z),
                (x2, y2, GROUND_Z),
                (x2, y2, BOUNDARY_WALL_HEIGHT_M),
                (x1, y1, BOUNDARY_WALL_HEIGHT_M),
            ]
        )
        faces.extend((4, start_index, start_index + 1, start_index + 2, start_index + 3))

    return pv.PolyData(
        np.array(points, dtype=np.float32),
        faces=np.array(faces, dtype=np.int64),
    )


def _build_ground_plane(bounds_xy: tuple[float, float, float, float]) -> pv.PolyData:
    minx, miny, maxx, maxy = bounds_xy
    minx -= GROUND_MARGIN_M
    miny -= GROUND_MARGIN_M
    maxx += GROUND_MARGIN_M
    maxy += GROUND_MARGIN_M
    center = ((minx + maxx) / 2, (miny + maxy) / 2, GROUND_Z)
    return pv.Plane(
        center=center,
        direction=(0.0, 0.0, 1.0),
        i_size=maxx - minx,
        j_size=maxy - miny,
        i_resolution=1,
        j_resolution=1,
    )


def _union_bounds(
    first: tuple[float, float, float, float] | None,
    second: tuple[float, float, float, float] | None,
) -> tuple[float, float, float, float]:
    if first is None:
        return second or (0.0, 0.0, 0.0, 0.0)
    if second is None:
        return first
    return (
        min(first[0], second[0]),
        min(first[1], second[1]),
        max(first[2], second[2]),
        max(first[3], second[3]),
    )


def _bounds_from_points(
    points: list[tuple[float, float]],
) -> tuple[float, float, float, float] | None:
    if not points:
        return None
    xs = [x for x, _ in points]
    ys = [y for _, y in points]
    return (min(xs), min(ys), max(xs), max(ys))


def build_city_meshes(data: OSMData) -> dict[str, pv.DataSet]:
    """Produce named meshes that the scene layer will add to the plotter."""

    ground_bounds = _union_bounds(data.view_bounds_xy, data.bounds_xy)
    ground_bounds = _union_bounds(ground_bounds, _bounds_from_points(data.contour_xy))
    ground_bounds = _union_bounds(ground_bounds, _bounds_from_points(data.boundary_xy))
    return {
        "ground": _build_ground_plane(ground_bounds),
        "city_contour": _build_contour_mesh(data.contour_xy),
        "city_walls": _build_boundary_walls_mesh(data.boundary_xy),
        "buildings": _build_buildings_mesh(data.buildings),
        **_build_tower_visual_meshes(data.towers),
        **build_ferry_meshes(data),
        **build_uav_meshes(data),
        **build_wave_meshes(data),
    }
