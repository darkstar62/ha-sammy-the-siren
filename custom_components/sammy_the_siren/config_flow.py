""" Config flow """

import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import (
        DOMAIN,
        CONF_HOSTNAME,
        CONF_PORT
)
from .libsiren import validate_config


_LOGGER = logging.getLogger(__name__)


class SammyConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """ Config flow for Sammy the Siren """
    VERSION = 1
    MINOR_VERSION = 1

    def __init__(self):
        self.schema = vol.Schema({
            vol.Required(CONF_HOSTNAME): str,
            vol.Required(CONF_PORT): str,
        })

        self._hostname = None
        self._port = None

    async def async_step_user(self, user_input=None):
        if self._async_current_entries():
            self.async_abort(reason="Already configured")

        if not user_input:
            return self._show_form()

        self._hostname = user_input[CONF_HOSTNAME]
        self._port = user_input[CONF_PORT]

        _LOGGER.info(f'Got {self._hostname}:{self._port}')

        if not await validate_config(self._hostname, self._port):
            _LOGGER.error(f'Attempt failed')
            return self.show_form(errors={'base': 'connect_failure'})

        return await self._async_create_entry()

    async def _async_create_entry(self):
        config_data = {
                CONF_HOSTNAME: self._hostname,
                CONF_PORT: self._port,
        }

        return self.async_create_entry(title=self._hostname, data=config_data)

    @callback
    def _show_form(self, errors=None):
        return self.async_show_form(
                step_id="user",
                data_schema=self.schema,
                errors=errors if errors else {},
        )

