#!/usr/bin/env python

#  SPDX-FileCopyrightText: 2019-2025 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0

import xarray as xr

from weather_provider_libraries.core.format import FileFormat


def convert_xarray_to_file_format(base_data: xr.Dataset, file_format: FileFormat, flatten_to_v2: bool = False):
    """Convert a xarray DataSet to a file format.

    This function converts a xarray DataSet to a file format specified by the file_format parameter.

    Args:
    ----
        base_data (xr.Dataset):
                The Xarray Dataset to convert to the given file format.
        file_format (FileFormat):
                The file format to convert the xarray DataSet to.
        flatten_to_v2 (bool):
                The old V2 format would have multi-level factors flattened into separate factors even if the output
                 format is not a flat file format. This is useful for compatibility with older systems.

    """
    if not isinstance(file_format, FileFormat):
        raise ValueError(f"Invalid file format '{file_format}'.")

    if file_format == FileFormat.CSV:
        return _convert_xarray_to_csv(base_data, use_semicolon_separator=False, flatten_to_v2=flatten_to_v2)
    if file_format == FileFormat.CSV_SEMICOLON:
        return _convert_xarray_to_csv(base_data, use_semicolon_separator=True, flatten_to_v2=flatten_to_v2)
    if file_format == FileFormat.JSON:
        return _convert_xarray_to_json(base_data, dataset_structure=False, flatten_to_v2=flatten_to_v2)
    if file_format == FileFormat.JSON_DATASET:
        return _convert_xarray_to_json(base_data, dataset_structure=True, flatten_to_v2=flatten_to_v2)
    if file_format == FileFormat.NETCDF3:
        return _convert_xarray_to_netcdf(base_data, netcdf_version=3, flatten_to_v2=flatten_to_v2)
    if file_format == FileFormat.NETCDF4:
        return _convert_xarray_to_netcdf(base_data, netcdf_version=4, flatten_to_v2=flatten_to_v2)


def _convert_xarray_to_csv(base_data: xr.Dataset, use_semicolon_separator: bool = False, flatten_to_v2: bool = False):
    """Convert a xarray DataSet to a CSV file.

    This function converts a xarray DataSet to a CSV file with a semicolon separator if specified.

    Args:
    ----
        base_data (xr.Dataset):
                The Xarray Dataset to convert to a CSV file.
        use_semicolon_separator (bool):
                If True, the CSV file will use a semicolon separator instead of a comma.
        flatten_to_v2 (bool):
                The old V2 format would have multi-level factors flattened into separate factors even if the output
                 format is not a flat file format. This is useful for compatibility with older systems.

    """
    pass


def _convert_xarray_to_json(base_data: xr.Dataset, dataset_structure: bool = False, flatten_to_v2: bool = False):
    """Convert a xarray DataSet to a JSON file.

    This function converts a xarray DataSet to a JSON file.

    Args:
    ----
        base_data (xr.Dataset):
                The Xarray Dataset to convert to a JSON file.
        dataset_structure (bool):
                If True, the JSON file will have a dataset structure.
        flatten_to_v2 (bool):
                The old V2 format would have multi-level factors flattened into separate factors even if the output
                 format is not a flat file format. This is useful for compatibility with older systems.

    """
    pass


def _convert_xarray_to_netcdf(base_data: xr.Dataset, netcdf_version: int, flatten_to_v2: bool = False):
    """Convert a xarray DataSet to a NetCDF file.

    This function converts a xarray DataSet to a NetCDF file.

    Args:
    ----
        base_data (xr.Dataset):
                The Xarray Dataset to convert to a NetCDF file.
        netcdf_version (int):
                The version of the NetCDF format to use.
        flatten_to_v2 (bool):
                The old V2 format would have multi-level factors flattened into separate factors even if the output
                 format is not a flat file format. This is useful for compatibility with older systems.

    """
    pass
