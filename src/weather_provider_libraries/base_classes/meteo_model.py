#!/usr/bin/env python

#  SPDX-FileCopyrightText: 2019-2025 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0

import xarray as xr

from weather_provider_libraries.base_classes.meteo_request import MeteoRequest


class MeteoModel:
    """This class is the base class for the WPAS libraries Meteo Models."""

    def __init__(self):
        """Initialize the model."""
        ...

    def get_meteo_data(self, request: MeteoRequest) -> xr.Dataset:
        """Get the meteo data."""
        data = self._gather_data(request)
        return self.format_data(data, request.target_format)

    def _gather_data(self, request: MeteoRequest) -> xr.Dataset:
        """Gather the data."""
        ...

    def format_data(self, data: xr.Dataset, target_format) -> xr.Dataset:
        """Process the data."""
        # Validate the data as model-data. Warn if not valid.
        self.validate_data(data)

        # Format the data
        ...

    def validate_data(self, data: xr.Dataset):
        """Validate the data."""
        # Validate data identity via metadata
        ...

        # Verify data field existence
        ...
