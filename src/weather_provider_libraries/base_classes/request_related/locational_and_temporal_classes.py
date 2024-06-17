#!/usr/bin/env python

#  -------------------------------------------------------
#  SPDX-FileCopyrightText: 2019-2024 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0
#  -------------------------------------------------------

from pydantic import BaseModel


class WPTimePeriod(BaseModel):
    # TODO: Implement
    #       -----
    #       Input consists of "start" and "end" objects of types np.datetime64, np.timedelta64,
    #       datetime.datetime, or datetime.timedelta.
    #       The "start" and "end" objects can be of different types.
    #       Upon initialization, the "start" and "end" objects are converted to np.datetime64 and np.timedelta64
    #       objects and stored as __start and __end.
    #       -----
    #       Properties:
    #           - start (np.datetime64): The start of the period. Resolved from __start.
    #           - end (np.datetime64): The end of the period. Resolved from __end.
    #           - original_values (tuple): The original values of the start and end objects.
    #           - is_a_valid_period (bool): Whether the period is valid.
    #       Methods:
    #           - __add__(other: PERIOD) -> PERIOD: Adds two periods.
    #           - __sub__(other: PERIOD) -> PERIOD: Subtracts two periods.
    #           - __contains__(other: PERIOD) -> bool: Checks if a period is contained in another period.
    #       -----
    #       Model Properties:
    #           - arbitrary types allowed (numpy datetimes etc.)
    #           - frozen values (no alterations allowed or needed. Use methods for alterations.)
    #           - no default values
    #           - All np.datetime64 and np.timedelta64 objects refer to UTC.
    #           - All timedelta objects will be considered relative to now.
    #           - All np.datetime64 and np.timedelta64 objects will be standardized to a resolution of minutes.
    #             (There is no need for a higher resolution.)

    ...
