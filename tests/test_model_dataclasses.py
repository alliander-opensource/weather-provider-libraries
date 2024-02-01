#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

from pathlib import Path

import numpy as np
import pytest
from pydantic import ValidationError
from pydantic_core import Url
from pyproj import CRS
from pyproj.aoi import BBox

from weather_provider_libraries.__old__.supporting_classes import (
    WPLModelIdentity,
    WPLModelConfiguration,
    WPLModelEnvironment,
)
from weather_provider_libraries.__old__.supporting_classes import WPLStorageMode
from weather_provider_libraries.__old__.utils.constant_values import DEFAULT_DATETIME_FORMAT
from weather_provider_libraries.__old__.utils.validation_utils import WPLTimePeriod


@pytest.fixture(scope="module")
def valid_model_identity_data():
    data = {
        "code": "test_code",
        "name": "Testing Name",
        "description": "Just a testing description",
        "information_url": "https://example.com",
        "license_information": "NOT_A_REAL_LICENSE 2.0",
    }
    return data


@pytest.fixture(scope="module")
def too_long_model_identity_data():
    too_long_data = {
        "code": "far_too_long_a_code",
        "name": "Testing Name is Way Too Long" + ("!" * 32),
        "description": "Testing description is way too long" + ("!" * 255),
        "information_url": "https://too_long_a_sitename.nl" + "/" + ("a" * 255),
        "license_information": "TOO LONG TO BE A LICENSE 0.1" + ("!" * 255),
    }
    return too_long_data


@pytest.fixture(scope="module")
def too_short_model_identity_data():
    too_short_data = {
        "code": "n",
        "name": "TS",
        "description": "TSD",
        "information_url": "https://n.n",
        "license_information": "A1",
    }
    return too_short_data


@pytest.fixture(scope="module")
def erroneous_model_identity_data():
    erroneous_data = {
        "code": 15,
        "name": 1234556789,
        "description": Path("Description, but hidden in another type"),
        "information_url": "ftp://ftp.insteadof.http",
        "license_information": 2.67,
    }
    return erroneous_data


def test_model_identity_is_valid(valid_model_identity_data):
    # Execution
    valid_model_identity = WPLModelIdentity(
        code=valid_model_identity_data["code"],
        name=valid_model_identity_data["name"],
        description=valid_model_identity_data["description"],
        information_url=valid_model_identity_data["information_url"],
        license_information=valid_model_identity_data["license_information"],
    )

    # Evaluation
    assert valid_model_identity.metadata == {
        "Code": valid_model_identity_data["code"],
        "Name": valid_model_identity_data["name"],
        "Description": valid_model_identity_data["description"],
        "Information URL": Url(valid_model_identity_data["information_url"]),
        "Licensing information": valid_model_identity_data["license_information"],
    }


@pytest.mark.parametrize(
    "replacement_code_source, expected_error_type, expected_error_content",
    [
        ("erroneous_model_identity_data", ValidationError, "Input should be a valid string"),
        ("too_short_model_identity_data", ValueError, "String should have at least 4 characters "),
        ("too_long_model_identity_data", ValueError, "String should have at most 12 characters"),
    ],
)
def test_invalid_code_is_used_for_model_identity(
    replacement_code_source, expected_error_type, expected_error_content, valid_model_identity_data, request
):
    # Execution
    with pytest.raises(expected_error_type) as error_info:
        _ = WPLModelIdentity(
            code=request.getfixturevalue(replacement_code_source)["code"],
            name=valid_model_identity_data["name"],
            description=valid_model_identity_data["description"],
            information_url=valid_model_identity_data["information_url"],
            license_information=valid_model_identity_data["license_information"],
        )

    # Evaluation
    assert expected_error_content in error_info.value.__str__()


@pytest.mark.parametrize(
    "replacement_code_source, expected_error_type, expected_error_content",
    [
        ("erroneous_model_identity_data", ValidationError, "Input should be a valid string"),
        ("too_short_model_identity_data", ValueError, "String should have at least 8 characters "),
        ("too_long_model_identity_data", ValueError, "String should have at most 32 characters"),
    ],
)
def test_invalid_name_is_used_for_model_identity(
    replacement_code_source, expected_error_type, expected_error_content, valid_model_identity_data, request
):
    # Execution
    with pytest.raises(expected_error_type) as error_info:
        _ = WPLModelIdentity(
            code=valid_model_identity_data["code"],
            name=request.getfixturevalue(replacement_code_source)["name"],
            description=valid_model_identity_data["description"],
            information_url=valid_model_identity_data["information_url"],
            license_information=valid_model_identity_data["license_information"],
        )

    # Evaluation
    assert expected_error_content in error_info.value.__str__()


