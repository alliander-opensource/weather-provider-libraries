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
from weather_provider_libraries.data_classes.enums import DataStorageMode

"""This module contains the data-classes make up the WeatherProviderModel main base class."""


class WPModelIdentity(BaseModel):
    """A class to hold the identity of a WeatherProviderModel class.

    This immutable dataclass holds a number of attributes, aimed at allowing the project and its users identify and
         address the model in question. The only output besides the attributes themselves are the [metadata] property,
         intended to retrieve a visual dictionary representation of the WPL Meteo Model that can be used for notebook or
         API purposes.

    Attributes:
            id (str):
                The unique identifying code used to address the model. This is used by WPL Meteo Source classes and the
                 project's API component to identify the model.
            name (str):
                A short name for the model. This will be the human-readable name for this model. While it doesn't need
                to be unique itself, it is recommended to use a unique name to prevent any confusion. This name is used
                in logs and certain views to represent the model.
            description (str):
                A short description for the model. Ideally it tells of the model's purpose, background, contents and
                applicability.
            information_url (HttpUrl | IPv4Address | IPv6Address):
                A link holding a URL or IP address where information on the model or it's data source can be found.
                It should hold at least basic information on the model's known factors and usability.
            license_information(str):
                A short string holding the licensing information for the model's source data. This can be a short
                description or a list of license codes that apply, depending on what best represents the information.

    Raises:
        (Pydantic) ValidationError:
            If the supplied data isn't valid, or attempts are being made to change data using invalid data, Pydantic's
            standard range of errors will be raised.

    """

    id: str = Field(
        min_length=4,
        max_length=12,
        title="Model Identifier",
        description="Short string identifier of the model. Lower case letters only",
        pattern="^[a-z]+$",
    )
    name: str = Field(
        min_length=8,
        max_length=32,
        title="Model Name",
        description="Short identifying name of the model. Letters only",
        pattern="^[a-zA-Z ]+$",
    )
    description: str = Field(
        min_length=12,
        max_length=255,
        title="Model Description",
        description="A short description of the model. Should contain minimal data on usability and contents",
    )
    information_url: HttpUrl | IPv4Address | IPv6Address = Field(
        title="Model Information URL",
        description="A link to an URL or IP address holding extensive information on the model or it's source data.",
    )
    license_information: str = Field(
        min_length=2,
        max_length=255,
        title="Model Licensing Information",
        description="Licensing information for the model's source data. Where possible use existing licensing codes",
    )

    # Pydantic class configuration
    model_config = ConfigDict(frozen=True)

    @property
    def metadata(self) -> dict[str, str]:
        """Return a metadata dictionary representation of this ModelIdentity object."""
        return {
            "ID": self.id,
            "Name": self.name,
            "Description": self.description,
            "Information URL": str(self.information_url),
            "License Information": self.license_information,
        }


