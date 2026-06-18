"""High-level helpers: load OSM and add meshes to a PyVista plotter."""

from __future__ import annotations

import math
from pathlib import Path

import pyvista as pv

from .builder import (
    build_city_meshes,
    build_coverage_slice_mesh,
    build_coverage_slice_mesh_for_grid,
    build_ray_meshes,
    coverage_quality_range_db,
    coverage_power_range_dbm,
)
from .osm_parser import Building, OSMData, Tower, parse_osm


STYLE = {
    "ground": {"color": "#2a2a2a", "opacity": 1.0},
    "city_contour": {"color": "#d0d4dc", "line_width": 5.0},
    "city_walls": {"color": "#48c7ff", "opacity": 0.0, "show_edges": False},
    "ferry_body": {"color": "#e3e6ec", "show_edges": True},
    "ferry_edges": {"color": "#3a4250", "line_width": 1.0},
    "uav_body": {"color": "#ff3366", "show_edges": True, "smooth_shading": True},
    "uav_edges": {"color": "#7a1630", "line_width": 1.0},
    "tower_waves_1": {"color": "#48c7ff", "opacity": 0.5, "line_width": 2.0},
    "tower_waves_2": {"color": "#ff7a45", "opacity": 0.5, "line_width": 2.0},
    "buildings": {"color": "#d0d4dc", "show_edges": False},
    "building_edges": {"color": "#606672", "line_width": 1.2},
    "tower_enabled": {"color": "#18b957", "show_edges": False, "smooth_shading": True},
    "tower_disabled": {"color": "#d84f4f", "show_edges": False, "smooth_shading": True},
    "tower_edges": {"color": "#36424a", "line_width": 1.0},
    "radio_rays": {"line_width": 1.5, "opacity": 0.85},
    "coverage_slice": {"opacity": 0.7, "show_edges": False},
}

RADIO_COLORMAP = "RdYlGn"
RADIO_RAYS_ACTOR = "radio_rays"
COVERAGE_SLICE_ACTOR = "coverage_slice"

PERIMETER_TOWER_OFFSET_M = 80.0
BOUNDARY_WALL_GAP_M = 60.0
PERIMETER_TOWER_HEIGHT_M = 367.0
PERIMETER_TOWER_RADIUS_M = 5.15
PERIMETER_TOWER_FOOTPRINT_POINTS = 24
PERIMETER_TOWER_NAME_PREFIX = "perimeter_tower_"
FERRY_PATH_X = -240.0
FERRY_PATH_MARGIN_M = 45.0
REMOVED_BUILDING_STRIP_X_MIN = -255.0
REMOVED_BUILDING_STRIP_X_MAX = -190.0
REMOVED_BUILDING_STRIP_EXTRA_X_MIN = -290.0
REMOVED_BUILDING_STRIP_EXTRA_X_MAX = -275.0
REMOVED_BUILDING_STRIP_EXTRA_Y_MIN = -160.0
REMOVED_BUILDING_STRIP_EXTRA_Y_MAX = -135.0


def _circle_footprint(
    center_xy: tuple[float, float],
    radius_m: float,
    point_count: int = PERIMETER_TOWER_FOOTPRINT_POINTS,
) -> list[tuple[float, float]]:
    cx, cy = center_xy
    return [
        (
            cx + math.cos(2.0 * math.pi * i / point_count) * radius_m,
            cy + math.sin(2.0 * math.pi * i / point_count) * radius_m,
        )
        for i in range(point_count)
    ]


def contour_bounds_for_data(data: OSMData) -> tuple[float, float, float, float]:
    minx, miny, maxx, maxy = data.view_bounds_xy or data.bounds_xy
    return (
        minx - PERIMETER_TOWER_OFFSET_M,
        miny - PERIMETER_TOWER_OFFSET_M,
        maxx + PERIMETER_TOWER_OFFSET_M,
        maxy + PERIMETER_TOWER_OFFSET_M,
    )


