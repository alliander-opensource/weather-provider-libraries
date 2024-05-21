#!/usr/bin/env python

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

from ipaddress import IPv4Address, IPv6Address

from pydantic import BaseModel, ConfigDict, Field, HttpUrl
from pyproj import CRS
from pyproj.aoi import BBox

from weather_provider_libraries.data_classes.commons import TimePeriod
from weather_provider_libraries.data_classes.enums import WPDataStorageMode


class WPModelIdentity(BaseModel):
    """A class representing the identity of a weather provider model.

    This immutable class contains everything relevant about the identity of a singular weather provider model.

    """

    id: str = Field(
        min_length=3,
        max_length=12,
        title="Identifier",
        description="Short string identifier of the Model. Lower case letters only",
        pattern="^[a-z]+$",
    )
    name: str = Field(
        min_length=4,
        max_length=32,
        title="Name",
        description="Short name of the Model. Letters and spaces only",
        pattern="^[a-zA-Z ]+$",
    )
    description: str = Field(
        min_length=12,
        max_length=512,
        title="Description",
        description="Short description of the Model. Should contain a brief description of the Model",
    )
    information_url: HttpUrl | IPv4Address | IPv6Address = Field(
        title="Source Data Information URL",
        description="A link to a URL or IP address holding extensive information on the model or it's source data",
    )
    license_information: str = Field(
        min_length=2,
        max_length=512,
        title="Data Licensing Information",
        description="Information about the licensing of the model data. Should preferably contain a "
        "SPDX-License-Identifier, and otherwise a brief description of the license.",
    )

    # Pydantic class configuration:
    model_config = ConfigDict(frozen=True, extra="forbid")

    @property
    def metadata(self) -> dict[str, str]:
        """Return the metadata for the model.

        Returns:
            dict[str, str]:
                    The metadata for the model.
        """
        return {
            self.model_fields["id"].title: self.id,
            self.model_fields["name"].title: self.name,
            self.model_fields["description"].title: self.description,
            self.model_fields["information_url"].title: self.information_url,
            self.model_fields["license_information"].title: self.license_information,
        }


class WPModelDataProperties(BaseModel):
    """A class that holds information on how the model data is structured and formatted.

    This immutable class contains everything relevant about the data properties of a singular weather provider model.
    These properties are those relating to the nature of the data as it exists globally and not its detailed contents.


    """

    direct_access_is_possible: bool = Field(
        title="Direct Data Access is Possible",
        description="A boolean indicating whether direct access to the model data is possible."
        "Used to determine if the request can be handled directly or if it should be handed to the broker.",
    )
    data_is_predictive_in_nature: bool = Field(
        title="Data is Predictive in Nature",
        description="A boolean indicating whether the model data is predictive in nature."
        "Used to determine if the data is historical or predictive in nature.",
    )
    data_is_temporal: bool = Field(
        default=True,
        title="Data is Temporal in Nature",
        description="A boolean indicating whether the model data is temporal in nature or that its value(s) only "
        "represent a single moment/period in time.",
    )
    data_is_geospatial: bool = Field(
        default=True,
        title="Data is Geospatial",
        description="A boolean indicating whether the model data is geospatial in nature or that its value(s) "
        "represent the full zone the model is associated with.",
    )

    # Pydantic class configuration:
    model_config = ConfigDict(frozen=True, extra="forbid")

    @property
    def metadata(self) -> dict[str, bool]:
        """Return the metadata for the model data properties.

        Returns:
            dict[str, bool]:
                    The metadata for the model data properties.
        """
        return {
            self.model_fields["direct_access_is_possible"].title: self.direct_access_is_possible,
            self.model_fields["data_is_predictive_in_nature"].title: self.data_is_predictive_in_nature,
            self.model_fields["data_is_temporal"].title: self.data_is_temporal,
            self.model_fields["data_is_geospatial"].title: self.data_is_geospatial,
        }


class WPModelGeoTemporalProperties(BaseModel):
    """A class that holds the geospatial and temporal properties of a model.

    This immutable class contains everything relevant about the geospatial and temporal properties of a singular weather
    provider model. These properties represent the spatial and temporal characteristics of the model data as a whole
    and not any specific factors.
    """

    area_bounding_box: BBox | None = Field(
        default=None,
        title="Bounding Box for Model Data Geospatial Area",
        description="The bounding box for the geospatial area the model data covers. "
        "If the model data covers a single point, the eastern and western longitudes and the northern and "
        "southern latitudes should be the same.",
    )
    available_time_period: TimePeriod = Field(
        title="Available Time Period for Model Data",
        description="The time period for which the model data is available for acquisition. This doesn't need to be "
        "very accurate, but should at least give a rough idea of the time period the data covers.",
    )
    data_crs: CRS = Field(
        title="Coordinate Reference System for Model Data",
        description="The coordinate reference system (CRS) that applies to the model's data source. "
        "This should be a valid PyProj CRS.",
    )

    # Pydantic class configuration:
    model_config = ConfigDict(frozen=True, extra="forbid", arbitrary_types_allowed=True)


class WPModelDataStorageSettings(BaseModel):
    """A class that holds the data storage settings for a model.

    This immutable class contains everything relevant about the data storage settings of a singular weather provider
    model.
    """

    storage_mode: WPDataStorageMode = Field(
        default=WPDataStorageMode.NONE,
        title="Data Storage Mode",
        description="The data storage mode for the model. This indicates how the model data is stored, if at all.",
    )
    cache_size_in_mb: int = Field(
        default=512,
        title="Cache Size in Megabytes",
        description="The size of the cache in megabytes. This is the amount of memory that can be used to store the "
        "model data in memory. Ignored if the storage mode does not support a cache.",
    )
    archive_period: TimePeriod = Field(
        title="Archive Period",
        description="The period for which the model data is archived. This is the time period for which the model data "
        "is stored in the cache. Ignored if the storage mode does not support an archive.",
    )
    max_archive_size_in_mb: int = Field(
        default=1024,
        title="Maximum Archive Size in Megabytes",
        description="The maximum size of the archive in megabytes. This is the maximum amount of memory that can be "
        "used to store the model data in the archive. Ignored if the storage mode does not support an archive.",
    )
