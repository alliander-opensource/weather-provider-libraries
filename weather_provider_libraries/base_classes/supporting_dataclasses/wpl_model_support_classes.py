#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

"""This module holds supporting data classes that hold together the WPL Model base class properties.

"""
from ipaddress import IPv6Address, IPv4Address

from pydantic import BaseModel, Field, HttpUrl
from pyproj import CRS
from pyproj.aoi import BBox


class WPLModelIdentity(BaseModel, frozen=True):
    """The WPL Model supporting class responsible for establishing a WPL Model's identity components.

    This immutable class consists of a number of attributes used on creation, and a metadata property that can be used
     to represent that identity.

    Attributes:
        code (str): The code of the WPL Model to identify. This is what is used to address and identify a WPL Model
                     from within a WPL Source context.
        name (str): The name of the WPL Model to identify. This is the identity representation used in logs to
                     help identify the WPL Model. (together with the code)
        description (str): A description of the WPL Model. This should tell a user about the WPL Model's purpose,
                            background, content and applicability.
        information_url (str): A link address to the WPL Model's information page. Depending on WPL Model itself, this
                                could refer either an information page for the WPL Model itself, or an information page
                                on the WPL Model's data source. It should at least cover information on both usability
                                and known factors and traits.
        license_information (str): The License(s) applicable to the WPL Model. Depending on the source of the data for
                                    the WPL Model, this source may be either used freely, or under specific
                                    circumstances. License information should refer either to a common existing
                                    license type (like GPLv4, MPL-2, et cetera), or a custom specification. Custom
                                    specifications should always be included within the repository where the WPL
                                    Model's implementation is placed.

    """

    code: str = Field(min_length=4, max_length=12, description="WPL Model - Identity Code")
    name: str = Field(min_length=8, max_length=32, description="WPL Model - Name")
    description: str = Field(min_length=12, max_length=255, description="WPL Model - Description")
    information_url: HttpUrl | IPv4Address | IPv6Address = Field(description="WPL Model - Information URL")
    license_information: str = Field(description="WPL Model - Licensing Information")

    @property
    def metadata(self) -> dict[str, str]:
        """The metadata representation of the WPL Model's identity."""
        return {
            "code": self.code,
            "name": self.name,
            "description": self.description,
            "information_url": str(self.information_url),
            "license_information": self.license_information,
        }


class WPLModelProperties(BaseModel, frozen=True):
    """The WPL Model supporting class responsible for storing WPL Model properties.

    Model properties are those properties that directly tell of the WPL Model's possibilities.

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

    direct_access: bool = Field(description="WPL Model - Directly accessible")
    predictive: bool = Field(description="WPL Model - Predictive in nature")
    singular_data_point: bool = Field(default=False, description="WPL Model - Singular data point available")
    local_storage_mode: WPLStorageMode = Field(
        default=WPLStorageMode.NO_STORAGE, description="WPL Model - File storage mode"
    )

    @property
    def metadata(self) -> dict[str, str]:
        """The metadata representation of the WPL Model's properties."""
        return {
            "direct_access": self.direct_access,
            "predictive": self.predictive,
            "singular_data_point": self.singular_data_point,
            "storage_mode": self.local_storage_mode,
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
        datetime_range (WPLTimePeriod):
                                    This WPLTimePeriod object is used to set the boundary values for available moments
                                     to request. If only a singular data point is available for the model, just set
                                     both boundary values tot the same (relative) moment in time.
                                     You can use both np.datetime64 and np.timedelta64 types to set the object.
                                     (all relative moments will be calculated from the moment of "now")

    """

    boundary_box: BBox | None = Field(description="WPL Model - Boundary box")
    datetime_range: WPLTimePeriod = Field(description="WPL Model - Datetime range")
    coordinate_system: CRS = Field(default=CRS("EPSG:4326"), description="WPL Model - Coordinate system")

    @property
    def metadata(self) -> dict[str, str]:
        """Metadata dictionary return method used to produce metadata"""
        current_datetime_range = self.datetime_range.active_period
        return {
            "Boundary box": str(self.boundary_box),
            "Coordinate system": self.coordinate_system.name,
            "First date allowed": current_datetime_range.first_moment_allowed.astype(str),
            "Last date allowed": current_datetime_range.last_moment_allowed.astype(str),
        }
