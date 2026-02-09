""" Integration main """

from homeassistant.const import Platform
from .const import (CONF_HOSTNAME, CONF_PORT, DOMAIN)
import logging

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [
        Platform.SIREN,
]

def setup(hass, config):
    return True


class SirenDevice:
    def __init__(self, hostname, port):
        self._hostname = hostname
        self._port = port
        self._url = f'ws://{hostname}:{port}'

    @property
    def is_on(self):
        return self._is_on

    @property
    def hostname(self):
        return self._hostname

    @property
    def url(self):
        return self._url


async def async_setup_entry(hass, config_entry):
    hostname = config_entry.data.get(CONF_HOSTNAME)
    port = config_entry.data.get(CONF_PORT)

    device = SirenDevice(hostname, port)
    hass.data[DOMAIN] = device

    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)
    return True

