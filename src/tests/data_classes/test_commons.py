#!/usr/bin/env python

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

import numpy as np
import pytest
from weather_provider_libraries.data_classes.commons import TimePeriod


def time_period_creation_happy_path():
    """Test the happy path of creating a TimePeriod object."""
    tp = TimePeriod(start=np.datetime64("2022-01-01"), end=np.datetime64("2022-12-31"))
    assert tp.resolved_start == np.datetime64("2022-01-01")
    assert tp.resolved_end == np.datetime64("2022-12-31")


def time_period_creation_start_after_end():
    """Test the case where the start date is after the end date."""
    with pytest.raises(ValueError):
        TimePeriod(start=np.datetime64("2022-12-31"), end=np.datetime64("2022-01-01"))


def time_period_creation_start_equal_end():
    """Test the case where the start date is equal to the end date."""
    with pytest.raises(ValueError):
        TimePeriod(start=np.datetime64("2022-01-01"), end=np.datetime64("2022-01-01"))


def time_period_creation_start_before_allowed():
    """Test the case where the start date is before the allowed start date."""
    with pytest.raises(ValueError):
        TimePeriod(start=np.datetime64("1868-12-31"), end=np.datetime64("2022-12-31"))


def time_period_creation_end_after_allowed():
    """Test the case where the end date is after the allowed end date."""
    with pytest.raises(ValueError):
        TimePeriod(start=np.datetime64("2022-01-01"), end=np.datetime64("2043-01-01"))


def time_period_creation_start_timedelta():
    """Test the case where the start date is a timedelta."""
    tp = TimePeriod(start=np.timedelta64(1, "D"), end=np.datetime64("2022-12-31"))
    assert tp.resolved_start == np.datetime64("now") + np.timedelta64(1, "D")


def time_period_creation_end_timedelta():
    """Test the case where the end date is a timedelta."""
    tp = TimePeriod(start=np.datetime64("2022-01-01"), end=np.timedelta64(1, "D"))
    assert tp.resolved_end == np.datetime64("now") + np.timedelta64(1, "D")
