#!/usr/bin/env python

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------


class WPLStorage:
    ...

    # TODO:
    #   - Initialize the storage with the given configuration
    #   - Establish the storage locations and methods. (archive is time based, cache is size based)
    #   - Establish the handling of partial cache requests
    #   - Establish the handling of out of bounds archive requests
    #   - Establish the handling of overlap between cache and archive, with and without empty timeframes between them
    #   - Establish the best ZARR storage configuration for both cache and archive styled data

    def __init__(self, config):
        # 1. Store and format the given configuration
        # 2. Determine and validate the storage locations based on base configuration and source-model combination
        # 3. Test read- and write-access
        ...

    def which_data_lies_in_storage_from_selection(self, start, end, factors) -> dict:
        """Evaluate which data is available in the cache and archive, and return information on that data."""
        # 1. If a cache was set, check if the requested data can be found completely or partially within the cache
        # 1a. If the data is completely found within the cache, return that all the data was found.
        # 1b. If the data is partially found within the cache, retain the period and factors accounted for.
        # 2. If an archive was set, check if the requested data can be found completely or partially within the archive
        # 2a. If the data is completely found within the archive, return that all the data was found.
        # 2b. If the data is partially found within the archive, retain the period and factors accounted for.
        # 3. If any partial data was found, return the period(s) and factors accounted for.
        # 4. If no data was found, return that no data could be found.
        ...

    def retrieve_stored_data_from_selection(self, start, end, factors):
        """Retrieve the data from the storage based on the given selection."""
        availability = self.which_data_lies_in_storage_from_selection(start, end, factors)

        # 1. Use the availability information to format requests for the cache and/or archive.
        # 2. Retrieve the data from the cache and/or archive.
        # 3. Combine multiple sources into one dataset if needed.
        # 4. Return the data found, and the availability information, so that a model can decide what to do with the
        #    remainder.

    def store_data_in_archive(self, dataset):
        """Attempt to store the given dataset within the archive."""
        # 1.  Validate the data as being within the correct timeframe
        # 2.  Validate requirements for the data to be stored in the archive such as availability of space or issues
        #     with the data itself (incomplete or corrupt data).
        # 3.  Store the data in the archive.

    def store_data_in_cache(self, dataset):
        """Attempt to store the given dataset within the cache."""
        # 1.  Validate the data as being fitting within the set size limitations
        # 2.  Validate requirements for the data to be stored in the cache such as availability of space or issues
        #     with the data itself (incomplete or corrupt data).
        # 3.  If needed, clear enough space in the cache to store the data.
        # 4.  Store the data in the cache.

    def clear_cache_size(self, size_to_clear_in_mb):
        """Clear the cache to the given size."""
        # 1.  Validate that the size to clear is within the bounds of the cache (raise an error if not)
        # 2.  Prioritize what to clear based on the data that is stored in the cache
        #     (e.g. clear the oldest data first, or the least used data first, choose between 1 large object or
        #     multiple smaller ones, et cetera)
        # 3.  Clear the data from the cache until the size is within the given bounds.
        # 4.  Raise an error if the cache could not be cleared to the given size indicating reason and details.

    def clear_archive_period(self, start, end):
        """Clear the archive of the given period."""
        # 1.  Validate that the period to clear is within the bounds of the archive (raise an error if not)
        # 2.  Clear the data from the archive for the given period.
        # 3.  Raise an error if the archive could not be cleared for the given period indicating reason and details.
