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
        # Amsterdam: WGS84 to RD New and back
        (52.377956, 4.897070, CRS.from_epsg(4326), CRS.from_epsg(28992), 121626., 487900.),
        (121626., 487900., CRS.from_epsg(28992), CRS.from_epsg(4326), 52.377956, 4.897070),
        # Arnhem: RD New to ETRS89 and back
        (121626., 487900., CRS.from_epsg(28992), CRS.from_epsg(23031), 629221, 5804980),
        (629221., 5804980., CRS.from_epsg(23031), CRS.from_epsg(28992), 121626, 487900),
    ],
)
def test__convert_to_target_crs(x, y, from_crs, to_crs, expected_x, expected_y):
    """Test the conversion of a location to a different coordinate system."""
    # Arrange
    geo_location_to_convert = WPGeoLocation(x=x, y=y, coordinate_system=from_crs)

    # Act
    converted_location = geo_location_to_convert._convert_to_target_crs(to_crs)

    # Assert
    assert converted_location.coordinate_system == to_crs
    assert converted_location.x == pytest.approx(expected_x, rel=0.01)
    assert converted_location.y == pytest.approx(expected_y, rel=0.01)


@pytest.mark.parametrize(
    "x, y, crs, expected_result",
    [
        # Amsterdam: WGS84 to RD New and back
        (52.377956, 4.897070, CRS.from_epsg(4326), "x=northing, y=easting"),
        (121626., 487900., CRS.from_epsg(28992), "x=easting, y=northing"),
        # Arnhem: RD New to ETRS89 and back
        (121626., 487900., CRS.from_epsg(28992), "x=easting, y=northing"),
        (629221., 5804980., CRS.from_epsg(23031), "x=easting, y=northing"),
    ]
)
def test_x_y_order(x, y, crs, expected_result):
    """Test the x_y_as_northing_and_easting property."""
    # Arrange
    geo_location = WPGeoLocation(x=x, y=y, coordinate_system=crs)

    # Act
    result = geo_location.x_y_order

    # Assert
    assert result == expected_result
