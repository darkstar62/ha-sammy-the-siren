""" Integration main """

from homeassistant.const import Platform
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import (CONF_HOSTNAME, CONF_PORT, DOMAIN)
from .coordinator import SirenDataUpdateCoordinator
import logging

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SIREN]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    hostname = entry.data.get(CONF_HOSTNAME)
    port = entry.data.get(CONF_PORT)
    coordinator = SirenDataUpdateCoordinator(hostname, port, hass, entry)

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    entry.async_on_unload(entry.add_update_listener(options_update_listener))

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def options_update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """ Handle options update. """
    await hass.config_entries.async_reload(entry.entity_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """ Unload a config entry. """
    coordinator = hass.data[DOMAIN][entry.entry_id]
    await coordinator.siren.disconnect()

    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok

