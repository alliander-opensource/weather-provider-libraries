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

from weather_provider_libraries.utils.validation_utils import (
    ParameterValidationSettings,
    validate_parameters_using_scheme,
)


@dataclass
class SourceIdentityInfo:
    """"""

    source_code: str
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
        parameters = {"source_code": self.source_code, "name": self.name, "description": self.description}
        validation_scheme = [
            ParameterValidationSettings("source_code", 4, 6, str, False),
            ParameterValidationSettings("name", 8, 32, str, False),
            ParameterValidationSettings("description", 32, 255, str, False),
        ]
        validate_parameters_using_scheme(parameters=parameters, validation_scheme=validation_scheme)

        if not validators.url(self.information_url):
            raise ValueError(
                "The Parameter [url] of type [URL] could not be validated as the value did not "
                f" properly validate as an URL: {self.information_url}"
            )

        self.source_code = self.source_code.lower()  # Finally lower case the source access code
        logger.debug("SourceIdentityInfo was properly initialized.")

    @property
    def metadata(self) -> dict:
        """Metadata dictionary return method used to produce metadata"""
        return {"Access code": self.source_code, "Name": self.name, "Description": self.description}
