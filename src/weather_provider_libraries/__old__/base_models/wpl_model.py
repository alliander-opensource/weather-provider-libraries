#!/usr/bin/env python

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

"""This module contains the WeatherProviderModel class."""

import xarray as xr
from weather_provider_libraries.data_classes.factors import ModelFactor
from weather_provider_libraries.data_classes.model_related import (
    WPModelDataProperties,
    WPModelGeoTemporalProperties,
    WPModelIdentity,
)
from weather_provider_libraries.data_classes.requests import WeatherProviderRequest
from weather_provider_libraries.utils.pint_utils import validate_xarray_dataset_with_pint_units


class WeatherProviderModel:
    """A base class for all weather provider models."""

    def __init__(
        self,
        model_identity: WPModelIdentity,
        model_data_properties: WPModelDataProperties,
        model_geo_temporal_properties: WPModelGeoTemporalProperties,
        model_factors: list[ModelFactor],
    ):
        """The constructor for the WeatherProviderModel class."""
        if not isinstance(model_identity, WPModelIdentity):
            raise ValueError("The model_identity parameter must be an instance of WPModelIdentity.")
        if not isinstance(model_data_properties, WPModelDataProperties):
            raise ValueError("The model_data_properties parameter must be an instance of WPModelDataProperties.")
        if not isinstance(model_geo_temporal_properties, WPModelGeoTemporalProperties):
            raise ValueError(
                "The model_geo_temporal_properties parameter must be an instance of WPModelGeoTemporalProperties."
            )
        if not isinstance(model_factors, list):
            raise ValueError("The model_factors parameter must be a list.")
        if not isinstance(model_factors[0], ModelFactor):
            raise ValueError("The model_factors parameter must be a list of ModelFactor instances.")

        self.identity = model_identity
        self.data_properties = model_data_properties
        self.geo_temporal_properties = model_geo_temporal_properties
        self.factors = model_factors

    def __str__(self):
        """Return a string representation of the model."""
        return f"WeatherProviderModel[{self.identity.id} - {self.identity.name}]"

    @property
    def metadata(self) -> dict[str, str | dict[str, str]]:
        """Return the metadata for the model.

        Returns:
            dict[str, str | dict]:
                    The metadata for the model.

        """
        metadata = self.identity.metadata
        metadata_2 = {
            "Data Properties": self.data_properties.metadata,
            "Geo Temporal Properties": self.geo_temporal_properties.metadata,
        }
        return metadata | metadata_2

    @property
    def known_factors_as_string(self) -> list[str]:
        """Return the known factors for the model.

        Returns:
            list[str]:
                The known factors for the model as a list of strings.

        """
        factor_string_list = [factor.id for factor in self.factors]

        return factor_string_list

    @property
    def id(self) -> str:
        """Getter for the id property. Returns the id of the model."""
        return self.identity.id

    def get_weather_data(self, request: WeatherProviderRequest) -> xr.Dataset:
        """Retrieve data from the model based on a request.

        Returns:
            xr.Dataset:
                    An xarray dataset containing the requested data.

        """
        raise NotImplementedError("Haven't implemented this method yet.")

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
        converted_data = convert_dataset_to_target_unit_system(data_to_convert, target_unit_system, self.factors)
        return converted_data
