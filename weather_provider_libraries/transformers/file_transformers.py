#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

import os
from pathlib import Path

from loguru import logger

_FOLDER_WITH_THIS_MODULE = Path(os.path.dirname(os.path.realpath(__file__)))
_NEEDED_CONFIG_FILES = ["", ""]


def identify_project_folders() -> list[Path]:
    """"""
    return [identify_main_project_folder(), identify_config_folder()]


def identify_main_project_folder() -> Path:
    main_project_folder = _FOLDER_WITH_THIS_MODULE.parent.parent
    logger.info(f"WP Libraries - Main Project Folder found at: {main_project_folder}")
    return main_project_folder


def identify_config_folder() -> Path:
    """"""
    list_of_possible_config_folder_locations = [
        Path(f"/etc/{project_name}/config"),
        Path(_FOLDER_WITH_THIS_MODULE.joinpath("config")),
        Path(_FOLDER_WITH_THIS_MODULE.parent.parent.joinpath("config")),
    ]

    # Evaluate environment variable settings.
    environment_config = os.getenv("WPL_CONFIG_FOLDER")
    if environment_config:
        logger.debug(f"Found a WPL_CONFIG_FOLDER environment setting: {environment_config}")
        list_of_possible_config_folder_locations = [Path(environment_config)] + list_of_possible_config_folder_locations

        print(list_of_possible_config_folder_locations)

    validate_possible_config_folder(config_path)

    # Evaluate relative folders
    # -- Verify installation or copy

    # -- Verify location based on result of previous check

    configuration_folder = _FOLDER_WITH_THIS_MODULE.parent.parent
    logger.info(f"WP Libraries - Configuration Folder found at: {configuration_folder}")
    return configuration_folder


def validate_possible_config_folder(possible_config_folder: Path):
    """This method checks a given folder path for existence and checks if the needed files to make it a configuration
     folder for this project exist within it.

    It does this by first checking if the given folder path both exists and is an actual folder. After this, if
     the first check was successful, it will check for a listing of files that should exist in a valid configuration
     folder. If successful, it will return a value of [True]. If at any point a check failed, it will return a value
     of [False].

    Notes:
        - This method will only check for the proper folder structure of a configuration folder. The actual file
           contents may still differ from what is expected from a configuration folder. However, this will be evaluated
           by the methods responsible for loading the configuration, rather than this one.


    Args:
        possible_config_folder (Path):
                A pathlib Path object containing a possible valid config folder

    Returns:
        bool: A boolean indicating if the given config folder is valid [True] or not [False]

    """
    if possible_config_folder.exists() and possible_config_folder.is_dir():
        # The suggested config path exists. Verify if the required files all exist within the folder:
        for filename in _NEEDED_CONFIG_FILES:
            file = possible_config_folder.joinpath(filename)
            if not file.exists() or not file.is_file():
                # If a needed file doesn't exist, the config folder is invalid
                raise FileNotFoundError(
                    f"A possible WPL Libraries configuration folder was found at [{possible_config_folder}], "
                    f"but it did not contain the required file:{filename}"
                )

        # The path exists, and the required files are all there. The folder itself is considered valid.
        return True

    # The given folder either didn't exist, or wasn't a folder
    raise NotADirectoryError(
        f"A possible WPL Libraries configuration folder was not found at [{possible_config_folder}]"
    )
