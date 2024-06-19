#!/usr/bin/env python

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-{2024}} Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

from datetime import datetime

import numpy as np
from pydantic import BaseModel, ConfigDict, PrivateAttr

from weather_provider_libraries.utils.period_utils import (
    HARMONIZED_DATETIME_FORMAT,
    HARMONIZED_TIMEDELTA_FORMAT,
    translate_datetime_to_np_datetime64,
)


class WPTimePeriod(BaseModel):
    """A class to represent a time period.

    The class is designed to handle time periods in a standardized way and can handle absolute times in the form of
    datetime and np.datetime64 objects, as well as relative times in the form of np.timedelta64 objects.

    Attributes:
        __start (np.datetime64 | np.timedelta64):
            The start of the period as a np.datetime64 or np.timedelta64 object.
        __end (np.datetime64  | np.timedelta64):
            The end of the period as a np.datetime64 or np.timedelta64 object.
    Properties:
        start (np.datetime64):
            The start of the period as resolved into a np.datetime64 object.
        end (np.datetime64):
            The end of the period as resolved into a np.datetime64 object.
        original_values (tuple):
            The original and possibly relative values of the start and end objects.
        is_a_valid_period (bool): Whether the period is valid.\

    Methods:
        The following mathematical methods are supported:
        __add__(other: PERIOD) -> PERIOD:
            Adds two periods.
        __sub__(other: PERIOD) -> PERIOD:
            Subtracts two periods.
        __contains__(other: PERIOD) -> bool:
            Checks if a period is contained in another period.

    """

    __start: np.datetime64 | np.timedelta64 = PrivateAttr()
    __end: np.datetime64 | np.timedelta64 = PrivateAttr()

    # Pydantic model configuration
    model_config = ConfigDict(arbitrary_types_allowed=True, validate_assignment=True, extra="forbid")

    def __init__(
        self, start: np.datetime64 | np.timedelta64 | datetime, end: np.datetime64 | np.timedelta64 | datetime, **data
    ):
        """Initialize the WPTimePeriod object."""
        super().__init__(**data)

        if isinstance(start, datetime):
            start = translate_datetime_to_np_datetime64(start)
        if isinstance(end, datetime):
            end = translate_datetime_to_np_datetime64(end)

        # Harmonize the np.datetime64 and np.timedelta64 object formats
        if isinstance(start, np.datetime64):
            start = start.astype(HARMONIZED_DATETIME_FORMAT)
        if isinstance(end, np.datetime64):
            end = end.astype(HARMONIZED_DATETIME_FORMAT)

        if isinstance(start, np.timedelta64):
            start = start.astype(HARMONIZED_TIMEDELTA_FORMAT)
        if isinstance(end, np.timedelta64):
            end = end.astype(HARMONIZED_TIMEDELTA_FORMAT)

        self.__start = start
        self.__end = end

    @property
    def start(self) -> np.datetime64:
        """The start of the period. Resolved from __start."""
        if isinstance(self.__start, np.timedelta64):
            return np.datetime64("now") + self.__start
        return self.__start

    @property
    def end(self) -> np.datetime64:
        """The end of the period. Resolved from __end."""
        if isinstance(self.__end, np.timedelta64):
            return np.datetime64("now") + self.__end
        return self.__end

    @property
    def original_values(self) -> tuple:
        """The base values of the start and end objects."""
        return self.__start, self.__end

    @property
    def is_a_valid_period(self) -> bool:
        """Check if the period is valid."""
        return self.start < self.end

    def _overlaps(self, other: "WPTimePeriod") -> bool:
        """Check if two periods overlap."""
        return self.start < other.end and other.start < self.end

    def __add__(self, other: "WPTimePeriod") -> "WPTimePeriod":
        """Add two periods."""
        if not isinstance(other, WPTimePeriod):
            raise ValueError("Expected a WPTimePeriod object, but got {type(other)}.")
        if not self._overlaps(other):
            raise ValueError("The periods do not overlap and cannot be added to another")
        return WPTimePeriod(min(self.start, other.start), max(self.end, other.end))

    def __sub__(self, other: "WPTimePeriod") -> "WPTimePeriod":
        """Subtract two periods."""
        if not isinstance(other, WPTimePeriod):
            raise ValueError("Expected a WPTimePeriod object, but got {type(other)}.")
        if not self._overlaps(other):
            raise ValueError("The periods do not overlap and cannot be subtracted from another")
        return WPTimePeriod(max(self.start, other.start), min(self.end, other.end))

    def __contains__(self, other) -> bool:
        """Check if a period is contained in another period."""
        if isinstance(other, np.datetime64):
            return self.start <= other <= self.end
        if isinstance(other, self.__class__):
            return self.start <= other.start and self.end >= other.end

        raise ValueError(f"Expected a WPTimePeriod or np.datetime64 object, but got {type(other)}.")

    def __str__(self) -> str:
        """Return the period as a string."""
        return f"WPTimePeriod({self.start} - {self.end})"

    def __repr__(self) -> str:
        """Return the period as a string."""
        return f"WPTimePeriod({self.start} - {self.end}) [{type(self.__start)}, {type(self.__end)}]"
