#!/usr/bin/env python

#  SPDX-FileCopyrightText: 2019-2025 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0

"""A base module that contains the pydantic_settings based class for the WPAS libraries."""

import re
import tempfile
import warnings
from pathlib import Path
from typing import Annotated, Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict

from weather_provider_libraries import __version__


class ProjectSettings(BaseSettings):
    """A class implementing the settings for the WPAS libraries.

    Its goal is to grant access to all settings from a singular point of origin.
    """

    # Model Configuration:
    model_config = SettingsConfigDict(env_prefix="WPAS_LIB__")

    # General Settings:
    project_name: str = Field("WPAS", alias="WPAS_PROJECT_NAME")
    version: str = __version__

    # Logger Settings:
    log_level: str = "INFO"
    log_prefix: str = project_name
    log_mode: Literal["basic", "extensive"] = "basic"
    log_file_path: Path | None = None
    log_file_retention: str = "1 week"
    log_file_rotation: str = "1 month"

    # Controller Settings:
    controller_sources: Annotated[list[str] | str, NoDecode] = "autoloader"
    controller_classical_harmonization_supported: bool = True
    controller_external_eccodes_file: Path | None = None

    # Storage Settings:
    storage_default_mode: str = "cache"
    storage_base_path: Path = Path(tempfile.gettempdir())

    # Validation Methods:
    @field_validator("controller_sources", mode="before")
    def validate_controller_sources(cls, value) -> list[str]:
        """Validate the controller sources setting.

        This method validates the controller sources setting, which should be a comma-separated list of strings,
        each containing 3-8 lowercase characters, the restriction set for source IDs.
        """
        _SOURCE_ID_PATTERN = r"^[a-z]{3,8}(?:\s*,\s*[a-z]{3,8})*$"

        if not isinstance(value, str) and not (
            isinstance(value, list) and all(isinstance(item, str) for item in value)
        ):
            raise ValueError(
                f"The <PROJECT>_CONTROLLER_SOURCES environment variable must be a string. (Found: {type(value)})"
            )

        # Clean up the string(s) and convert to lowercase for further processing.
        value = value.strip().lower() if isinstance(value, str) else [item.strip().lower() for item in value]

        if not bool(re.fullmatch(_SOURCE_ID_PATTERN, value)) and value != "autoloader":
            raise ValueError(
                "There was an invalid value found for the <PROJECT>_CONTROLLER_SOURCES environment "
                "variable. Please provide a comma-separated list of allowed controller sources, each "
                "containing 3-8 lowercase letters or leave the variable empty to use the auto-loader."
            )

        return value

    @field_validator("storage_base_path", mode="before")
    def validate_storage_base_path(cls, value) -> Path:
        """Validate the storage base path setting.

        This method validates the storage base path setting, which should point to an existing directory.
        """
        if not value.exists() or not value.is_dir():
            raise ValueError(
                "The <PROJECT>_STORAGE_BASE_PATH environment variable must point to an existing directory."
            )

        if value == Path(tempfile.gettempdir()):
            warnings.warn(
                "The storage base path is set to the system's temporary directory. This is not recommended.",
                stacklevel=2,
            )

        return value


PROJECT_SETTINGS = ProjectSettings()
