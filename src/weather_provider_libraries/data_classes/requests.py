#!/usr/bin/env python


#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

from pydantic import BaseModel

from weather_provider_libraries.data_classes.commons import GeoLocation, TimePeriod


class WPLRequest(BaseModel):
    """A base class for all weather provider requests."""

    time_period: TimePeriod
    locations: list[GeoLocation]
    factors: list[str] | None = None
