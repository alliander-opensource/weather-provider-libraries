#!/usr/bin/env python

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

from datetime import UTC, datetime

import numpy as np
import pytest
from weather_provider_libraries.data_classes.commons import TimePeriod
from weather_provider_libraries.data_classes.constants import DEFAULT_DATETIME_FORMAT


@pytest.mark.parametrize(
    "start, end, first_allowed_start, last_allowed_end, expected_resolved_start, expected_resolved_end, "
    "expected_resolved_first_allowed_start, expected_resolved_last_allowed_end",
    [
        # np.datetime64 start and end, no changes to boundary values
        (
            np.datetime64("2022-01-01T00:00"),
            np.datetime64("2022-02-02T23:59"),
            None,
            None,
            np.datetime64("2022-01-01T00:00"),
            np.datetime64("2022-02-02T23:59"),
            None,
            None,
        ),
        # np.timedelta64 start and end, no changes to boundary values
        (
            np.timedelta64(-5, "D"),
            np.timedelta64(+6, "h"),
            None,
            None,
            np.datetime64("now") + np.timedelta64(-5, "D"),
            np.datetime64("now") + np.timedelta64(+6, "h"),
            None,
            None,
        ),
        # np.datetime64 start and end, boundary values set as np.datetime64
        (
            np.datetime64("2022-01-01T00:00"),
            np.datetime64("2022-02-02T23:59"),
            np.datetime64("2021-01-01T00:00"),
            np.datetime64("2024-01-01T00:00"),
            np.datetime64("2022-01-01T00:00"),
            np.datetime64("2022-02-02T23:59"),
            np.datetime64("2021-01-01T00:00"),
            np.datetime64("2024-01-01T00:00"),
        ),
        # np.timedelta64 start and end, boundary values set as np.timedelta64
        (
            np.timedelta64(-5, "D"),
            np.timedelta64(+6, "h"),
            np.timedelta64(-6, "D"),
            np.timedelta64(+7, "h"),
            np.datetime64("now") + np.timedelta64(-5, "D"),
            np.datetime64("now") + np.timedelta64(+6, "h"),
            np.datetime64("now") + np.timedelta64(-6, "D"),
            np.datetime64("now") + np.timedelta64(+7, "h"),
        ),
        # datetime start and end, boundary values set as datetime
        (
            datetime(2022, 1, 1, 0, 0, tzinfo=UTC),
            datetime(2022, 2, 2, 23, 59, tzinfo=UTC),
            datetime(2020, 1, 1, 0, 0, tzinfo=UTC),
            datetime(2024, 2, 2, 23, 59, tzinfo=UTC),
            np.datetime64("2022-01-01T00:00"),
            np.datetime64("2022-02-02T23:59"),
            np.datetime64("2020-01-01T00:00"),
            np.datetime64("2024-02-02T23:59"),
        ),
    ],
)
def test_time_period_valid_input(
    start,
    end,
    first_allowed_start,
    last_allowed_end,
    expected_resolved_start,
    expected_resolved_end,
    expected_resolved_first_allowed_start,
    expected_resolved_last_allowed_end,
):
    """This test evaluates variations of valid TimePeriod parameters.

    All the parametrized values should resolve to valid TimePeriods without errors and generate periods with the
    supplied expectation values.

    Notes:
        Ideally we'd like to reduce the number of input values for this test. Eight is a bit much, and we're using
        TimePeriod objects anyway.
    """
    # Generation
    print(first_allowed_start, last_allowed_end)
    if first_allowed_start is None:
        time_period = TimePeriod(start=start, end=end)
    else:
        time_period = TimePeriod(
            start=start,
            end=end,
            first_moment_allowed_in_period=first_allowed_start,
            last_moment_allowed_in_period=last_allowed_end,
        )
        # Evaluation
        assert time_period.resolved_first_moment_allowed == expected_resolved_first_allowed_start.astype(
            DEFAULT_DATETIME_FORMAT
        )
        assert time_period.resolved_last_moment_allowed == expected_resolved_last_allowed_end.astype(
            DEFAULT_DATETIME_FORMAT
        )

    # Evaluation
    assert time_period.resolved_start == expected_resolved_start.astype(DEFAULT_DATETIME_FORMAT)
    assert time_period.resolved_end == expected_resolved_end.astype(DEFAULT_DATETIME_FORMAT)


@pytest.mark.parametrize(
    "start, end, first_allowed_start, last_allowed_end, expected_error_content",
    [
        # np.datetime64 start and end, no changes to boundary values, start lies before default boundary
        (
            np.datetime64("1722-01-01T00:00"),
            np.datetime64("2022-02-02T23:59"),
            None,
            None,
            "should always lie between the current first moment allowed",
        ),
        # np.timedelta64 start and end, no changes to boundary values, end lies after default boundary
        (
            np.timedelta64(-5, "D"),
            np.timedelta64(+40, "Y"),
            None,
            None,
            "should always lie between the current first moment allowed",
        ),
        # np.datetime64 start and end, boundary values set as np.datetime64, end lies after altered boundary
        (
            np.datetime64("2022-01-01T00:00"),
            np.datetime64("2025-02-02T23:59"),
            np.datetime64("2021-01-01T00:00"),
            np.datetime64("2024-01-01T00:00"),
            "should always lie between the current first moment allowed",
        ),
        # np.timedelta64 start and end, boundary values set as np.timedelta64, start lies before altered boundary
        (
            np.timedelta64(-7, "D"),
            np.timedelta64(+6, "h"),
            np.timedelta64(-6, "D"),
            np.timedelta64(+7, "h"),
            "should always lie between the current first moment allowed",
        ),
        # np.datetime64 start and end, boundary unaltered, but start lies after end
        (
            np.datetime64("2023-01-01T00:00"),
            np.datetime64("2022-02-02T23:59"),
            None,
            None,
            "Please change period values in a way that [start] lies before [end]!",
        ),
    ],
)
def test_time_period_invalid_input_resolution(
    start, end, first_allowed_start, last_allowed_end, expected_error_content
):
    """This test evaluates variations of invalid TimePeriod parameters.

    All the parametrized values should raise ValueErrors, rather than resolve to valid TimePeriods and result in the
     expected error message for those parameters.

    """
    # Generation
    with pytest.raises(ValueError) as val_error:
        if first_allowed_start is None:
            TimePeriod(start=start, end=end)
        else:
            TimePeriod(
                start=start,
                end=end,
                first_moment_allowed_in_period=first_allowed_start,
                last_moment_allowed_in_period=last_allowed_end,
            )

    # Evaluation
    assert expected_error_content in str(val_error.value)
