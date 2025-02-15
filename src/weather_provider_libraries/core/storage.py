#!/usr/bin/env python

#  SPDX-FileCopyrightText: 2019-2025 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0

from enum import StrEnum

from pydantic import BaseModel, Field


class StorageType(StrEnum):
    """Possible methods of storing data for a model."""

    NO_STORAGE = "No data storage required"
    CACHE = "Store data in cache for a limited time and up to a certain size"
    REPOSITORY = "Store data in a repository for a longer time and up to a certain size"
    CACHE_AND_REPOSITORY = "Combine cache and repository storage methods"


class StorageSettings(BaseModel):
    """..."""

    storage_type: StorageType = Field(StorageType.NO_STORAGE, description="The storage type for the model.")
    max_cache_size_in_mb: int | None = Field(500, description="The maximum cache size in MB.")
    max_cache_time_in_minutes: int | None = Field(24 * 60, description="The maximum cache time in minutes.")
    max_repository_size_in_gb: int | None = Field(100, description="The maximum repository size in GB.")


class Storage:
    """..."""

    def __init__(self, storage_settings: StorageSettings):
        """Initialize the storage."""
        self._storage_settings: StorageSettings = storage_settings
