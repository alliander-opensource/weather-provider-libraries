#!/usr/bin/env python

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

from pydantic import BaseModel

"""This module contains the factor related classes for the weather provider libraries."""


class ModelFactor(BaseModel):
    """"""

    id: str
    eccodes_id: int | None
    units: str
