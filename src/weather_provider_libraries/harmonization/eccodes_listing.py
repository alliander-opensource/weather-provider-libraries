#!/usr/bin/env python

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

import json

from jsonschema.validators import validate
from loguru import logger

from weather_provider_libraries.data_classes.factors import EccodesFactor, EccodesFactorDescriptors, EccodesUnitMappings
from weather_provider_libraries.utils.file_utils import get_main_config_folder, get_main_project_folder


def _load_known_eccodes_configuration_from_file() -> dict[int, EccodesFactor]:
    """Load the known eccodes configuration from a file."""
    config_folder = get_main_config_folder()
    eccodes_config_file = config_folder.joinpath("eccodes_factors.json")

    # Load the eccodes config file
    with open(eccodes_config_file) as eccodes_config_file:
        eccodes_config = json.load(eccodes_config_file)

    # Validate the eccodes config file
    _validate_eccodes_config(eccodes_config)

    # Create the known eccodes dictionary
    known_eccodes = {}
    for key in eccodes_config:
        known_eccodes[int(key)] = EccodesFactor(
            id=key,
            descriptors=EccodesFactorDescriptors(
                name=eccodes_config[key]["name"],
                short_name=eccodes_config[key]["shortName"],
                description=eccodes_config[key]["description"],
                old_harmonisation_name=eccodes_config[key]["oldHarmonisationName"],
            ),
            units=EccodesUnitMappings(
                original_unit=eccodes_config[key]["originalUnit"],
                si_unit=eccodes_config[key]["SIUnit"],
                human_unit=eccodes_config[key]["humanUnit"],
                metric_unit=eccodes_config[key]["metricUnit"],
                american_unit=eccodes_config[key]["americanUnit"],
                imperial_unit=eccodes_config[key]["imperialUnit"],
            ),
        )

    return known_eccodes


def _validate_eccodes_config(eccodes_list: any):
    """Validate a loaded eccodes json file against the schema.

    Args:
        eccodes_list (any):
            The eccodes list to validate.

    Raises:
        ValueError:
            If the eccodes list is not valid according to the schema.

    """
    json_schema_file = get_main_project_folder().joinpath("harmonization/eccodes_factor_list.schema.json")
    with open(json_schema_file) as eccodes_factors_schema_json_data:
        json_schema = json.load(eccodes_factors_schema_json_data)

    try:
        validate(eccodes_list, json_schema)
    except Exception as unknown_exception:
        logger.error(unknown_exception.__str__())
        raise ValueError("The eccodes factors json file is not valid according to the schema.") from unknown_exception


KNOWN_ECCODES_LISTING = _load_known_eccodes_configuration_from_file()
