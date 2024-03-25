#!/usr/bin/env python

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

"""This module contains the WeatherProviderModel class."""

import xarray as xr

from weather_provider_libraries.utils.pint_utils import validate_xarray_dataset_with_pint_units


class WeatherProviderModel:
    """A base class for all weather provider models."""

    def __init__(self):
        """The constructor for the WeatherProviderModel class."""
        ...

    @property
    def metadata(self) -> dict[str, str | dict]:
        """Return the metadata for the model.

        Returns:
            dict[str, str | dict]:
                    The metadata for the model.

        """
        ...

    @property
    def id(self) -> str:
        """Getter for the id property. Returns the id of the model."""
        ...

    def get_data_by_request(self) -> xr.Dataset:
        """Retrieve data from the model based on a request.

        Returns:
            xr.Dataset:
                    An xarray dataset containing the requested data.

        """
        ...

    def convert_data_to_unit_system(self, data_to_convert: xr.Dataset, target_unit_system) -> xr.Dataset:
        """Convert the data to a target unit system.

        Args:
            data_to_convert (xr.Dataset):
                The data to convert. This Xarray dataset should have a 'unitSystem' metadata attribute and each
                variable should have a Pint 'units' attribute.
            target_unit_system:
                The target unit system to convert the data to.

        Returns:
            xr.Dataset:
                    An xarray dataset containing the converted data.

        Raises:
            TypeError:
                If the dataset is not a xarray dataset.
            ValueError:
                If the dataset does not have a 'unitSystem' metadata attribute.
                If a variable within the dataset does not have a 'units' attribute.
                If the 'units' attribute of a variable is not a valid Pint unit string.
        """
        # 1. Validate the input dataset for type and content
        validate_xarray_dataset_with_pint_units(data_to_convert)

        # 2. Convert the data to the target unit system
        converted_data = convert_dataset_to_target_unit_system(data_to_convert, target_unit_system, self.known_factors)
        return converted_data
