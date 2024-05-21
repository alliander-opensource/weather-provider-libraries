#!/usr/bin/env python

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

from pydantic import BaseModel, ConfigDict, Field

from weather_provider_libraries.__old__.data_classes.enums import DataStorageMode
from weather_provider_libraries.data_classes.commons import TimePeriod
from weather_provider_libraries.utils.transformation.string_related import parse_bytesize_to_easily_readable


class WPStorageConfiguration(BaseModel):
    """A dataclass responsible for the configuration of a WPL Meteo Storage object."""

    weather_source_id: str = Field(
        min_length=4,
        max_length=12,
        title="Source Identifier",
        description="Short string identifier of the source this storage belongs to. Lower case letters only",
        pattern="^[a-z]+$",
    )
    weather_model_id: str = Field(
        min_length=4,
        max_length=12,
        title="Model Identifier",
        description="Short string identifier of the model this storage belongs to. Lower case letters only",
        pattern="^[a-z]+$",
    )
    storage_mode: DataStorageMode = Field(
        title="Storage Mode", description="The WPL Meteo Storage object's storage mode."
    )
    cache_size_in_mb: int = Field(
        default=0,
        title="Storage Cache Size",
        description="The WPL Meteo Storage object's available cache size. "
        "Ignored if the mode set doesn't support cache usage.",
    )
    period_to_archive: TimePeriod | None = Field(
        default=None,
        title="Storage Archival Period",
        description="The WPL Meteo Storage object's configured archival period. "
        "Sets the criteria for archiving actions and cleanup. "
        "Ignored if the mode set doesn't support archives.",
    )
    is_cache_allowed_to_archive: bool = Field(
        default=True,
        title="Is Cache allowed to save to the Archive",
        description="The WPL Meteo Storage object's setting allowing for the cache to push not yet archived data to "
        "the archive [True] or not [False]. "
        "Ignored if the mode set doesn't support both cache and archives",
    )

    # Pydantic class configuration
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    @property
    def metadata(self) -> dict[str, str]:
        """Return the metadata of the storage configuration."""
        metadata_dict = {"Associated Model": self.weather_model_id, "Storage Mode": self.storage_mode}
        if self.storage_mode in [WPStorageMode.CACHE, WPStorageMode.CACHE_AND_ARCHIVE]:
            metadata_dict["Cache Size"] = parse_bytesize_to_easily_readable(self.cache_size_in_mb)

        if self.storage_mode in [WPStorageMode.ARCHIVE, WPStorageMode.CACHE_AND_ARCHIVE]:
            metadata_dict["Archive Period - First date in archive"] = self.period_to_archive.resolved_start
            metadata_dict["Archive Period - Last date in archive"] = self.period_to_archive.resolved_end

        if self.storage_mode == WPStorageMode.CACHE_AND_ARCHIVE:
            metadata_dict["Push Cache to Archive"] = str(self.is_cache_allowed_to_archive)

        return metadata_dict
