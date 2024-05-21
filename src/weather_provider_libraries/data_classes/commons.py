#!/usr/bin/env python


#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

from datetime import datetime

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------
import numpy as np
from pydantic import BaseModel, ConfigDict, PrivateAttr

from weather_provider_libraries.utils.constants import DEFAULT_DATETIME_FORMAT, DEFAULT_TIMEDELTA_FORMAT
from weather_provider_libraries.utils.validators.datetime_validation import validation_of_datetime64_elements


class TimePeriod(BaseModel):
    """A dataclass aimed at storing simple time periods.

    Attributes:
        __start (np.datetime64 | np.timedelta64):
            The start of the time period. Passed to the class as "start" as a datetime64, timedelta64 or datetime
            object.
        __end (np.datetime64 | np.timedelta64):
            The end of the time period. Passed to the class as "end" as a datetime64, timedelta64 or datetime object.
    """

    __start: np.datetime64 | np.timedelta64 = PrivateAttr()
    __end: np.datetime64 | np.timedelta64 = PrivateAttr()

    # Pydantic class config
    model_config = ConfigDict(validate_assignment=True, arbitrary_types_allowed=True, extra="forbid")

    def __init__(
        self, start: np.datetime64 | np.timedelta64 | datetime, end: np.datetime64 | np.timedelta64 | datetime, **data
    ):
        """Initialize the TimePeriod class."""
        super().__init__(**data)
        start = validation_of_datetime64_elements(start)
        end = validation_of_datetime64_elements(end)

        if isinstance(start, np.datetime64):
            self.__start = start.astype(DEFAULT_DATETIME_FORMAT)
        else:
            self.__start = start.astype(DEFAULT_TIMEDELTA_FORMAT)

        if isinstance(end, np.datetime64):
            self.__end = end.astype(DEFAULT_DATETIME_FORMAT)
        else:
            self.__end = end.astype(DEFAULT_TIMEDELTA_FORMAT)

    @property
    def start(self) -> np.datetime64 | np.timedelta64:
        """Get the current interpretation of the __start attribute."""
        if isinstance(self.__start, np.timedelta64):
            return (np.datetime64("now") + self.__start).astype(DEFAULT_DATETIME_FORMAT)

        return self.__start

    @property
    def end(self) -> np.datetime64 | np.timedelta64:
        """Get the current interpretation of the __end attribute."""
        if isinstance(self.__end, np.timedelta64):
            return (np.datetime64("now") + self.__end).astype(DEFAULT_DATETIME_FORMAT)

        return self.__end

    @property
    def is_period_valid(self) -> bool:
        """Check if the TimePeriod object is valid."""
        return self.start < self.end and not np.isnat(self.start)

    def __str__(self):
        """Return a string representation of the TimePeriod object."""
        return f"TimePeriod(start={self.start}, end={self.end})"

    def __repr__(self):
        """Return a string representation of the TimePeriod object."""
        return f"TimePeriod(start={self.start}, end={self.end})"

    def get_current_overlap(self, other_period: "TimePeriod") -> "TimePeriod":
        """Get the current overlapping period between two TimePeriod objects if it exists.

        Notes:
            This method uses the current interpretation of the TimePeriod object to check for overlaps.
            This means that if the TimePeriod object is based on timedelta64 values, the current interpretation
            of that value will be based on the current time.

        Args:
            other_period (TimePeriod):
                The other TimePeriod object to check for overlaps with.

        Returns:
            TimePeriod:
                A TimePeriod object representing the overlapping period between the two TimePeriod objects.
                If no overlap exists, the start and end of the returned TimePeriod object will be NaT.

        """
        if self.start > other_period.end or self.end < other_period.start:
            return TimePeriod(np.datetime64("NaT"), np.datetime64("NaT"))

        return TimePeriod(max(self.start, other_period.start), min(self.end, other_period.end))

    def does_period_overlap(self, other_period: "TimePeriod") -> bool:
        """Check if the passed period overlaps with the current TimePeriod object.

        Notes:
            This method used the current interpretation of the TimePeriod object to check for overlaps.
            This means that if the TimePeriod object is based on timedelta64 values, the current interpretation
            of that value will be based on the current time. This method uses the get_current_overlap method to
            establish the current overlap between the two TimePeriod objects and then evaluates by checking if the
            start of the overlap is not NaT.

        Args:
            other_period (TimePeriod):
                The other TimePeriod object to check for overlaps with.

        Returns:
            bool:
                True if the two TimePeriod objects overlap, False otherwise.

        """
        return not np.isnat(self.get_current_overlap(other_period).start)
