#!/usr/bin/env python
from weather_provider_libraries import WeatherProviderModel
from weather_provider_libraries.data_classes.source_related import WPSourceIdentity


class WeatherProviderSource:
    """"""

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
    def is_valid(self) -> bool:
        """Check if the current source is valid."""
        return all(model.is_valid for model in self.identity.models.values())

    def get_model(self, model_id: str) -> WeatherProviderModel:
        """Return the model with the given id."""
        return self.identity.models[model_id]
