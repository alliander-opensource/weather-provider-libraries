#!/usr/bin/env python

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

from weather_provider_libraries.utils.module_finder import find_weather_sources


class WeatherProviderController:
    """The main controller class for the Weather Provider Libraries package.

    This controller is used to interact with the different weather provider libraries.

    Notes:
        This class uses the Weather Provider Source structure to check for available sources.
        Sources should be traceable by having a source module folder with a [source.py] file in it.
        Any models belonging to the source should be in a sub-folder [models] from the [source.py] file and be
        referenced from the [source.py] file.

        -- Example --
        weather_provider_libraries/
            ├── source_module/
            │   ├── models/
            │   │   ├── model.py
            │   │   └── ...
            │   ├── source.py
            │   └── ...
            └── ...
    """

    def __init__(self):
        """Initializes the WeatherProviderController class."""
        # load any available sources into the controller using the weather provider source structure
        possible_sources: set[str] = find_weather_sources()
        self.sources = self._validate_sources(possible_sources)
            
    def _validate_sources(self, possible_sources: set[str]) -> set[str]:
        """Args:
            possible_sources: 

        Returns:

        """
        for possible_source in possible_sources:
            importlib.import_module(possible_source)