#!/usr/bin/env python
# -*- coding: utf-8 -*-


#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2023 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------


""" The module that houses the "WPL Base Model" class. """
import xarray as xr
from loguru import logger

from weather_provider_libraries.__OLD__supporting_classes.harmonisation_standards import WPLHarmonisationStandard
from weather_provider_libraries.__OLD__supporting_classes.model_configuration import ModelConfiguration
from weather_provider_libraries.__OLD__supporting_classes.model_metadata import ModelIdentityInfo, ModelAvailabilityInfo
from weather_provider_libraries.__OLD__supporting_classes.query_settings import WPLQuerySettings


class WPLBaseModel:
    """The Weather Provider Libraries Base Model class.

    This class is the core class for handling meteorological data for any dataset or dataset combination within the WPL
     system. WPL Model classes should normally be housed within a Source class, as only via Source classes can Models
     be appended to a Controller (or API, within a WPLA setting) environment.

    Attributes:
        ...  # TODO: Write down attributes

    """

    def __init__(
        self,
        base_information: ModelIdentityInfo,
        availability_information: ModelAvailabilityInfo,
        configuration: ModelConfiguration,
    ):
        """Class Initializer"""
        self.base_information = base_information
        self._partial_metadata = {
            "model_info": base_information.metadata,
            "model_availability": availability_information.metadata,
        }
        self.configuration = configuration
        logger.info(f"WPL Model initialisation of model [{self.base_information.name}] has completed successfully.")

    @property
    def metadata(self) -> dict:
        """Metadata property method used to retrieve metadata"""
        metadata = self._partial_metadata
        metadata["model_configuration"] = self.configuration.metadata
        return metadata

    def get_standardized_model_data(
        self, query: WPLQuerySettings, standard_to_use: WPLHarmonisationStandard = WPLHarmonisationStandard.ECCODES
    ) -> xr.Dataset:
        """

        Args:
            query (WPLQuerySettings):   The query-parameters to request data by
            standard_to_use (WPLHarmonisationStandard):
                                        The HarmonisationStandard to use to format the output.
                                        Default is the ECCODES Parameter ID harmonisation method.

        Returns:
            xarray.Dataset: A Xarray Dataset holding the retrieved data, harmonised according to the set standard.

        """
        raw_data_dataset = self._retrieve_raw_data_as_dataset(query)

        self._evaluate_dataset(raw_data_dataset)

        harmonised_dataset = self._harmonise_dataset(raw_data_dataset, standard_to_use)

        return harmonised_dataset

    def _retrieve_raw_data_as_dataset(self, query: WPLQuerySettings) -> xr.Dataset:
        """...

        Args:
            query:

        Returns:

        """
        ...

    def _evaluate_dataset(self, dataset_to_evaluate: xr.Dataset):
        """...

        Args:
            dataset_to_evaluate:

        Returns:

        """
        ...

    def _harmonise_dataset(
        self, dataset_to_harmonise: xr.Dataset, standard_to_use: WPLHarmonisationStandard
    ) -> xr.Dataset:
        """...

        Args:
            dataset_to_harmonise:

        Returns:

        """
        ...
