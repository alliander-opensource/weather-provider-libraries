#!/usr/bin/env python


#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

from weather_provider_libraries.classification.model import WeatherAccessModel

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------


class WeatherAccessSource:
    """The Weather Provider Access Suite Source class.

    This class forms a unifying interface for all installed Weather Provider Access Suite sources.
    """

    def __init__(
        self,
        source_information: SourceInformation,
    ):
        """Initialize the source with the given information."""
        if not isinstance(source_information, SourceInformation):
            raise TypeError("The information should be an instance of SourceInformation.")

        self.information = source_information
        self.models: dict[str, WeatherAccessModel] = {}

    def __load_models(self):
        """Load all models for the current source.

        This method should load all models for the current source and store them in the models attribute.
        The models themselves are gathered using the source's package folder.
        """
        ...

    @property
    def model_names(self) -> set[str]:
        """Return the names of all models for the current source."""
        return set(self.models.keys())


# class WPLSource:
#
#     def __init__(self): ...
#
#     @property
#     def metadata(self):
#         # TODO: Implement this method
#         return {"source_id": self.source_id, ...: ...}
#
#     def __load_models(self): ...
#
#     def get_weather_data(self, model, weather_request: WPWeatherRequestWithoutPeriod | WPWeatherRequestWithPeriod): ...
#
#     def get_model_list(self): ...
