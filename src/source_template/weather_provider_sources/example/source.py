#!/usr/bin/env python

#  SPDX-FileCopyrightText: 2019-2025 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0

from weather_provider_libraries.base_classes.meteo_source import MeteoSource


class TemplateSource(MeteoSource):
    """Template source class"""

    def __init__(self):
        """Constructor"""
        super().__init__()
        self.id = "template"
        self.update_frequency = 60 * 60 * 24  # Default update frequency is 24 hours

    def get_meteo_data(self, model_id: str, request):
        """Get the meteo data"""
        pass
