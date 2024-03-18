#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

import xarray as xr

from weather_provider_libraries.data_classes.factor_related import ModelFactor
from weather_provider_libraries.data_classes.model_related import ModelIdentity, ModelProperties, ModelGeography
from weather_provider_libraries.data_classes.other import UnitSystem


class WPLMeteoModel:
    """ """

    def __init__(
        self,
        identity: ModelIdentity,
        properties: ModelProperties,
        geography: ModelGeography,
        factor_information: list[ModelFactor],
    ):
        self.identity = identity
        self.properties = properties
        self.geography = geography
        self.factor_information = factor_information

    @property
    def id(self) -> str:
        return self.identity.id

    @property
    def name(self) -> str:
        return self.identity.name

    @property
    def metadata(self) -> dict[str, str]:
        new_metadata = self.identity.metadata.copy()
        new_metadata.update(self.properties.metadata)
        new_metadata.update(self.geography.metadata)
        return new_metadata

    @property
    def known_factors(self) -> dict[str, str]:
        known_factors = {}
        for factor in self.factor_information:
            known_factors.update(factor.metadata)
        return known_factors

    def validate(self):
        for factor in self.factor_information:
            ModelFactor.model_validate(factor)
        return True

    def convert(self, data_to_convert: xr.Dataset, target_unit_system: UnitSystem) -> xr.Dataset:
        """ """
        raise NotImplementedError

    def harmonize(self, data_to_harmonize: xr.Dataset) -> xr.Dataset:
        """ """
        raise NotImplementedError
