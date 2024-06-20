#!/usr/bin/env python

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-{2024}} Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

from pydantic import ConfigDict, Field
from pydantic.main import BaseModel

from weather_provider_libraries.utility_classes.location import WPGeoLocation
from weather_provider_libraries.utility_classes.period import WPTimePeriod


class WPWeatherRequestWithoutPeriod(BaseModel):
    """A class for a weather request with a period."""

    locations: list[WPGeoLocation] = Field(
        title="Locations", description="The locations for which the weather data is requested.", min_length=1
    )
    factors: list[str] = Field(title="Factors", description="The factors for which the weather data is requested.")

    # Pydantic model configuration
    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True, extra="forbid")

    def __str__(self):
        """Return a string representation of the object."""
        return f"WPWeatherRequestWithoutPeriod(Number of locations: {len(self.locations)}), Factors: {self.factors}"


class WPWeatherRequestWithPeriod(WPWeatherRequestWithoutPeriod, BaseModel):
    """A class for a weather request with a period."""

    period: WPTimePeriod = Field(title="Period", description="The period for which the weather data is requested.")

    # Pydantic model configuration
    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True, extra="forbid")

    def __str__(self):
        """Return a string representation of the object."""
        return (
            f"WPWeatherRequestWithoutPeriod(Number of locations: {len(self.locations)}), "
            f"Period: from {self.period.start} to {self.period.end}, Factors: {self.factors}"
        )
