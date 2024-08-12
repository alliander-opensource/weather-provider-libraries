#!/usr/bin/env python

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------


from pydantic import BaseModel, ConfigDict, Field
from pyproj import CRS, Geod
from pyproj.aoi import BBox
from weather_provider_libraries.utility.coordinate_utils import (
    convert_box_from_crs_to_crs,
    convert_coordinate_to_crs,
    get_x_y_order_northing_easting_as_string,
    translate_coordinate_to_wgs84,
    validate_crs,
)


class WPGeoLocation(BaseModel):
    """A utility class aimed at supplying a default project interface for geographical locations.

    This utility class supplies the project with a default interface and standardized interactions for that interface.

    Attributes:
        x (float):
            The latitude of the location.
        y (float):
            The longitude of the location.
        coordinate_system (CRS):
            The coordinate system of the location.

    """

    x: float = Field(title="X-coordinate", description="The latitude- or x-coordinate for the location.")
    y: float = Field(title="Y-coordinate", description="The longitude- or y-coordinate of the location.")
    coordinate_system: CRS = Field(title="Coordinate System", description="The coordinate system of the location.")

    # Pydantic model config
    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)

    def __str__(self):
        """Return a string representation of the location."""
        return f"WPGeoLocation(({self.x}, {self.y}) - [{self.coordinate_system.name}])"

    def __repr__(self):
        """Return a string representation of the location."""
        return f"WPGeoLocation(({self.x}, {self.y}) - [{self.coordinate_system.name}]:[{self.x_y_order}])"

    def __eq__(self, other):
        """Check if two locations are equal."""
        if not isinstance(other, self.__class__):
            raise TypeError(f"Expected a WPGeoLocation object, got {type(other)}")

        distance = self.get_distance_to_location_in_m(other)
        return distance == 0

    @property
    def is_valid(self) -> bool:
        """Check if the location lies within the bounds of the coordinate system."""
        try:
            # The converter will raise a ValueError if the location lies outside the bounds of the coordinate system.
            self._coordinate_within_bounds(self.coordinate_system)
        except ValueError:
            return False

        return True

    @property
    def x_y_order(self) -> str:
        """Check the current WPGeolocation object's x and y order as northing and easting."""
        return get_x_y_order_northing_easting_as_string(self.coordinate_system)

    def as_crs(self, crs: CRS | int = 4326) -> "WPGeoLocation":
        """Convert the location to the specified coordinate system."""
        converted_x, converted_y = convert_coordinate_to_crs(self.x, self.y, self.coordinate_system, crs)
        return WPGeoLocation(x=converted_x, y=converted_y, coordinate_system=crs)

    def get_closest_location_from_list(self, locations: list["WPGeoLocation"]) -> "WPGeoLocation":
        """Get the closest location from a list of locations."""
        closest_location = None
        closest_distance_in_m = None

        for location in locations:
            distance_in_m = self.get_distance_to_location_in_m(location)

            if not closest_location or distance_in_m < closest_distance_in_m:
                closest_location = location
                closest_distance_in_m = distance_in_m

        return closest_location

    def get_distance_to_location_in_m(self, location: "WPGeoLocation") -> float:
        """Get the distance to another location in meters."""
        wgs84_x, wgs84_y = translate_coordinate_to_wgs84(self.x, self.y, self.coordinate_system)
        location_wgs84_x, location_wgs84_y = translate_coordinate_to_wgs84(
            location.x, location.y, location.coordinate_system
        )

        geodetic_reference_wsg84 = Geod(ellps="WGS84")
        _, _, distance_in_m = geodetic_reference_wsg84.inv(location_wgs84_x, location_wgs84_y, wgs84_x, wgs84_y)

        return distance_in_m

    def lies_within_bounding_box(self, bounding_box: BBox, box_crs: CRS) -> bool:
        """Check if the location lies within the given bounding box."""
        box_crs = validate_crs(box_crs)

        converted_bounding_box = convert_box_from_crs_to_crs(bounding_box, box_crs, CRS.from_epsg(4326))
        wgs84_x, wgs84_y = translate_coordinate_to_wgs84(self.x, self.y, self.coordinate_system)

        if converted_bounding_box.contains(BBox(wgs84_y, wgs84_x, wgs84_y, wgs84_x)):
            return True
        return False

    def lies_within_meters_radius(self, location: "WPGeoLocation", meters_of_radius: float) -> bool:
        """Check if the location lies within a certain radius (meters distance) of another location."""
        if self.get_distance_to_location_in_m(location) <= meters_of_radius:
            return True

        return False
