#!/usr/bin/env python
# -*- coding: utf-8 -*-


#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2023 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------


""" The module that houses the "WPL Base Source" class. """
from dataclasses import dataclass

from weather_provider_libraries.__OLD__supporting_classes.__OLD__wpl_model import WPLBaseModel
from weather_provider_libraries.__OLD__supporting_classes.source_metadata import SourceIdentityInfo


@dataclass
class WPLBaseSource:
    """"""

    metadata: SourceIdentityInfo
    models: dict[str, WPLBaseModel]
