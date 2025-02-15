#!/usr/bin/env python
#  SPDX-FileCopyrightText: 2019-2025 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
import json
import tempfile
import uuid
from pathlib import Path

import xarray as xr
from _typeshed import SupportsWrite
from loguru import logger

from weather_provider_libraries.core.format import FileFormat


def convert_xarray_dataset_to_target_file_format(
    dataset_to_convert: xr.Dataset,
    target_file_format: FileFormat,
    include_metadata: bool = True,
    flatten_to_v2: bool = False,
    target_file_path: Path | None = None,
) -> Path:
    """Convert a xarray DataSet to a target file format.

    This function is used to convert a xarray DataSet to a target file format and store it where it can be accessed.

    Args:
    ----
        dataset_to_convert (xr.Dataset):
            The xarray DataSet to convert to the target file format.
        target_file_format (FileFormat):
            The target file format to convert the xarray DataSet to.
        include_metadata (bool):
            If True, the metadata of the xarray Dataset's metadata will be included in the target file format.
        flatten_to_v2 (bool):
            The old V2 format would have multi-level factors flattened into separate factors even if the output
            format is not a flat file format. This is useful for compatibility with older systems and V2 API endpoint
            compatibility.
        target_file_path (Path):
            The optional path to store the converted file.

    Returns:
    -------
        Path:
            The path to the converted file.

    Raises:
    ------
        ValueError:
            If the target file format is not supported.
        ...
            Other exceptions that can be raised.

    """
    _validate_convert_xarray_dataset_to_target_file_format_settings(
        dataset_to_convert, target_file_format, include_metadata, flatten_to_v2
    )

    if target_file_format == FileFormat.CSV:
        return _convert_xarray_dataset_to_csv(
            base_data=dataset_to_convert,
            include_metadata=include_metadata,
            use_semicolon_separator=False,
            flatten_to_v2=flatten_to_v2,
            target_file_path=target_file_path,
        )

    if target_file_format == FileFormat.CSV_SEMICOLON:
        return _convert_xarray_dataset_to_csv(
            base_data=dataset_to_convert,
            include_metadata=include_metadata,
            use_semicolon_separator=True,
            flatten_to_v2=flatten_to_v2,
            target_file_path=target_file_path,
        )

    if target_file_format == FileFormat.JSON:
        return _convert_xarray_dataset_to_json(
            base_data=dataset_to_convert,
            include_metadata=include_metadata,
            store_in_dataset_structure=False,
            flatten_to_v2=flatten_to_v2,
            target_file_path=target_file_path,
        )

    if target_file_format == FileFormat.JSON_DATASET:
        return _convert_xarray_dataset_to_json(
            base_data=dataset_to_convert,
            include_metadata=include_metadata,
            store_in_dataset_structure=True,
            flatten_to_v2=flatten_to_v2,
            target_file_path=target_file_path,
        )

    if target_file_format == FileFormat.NETCDF3:
        return _convert_xarray_dataset_to_netcdf(
            base_data=dataset_to_convert,
            netcdf_version=3,
            flatten_to_v2=flatten_to_v2,
            target_file_path=target_file_path,
        )

    if target_file_format == FileFormat.NETCDF4:
        return _convert_xarray_dataset_to_netcdf(
            base_data=dataset_to_convert,
            netcdf_version=4,
            flatten_to_v2=flatten_to_v2,
            target_file_path=target_file_path,
        )

    raise ValueError(f"Unsupported target file format '{target_file_format}'.")


def _validate_convert_xarray_dataset_to_target_file_format_settings(
    dataset_to_convert: xr.Dataset,
    target_file_format: FileFormat,
    include_metadata: bool,
    flatten_to_v2: bool,
):
    if not isinstance(dataset_to_convert, xr.Dataset):
        raise ValueError(f"Invalid dataset '{dataset_to_convert}'.")

    if not isinstance(target_file_format, FileFormat):
        raise ValueError(f"Invalid file format '{target_file_format}'.")

    if not isinstance(include_metadata, bool):
        raise ValueError(f"Invalid include_metadata '{include_metadata}'.")

    if not isinstance(flatten_to_v2, bool):
        raise ValueError(f"Invalid flatten_to_v2 '{flatten_to_v2}'.")


