#!/usr/bin/env python

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

"""This module is intended to provide a list of all the eccodes factors that are known to the system."""

import json

from weather_provider_libraries.data_classes.factor_related import EccodesFactor
from weather_provider_libraries.defaults.file_locations import MAIN_CONFIG_FOLDER, MAIN_PROJECT_FOLDER
from weather_provider_libraries.utils.validation.json_validation import validate_json_using_schema

_json_file = "meteo_factors.json"
_json_file = MAIN_CONFIG_FOLDER.joinpath(_json_file)
_json_schema_file = "defaults/meteo_factors.schema.json"
_json_schema_file = MAIN_PROJECT_FOLDER.joinpath(_json_schema_file)

with open(_json_file) as eccodes_factors_json_data:
    _json_loaded_values = json.load(eccodes_factors_json_data)

with open(_json_schema_file) as eccodes_factors_schema_json_data:
    _json_schema = json.load(eccodes_factors_schema_json_data)

if not validate_json_using_schema(_json_loaded_values, _json_schema):
    raise ValueError("The eccodes factors json file is not valid according to the schema.")

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
