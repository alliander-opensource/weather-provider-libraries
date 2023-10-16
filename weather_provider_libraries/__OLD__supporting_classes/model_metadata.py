#!/usr/bin/env python
# -*- coding: utf-8 -*-


#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2023 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------


""" The module that houses the "WPL Model Metadata" and related classes. """
from dataclasses import dataclass

import validators
from loguru import logger
from pyproj import CRS

from weather_provider_libraries.utils.validation_utils import (
    validate_parameters_using_scheme,
    ParameterValidationSettings,
)


@dataclass
class ModelIdentity:
    """This DataClass holds basic WPL Model information"""

    model_code: str
    name: str
    description: str
    information_url: str

    def __post_init__(self):
        """DataClass Post Init method used for data validation

        Returns:
            Nothing

        Raises:
            ValueError: Every failed evaluation will result in ValueError through the
                         validate_parameters_using_scheme() method.

        """
        parameters = {"model_code": self.model_code, "name": self.name, "description": self.description}
        validation_scheme = [
            ParameterValidationSettings("model_code", 4, 6, str, False),
            ParameterValidationSettings("name", 8, 32, str, False),
            ParameterValidationSettings("description", 32, 255, str, False),
        ]
        validate_parameters_using_scheme(parameters=parameters, validation_scheme=validation_scheme)

        if not validators.url(self.information_url):
            raise ValueError(
                "The Parameter [url] of type [URL] could not be validated as the value did not "
                f" properly validate as an URL: {self.information_url}"
            )

        self.access_code = self.model_code.lower()  # Finally lower case the model access code
        logger.debug("ModelIdentityInfo was properly initialized.")

    @property
    def metadata(self) -> dict:
        """Metadata dictionary return method used to produce metadata"""
        return {"Access code": self.access_code, "Name": self.name, "Description": self.description}


@dataclass
class ModelAvailabilityInfo:
    """This DataClass holds basic WPL Model availability information"""

    license_information: str
    version_support: str
    first_moment_in_dataset: str
    last_moment_in_dataset: str
    update_frequency: str
    crs_grid_resolution: str
    crs_grid_type: CRS = CRS("EPSG:4326")

    def __post_init__(self):
        """DataClass Post Init method used for data validation

        Returns:
            Nothing

        Raises:
            ValueError: Every failed evaluation will result in ValueError through the
                         validate_parameters_using_scheme() method.

        """
        parameters = {
            "license_information": self.license_information,
            "version_support": self.version_support,
            "first_moment_in_dataset": self.first_moment_in_dataset,
            "last_moment_in_dataset": self.last_moment_in_dataset,
            "update_frequency": self.update_frequency,
            "crs_grid_resolution": self.crs_grid_resolution,
            "crs_grid_type": self.crs_grid_type,
        }
        validation_scheme = [
            ParameterValidationSettings("license_information", 4, 255, str, False),
            ParameterValidationSettings("version_support", 4, 32, str, False),
            ParameterValidationSettings("first_moment_in_dataset", 8, 120, str, False),
            ParameterValidationSettings("last_moment_in_dataset", 8, 120, str, False),
            ParameterValidationSettings("update_frequency", 8, 120, str, False),
            ParameterValidationSettings("crs_grid_resolution", 3, 120, str, False),
            ParameterValidationSettings("crs_grid_type", None, None, CRS, False),
        ]
        validate_parameters_using_scheme(parameters=parameters, validation_scheme=validation_scheme)
        logger.debug("ModelAvailabilityInfo was properly initialized.")

    @property
    def metadata(self) -> dict:
        """Metadata dictionary return method used to produce metadata"""
        return {
            "license_information": self.license_information,
            "version_support": self.version_support,
            "first_moment_in_dataset": self.first_moment_in_dataset,
            "last_moment_in_dataset": self.last_moment_in_dataset,
        }
