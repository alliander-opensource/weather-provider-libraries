#!/usr/bin/env python


#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

import xarray as xr

from weather_provider_libraries import WeatherProviderModel
from weather_provider_libraries.data_classes.requests import WeatherProviderRequest
from weather_provider_libraries.data_classes.source_related import WPSourceIdentity


class WeatherProviderSource:
    """A class representing a weather provider source."""

    def __init__(self, identity: WPSourceIdentity):
        """The constructor for the WeatherProviderSource class."""
        self.identity = identity

    def __str__(self):
        """Return a string representation of the source."""
        return f"WeatherProviderSource[{self.id}- {self.identity.name}]"

    @property
    def id(self) -> str:
        """Return the id of the source."""
        return self.identity.id

    @property
    def models(self) -> dict[str, WeatherProviderModel]:
        """Return the models of the source."""
        return self.identity.models

    @property
    def list_of_models(self) -> list[str]:
        """Return the list of models of the source."""
        return list(self.models.keys())

    @property
    def metadata(self) -> dict[str, str | dict[str, str]]:
        """Return the metadata for the source.

        Returns:
            dict[str, str | dict]:
                A dictionary containing the metadata for the source.
        """
        return {
            "id": self.id,
            "name": self.identity.name,
            "description": self.identity.description,
            "information_url": self.identity.information_url,
            "models": {model_id: model.metadata for model_id, model in self.models.items()},
        }

    def load_model(self, model: WeatherProviderModel):
        """Load a weather provider model."""
        self.identity.models[model.id] = model

    def get_model(self, model_id: str) -> WeatherProviderModel:
        """Return the model with the given id."""
        return self.identity.models[model_id]

    def get_weather_data(self, model_id: str, weather_request: WeatherProviderRequest) -> xr.Dataset:
        """Get the weather data for the given model."""
        return self.get_model(model_id).get_weather_data(weather_request)