def contour_points_for_bounds(
    bounds_xy: tuple[float, float, float, float],
) -> list[tuple[float, float]]:
    minx, miny, maxx, maxy = bounds_xy
    return [
        (minx, miny),
        (maxx, miny),
        (maxx, maxy),
        (minx, maxy),
    ]


def expand_bounds(
    bounds_xy: tuple[float, float, float, float],
    margin_m: float,
) -> tuple[float, float, float, float]:
    minx, miny, maxx, maxy = bounds_xy
    return (
        minx - margin_m,
        miny - margin_m,
        maxx + margin_m,
        maxy + margin_m,
    )


def point_on_contour(
    bounds_xy: tuple[float, float, float, float],
    progress: float,
) -> tuple[float, float]:
    """Map progress in [0, 1) to a point on the rectangular contour.

    The path starts at the left midpoint. Progress values separated by 0.5 are
    opposite on the rectangle, which keeps the two tower sources symmetric.
    """

    minx, miny, maxx, maxy = bounds_xy
    width = maxx - minx
    height = maxy - miny
    center_y = (miny + maxy) / 2.0
    perimeter = 2.0 * (width + height)
    distance = (progress % 1.0) * perimeter
    path = (
        ((minx, center_y), (minx, maxy), height / 2.0),
        ((minx, maxy), (maxx, maxy), width),
        ((maxx, maxy), (maxx, center_y), height / 2.0),
        ((maxx, center_y), (maxx, miny), height / 2.0),
        ((maxx, miny), (minx, miny), width),
        ((minx, miny), (minx, center_y), height / 2.0),
    )

    for start, end, segment_length in path:
        if distance <= segment_length:
            if segment_length == 0:
                return start
            ratio = distance / segment_length
            return (
                start[0] + (end[0] - start[0]) * ratio,
                start[1] + (end[1] - start[1]) * ratio,
            )
        distance -= segment_length

    return minx, center_y


def set_perimeter_towers(data: OSMData, position: float = 0.0) -> None:
    """Place two generated towers on opposite sides of the city contour."""

    contour_bounds = contour_bounds_for_data(data)
    data.contour_xy = contour_points_for_bounds(contour_bounds)
    data.boundary_xy = contour_points_for_bounds(expand_bounds(contour_bounds, BOUNDARY_WALL_GAP_M))
    enabled_by_name = {
        tower.name: tower.enabled
        for tower in data.towers
        if (tower.name or "").startswith(PERIMETER_TOWER_NAME_PREFIX)
    }
    data.towers = [
        tower
        for tower in data.towers
        if not (tower.name or "").startswith(PERIMETER_TOWER_NAME_PREFIX)
    ]

    for index, tower_position in enumerate((position, position + 0.5), start=1):
        center = point_on_contour(contour_bounds, tower_position)
        footprint = _circle_footprint(center, PERIMETER_TOWER_RADIUS_M)
        data.towers.append(
            Tower(
                footprint=footprint,
                height_m=PERIMETER_TOWER_HEIGHT_M,
                name=f"{PERIMETER_TOWER_NAME_PREFIX}{index}",
                kind="communications_tower",
                tower_type="communication",
                construction="freestanding",
                enabled=enabled_by_name.get(f"{PERIMETER_TOWER_NAME_PREFIX}{index}", True),
            )
        )


def set_perimeter_tower_enabled(data: OSMData, tower_index: int, enabled: bool) -> None:
    tower_name = f"{PERIMETER_TOWER_NAME_PREFIX}{tower_index}"
    for tower in data.towers:
        if tower.name == tower_name:
            tower.enabled = enabled
            return


def _building_bbox(building: Building) -> tuple[float, float, float, float]:
    footprint = building.footprint
    xs = [x for x, _ in footprint]
    ys = [y for _, y in footprint]
    return min(xs), min(ys), max(xs), max(ys)


