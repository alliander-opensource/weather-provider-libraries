#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

from pydantic import BaseModel, Field, ConfigDict


class EccodesFactor(BaseModel):
    """The identifying class for an ECCODES meteorological factor.

    This class is used as a conversion target for the harmonisation status, from which we can shift into the intended
     output as desired.

    Attributes:
        id (str):
                The ECCODES GRIB 2.0 ID code for the factor as it is known in the ECCODES Parameter Database.
                 The database can be found at: https://codes.ecmwf.int/grib/param-db/
                 Factor information can be found at: https://codes.ecmwf.int/grib/param-db/{id}
        name (str):
                A string holding the long name for the factor as it is known in the ECCODES Parameter Database.
        short_name (str):
                A string holding the short name for the factor as it is known in the ECCODES Parameter Database.
        description (str):
                A string holding a short and explanatory version of the description of the factor as it is known in
                 the ECCODES Parameter Database.
        unit (str):
                The unit of the factor as it is known in the ECCODES, as written in the Pint unit string format.
        harmonisation_name (str):
                The harmonisation name that this factor would have had under the old harmonisation system.
                 This is used to grant backwards compatibility with the previous version of the project.

    """

    id: int = Field(title="ECCODES GRIB 2.0 ID", description="The ECCODES Parameter DB ID known for this factor")
    name: str = Field(
        title="ECCODES GRIB 2.0 Long Name", description="The ECCODES Parameter DB longer name known for this factor"
    )
    short_name: str = Field(
        title="ECCODES GRIB 2.0 Short Name", description="The ECCODES Parameter DB shorter name known for this factor"
    )
    description: str = Field(
        title="ECCODES GRIB 2.0 Description",
        description="A short description based on that in the ECCODES Parameter DB ",
    )
    unit: str = Field(
        title="ECCODES GRIB 2.0 Pint Unit Specification",
        description="A Pint translated unit specification based on the ECCODES Parameter's unit field for this factor",
    )
    harmonisation_name: str = Field(
        title="Old Weather Provider API Harmonised Name",
        description="How this factor would be named under the old harmonisation naming convention. "
        "Used for backwards support.",
    )

    @property
    def metadata(self) -> dict[str, str]:
        """Return a metadata dictionary representation of this EccodesFactor object"""
        return {
            "ECCODES ID": str(self.id),
            "ECCODES Long Name": self.name,
            "ECCODES Short Name": self.short_name,
            "ECCODES Description": self.description,
            "ECCODES Pint Unit Declaration": self.unit,
            "ECCODES Old Style Harmonisation Name": self.harmonisation_name,
        }


class ModelFactor(BaseModel):
    """The identifying class for a single factor of Model source data, used for conversion and identification.

    Attributes:
         identifier (str):
                A string holding the identifier for the factor. This should be the name as it appears in the raw
                 weather data as it would be loaded into the project.
         linked_eccodes_factor (EccodesFactor):
                An EccodesFactor object representing a supported ECCODES GRIB 2.0 factor as declared in the
                 [/factor_data/meteo_factors.json] file of the project. For harmonisation purposes there always needs
                 to be such a factor.
         unit (str):
                An optional string holding a Pint unit specification for the factor. This should be used to declare
                 unit type whenever possible for automated unit conversion. If the original unit type is not supported
                 by Pint, leave this field empty. The system will then use custom unit conversion to the intended
                 factor by using the [factor_convert()] class method.

    """

    identifier: str = Field(
        title="Model Factor Identifier",
        description="The Model factor's identification string. Used for identifying the factor in model data.",
    )
    linked_eccodes_factor: int = Field(
        title="Model Factor Linked ECCODES ID code",
        description="The Model factor's associated ECCODES factor ID code. Used to harmonise and format data.",
    )
    unit: str | None = Field(
        default=None,
        title="Model Factor Pint Unit Specification",
        description="The Model factor's original unit specification, translated into a Pint unit string. "
        "Leave empty for customised model factor conversion. ",
    )

    # Pydantic class configuration
    model_config = ConfigDict(frozen=True)

    @property
    def metadata(self) -> dict[str, str]:
        """Return a metadata dictionary representation of this EccodesFactor object"""
        return {
            "Factor Identifier": self.identifier,
            "Linked ECCODES Factor": self.linked_eccodes_factor.metadata,
            "Factor Pint Unit Declaration": self.unit,
        }
