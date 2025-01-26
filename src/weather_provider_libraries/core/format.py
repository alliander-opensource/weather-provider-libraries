#!/usr/bin/env python

#  SPDX-FileCopyrightText: 2019-2025 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0

from enum import StrEnum
from pathlib import Path

import xarray as xr
from pydantic import BaseModel, ConfigDict


class UnitSystem(StrEnum):
    """An enumeration class for the unit systems supported by the WPAS libraries."""

    ORIGINAL = "original"  # Use the originally supplied unit system for the data
    ECCODES = "eccodes"  # Use the eccodes default unit system for the data
    IMPERIAL = "imperial"  # Use the imperial unit system for the data
    METRIC = "metric"  # Use the metric unit system for the data
    SI = "si"  # Use the SI unit system for the data


class FileFormat(StrEnum):
    """The enumeration class for the file formats supported by the WPAS libraries."""

    CSV = "csv"  # Comma-separated values
    CSV_SEMICOLON = "csv_semicolon"  # CSV with a semicolon separator instead (European standard)
    JSON = "json"  # JavaScript Object Notation - Regular JSON
    JSON_DATASET = "json_dataset"  # JSON with a dataset structure
    NETCDF3 = "netcdf3"  # NetCDF3 format
    NETCDF4 = "netcdf4"  # NetCDF4 format


class Format(BaseModel):
    """A basemodel dataclass for specifying a file format and unit system for weather data."""

    model_config = ConfigDict(...)

    # required fields
    unit_system: UnitSystem
    file_format: FileFormat

    # optional fields
    use_original_naming: bool = False


def weather_data_to_file(weather_data: xr.Dataset, file_format: FileFormat) -> Path:
    """Transform Xarray formatted weather data to a file response in the specified format."""
    file_path = Path(...)
    return file_path
