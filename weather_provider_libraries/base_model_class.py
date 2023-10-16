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
from weather_provider_libraries.supporting_classes.model_dataclasses import (
    WPLModelConfiguration,
    WPLModelIdentity,
    WPLModelEnvironment,
)


class WPLBaseModel:
    """The WPL Base Model class.

    This base class provides the parameter and methods needed to properly set up a WPL Model for a dataset or view
     thereof.

    """

    def __new__(
        cls,
        model_data: WPLModelIdentity,
        model_environment: WPLModelEnvironment,
        model_configuration: WPLModelConfiguration,
    ):
        obj = object.__new__(cls)

        # Initialise the model's identity
        obj.code = model_data.code
        obj.name = model_data.name
        obj.metadata = model_data.metadata

        # Initialise the model's environment
        obj.environment = model_environment

        # Initialise model configuration
        obj.model_configuration = model_configuration
        obj.metadata.update(model_configuration.metadata)

        return obj
