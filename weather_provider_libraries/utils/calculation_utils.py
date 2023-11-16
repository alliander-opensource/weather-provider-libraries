#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2023 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

""" This ... """


def generate_size_string_from_value(size: int | float, bytesize: str, decimals: int = 2):
    bytesize_range = ["B", "KB", "MB", "GB", "TB", "EB"]
    if bytesize not in bytesize_range:
        raise ValueError(f"Cannot generate bytesize string. Please supply a valid bytesize indicator: {bytesize_range}")

    step_in_range = bytesize_range.index(bytesize)
    while size > 1024 or size < 1:
        if size > 1024:
            step_in_range += 1
            size = size / 1024
        if size < 1:
            step_in_range -= 1
            size = size * 1024

    return f"{size:.{decimals}f}{bytesize_range[step_in_range]}"
