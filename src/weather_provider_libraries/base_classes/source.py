#!/usr/bin/env python

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------


class WPLSource:

    @property
    def metadata(self): ...

    def __init__(self): ...

    def get_weather_data(self, model, request): ...

    def get_model_list(self): ...
