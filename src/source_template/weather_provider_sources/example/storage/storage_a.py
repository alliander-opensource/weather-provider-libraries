#!/usr/bin/env python

#  SPDX-FileCopyrightText: 2019-2025 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0

from weather_provider_libraries.BACKUP.base_classes.meteo_storage import MeteoStorage


class StorageA(MeteoStorage):
    def __init__(self):
        super().__init__()

    def store(self, data):
        # Store data in storage A
        pass

    def retrieve(self):
        # Retrieve data from storage A
        pass

    def delete(self):
        # Delete data from storage A
        pass

    def update(self, data):
        # Update data in storage A
        pass
