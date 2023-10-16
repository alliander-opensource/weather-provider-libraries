#!/usr/bin/env python
# -*- coding: utf-8 -*-


#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2023 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------


""" This module """

from dataclasses import dataclass

import numpy as np


@dataclass
class WPLQuerySettings:
    first_moment: np.datetime64 | None = None
    last_moment: np.datetime64 | None = None
    lat_or_x_coord: float | None = None
    lon_or_y_coord: float | None = None
    requested_factors: list[str] | None = None
