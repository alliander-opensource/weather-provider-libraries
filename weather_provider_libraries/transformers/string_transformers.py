#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

import math


def parse_bytesize_to_easily_readable(
        byte_value: int | float, current_unit: str = "MB", decimals: int = 2
) -> str:
    """This method converts of a number of bytes with a given unit into an easily readable string with the most 
     appropriate format and the requested number of decimal places.
    
    Args:
        byte_value (float):
                The number of bytes to convert. Please note that the unit will affect the actual number. 
        current_unit (str):
                The unit of the number of bytes to convert. Consists of a two-letter combination indicating the byte 
                 size (i.e. "MB" or "GB").                 
        decimals (int):
                The number of decimals to use for the output string. Eventual values will be rounded to this number of 
                 decimals.

    Returns:
        (str):  A readable string representing the byte size originally passed. 

    """
    size_names = ["B", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]  # Above TB isn't expected, but you never know...

    if not isinstance(byte_value, float) and not isinstance(byte_value, int):
        raise TypeError(
            f"When converting byte size into a readable string, a byte_size of type float or int is expected. "
            f"Received a value of type: {type(byte_value)}"
        )
    if not isinstance(current_unit, str):
        raise TypeError(
            f"When converting byte size into a readable string, the [current_unit] parameter is expected to be of "
            f"type [str]. Received a value of type: {type(current_unit)}"
        )
    if not isinstance(decimals, int):
        raise TypeError(
            f"When converting byte size into a readable string, the [decimals] parameter is expected to be of "
            f"type [int]. Received a value of type: {type(decimals)}"
        )
    if current_unit.upper() not in size_names:
        raise ValueError(
            f"When converting byte size into a readable string, the [current_unit] parameter ({current_unit}) did not "
            f"match any of the allowed values ({size_names}).")
    if decimals < 0:
        raise ValueError(
            f"When converting byte size into a readable string, "
            f"the [decimals] parameter ({decimals}) cannot be below 0."
        )

    if byte_value == 0:
        return "0B"

    current_level = size_names.index(current_unit.upper())

    size_in_bytes = byte_value * 1024 ** current_level

    best_level = int(math.floor(math.log(size_in_bytes, 1024)))
    size_at_level = round(size_in_bytes / 1024 ** best_level, decimals)
    if decimals == 0:
        size_at_level = int(size_at_level)
    return f"{size_at_level}{size_names[best_level]}"
