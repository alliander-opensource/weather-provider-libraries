#!/usr/bin/env python

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

import xarray as xr
from loguru import logger
from weather_provider_libraries.data_classes.source_related import WPSourceIdentity


class WeatherProviderSource:
    """The base class for representing weather provider sources.

    A weather provider source is any collection of multiple models that provide weather data. Usually a source will be
    based on a meteorological institute or a weather data provider, but it can also just be a collection of models with
    no specific provider but similar traits.
    """

    def __init__(self, source_identity: WPSourceIdentity):
        """The constructor for the WeatherProviderSource class."""
        if not isinstance(source_identity, WPSourceIdentity):
            logger.error(f"The source identity type should be WPSourceIdentity, but was: {type(source_identity)}")
            raise TypeError("source_identity must be of type WPSourceIdentity")

        self.__source_identity: WPSourceIdentity = source_identity

        logger.info(f"Searching for available models for source: {self.id}")
        self.__available_models: dict[str, str] = self._find_available_models()
        logger.info(f"Valid available models found for source: {self.id} - {len(self.__available_models)} models")

        if len(self.__available_models) == 0:
            logger.error(f"No models found for source: {self.id}")
            raise IndexError(f"No models found for source: {self.id}")

    def __str__(self):
        """Return a string representation of the source."""
        return f"WeatherProviderSource[{self.id}- {self.__source_identity.name}]"

    @property
    def id(self) -> str:
        """Return the id of the source."""
        return self.__source_identity.id

    @property
    def models(self) -> set[str]:
        """Return the id's of the available models for the source."""
        return set(self.__available_models.keys())

    @property
    def metadata(self) -> dict[str, str | dict[str, str]]:
        """Return the metadata for the source."""
        return {
            "id": self.id,
            "name": self.__source_identity.name,
            "description": self.__source_identity.description,
            "information_url": self.__source_identity.information_url,
            "models": self._get_models_metadata(),
        }

    def get_weather_data(self, request: WPRequest, format: WPFormat) -> xr.Dataset:
        """Get weather data from the source."""
        if not isinstance(request, WPRequest):
            raise TypeError("request must be of type WPRequest")
        if not isinstance(format, WPFormat):
            raise TypeError("format must be of type WPFormat")
        if request.model_id not in self.models:
            raise ValueError(f"Model {request.model_id} is not available for source {self.id}")
        return self._get_weather_data(request, format)

    def get_model(self, model_id: str) -> WeatherProviderModel:
        """Get a model from the source."""
        if model_id not in self.models:
            raise ValueError(f"Model {model_id} is not available for source {self.id}")
        return self._get_model(model_id)
