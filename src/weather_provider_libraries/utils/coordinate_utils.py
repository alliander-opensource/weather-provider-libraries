#!/usr/bin/env python

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

from pyproj import CRS, Transformer


def validate_crs(crs: CRS | int) -> CRS:
    """Check if the given CRS is valid."""
    if isinstance(crs, int):
        crs = CRS.from_epsg(crs)
    if not isinstance(crs, CRS):
        raise TypeError(f"Expected a CRS or int, got {type(crs)}")

    return crs


def get_xy_order_from_crs(crs: CRS | int) -> str:
    """Get the x and y order from the coordinate reference system.

    The result is returned as a string indicating if x is northing and y easting or vice versa.
    """
    crs = validate_crs(crs)

    return f"x={CRS(crs).axis_info[0].direction}ing, y={CRS(crs).axis_info[1].direction}ing"


def convert_coordinate_to_wgs84(x: float, y: float) -> tuple[float, float]:
    """Convert the given coordinates to WGS84."""
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:4326")
    return transformer.transform(x, y)

def do_coordinates_lie_within_bounds(x: float, y: float, crs: CRS | int) -> bool:
    """Check if the given coordinates lie within the bounds of the given CRS."""
    crs = validate_crs(crs)

    wgs84_x, wgs84_y = convert_coordinate_to_wgs84(x, y)
    west_bound, south_bound, east_bound, north_bound = crs.area_of_use.bounds

    # Verify the order of the x and y coordinates for proper area of use comparison
    if get_xy_order_from_crs(crs) == f"x=northing, y=easting":
        north_south_value, east_west_value = wgs84_x, wgs84_y
    else:
        north_south_value, east_west_value = wgs84_y, wgs84_x

    if west_bound <= east_west_value <= east_bound and south_bound <= north_south_value <= north_bound:
        return True

    return False


def convert_coordinates_from_crs_to_other_crs(x: float, y: float, from_crs: CRS | int, to_crs: CRS | int) -> tuple[
    float, float]:
    """Convert the given coordinates from one CRS to another."""
    from_crs = validate_crs(from_crs)
    to_crs = validate_crs(to_crs)

    # Conversion to WGS84 for boundary check and conversion stabilization
    wgs84_x, wgs84_y = convert_coordinate_to_wgs84(x, y)

    if not self._coordinate_within_bounds(to_crs):
        raise ValueError(f"The location lies outside the bounds of the target coordinate system: {to_crs}")

    transformer = Transformer.from_crs(CRS.from_epsg(4326), to_crs)

    return transformer.transform(wgs84_x, wgs84_y)
