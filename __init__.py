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
    from .storage import BabyMonitorStorage
    from .const import ATTR_BABY_NAME
    
    hass.data.setdefault(DOMAIN, {})
    
    # Initialize storage
    baby_name = entry.data[ATTR_BABY_NAME]
    storage = BabyMonitorStorage(hass, baby_name)
    await storage.async_load()
    
    # Store data for platforms to access
    hass.data[DOMAIN][entry.entry_id] = {
        "storage": storage,
        "baby_name": baby_name
    }
    
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