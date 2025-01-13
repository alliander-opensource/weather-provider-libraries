#!/usr/bin/env python

#  SPDX-FileCopyrightText: 2019-2025 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0

from pydantic import BaseModel, ConfigDict


class MeteoRequest(BaseModel):
    """This class is the class used for any request made to the WPAS libraries project."""

    # Model Configuration
    model_config = ConfigDict()

    # Request parameters
    target_format: str
    suppress_warnings: bool = False
    