@pytest.mark.parametrize(
    "replacement_code_source, expected_error_type, expected_error_content",
    [
        ("erroneous_model_identity_data", ValidationError, "Input should be a valid string"),
        ("too_short_model_identity_data", ValueError, "String should have at least 12 characters "),
        ("too_long_model_identity_data", ValueError, "String should have at most 255 characters"),
    ],
)
def test_invalid_description_is_used_for_model_identity(
    replacement_code_source, expected_error_type, expected_error_content, valid_model_identity_data, request
):
    # Execution
    with pytest.raises(expected_error_type) as error_info:
        _ = WPLModelIdentity(
            code=valid_model_identity_data["code"],
            name=valid_model_identity_data["name"],
            description=request.getfixturevalue(replacement_code_source)["description"],
            information_url=valid_model_identity_data["information_url"],
            license_information=valid_model_identity_data["license_information"],
        )

    # Evaluation
    assert expected_error_content in error_info.value.__str__()


@pytest.mark.parametrize(
    "replacement_code_source, expected_error_type, expected_error_content",
    [
        ("erroneous_model_identity_data", ValidationError, "Input is not a valid IPv6 address"),
    ],
)
def test_invalid_information_url_is_used_for_model_identity(
    replacement_code_source, expected_error_type, expected_error_content, valid_model_identity_data, request
):
    # Execution
    with pytest.raises(expected_error_type) as error_info:
        _ = WPLModelIdentity(
            code=valid_model_identity_data["code"],
            name=valid_model_identity_data["name"],
            description=valid_model_identity_data["description"],
            information_url=request.getfixturevalue(replacement_code_source)["information_url"],
            license_information=valid_model_identity_data["license_information"],
        )

    # Evaluation
    assert expected_error_content in error_info.value.__str__()


@pytest.mark.parametrize(
    "replacement_code_source, expected_error_type, expected_error_content",
    [
        ("erroneous_model_identity_data", ValidationError, "Input should be a valid string"),
        ("too_short_model_identity_data", ValueError, "String should have at least 4 characters "),
        ("too_long_model_identity_data", ValueError, "String should have at most 255 characters"),
    ],
)
def test_invalid_license_information_is_used_for_model_identity(
    replacement_code_source, expected_error_type, expected_error_content, valid_model_identity_data, request
):
    # Execution
    with pytest.raises(expected_error_type) as error_info:
        _ = WPLModelIdentity(
            code=valid_model_identity_data["code"],
            name=valid_model_identity_data["name"],
            description=valid_model_identity_data["description"],
            information_url=valid_model_identity_data["information_url"],
            license_information=request.getfixturevalue(replacement_code_source)["license_information"],
        )

    # Evaluation
    assert expected_error_content in error_info.value.__str__()


@pytest.mark.parametrize(
    "singular_data_point, local_storage_mode, expected_singular_data_point, expected_local_storage_mode",
    [
        (True, WPLStorageMode.NO_STORAGE, True, WPLStorageMode.NO_STORAGE),
        (False, WPLStorageMode.CACHE_ONLY, False, WPLStorageMode.CACHE_ONLY),
        (None, None, False, WPLStorageMode.NO_STORAGE),
    ],
)
def test_model_configuration_is_valid(
    singular_data_point, local_storage_mode, expected_singular_data_point, expected_local_storage_mode
):
    # Execution
    params = {"direct_access": True, "predictive": False}
    if singular_data_point is not None:
        params["singular_data_point"] = singular_data_point

    if local_storage_mode is not None:
        params["local_storage_mode"] = local_storage_mode

    model_configuration = WPLModelConfiguration(**params)

    # Evaluation
    assert model_configuration.metadata == {
        "Can be accessed directly": True,
        "Predictive in nature": False,
        "Consist of only a single data moment": expected_singular_data_point,
        "Storage usage": expected_local_storage_mode,
    }


def test_model_environment_is_valid():
    # Preparation
    temporal_reach = WPLTimePeriod(np.datetime64("2022-01-01T00:00"), np.timedelta64(5, "D"))
    bbox = BBox(west=3.31497114423, east=7.09205325687, north=53.5104033474, south=50.803721015)
    coordinate_system = CRS("EPSG:28992")  # RD New (Rijksdriehoek-coordinates)

    # Execution
    model_environment = WPLModelEnvironment(
        boundary_box=bbox, temporal_reach=temporal_reach, coordinate_system=coordinate_system
    )

    model_environment_2 = WPLModelEnvironment(
        # Timeframe only
        temporal_reach=temporal_reach
    )

    # Evaluation
    assert model_environment.metadata == {
        "Boundary box": str(bbox),
        "Coordinate system": coordinate_system.name,
        "First date allowed": temporal_reach.first_moment_allowed.astype(str),
        "Last date allowed": (np.datetime64("now") + temporal_reach.last_moment_allowed)
        .astype(DEFAULT_DATETIME_FORMAT)
        .astype(str),
    }

    assert model_environment_2.metadata == {
        "Boundary box": "None",
        "Coordinate system": CRS("EPSG:4326").name,
        "First date allowed": temporal_reach.first_moment_allowed.astype(str),
        "Last date allowed": (np.datetime64("now") + temporal_reach.last_moment_allowed)
        .astype(DEFAULT_DATETIME_FORMAT)
        .astype(str),
    }
