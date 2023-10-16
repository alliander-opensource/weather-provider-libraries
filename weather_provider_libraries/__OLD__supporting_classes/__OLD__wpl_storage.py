#!/usr/bin/env python
# -*- coding: utf-8 -*-


#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2023 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------


""" This module houses the WPL Storage Base Class, as well as supporting systems """

from enum import Enum


class WPLStorageMethod(str, Enum):
    """An Enum Class for describing and discerning WPL Storage Class supported storage methods"""

    NO_STORAGE = "No data stored"
    CACHE_ONLY = "Only cache is stored"
    PERIODICAL_ONLY = "A period of data is stored"
    CACHE_AND_PERIODICAL = "Both cache and a period of data are stored"
