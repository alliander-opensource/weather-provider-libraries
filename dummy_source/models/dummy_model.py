#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

import numpy as np

from weather_provider_libraries.data_classes.factor_related import ModelFactor
from weather_provider_libraries.data_classes.model_related import ModelIdentity, ModelProperties, ModelGeography
from weather_provider_libraries.data_classes.other import TimePeriod
from weather_provider_libraries.data_classes.storage_related import StorageMode
from weather_provider_libraries.wpl_meteo_model import WPLMeteoModel


class DummyModel(WPLMeteoModel):
    def __init__(self):
        super().__init__(
            identity=ModelIdentity(
                id="dummy",
                name="Dummy Example Model",
                description="An example of the WPL Meteo Model class in action",
                information_url="https://bull.crap",
                license_information="Just do whatever",
            ),
            properties=ModelProperties(
                predictive_model=False,
                directly_accessible=True,
                storage_mode_to_use=StorageMode.NO_STORAGE,
                singular_datapoint=False,
            ),
            geography=ModelGeography(
                time_range=TimePeriod(start=np.datetime64("2022-01-01"), end=np.datetime64("2024-04-04"))
            ),
            factor_information=[
                ModelFactor(
                    identifier="temperature",
                    linked_eccodes_factor=167,
                    unit="C",
                ),
                ModelFactor(
                    identifier="temperature",
                    linked_eccodes_factor=10,
                    unit="kilometers / hour",
                ),
            ],
        )
