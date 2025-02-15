#!/usr/bin/env python

#  SPDX-FileCopyrightText: 2019-2025 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0

from pydantic import BaseModel, ConfigDict


class ModelFactor(BaseModel):
    """A dataclass aimed at providing an interface for external meteorological factors before harmonisation.

    The goal of this class is to provide a common interface for external meteorological factors before harmonisation
    that will allow for a standardized interface between the WPAS libraries and the external data providers. This will
    allow for the WPAS libraries to be able to handle data from multiple sources in a consistent manner.

    Its counterpart, the EccodesFactor dataclass (linked via the eccodes_id), stores information on how to format any
    Modelfactor that is a direct or indirect equivalent of an ECCODES factor as such.
    """

    # Model Configuration
    model_config = ConfigDict()

    # Request parameters
    factor_id: str  # The original identifier of the factor as supplied by the data provider
    factor_name: str  # The descriptive name of the factor for support purposes
    eccodes_id: int | None  # The matching eccodes identifier for the factor if available
    pint_unit_string: str  # The original unit of the factor as supplied by the data provider


class EccodesFactor(BaseModel):
    """A dataclass aimed at providing an interface for ECCODES compatible meteorological factors.

    Where the ModelFactor dataclass is aimed at providing an interface for external meteorological factors before
    harmonisation, the EccodesFactor dataclass is aimed at providing an interface for ECCODES compatible meteorological
    factors that allows Modelfactors to convert to harmonised ECCODES factors and to format those into any compatible
    unit system. This will allow for a standardized interface between the WPAS libraries and the ECCODES library. This
    will allow for the WPAS libraries to be able to handle data from multiple sources in a consistent manner.
    """

    # Model Configuration
    model_config = ConfigDict()

    # Request parameters
    id: int  # The eccodes numeric identifier for the factor
    short_name: str  # The eccodes short name of the factor
    long_name: str  # The eccodes name of the factor
    description: str  # The eccodes description of the factor

    # Pint unit strings
    pint_unit_string: str  # The eccodes default unit of the factor
    pint_unit_string_si: str  # The unit for this factor as it would be in the SI system
    pint_unit_string_imperial: str  # The unit for this factor as it would be in the imperial system
    pint_unit_string_metric: str  # The unit for this factor as it would be in the metric system
