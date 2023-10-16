#!/usr/bin/env python
# -*- coding: utf-8 -*-


#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2023 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------


"""This module hold any utilities that can be used in a project-wide range and that have to do with object
 validation."""
import numpy as np
from pydantic import ConfigDict
from pydantic.dataclasses import dataclass

from weather_provider_libraries.utils.constant_values import DEFAULT_DATETIME_FORMAT


@dataclass(config=ConfigDict(arbitrary_types_allowed=True))
class WPLTimePeriod:
    first_moment_allowed: np.datetime64 | np.timedelta64
    last_moment_allowed: np.datetime64 | np.timedelta64
    _unconstrained: bool = False

    def __post_init__(self):
        self.first_moment_allowed = self.first_moment_allowed.astype(DEFAULT_DATETIME_FORMAT)
        self.last_moment_allowed = self.last_moment_allowed.astype(DEFAULT_DATETIME_FORMAT)

        if self.last_moment_allowed < self.first_moment_allowed:
            raise ValueError(
                f"The value for [first_moment_allowed]({self.first_moment_allowed}) lies after the value"
                f" for [last_moment_allowed]({self.last_moment_allowed}), which would result in an"
                f" impossible period of time."
            )

        if not self._unconstrained:
            # First time ever that someone started recording the weather
            __FIRST_ALLOWED_MOMENT_EVER = np.datetime64("1869-01-01T00:00").astype(DEFAULT_DATETIME_FORMAT)
            # Any kind of meteorological prediction over 10 years already becomes near unusable. Doubling it to be sure.
            __LAST_ALLOWED_MOMENT_EVER = np.timedelta64(20, "Y").astype(DEFAULT_DATETIME_FORMAT)

            print("GOT HERE")

            if self.first_moment_allowed < __FIRST_ALLOWED_MOMENT_EVER:
                raise ValueError(
                    f"The value given for [first_moment_allowed]({self.first_moment_allowed}) lies before "
                    f"the boundary set at [{__FIRST_ALLOWED_MOMENT_EVER}]. Please correct this, or "
                    f"set the parameter '_unconstrained' to [True]"
                )

            if self.last_moment_allowed > __LAST_ALLOWED_MOMENT_EVER:
                raise ValueError(
                    f"The value given for [first_moment_allowed]({self.last_moment_allowed}) lies before "
                    f"the boundary set at [{__LAST_ALLOWED_MOMENT_EVER}]. Please correct this, or "
                    f"set the hidden parameter '__unconstrained' to [True]"
                )
