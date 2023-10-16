#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2023 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------


""" This module holds all the dataclasses that make up the WPLBaseStorage class """
from enum import Enum


class WPLStorageMode(str, Enum):
    NO_STORAGE = "No data stored"
    CACHE_ONLY = "Only cache is stored"
    PERIODICAL_ONLY = "A period of data is stored"
    CACHE_AND_PERIODICAL = "Both cache and a period of data are stored"
