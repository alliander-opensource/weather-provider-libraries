#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2023 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

""" This ... """
from loguru import logger

from weather_provider_libraries.__old__.supporting_classes import WPLStorageIdentity, WPLStorageMode
from weather_provider_libraries.__old__.utils.calculation_utils import generate_size_string_from_value
from weather_provider_libraries.__old__.utils.validation_utils import WPLTimePeriod


class WPLBaseStorage:
    """The Base WPL Storage class

    This class provides a standardized method of storing and requesting stored data for WPL models. Any model set
     with a proper WPLStorageMode should have their WPLBaseStorage class automatically hooked up for accessing any
     stored data.

    If used with cache mode, new requests should also automatically be stored in the cache, pushing out older data if
     needed.

    If used with periodical mode, a pod / process with the WPLChronicler should be booted. The WPLChronicler should
     automatically detect the proper settings from the model's configuration file.

    """

    def __new__(
        cls, storage_identity: WPLStorageIdentity, cache_size_mb: int = None, period_stored: WPLTimePeriod = None
    ):
        obj = object.__new__(cls)
        obj.identity = storage_identity
        obj.cache_size_mb = None
        obj.period_stored = None

        if storage_identity.storage_mode == WPLStorageMode.NO_STORAGE:
            # There is no reason to set a WPLStorage class if no storage is used.
            raise ValueError(
                "The WPLStorageMode was set to [NO_STORAGE]. No WPLStorage class should be used if no data needs to be "
                "stored! Please alter either the WPLStorageMode or remove the WPLStorage initialisation."
            )

        if storage_identity.storage_mode in (WPLStorageMode.CACHE_ONLY, WPLStorageMode.CACHE_AND_PERIODICAL):
            # If a storage cache applies, a size should be set as well
            if not cache_size_mb:
                raise ValueError(
                    f"The WPLStorageMode was set to [{storage_identity.storage_mode}] but no [cache_size_mb] was given"
                )
            obj.cache_size_mb = cache_size_mb

        if storage_identity.storage_mode in (WPLStorageMode.PERIODICAL_ONLY, WPLStorageMode.CACHE_AND_PERIODICAL):
            # If a storage period applies, the period should be set as well
            if not period_stored or not isinstance(period_stored, WPLTimePeriod):
                raise ValueError(
                    f"The WPLStorageMode was set to [{storage_identity.storage_mode}] but no proper [period_stored] "
                    f"value was given. (A proper [period_stored] value should be of type [WPLTimePeriod])"
                )
            obj.period_stored = period_stored

        logger.info(f"The WPLStorage class for [{obj.identity.name}] has been successfully initialized.")
        return obj

    @property
    def code(self):
        return self.identity.code

    @property
    def name(self):
        return self.identity.name

    @property
    def metadata(self):
        metadata = self.identity.metadata
        if self.period_stored:
            metadata["First moment allowed in storage"] = self.period_stored.active_period.first_moment_allowed
            metadata["Last moment allowed in storage"] = self.period_stored.active_period.last_moment_allowed

        if self.cache_size_mb:
            metadata["Reserved Cache Size"] = generate_size_string_from_value(self.cache_size_mb, "MB")
        return metadata
