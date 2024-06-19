#!/usr/bin/env python

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-{2024}} Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

from pyproj import CRS, Transformer
from pyproj.aoi import BBox


def validate_crs(crs: CRS | int) -> CRS:
    """Check if the given CRS is valid."""
    if isinstance(crs, int):
        crs = CRS.from_epsg(crs)
    if not isinstance(crs, CRS):
        raise TypeError(f"Expected a CRS or int, got {type(crs)}")

    return crs


def is_x_y_order_northing_easting(crs: CRS | int) -> bool:
    """Check if the x and y order for the given CRS is northing and easting."""
    crs = validate_crs(crs)
    return crs.axis_info[0].direction == "north" and crs.axis_info[1].direction == "east"


def get_x_y_order_northing_easting_as_string(crs: CRS | int) -> str:
    """Get the x and y order from the coordinate reference system.

    The result is returned as a string indicating if x is northing and y easting or vice versa.
    """
    if is_x_y_order_northing_easting(crs):
        return "x=northing, y=easting"
    return "x=easting, y=northing"


def translate_coordinate_to_wgs84(x: float, y: float, original_crs: CRS | int) -> tuple[float, float]:
    """Translate the given coordinates to WGS84."""
    original_crs = validate_crs(original_crs)

    transformer = Transformer.from_crs(original_crs, "EPSG:4326")
    return transformer.transform(x, y)


def is_coordinate_withing_target_crs_boundaries(
    x: float, y: float, original_crs: CRS | int, target_crs: CRS | int
) -> bool:
    """Check if the given coordinates lie within the bounds of the given CRS."""
    original_crs = validate_crs(original_crs)
    target_crs = validate_crs(target_crs)

    wgs84_x, wgs84_y = (x, y) if original_crs.to_epsg() == 4326 else translate_coordinate_to_wgs84(x, y, original_crs)

    west_bound, south_bound, east_bound, north_bound = target_crs.area_of_use.bounds

    if is_x_y_order_northing_easting(target_crs):
        north_south_value, east_west_value = wgs84_y, wgs84_x
    else:
        north_south_value, east_west_value = wgs84_x, wgs84_y

    if west_bound <= east_west_value <= east_bound and south_bound <= north_south_value <= north_bound:
        return True

    return False


def convert_coordinate_to_crs(x: float, y: float, current_crs: CRS | int, target_crs: CRS | int) -> tuple[float, float]:
    """Convert the given coordinates from one CRS to another."""
    current_crs = validate_crs(current_crs)
    target_crs = validate_crs(target_crs)

    wgs84_x, wgs84_y = (x, y) if current_crs.to_epsg() == 4326 else translate_coordinate_to_wgs84(x, y, current_crs)

    if not is_coordinate_withing_target_crs_boundaries(wgs84_x, wgs84_y, CRS.from_epsg(4326), target_crs):
        raise ValueError(f"The location lies outside the bounds of the target coordinate system: {target_crs}")

    transformer = Transformer.from_crs(CRS.from_epsg(4326), target_crs)

    return transformer.transform(wgs84_x, wgs84_y)


def convert_box_from_crs_to_crs(bbox: BBox, original_crs: CRS, target_crs: CRS) -> BBox:
    """Convert the given bounding box from one CRS to another."""
    original_crs = validate_crs(original_crs)
    target_crs = validate_crs(target_crs)

    if not is_coordinate_withing_target_crs_boundaries(bbox.west, bbox.south, original_crs, target_crs):
        raise ValueError("The location lies outside the bounds of the target coordinate system")

    if not is_coordinate_withing_target_crs_boundaries(bbox.east, bbox.north, original_crs, target_crs):
        raise ValueError("The location lies outside the bounds of the target coordinate system")

    transformer = Transformer.from_crs(original_crs, target_crs)

    return BBox(*transformer.transform(bbox.west, bbox.south, bbox.east, bbox.north))