def _is_removed_building_strip(building: Building) -> bool:
    minx, _miny, maxx, _maxy = _building_bbox(building)
    if minx <= REMOVED_BUILDING_STRIP_X_MAX and maxx >= REMOVED_BUILDING_STRIP_X_MIN:
        return True

    footprint = building.footprint
    center_x = sum(x for x, _ in footprint) / len(footprint)
    center_y = sum(y for _, y in footprint) / len(footprint)
    return (
        REMOVED_BUILDING_STRIP_EXTRA_X_MIN <= center_x <= REMOVED_BUILDING_STRIP_EXTRA_X_MAX
        and REMOVED_BUILDING_STRIP_EXTRA_Y_MIN <= center_y <= REMOVED_BUILDING_STRIP_EXTRA_Y_MAX
    )


def remove_city_building_strip(data: OSMData) -> None:
    data.buildings = [
        building for building in data.buildings if not _is_removed_building_strip(building)
    ]


def set_ferry_path(data: OSMData) -> None:
    _minx, miny, _maxx, maxy = data.view_bounds_xy or data.bounds_xy
    data.ferry_path_x = FERRY_PATH_X
    data.ferry_path_y_bounds = (
        miny - FERRY_PATH_MARGIN_M,
        maxy + FERRY_PATH_MARGIN_M,
    )
    if data.contour_xy:
        contour_ys = [y for _, y in data.contour_xy]
        data.ferry_clip_y_bounds = (min(contour_ys), max(contour_ys))


def build_city_scene(
    osm_path: str | Path,
    tower_position: float = 0.0,
) -> tuple[OSMData, dict[str, pv.DataSet]]:
    """Parse the OSM file and build meshes in one step."""

    data = parse_osm(osm_path)
    remove_city_building_strip(data)
    if data.buildings and not data.towers:
        set_perimeter_towers(data, tower_position)
    set_ferry_path(data)
    meshes = build_city_meshes(data)
    return data, meshes


def add_city_to_plotter(plotter: pv.Plotter, meshes: dict[str, pv.DataSet]) -> None:
    """Attach city meshes to the plotter using the default style."""

    ground = meshes.get("ground")
    if ground is not None and ground.n_points > 0:
        plotter.add_mesh(ground, name="ground", **STYLE["ground"])

    city_contour = meshes.get("city_contour")
    if city_contour is not None and city_contour.n_points > 0:
        plotter.add_mesh(
            city_contour,
            name="city_contour",
            render_lines_as_tubes=True,
            **STYLE["city_contour"],
        )

    city_walls = meshes.get("city_walls")
    if city_walls is not None and city_walls.n_points > 0:
        plotter.add_mesh(city_walls, name="city_walls", **STYLE["city_walls"])

    buildings = meshes.get("buildings")
    if buildings is not None and buildings.n_blocks > 0:
        plotter.add_mesh(buildings, name="buildings", **STYLE["buildings"])
        for i, block in enumerate(buildings):
            if block is None or block.n_points == 0:
                continue
            edges = block.extract_feature_edges(
                boundary_edges=False,
                feature_edges=True,
                manifold_edges=False,
                non_manifold_edges=False,
                feature_angle=30.0,
            )
            if edges.n_points > 0:
                plotter.add_mesh(edges, name=f"building_edges_{i}", **STYLE["building_edges"])

    for mesh_name in ("tower_enabled", "tower_disabled"):
        tower_mesh = meshes.get(mesh_name)
        if tower_mesh is None or tower_mesh.n_blocks == 0:
            continue
        plotter.add_mesh(tower_mesh, name=mesh_name, **STYLE[mesh_name])
        for i, block in enumerate(tower_mesh):
            if block is None or block.n_points == 0:
                continue
            edges = block.extract_feature_edges(
                boundary_edges=False,
                feature_edges=True,
                manifold_edges=False,
                non_manifold_edges=False,
                feature_angle=30.0,
            )
            if edges.n_points > 0:
                plotter.add_mesh(edges, name=f"{mesh_name}_edges_{i}", **STYLE["tower_edges"])

    ferry_body = meshes.get("ferry_body")
    if ferry_body is not None and ferry_body.n_blocks > 0:
        plotter.add_mesh(ferry_body, name="ferry_body", **STYLE["ferry_body"])
        for i, block in enumerate(ferry_body):
            if block is None or block.n_points == 0:
                continue
            edges = block.extract_feature_edges(
                boundary_edges=False,
                feature_edges=True,
                manifold_edges=False,
                non_manifold_edges=False,
                feature_angle=30.0,
            )
            if edges.n_points > 0:
                plotter.add_mesh(edges, name=f"ferry_edges_{i}", **STYLE["ferry_edges"])

    uav_body = meshes.get("uav_body")
    if uav_body is not None and uav_body.n_blocks > 0:
        plotter.add_mesh(uav_body, name="uav_body", **STYLE["uav_body"])
        for i, block in enumerate(uav_body):
            if block is None or block.n_points == 0:
                continue
            edges = block.extract_feature_edges(
                boundary_edges=False,
                feature_edges=True,
                manifold_edges=False,
                non_manifold_edges=False,
                feature_angle=30.0,
            )
            if edges.n_points > 0:
                plotter.add_mesh(edges, name=f"uav_edges_{i}", **STYLE["uav_edges"])

    for mesh_name in ("tower_waves_1", "tower_waves_2"):
        tower_waves = meshes.get(mesh_name)
        if tower_waves is not None and tower_waves.n_points > 0:
            plotter.add_mesh(
                tower_waves,
                name=mesh_name,
                render_lines_as_tubes=True,
                **STYLE[mesh_name],
            )


