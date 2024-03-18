#!/usr/bin/env python
# -*- coding: utf-8 -*-


#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

import pytest

from weather_provider_libraries.validators.factor_validation import (
    split_valid_and_invalid_eccodes_factors_list_by_id_code,
    validate_eccodes_factors_list_by_id_code,
)


@pytest.mark.parametrize(
    "validation_list, filterlist, expected_error_message",
    [
        (None, None, "The potential_factors argument must be a list of integers."),
        (None, [10], "The potential_factors argument must be a list of integers."),
        ([10], "10", "The filter_list argument must be a list of integers, or None."),
    ],
)
def test_eccodes_splitter_with_invalid_inputs(
    validation_list: list[int] | None, filterlist: list[int] | str | None, expected_error_message: str
):
    """Test the eccodes splitter with invalid inputs."""
    with pytest.raises(TypeError) as type_error:
        split_valid_and_invalid_eccodes_factors_list_by_id_code(validation_list, filterlist)
    assert (
        type_error.value.args[0] == expected_error_message
    ), "Invalid error message when testing method with invalid inputs."


@pytest.mark.parametrize(
    "validation_list, filterlist, expected_result",
    [
        ([10, 200], None, ([10], [200])),
        ([10, 200], [10], ([10], [200])),
        ([10, 200], [-1], ([], [10, 200])),
    ],
)
def test_eccodes_splitter_with_valid_inputs(
    validation_list: list[int], filterlist: list[int] | None, expected_result: tuple[list[int], list[int]]
):
    """Test the eccodes splitter with valid inputs."""
    assert (
        split_valid_and_invalid_eccodes_factors_list_by_id_code(validation_list, filterlist) == expected_result
    ), "Invalid result when testing method with valid inputs."


def test_eccodes_validator():
    """Test the validate_eccodes_factors_list_by_id_code method."""
    assert (
        validate_eccodes_factors_list_by_id_code([10, 200]) == False
    ), "Invalid result when testing method with valid inputs but invalid list items."

    assert (
        validate_eccodes_factors_list_by_id_code([10]) == True
    ), "Invalid result when testing method with valid inputs and valid list items."

    with pytest.raises(TypeError) as type_error:
        validate_eccodes_factors_list_by_id_code("10")
    assert (
        type_error.value.args[0] == "The potential_factors argument must be a list of integers."
    ), "Invalid error message when testing method with invalid inputs."
