#!/usr/bin/env python

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-{2024}} Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

from datetime import UTC, datetime

import numpy as np

# Harmonize to minute resolution
HARMONIZED_DATETIME_FORMAT = "datetime64[m]"
HARMONIZED_TIMEDELTA_FORMAT = "timedelta64[m]"


def translate_datetime_to_np_datetime64(datetime_to_translate: datetime) -> np.datetime64:
    """Translate a datetime object to a numpy datetime64 object."""
    if not isinstance(datetime_to_translate, datetime):
        raise ValueError(f"Expected a datetime object, but got {type(datetime_to_translate)}.")

    if not (
        datetime_to_translate.tzinfo is None
        or datetime_to_translate.utcoffset() is None
        or datetime_to_translate.utcoffset().total_seconds() == 0
    ):
        # Convert to UTC if not already, allowing for naive datetime objects:
        datetime_to_translate = datetime_to_translate.astimezone(UTC)

    # Make sure the datetime object is timezone naive and convert to np.datetime64:
    naive_datetime_to_translate = datetime_to_translate.replace(tzinfo=None)

    return np.datetime64(naive_datetime_to_translate).astype(HARMONIZED_DATETIME_FORMAT)
