#!/usr/bin/env python

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

from weather_provider_libraries.data_classes.storage_related import WPStorageConfiguration


class WeatherProviderStorage:
    """"""

    def __init__(self, storage_configuration: WPStorageConfiguration):
        """This is the WeatherProviderStorage class init method."""
        self.configuration = storage_configuration

    @property
    def model_id(self) -> str:
        """Return the model id of the storage configuration."""
        return self.configuration.model_id

    @property
    def metadata(self) -> dict[str, str]:
        """Return the metadata of the storage configuration."""
        # TODO

        return self.configuration.dict()
