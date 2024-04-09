#!/usr/bin/env python

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

from pydantic import BaseModel

"""This module contains the factor related classes for the weather provider libraries."""


class EccodesFactorDescriptors(BaseModel):
    """The class represents the descriptors of a factor in the ECCODES library.

    Attributes:
        name (str):
            The long name of the factor.
        short_name (str):
            The short name of the factor.
        description (str):
            The description of the factor.
        old_harmonisation_name (str):
            The old harmonisation name of the factor.
    """

    name: str
    short_name: str
    description: str
    old_harmonisation_name: str


class EccodesUnitMappings(BaseModel):
    """The class represents the unit mappings of a factor in the ECCODES library.

    Attributes:
        original_unit (str):
            The original unit of the factor.
        si_unit (str):
            The SI unit of the factor.
        human_unit (str):
            The human unit of the factor.
        metric_unit (str):
            The metric unit of the factor.
        american_unit (str):
            The American unit of the factor.
        imperial_unit (str):
            The imperial unit of the factor.
    """

    original_unit: str
    si_unit: str
    human_unit: str
    metric_unit: str
    american_unit: str
    imperial_unit: str


class ModelFactor(BaseModel):
    """This class represents a factor in a WPLModel class.

    It is used to identify factors and translate them using their ECCODES equivalent factor if set.

    Attributes:
        id (str):
            The identifier of the factor. This directly corresponds to how the factor in the model is addressed in
            acquired data.
        eccodes_id (int):
            The optional ECCODES id of the factor. If you want to use ECCODES to translate the factor, this id is
            necessary. If not set, the factor will not be translated using ECCODES, but translated using the
            Model's [factor_translation()] method with the original identifier as the parameter.
        units (str):
            The unit specification applicable to the factor.
    """

    id: str
    eccodes_id: int | None
    units: str

    @property
    def metadata(self) -> dict[str, str]:
        """Returns the metadata of the factor."""
        metadata = {
            "id": self.id,
            "ECCODES id": self.eccodes_id,
            "Unit specification": self.units,
        }

        return metadata


class EccodesFactor(BaseModel):
    """The class represents a factor in the ECCODES library.

    It is mainly used to identify factors and translate them.

    Attributes:
        id (int):
            The identifier of the factor. This directly corresponds to how the factor in the model is addressed in
            acquired data.
        descriptors (dict[str, str]):
            The descriptors of the factor.
        units (dict[str, str]):
            The units of the factor.
    """

    id: int
    descriptors: EccodesFactorDescriptors
    units: EccodesUnitMappings

    @property
    def name(self) -> str:
        """Returns the long name of the factor."""
        return self.descriptors.name

    @property
    def short_name(self) -> str:
        """Returns the short name of the factor."""
        return self.descriptors.short_name

    @property
    def description(self) -> str:
        """Returns the description of the factor."""
        return self.descriptors.description

    @property
    def old_harmonisation_name(self) -> str:
        """Returns the old harmonisation name of the factor."""
        return self.descriptors.old_harmonisation_name

    @property
    def original_unit(self) -> str:
        """Returns the original unit of the factor."""
        return self.units.original_unit

    @property
    def si_unit(self) -> str:
        """Returns the SI unit of the factor."""
        return self.units.si_unit

    @property
    def human_unit(self) -> str:
        """Returns the human unit of the factor."""
        return self.units.human_unit

    @property
    def metric_unit(self) -> str:
        """Returns the metric unit of the factor."""
        return self.units.metric_unit

    @property
    def american_unit(self) -> str:
        """Returns the American unit of the factor."""
        return self.units.american_unit

    @property
    def imperial_unit(self) -> str:
        """Returns the imperial unit of the factor."""
        return self.units.imperial_unit

    @property
    def metadata(self) -> dict[str, str]:
        """Returns the metadata of the factor."""
        metadata = {
            "ID": self.id,
            "Long Name": self.name,
            "Short Name": self.short_name,
            "Description": self.description,
            "Oldstyle Harmonisation Name": self.old_harmonisation_name,
            "Default Unit Specification": self.original_unit,
            "SO Unit Specification": self.si_unit,
            "human Unit Specification": self.human_unit,
            "Metric Unit Specification": self.metric_unit,
            "American Unit Specification": self.american_unit,
            "Imperial Unit Specification": self.imperial_unit,
        }

        return metadata
