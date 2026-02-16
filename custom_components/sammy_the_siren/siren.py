""" Platform for siren integration """
import logging
from homeassistant.components.siren import (
    SirenEntityFeature,
    SirenEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from .const import DOMAIN
from .coordinator import SirenDataUpdateCoordinator
from .entity import BaseSirenEntity
from .libsiren import Siren

_LOGGER = logging.getLogger(__name__)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """ Platform uses config entry setup. """
    pass

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """ Setup Sammy. """
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entity = SammySiren(hass, coordinator)
    async_add_entities([entity])

    entity.initialize()


class SammySiren(BaseSirenEntity, SirenEntity):
    _attr_supported_features = (
            SirenEntityFeature.TONES
            | SirenEntityFeature.TURN_ON
            | SirenEntityFeature.TURN_OFF
            | SirenEntityFeature.DURATION)

    def __init__(
        self,
        hass: HomeAssistant,
        coordinator: SirenDataUpdateCoordinator,
    ):
        super().__init__(coordinator, coordinator.siren.hostname)
        self.siren = coordinator.siren
        self.hass = hass

    def initialize(self):
        self.siren.on_update(self.async_write_ha_state)

    @property
    def unique_id(self):
        return self.siren.hostname

    @property
    def icon(self):
        return 'mdi:siren'

    @property
    def is_on(self):
        return self.siren.is_on

    @property
    def should_poll(self):
        return False

    @property
    def available_tones(self):
        return self.siren.tones

    @property
    def available(self):
        return self.siren.available

    ## SirenEntity Implementation

    async def async_turn_on(self, **kwargs) -> None:
        """ Turn the siren on """
        duration = None if 'duration' not in kwargs else kwargs['duration']

        if 'tone' in kwargs:
            tone = kwargs['tone']
            await self.siren.set_tone(tone, duration)
        else:
            await self.siren.turn_on(duration)

    async def async_turn_off(self, **kwargs) -> None:
        """ Turn the siren off """
        await self.siren.turn_off()

