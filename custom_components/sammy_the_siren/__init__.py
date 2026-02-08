""" Integration main """

from homeassistant.const import Platform
import requests
from .const import (CONF_HOSTNAME, CONF_PORT, DOMAIN)


PLATFORMS: list[Platform] = [
        Platform.SIREN,
]

def setup(hass, config):
    return True


class SirenDevice:
    def __init__(self, hostname, port):
        self._hostname = hostname
        self._port = port
        self._url = f'http://{hostname}:{port}'
        self._is_on = False
        self._tones = []

    def init(self):
        response = self._request('/tone')
        if not response.ok:
            return False

        self._tones = response.json()['tone']
        return True

    def set_tone(self, tone, duration=None):
        url = f'/tone/{tone}'
        if duration:
            url += f'?duration={duration}'

        response = self._request(url)
        if response.ok:
            self._is_on = True

    def turn_on(self, duration=None):
        url = f'/on'
        if duration:
            url += f'?duration={duration}'
        response = self._request(url)
        if response.ok:
            self._is_on = True

    def turn_off(self):
        response = self._request('/off')
        if response.ok:
            self._is_on = False

    def update(self):
        response = self._request('/is_on')
        if response.ok:
            self._is_on = response.json()['on']

    @property
    def is_on(self):
        return self._is_on

    @property
    def hostname(self):
        return self._hostname

    @property
    def tones(self):
        return self._tones

    def _request(self, path):
        url = self._url + path
        return requests.get(url)


async def async_setup_entry(hass, config_entry):
    hostname = config_entry.data.get(CONF_HOSTNAME)
    port = config_entry.data.get(CONF_PORT)

    device = SirenDevice(hostname, port)
    if not await hass.async_add_executor_job(device.init):
        return False

    hass.data[DOMAIN] = device

    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)
    return True

