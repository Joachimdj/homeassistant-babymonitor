"""Baby Monitor integration for Home Assistant."""
from __future__ import annotations

import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN
from .services import async_setup_services, async_remove_services

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BUTTON,
]


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Baby Monitor component."""
    _LOGGER.info("Setting up Baby Monitor integration")
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Baby Monitor from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data
    
    # Set up services (only once)
    if len(hass.data[DOMAIN]) == 1:
        await async_setup_services(hass)
    
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
        
        # Remove services if this was the last entry
        if not hass.data[DOMAIN]:
            await async_remove_services(hass)
    
    return unload_ok