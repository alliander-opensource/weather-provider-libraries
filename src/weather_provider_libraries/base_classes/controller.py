#!/usr/bin/env python

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------


class WPLController:
    """The Weather Provider Access Suite Controller class.

    This class forms a unifying interface for all installed Weather Provider Access Suite sources and models.


    """

    def __init__(self): ...

    @property
    def metadata(self): ...

    def get_weather_data(self, source, model, request): ...
