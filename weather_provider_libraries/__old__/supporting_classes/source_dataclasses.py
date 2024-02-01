#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2023 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

from ipaddress import IPv4Address, IPv6Address

from pydantic import BaseModel, Field, HttpUrl


class WPLSourceIdentity(BaseModel, frozen=True):
    """"""

    code: str = Field(min_length=4, max_length=10)
    name: str = Field(min_length=8, max_length=48)
    description: str = Field(min_length=12, max_length=255)
    information_url: HttpUrl | IPv4Address | IPv6Address

    @property
    def metadata(self) -> dict[str, str]:
        """Metadata dictionary return method used to produce metadata"""
        return {
            "Code": self.code,
            "Name": self.name,
            "Description": self.description,
            "Information URL": self.information_url.__str__(),
        }
