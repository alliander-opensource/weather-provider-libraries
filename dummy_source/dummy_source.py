#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

from dummy_source.models.dummy_model import DummyModel

from weather_provider_libraries.data_classes.source_related import SourceIdentity
from weather_provider_libraries.wpl_meteo_source import WPLMeteoSource


class DummySource(WPLMeteoSource):
    def __init__(self):
        identity = SourceIdentity(
            id="dumdum",
            name="Dummy Source",
            description="A dummy source for testing purposes",
            information_url="https://www.example.com",
        )
        super().__init__(identity=identity)
        self.load_model(DummyModel())
