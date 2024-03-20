#!/usr/bin/env python

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------


from weather_provider_libraries.utils.transformation.file_transformers import (
    get_main_config_folder,
    get_main_project_folder,
)

MAIN_PROJECT_FOLDER = get_main_project_folder()
MAIN_CONFIG_FOLDER = get_main_config_folder()
