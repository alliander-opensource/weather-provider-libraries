#!/usr/bin/env python

#  SPDX-FileCopyrightText: 2019-2025 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0

from weather_provider_libraries.base_classes.meteo_request import MeteoRequest


class MeteoStorage:
    """Base class for storing meteo data"""

    def __init__(self):
        """Constructor"""
        self.id: str
        self.update_frequency: int = 60 * 60 * 24  # Default update frequency is 24 hours

    async def update(self, request: MeteoRequest):
        """Update the meteo data."""
        pass

    async def auto_update(self):
        """Update the meteo data automatically."""
        update_request = MeteoRequest(...)
        await self.update(update_request)

    async def get(self, request: MeteoRequest):
        """Get the meteo data"""
        pass
