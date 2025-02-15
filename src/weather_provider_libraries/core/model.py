#!/usr/bin/env python

#  SPDX-FileCopyrightText: 2019-2025 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0

import xarray as xr
from pydantic import BaseModel, Field

from weather_provider_libraries.core.factors import ModelFactor
from weather_provider_libraries.core.format import Format
from weather_provider_libraries.core.request import Request
from weather_provider_libraries.core.storage import StorageSettings, StorageType


class ModelData(BaseModel):
    """..."""

    id: str = Field(..., description="The model identifier.", min_length=3, max_length=12)
    name: str = Field(..., description="The model name.", min_length=3, max_length=50)
    description: str = Field(..., description="The model description.", min_length=3, max_length=100)


class Model:
    """The main class for the WPAS Libraries project dedicated to meteorological data models.

    A model is a representation of an existing specific weather model that provides weather data. The model is
    responsible for providing the user with the necessary methods to retrieve that weather data and format it.
    """

    def __init__(self, model_data: ModelData, model_factors: list[ModelFactor]):
        """Initialize the model."""
        # Set the model data
        self._model_data: ModelData = model_data
        self._model_factors: dict[str, ModelFactor] = {factor.factor_id: factor for factor in model_factors}
        self.storage_settings: StorageSettings = self._load_storage_settings() or StorageSettings(
            storage_type=StorageType.NO_STORAGE
        )

        # Run a self validation to check if everything is correctly loaded
        self._validate()

    @staticmethod
    def _load_storage_settings() -> StorageSettings | None:
        """Load the storage settings."""
        # Load the storage settings from the Environment variables
        return None

    def get_weather(self, weather_request: Request) -> xr.Dataset:
        """Retrieve weather data from the model.

        Args:
        ----
            weather_request (WeatherRequest):
                    The weather request object.

        Returns:
        -------
            xr.Dataset:
                    The weather data.

        """
        raw_weather_data = self._retrieve_weather(weather_request)
        harmonized_weather_data = self._harmonize_weather(raw_weather_data)

        return harmonized_weather_data

    def _retrieve_weather(self, weather_request: Request) -> xr.Dataset:
        """Retrieve weather data from the model.

        Retrieve weather data from the model based on the weather request object.
        """
        raise NotImplementedError("The method '_retrieve_weather' must be implemented in a subclass.")

    def _harmonize_weather(self, raw_weather_data: xr.Dataset) -> xr.Dataset:
        """Harmonize the weather data.

        Harmonize the weather data to make it compatible with the model's formatting process.
        """
        raise NotImplementedError("The method '_harmonize_weather' must be implemented in a subclass.")

    def format_weather(self, weather_data: xr.Dataset, target_format: Format) -> str:
        """Format the weather data according to a specific format.

        Format the weather data according to the target format.
        """
        factor_reformatted_data = self._reformat_weather(weather_data, target_format)
        file_data = self._save_data(factor_reformatted_data, target_format)

        return file_data

    def _reformat_weather(self, weather_data: xr.Dataset, target_format: Format) -> xr.Dataset:
        """Reformat the weather data.

        Reformat the weather data according to the target format.
        """
        raise NotImplementedError("The method '_reformat_weather' must be implemented in a subclass.")

    def _save_data(self, factor_reformatted_data: xr.Dataset, target_format: Format) -> str:
        """Save the reformatted data.

        Save the reformatted data to a file.
        """
        raise NotImplementedError("The method '_save_data' must be implemented in a subclass.")

    def _validate(self):
        """Validate the model."""
        if self.storage_settings.storage_type not in StorageType:
            raise ValueError(f"Invalid storage type: {self.storage_settings.storage_type}")

        for factor_id in self._model_factors:
            if not isinstance(self._model_factors[factor_id], ModelFactor):
                raise ValueError(f"Invalid factor: {self._model_factors[factor_id]}")

        if not isinstance(self._model_data, ModelData):
            raise ValueError(f"Invalid model data: {self._model_data}")

    @property
    def metadata(self) -> dict:
        """Return the model metadata."""
        metadata: dict[str, str] = {
            "id": self._model_data.id,
            "name": self._model_data.name,
            "description": self._model_data.description,
            "factors": [factor_id for factor_id in self._model_factors],
            "storage_type": self.storage_settings.storage_type,
        }

        if self.storage_settings.storage_type in [StorageType.CACHE, StorageType.CACHE_AND_REPOSITORY]:
            metadata["max_cache_size_in_mb"] = f"{self.storage_settings.max_cache_size_in_mb} MB"
            metadata["max_cache_time_in_minutes"] = f"{self.storage_settings.max_cache_time_in_minutes} minutes"

        if self.storage_settings.storage_type in [StorageType.REPOSITORY, StorageType.CACHE_AND_REPOSITORY]:
            metadata["max_repository_size_in_gb"] = f"{self.storage_settings.max_repository_size_in_gb} GB"

        return metadata
