#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

""" This ... """
from pyproj import CRS, Transformer


def generate_size_string_from_value(size: int | float, bytesize: str, decimals: int = 2):
    bytesize_range = ["B", "KB", "MB", "GB", "TB", "EB"]
    if bytesize not in bytesize_range:
        raise ValueError(f"Cannot generate bytesize string. Please supply a valid bytesize indicator: {bytesize_range}")

    step_in_range = bytesize_range.index(bytesize)
    while size > 1024 or size < 1:
        if size > 1024:
            step_in_range += 1
            size = size / 1024
        if size < 1:
            step_in_range -= 1
            size = size * 1024

    return f"{size:.{decimals}f}{bytesize_range[step_in_range]}"


def does_coordinate_lie_within_crs(crs: CRS, coordinate: tuple[float, float]) -> bool:
    """This method references a coordinate for a given CRS to the officially known area of use and returns a boolean
     indicating if the coordinate lies within that area of use.

    Args:
        crs (CRS): The CRS coordinate system that the coordinate is formatted in, and the system it should be
                    referenced to.
        coordinate (tuple[float, float]): A tuple containing the x,y or lat, lon formatted coordinate to verify. The
                    first value is always assumed to be of an east/west nature, while the second value is always
                    assumed to be of a north/south nature.

    Returns:
        bool: Returns True if the coordinate lies within the given crs' bounding box, False otherwise

    """
    transformer = Transformer.from_crs(crs.geodetic_crs, crs, always_xy=True)
    crs_formatted_bounds = transformer.transform_bounds(*crs.area_of_use.bounds)

    coordinate_within_bounds = (
        crs_formatted_bounds[0] <= coordinate[0] <= crs_formatted_bounds[2]
        and crs_formatted_bounds[1] <= coordinate[1] <= crs_formatted_bounds[3]
    )
    return coordinate_within_bounds


def transform_coordinates_between_crs(
    coordinate: tuple[float, float], source_crs: CRS, target_crs: CRS
) -> tuple[float, float]:
    """Transform a coordinate from a source CRS projection into a target CRS projection.

    Args:
        coordinate (tuple[float, float]): The coordinate to transform.
        source_crs (CRS): The CRS the coordinate will be transformed from.
        target_crs (CRS): The CRS the coordinate will be transformed to.

    Returns:
        (tuple[float, float]): If successful, the transformed coordinate will be returned.

    Raises:
        ValueError: If the coordinate either lies outside the source CRS bounds before the transformation or it lies
                     outside the target CRS bounds after the transformation, a ValueError will be raised.

    """
    # Evaluate parameters
    if not isinstance(coordinate, tuple) or not isinstance(source_crs, CRS) or not isinstance(target_crs, CRS):
        raise TypeError(
            "Wrong parameters were passed to the transform_coordinates_between_crs() method. "
            "Expected: coordinate=tuple[float,float], source_crs=CRS, target_crs=CRS || "
            f"Received: coordinate={type(coordinate)}, source_crs={type(source_crs)}, "
            f"target_crs={type(target_crs)}"
        )

    if (
        len(coordinate) != 2
        or (not isinstance(coordinate[0], float) and not isinstance(coordinate[0], int))
        or (not isinstance(coordinate[1], float) and not isinstance(coordinate[1], int))
    ):
        raise ValueError(
            "Wrong coordinate parameters were passed to the transform_coordinates_between_crs() method. "
            "A tuple holding only two float values is expected."
        )

    # Transform
    if not does_coordinate_lie_within_crs(source_crs, coordinate):
        raise ValueError(
            f"Could not transform coordinate ({coordinate[0]}, {coordinate[1]}). "
            f"The coordinate lies outside of the bounds of the source crs!"
        )

    transformer = Transformer.from_crs(source_crs, target_crs, always_xy=True)
    transformed_coordinate = transformer.transform(coordinate[0], coordinate[1])

    if not does_coordinate_lie_within_crs(target_crs, transformed_coordinate):
        raise ValueError(
            f"Could transform coordinate ({coordinate[0]}, {coordinate[1]}), "
            f"but the new coordinate lies outside of the bounds of the target crs!"
        )

    return transformed_coordinate