class WPModelDataProperties(BaseModel):
    """A class to hold the data properties of a WeatherProviderModel class.

    This immutable dataclass holds properties relating to the nature of the source data that the model can access.

    Attributes:
        directly_accessible (bool):
            A boolean indicating if requests will directly access the source data itself, or not. All models with this
            attribute set to [True] will allow you to specifically request data from the source itself, regardless of
            any set cache or archive. Models that do not store data at all should always have this set to [True]!
        predictive_model (bool):
            A boolean indicating if the model's source data is predictive in nature. Setting this to [True] will allow
            model data to also be requested via [prediction_moment]. The model data should of course have such a
            moment, for it to work.
        singular_datapoint (bool):
            A boolean indicating that the model's source consist of a singular datapoint. Some data sources will only
            supply data "now", meaning there is no concept of history. As such a model with this property set to [True]
             will not do anything with parameters related to timeframes.
             The default value is [False], meaning that models are by default expected to have multiple datapoints.
        storage_mode_to_use (StorageMode):
            A StorageMode object indicating the WPL Meteo Storage type to use for caching and/or archiving request
            data. This attribute is used to configure a WPL Meteo Storage object for handling data.
            The default value is [StorageMode.NO_STORAGE], meaning that no data will be stored.

    Raises:
        (Pydantic) ValidationError:
            If the supplied data isn't valid, or attempts are being made to change data using invalid data, Pydantic's
            standard range of errors will be raised.

    """

    directly_accessible: bool = Field(
        title="Model is Directly Accessible",
        description="A boolean indicating if the model's source data is directly accessible [True] or not [False]",
    )
    predictive_model: bool = Field(
        title="Model is Predictive",
        description="A boolean indicating if the model's source data is predictive in nature [True] or not [False]",
    )
    singular_datapoint: bool = Field(
        default=False,
        title="Model Output is Singular Datapoint",
        description="A boolean indicating if the model's source data is just a single datapoint [True] or not [False]",
    )
    storage_mode_to_use: DataStorageMode = Field(
        default=DataStorageMode.NONE,
        title="Model Storage Mode",
        description="A StorageMode object indicating if and how the model's source data should be stored",
    )

    # Pydantic class configuration
    model_config = ConfigDict(frozen=True)

    @property
    def metadata(self) -> dict[str, str]:
        """Return a metadata dictionary representation of this ModelProperties object."""
        return {
            "Is Directly Accessible": str(self.directly_accessible),
            "Is Predictive in Nature": str(self.predictive_model),
            "Consists of a Singular Datapoint": str(self.singular_datapoint),
            "Storage Mode": self.storage_mode_to_use.value,
        }


class WPModelGeoTemporalProperties(BaseModel):
    """A class to hold the geographical and temporal properties of a WeatherProviderModel class.

    This immutable dataclass holds properties related to the model's geographical and temporal properties, meaning that
    it contains all information on where and when the source's data can come from.

    Warnings:
        area_bounding_box:
            If the area_bounding_box attribute is not set, the model will not know if a request is out of bounds, and simply
            retrieve the data found closest to any requested coordinate, even if it is hundreds of kilometers/miles away
            from the originally requested coordinate!
        source_crs:
            The source_crs attribute is used to allow for transformations into other coordinate systems. Each CRS has its
            own boundary areas, however, which means that not every CRS may be compatible with the source CRS!

    Notes:
        time_range:
            Any np.timedelta64 relative moments used here will be calculated from the moment of "now" at the time of
            usage.

    Attributes:
        area_bounding_box (BBox):
            An optional PyProj Bounding Box object holding the source data's geographical boundaries. If set, the model
            uses this information to report requests outside these boundaries as considered invalid.
        time_range (TimePeriod):
            An TimePeriod object indicating the available time frame from which data can be retrieved from the data
            source.
        source_crs (CRS):
            A PyProj CRS object holding the CRS identity of the coordinate system used by data retrieved from the
            source data. If not set WGS84 (EPSG:4326) is assumed to be coordinate system used.
            The CRS set here is used to allow for transformations into other coordinate systems.

    Raises:
        (Pydantic) ValidationError:
            If the supplied data isn't valid, or attempts are being made to change data using invalid data, Pydantic's
            standard range of errors will be raised.

    """

    area_bounding_box: BBox | None = Field(
        default=None,
        title="Model Area Bounding Box",
        description="A PyProj BBox object representing the outer bounds of the data covered by this model's data "
        "source",
    )
    time_range: TimePeriod = Field(
        title="Model Time Range",
        description="A TimePeriod (internal class) object representing the period of time that the model's data source "
        "covers",
    )
    source_crs: CRS = Field(
        default=CRS("EPSG:4326"),
        title="Model CRS",
        description="A PyProj CRS object representing the coordinate system that the model's data source uses to "
        "supply data to the project",
    )

    # Pydantic class configuration
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    @property
    def metadata(self) -> dict[str, str]:
        """Return a metadata dictionary representation of this ModelGeography object."""
        return {
            "Source Area Bounding Box": str(self.area_bounding_box),
            "Source CRS": self.source_crs.name,
            "First Moment allowed": self.time_range.resolved_start.astype(str),
            "Last Moment allowed": self.time_range.resolved_end.astype(str),
        }
