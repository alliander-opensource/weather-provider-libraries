#!/usr/bin/env python

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-{2024}} Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

from enum import StrEnum


class WPDataStorageMode(StrEnum):
    NO_STORAGE = "No data will be stored, only processed on demand"
    ARCHIVE = "Data will be stored in an period-bound archive based on the model's settings"
    CACHE = (
        "Recent request results will be stored in a cache for recent results up to a certain size, "
        "based on the model's settings"
    )
    CACHE_AND_ARCHIVE = (
        "Data will be stored in both an period-bound archive and a cache for recent results up to a certain size "
        "for a limited time, based on the model's settings"
    )
