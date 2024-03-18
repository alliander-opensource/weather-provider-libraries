#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

from datetime import datetime
from enum import Enum

import numpy as np
from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator

from weather_provider_libraries.defaults.constants import DEFAULT_DATETIME_FORMAT, DEFAULT_TIMEDELTA_FORMAT

"""The purpose of this module is to house any dataclasses that don't specifically belong to one of the project's 
 main classes.
 
Currently the dataclasses in here are the following:
 - TimePeriod: A dataclass for storing simple time periods. Assures basic period and value validity for project 
                purposes, and allows for setting periods using [datetime], [np.datetime64] and [np.timedelta64]. 

"""


class TimePeriod(BaseModel):
    """A dataclass aimed at storing simple time periods.

    Attributes:
        start (np.datetime64 | np.timedelta64): ...
        end (np.datetime64 | np.timedelta64): ...
        first_moment_allowed (np.datetime64 | np.timedelta64): ...
        last_moment_allowed (datetime.datetime | np.timedelta64): ...

    """

    start: np.datetime64 | np.timedelta64 = Field(title="", description="")
    end: np.datetime64 | np.timedelta64 = Field(title="", description="")
    first_moment_allowed: np.datetime64 | np.timedelta64 = Field(
        default=np.datetime64("1869-01-01T00:00").astype(DEFAULT_DATETIME_FORMAT), title="", description=""
    )
    last_moment_allowed: np.datetime64 | np.timedelta64 = Field(
        default=(
            np.datetime64("now").astype(DEFAULT_DATETIME_FORMAT)
            + np.timedelta64((20 * 365) + 5, "D").astype(DEFAULT_TIMEDELTA_FORMAT)
        ),
        title="",
        description="",
    )

    # Pydantic class config
    model_config = ConfigDict(validate_assignment=True, arbitrary_types_allowed=True, extra="allow")

    @field_validator("start", "end", "first_moment_allowed", "last_moment_allowed", mode="before")
    def __validate_fields(
        cls, value_to_validate: np.datetime64 | np.timedelta64 | datetime
    ) -> np.datetime64 | np.timedelta64:
        if isinstance(value_to_validate, datetime):
            # Convert datetime directly to np.datetime64:
            return_value = np.datetime64(value_to_validate).astype(DEFAULT_DATETIME_FORMAT)
        else:
            return_value = (
                value_to_validate.astype(DEFAULT_DATETIME_FORMAT)
                if isinstance(value_to_validate, np.datetime64)
                else value_to_validate.astype(DEFAULT_TIMEDELTA_FORMAT)
            )
        return return_value

    @model_validator(mode="after")
    def __validate_period(self):
        """Checks if the currently resolved values make up a valid period.

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
        return (
            self.start
            if isinstance(self.start, np.datetime64)
            else (np.datetime64("now").astype(DEFAULT_DATETIME_FORMAT) + self.start)
        )

    @property
    def resolved_end(self) -> np.datetime64:
        return (
            self.end
            if isinstance(self.end, np.datetime64)
            else (np.datetime64("now").astype(DEFAULT_DATETIME_FORMAT) + self.end)
        )

    @property
    def resolved_first_moment_allowed(self) -> np.datetime64:
        return (
            self.first_moment_allowed
            if isinstance(self.first_moment_allowed, np.datetime64)
            else (np.datetime64("now").astype(DEFAULT_DATETIME_FORMAT) + self.first_moment_allowed)
        )

    @property
    def resolved_last_moment_allowed(self) -> np.datetime64:
        return (
            self.last_moment_allowed
            if isinstance(self.last_moment_allowed, np.datetime64)
            else (np.datetime64("now").astype(DEFAULT_DATETIME_FORMAT) + self.last_moment_allowed)
        )


class UnitSystem(str, Enum):
    """An enumeration of the different unit systems that are supported by the project."""

    SI = "si"
    IMPERIAL = "imperial"
    US = "us"
    METRIC = "metric"
    ORIGINAL = "original"
