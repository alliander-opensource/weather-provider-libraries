#!/usr/bin/env python

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field

from weather_provider_libraries.data_classes.other import TimePeriod
from weather_provider_libraries.utils.transformation.string_transformers import parse_bytesize_to_easily_readable


class StorageMode(str, Enum):
    """An enumeration of the different storage modes available for a WPL Meteo Storage object."""

    NO_STORAGE = "Do not store any data"
    CACHE = "Store recent requests up to a size limit"
    ARCHIVE = "Store a specifically set period"
    CACHE_AND_ARCHIVE = "Combine cached and archive options"


class StorageConfiguration(BaseModel):
    """A dataclass responsible for the configuration of a WPL Meteo Storage object.

    This immutable dataclass holds the basic configuration of a WPL Meteo Storage object, used to evaluate what data to
    gather and store on disk, either periodically or temporarily.

    """

    storage_mode: StorageMode = Field(title="Storage Mode", description="The WPL Meteo Storage object's storage mode.")
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
    cache_to_archive: bool = Field(
        default=True,
        title="Storage Cache to Archive Mode",
        description="The WPL Meteo Storage object's setting allowing for the cache to push not yet archived data to "
        "the archive [True] or not [False]. "
        "Ignored if the mode set doesn't support both cache and archives",
    )

    # Pydantic class configuration
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    @property
    def metadata(self) -> dict[str, str]:
        """Return a metadata dictionary representation of this StorageConfiguration object."""
        metadata_dict = {"Storage Mode": self.storage_mode}
        if self.storage_mode in [StorageMode.CACHE, StorageMode.CACHE_AND_ARCHIVE]:
            metadata_dict["Cache Size"] = parse_bytesize_to_easily_readable(self.cache_size_in_mb)

        if self.storage_mode in [StorageMode.ARCHIVE, StorageMode.CACHE_AND_ARCHIVE]:
            metadata_dict["Archive Period - First date in archive"] = self.period_to_archive.resolved_start
            metadata_dict["Archive Period - Last date in archive"] = self.period_to_archive.resolved_end

        if self.storage_mode == StorageMode.CACHE_AND_ARCHIVE:
            metadata_dict["Push Cache to Archive"] = str(self.cache_to_archive)
        return metadata_dict
