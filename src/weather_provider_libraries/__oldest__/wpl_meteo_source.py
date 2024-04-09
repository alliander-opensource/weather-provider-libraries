#!/usr/bin/env python

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

from weather_provider_libraries.__oldest__.data_classes import SourceIdentity
from weather_provider_libraries.__oldest__.wpl_meteo_model import WPLMeteoModel


class WPLMeteoSource:
    """The base class for a weather source."""

    def __init__(self, identity: SourceIdentity):
        """The constructor for the WPLMeteoSource class."""
        self.identity = identity
        self.models: dict[str, WPLMeteoModel] = {}

    def load_model(self, model: WPLMeteoModel):
        """Load a model into the source.

        Args:
            model (WPLMeteoModel):
                    The model to load into the source.

        """
        if not isinstance(model, WPLMeteoModel):
            raise TypeError(f"Model {model} is not an instance of WPLMeteoModel")

        self.models[model.id] = model

    @property
    def metadata(self) -> dict[str, str | dict]:
        """Return the metadata for the source.

        Returns:
            dict[str, str | dict]:
                    The metadata for the source.

        """
        return {
            "id": self.identity.id,
            "name": self.identity.name,
            "description": self.identity.description,
            "models": {model_id: model.metadata for model_id, model in self.models.items()},
        }
