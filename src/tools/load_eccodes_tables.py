#!/usr/bin/env python

#  SPDX-FileCopyrightText: 2019-2025 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0

import json

from eccodes import codes_get, codes_grib_new_from_samples, codes_release, codes_set
from pint import UnitRegistry


def extract_grib1_factors(output_json_path):
    """Extract GRIB1 factors from ECCODES parameter tables and save them as a JSON file.

    :param output_json_path: Path to save the resulting JSON file.
    """
    weather_factors = {}
    ureg = UnitRegistry()

    # Use a GRIB1 sample to access parameter information
    grib_handle = codes_grib_new_from_samples("regular_ll_sfc_grib1")
    if not grib_handle:
        raise RuntimeError("Failed to create a GRIB handle from GRIB1 sample.")

    try:
        # Extract metadata for all GRIB1 parameters
        for param_id in range(1, 256):  # GRIB1 uses parameter IDs 1–255
            try:
                # Set the parameter ID
                codes_set(grib_handle, "paramId", param_id)

                # Extract metadata
                short_name = codes_get(grib_handle, "shortName")
                long_name = codes_get(grib_handle, "name")
                unit = codes_get(grib_handle, "units")

                # Attempt to create unit variants
                try:
                    unit_quantity = ureg(unit)
                    units_metric = str(unit_quantity.to_base_units())
                    units_si = str(unit_quantity.to_base_units())

                    # Attempt to derive an appropriate imperial unit
                    if unit_quantity.dimensionality == ureg("meter").dimensionality:
                        units_imperial = str(unit_quantity.to(ureg.feet))
                    elif unit_quantity.dimensionality == ureg("kilogram").dimensionality:
                        units_imperial = str(unit_quantity.to(ureg.pound))
                    elif unit_quantity.dimensionality == ureg("kelvin").dimensionality:
                        units_imperial = str(unit_quantity.to(ureg.degF))
                    else:
                        units_imperial = None
                except Exception:
                    # Handle unit conversion errors
                    units_imperial = None
                    units_metric = None
                    units_si = None

                # Store the metadata
                weather_factors[param_id] = {
                    "short_name": short_name,
                    "long_name": long_name,
                    "unit": unit,
                    "units_imperial": units_imperial,
                    "units_metric": units_metric,
                    "units_si": units_si,
                }
            except Exception:
                # Skip invalid or unavailable parameter IDs
                continue

    finally:
        # Always release the GRIB handle
        codes_release(grib_handle)

    # Write the extracted data to a JSON file
    with open(output_json_path, "w") as json_file:
        json.dump(weather_factors, json_file, indent=4)

    print(f"GRIB1 factors have been saved to {output_json_path}")


# Example usage
if __name__ == "__main__":
    output_json = "./grib1_factors.json"
    extract_grib1_factors(output_json)
