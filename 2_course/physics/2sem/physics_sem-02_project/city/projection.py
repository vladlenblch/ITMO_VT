"""Lat/lon to local meters projection.

Equirectangular projection relative to a reference point. For the small areas
we work with (a few hundred meters across) the distortion is negligible.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


EARTH_RADIUS_M = 6_378_137.0


@dataclass(frozen=True)
class Projection:
    """Projects (lat, lon) in degrees to local (x, y) meters.

    X axis points east, Y axis points north. The reference point maps to (0, 0).
    """

    ref_lat: float
    ref_lon: float

    def to_xy(self, lat: float, lon: float) -> tuple[float, float]:
        ref_lat_rad = math.radians(self.ref_lat)
        x = math.radians(lon - self.ref_lon) * EARTH_RADIUS_M * math.cos(ref_lat_rad)
        y = math.radians(lat - self.ref_lat) * EARTH_RADIUS_M
        return x, y
