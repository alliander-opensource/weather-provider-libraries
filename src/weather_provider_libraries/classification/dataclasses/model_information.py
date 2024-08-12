#!/usr/bin/env python

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

from ipaddress import IPv4Address, IPv6Address

from pydantic import BaseModel, ConfigDict, Field, HttpUrl
from pyproj.aoi import BBox
from weather_provider_libraries.__old__locations.base_classes import WPDataStorageMode
from weather_provider_libraries.utility.classes.period import WPTimePeriod


class ModelInformation(BaseModel):
    """A dataclass used to store the basic information for a model.

    This is used to identify a model and to provide basic text-based information on the model and its contents.
    """

    id: str = Field(
        title="Model identifier",
        description="A unique identifier for the model within the source",
        min_length=4,
        max_length=12,
        pattern="^[a-z_]+$",
    )
    name: str = Field(
        title="Model name",
        description="The official name for the model, used by the project logs.",
        min_length=8,
        max_length=50,
        pattern="^[a-zA-Z ]+$",
    )
    supported_version: str = Field(
        title="Supported version",
        description="Description of what version of the available data is supported.",
        min_length=4,
        max_length=250,
    )
    licensing_information: str = Field(
        title="Licensing information",
        description="Information on the licensing of the used data. At least a reference to the license type.",
        min_length=4,
        max_length=120,
    )
    information_url: HttpUrl | IPv4Address | IPv6Address = Field(
        title="Information URL",
        description="URL to an information page where one can read more about the model or the data it provides.",
    )
    description: str = Field(
        title="Description",
        description="A basic description of the model and its (intended) contents.",
        min_length=8,
        max_length=500,
    )

    # Pydantic model configuration
    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)

    @property
    def metadata(self) -> dict[str, str]:
        return {
            "ID": self.id,
            "Name": self.name,
            "Version Supported": self.supported_version,
            "Licensing Information": self.licensing_information,
            "Information URL": self.information_url,
            "Description": self.description,
        }


class ModelRestrictions(BaseModel):
    """A dataclass used to store the restrictions of a model.

    This is used to check if a model is valid for a certain geographical area and/or time period.
    """

    data_availability_period: WPTimePeriod = Field(
        title="Data availability period", description="The period for which data could be available to the model."
    )
    data_usage_period: WPTimePeriod = Field(
        title="Data usage period", description="The period for which data is actually used by the model."
    )
    area_availability_zone: BBox = Field(
        title="Area availability zone", description="The area for which data could be available to the model."
    )
    area_usage_zone: BBox = Field(
        title="Area usage zone", description="The area for which data is actually used by the model."
    )

    # Pydantic model configuration
    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)

    @property
    def metadata(self) -> dict[str, str]:
        return {
            "Data availability": f"{self.data_availability_period.start} - {self.data_availability_period.end}",
            "Data usage": f"{self.data_usage_period.start} - {self.data_usage_period.end}",
            "Geographic area available": f"[W: {self.area_availability_zone.west}, "
            f"E: {self.area_availability_zone.east}, "
            f"N: {self.area_availability_zone.north}, "
            f"S: {self.area_availability_zone.south}]",
            "Geographic area used": f"[W: {self.area_usage_zone.west}, E: {self.area_usage_zone.east}, "
            f"N: {self.area_usage_zone.north}, S: {self.area_usage_zone.south}]",
        }


class ModelConfiguration(BaseModel):
    """A dataclass used to store the configuration of a model.

    This is used to instruct the project how a model should be handled.
    """

    periodical_data_can_be_requested: bool = Field(
        True,
        title="Periodical data can be requested",
        description="Indicator for if periodical data can be requested for the model.",
    )
    use_data_storage_mode: WPDataStorageMode = Field(
        WPDataStorageMode.NO_STORAGE,
        title="Model data storage mode to use",
        description="The standard data storage mode to use for the model.",
    )
    archive_data_period: WPTimePeriod | None = Field(
        None,
        title="Model archiving period",
        description="The period for which data is archived. "
        "Only interpreted when also using a storage mode that supports archiving.",
    )
    cache_data_size_in_mb: WPTimePeriod | None = Field(
        None,
        title="Model cache data size in MB",
        description="The size of the cache data in MB. "
        "Only interpreted when also using a storage mode that supports caching.",
    )

    # Pydantic model configuration
    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)

    @property
    def metadata(self) -> dict[str, str]:
        return {
            "Data retrieval for periods is possible": str(self.periodical_data_can_be_requested),
            "Data storage method used": str(self.use_data_storage_mode),
            "Period stored in archive (if applicable)": str(self.archive_data_period),
            "Amount of MBs stored in cache (if applicable)": self.cache_data_size_in_mb,
        }
