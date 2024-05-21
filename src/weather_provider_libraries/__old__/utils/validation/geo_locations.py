#!/usr/bin/env python

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

from weather_provider_libraries.data_classes.commons import GeoLocation


def validation_of_list_of_geo_locations(list_of_locations: list[GeoLocation]):
    """Validate a list of GeoLocation objects.

    Args:
        list_of_locations (list[GeoLocation]):
            The list of GeoLocation objects to validate.
    """
    for location in list_of_locations:
        if not location.is_valid:
            raise ValueError(
                f"Invalid GeoLocation object in supplied list: "
                f"({location.longitude}, {location.latitude}) {location.coordinate_system}"
            )
