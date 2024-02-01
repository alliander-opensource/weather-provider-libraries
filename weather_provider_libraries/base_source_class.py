#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2023 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

""" This module houses the WPL Base Source class.

WPL Source classes are containers for WPL Models.

"""

import xarray as xr

from weather_provider_libraries.base_model_class import WPLBaseModel
from weather_provider_libraries.supporting_classes.source_dataclasses import WPLSourceIdentity


class WPLBaseSource:
    """The WPL Base Source class

    This class provides access to one or more WPL Model classes. Its purpose is to group multiple weather models based
     on their source (or nature) and to allow for the re-use of model id's.
     (For instance, if two sources carry a "daily weather" model with similar / identical data, you could label both
     using the "daily" id. This prevents builders from having to initialize a "source_1_daily" and "source_2_daily",
     reducing effort in both creation and the calling of the model.)

    """

    def __init__(self, source_identity: WPLSourceIdentity):
        # Initialise the source's identity
        self.identity = source_identity

        # Set model list
        self.models_loaded: dict[str, WPLBaseModel] = {}

    @property
    def code(self) -> str:
        return self.identity.code

    @property
    def name(self) -> str:
        return self.identity.name

    @property
    def metadata(self) -> dict[str, str | list]:
        models_list = []
        for model in self.models_loaded.values():
            models_list.append(model.metadata)

        metadata = {**self.identity.metadata, **{"models": models_list}}

        return metadata

    def load_wpl_model(self, wpl_model: WPLBaseModel):
        """This method loads a WPL Base Model based model into the source if possible.

        The method checks for duplicates and invalid types.

        Args:
            wpl_model (WPLBaseModel):   A WPLBaseModel extended model to add to this source

        Returns:
            Nothing

        Raises:
            ValueError: If a model with the same code identifier already exists within the source, a ValueError is
                        returned.
            TypeError:  If something that isn't a WPLBaseModel extended class is passed, a TypeError is returned.

        """
        if wpl_model.code in self.models_loaded.keys():
            raise ValueError(
                f"A Model with designation {wpl_model.code} already exists within this WPL Source. "
                "Loading this model is not possible."
            )

        if not issubclass(type(wpl_model), WPLBaseModel):
            raise TypeError(
                "The model passed for loading does not extend the type WPLBaseModel, as required. Actual type: "
                f"{type(wpl_model)}"
            )

        self.models_loaded[wpl_model.code.__str__()] = wpl_model

    def get_meteo(self, model_code: str) -> xr.Dataset:
        """Passthrough method for calling a specific WPL Model's get_meteo() method"""
        return self.models_loaded[model_code].get_meteo_data()
