#!/usr/bin/env python

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

from pydantic import BaseModel, Field


class WPFactorDescriptors(BaseModel):
    short_name: str = Field(title="Short name", description="A short name for the factor.")
    long_name: str = Field(title="Long name", description="A long name for the factor.")
    descriptions: str = Field(title="Description", description="A description of the factor.")


class WPUnitGrid(BaseModel):
    base_unit: str = Field(title="Base harmonized unit", description="The base harmonized unit for the factor.")
    scientific_unit: str = Field(title="Scientific unit", description="The scientific unit for the factor.")
    human_readable_unit: str = Field(title="Human readable unit", description="The human readable unit for the factor.")
    metric_unit: str = Field(title="Metric unit", description="The Metric unit for the factor.")
    imperial_unit: str = Field(title="Imperial unit", description="The Imperial unit for the factor.")
    american_unit: str = Field(title="American unit", description="The American unit for the factor.")

    # TODO:
    #  - Add a validator to ensure that the base unit is a valid unit, and that the other units are valid conversions.


class WPModelWeatherFactor(BaseModel):
    """A dataclass to represent a model's weather factor.

    A weather factor is a physical quantity that can be measured and that influences the weather. This class
    represents the factor as it is stored in the model's original datasource(s).

    Notes:
        - If possible, any factor should be mapped to an ECCODES factor.
        - If a factor cannot be mapped to an ECCODES factor, the ECCODES identifier should be set to None.
        - Any unmapped factor should be handled via the model's "_manual_factor_harmonization(identifier: str)" method.

    """

    identifier: str = Field()
    eccodes_identifier: int | None = Field()
    descriptors: WPFactorDescriptors = Field()
    unit_of_retrieved_factor: str = Field()


class WPECCODESFactor(BaseModel):
    """A dataclass to represent a weather factor as it is stored in the ECCODES library.

    A Weather factor is a physical quantity that can be measured and that influences the weather. This class
    represents the factor as it is stored in the ECCODES library.

    Notes:
        - The descriptors and unit grid should be taken from the official ECCODES library.
        - As yet, we can't reliably load the full ECCODES library into memory, so we're doing this manually for now...
        - The old_style_harmonization_name references the naming convention used for the old v2 harmonization style.
          As such, the name should for any supported factor should be identical to its base harmonization name with v2
          if it exists.
        - The units within unit_grid should all be valid units that can be directly converted to and from the base unit
          using PintXarray.

    """

    identifier: int = Field()
    descriptors: WPFactorDescriptors = Field()
    unit_grid: WPUnitGrid = Field()
    old_style_harmonization_name: str = Field()
