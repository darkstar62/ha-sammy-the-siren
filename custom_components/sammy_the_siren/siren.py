""" Platform for siren integration """
from datetime import timedelta
import logging
import voluptuous as vol
import asyncio
import websockets
import json
from homeassistant.components.siren import (PLATFORM_SCHEMA, TURN_ON_SCHEMA, SirenEntityFeature, SirenEntity)
from .const import DOMAIN


_LOGGER = logging.getLogger(__name__)

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
        self._available = False
        self._is_on = False
        self._tones = []

        asyncio.ensure_future(self._connect())

    @property
    def unique_id(self):
        return self._device.hostname

    @property
    def icon(self):
        return 'mdi:siren'

    @property
    def is_on(self):
        return self._is_on

    @property
    def should_poll(self):
        return False

    @property
    def available_tones(self):
        return self._tones

    @property
    def available(self):
        return self._available

    ## SirenEntity Implementation

    async def async_turn_on(self, **kwargs) -> None:
        """ Turn the siren on """
        duration = None if 'duration' not in kwargs else kwargs['duration']

        if 'tone' in kwargs:
            tone = kwargs['tone']
            await self._set_tone(tone, duration)
        else:
            await self._turn_on(duration)

    async def async_turn_off(self, **kwargs) -> None:
        """ Turn the siren off """
        await self._turn_off()

    ## Private functions

    async def _connect(self):
        while True:
            # Keep trying to connect until we get it.
            try:
                self._websocket = await websockets.connect(self._device.url)
            except Exception as e:
                await asyncio.sleep(5)
                continue

            await self._websocket.send(json.dumps({'request': 'get_tones'}))
            self._available = True
            self.async_write_ha_state()

            # Start a loop to receive data.
            try:
                async for data in self._websocket:
                    self._handle_websocket_data(data)
                    self.async_write_ha_state()
                    _LOGGER.warn(f'Processed message: {data}')
            except Exception as e:
                pass

            self._available = False
            self.async_write_ha_state()

    def _handle_websocket_data(self, data):
        _LOGGER.warn(f'Received message: {data}')
        try:
            message = json.loads(data)
            if 'is_on' in message:
                self._is_on = message['is_on']
            if 'tones' in message:
                self._tones = message['tones']
        except Exception as e:
            pass

    async def _set_tone(self, tone, duration=None):
        request = {'request': 'set_tone',
                   'tone': tone}
        if duration is not None:
            request['duration'] = duration
        await self._request(request)

    async def _turn_on(self, duration=None):
        request = {'request': 'turn_on'}
        if duration:
            request['duration'] = duration
        await self._request(request)

    async def _turn_off(self):
        request = {'request': 'turn_off'}
        await self._request(request)

    async def _request(self, request):
        _LOGGER.warn(f'Sending request: {request}')
        await self._websocket.send(json.dumps(request))

