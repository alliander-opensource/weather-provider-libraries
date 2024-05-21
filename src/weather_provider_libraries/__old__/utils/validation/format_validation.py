#!/usr/bin/env python

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

from jsonschema.validators import validate
from loguru import logger


def validate_json_using_schema(json_data: dict, json_schema: dict) -> bool:
    """Validate a json object using a schema and return the result.

    Args:
        json_data (dict):
                The json object that is to be validated.
        json_schema (dict):
                The json schema that is to be used for validation.

    Returns:
        bool:
                The result of the validation. If the json object is valid according to the json schema, the method will
                return True. If the json object is invalid according to the json schema, however, the method will return
                False.

    """
    try:
        validate(json_data, json_schema)
        return True
    except Exception as unknown_exception:
        logger.warning(unknown_exception.__str__())
        return False
