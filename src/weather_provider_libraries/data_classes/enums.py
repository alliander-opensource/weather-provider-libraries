#!/usr/bin/env python

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

"""This module is responsible for various enumerations used in the library."""

from enum import Enum


class SupportedUnitSystem(str, Enum):
    """An enumeration of the supported unit systems."""

    ORIGINAL = "original"
    SI = "si"
    IMPERIAL = "imperial"
    METRIC = "metric"
    US = "us"
    HARMONIZED = "si"  # Harmonized is the same as SI


class DataStorageMode(str, Enum):
    """An enumeration of the different data storage modes that are supported by the project."""

    ARCHIVE = "Store in Archive only"
    CACHE = "Store in Cache only"
    COMPLETE = "Store in both Archive and Cache"
    NONE = "Do not store data"
