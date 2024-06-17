#!/usr/bin/env python

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------


class WPLModel:

    def __init__(self): ...

    @property
    def metadata(self): ...

    def get_weather_data(self, request): ...
