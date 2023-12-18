#!/usr/bin/env python
# -*- coding: utf-8 -*-


#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2023 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------


"""This module hold any utilities that can be used in a project-wide range and that have to do with object
 validation."""
from typing import Self

import numpy as np
from pydantic import ConfigDict
from pydantic.dataclasses import dataclass

from weather_provider_libraries.utils.constant_values import DEFAULT_DATETIME_FORMAT, DEFAULT_TIMEDELTA_FORMAT


@dataclass(config=ConfigDict(arbitrary_types_allowed=True))
class WPLTimePeriod:
    first_moment_allowed: np.datetime64 | np.timedelta64
    last_moment_allowed: np.datetime64 | np.timedelta64
    unconstrained: bool = False

    def __post_init__(self):
        absolute_first_moment_allowed = self.first_moment_allowed
        absolute_last_moment_allowed = self.last_moment_allowed

        if isinstance(absolute_first_moment_allowed, np.timedelta64):
            self.first_moment_allowed = self.first_moment_allowed.astype(DEFAULT_TIMEDELTA_FORMAT)
            absolute_first_moment_allowed = np.datetime64("now").astype(
                DEFAULT_DATETIME_FORMAT
            ) + absolute_first_moment_allowed.astype(DEFAULT_TIMEDELTA_FORMAT)
        else:
            self.first_moment_allowed = self.first_moment_allowed.astype(DEFAULT_DATETIME_FORMAT)

        if isinstance(absolute_last_moment_allowed, np.timedelta64):
            self.last_moment_allowed = self.last_moment_allowed.astype(DEFAULT_TIMEDELTA_FORMAT)
            absolute_last_moment_allowed = np.datetime64("now").astype(
                DEFAULT_DATETIME_FORMAT
            ) + absolute_last_moment_allowed.astype(DEFAULT_TIMEDELTA_FORMAT)
        else:
            self.last_moment_allowed = self.last_moment_allowed.astype(DEFAULT_DATETIME_FORMAT)

        if absolute_first_moment_allowed > absolute_last_moment_allowed:
            raise ValueError(
                f"The value for [first_moment_allowed](resolved as {absolute_first_moment_allowed}) lies after the "
                f"value for [last_moment_allowed](resolved as {absolute_last_moment_allowed}), which would result in an"
                f" impossible period of time."
            )

        if not self.unconstrained:
            # First time ever that someone started recording the weather
            __FIRST_ALLOWED_MOMENT_EVER = np.datetime64("1869-01-01T00:00").astype(DEFAULT_DATETIME_FORMAT)
            # Any kind of meteorological prediction over 10 years already becomes near unusable. Doubling it to be sure.
            __LAST_ALLOWED_MOMENT_EVER = np.datetime64("now").astype(DEFAULT_DATETIME_FORMAT) + np.timedelta64(
                20, "Y"
            ).astype(DEFAULT_TIMEDELTA_FORMAT)

            if absolute_first_moment_allowed < __FIRST_ALLOWED_MOMENT_EVER:
                raise ValueError(
                    f"The value given for [first_moment_allowed](resolved as {absolute_first_moment_allowed}) lies "
                    f"before the boundary set at [{__FIRST_ALLOWED_MOMENT_EVER}]. Please correct this, or "
                    f"set the parameter '_unconstrained' to [True]"
                )

            if absolute_last_moment_allowed > __LAST_ALLOWED_MOMENT_EVER:
                raise ValueError(
                    f"The value given for [last_moment_allowed](resolved as {absolute_last_moment_allowed}) lies "
                    f"after the boundary set at [{__LAST_ALLOWED_MOMENT_EVER}]. Please correct this, or "
                    f"set the hidden parameter '__unconstrained' to [True]"
                )

    @property
    def active_period(self) -> Self:
        """This method translates any relative timedelta64 components into absolute components based on the moment of
         now.

        Returns:
            WPLTimePeriod:  Another WPLTimePeriod object, with any relative np.timedelta64 components replaced by
                             absolute np.datetime64 components.

        """
        first_moment = self.first_moment_allowed
        last_moment = self.last_moment_allowed

        if not isinstance(first_moment, np.datetime64):
            first_moment = np.datetime64("now") + first_moment

        if not isinstance(last_moment, np.datetime64):
            last_moment = np.datetime64("now") + last_moment

        return WPLTimePeriod(first_moment, last_moment, self.unconstrained)
