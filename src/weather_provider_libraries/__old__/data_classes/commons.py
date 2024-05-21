#!/usr/bin/ python

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

from typing import Self

import numpy as np
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from pyproj import CRS, Transformer

from weather_provider_libraries.data_classes.constants import DEFAULT_DATETIME_FORMAT, DEFAULT_TIMEDELTA_FORMAT
from weather_provider_libraries.utils.validation.date_time_related import validation_of_datetime64_elements

"""The purpose of this module is to house any dataclasses that don't specifically belong to one of the project's
main classes.
 
Currently, the dataclasses in here are the following:
    TimePeriod:
        A dataclass for storing simple time periods. Assures basic period and value validity for project purposes, 
        and allows for setting periods using [datetime], [np.datetime64] and [np.timedelta64]. 

"""


class TimePeriod(BaseModel):
    """A dataclass aimed at storing simple time periods.

    Notes:
        This class is used to properly handle the way time periods are handled within the project.
        It automatically handles supplied datetime and timedelta values and converts them to standardized np.datetime64
        values. It also assures that the period is valid for project purposes, and allows for customized validation
        based on boundary values.
    """

    start: np.datetime64 | np.timedelta64
    end: np.datetime64 | np.timedelta64

    first_moment_allowed_in_period: np.datetime64 | np.timedelta64 = Field(
        default=np.datetime64("1869-01-01T00:00").astype(DEFAULT_DATETIME_FORMAT)
    )
    last_moment_allowed_in_period: np.datetime64 | np.timedelta64 = Field(
        default=np.datetime64("now").astype(DEFAULT_DATETIME_FORMAT)
        + np.timedelta64((20 * 365) + 5, "D").astype(DEFAULT_TIMEDELTA_FORMAT)
    )

    # Pydantic class config
    model_config = ConfigDict(validate_assignment=True, arbitrary_types_allowed=True, extra="allow")

    # Pydantic validators
    _validate_start = field_validator("start", mode="before")(validation_of_datetime64_elements)
    _validate_end = field_validator("end", mode="before")(validation_of_datetime64_elements)
    _validate_first_moment_allowed_in_period = field_validator("first_moment_allowed_in_period", mode="before")(
        validation_of_datetime64_elements
    )
    _validate_last_moment_allowed_in_period = field_validator("last_moment_allowed_in_period", mode="before")(
        validation_of_datetime64_elements
    )

    @model_validator(mode="after")
    def __validate_period(self):
        """Check if the currently resolved values make up a valid period.

        Because a period based on timedelta64 values could shift from valid TimePeriod into an invalid one, this
         property allows users to verify before use that the TimePeriod is indeed still valid.

        """
        if not (self.resolved_first_moment_allowed <= self.resolved_start < self.resolved_last_moment_allowed):
            raise ValueError(
                f"TimePeriod [{self.start} - {self.end}]: The current value of [start] ({self.resolved_start}) "
                f"should always lie between the current first moment allowed ({self.resolved_first_moment_allowed}) "
                f"and the current last moment allowed ({self.resolved_last_moment_allowed})."
            )

        if not (self.resolved_first_moment_allowed < self.resolved_end <= self.resolved_last_moment_allowed):
            raise ValueError(
                f"TimePeriod [{self.start} - {self.end}]: The current value of [end] ({self.resolved_end}) "
                f"should always lie between the current first moment allowed ({self.resolved_first_moment_allowed}) "
                f"and the current last moment allowed ({self.resolved_last_moment_allowed})."
            )

        if self.resolved_start >= self.resolved_end:
            raise ValueError(
                f"A TimePeriod cannot have the resolved value for [start] ({self.resolved_start}) lie after the "
                f"resolved value for [end] ({self.resolved_end}). "
                f"Please change period values in a way that [start] lies before [end]!"
            )
        return self

    @property
    def resolved_start(self) -> np.datetime64:
        """Resolve and retrieve the start value as a np.datetime64 value."""
        return (
            self.start
            if isinstance(self.start, np.datetime64)
            else (np.datetime64("now").astype(DEFAULT_DATETIME_FORMAT) + self.start)
        )

    @property
    def resolved_end(self) -> np.datetime64:
        """Resolve and retrieve the end value as a np.datetime64 value."""
        return (
            self.end
            if isinstance(self.end, np.datetime64)
            else (np.datetime64("now").astype(DEFAULT_DATETIME_FORMAT) + self.end)
        )

    @property
    def resolved_first_moment_allowed(self) -> np.datetime64:
        """Resolve and retrieve the first_moment_allowed value as a np.datetime64 value."""
        return (
            self.first_moment_allowed_in_period
            if isinstance(self.first_moment_allowed_in_period, np.datetime64)
            else (np.datetime64("now").astype(DEFAULT_DATETIME_FORMAT) + self.first_moment_allowed_in_period)
        )

    @property
    def resolved_last_moment_allowed(self) -> np.datetime64:
        """Resolve and retrieve the last_moment_allowed value as a np.datetime64 value."""
        return (
            self.last_moment_allowed_in_period
            if isinstance(self.last_moment_allowed_in_period, np.datetime64)
            else (np.datetime64("now").astype(DEFAULT_DATETIME_FORMAT) + self.last_moment_allowed_in_period)
        )


