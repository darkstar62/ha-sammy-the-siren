""" Define a siren coordinator. """

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .libsiren import Siren

import logging

_LOGGER = logging.getLogger(__name__)


class SirenDataUpdateCoordinator(
        DataUpdateCoordinator[bool]
):
    """ Class to manage fetching data from a single siren. """

    config_entry: ConfigEntry

    def __init__(
            self,
            hostname: str,
            port: int,
            hass: HomeAssistant,
            config_entry: ConfigEntry
    ) -> None:
        """ Initialize """
        super().__init__(
                hass,
                _LOGGER,
                config_entry=config_entry,
                name=config_entry.title,
        )

        self.siren = Siren(hostname, port)
        self.siren.initialize()
