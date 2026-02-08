""" Platform for siren integration """
from datetime import timedelta
import logging
import voluptuous as vol
from homeassistant.components.siren import (PLATFORM_SCHEMA, TURN_ON_SCHEMA, SirenEntityFeature, SirenEntity)
from .const import DOMAIN


SCAN_INTERVAL = timedelta(seconds=1)

def setup_platform(hass, config, add_entities, discovery_info=None):
    """ Platform uses config entry setup. """
    pass

async def async_setup_entry(hass, config_entry, async_add_entities):
    """ Setup Sammy. """
    sammy = hass.data[DOMAIN]

    devices = [SammySiren(sammy)]
    async_add_entities(devices)


class SammySiren(SirenEntity):
    _attr_supported_features = (
            SirenEntityFeature.TONES
            | SirenEntityFeature.TURN_ON
            | SirenEntityFeature.TURN_OFF
            | SirenEntityFeature.DURATION)

    def __init__(self, device):
        self._device = device
        self._attr_available_tones = device.tones
        self._available = True

    @property
    def unique_id(self):
        return self._device.hostname

    @property
    def icon(self):
        return 'mdi:siren'

    @property
    def is_on(self):
        return self._device.is_on

    def turn_on(self, **kwargs) -> None:
        """ Turn the siren on """
        duration = None if 'duration' not in kwargs else kwargs['duration']

        if 'tone' in kwargs:
            tone = kwargs['tone']
            self._device.set_tone(tone, duration)
        else:
            self._device.turn_on(duration)

    def turn_off(self, **kwargs) -> None:
        """ Turn the siren off """
        self._device.turn_off()

    def update(self):
        """ Update the state of the siren. """
        self._device.update()

