#!/usr/bin/env python

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

from pydantic import BaseModel, ConfigDict, Field
from pyproj import CRS, Transformer
from pyproj.aoi import BBox

from weather_provider_libraries.utils.coordinate_utils import get_xy_order_from_crs, validate_crs, convert_coordinates, \
    convert_coordinates_from_crs_to_other_crs


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
        return get_xy_order_from_crs(self.coordinate_system)

    def as_crs(self, crs: CRS | int = 4326) -> "WPGeoLocation":
        """Convert the location to the specified coordinate system.

        Args:
            crs (CRS):
                The coordinate system to convert the location to. The default is WGS84.

        Returns:
            WPGeoLocation:
                The location converted to the specified coordinate system.

        """
        crs = validate_crs(crs)

        if self.coordinate_system == crs:
            return self

        converted_x, converted_y = convert_coordinates_from_crs_to_other_crs(
            self.x, self.y, self.coordinate_system, crs
        )

        return WPGeoLocation(x=converted_x, y=converted_y, coordinate_system=crs)

    def get_closest_location(self, locations: list["WPGeoLocation"]) -> "WPGeoLocation":
        """Get the closest location from a list of locations.

        Args:
            locations (list[WPGeoLocation]):
                A list of locations to compare against.

        Returns:
            WPGeoLocation:
                The closest location from the list.

        """
        # 0. Validate the input.

        # 1. Equalize the coordinate systems.

        # 2. Evaluate the distance between the locations.

        # 3. Return the closest location.

    def lies_within_bounding_box(self, bounding_box: BBox) -> bool:
        """Check if the location lies within a bounding box.

        Args:
            bounding_box (BBox):
                The bounding box to check against.

        Returns:
            bool:
                Whether the location lies within the bounding box.

        """
        # 0. Validate the input.

        # 1. Check if the location lies within the bounding box.

    def lies_within_radius(self, location: "WPGeoLocation", radius: float, use_miles_as_unit: bool = False) -> bool:
        """Check if the location lies within a certain radius of another location.

        Args:
            location (WPGeoLocation):
                The location to check against.
            radius (float):
                The radius to check for. By default, the unit of measurement is kilometers.
            use_miles_as_unit (bool):
                Whether to use miles as the unit of measurement for radius.

        Returns:
            bool:
                Whether the location lies within the radius of the other location.

        """
        # 0. Validate the input.

        # 1. Evaluate the distance between the locations.

        # 2. Check if the distance is within the radius.

    def _convert_to_wgs84(self) -> "WPGeoLocation":
        """Convert the location to WGS84."""
        wgs84_transformer = Transformer.from_crs(self.coordinate_system, CRS.from_epsg(4326))
        wgs84_x, wgs84_y = wgs84_transformer.transform(self.x, self.y)
        return WPGeoLocation(x=wgs84_x, y=wgs84_y, coordinate_system=CRS.from_epsg(4326))

    def _coordinate_within_bounds(self, target_crs: CRS | int = 4326) -> bool:
        """Check if a coordinate lies within the bounds of the coordinate system."""
        if isinstance(target_crs, int):
            target_crs = CRS.from_epsg(target_crs)

        # WGS84 uses X for latitude (N,S) and Y for longitude (W,E)
        wgs84_coord = self._convert_to_wgs84()
        west_bound, south_bound, east_bound, north_bound = target_crs.area_of_use.bounds

        if west_bound <= wgs84_coord.y <= east_bound and south_bound <= wgs84_coord.x <= north_bound:
            return True

        return False
