#!/usr/bin/env python
# -*- coding: utf-8 -*-


#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2023 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------


""" This module is used to house the ModelConfiguration Supporting Class """
from dataclasses import dataclass

import numpy as np

from weather_provider_libraries.__OLD__supporting_classes.__OLD__wpl_storage import WPLStorageMethod


@dataclass
class AccessibilitySettings:
    """

    Attributes:
        first_moment_accessible (np.datetime64 | np.timedelta64):
                                        An optional direct or relative datetime64 indication of the first moment
                                         accessible by WPL for the model. If available this value is used to generate
                                         current metadata information, pre-emptively evaluate requests for validity and
                                         filter stored data if applicable.
                                        (Please note that this moment always and only refers to a moment for which data
                                         exists. In the case of prediction datasets that generate multiple data values
                                         for a singular moment, this moment refers to the first moment of the first
                                         prediction available)
        last_moment_accessible (np.datetime64 | np.timedelta64):
                                        An optional direct or relative datetime64 indication of the last moment
                                         accessible by WPL for the model. If available this value is used to generate
                                         current metadata information, pre-emptively evaluate requests for validity and
                                         filter stored data if applicable.
                                        (Please note that this moment always and only refers to a moment for which data
                                         exists. In the case of prediction datasets that generate multiple data values
                                         for a singular moment, this moment refers to the last moment of the last
                                         prediction available)
        first_prediction_accessible (np.datetime64 | np.timedelta64):
                                        An optional direct or relative datetime64 indication of the first prediction
                                         accessible by WPL for the model. If available this value is used to generate
                                         current metadata information, pre-emptively evaluate requests for validity and
                                         filter stored data if applicable.
                                        (Please note that this moment always and only refers to a prediction for which
                                         data exists. In the case of non-prediction datasets that generate only
                                         singular data values for each moment, this refers to the first prediction
                                         moment available)
                                        Defaults to None
        last_prediction_accessible (np.datetime64 | np.timedelta64):
                                        An optional direct or relative datetime64 indication of the last prediction
                                         accessible by WPL for the model. If available this value is used to generate
                                         current metadata information, pre-emptively evaluate requests for validity and
                                         filter stored data if applicable.
                                        (Please note that this moment always and only refers to a prediction for which
                                         data exists. In the case of non-prediction datasets that generate only
                                         singular data values for each moment, this refers to the last prediction
                                         moment available)
                                        Defaults to None

    """

    first_moment_accessible: np.datetime64 | np.timedelta64 | None = None
    last_moment_accessible: np.datetime64 | np.timedelta64 | None = None
    first_prediction_accessible: np.datetime64 | np.timedelta64 | None = None
    last_prediction_accessible: np.datetime64 | np.timedelta64 | None = None

    @property
    def metadata(self) -> dict:
        return {
            "First moment in dataset": self._get_metadata(self.first_moment_accessible),
            "Last moment in dataset": self._get_metadata(self.last_moment_accessible),
            "First prediction in dataset": self._get_metadata(self.first_prediction_accessible),
            "Last prediction in dataset": self._get_metadata(self.last_prediction_accessible),
        }

    @staticmethod
    def _get_metadata(parameter: np.datetime64 | np.timedelta64 | None) -> str | np.datetime64:
        if isinstance(parameter, np.datetime64):
            return parameter
        elif isinstance(parameter, np.timedelta64):
            return np.datetime64("now") - parameter
        else:
            return "Not set"


@dataclass
class ModelConfiguration:
    """The ModelConfiguration Supporting Class.

    This Class is used to set and evaluate Model Configuration settings.

    Attributes:
        directly_accessible (bool):     A boolean used to indicate if a Model can be accessed directly.
                                        Having this value set at True means that it is possible to directly call and
                                        access any data directly from the original dataset without having to wait long
                                        enough to require tickets, or having to have data stored locally.
                                        A value of False, however indicates that to request data for this model, data
                                         will be requested either via the ticket system or from local storage if this
                                         is set.
        singular_data_moment (bool):    A boolean indicating if the data consist of only one singular moment of data.
                                         A value of True means that this model does not have a history or future of
                                          data measurement moments, but only ever holds current data.
                                         (This means that any given values for data ranges, both for configuration
                                          and for requests will be ignored entirely. In essence, this indicates that
                                          only a singular request can be made, and that is for the current data)
        predictive_dataset (bool):      A boolean indicating if the data is predictive in nature. A value of True here
                                         means that the retrieved data will have been made as a prediction.
                                        (Please note that this does NOT necessarily mean that multiple predictions are
                                         available. Data could consist of a singular data moment with a prediction of
                                         the upcoming 48 hours for example.)
        local_storage_mode (WPLStorageMethod):
                                        A WPLStorageMethod specification used to set the storage method.


    Notes:
        Please note that the singular_data_moment attribute is used to:
         1. determine if there are one or more moments of data available for filtering.
         2. if the dataset is set to predictive, determine if there are one or more predictions available for filtering.
        As such

    """

    directly_accessible: bool
    singular_data_moment: bool
    predictive_dataset: bool
    local_storage_mode: WPLStorageMethod = WPLStorageMethod.NO_STORAGE
    accessibility: AccessibilitySettings | None = None

    @property
    def metadata(self) -> dict:
        """Metadata dictionary return method used to produce metadata"""
        metadata = {
            "Directly Accessible": self.directly_accessible,
            "Fetches only a singular data moment": self.singular_data_moment,
            "Handles predictive data": self.predictive_dataset,
            "Storage Mode": self.local_storage_mode,
        }
        if not self.singular_data_moment and self.accessibility is not None:
            metadata["Accessibility"] = self.accessibility.metadata

        return metadata
