#!/usr/bin/env python

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

from pathlib import Path

from weather_provider_libraries.wpl_meteo_model import WPLMeteoModel


class DummyModel(WPLMeteoModel):
    def __init__(self):
        super().__init__(init_folder=Path(__file__).parent.resolve())
