#!/usr/bin/env python

#  SPDX-FileCopyrightText: 2019-2025 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0

"""A module aimed at configuring the Loguru logger for the WPAS libraries."""
import sys

from loguru import logger

from weather_provider_libraries._settings import PROJECT_SETTINGS

_BASIC_LOGGING_FORMAT = (
    f"<b><yellow>[{PROJECT_SETTINGS.log_prefix}_LIB]</yellow> "
    "<i>{time:YY-MM-DD HH:mm:ss}</i></b> <level>[{level}]</level>"
    " <cyan>{name}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
)

_EXTENSIVE_LOGGING_FORMAT = (
    f"<i><WHITE>[<b>{PROJECT_SETTINGS.log_prefix} Libraries "
    "{time:YYYY-MM-DD HH:mm:ss Z}</b>]</WHITE></i> <level>[{level}]</level>"
    " >> <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
)


def configure_logger():
    """Configure the Loguru logger for this Project (component)."""
    # Clean up existing logger(s)
    _cleanup_loggers()

    # Add a console logging handler
    _add_console_logger()

    # Add a file logging handler if configured
    _add_file_logger()

    logger.info("Loguru logging handlers configured for project "
                f"[{PROJECT_SETTINGS.project_name}, version {PROJECT_SETTINGS.version}].")


def _cleanup_loggers():
    """Remove all existing loggers."""
    logger.remove()
    logger.info("All existing loggers removed.")


def _add_console_logger():
    """Add a console logging handler."""
    logger.add(
        sink=sys.stdout,
        level=PROJECT_SETTINGS.log_level,
        format=_get_logging_format(),
        enqueue=True,  # Enqueue messages for better performance.
    )
    logger.info("Console logging handler added.")


def _get_logging_format():
    """Return the logging format based on the project settings."""
    return _EXTENSIVE_LOGGING_FORMAT if PROJECT_SETTINGS.log_mode == "extensive" else _BASIC_LOGGING_FORMAT


def _add_file_logger():
    """Add a file logging handler if configured."""
    if PROJECT_SETTINGS.log_file_path:
        logfile = PROJECT_SETTINGS.log_file_path / "wpas_libraries.log"
        logfile.parent.mkdir(parents=True, exist_ok=True)
        logger.add(
            sink=logfile,
            level=PROJECT_SETTINGS.log_level,
            format=_get_logging_format(),
            retention=PROJECT_SETTINGS.log_file_retention,
            rotation=PROJECT_SETTINGS.log_file_rotation,
            enqueue=True,  # Enqueue messages for better performance.
            backtrace=True,  # Include backtrace in case of errors.
            diagnose=True,  # Include diagnostic information in case of errors.
        )
