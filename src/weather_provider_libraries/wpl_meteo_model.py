#!/usr/bin/env python

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

import json
from pathlib import Path

import numpy as np
import toml
import xarray as xr
from pyproj import CRS
from pyproj.aoi import BBox

from weather_provider_libraries.data_classes.factor_related import ModelFactor
from weather_provider_libraries.data_classes.model_related import ModelGeography, ModelIdentity, ModelProperties
from weather_provider_libraries.data_classes.other import TimePeriod, UnitSystem
from weather_provider_libraries.data_classes.storage_related import StorageMode


class WPLMeteoModel:
    """Class for the WPLMeteoModel.

    This class is used to represent a weather model in the Weather Provider Libraries.
    """
    
    def __init__(self, init_folder: Path):
        """Constructor for the WPLMeteoModel class."""
        with open(init_folder / "factors.json") as model_factors_json_data:
            model_factors = json.load(model_factors_json_data)

        config_toml = toml.load(init_folder / "config.toml")
        
        self.identity = ModelIdentity(
            id=config_toml["identity"]["id"],
            name=config_toml["identity"]["name"],
            description=config_toml["identity"]["description"],
            information_url=config_toml["identity"]["information_url"],
            license_information=config_toml["identity"]["license_information"]
        )
        
        self.properties = ModelProperties(
            predictive_model=config_toml["properties"]["predictive_model"],
            directly_accessible=config_toml["properties"]["directly_accessible"],
            storage_mode_to_use=getattr(StorageMode, config_toml["properties"]["storage_mode_to_use"]),
            singular_datapoint=config_toml["properties"]["singular_datapoint"]
        )

        bbox_contents = config_toml["geography"].get("area_bounding_box", None)
        if bbox_contents is not None and isinstance(bbox_contents, list) and len(bbox_contents) == 4:
            area_bounding_box = BBox(
                west=bbox_contents[0],
                south=bbox_contents[1],
                east=bbox_contents[2],
                north=bbox_contents[3]
            )
        else:
            area_bounding_box = None
        
        self.geography = ModelGeography(
            area_bounding_box=area_bounding_box,
            time_range=TimePeriod(
                start=np.datetime64(config_toml["geography"]["time_range_start"]),
                end=np.datetime64(config_toml["geography"]["time_range_end"])
            ),
            source_crs=CRS(config_toml["geography"].get("source_crs", None))
        )
        
        self.factor_information = {
            factor_id: ModelFactor(
                identifier=factor_id,
                linked_eccodes_factor=factor_info["linkedECCODESFactor"],
                unit=factor_info["unit"]
            ) for factor_id, factor_info in model_factors.items()
        }

    @property
    def id(self) -> str:
        """Getter for the id property."""
        return self.identity.id

    @property
    def name(self) -> str:
        """Getter for the name property."""
        return self.identity.name

    @property
    def metadata(self) -> dict[str, str | dict]:
        """Getter for the metadata property."""
        new_metadata: dict[str, str | dict] = self.identity.metadata
        new_metadata["Properties"] = self.properties.metadata
        new_metadata["Geography"] = self.geography.metadata
        return new_metadata

    @property
    def known_factors(self) -> dict[str, str]:
        """Getter for the known_factors property."""
        known_factors = {}
        for factor in self.factor_information:
            known_factors.update(factor.metadata)
        return known_factors

    def validate(self):
        """Validate the model."""
        for factor in self.factor_information:
            if not isinstance(factor, ModelFactor):
                raise TypeError(f"Factor {factor} is not a ModelFactor object.")
        return True

    def convert(self, data_to_convert: xr.Dataset, target_unit_system: UnitSystem) -> xr.Dataset:
        """Convert the data to the target unit system."""
        raise NotImplementedError

    def harmonize(self, data_to_harmonize: xr.Dataset) -> xr.Dataset:
        """Harmonize the data."""
        raise NotImplementedError
