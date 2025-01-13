#!/usr/bin/env python

#  SPDX-FileCopyrightText: 2019-2025 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0

"""This module contains the base class for the WPAS libraries Sources."""
import xarray as xr

from weather_provider_libraries.base_classes.meteo_model import MeteoModel
from weather_provider_libraries.base_classes.meteo_request import MeteoRequest


class MeteoSource:
    """This class is the base class for the WPAS libraries Meteo Sources."""

    def __init__(self):
        """Initialize the source."""
        self._models: dict[str, MeteoModel] = {}

    @property
    def models(self) -> set[str]:
        """Get the models."""
        return set(self._models.keys())

    def get_meteo_data(self, model_id: str, request: MeteoRequest) -> xr.Dataset:
        """Get the meteo data."""
        ...

    def get_model(self, model_id: str) -> MeteoModel:
        """Get the model."""
        return self._models[model_id]
