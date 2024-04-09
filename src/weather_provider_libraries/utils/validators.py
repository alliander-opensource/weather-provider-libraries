#!/usr/bin/env python

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

from datetime import UTC, datetime

import numpy as np

from weather_provider_libraries.data_classes.commons import GeoLocation
from weather_provider_libraries.data_classes.constants import DEFAULT_DATETIME_FORMAT, DEFAULT_TIMEDELTA_FORMAT


def validation_of_datetime64_elements(
    value_to_validate: np.datetime64 | np.timedelta64 | datetime,
) -> np.datetime64 | np.timedelta64:
    """Datetime field validation for the TimePeriod class."""
    if isinstance(value_to_validate, datetime):
        if not (
            value_to_validate.tzinfo is None
            or value_to_validate.utcoffset() is None
            or value_to_validate.utcoffset().total_seconds() == 0
        ):
            # Convert to UTC if not already, allowing for naive datetime objects:
            value_to_validate = value_to_validate.astimezone(UTC)

        # Make sure the datetime object is timezone naive and convert to np.datetime64:
        value_to_validate = value_to_validate.replace(tzinfo=None)
        return_value = np.datetime64(value_to_validate).astype(DEFAULT_DATETIME_FORMAT)
    else:
        return_value = (
            value_to_validate.astype(DEFAULT_DATETIME_FORMAT)
            if isinstance(value_to_validate, np.datetime64)
            else value_to_validate.astype(DEFAULT_TIMEDELTA_FORMAT)
        )
    return return_value


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
