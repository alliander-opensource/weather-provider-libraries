#!/usr/bin/env python

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

import xarray as xr
from weather_provider_libraries.data_classes.model_related import (
    WPModelDataProperties,
    WPModelDataStorageSettings,
    WPModelGeoTemporalProperties,
    WPModelIdentity,
)


class WeatherProviderModel:
    """The base class for all Weather Provider models.

    This class is responsible for handling all Weather Provider models. Classes without this base class will not be
    recognized as Weather Provider models. The goal of this class is to enforce a consistent structure for all models,
    as well as enforce a certain level of metadata and provide a consistent way to access this metadata and the model's
    affiliated weather data.
    """

    def __init__(
        self,
        identity: WPModelIdentity,
        data_properties: WPModelDataProperties,
        geo_temporal_properties: WPModelGeoTemporalProperties,
        data_storage_settings: WPModelDataStorageSettings,
        factors: set[ModelFactor],
    ):
        """The constructor for the WeatherProviderModel class."""
        self._validate_class_input(identity, data_properties, geo_temporal_properties, factors)

        self.identity: WPModelIdentity = identity
        self.__data_properties: WPModelDataProperties = data_properties
        self.__geo_temporal_properties: WPModelGeoTemporalProperties = geo_temporal_properties
        self.__data_storage_settings: WPModelDataStorageSettings = data_storage_settings
        self.__factors: set[ModelFactor] = factors

    def __str__(self):
        """Return a string representation of the model."""
        return f"WeatherProviderModel[{self.identity.id} - {self.identity.name}]"

    @property
    def id(self) -> str:
        """Return the id of the model."""
        return self.identity.id

    @property
    def known_factors(self) -> set[str]:
        """Return the known factors for the model."""
        return {factor.id for factor in self.__factors}

    def get_weather_data(self, data_request: WPDataRequest) -> xr.Dataset:
        """Get the weather data for the model.

        Args:
            data_request (WeatherProviderRequest):
                The request for the weather data.

        Returns:
            xr.Dataset: The weather data for the model.
        """
        raise NotImplementedError("Haven't implemented this method yet.")

    def format_weather_data(self, data: xr.Dataset, format_request: WPFormatRequest) -> xr.Dataset:
        """Format the weather data for the model.

        Args:
            data (xr.Dataset):
                The weather data to format.
            format_request (WeatherProviderFormatRequest):
                The request for the formatting.

        Returns:
            xr.Dataset: The formatted weather data.
        """
        raise NotImplementedError("Haven't implemented this method yet.")
