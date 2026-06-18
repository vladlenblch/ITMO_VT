"""City scene package: OSM parsing and 3D construction.

Heavy dependencies (pyvista) are imported lazily so that the parser module
can be used without a GUI stack installed.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .osm_parser import OSMData, Tower, parse_osm

if TYPE_CHECKING:
    from .scene import (
        add_city_to_plotter,
        add_coverage_slice,
        add_coverage_result_slice,
        add_radio_rays,
        build_city_scene,
        remove_actor_if_present,
    )

__all__ = [
    "OSMData",
    "Tower",
    "add_city_to_plotter",
    "add_coverage_result_slice",
    "add_coverage_slice",
    "add_radio_rays",
    "build_city_scene",
    "parse_osm",
    "remove_actor_if_present",
]

_LAZY_SCENE_ATTRS = {
    "add_city_to_plotter",
    "add_coverage_result_slice",
    "add_coverage_slice",
    "add_radio_rays",
    "build_city_scene",
    "remove_actor_if_present",
}


def __getattr__(name: str) -> Any:
    if name in _LAZY_SCENE_ATTRS:
        from . import scene

        return getattr(scene, name)
    raise AttributeError(f"module 'city' has no attribute {name!r}")
