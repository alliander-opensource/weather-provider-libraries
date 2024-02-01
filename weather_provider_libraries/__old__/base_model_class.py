#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2023 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------


""" This module houses the WPL Base Model class.

WPL Model classes are the core level at which the WPL project handles datasets. As such a WPL Model class can usually
 either be considered an interpretation of a dataset, or a view thereof.

"""

import xarray as xr

from weather_provider_libraries.__old__.supporting_classes import (
    WPLModelConfiguration,
    WPLModelIdentity,
    WPLModelEnvironment,
)
from weather_provider_libraries.__old__.supporting_classes.request_dataclasses import WPLMeteoRequest
from weather_provider_libraries.__old__.utils.validation_utils import WPLTimePeriod


class WPLBaseModel:
    """The WPL Base Model class.

    This base class provides the parameter and methods needed to properly set up a WPL Model for a dataset or view
     thereof.

    """

    def __new__(
        cls,
        model_settings: WPLModelSettings,  # TODO: Implement model settings frame for config_file
        model_identity: WPLModelIdentity,
        model_environment: WPLModelEnvironment,
        model_configuration: WPLModelConfiguration,
    ):
        obj = object.__new__(cls)

        # Initialise the model's identity
        obj.identity = model_identity

        # Initialise the model's environment
        obj.environment = model_environment

        # Initialise model configuration
        obj.configuration = model_configuration

        return obj

    @property
    def code(self) -> str:
        return self.identity.code

    @property
    def name(self) -> str:
        return self.identity.name

    @property
    def metadata(self) -> dict[str, str]:
        return {**self.identity.metadata, **self.environment.metadata, **self.configuration.metadata}

    @property
    def period_of_data_acquirable(self) -> WPLTimePeriod:
        """Property to retrieve the period of time set within the model environment"""
        return self.environment.temporal_reach.active_period

    def get_meteo_data(self, request: WPLMeteoRequest()) -> xr.Dataset:
        """"""

        self.validate_request()

        self._retrieve_raw_data()
        return ...

    def _retrieve_raw_data(self):
        ...
