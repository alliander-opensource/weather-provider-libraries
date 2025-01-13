#!/usr/bin/env python

#  SPDX-FileCopyrightText: 2019-2025 Alliander N.V.
#  SPDX-License-Identifier: MPL-2.0

"""Base class for managing meteo updates"""
import threading
import time

from loguru import logger

from weather_provider_libraries.base_classes.meteo_controller import MeteoController
from weather_provider_libraries.base_classes.meteo_storage import MeteoStorage
from weather_provider_libraries.utils.logger_utils import configure_logger


class MeteoUpdateManager:
    """Base class for managing meteo updates"""

    def __init__(self):
        """Constructor"""
        self.storages: set[MeteoStorage] = self._load_storage_for_configured_models()
        self.threads: list[threading.Thread] = []
        self.stop_event = threading.Event()

    def start_updates(self):
        """Start the updates"""
        for storage in self.storages:
            # Check if the object has an 'update_frequency' and 'update' method
            if hasattr(storage, 'update_frequency') and hasattr(storage, 'mode') and storage.mode in ['auto', 'manual']:
                thread = threading.Thread(
                    target=self._run_updates,
                    args=(storage,),
                    daemon=True
                )
                self.threads.append(thread)
                thread.start()
                logger.info(f"Started update thread for {storage}")
            else:
                logger.warning(f"Object {storage} is missing 'update_frequency' or 'update' method.")

    def _load_storage_for_configured_models(self) -> set[MeteoStorage]:
        """Load the storage for the configured models"""
        controller = MeteoController()

        return controller.get_storage_objects()

    def _run_updates(self, storage: MeteoStorage):
        while not self.stop_event.is_set():
            try:
                # Call the update method
                storage.auto_update()
                # Wait for the next update cycle
                logger.info(f"Waiting for {storage.update_frequency} seconds before updating {storage}")
                time.sleep(storage.update_frequency)
            except Exception as e:
                logger.error(f"Error updating {storage}: {e}")
                break


if __name__ == '__main__':
    configure_logger()
    logger.info("Starting MeteoUpdateManager")
    manager = MeteoUpdateManager()
    try:
        manager.start_updates()
    finally:
        manager.stop_event.set()
        logger.info("MeteoUpdateManager stopped")

