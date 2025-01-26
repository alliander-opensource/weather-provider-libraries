#!/usr/bin/env python


#  SPDX-FileCopyrightText: 2019-2025 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0

from weather_provider_libraries.core.factors import EccodesFactor


def load_eccodes_factors() -> dict[int, EccodesFactor]:
    """Load the eccodes factors from the eccodes library.

    This method loads the eccodes factors from the eccodes library and returns them as a dictionary with the eccodes
    numeric identifier as the key.

    Returns
    -------
    dict[int, EccodesFactor]: The eccodes factors as a dictionary with the eccodes numeric identifier as the key.

    """
    # Load the eccodes factors from the eccodes library


ECCODES_FACTORS = ...
