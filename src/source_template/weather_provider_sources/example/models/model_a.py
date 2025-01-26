#!/usr/bin/env python

#  SPDX-FileCopyrightText: 2019-2025 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0

from weather_provider_libraries.BACKUP.base_classes.meteo_model import MeteoModel


class ModelA(MeteoModel):
    """Model A class"""

    def __init__(self):
        """Constructor"""
        super().__init__()
        self.id = "model_a"

    def get_meteo_data(self, request):
        """Get the meteo data"""
        pass
