"""Minimal OSM XML parser tailored for the city visualization.

We only extract what the 3D scene needs:
- buildings (closed ways with a ``building`` tag) with optional height/levels;
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path

from .projection import Projection


DEFAULT_LEVEL_HEIGHT_M = 3.0
DEFAULT_BUILDING_HEIGHT_M = 9.0  # fallback if no tags provided
DEFAULT_COVERAGE_VOXEL_SIZE_M = 15.0
UAV_FLIGHT_ALTITUDE_M = 120.0
UAV_ACTIVE_SECONDS = 10.0
UAV_JAM_POWER_DBM = 20.0


@dataclass
class Building:
    """Building footprint with vertical extent in local meters."""

    footprint: list[tuple[float, float]]
    height_m: float
    kind: str = "building"


@dataclass
class Tower:
    """Communication tower footprint with parsed OSM metadata."""

    footprint: list[tuple[float, float]]
    height_m: float
    name: str | None = None
    kind: str = "tower"
    tower_type: str | None = None
    construction: str | None = None
    operator: str | None = None
    enabled: bool = True


@dataclass
class OSMData:
    """Projected OSM features ready for mesh building."""

    projection: Projection
    bounds_xy: tuple[float, float, float, float]  # (minx, miny, maxx, maxy)
    # Projected rectangle of the original <bounds> element, if present.
    # Useful as a viewport/ground rectangle when features extend far outside.
    view_bounds_xy: tuple[float, float, float, float] | None = None
    buildings: list[Building] = field(default_factory=list)
    towers: list[Tower] = field(default_factory=list)
    contour_xy: list[tuple[float, float]] = field(default_factory=list)
    boundary_xy: list[tuple[float, float]] = field(default_factory=list)
    ferry_path_x: float | None = None
    ferry_path_y_bounds: tuple[float, float] | None = None
    ferry_clip_y_bounds: tuple[float, float] | None = None
    ferry_enabled: bool = True
    ferry_progress: float = 0.0
    uav_enabled: bool = True
    uav_active: bool = False
    uav_progress: float = 0.0
    uav_flight_time_s: float = 0.0
    wave_phase_m: float = 0.0
    tower_wave_phases_m: dict[str, float] = field(default_factory=dict)
    ray_count: int = 1500
    ray_max_bounces: int = 2
    voxel_size_m: float = DEFAULT_COVERAGE_VOXEL_SIZE_M
    coverage_slice_z_m: float = 0.0
    coverage_grid: object | None = None
    coverage_signature: tuple = ()
    coverage_cache: dict[tuple, object] = field(default_factory=dict)
    coverage_cache_order: list[tuple] = field(default_factory=list)


def _parse_height(tags: dict[str, str]) -> float:
    raw_height = tags.get("height")
    if raw_height is not None:
        try:
            return float(raw_height.split()[0])
        except ValueError:
            pass
    raw_levels = tags.get("building:levels")
    if raw_levels is not None:
        try:
            return float(raw_levels) * DEFAULT_LEVEL_HEIGHT_M
        except ValueError:
            pass
    return DEFAULT_BUILDING_HEIGHT_M


def _way_tags(way: ET.Element) -> dict[str, str]:
    return {t.attrib["k"]: t.attrib["v"] for t in way.findall("tag")}


def _way_node_ids(way: ET.Element) -> list[str]:
    return [nd.attrib["ref"] for nd in way.findall("nd")]


def _is_tower(tags: dict[str, str]) -> bool:
    return (
        tags.get("building") == "tower"
        or tags.get("man_made") in {"communications_tower", "tower", "mast"}
        or tags.get("tower:type") is not None
    )


def parse_osm(path: str | Path) -> OSMData:
    """Parse an OSM XML file and return projected features.

    The projection reference point is the center of the ``<bounds>`` element
    when present, otherwise the mean of all node coordinates.
    """

    tree = ET.parse(path)
    root = tree.getroot()

    nodes: dict[str, tuple[float, float]] = {}
    for node in root.findall("node"):
        try:
            nodes[node.attrib["id"]] = (
                float(node.attrib["lat"]),
                float(node.attrib["lon"]),
            )
        except (KeyError, ValueError):
            continue

    bounds = root.find("bounds")
    bounds_latlon: tuple[float, float, float, float] | None = None
    if bounds is not None:
        minlat = float(bounds.attrib["minlat"])
        maxlat = float(bounds.attrib["maxlat"])
        minlon = float(bounds.attrib["minlon"])
        maxlon = float(bounds.attrib["maxlon"])
        bounds_latlon = (minlat, minlon, maxlat, maxlon)
        ref_lat = (minlat + maxlat) / 2
        ref_lon = (minlon + maxlon) / 2
    elif nodes:
        ref_lat = sum(lat for lat, _ in nodes.values()) / len(nodes)
        ref_lon = sum(lon for _, lon in nodes.values()) / len(nodes)
    else:
        ref_lat, ref_lon = 0.0, 0.0
    projection = Projection(ref_lat=ref_lat, ref_lon=ref_lon)

    nodes_xy: dict[str, tuple[float, float]] = {
        node_id: projection.to_xy(lat, lon) for node_id, (lat, lon) in nodes.items()
    }

    buildings: list[Building] = []
    towers: list[Tower] = []
    for way in root.findall("way"):
        ids = _way_node_ids(way)
        if len(ids) < 2:
            continue
        path_xy = [nodes_xy[i] for i in ids if i in nodes_xy]
        if len(path_xy) < 2:
            continue

        tags = _way_tags(way)

        if _is_tower(tags) and len(path_xy) >= 3:
            footprint = path_xy[:-1] if path_xy[0] == path_xy[-1] else path_xy
            towers.append(
                Tower(
                    footprint=footprint,
                    height_m=_parse_height(tags),
                    name=tags.get("name:en") or tags.get("name"),
                    kind=tags.get("man_made") or tags.get("building", "tower"),
                    tower_type=tags.get("tower:type"),
                    construction=tags.get("tower:construction"),
                    operator=tags.get("operator"),
                )
            )
            continue

        if "building" in tags and len(path_xy) >= 3:
            footprint = path_xy[:-1] if path_xy[0] == path_xy[-1] else path_xy
            buildings.append(
                Building(
                    footprint=footprint,
                    height_m=_parse_height(tags),
                    kind=tags.get("building", "yes"),
                )
            )
            continue

    feature_points: list[tuple[float, float]] = []
    for b in buildings:
        feature_points.extend(b.footprint)
    for tower in towers:
        feature_points.extend(tower.footprint)

    if feature_points:
        xs = [p[0] for p in feature_points]
        ys = [p[1] for p in feature_points]
        bounds_xy = (min(xs), min(ys), max(xs), max(ys))
    elif nodes_xy:
        xs = [p[0] for p in nodes_xy.values()]
        ys = [p[1] for p in nodes_xy.values()]
        bounds_xy = (min(xs), min(ys), max(xs), max(ys))
    else:
        bounds_xy = (0.0, 0.0, 0.0, 0.0)

    view_bounds_xy: tuple[float, float, float, float] | None = None
    if bounds_latlon is not None:
        minlat, minlon, maxlat, maxlon = bounds_latlon
        min_xy = projection.to_xy(minlat, minlon)
        max_xy = projection.to_xy(maxlat, maxlon)
        view_bounds_xy = (min_xy[0], min_xy[1], max_xy[0], max_xy[1])

    return OSMData(
        projection=projection,
        bounds_xy=bounds_xy,
        view_bounds_xy=view_bounds_xy,
        buildings=buildings,
        towers=towers,
    )
