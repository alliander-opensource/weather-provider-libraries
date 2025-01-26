#!/usr/bin/env python

#  SPDX-FileCopyrightText: 2019-2025 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0

import xarray as xr

from weather_provider_libraries.core.format import Format
from weather_provider_libraries.core.model import Model
from weather_provider_libraries.core.request import Request
from weather_provider_libraries.core.storage import Storage


class Source:
    """The main class for the WPAS Libraries project dedicated to meteorological data sources.

    A source is a collection of models that provide weather data. The source is responsible for loading the models and
    providing the user with the necessary methods to retrieve weather data and format it.
    """

    def __init__(self):
        """Initialize the source."""
        # Initialize the models
        self._models: dict[str, Model] = ...

        # Initialize the storage settings
        self._storage_settings: dict[str, Storage] = ...

        # Run a self validation to check if everything is correctly loaded
        ...

    def get_model(self, model_id: str) -> Model:
        """Retrieve a specific model from the source."""
        return self._models[model_id]

    def get_weather(self, model_id: str, weather_request: Request) -> xr.Dataset:
        """Retrieve weather data from a specific model.

        Args:
        ----
            model_id (str):
                    The model identifier.
            weather_request (WeatherRequest):
                    The weather request object.

        Returns:
        -------
            xr.Dataset:
                    The weather data.

        """
        model = self.get_model(model_id)

        return model.get_weather(weather_request)

    def format_weather(self, weather_data: xr.Dataset, target_format: Format) -> str:
        """Format the weather data according to a specific format.

        Format the weather data according to the target format.
        """
        model_id = weather_data.attrs["model_id"]

        model = self.get_model(model_id)

        return model.format_weather(weather_data, target_format)

    @property
    def metadata(self) -> dict:
        """Return the metadata of the source."""
        return {
            "name": self.metadata["name"],
            "version": self.metadata["version"],
            "models": [self._models[model].metadata for model in self.models],
        }

    @property
    def models(self) -> list[str]:
        """Return the models of the source."""
        return list(self._models.keys())
