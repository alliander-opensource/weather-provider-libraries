#!/usr/bin/env python
# -*- coding: utf-8 -*-


#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2023 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------


"""This module..."""
from enum import Enum, auto


class WPLHarmonisationStandard(Enum):
    ECCODES = auto()  # Harmonisation using ECCODES Parameter codes
    CLASSIC = auto()  # Harmonisation using the old method of keyword harmonisation
