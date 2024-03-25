#!/usr/bin/env python

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

from weather_provider_libraries import SourceIdentity, WPLMeteoSource

from dummy_source.models.dummy.dummy_model import DummyModel


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
