#!/usr/bin/env python

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

from enum import Enum


class WPDataStorageMode(str, Enum):
    """An enumeration representing the available storage modes for data."""

    ARCHIVE = "Data is stored based on TimePeriod in an ARCHIVE folder."
    CACHE = "Data is stored in a CACHE folder based on a size limit."
    COMPLETE = (
        "Data is stored in both an ARCHIVE folder based on a TimePeriod and a CACHE folder based on a size limit."
    )
    NONE = "Data is not stored at all and can only be accessed directly via (ticketed) request."


class SupportedUnitSystem(str, Enum):
    """An enumeration of the supported unit systems."""

    ORIGINAL = "original"
    SI = "si"
    IMPERIAL = "imperial"
    METRIC = "metric"
    US = "us"
    HARMONIZED = "si"  # Harmonized is the same as SI
