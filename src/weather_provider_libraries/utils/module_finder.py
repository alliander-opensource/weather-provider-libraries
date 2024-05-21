#!/usr/bin/env python

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

import importlib
import pkgutil
from importlib.util import find_spec

from loguru import logger


def find_weather_sources() -> set[str]:
    """Find all available weather sources within the project and returns their names.

    Notes:
        This function searches for all available sources within the project and returns their names using the
        weather_provider_sources structure.

    Returns:
        set[str]:
        A set containing all found source names.
    """
    logger.debug("Finding available weather sources.")
    main_package_name = "weather_provider_sources"
    source_package = importlib.import_module(main_package_name)
    source_package_path = source_package.__path__[0]

    result_set = set()

    for _, sub_package_name, is_a_package in pkgutil.iter_modules([source_package_path]):
        if is_a_package:
            full_package_name = f"{main_package_name}.{sub_package_name}"
            source_module_name = f"{full_package_name}.source"

            # check if the main module exists
            if find_spec(source_module_name):
                logger.debug(f"Found source: {sub_package_name}")
                if _check_if_source_has_models(sub_package_name):
                    logger.debug(f"Source [{sub_package_name}] was confirmed to have models. Appending to list.")
                    result_set.add(sub_package_name)

    logger.info(f"Found {len(result_set)} source(s).")
    return result_set


def _check_if_source_has_models(source_package: str) -> bool:
    """Check if a source package has models.

    Args:
        source_package (str):
            The name of the source package to check.

    Returns:
        bool:
        True if models are found, False otherwise.
    """
    logger.debug(f"Checking if source: {source_package} has models.")
    main_package_name = "weather_provider_sources"
    full_package_name = f"{main_package_name}.{source_package}"
    models_package_name = f"{full_package_name}.models"

    models_package = importlib.import_module(models_package_name)
    models_package_path = models_package.__path__[0]

    for _, possible_model, is_a_package in pkgutil.iter_modules([models_package_path]):
        if is_a_package:
            logger.debug(f"Found models for source: {possible_model}")
            return True

    return False
