#!/usr/bin/env python

#  SPDX-FileCopyrightText: 2019-2025 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0

from datetime import datetime, timedelta, timezone

import numpy as np
import pytest


def test_invalid_type_when_translating_datetime_to_np_datetime64():
    """Test that an error is raised when input is not a datetime object when converting a datetime to np.datetime64."""
    with pytest.raises(ValueError) as exc_info:
        # noinspection PyTypeChecker
        translate_datetime_to_np_datetime64("not a datetime object")
    assert "Expected a datetime object, but got <class 'str'>." in str(exc_info.value)


def test_utcoffset_when_translating_datetime_to_np_datetime64():
    """Test that a datetime is properly translated into UTC when translating to np.datetime64."""
    translated_datetime64 = translate_datetime_to_np_datetime64(
        datetime(2021, 1, 1, 0, 0, 0, tzinfo=timezone(timedelta(hours=1)))
    )
    assert translated_datetime64 == np.datetime64("2020-12-31 23:00:00")