def _convert_xarray_dataset_to_csv(
    base_data: xr.Dataset,
    include_metadata: bool = True,
    use_semicolon_separator: bool = False,
    flatten_to_v2: bool = False,
    target_file_path: Path | None = None,
) -> Path:
    """Convert a xarray DataSet to a CSV file.

    This function converts a xarray DataSet to a CSV file. The CSV file will have a comma separator by default,
    but can be set to use a semicolon separator instead.

    Args:
    ----
        base_data (xr.Dataset):
                The Xarray Dataset to convert to a CSV file.
        include_metadata (bool):
                If True, the metadata of the xarray Dataset's metadata will be included in the CSV file.
        use_semicolon_separator (bool):
                If True, the CSV file will have a semicolon separator instead of a comma separator.
        flatten_to_v2 (bool):
                The old V2 format would have multi-level factors flattened into separate factors even if the output
                 format is not a flat file format. This is useful for compatibility with older systems.
        target_file_path (Path):
                The optional path to store the converted CSV file.

    Returns:
    -------
        Path:
            The path to the converted CSV file.

    """
    target_file_path = create_and_establish_target_file(target_file_path)
    separator = ";" if use_semicolon_separator else ","

    # Store the data as CSV
    try:
        with open("data_with_metadata.csv", "w") as f:
            data_frame = base_data.to_dataframe()
            for key, value in base_data.attrs.items():
                f.write(f"# {key}: {value}\n")
            data_frame.to_csv(f, sep=separator, index=True)
    except Exception as e:
        logger.error(f"Failed to write data to CSV file '{target_file_path}'.")
        raise e
    return target_file_path


def _convert_xarray_dataset_to_json(
    base_data: xr.Dataset,
    include_metadata: bool = True,
    store_in_dataset_structure: bool = False,
    flatten_to_v2: bool = False,
    target_file_path: Path | None = None,
) -> Path:
    """Convert a xarray DataSet to a JSON file.

    This function converts a xarray DataSet to a JSON file.

    Args:
    ----
        base_data (xr.Dataset):
                The Xarray Dataset to convert to a JSON file.
        include_metadata (bool):
                If True, the metadata of the xarray Dataset's metadata will be included in the JSON file.
        store_in_dataset_structure (bool):
                If True, the JSON file will have a dataset structure.
        flatten_to_v2 (bool):
                The old V2 format would have multi-level factors flattened into separate factors even if the output
                 format is not a flat file format. This is useful for compatibility with older systems.
        target_file_path (Path):
                The optional path to store the converted JSON file.

    Returns:
    -------
        Path:
            The path to the converted JSON file.

    """
    target_file_path = create_and_establish_target_file(target_file_path)

    # Store the data as JSON
    try:
        f: SupportsWrite[str]
        with open(target_file_path, "w", encoding="utf-8") as f:
            if store_in_dataset_structure:
                json.dump(base_data.to_dict("array"), f, indent=4)

            else:
                json.dump(base_data.to_dict("list"), f, indent=4)
    except Exception as e:
        logger.error(f"Failed to write data to JSON file '{target_file_path}'.")
        raise e
    return target_file_path


def create_and_establish_target_file(target_file_path: Path | None) -> Path:
    """Create and establish a target file.

    This function creates and establishes a target file.

    Args:
    ----
        target_file_path (Path):
            The path to the target file.

    Returns:
    -------
        Path:
            The path to the target file.

    """
    if target_file_path:
        # Create and open the specified file
        target_file_path.touch(exist_ok=True)
    else:
        # Create and open a randomly named temp file with the suffix ".csv"
        target_file_path = Path(tempfile.TemporaryDirectory().name).joinpath(f"{uuid.uuid4()}.csv")

    logger.debug(f"Created and established target file '{target_file_path}'.")
    return target_file_path


#
# def _convert_xarray_to_json(base_data: xr.Dataset, dataset_structure: bool = False, flatten_to_v2: bool = False):
#     """Convert a xarray DataSet to a JSON file.
#
#     This function converts a xarray DataSet to a JSON file.
#
#     Args:
#     ----
#         base_data (xr.Dataset):
#                 The Xarray Dataset to convert to a JSON file.
#         dataset_structure (bool):
#                 If True, the JSON file will have a dataset structure.
#         flatten_to_v2 (bool):
#                 The old V2 format would have multi-level factors flattened into separate factors even if the output
#                  format is not a flat file format. This is useful for compatibility with older systems.
#
#     """
#     pass
#
#
# def _convert_xarray_to_netcdf(base_data: xr.Dataset, netcdf_version: int, flatten_to_v2: bool = False):
#     """Convert a xarray DataSet to a NetCDF file.
#
#     This function converts a xarray DataSet to a NetCDF file.
#
#     Args:
#     ----
#         base_data (xr.Dataset):
#                 The Xarray Dataset to convert to a NetCDF file.
#         netcdf_version (int):
#                 The version of the NetCDF format to use.
#         flatten_to_v2 (bool):
#                 The old V2 format would have multi-level factors flattened into separate factors even if the output
#                  format is not a flat file format. This is useful for compatibility with older systems.
#
#     """
#     pass
