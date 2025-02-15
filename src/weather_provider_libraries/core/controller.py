#!/usr/bin/env python


#  SPDX-FileCopyrightText: 2019-2025 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0


import xarray as xr

from weather_provider_libraries._settings import PROJECT_SETTINGS
from weather_provider_libraries.core.format import Format
from weather_provider_libraries.core.request import Request
from weather_provider_libraries.core.source import Source


class Controller:
    """The main controller for the WPAS Libraries project.

    The controller is meant to be a main entry point for the WPAS Libraries project and is the main interface for the
    user to interact with the project. The controller is responsible for loading the configuration, initializing the
    sources and models, and providing the user with the necessary methods to retrieve weather data and format it.
    """

    def __init__(self):
        """Initialize the controller.

        Load the configuration from the Pydantic Settings object and initialize the sources and models.
        """
        # Load the configuration from the Pydantic Settings object
        ...

        # Initialize the sources and models
        self._sources: dict[str, Source] = ...

        # Run a self validation to check if everything is correctly loaded
        ...

    def get_weather(self, source_id: str, model_id: str, weather_request: Request) -> xr.Dataset:
        """Retrieve weather data from a specific model within a source.

        Args:
        ----
            source_id (str):
                    The source identifier.
            model_id (str):
                    The model identifier.
            weather_request (WeatherRequest):
                    The weather request object.

        Returns:
        -------
            xr.Dataset:
                    The weather data.

        """
        source = self.get_source(source_id)

        return source.get_weather(model_id, weather_request)

    def format_weather(self, weather_data: xr.Dataset, target_format: Format) -> str:
        """Format the weather data according to a specific format.

        Retrieve the source and model from the weather data and format the data according to the target format.
        """
        source_id = weather_data.attrs["source_id"]
        source = self.get_source(source_id)

        return source.format_weather(weather_data, target_format)

    def get_source(self, source_id: str) -> Source | None:
        if not self._sources or source_id not in self.sources:
            return None
        return self.sources[source_id]

    @property
    def metadata(self) -> dict:
        """Return the metadata."""
        return {
            "name": PROJECT_SETTINGS.project_name,
            "version": PROJECT_SETTINGS.version,
            "sources": self.sources,
        }

    @property
    def sources(self) -> dict[str, Source] | None:
        """Return the Sources metadata."""
        if len(self._sources) == 0:
            return None
        source_metadata = {}
        for source in self._sources:
            source_metadata[source] = self._sources[source].metadata
        return source_metadata
