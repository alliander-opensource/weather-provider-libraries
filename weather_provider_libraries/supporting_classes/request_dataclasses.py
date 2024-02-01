#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

""" This """
from pydantic import BaseModel

from weather_provider_libraries.utils.validation_utils import WPLTimePeriod, WPLCoordinateList


class WPLMeteoRequest(BaseModel):
    """This Dataclass is used to convey a request for meteorological data.

    Attributes:
        requested_period (WPLTimePeriod): ...

    """

    coordinates: WPLCoordinateList
    requested_period: WPLTimePeriod
    factors: ...


class WPLMeteoFormat(BaseModel):
    """ """

    ...
