#!/usr/bin/env python

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

import pytest
from pyproj import CRS
from weather_provider_libraries.utility_classes.location import WPGeoLocation


@pytest.mark.parametrize(
    "x, y, from_crs, to_crs, expected_x, expected_y",
    [
        (52.0, 4.0, CRS.from_epsg(4326), CRS.from_epsg(28992), 122244.0, 455662.0),
        (122244.0, 455662.0, CRS.from_epsg(28992), CRS.from_epsg(4326), 52.0, 4.0),
    ],
)
def test__convert_location_to_crs(x, y, from_crs, to_crs, expected_x, expected_y):
    """Test the conversion of a location to a different coordinate system."""
    # Arrange
    geo_location_to_convert = WPGeoLocation(x=x, y=y, coordinate_system=from_crs)

    # Act
    converted_location = geo_location_to_convert._convert_location_to_crs(to_crs)

    # Assert
    assert converted_location.coordinate_system == to_crs
    assert converted_location.x == expected_x
    assert converted_location.y == expected_y
