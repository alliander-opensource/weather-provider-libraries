#!/usr/bin/env python
# -*- coding: utf-8 -*-


#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

from weather_provider_libraries.data_classes.source_related import SourceIdentity
from weather_provider_libraries.wpl_meteo_model import WPLMeteoModel


class WPLMeteoSource:
    def __init__(self, identity: SourceIdentity):
        self.identity = identity
        self.models: dict[str, WPLMeteoModel] = {}

    def load_model(self, model: WPLMeteoModel):
        """"""
        try:
            model.validate()
        except Exception as e:
            raise ValueError(f"Model {model.id} failed to validate: {e}") from e

        self.models[model.id] = model
