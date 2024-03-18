#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

import xarray as xr

from weather_provider_libraries.data_classes.factor_related import EccodesFactor
from weather_provider_libraries.data_classes.other import UnitSystem
from weather_provider_libraries.wpl_meteo_model import WPLMeteoModel


class WPLMeteoConverter:
    """ """

    def __init__(self, eccodes_factors: dict[int, EccodesFactor] = None):
        self.known_eccodes_factors = eccodes_factors

    @property
    def metadata(self) -> dict[str, str]:
        """ """
        metadata = {}
        for factor in self.known_eccodes_factors:
            metadata[str(factor)] = self.known_eccodes_factors[factor].name
        return metadata

    def convert(
        self, data_to_convert: xr.Dataset, source_model: WPLMeteoModel, target_unit_system: UnitSystem
    ) -> xr.Dataset:
        """ """
        raise NotImplementedError
