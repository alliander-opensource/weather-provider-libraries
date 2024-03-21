#!/usr/bin/env python

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

from weather_provider_libraries.defaults.eccodes_listing import KNOWN_ECCODES_FACTORS_BY_ID


def validate_eccodes_factors_list_by_id_code(potential_factors: list[int]) -> bool:
    """A method aimed at validating a list of eccodes factors by their suggested id code.

    Upon succes, a boolean is returned containing the result of this evaluation.

    Args:
        potential_factors (list[int]):
                The list of eccodes factors that are to be validated.

    Returns:
        bool:
                The result of the validation. If all the requested factors are valid, the method will return True.
                If any of the requested factors are invalid, however, the method will return False.

    """
    if not isinstance(potential_factors, list) or not all(isinstance(factor, int) for factor in potential_factors):
        raise TypeError("The potential_factors argument must be a list of integers.")

    return all(i in KNOWN_ECCODES_FACTORS_BY_ID for i in potential_factors)


def split_valid_and_invalid_eccodes_factors_list_by_id_code(
    potential_factors: list[int], filter_list: list[int] | None = None
) -> tuple[list[int], list[int]]:
    """This is a method aimed at splitting a list of eccodes factors into lists of valid and invalid factors.

    Factors are considered valid if they are present in the KNOWN_ECCODES_FACTORS_BY_ID dictionary, and they are in
    the filter_list. Factors are considered invalid if they are not present in the KNOWN_ECCODES_FACTORS_BY_ID
    dictionary, or if they are not in the filter_list.

    Args:
        potential_factors (list[int]):
                The list of eccodes factors (by id code) that are to be validated.
        filter_list (list[int]):
                An optional list of eccodes factors (by id code) that are to be used as a filter.
                If supplied, only factors that are present in this list can be considered valid.

    Returns:
        tuple[list[int], list[int]]:
                A tuple containing two lists. The first list contains all the valid eccodes factors, and the
                second list contains all the invalid eccodes factors.

    """
    if not isinstance(potential_factors, list) or not all(isinstance(factor, int) for factor in potential_factors):
        raise TypeError("The potential_factors argument must be a list of integers.")

    if (
        not isinstance(filter_list, list) or not all(isinstance(factor, int) for factor in filter_list)
    ) and filter_list is not None:
        raise TypeError("The filter_list argument must be a list of integers, or None.")

    if filter_list is None:
        list_of_existing_factors = [factor for factor in potential_factors if factor in KNOWN_ECCODES_FACTORS_BY_ID]
        list_of_non_existing_factors = [
            factor for factor in potential_factors if factor not in KNOWN_ECCODES_FACTORS_BY_ID
        ]
    else:
        list_of_existing_factors = [
            factor for factor in potential_factors if factor in filter_list and factor in KNOWN_ECCODES_FACTORS_BY_ID
        ]
        list_of_non_existing_factors = [
            factor
            for factor in potential_factors
            if factor not in list_of_existing_factors or factor not in KNOWN_ECCODES_FACTORS_BY_ID
        ]

    return list_of_existing_factors, list_of_non_existing_factors
