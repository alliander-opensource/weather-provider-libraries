#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2023 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

from datetime import datetime

import numpy as np
import pytest
from pydantic import ValidationError

from weather_provider_libraries.utils.constant_values import DEFAULT_TIMEDELTA_FORMAT, DEFAULT_DATETIME_FORMAT
from weather_provider_libraries.utils.validation_utils import WPLTimePeriod

valid_test_periods = [
    (
        np.datetime64("2020-12-20 00:00"),
        np.datetime64("2020-12-21 23:59"),
        False,
        np.datetime64("2020-12-20 00:00"),
        np.datetime64("2020-12-21 23:59"),
    ),
    (
        np.timedelta64(-10, "Y"),
        np.datetime64("today"),
        False,
        np.datetime64("now") + np.timedelta64(-10, "Y").astype(DEFAULT_TIMEDELTA_FORMAT),
        np.datetime64("today"),
    ),
    (
        np.datetime64("2022-12-20 00:00"),
        np.timedelta64(-5, "D"),
        False,
        np.datetime64("2022-12-20 00:00"),
        np.datetime64("now") + np.timedelta64(-5, "D").astype(DEFAULT_TIMEDELTA_FORMAT),
    ),
    (
        np.timedelta64(-2, "M"),
        np.timedelta64(-1, "D"),
        False,
        np.datetime64("now") + np.timedelta64(-2, "M").astype(DEFAULT_TIMEDELTA_FORMAT),
        np.datetime64("now") + np.timedelta64(-1, "D").astype(DEFAULT_TIMEDELTA_FORMAT),
    ),
    (
        np.datetime64("1868-01-01 00:00"),
        np.timedelta64(21, "Y"),
        True,
        np.datetime64("1868-01-01 00:00"),
        np.datetime64("now") + np.timedelta64(21, "Y").astype(DEFAULT_TIMEDELTA_FORMAT),
    ),
]

invalid_test_periods = [
    (
        np.datetime64("1868-01-01 00:00"),
        np.datetime64("1868-01-02 00:00"),
        False,
        ValueError,
        "lies before the boundary set",
    ),
    (
        np.timedelta64(21, "Y"),
        np.timedelta64(22, "Y"),
        False,
        ValueError,
        "lies after the boundary set",
    ),
    (
        np.datetime64("2022-01-01 00:00"),
        np.datetime64("2021-12-31 00:00"),
        False,
        ValueError,
        "which would result in an impossible period of time.",
    ),
    (datetime(2022, 1, 1, 0, 0), datetime(2022, 1, 2, 0, 0), False, ValidationError, "Input should be an instance of"),
]


@pytest.mark.parametrize("start, end, unconstrained, calculated_start, calculated_end", valid_test_periods)
def test_wpltime_valid_periods(start, end, unconstrained, calculated_start, calculated_end):
    period = WPLTimePeriod(start, end, unconstrained).active_period

    assert period.first_moment_allowed == calculated_start.astype(DEFAULT_DATETIME_FORMAT)
    assert period.last_moment_allowed == calculated_end.astype(DEFAULT_DATETIME_FORMAT)


@pytest.mark.parametrize("start, end, unconstrained, error_type, expected_error_string", invalid_test_periods)
def test_wpltime_invalid_periods(start, end, unconstrained, error_type, expected_error_string):
    with pytest.raises(error_type) as error_info:
        WPLTimePeriod(start, end, unconstrained)
    assert expected_error_string in str(error_info.value)
