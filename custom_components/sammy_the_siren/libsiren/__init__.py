""" Module implementing the Siren API. """

import asyncio
import json
import logging
import websockets

_LOGGER = logging.getLogger(__name__)


async def validate_config(hostname: str, port: int) -> bool:
    url = f'ws://{hostname}:{port}'

    try:
        websocket = await websockets.connect(url)
        await websocket.close()
    except Exception as e:
        return False

    return True


class Siren:
    """ Implements the API for communicating with a siren. """

    def __init__(self, hostname: str, port: int):
        self._hostname = hostname
        self._port = port
        self._url = f'ws://{hostname}:{port}'

        self._available = False
        self._is_on = False
        self._tones = []

        self._on_update = None
        self._disconnect = False

    @property
    def hostname(self):
        return self._hostname

    @property
    def url(self):
        return self._url

    @property
    def is_on(self):
        return self._is_on

    @property
    def tones(self):
        return self._tones

    @property
    def available(self):
        return self._available

    def initialize(self) -> None:
        self._disconnect = False
        asyncio.ensure_future(self._connect())

    def on_update(self, callback):
        self._on_update = callback
        self._on_update()

    async def disconnect(self) -> None:
        self._disconnect = True
        await self._websocket.close()
        _LOGGER.debug(f'Connection disconnect completed')

    async def set_tone(self, tone, duration=None):
        request = {'request': 'set_tone',
                   'tone': tone}
        if duration is not None:
            request['duration'] = duration
        await self._request(request)

    async def turn_on(self, duration=None):
        request = {'request': 'turn_on'}
        if duration:
            request['duration'] = duration
        await self._request(request)

    async def turn_off(self):
        request = {'request': 'turn_off'}
        await self._request(request)

    async def _connect(self):
        while not self._disconnect:
            # Keep trying to connect until we get it.
            try:
                _LOGGER.debug('Establishing connection')
                self._websocket = await websockets.connect(self._url)
            except Exception as e:
                await asyncio.sleep(5)
                continue

            await self._websocket.send(json.dumps({'request': 'get_tones'}))
            self._available = True
            self._update()

            # Start a loop to receive data.
            try:
                async for data in self._websocket:
                    self._handle_websocket_data(data)
                    self._update()
                    _LOGGER.debug(f'Processed message: {data}')
            except Exception as e:
                _LOGGER.warn(f'Error waiting for data: {e}')
                pass

            self._available = False
            self._update()

    def _handle_websocket_data(self, data):
        _LOGGER.debug(f'Received message: {data}')
        try:
            message = json.loads(data)
            if 'is_on' in message:
                self._is_on = message['is_on']
            if 'tones' in message:
                self._tones = message['tones']
        except Exception as e:
            pass

    async def _request(self, request):
        _LOGGER.debug(f'Sending request: {request}')
        await self._websocket.send(json.dumps(request))

    def _update(self):
        if self._on_update is not None:
            self._on_update()