def remove_actor_if_present(plotter: pv.Plotter, name: str) -> None:
    if name in plotter.actors:
        plotter.remove_actor(name, render=False)


def add_radio_rays(plotter: pv.Plotter, data: OSMData) -> None:
    remove_actor_if_present(plotter, RADIO_RAYS_ACTOR)
    rays = build_ray_meshes(data).get("radio_rays")
    if rays is None or rays.n_points == 0:
        return
    plotter.add_mesh(
        rays,
        name=RADIO_RAYS_ACTOR,
        scalars="power_dbm",
        cmap=RADIO_COLORMAP,
        clim=coverage_power_range_dbm(),
        show_scalar_bar=False,
        **STYLE["radio_rays"],
    )


def add_coverage_slice(plotter: pv.Plotter, data: OSMData) -> None:
    remove_actor_if_present(plotter, COVERAGE_SLICE_ACTOR)
    slice_mesh = build_coverage_slice_mesh(data).get("coverage_slice")
    if slice_mesh is None or slice_mesh.n_points == 0:
        return
    plotter.add_mesh(
        slice_mesh,
        name=COVERAGE_SLICE_ACTOR,
        scalars="quality_snr_db",
        cmap=RADIO_COLORMAP,
        clim=coverage_quality_range_db(),
        scalar_bar_args={"title": "SNR, дБ"},
        **STYLE["coverage_slice"],
    )


def add_coverage_result_slice(
    plotter: pv.Plotter,
    coverage_result: object,
    z_m: float,
) -> None:
    """Draw a coverage slice from an already computed result without recomputing."""

    remove_actor_if_present(plotter, COVERAGE_SLICE_ACTOR)
    if not isinstance(coverage_result, tuple) or not coverage_result:
        return

    coverage = coverage_result[0]
    slice_mesh = build_coverage_slice_mesh_for_grid(coverage, z_m).get("coverage_slice")
    if slice_mesh is None or slice_mesh.n_points == 0:
        return
    plotter.add_mesh(
        slice_mesh,
        name=COVERAGE_SLICE_ACTOR,
        scalars="quality_snr_db",
        cmap=RADIO_COLORMAP,
        clim=coverage_quality_range_db(),
        scalar_bar_args={"title": "SNR, дБ"},
        **STYLE["coverage_slice"],
    )
