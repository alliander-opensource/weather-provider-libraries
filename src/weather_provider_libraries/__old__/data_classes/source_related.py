#!/usr/bin/env python

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

from ipaddress import IPv4Address, IPv6Address

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator

from weather_provider_libraries import WeatherProviderModel


class WPSourceIdentity(BaseModel):
    """A class to represent the identity of a weather provider source.

    This immutable class contains the identity of a weather provider source.

    Attributes:
        id (str):
            A short string identifier of the Source. Lower case letters only.
        name (str):
            A short name of the Source. Letters and spaces only.
        description (str):
            A short description of the Source. Should contain a brief description of the Source.
        information_url (HttpUrl | IPv4Address | IPv6Address):
            A link to an URL or IP address holding extensive information on the model or it's source data.
        models (dict[str, WeatherProviderModel]):
            A dictionary containing the models of the source. The keys are the model ids and the values are the models.

    Raises:
        (Pydantic) ValueError:
            If the supplied data isn't valid, or attempts are made to change data using invalid data, the Pydantic
            standard range of errors will be raised.

    """

    id: str = Field(
        min_length=3,
        max_length=12,
        title="Source Identifier",
        description="Short string identifier of the Source. Lower case letters only",
        pattern="^[a-z]+$",
        frozen=True,
    )
    name: str = Field(
        min_length=4,
        max_length=32,
        title="Source Name",
        description="Short name of the Source. Letters and spaces only",
        pattern="^[a-zA-Z ]+$",
        frozen=True,
    )
    description: str = Field(
        min_length=12,
        max_length=512,
        title="Source Description",
        description="Short description of the Source. Should contain a brief description of the Source",
        frozen=True,
    )
    information_url: HttpUrl | IPv4Address | IPv6Address = Field(
        title="Source Information URL",
        description="A link to an URL or IP address holding extensive information on the model or it's source data.",
        frozen=True,
    )
    models: dict[str, WeatherProviderModel] = Field(
        title="Source Models",
        description="A dictionary containing the models of the source. "
        "The keys are the model ids and the values are the models.",
        default={},
        frozen=False,
    )

    # Pydantic class configuration
    model_config = ConfigDict(arbitrary_types_allowed=True)

    # Pydantic validation
    @field_validator("models", mode="before")
    def __validate_models(cls, value):
        """Validate the models field of the SourceIdentity class."""
        if not isinstance(value, dict):
            raise ValueError("The models field must be a dictionary.")

        for key, model in value.items():
            if not isinstance(key, str):
                raise ValueError("The keys in the models dictionary must all be strings.")
            if not isinstance(model, WeatherProviderModel):
                raise ValueError("The values in the models dictionary must all be WeatherProviderModel instances.")
            if key != model.id:
                raise ValueError(
                    "The keys in the models dictionary must match the id of the WeatherProviderModel instance."
                )

        return value
