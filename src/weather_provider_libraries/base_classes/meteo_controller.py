#!/usr/bin/env python

#  SPDX-FileCopyrightText: 2019-2025 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0

"""This module contains the base class for the WPAS libraries controller."""
from copy import deepcopy

import xarray as xr
from loguru import logger

from weather_provider_libraries._settings import PROJECT_SETTINGS
from weather_provider_libraries.base_classes.meteo_request import MeteoRequest
from weather_provider_libraries.base_classes.meteo_source import MeteoSource
from weather_provider_libraries.base_classes.meteo_storage import MeteoStorage

"""This module contains the base class for the WPAS libraries meteo data controller."""


class MeteoController:
    """This class is the base class for the WPAS libraries controller.

    The controller is responsible for managing the just sources and accessing their data. The sources themselves handle
     things like the data retrieval and processing.
    """

    def __init__(self):
        """Initialize the controller."""
        self._sources: dict[str, MeteoSource] = {}
        self.init_sources()

    @property
    def sources(self) -> set[str]:
        """Get the sources."""
        return set(self._sources.keys())

    def get_meteo_data(self, source_id: str, model_id: str, request: MeteoRequest) -> xr.Dataset:
        """Get the meteo data from a source."""
        if source_id not in self.sources:
            logger.error(f"Source {source_id} not found.")
            raise AttributeError(f"Source {source_id} not found.")

        return self._sources[source_id].get_meteo_data(model_id, request)

    def get_source(self, source_id: str) -> MeteoSource:
        """Get the source."""
        return self._sources[source_id]

    def init_sources(self):
        """Check for the project settings and initialize sources according to the configuration desired."""
        if PROJECT_SETTINGS.controller_sources == "autoloader":
            self._autoload_sources()
        else:
            for source in PROJECT_SETTINGS.controller_sources:
                self.add_source(source)

        if len(self.sources) == 0:
            logger.error("No sources found. Please check the configuration.")
            raise AttributeError("No sources found. Please check the configuration.")

    def add_source(self, source_name: str):
        """Add a source."""
        ...

    def get_storage_objects(self) -> set[MeteoStorage]:
        """Get the storage objects for each model with a storage object."""
        storage_objects = set()

        for source_id in self.sources:
            source = self.get_source(source_id)
            for model_id in source.models:
                model = source.get_model(model_id)
                if model.storage:
                    storage_objects.add(deepcopy(model.storage))

        return storage_objects

    def _autoload_sources(self):
        """Autoload the sources."""
        # Check all existing modules within the weather_provider_sources package currently available for possible
        #  sources.
        possible_sources = ...

        # Check all possible sources for validity and add them to the sources list.
        for source in possible_sources:
            if self._is_possible_source_valid(source):
                self.add_source(source)
 
    def _is_possible_source_valid(self, source_name: str) -> bool:
        """Validate a possible source from a name."""
        # Check if the source is a valid source by checking if it exists as a package within the
        #  weather_provider_sources base package.
        ...

        # Check if the source is a valid source by checking if it is a subclass of the MeteoSource class.
        ...

        # Verify that the source has a valid configuration.
        ...

        # Check if the source is a valid source by checking if it has models.
        ...

        return True
    