#!/usr/bin/env python

#  SPDX-FileCopyrightText: 2019-2025 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Request(BaseModel):
    model_config = ConfigDict(...)

    # Required fields
    x: float
    y: float
    start: datetime
    end: datetime

    # Optional fields
    factors: list[str] | list[int] | None = None
    source_crs: str | None = None
    target_crs: str | None = None
    use_backwards_compatibility: bool = False
    include_wgs_coordinates: bool = False
    factors_are_original: bool = False
