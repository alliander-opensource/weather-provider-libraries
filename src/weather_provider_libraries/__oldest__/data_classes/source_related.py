#!/usr/bin/env python

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

from ipaddress import IPv4Address, IPv6Address

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class SourceIdentity(BaseModel):
    """A dataclass responsible for holding a WPL Meteo Source's identifying data.

    This immutable dataclass holds a number of attributes, aimed at allowing the project and its users identify and
     address the source in question. The only output besides the attributes themselves are the [metadata()] property,
     intended to retrieve a visual dictionary representation of the WPL Meteo Source that can be used for notebook or
     API purposes.

    Attributes:
        id (str):   The unique identifying code used to address the source. This is used by the project's API
                     component to identify the model.
        name (str): A short name for the source. This will be the human-readable name for this source. While it doesn't
                     need to be unique itself, it is recommended to use a unique name to prevent any confusion. This
                     name is used in logs and certain views to represent the source.
        description (str): A short description for the source. Ideally it tells of the source's purpose, background,
                     contents and applicability.
        information_url (HttpUrl | IPv4Address | IPv6Address):
                    A link holding a URL or IP address where information on the source or it's data sources can be
                    found. It should hold at least basic information on the source's identity and global usability.

    Raises:
          Pydantic generated errors if the supplied data isn't valid, or attempts are being made to change data.

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

    # Pydantic class configuration
    model_config = ConfigDict(frozen=True)

    @property
    def metadata(self) -> dict[str, str]:
        """Return a metadata dictionary representation of this SourceIdentity object."""
        return {
            "ID": self.id,
            "Name": self.name,
            "Description": self.description,
            "Information URL": str(self.information_url),
        }
