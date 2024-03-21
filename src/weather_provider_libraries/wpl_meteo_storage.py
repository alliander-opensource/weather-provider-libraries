#!/usr/bin/env python


#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

import xarray as xr

from weather_provider_libraries.data_classes.other import TimePeriod
from weather_provider_libraries.data_classes.storage_related import StorageConfiguration
from weather_provider_libraries.utils.validation.factor_validation import (
    split_valid_and_invalid_eccodes_factors_list_by_id_code,
)


class WPLMeteoStorage:
    """A base class for all storage classes that are used to retrieve meteo data from a storage location."""

    def __init__(self, configuration: StorageConfiguration, eccodes_factors: list[int]):
        """This is the WPLMeteoStorage class init method."""
        self.configuration = configuration

        # Validate eccodes_factors list:
        self.eccodes_factors = eccodes_factors

    def get_meteo_data(
        self, requested_locations: list[...], requested_timeframe: TimePeriod, requested_eccodes_factors: list[int]
    ) -> tuple[xr.Dataset, dict[str, str]]:
        """Retrieve meteo data from the storage location.

        Args:
            requested_locations (list[...]):
                    A list of locations for which the data is requested.
            requested_timeframe (TimePeriod):
                    A TimePeriod object that represents the timeframe for which the data is requested.
            requested_eccodes_factors (list[int]):
                    A list of eccodes factor id codes for which the data is requested.

        Returns:
            xr.Dataset:
                    An xarray dataset containing the requested data.

        """
        # Verify that the eccodes_factors are valid existing factors
        valid_eccodes_factors, invalid_eccodes_factors = split_valid_and_invalid_eccodes_factors_list_by_id_code(
            potential_factors=requested_eccodes_factors, filter_list=self.eccodes_factors
        )

        # Verify that the requested location is a valid one for the data
        valid_locations, invalid_locations = self.evaluate_requested_location(requested_locations)

        # Verify that the requested timeframe is valid for the data
        valid_part_of_timeframe, invalid_part_of_timeframe = self.evaluate_requested_timeframe(requested_timeframe)

        #
        inaccessible_data_metadata = self.parse_inaccesible_data_to_metadata(
            invalid_locations, invalid_part_of_timeframe, invalid_eccodes_factors
        )

        # Retrieve the actual data from storage
        requested_data = self._fetch_meteo_data_from_storage(
            valid_locations, valid_part_of_timeframe, valid_eccodes_factors
        )

        return requested_data, inaccessible_data_metadata

    def evaluate_requested_eccodes_factors(self, eccodes_factors: list[int]) -> tuple[list[int], list[int]]:
        """Evaluate the requested eccodes factors and return the valid and invalid factors."""
        valid_eccodes_factors = [factor in eccodes_factors for factor in self.storage.eccodes_factors]
        invalid_eccodes_factors = [factor for factor in eccodes_factors if factor not in self.storage.eccodes_factors]
        return valid_eccodes_factors, invalid_eccodes_factors

    def evaluate_requested_location(self, requested_locations: list[...]) -> tuple[list[...], list[...]]:
        """Evaluate the requested locations and return the valid and invalid locations."""
        raise NotImplementedError("This method is not implemented yet")

    def evaluate_requested_timeframe(self, requested_timeframe: TimePeriod) -> tuple[TimePeriod, TimePeriod]:
        """Evaluate the requested timeframe and return the valid and invalid parts of the timeframe."""
        raise NotImplementedError("This method is not implemented yet")
