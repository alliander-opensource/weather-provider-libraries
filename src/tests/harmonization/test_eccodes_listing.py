#!/usr/bin/env python

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

import json
from unittest.mock import mock_open, patch

import pytest

from src.weather_provider_libraries.harmonization.eccodes_listing import (
    _load_known_eccodes_configuration_from_file,
    _validate_eccodes_config,
)


def load_known_eccodes_configuration_from_file_happy_path():
    """Test the happy path of loading the known eccodes configuration from file."""
    with (
        patch(
            "builtins.open",
            mock_open(
                read_data='{"1": {'
                '"name": "test", "shortName": "t", "description": "desc", "oldHarmonisationName": "old", '
                '"originalUnit": "o", "SIUnit": "si", "humanUnit": "h", "metricUnit": "m", '
                '"americanUnit": "a", "imperialUnit": "i"}'
                "}"
            ),
        ),
        patch(
            "src.weather_provider_libraries.harmonization.eccodes_listing.get_main_config_folder",
            return_value="path/to/config",
        ),
    ):
        result = _load_known_eccodes_configuration_from_file()
        assert len(result) == 1
        assert result[1].id == "1"


def load_known_eccodes_configuration_from_file_invalid_json():
    """Test the case where the eccodes configuration file is invalid json."""
    with (
        patch("builtins.open", mock_open(read_data="invalid json")),
        patch(
            "src.weather_provider_libraries.harmonization.eccodes_listing.get_main_config_folder",
            return_value="path/to/config",
        ),
        pytest.raises(json.JSONDecodeError),
    ):
        _load_known_eccodes_configuration_from_file()


def validate_eccodes_config_happy_path():
    """Test the happy path of validating the eccodes config."""
    eccodes_list = {
        "1": {
            "name": "test",
            "shortName": "t",
            "description": "desc",
            "oldHarmonisationName": "old",
            "originalUnit": "o",
            "SIUnit": "si",
            "humanUnit": "h",
            "metricUnit": "m",
            "americanUnit": "a",
            "imperialUnit": "i",
        }
    }
    with (
        patch("builtins.open", mock_open(read_data='{"type": "object"}')),
        patch(
            "src.weather_provider_libraries.harmonization.eccodes_listing.get_main_project_folder",
            return_value="path/to/project",
        ),
    ):
        _validate_eccodes_config(eccodes_list)


def validate_eccodes_config_invalid_schema():
    """Test the case where the eccodes config has an invalid schema."""
    eccodes_list = {
        "1": {
            "name": "test",
            "shortName": "t",
            "description": "desc",
            "oldHarmonisationName": "old",
            "originalUnit": "o",
            "SIUnit": "si",
            "humanUnit": "h",
            "metricUnit": "m",
            "americanUnit": "a",
            "imperialUnit": "i",
        }
    }
    with (
        patch("builtins.open", mock_open(read_data='{"type": "array"}')),
        patch(
            "src.weather_provider_libraries.harmonization.eccodes_listing.get_main_project_folder",
            return_value="path/to/project",
        ),
        pytest.raises(ValueError),
    ):
        _validate_eccodes_config(eccodes_list)
