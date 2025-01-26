#!/usr/bin/env python

#  SPDX-FileCopyrightText: 2019-2025 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0

from datetime import datetime

import numpy as np
from weather_provider_libraries.BACKUP.__OLD__.base.interfaces.period import WPTimePeriod


def test_wp_time_period_initialization_with_np_datetime64():
    """Test the initialization of a WPTimePeriod object with np.datetime64 objects."""
    start = np.datetime64("2022-01-01")
    end = np.datetime64("2022-12-31")
    period = WPTimePeriod(start=start, end=end)
    assert period.start == start
    assert period.end == end


def test_wp_time_period_initialization_with_np_timedelta64():
    """Test the initialization of a WPTimePeriod object with np.timedelta64 objects."""
    start = np.timedelta64(1, "D")
    end = np.timedelta64(10, "D")
    period = WPTimePeriod(start=start, end=end)
    assert period.start == np.datetime64("now") + start
    assert period.end == np.datetime64("now") + end


def test_wp_time_period_initialization_with_datetime():
    """Test the initialization of a WPTimePeriod object with datetime objects."""
    start = datetime(2022, 1, 1)
    end = datetime(2022, 12, 31)
    period = WPTimePeriod(start=start, end=end)
    assert period.start == np.datetime64(start)
    assert period.end == np.datetime64(end)


def test_wp_time_period_invalid_initialization():
    """Test the initialization of a WPTimePeriod object with invalid values."""
    assert WPTimePeriod(start=np.datetime64("2022-12-31"), end=np.datetime64("2022-01-01")).is_a_valid_period is False


def test_wp_time_period_properties():
    """Test the properties of a WPTimePeriod object."""
    start = np.datetime64("2022-01-01")
    end = np.datetime64("2022-12-31")
    period = WPTimePeriod(start=start, end=end)
    assert period.original_values == (start, end)
    assert period.is_a_valid_period


def test_wp_time_period_overlaps():
    """Test the _overlaps method of a WPTimePeriod object."""
    period1 = WPTimePeriod(start=np.datetime64("2022-01-01"), end=np.datetime64("2022-12-31"))
    period2 = WPTimePeriod(start=np.datetime64("2022-06-01"), end=np.datetime64("2022-06-30"))
    assert period1.overlaps(period2)


def test_wp_time_period_addition():
    """Test the addition of two WPTimePeriod objects."""
    period1 = WPTimePeriod(start=np.datetime64("2022-01-01"), end=np.datetime64("2022-06-30"))
    period2 = WPTimePeriod(start=np.datetime64("2022-06-01"), end=np.datetime64("2022-12-31"))
    combined = period1 + period2
    assert combined.start == np.datetime64("2022-01-01")
    assert combined.end == np.datetime64("2022-12-31")


def test_wp_time_period_subtraction():
    """Test the subtraction of two WPTimePeriod objects."""
    period1 = WPTimePeriod(start=np.datetime64("2022-01-01"), end=np.datetime64("2022-12-31"))
    period2 = WPTimePeriod(start=np.datetime64("2022-06-01"), end=np.datetime64("2022-06-30"))
    subtracted = period1 - period2
    assert subtracted.start == np.datetime64("2022-06-01")
    assert subtracted.end == np.datetime64("2022-06-30")


def test_wp_time_period_contains():
    """Test the __contains__ method of a WPTimePeriod object."""
    period = WPTimePeriod(start=np.datetime64("2022-01-01"), end=np.datetime64("2022-12-31"))
    assert np.datetime64("2022-06-01") in period
    assert WPTimePeriod(start=np.datetime64("2022-06-01"), end=np.datetime64("2022-06-30")) in period


def test_wp_time_period_str():
    """Test the __str__ method of a WPTimePeriod object."""
    period = WPTimePeriod(start=np.datetime64("2022-01-01"), end=np.datetime64("2022-12-31"))
    assert str(period) == "WPTimePeriod(2022-01-01T00:00 - 2022-12-31T00:00)"


def test_wp_time_period_repr():
    """Test the __repr__ method of a WPTimePeriod object."""
    period = WPTimePeriod(start=np.datetime64("2022-01-01"), end=np.datetime64("2022-12-31"))
    assert (
        repr(period)
        == "WPTimePeriod(2022-01-01T00:00 - 2022-12-31T00:00) [<class 'numpy.datetime64'>, <class 'numpy.datetime64'>]"
    )
