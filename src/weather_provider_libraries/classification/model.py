#!/usr/bin/env python

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

import xarray as xr
from weather_provider_libraries.classification.dataclasses.model_information import (
    ModelConfiguration,
    ModelInformation,
    ModelRestrictions,
)
from weather_provider_libraries.classification.request import WPWeatherRequestWithoutPeriod, WPWeatherRequestWithPeriod


class WeatherAccessModel:
    """The Weather Access Model class.

    This class forms a unifying interface for all installed Weather Access Suite models.
    """

    def __init__(
        self,
        model_source_id: str,
        information: ModelInformation,
        restrictions: ModelRestrictions,
        configuration: ModelConfiguration,
    ):
        """Initialize the model with the given information, restrictions, and configuration."""
        if not isinstance(information, ModelInformation):
            raise TypeError("The information should be an instance of ModelInformation.")
        if not isinstance(restrictions, ModelRestrictions):
            raise TypeError("The restrictions should be an instance of ModelRestrictions.")
        if not isinstance(configuration, ModelConfiguration):
            raise TypeError("The configuration should be an instance of ModelConfiguration.")

        self.source_id = model_source_id
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
        self._validate_request(weather_request)

        weather_data_ds = self._retrieve_weather_data(weather_request)
        parsed_weather_data_ds = self._parse_weather_data(weather_data_ds)

        self._validate_returned_data(parsed_weather_data_ds)

        return parsed_weather_data_ds

    def _validate_request(self, weather_request: WPWeatherRequestWithoutPeriod | WPWeatherRequestWithPeriod):
        """Validate the request type with the model configuration."""
        # TODO: Implement the validation logic
        raise NotImplementedError("Not implemented yet.")

    def _retrieve_weather_data(
        self, weather_request: WPWeatherRequestWithoutPeriod | WPWeatherRequestWithPeriod
    ) -> xr.Dataset:
        """Retrieve the weather data for the given request."""
        raise NotImplementedError("This method should be implemented in the child class.")

    def _parse_weather_data(self, weather_data: xr.Dataset) -> xr.Dataset:
        """Parse the weather data."""
        raise NotImplementedError("This method should be implemented in the child class.")

    def _validate_returned_data(self, weather_data: xr.Dataset):
        """Validate the returned weather data for proper formatting."""
        # TODO: Implement the validation logic
        raise NotImplementedError("Not implemented yet.")
