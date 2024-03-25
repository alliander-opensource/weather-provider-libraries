#!/usr/bin/env python

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------


import numpy as np
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from weather_provider_libraries.data_classes.constants import DEFAULT_DATETIME_FORMAT, DEFAULT_TIMEDELTA_FORMAT
from weather_provider_libraries.utils.validators import validation_of_datetime64_elements

"""The purpose of this module is to house any dataclasses that don't specifically belong to one of the project's
main classes.
 
Currently, the dataclasses in here are the following:
    TimePeriod:
        A dataclass for storing simple time periods. Assures basic period and value validity for project purposes, 
        and allows for setting periods using [datetime], [np.datetime64] and [np.timedelta64]. 

"""


class TimePeriod(BaseModel):
    """A dataclass aimed at storing simple time periods."""

    start: np.datetime64 | np.timedelta64
    end: np.datetime64 | np.timedelta64

    first_moment_allowed_in_period: np.datetime64 | np.timedelta64 = Field(
        default=np.datetime64("1869-01-01T00:00").astype(DEFAULT_DATETIME_FORMAT)
    )
    last_moment_allowed_in_period: np.datetime64 | np.timedelta64 = Field(
        default=np.datetime64("now").astype(DEFAULT_DATETIME_FORMAT)
        + np.timedelta64((20 * 365) + 5, "D").astype(DEFAULT_TIMEDELTA_FORMAT)
    )

    # Pydantic class config
    model_config = ConfigDict(validate_assignment=True, arbitrary_types_allowed=True, extra="allow")

    # Pydantic validators
    validate_start = field_validator("start")(validation_of_datetime64_elements)
    validate_end = field_validator("end")(validation_of_datetime64_elements)
    validate_first_moment_allowed_in_period = field_validator("first_moment_allowed_in_period")(
        validation_of_datetime64_elements
    )
    validate_last_moment_allowed_in_period = field_validator("last_moment_allowed_in_period")(
        validation_of_datetime64_elements
    )

    @model_validator(mode="after")
    def __validate_period(self):
        """Check if the currently resolved values make up a valid period.

        Because a period based on timedelta64 values could shift from valid TimePeriod into an invalid one, this
         property allows users to verify before use that the TimePeriod is indeed still valid.

        """
        if not (self.resolved_first_moment_allowed <= self.resolved_start < self.resolved_last_moment_allowed):
            raise ValueError(
                f"TimePeriod [{self.start} - {self.end}]: The current value of [start] ({self.resolved_start}) "
                f"should always lie between the current first moment allowed ({self.resolved_first_moment_allowed}) "
                f"and the current last moment allowed ({self.resolved_last_moment_allowed})."
            )

        if not (self.resolved_first_moment_allowed < self.resolved_end <= self.resolved_last_moment_allowed):
            raise ValueError(
                f"TimePeriod [{self.start} - {self.end}]: The current value of [end] ({self.resolved_end}) "
                f"should always lie between the current first moment allowed ({self.resolved_first_moment_allowed}) "
                f"and the current last moment allowed ({self.resolved_last_moment_allowed})."
            )

        if self.resolved_start >= self.resolved_end:
            raise ValueError(
                f"A TimePeriod cannot have the resolved value for [start] ({self.resolved_start}) lie after the "
                f"resolved value for [end] ({self.resolved_end}). "
                f"Please change period values in a way that [start] lies before [end]!"
            )
        return self

    @property
    def resolved_start(self) -> np.datetime64:
        """Resolve and retrieve the start value as a np.datetime64 value."""
        return (
            self.start
            if isinstance(self.start, np.datetime64)
            else (np.datetime64("now").astype(DEFAULT_DATETIME_FORMAT) + self.start)
        )

    @property
    def resolved_end(self) -> np.datetime64:
        """Resolve and retrieve the end value as a np.datetime64 value."""
        return (
            self.end
            if isinstance(self.end, np.datetime64)
            else (np.datetime64("now").astype(DEFAULT_DATETIME_FORMAT) + self.end)
        )

    @property
    def resolved_first_moment_allowed(self) -> np.datetime64:
        """Resolve and retrieve the first_moment_allowed value as a np.datetime64 value."""
        return (
            self.first_moment_allowed_in_period
            if isinstance(self.first_moment_allowed_in_period, np.datetime64)
            else (np.datetime64("now").astype(DEFAULT_DATETIME_FORMAT) + self.first_moment_allowed_in_period)
        )

    @property
    def resolved_last_moment_allowed(self) -> np.datetime64:
        """Resolve and retrieve the last_moment_allowed value as a np.datetime64 value."""
        return (
            self.last_moment_allowed_in_period
            if isinstance(self.last_moment_allowed_in_period, np.datetime64)
            else (np.datetime64("now").astype(DEFAULT_DATETIME_FORMAT) + self.last_moment_allowed_in_period)
        )
