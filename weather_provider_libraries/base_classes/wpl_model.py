#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

"""The Module housing the WPL Model base class.

The WPL Model class is the base class for handling all weather data models within the project. It provides basic 
 interfaces for requesting and manipulating weather data for the data source it is configured for in its implementation 
 class.  
"""

import xarray as xr

from weather_provider_libraries.base_classes.supporting_dataclasses.wpl_model_support_classes import (
    WPLModelIdentity,
    WPLModelEnvironment,
    WPLModelProperties,
)


class WPLModel:
    """The WPL Model base class.

    This class interfaces for requesting and manipulating weather data for the data source it is configured for in its implementation
     class.

    Attributes:
        code (str): The Model's identity code. This is used to address and identify the model.
        name (str): The Model's name. This is used to represent the model in metadata and logging messages.
        metadata (dict[str, str]): The model's metadata representation.


    Methods:
        fetch_meteorological_data()

    """

    def __new__(
        cls,
        model_identity: WPLModelIdentity,
        model_properties: WPLModelProperties,
        model_environment: WPLModelEnvironment,
    ):
        """

        Args:
            model_identity (WPLModelIdentity):
            model_properties (WPLModelConfiguration):
            model_environment (WPLModelEnvironment):
        """
        obj = object.__new__(cls)
        obj.identity = model_identity
        obj.properties = model_properties
        obj.environment = model_environment

        return obj

    @property
    def code(self) -> str:
        return self.identity.code

    @property
    def name(self) -> str:
        return self.identity.name

    @property
    def metadata(self) -> dict[str, str]:
        return {**self.identity.metadata, **self.environment.metadata, **self.properties.metadata}

    def fetch_meteorological_data(self) -> xr.Dataset:
        ...
        # Evaluate Request

        # Retrieve Raw Data

        return ...
