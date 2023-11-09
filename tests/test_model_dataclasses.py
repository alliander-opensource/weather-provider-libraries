#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2023 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

import pytest
from pydantic import ValidationError
from pydantic_core import Url

from weather_provider_libraries.supporting_classes.model_dataclasses import WPLModelIdentity, WPLModelConfiguration
from weather_provider_libraries.supporting_classes.storage_dataclasses import WPLStorageMode


def test_valid_wpl_model_identity():
    code = "test_code"
    name = "Testing Name"
    description = "Just a testing description"
    information_url = "https://somesite.com/"
    license_information = "NOTAREALLICENSE2.0"

    wpl_model_identity = WPLModelIdentity(
        code="test_code",
        name="Testing Name",
        description="Just a testing description",
        information_url="https://somesite.com/",
        license_information="NOTAREALLICENSE2.0",
    )
    assert wpl_model_identity.metadata == {
        "Code": code,
        "Name": name,
        "Description": description,
        "Information URL": Url(information_url),
        "Licensing information": license_information,
    }


invalid_wpl_model_identities = [
    (
        "ts",
        "Testing Name",
        "Just a testing description",
        "https://somesite.com/",
        "NOTAREALLICENSE2.0",
        ValidationError,
        "String should have at least",
    ),
    (
        "test_code_too_long",
        "Testing Name",
        "Just a testing description",
        "https://somesite.com/",
        "NOTAREALLICENSE2.0",
        ValidationError,
        "String should have at most",
    ),
    (
        "test_code",
        "TSName",
        "Just a testing description",
        "https://somesite.com/",
        "NOTAREALLICENSE2.0",
        ValidationError,
        "String should have at least",
    ),
    (
        "test_code",
        "Testing Name Too Long" + ("!" * 32),
        "Just a testing description",
        "https://somesite.com/",
        "NOTAREALLICENSE2.0",
        ValidationError,
        "String should have at most",
    ),
    (
        "test_code",
        "Testing Name",
        "Description",
        "https://somesite.com/",
        "NOTAREALLICENSE2.0",
        ValidationError,
        "String should have at least",
    ),
    (
        "test_code",
        "Testing Name",
        "Just a testing description" + ("!" * 255),
        "https://somesite.com/",
        "NOTAREALLICENSE2.0",
        ValidationError,
        "String should have at most",
    ),
    (
        "test_code",
        "Testing Name",
        "Just a testing description",
        "notasiteatall",
        "NOTAREALLICENSE2.0",
        ValidationError,
        "Input should be a valid URL",
    ),
    (
        "test_code",
        "Testing Name",
        "Just a testing description",
        "https://somesite.com/",
        "LIC",
        ValidationError,
        "String should have at least",
    ),
    (
        "test_code",
        "Testing Name",
        "Just a testing description",
        "https://somesite.com/",
        "NOTAREALLICENSE2.0" + ("-" * 255),
        ValidationError,
        "String should have at most",
    ),
]


@pytest.mark.parametrize(
    "code, name, description, information_url, license_information, error_type, expected_error_string",
    invalid_wpl_model_identities,
)
def test_invalid_model_identity(
    code, name, description, information_url, license_information, error_type, expected_error_string
):
    with pytest.raises(error_type) as error_info:
        WPLModelIdentity(
            code=code,
            name=name,
            description=description,
            information_url=information_url,
            license_information=license_information,
        )
    assert expected_error_string in str(error_info.value)


def test_wpl_model_configuration_metadata():
    wpl_model_configuration = WPLModelConfiguration(direct_access=True, predictive=True)
    assert wpl_model_configuration.metadata == {
        "Can be accessed directly": True,
        "Predictive in nature": True,
        "Consist of only a single data moment": False,
        "Storage usage": WPLStorageMode.NO_STORAGE,
    }
