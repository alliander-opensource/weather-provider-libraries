#!/usr/bin/env python

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

import xarray as xr

"""Pint utility functions for validating pint unit strings and xarray datasets with pint annotations."""


def validate_pint_unit_string(unit_string: str):
    """Validate a Pint unit string as being a valid unit string for Pint.

    Args:
        unit_string (str):
            The unit string to validate as a valid Pint unit string.

    Raises:
        ValueError:
            If the unit string is not a valid Pint unit string.
    """
    ...


def validate_xarray_dataset_with_pint_units(dataset_to_validate: xr.Dataset):
    """Validate a xarray dataset as having Pint annotations and a unitSystem metadata attribute.

    Notes:
        Each processed dataset within this project should have a 'unitSystem' metadata attribute and each factor
        stored within it should have a Pint unit quantification associated with it.

    Args:
        dataset_to_validate (xr.Dataset):
            The dataset to validate.

    Raises:
        TypeError:
            If the dataset is not a xarray dataset.
        ValueError:
            If the dataset does not have a 'unitSystem' metadata attribute.
            If a variable within the dataset does not have a 'units' attribute.
            If the 'units' attribute of a variable is not a valid Pint unit string.
    """
    # 0. Check if the dataset is an xarray dataset
    if not isinstance(dataset_to_validate, xr.Dataset):
        raise TypeError("The dataset is not an xarray dataset.")

    # 1. Check if the dataset has a 'unitSystem' metadata attribute
    if "unitSystem" not in dataset_to_validate.metadata:
        raise ValueError("The dataset does not have a 'unitSystem' metadata attribute.")

    for key in dataset_to_validate:
        # 2. Check if the variable has a Pint unit quantification
        if not dataset_to_validate[key].pint or not dataset_to_validate[key].pint.units:
            raise ValueError(f"The variable '{key}' does not have a 'units' attribute.")

        # 3. Validate that quantification as a valid Pint unit string
        validate_pint_unit_string(dataset_to_validate[key].pint.units)