class GeoLocation(BaseModel):
    """A dataclass aimed at storing simple geolocations.

    Notes:
        The GeoLocation class is aimed at storing simple geolocations. It assures basic validity for project purposes,
        and allows for setting locations using latitude and longitude values. The class also allows for easy conversion
        into other CRS systems.

    Warnings:
        While the class refers to the coordinates as latitude and longitude, this is done only for the sake of clarity
        on which coordinate component should go where. (As X,Y or Y,X can be confusing, depending on the CRS)
    """

    latitude: float
    longitude: float
    coordinate_system: int = 4326

    model_config = ConfigDict(validate_assignment=True)

    # Pydantic validators
    @field_validator("coordinate_system", mode="before")
    def __validate_coordinate_system(cls, value):
        """Check if the coordinate system is a valid one."""
        try:
            CRS.from_epsg(int(value))
        except ValueError as val_error:
            raise ValueError(
                f"The coordinate system [{value}] is not a valid one. "
                f"Please use an EPSG code to represent the coordinate system."
            ) from val_error

        return value

    @property
    def is_valid(self) -> bool:
        """Check if the current GeoLocation is valid."""
        # Only if the coordinate is within bounds for the current coordinate system, the coordinate is valid.
        bounds = CRS.from_epsg(self.coordinate_system).area_of_use.bounds
        return bounds[0] <= self.longitude <= bounds[2] and bounds[1] <= self.latitude <= bounds[3]

    def get_coordinate_translated_for_crs(self, crs: int) -> Self:
        """Get the coordinates in the current instance for a specific coordinate system.

        Args:
            crs (int):
                The EPSG code of the coordinate system to translate the current coordinates to.

        Returns:
            GeoLocation:
                A new GeoLocation instance with the translated coordinates.

        Raises:
            ValueError:
                If the current GeoLocation is not valid for the current coordinate system, or if the translated.
        """
        if not self.is_valid:
            raise ValueError(
                f"The current GeoLocation [{self.latitude}, {self.longitude}] is not valid for the current "
                f"coordinate system [{self.coordinate_system}]. Translation is therefore not possible."
            )

        source_crs = CRS.from_epsg(self.coordinate_system)
        target_crs = CRS.from_epsg(crs)

        coordinate_transformer = Transformer.from_crs(source_crs, target_crs)
        translated_location = coordinate_transformer.transform(self.longitude, self.latitude)

        translated_geo_location = GeoLocation(
            latitude=translated_location[1], longitude=translated_location[0], coordinate_system=crs
        )

        if not translated_geo_location.is_valid:
            raise ValueError(
                f"The current GeoLocation [{self.latitude}, {self.longitude}] is not valid for the target "
                f"coordinate system [{crs}]. Translation is therefore not possible."
            )

        return translated_geo_location
