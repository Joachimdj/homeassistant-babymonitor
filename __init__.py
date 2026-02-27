"""Baby Monitor integration for Home Assistant."""
from __future__ import annotations

import logging
from datetime import datetime
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform, STATE_ON, STATE_OFF
from homeassistant.core import HomeAssistant, callback, Event
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.event import async_track_state_change_event

from .const import (
    DOMAIN,
    CONF_CAMERA_CRYING_ENTITY,
    CONF_CAMERA_AUTO_TRACKING,
    ACTIVITY_CRYING,
    CRYING_MODERATE,
)
from .services import async_setup_services, async_remove_services

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BUTTON,
]


class CameraCryingTracker:
    """Track crying episodes automatically from camera sensor."""

    def __init__(
        self,
        hass: HomeAssistant,
        baby_name: str,
        storage,
        camera_entity: str,
    ) -> None:
        """Initialize the camera crying tracker."""
        self._hass = hass
        self._baby_name = baby_name
        self._storage = storage
        self._camera_entity = camera_entity
        self._crying_start_time: datetime | None = None
        self._unsub = None

    async def async_start(self) -> None:
        """Start tracking camera state changes."""
        _LOGGER.info(
            "Starting camera crying tracking for %s using entity %s",
            self._baby_name,
            self._camera_entity,
        )
        
        # Subscribe to state changes
        self._unsub = async_track_state_change_event(
            self._hass,
            [self._camera_entity],
            self._handle_camera_state_change,
        )

    @callback
    def _handle_camera_state_change(self, event: Event) -> None:
        """Handle camera state changes."""
        new_state = event.data.get("new_state")
        old_state = event.data.get("old_state")
        
        if new_state is None or old_state is None:
            return
        
        # Check if state actually changed
        if new_state.state == old_state.state:
            return
        
        # Crying started
        if new_state.state == STATE_ON and old_state.state == STATE_OFF:
            self._hass.async_create_task(self._log_crying_start())
        
        # Crying stopped
        elif new_state.state == STATE_OFF and old_state.state == STATE_ON:
            self._hass.async_create_task(self._log_crying_end())

    async def _log_crying_start(self) -> None:
        """Log the start of a crying episode."""
        self._crying_start_time = datetime.now()
        
        _LOGGER.info(
            "Camera detected crying for %s at %s",
            self._baby_name,
            self._crying_start_time.strftime("%H:%M:%S"),
        )
        
        # Log initial crying event with 0 duration
        await self._storage.async_add_activity(
            ACTIVITY_CRYING,
            {
                "crying_intensity": CRYING_MODERATE,
                "duration": 0,
                "notes": "Auto-detected by camera (start)",
            },
        )
        
        # Update sensors
        await self._update_sensors()

    async def _log_crying_end(self) -> None:
        """Log the end of a crying episode with duration."""
        if self._crying_start_time is None:
            _LOGGER.warning("Crying end detected but no start time recorded")
            return
        
        # Calculate duration in minutes
        end_time = datetime.now()
        duration_seconds = (end_time - self._crying_start_time).total_seconds()
        duration_minutes = round(duration_seconds / 60)
        
        _LOGGER.info(
            "Camera detected crying stopped for %s. Duration: %d minutes",
            self._baby_name,
            duration_minutes,
        )
        
        # Log final crying event with actual duration
        await self._storage.async_add_activity(
            ACTIVITY_CRYING,
            {
                "crying_intensity": CRYING_MODERATE,
                "duration": duration_minutes,
                "notes": f"Auto-detected by camera ({duration_minutes} min)",
            },
        )
        
        # Clear start time
        self._crying_start_time = None
        
        # Update sensors
        await self._update_sensors()

    async def _update_sensors(self) -> None:
        """Update all sensors after logging activity."""
        from homeassistant.helpers.entity_component import async_update_entity
        from homeassistant.helpers.entity_registry import async_get as async_get_entity_registry
        
        entity_registry = async_get_entity_registry(self._hass)
        baby_slug = self._baby_name.lower().replace(" ", "_")
        
        # Update all sensors for this baby
        for entity_id, entry in entity_registry.entities.items():
            if (
                entry.domain == "sensor"
                and entry.platform == DOMAIN
                and baby_slug in entity_id
            ):
                await async_update_entity(self._hass, entity_id)

    def stop(self) -> None:
        """Stop tracking camera state changes."""
        if self._unsub:
            self._unsub()
            self._unsub = None
        _LOGGER.info("Stopped camera crying tracking for %s", self._baby_name)


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
        "baby_name": baby_name,
        "options": entry.options,
        "camera_tracker": None,
    }
    
    # Set up services (only once)
    if len(hass.data[DOMAIN]) == 1:
        await async_setup_services(hass)
    
    # Set up camera tracking if enabled
    camera_entity = entry.options.get(CONF_CAMERA_CRYING_ENTITY)
    camera_enabled = entry.options.get(CONF_CAMERA_AUTO_TRACKING, False)
    
    if camera_enabled and camera_entity:
        tracker = CameraCryingTracker(hass, baby_name, storage, camera_entity)
        await tracker.async_start()
        hass.data[DOMAIN][entry.entry_id]["camera_tracker"] = tracker
        _LOGGER.info(
            "Camera auto-tracking enabled for %s using %s",
            baby_name,
            camera_entity,
        )
    
    # Register update listener for options changes
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle options update."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # Stop camera tracker if it exists
    entry_data = hass.data[DOMAIN].get(entry.entry_id, {})
    camera_tracker = entry_data.get("camera_tracker")
    if camera_tracker:
        camera_tracker.stop()
    
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
        
        # Remove services if this was the last entry
        if not hass.data[DOMAIN]:
            await async_remove_services(hass)
    
    return unload_ok