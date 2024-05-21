#!/usr/bin/env python

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

from ipaddress import IPv4Address, IPv6Address

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class WPSourceIdentity(BaseModel):
    """A class representing the identity of a weather provider source.

    This immutable class contains everything relevant about the identity of a singular weather provider source.

    Attributes:
        id (str):
            A short string identifier of the Source. Lower case letters only.
        name (str):
            A short name of the Source. Letters and spaces only.
        description (str):
            A short description of the Source. Should contain a brief description of the Source.
        information_url (HttpUrl | IPv4Address | IPv6Address):
            A link to a URL or IP address holding extensive information on the model or its source data.

    Raises:
        (Pydantic) ValueError:
            If the supplied data isn't valid, or attempts are made to change data using invalid data, the Pydantic
            standard range of errors will be raised.

    """

    id: str = Field(
        min_length=3,
        max_length=12,
        title="Source Identifier",
        description="Short string identifier of the Source. Lower case letters only",
        pattern="^[a-z]+$",
    )
    name: str = Field(
        min_length=4,
        max_length=32,
        title="Source Name",
        description="Short name of the Source. Letters and spaces only",
        pattern="^[a-zA-Z ]+$",
    )
    description: str = Field(
        min_length=12,
        max_length=512,
        title="Source Description",
        description="Short description of the Source. Should contain a brief description of the Source",
    )
    information_url: HttpUrl | IPv4Address | IPv6Address = Field(
        title="Information URL",
        description="A link to a URL or IP address holding extensive information on the model or it's source data",
    )

    # Pydantic class configuration:
    model_config = ConfigDict(arbitrary_types_allowed=False, frozen=True, extra="forbid")
