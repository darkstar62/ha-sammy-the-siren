""" Defines a base siren entity. """

from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import SirenDataUpdateCoordinator


class BaseSirenEntity(CoordinatorEntity[SirenDataUpdateCoordinator]):
    """ Base siren entity. """

    _attr_has_entity_name = False

    def __init__(
        self,
        coordinator: SirenDataUpdateCoordinator,
        hostname: str,
    ) -> None:
        """ Initialize the entity. """
        super().__init__(coordinator)

        self._hostname = hostname
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, hostname)},
            manufacturer="Sammy Siren Company",
            name="Sammy the Siren",
        )

