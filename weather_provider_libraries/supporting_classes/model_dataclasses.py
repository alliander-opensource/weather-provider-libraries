#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2023 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

""" This module holds all the dataclasses that make up the WPLBaseModel class """
from ipaddress import IPv4Address, IPv6Address
from typing import Optional

import pyproj.aoi
from pydantic import BaseModel, Field, HttpUrl
from pyproj import CRS
from pyproj.aoi import BBox

from weather_provider_libraries.supporting_classes.storage_dataclasses import WPLStorageMode
from weather_provider_libraries.utils.validation_utils import WPLTimePeriod


class WPLModelIdentity(BaseModel, frozen=True):
    """This Dataclass holds the settings that identify a WPLBaseModel class instance and that can serve as information
    for external and internal users.

    Attributes:
        code (str):     A string used to identify the WPL Model. In the case of non-unique code identifiers, the first
                         model using the code will be kept, and the newer model will be rejected.
        name (str):     A string used to name the WPL Model. This name functions as a short descriptor for the WPL
                         Model, allowing users to more properly identify the source and purpose of the Model.
        description (str):
                        A string used to hold a description for the WPL Model. This description is used to inform users
                         briefly about the Model's purpose, content and applicability.
        information_url (str):
                        A string holding a URL to the Model's information page. This can be a page for either the Model
                         itself, or one referring to the Model's source dataset, as long as it covers most of the
                         information for the Model on available data and available factors and traits that classify the
                         Model (and it's source)
        license_information (str):
                        A string holding information on the availability and licensing of the data source(s) that are
                         accessed for this Model. The main goal is to keep users and creators aware of any limitations
                         and usage policies they need to adhere to, to be allowed to use the source(s).

    """

    code: str = Field(min_length=4, max_length=10)
    name: str = Field(min_length=8, max_length=32)
    description: str = Field(min_length=12, max_length=255)
    information_url: HttpUrl | IPv4Address | IPv6Address
    license_information: str = Field(min_length=4, max_length=255)

    @property
    def metadata(self) -> dict[str, str]:
        """Metadata dictionary return method used to produce metadata"""
        return {
            "Code": self.code,
            "Name": self.name,
            "Description": self.description,
            "Information URL": self.information_url,
            "Licensing information": self.license_information,
        }


class WPLModelEnvironment(BaseModel, frozen=True, arbitrary_types_allowed=True):
    """This data class holds the environmental data for a WPLBaseModel class instance required to identify model
     spatial boundaries and temporal limitations.

    Attributes:
        coordinate_system (pyproj.CRS): A CRS object indicating the source dataset or view's used coordinate system.
                                    If no coordinates system applies (as with singular data points may be the case)
                                     there is no need to set this.
                                    The default value is set at "EPSG:4326", which indicates WGS84 lat/lon coordinates.
        boundary_box (pyproj.BBox):
                                    This optional tuple consisting of two tuples with each two float values, represents
                                     the boundary box within which coordinates for the dataset should lie. While
                                     WPLModels should aim to always returning the nearest point, this becomes
                                     meaningless if the dataset is bound to Alaska, but the requested data point was
                                     (for instance) for France. Therefor the intention of the boundary box is to inform
                                     users that the chosen coordinates will not result in any usable data.
        temporal_reach (WPLTimePeriod):
                                    This WPLTimePeriod object is used to set the boundary values for available moments
                                     to request. If only a singular data point is available for the model, just set
                                     both boundary values tot the same (relative) moment in time.
                                    You can use both np.datetime64 and np.timedelta64 types to set the object.
                                    (all relative moments will be calculated from the moment of "now")

    """

    boundary_box: Optional[BBox]
    temporal_reach: WPLTimePeriod
    coordinate_system: CRS = CRS("EPSG:4326")

    @property
    def metadata(self) -> dict[str, str]:
        """Metadata dictionary return method used to produce metadata"""
        current_temporal_reach = self.temporal_reach.active_period
        return {
            "Boundary box": str(self.boundary_box),
            "Coordinate system": self.coordinate_system.name,
            "First date allowed": current_temporal_reach.first_moment_allowed.tostring,
            "Last date allowed": current_temporal_reach.last_moment_allowed.tostring,
        }


class WPLModelConfiguration(BaseModel, validate_assignment=True):
    """This Dataclass holds the configuration for a WPLBaseModel class instance required for class methods to function
    properly and to inform users of what the class can do or can't.

    Attributes:
        direct_access (bool):   A boolean indicating if the model can directly access its sources without the need for
                                 tickets or the local storing of data.
        predictive (bool):      A boolean indicating if the model is predictive in nature. A model that is both
                                 predictive and has more than one data point will likely have multiple predictions
                                 covering a single moment in time.
        singular_data_point (bool):
                                A boolean indicating if the Model can retrieve only a singular point of data, based on
                                 the factor of time. Some sources can only retrieve a set of data for "now" or
                                 "the upcoming 24 hours", where that dataset has no further time based index.
                                (Meaning you'll only get singular field values for "now" or "the upcoming 24 hours".)
                                Because that renders any request for a specific moment in time meaningless, Models with
                                 this value set to True, will not evaluate any given requested time periods, but
                                 instead always supply their only available result.
                                The default value is set to False.
        local_storage_mode (WPLStorageMode):
                                A WPLStorageMode object indicating the use of any storage associated with the Model.
                                Because at times constantly requesting large amounts of data will be inefficient,
                                 multiple storage modes area available to any Model. Storage implementation is
                                 standardized, meaning this setting is all that is needed to start or stop storing data
                                 for a Model, though the Model configuration file can configure details on how much and
                                 what to store.
                                The default value is set to NO_STORAGE, indicating that no storage is needed.

    """

    direct_access: bool
    predictive: bool
    singular_data_point: bool = False
    local_storage_mode: WPLStorageMode = WPLStorageMode.NO_STORAGE

    @property
    def metadata(self) -> dict[str, str]:
        """Metadata dictionary return method used to produce metadata"""
        return {
            "Can be accessed directly": self.direct_access,
            "Predictive in nature": self.predictive,
            "Consist of only a single data moment": self.singular_data_point,
            "Storage usage": self.local_storage_mode,
        }
