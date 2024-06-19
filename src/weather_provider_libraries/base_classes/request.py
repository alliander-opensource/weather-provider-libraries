#!/usr/bin/env python

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-{2024}} Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

from pydantic import Field, create_model
from pydantic.main import Model

from weather_provider_libraries.base_classes.request_related.locational_and_temporal_classes import (
    WPTimePeriod,
)
from weather_provider_libraries.utility_classes.location import WPGeoLocation


def build_weather_request_model(identifier_for_request_model: str, can_request_periods: bool = True) -> Model:
    """A function intended to create one a Weather Provider Request model specific for a model.

    Args:
        identifier_for_request_model (str):
            The name of the Weather Provider Access Suite model that the request model is intended for.
        can_request_periods (bool, optional):
            Whether the model can request periods. Defaults to True.

    Returns:
        A class with the specified fields and name

    """
    if not isinstance(identifier_for_request_model, str) or not identifier_for_request_model.isalpha():
        raise ValueError("The identifier for the request model must be a string containing only letters.")

    field_dictionary = {
        "locations": (
            list[WPGeoLocation],
            Field(title="Locations", description="The locations for which the weather data is requested."),
        ),
        "period": (
            WPTimePeriod,
            Field(title="Period", description="The period for which the weather data is requested."),
        ),
        "factors": (
            list[str] | None,
            Field(title="Factors", description="The factors for which the weather data is requested."),
        ),
    }

    if not can_request_periods:
        field_dictionary.pop("period")

    return create_model(__model_name=f"{identifier_for_request_model}Request", **field_dictionary)
