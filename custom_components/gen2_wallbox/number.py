"""Platform for sensor integration."""
from __future__ import annotations

import logging

from homeassistant.components.number import NumberEntity
from homeassistant.const import ELECTRIC_CURRENT_AMPERE, EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
):
    """Set up the Ally binary_sensor platform."""
    _LOGGER.info("Setting up GEN2 Wallbox numbers")
    gen2 = hass.data[DOMAIN][entry.entry_id]

    entities = [WallBoxChargingCurrent(gen2)]

    async_add_entities(entities, True)


class WallBoxChargingCurrent(NumberEntity):
    """Representation actual output current of the Wallbox."""

    _attr_has_entity_name = True
    _attr_name = "Charging current"
    _attr_unique_id = "wallbox_charging_current"
    _attr_native_max_value = 16
    _attr_native_step = 1
    _attr_native_min_value = 8
    _attr_native_unit_of_measurement = ELECTRIC_CURRENT_AMPERE
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, device) -> None:
        super().__init__()
        self.device = device

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return self.device.device_info

    @property
    def native_value(self) -> int | None:
        """Return the state of the number entity."""
        data = self.device.get_value("Set32A")
        if data == None:
            self._attr_available = False
            return None
        else:
            self._attr_available = True
            return int(data)

    async def async_set_native_value(self, value: float) -> None:
        """Set the value of the entity."""
        _LOGGER.info(f"Seting Set32A: {value}")
        out = self.device.set_value("Set32A", int(value))
        self.device.update()
