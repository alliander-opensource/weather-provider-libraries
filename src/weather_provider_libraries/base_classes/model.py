#!/usr/bin/env python

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-{2024}} Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

from weather_provider_libraries.base_classes.model_related.model_information import (
    ModelConfiguration,
    ModelInformation,
    ModelRestrictions,
)
from weather_provider_libraries.base_classes.request import WPWeatherRequestWithoutPeriod, WPWeatherRequestWithPeriod


class WPLModel:

    def __init__(
        self, information: ModelInformation, restrictions: ModelRestrictions, configuration: ModelConfiguration
    ):
        """Initialize the model with the given information, restrictions, and configuration."""
        if not isinstance(information, ModelInformation):
            raise TypeError("The information should be an instance of ModelInformation.")
        if not isinstance(restrictions, ModelRestrictions):
            raise TypeError("The restrictions should be an instance of ModelRestrictions.")
        if not isinstance(configuration, ModelConfiguration):
            raise TypeError("The configuration should be an instance of ModelConfiguration.")

        self.information = information
        self.restrictions = restrictions
        self.configuration = configuration

        # TODO:
        #  1. Read factor information
        #  2. Setup storage if needed

    @property
    def id(self):
        """Return the model identifier."""
        return self.information.id

    @property
    def name(self):
        """Return the model name."""
        return self.information.name

    @property
    def metadata(self) -> dict[str, dict[str, str]]:
        """Return the metadata for the current model."""
        metadata = {self.id: self.information.metadata}

        metadata[self.id].update(self.restrictions.metadata)
        metadata[self.id].update(self.configuration.metadata)

        return metadata

    def get_weather_data(self, weather_request: WPWeatherRequestWithoutPeriod | WPWeatherRequestWithPeriod):
        """Get the weather data for the given request."""
        # TODO:
        #   1. Validate the request type with the model configuration
        #   2. Retrieve the weather data for the given request
        #   3. Parse the weather data
        #   4. Return the parsed weather data

    def _retrieve_weather_data(self, weather_request: WPWeatherRequestWithoutPeriod | WPWeatherRequestWithPeriod):
        """Retrieve the weather data for the given request."""
        raise NotImplementedError("This method should be implemented in the child class.")

    def _parse_weather_data(self, weather_data: dict):
        """Parse the weather data."""
        raise NotImplementedError("This method should be implemented in the child class.")
