#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2023 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------


""" This module holds all the dataclasses that make up the WPLBaseStorage class """
from enum import Enum

from pydantic import BaseModel, Field


class WPLStorageMode(str, Enum):  # pragma: no cover
    NO_STORAGE = "No data stored"
    CACHE_ONLY = "Only cache is stored"
    PERIODICAL_ONLY = "A period of data is stored"
    CACHE_AND_PERIODICAL = "Both cache and a period of data are stored"


class WPLStorageIdentity(BaseModel, frozen=True, arbitrary_types_allowed=True, use_enum_values=True):
    code: str = Field(min_length=4, max_length=10)
    name: str = Field(min_length=8, max_length=32)
    description: str = Field(min_length=12, max_length=255)
    storage_mode: WPLStorageMode

    @property
    def metadata(self) -> dict[str, str]:
        """Metadata dictionary return method used to produce metadata"""
        return {
            "Code": self.code,
            "Name": self.name,
            "Description": self.description,
            "Storage Mode": self.storage_mode.value,
        }
