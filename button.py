"""Button platform for Baby Monitor integration."""
from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN,
    ACTIVITY_DIAPER_CHANGE,
    ACTIVITY_FEEDING,
    ACTIVITY_SLEEP,
    DIAPER_WET,
    DIAPER_DIRTY,
    DIAPER_BOTH,
    FEEDING_BOTTLE,
    FEEDING_BREAST_LEFT,
    FEEDING_BREAST_RIGHT,
    FEEDING_BREAST_BOTH,
    SLEEP_START,
    SLEEP_END,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Baby Monitor buttons from a config entry."""
    # Get storage and baby name from data set up in __init__.py
    data = hass.data[DOMAIN][config_entry.entry_id]
    baby_name = data["baby_name"]
    storage = data["storage"]
    
    buttons = [
        QuickDiaperWetButton(baby_name, storage),
        QuickDiaperDirtyButton(baby_name, storage),
        QuickDiaperBothButton(baby_name, storage),
        QuickFeedingBottleButton(baby_name, storage),
        QuickFeedingBreastLeftButton(baby_name, storage),
        QuickFeedingBreastRightButton(baby_name, storage),
        QuickFeedingBreastBothButton(baby_name, storage),
        QuickSleepStartButton(baby_name, storage),
        QuickSleepEndButton(baby_name, storage),
        QuickBathButton(baby_name, storage),
        QuickTummyTimeButton(baby_name, storage),
        QuickHappyMoodButton(baby_name, storage),
        QuickCalmMoodButton(baby_name, storage),
        QuickCryingButton(baby_name, storage),
        LogCaregiverButton(baby_name, storage),
    ]
    
    async_add_entities(buttons, True)


class BabyMonitorButtonBase(ButtonEntity):
    """Base class for Baby Monitor buttons."""
    
    def __init__(self, baby_name: str, storage) -> None:
        """Initialize the button."""
        self._baby_name = baby_name
        self._storage = storage
        self._attr_name = f"{baby_name} {self._button_name}"
        self._attr_unique_id = f"{baby_name.lower().replace(' ', '_')}_{self._button_id}"
    
    @property
    def device_info(self) -> dict[str, Any]:
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self._baby_name)},
            "name": f"{self._baby_name} Monitor",
            "manufacturer": "Baby Monitor",
            "model": "Baby Care Tracker",
        }
    
    async def _trigger_sensor_updates(self) -> None:
        """Trigger sensor updates after button press."""
        from homeassistant.helpers import entity_registry
        
        # Get entity registry
        ent_reg = entity_registry.async_get(self.hass)
        
        # Find all sensors for this baby
        baby_id = self._baby_name.lower().replace(" ", "_")
        
        # Update all sensor entities for this baby
        for entity in ent_reg.entities.values():
            if entity.unique_id and entity.unique_id.startswith(f"{baby_id}_"):
                if entity.domain == "sensor":
                    # Trigger entity update
                    self.hass.async_create_task(
                        self.hass.helpers.entity_component.async_update_entity(entity.entity_id)
                    )


class QuickDiaperWetButton(BabyMonitorButtonBase):
    """Quick button for wet diaper change."""
    
    _button_name = "Quick Wet Diaper"
    _button_id = "quick_wet_diaper"
    _attr_icon = "mdi:water"
    
    async def async_press(self) -> None:
        """Handle the button press."""
        await self._storage.async_add_activity(
            ACTIVITY_DIAPER_CHANGE,
            {"diaper_type": DIAPER_WET, "notes": "Quick log"}
        )
        await self._trigger_sensor_updates()


class QuickDiaperDirtyButton(BabyMonitorButtonBase):
    """Quick button for dirty diaper change."""
    
    _button_name = "Quick Dirty Diaper"
    _button_id = "quick_dirty_diaper"
    _attr_icon = "mdi:delete-variant"
    
    async def async_press(self) -> None:
        """Handle the button press."""
        await self._storage.async_add_activity(
            ACTIVITY_DIAPER_CHANGE,
            {"diaper_type": DIAPER_DIRTY, "notes": "Quick log"}
        )
        await self._trigger_sensor_updates()


class QuickDiaperBothButton(BabyMonitorButtonBase):
    """Quick button for wet and dirty diaper change."""
    
    _button_name = "Quick Wet & Dirty Diaper"
    _button_id = "quick_both_diaper"
    _attr_icon = "mdi:water-alert"
    
    async def async_press(self) -> None:
        """Handle the button press."""
        await self._storage.async_add_activity(
            ACTIVITY_DIAPER_CHANGE,
            {"diaper_type": DIAPER_BOTH, "notes": "Quick log"}
        )
        await self._trigger_sensor_updates()


class QuickFeedingBottleButton(BabyMonitorButtonBase):
    """Quick button for bottle feeding."""
    
    _button_name = "Quick Bottle Feeding"
    _button_id = "quick_bottle_feeding"
    _attr_icon = "mdi:bottle-tonic-skull"
    
    async def async_press(self) -> None:
        """Handle the button press."""
        await self._storage.async_add_activity(
            ACTIVITY_FEEDING,
            {
                "feeding_type": FEEDING_BOTTLE,
                "feeding_amount": 120,  # Default amount
                "feeding_duration": 15,  # Default duration
                "notes": "Quick log"
            }
        )
        await self._trigger_sensor_updates()


class QuickFeedingBreastLeftButton(BabyMonitorButtonBase):
    """Quick button for left breast feeding."""
    
    _button_name = "Quick Breast Feeding (Left)"
    _button_id = "quick_breast_left_feeding"
    _attr_icon = "mdi:human-female"
    
    async def async_press(self) -> None:
        """Handle the button press."""
        await self._storage.async_add_activity(
            ACTIVITY_FEEDING,
            {
                "feeding_type": FEEDING_BREAST_LEFT,
                "feeding_duration": 15,  # Default duration
                "notes": "Quick log - Left breast"
            }
        )
        await self._trigger_sensor_updates()


class QuickFeedingBreastRightButton(BabyMonitorButtonBase):
    """Quick button for right breast feeding."""
    
    _button_name = "Quick Breast Feeding (Right)"
    _button_id = "quick_breast_right_feeding"
    _attr_icon = "mdi:human-female"
    
    async def async_press(self) -> None:
        """Handle the button press."""
        await self._storage.async_add_activity(
            ACTIVITY_FEEDING,
            {
                "feeding_type": FEEDING_BREAST_RIGHT,
                "feeding_duration": 15,  # Default duration
                "notes": "Quick log - Right breast"
            }
        )
        await self._trigger_sensor_updates()


class QuickFeedingBreastBothButton(BabyMonitorButtonBase):
    """Quick button for both breasts feeding."""
    
    _button_name = "Quick Breast Feeding (Both)"
    _button_id = "quick_breast_both_feeding"
    _attr_icon = "mdi:human-female"
    
    async def async_press(self) -> None:
        """Handle the button press."""
        await self._storage.async_add_activity(
            ACTIVITY_FEEDING,
            {
                "feeding_type": FEEDING_BREAST_BOTH,
                "feeding_duration": 25,  # Default duration
                "notes": "Quick log - Both breasts"
            }
        )
        await self._trigger_sensor_updates()


class QuickSleepStartButton(BabyMonitorButtonBase):
    """Quick button to start sleep tracking."""
    
    _button_name = "Start Sleep"
    _button_id = "quick_sleep_start"
    _attr_icon = "mdi:sleep"
    
    async def async_press(self) -> None:
        """Handle the button press."""
        await self._storage.async_add_activity(
            ACTIVITY_SLEEP,
            {
                "sleep_type": SLEEP_START,
                "notes": "Sleep started"
            }
        )
        await self._trigger_sensor_updates()


class QuickSleepEndButton(BabyMonitorButtonBase):
    """Quick button to end sleep tracking."""
    
    _button_name = "End Sleep"
    _button_id = "quick_sleep_end"
    _attr_icon = "mdi:sleep-off"
    
    async def async_press(self) -> None:
        """Handle the button press."""
        # Calculate duration from last sleep start
        sleep_activities = self._storage.get_activities_by_type(ACTIVITY_SLEEP, limit=10)
        duration = 0
        
        for activity in sleep_activities:
            if activity["data"].get("sleep_type") == SLEEP_START:
                start_time = datetime.fromisoformat(activity["timestamp"])
                end_time = datetime.now()
                duration = int((end_time - start_time).total_seconds() / 60)
                break
        
        await self._storage.async_add_activity(
            ACTIVITY_SLEEP,
            {
                "sleep_type": SLEEP_END,
                "duration": duration,
                "notes": f"Sleep ended - Duration: {duration // 60}h {duration % 60}m"
            }
        )
        await self._trigger_sensor_updates()


class QuickBathButton(BabyMonitorButtonBase):
    """Button for logging a quick bath."""
    
    _button_name = "Quick Bath"
    _button_id = "quick_bath"
    
    async def async_press(self) -> None:
        """Handle the button press."""
        await self._storage.async_add_activity(
            "bath",
            {
                "bath_type": "full_bath",
                "notes": "Quick bath logged"
            }
        )
        await self._trigger_sensor_updates()


class QuickTummyTimeButton(BabyMonitorButtonBase):
    """Button for logging tummy time session."""
    
    _button_name = "Quick Tummy Time"
    _button_id = "quick_tummy_time"
    
    async def async_press(self) -> None:
        """Handle the button press."""
        await self._storage.async_add_activity(
            "tummy_time",
            {
                "duration": 10,  # Default 10 minute session
                "notes": "Tummy time session completed"
            }
        )
        await self._trigger_sensor_updates()


class QuickHappyMoodButton(BabyMonitorButtonBase):
    """Button for logging happy mood."""
    
    _button_name = "Happy Mood"
    _button_id = "quick_happy_mood"
    
    async def async_press(self) -> None:
        """Handle the button press."""
        await self._storage.async_add_activity(
            "mood",
            {
                "mood_type": "happy",
                "notes": "Baby is happy and content"
            }
        )
        await self._trigger_sensor_updates()


class QuickCalmMoodButton(BabyMonitorButtonBase):
    """Button for logging calm mood."""
    
    _button_name = "Calm Mood"
    _button_id = "quick_calm_mood"
    
    async def async_press(self) -> None:
        """Handle the button press."""
        await self._storage.async_add_activity(
            "mood",
            {
                "mood_type": "calm",
                "notes": "Baby is calm and relaxed"
            }
        )
        await self._trigger_sensor_updates()


class QuickCryingButton(BabyMonitorButtonBase):
    """Button for logging crying episode start."""
    
    _button_name = "Start Crying"
    _button_id = "quick_crying"
    
    async def async_press(self) -> None:
        """Handle the button press."""
        await self._storage.async_add_activity(
            "crying",
            {
                "crying_intensity": "moderate",
                "duration": 0,  # Will be updated when crying ends
                "notes": "Crying episode started"
            }
        )
        await self._trigger_sensor_updates()


class LogCaregiverButton(BabyMonitorButtonBase):
    """Button for switching caregiver."""
    
    _button_name = "Switch Caregiver"
    _button_id = "switch_caregiver"
    
    async def async_press(self) -> None:
        """Handle the button press."""
        # This would ideally prompt for caregiver name, for now using "Parent"
        await self._storage.async_add_activity(
            "caregiver",
            {
                "caregiver_name": "Parent",
                "notes": "Caregiver changed"
            }
        )
        await self._trigger_sensor_updates()