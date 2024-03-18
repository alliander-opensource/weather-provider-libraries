#!/usr/bin/env python
# -*- coding: utf-8 -*-


#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

"""This module is intended to provide a list of all the eccodes factors that are known to the system."""
import json

from weather_provider_libraries.data_classes.factor_related import EccodesFactor
from weather_provider_libraries.transformers.file_transformers import identify_main_project_folder

_json_file = "meteo_factors.json"
_json_file = identify_main_project_folder().joinpath("weather_provider_libraries/factor_data", _json_file)

with open(_json_file) as eccodes_factors_json_data:
    _json_loaded_values = json.load(eccodes_factors_json_data)

KNOWN_ECCODES_FACTORS_BY_ID: dict[int, EccodesFactor] = {
    int(key): EccodesFactor(
        id=int(key),
        short_name=value["shortName"],
        name=value["name"],
        description=value["description"],
        unit=value["unit"],
        harmonisation_name=value["harmonisationName"],
    )
    for key, value in _json_loaded_values.items()
}
