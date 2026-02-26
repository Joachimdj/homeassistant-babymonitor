"""Services for Baby Monitor integration."""
from __future__ import annotations

import logging
import voluptuous as vol
from datetime import datetime

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.entity_component import async_update_entity
from homeassistant.helpers.entity_registry import async_get as async_get_entity_registry

from .const import (
    DOMAIN,
    SERVICE_LOG_DIAPER_CHANGE,
    SERVICE_LOG_FEEDING,
    SERVICE_LOG_SLEEP,
    SERVICE_LOG_TEMPERATURE,
    SERVICE_LOG_WEIGHT,
    SERVICE_LOG_HEIGHT,
    SERVICE_LOG_MEDICATION,
    SERVICE_LOG_MILESTONE,
    SERVICE_LOG_BATH,
    SERVICE_LOG_TUMMY_TIME,
    SERVICE_LOG_CRYING,
    SERVICE_LOG_MOOD,
    SERVICE_LOG_ENVIRONMENTAL,
    SERVICE_LOG_CAREGIVER,
    ATTR_BABY_NAME,
    ATTR_DIAPER_TYPE,
    ATTR_FEEDING_TYPE,
    ATTR_FEEDING_AMOUNT,
    ATTR_FEEDING_DURATION,
    ATTR_SLEEP_TYPE,
    ATTR_TEMPERATURE,
    ATTR_WEIGHT,
    ATTR_HEIGHT,
    ATTR_MEDICATION_NAME,
    ATTR_MEDICATION_DOSAGE,
    ATTR_MILESTONE_NAME,
    ATTR_NOTES,
    ATTR_DURATION,
    ATTR_CRYING_INTENSITY,
    ATTR_MOOD_TYPE,
    ATTR_ROOM_TEMPERATURE,
    ATTR_HUMIDITY,
    ATTR_CAREGIVER_NAME,
    ATTR_BATH_TYPE,
    ACTIVITY_DIAPER_CHANGE,
    ACTIVITY_FEEDING,
    ACTIVITY_SLEEP,
    ACTIVITY_TEMPERATURE,
    ACTIVITY_WEIGHT,
    ACTIVITY_HEIGHT,
    ACTIVITY_MEDICATION,
    ACTIVITY_MILESTONE,
    ACTIVITY_BATH,
    ACTIVITY_TUMMY_TIME,
    ACTIVITY_CRYING,
    ACTIVITY_MOOD,
    ACTIVITY_ENVIRONMENTAL,
    ACTIVITY_CAREGIVER,
    DIAPER_WET,
    DIAPER_DIRTY,
    DIAPER_BOTH,
    FEEDING_BOTTLE,
    FEEDING_BREAST_LEFT,
    FEEDING_BREAST_RIGHT,
    FEEDING_BREAST_BOTH,
    FEEDING_SOLID,
    SLEEP_START,
    SLEEP_END,
)

_LOGGER = logging.getLogger(__name__)

# Service schemas
SERVICE_LOG_DIAPER_CHANGE_SCHEMA = vol.Schema({
    vol.Required(ATTR_BABY_NAME): cv.string,
    vol.Required(ATTR_DIAPER_TYPE): vol.In([DIAPER_WET, DIAPER_DIRTY, DIAPER_BOTH]),
    vol.Optional(ATTR_NOTES, default=""): cv.string,
})

SERVICE_LOG_FEEDING_SCHEMA = vol.Schema({
    vol.Required(ATTR_BABY_NAME): cv.string,
    vol.Required(ATTR_FEEDING_TYPE): vol.In([
        FEEDING_BOTTLE, FEEDING_BREAST_LEFT, FEEDING_BREAST_RIGHT, 
        FEEDING_BREAST_BOTH, FEEDING_SOLID
    ]),
    vol.Optional(ATTR_FEEDING_AMOUNT, default=0): cv.positive_int,
    vol.Optional(ATTR_FEEDING_DURATION, default=0): cv.positive_int,
    vol.Optional(ATTR_NOTES, default=""): cv.string,
})

SERVICE_LOG_SLEEP_SCHEMA = vol.Schema({
    vol.Required(ATTR_BABY_NAME): cv.string,
    vol.Required(ATTR_SLEEP_TYPE): vol.In([SLEEP_START, SLEEP_END]),
    vol.Optional(ATTR_NOTES, default=""): cv.string,
})

SERVICE_LOG_TEMPERATURE_SCHEMA = vol.Schema({
    vol.Required(ATTR_BABY_NAME): cv.string,
    vol.Required(ATTR_TEMPERATURE): vol.Coerce(float),
    vol.Optional(ATTR_NOTES, default=""): cv.string,
})

SERVICE_LOG_WEIGHT_SCHEMA = vol.Schema({
    vol.Required(ATTR_BABY_NAME): cv.string,
    vol.Required(ATTR_WEIGHT): vol.Coerce(float),
    vol.Optional(ATTR_NOTES, default=""): cv.string,
})

SERVICE_LOG_HEIGHT_SCHEMA = vol.Schema({
    vol.Required(ATTR_BABY_NAME): cv.string,
    vol.Required(ATTR_HEIGHT): vol.Coerce(float),
    vol.Optional(ATTR_NOTES, default=""): cv.string,
})

SERVICE_LOG_MEDICATION_SCHEMA = vol.Schema({
    vol.Required(ATTR_BABY_NAME): cv.string,
    vol.Required(ATTR_MEDICATION_NAME): cv.string,
    vol.Optional(ATTR_MEDICATION_DOSAGE, default=""): cv.string,
    vol.Optional(ATTR_NOTES, default=""): cv.string,
})

SERVICE_LOG_MILESTONE_SCHEMA = vol.Schema({
    vol.Required(ATTR_BABY_NAME): cv.string,
    vol.Required(ATTR_MILESTONE_NAME): cv.string,
    vol.Optional(ATTR_NOTES, default=""): cv.string,
})

SERVICE_LOG_BATH_SCHEMA = vol.Schema({
    vol.Required(ATTR_BABY_NAME): cv.string,
    vol.Optional(ATTR_BATH_TYPE, default="full_bath"): vol.In(["full_bath", "sponge_bath", "hair_wash"]),
    vol.Optional(ATTR_NOTES, default=""): cv.string,
})

SERVICE_LOG_TUMMY_TIME_SCHEMA = vol.Schema({
    vol.Required(ATTR_BABY_NAME): cv.string,
    vol.Required(ATTR_DURATION): vol.Coerce(int),
    vol.Optional(ATTR_NOTES, default=""): cv.string,
})

SERVICE_LOG_CRYING_SCHEMA = vol.Schema({
    vol.Required(ATTR_BABY_NAME): cv.string,
    vol.Optional(ATTR_CRYING_INTENSITY, default="moderate"): vol.In(["light", "moderate", "intense"]),
    vol.Optional(ATTR_DURATION, default=0): vol.Coerce(int),
    vol.Optional(ATTR_NOTES, default=""): cv.string,
})

SERVICE_LOG_MOOD_SCHEMA = vol.Schema({
    vol.Required(ATTR_BABY_NAME): cv.string,
    vol.Required(ATTR_MOOD_TYPE): vol.In(["happy", "fussy", "calm", "sleepy", "alert"]),
    vol.Optional(ATTR_NOTES, default=""): cv.string,
})

SERVICE_LOG_ENVIRONMENTAL_SCHEMA = vol.Schema({
    vol.Required(ATTR_BABY_NAME): cv.string,
    vol.Optional(ATTR_ROOM_TEMPERATURE, default=0): vol.Coerce(float),
    vol.Optional(ATTR_HUMIDITY, default=0): vol.Coerce(int),
    vol.Optional(ATTR_NOTES, default=""): cv.string,
})

SERVICE_LOG_CAREGIVER_SCHEMA = vol.Schema({
    vol.Required(ATTR_BABY_NAME): cv.string,
    vol.Required(ATTR_CAREGIVER_NAME): cv.string,
    vol.Optional(ATTR_NOTES, default=""): cv.string,
})


async def async_setup_services(hass: HomeAssistant) -> None:
    """Set up services for Baby Monitor integration."""
    
    async def log_diaper_change(call: ServiceCall) -> None:
        """Handle diaper change logging service call."""
        baby_name = call.data[ATTR_BABY_NAME]
        diaper_type = call.data[ATTR_DIAPER_TYPE]
        notes = call.data.get(ATTR_NOTES, "")
        
        storage = await _get_storage_for_baby(hass, baby_name)
        if storage:
            await storage.async_add_activity(
                ACTIVITY_DIAPER_CHANGE,
                {
                    "diaper_type": diaper_type,
                    "notes": notes
                }
            )
            _LOGGER.info(f"Logged diaper change for {baby_name}: {diaper_type}")
            # Trigger sensor updates
            await _update_sensors(hass, baby_name)
    
    async def log_feeding(call: ServiceCall) -> None:
        """Handle feeding logging service call."""
        baby_name = call.data[ATTR_BABY_NAME]
        feeding_type = call.data[ATTR_FEEDING_TYPE]
        feeding_amount = call.data.get(ATTR_FEEDING_AMOUNT, 0)
        feeding_duration = call.data.get(ATTR_FEEDING_DURATION, 0)
        notes = call.data.get(ATTR_NOTES, "")
        
        storage = await _get_storage_for_baby(hass, baby_name)
        if storage:
            await storage.async_add_activity(
                ACTIVITY_FEEDING,
                {
                    "feeding_type": feeding_type,
                    "feeding_amount": feeding_amount,
                    "feeding_duration": feeding_duration,
                    "notes": notes
                }
            )
            _LOGGER.info(f"Logged feeding for {baby_name}: {feeding_type}")
            # Trigger sensor updates
            await _update_sensors(hass, baby_name)
    
    async def log_sleep(call: ServiceCall) -> None:
        """Handle sleep logging service call."""
        baby_name = call.data[ATTR_BABY_NAME]
        sleep_type = call.data[ATTR_SLEEP_TYPE]
        notes = call.data.get(ATTR_NOTES, "")
        
        storage = await _get_storage_for_baby(hass, baby_name)
        if storage:
            data = {
                "sleep_type": sleep_type,
                "notes": notes
            }
            
            # If ending sleep, calculate duration from last sleep start
            if sleep_type == SLEEP_END:
                sleep_activities = storage.get_activities_by_type(ACTIVITY_SLEEP, limit=10)
                for activity in sleep_activities:
                    if activity["data"].get("sleep_type") == SLEEP_START:
                        start_time = datetime.fromisoformat(activity["timestamp"])
                        end_time = datetime.now()
                        duration = int((end_time - start_time).total_seconds() / 60)
                        data["duration"] = duration
                        break
            
            await storage.async_add_activity(ACTIVITY_SLEEP, data)
            _LOGGER.info(f"Logged sleep for {baby_name}: {sleep_type}")
            # Trigger sensor updates
            await _update_sensors(hass, baby_name)
    
    async def log_temperature(call: ServiceCall) -> None:
        """Handle temperature logging service call."""
        baby_name = call.data[ATTR_BABY_NAME]
        temperature = call.data[ATTR_TEMPERATURE]
        notes = call.data.get(ATTR_NOTES, "")
        
        storage = await _get_storage_for_baby(hass, baby_name)
        if storage:
            await storage.async_add_activity(
                ACTIVITY_TEMPERATURE,
                {
                    "temperature": temperature,
                    "notes": notes
                }
            )
            _LOGGER.info(f"Logged temperature for {baby_name}: {temperature}°C")
    
    async def log_weight(call: ServiceCall) -> None:
        """Handle weight logging service call."""
        baby_name = call.data[ATTR_BABY_NAME]
        weight = call.data[ATTR_WEIGHT]
        notes = call.data.get(ATTR_NOTES, "")
        
        storage = await _get_storage_for_baby(hass, baby_name)
        if storage:
            await storage.async_add_activity(
                ACTIVITY_WEIGHT,
                {
                    "weight": weight,
                    "notes": notes
                }
            )
            _LOGGER.info(f"Logged weight for {baby_name}: {weight}kg")
    
    async def log_height(call: ServiceCall) -> None:
        """Handle height logging service call."""
        baby_name = call.data[ATTR_BABY_NAME]
        height = call.data[ATTR_HEIGHT]
        notes = call.data.get(ATTR_NOTES, "")
        
        storage = await _get_storage_for_baby(hass, baby_name)
        if storage:
            await storage.async_add_activity(
                ACTIVITY_HEIGHT,
                {
                    "height": height,
                    "notes": notes
                }
            )
            _LOGGER.info(f"Logged height for {baby_name}: {height}cm")
    
    async def log_medication(call: ServiceCall) -> None:
        """Handle medication logging service call."""
        baby_name = call.data[ATTR_BABY_NAME]
        medication_name = call.data[ATTR_MEDICATION_NAME]
        medication_dosage = call.data.get(ATTR_MEDICATION_DOSAGE, "")
        notes = call.data.get(ATTR_NOTES, "")
        
        storage = await _get_storage_for_baby(hass, baby_name)
        if storage:
            await storage.async_add_activity(
                ACTIVITY_MEDICATION,
                {
                    "medication_name": medication_name,
                    "medication_dosage": medication_dosage,
                    "notes": notes
                }
            )
            _LOGGER.info(f"Logged medication for {baby_name}: {medication_name}")
    
    async def log_milestone(call: ServiceCall) -> None:
        """Handle milestone logging service call."""
        baby_name = call.data[ATTR_BABY_NAME]
        milestone_name = call.data[ATTR_MILESTONE_NAME]
        notes = call.data.get(ATTR_NOTES, "")
        
        storage = await _get_storage_for_baby(hass, baby_name)
        if storage:
            await storage.async_add_activity(
                ACTIVITY_MILESTONE,
                {
                    "milestone_name": milestone_name,
                    "notes": notes
                }
            )
            _LOGGER.info(f"Logged milestone for {baby_name}: {milestone_name}")
    
    async def log_bath(call: ServiceCall) -> None:
        """Handle bath logging service call."""
        baby_name = call.data[ATTR_BABY_NAME]
        bath_type = call.data.get(ATTR_BATH_TYPE, "full_bath")
        notes = call.data.get(ATTR_NOTES, "")
        
        storage = await _get_storage_for_baby(hass, baby_name)
        if storage:
            await storage.async_add_activity(
                ACTIVITY_BATH,
                {
                    "bath_type": bath_type,
                    "notes": notes
                }
            )
            _LOGGER.info(f"Logged bath for {baby_name}: {bath_type}")
    
    async def log_tummy_time(call: ServiceCall) -> None:
        """Handle tummy time logging service call."""
        baby_name = call.data[ATTR_BABY_NAME]
        duration = call.data[ATTR_DURATION]
        notes = call.data.get(ATTR_NOTES, "")
        
        storage = await _get_storage_for_baby(hass, baby_name)
        if storage:
            await storage.async_add_activity(
                ACTIVITY_TUMMY_TIME,
                {
                    "duration": duration,
                    "notes": notes
                }
            )
            _LOGGER.info(f"Logged tummy time for {baby_name}: {duration} minutes")
    
    async def log_crying(call: ServiceCall) -> None:
        """Handle crying logging service call."""
        baby_name = call.data[ATTR_BABY_NAME]
        intensity = call.data.get(ATTR_CRYING_INTENSITY, "moderate")
        duration = call.data.get(ATTR_DURATION, 0)
        notes = call.data.get(ATTR_NOTES, "")
        
        storage = await _get_storage_for_baby(hass, baby_name)
        if storage:
            await storage.async_add_activity(
                ACTIVITY_CRYING,
                {
                    "crying_intensity": intensity,
                    "duration": duration,
                    "notes": notes
                }
            )
            _LOGGER.info(f"Logged crying episode for {baby_name}: {intensity} intensity")
    
    async def log_mood(call: ServiceCall) -> None:
        """Handle mood logging service call."""
        baby_name = call.data[ATTR_BABY_NAME]
        mood_type = call.data[ATTR_MOOD_TYPE]
        notes = call.data.get(ATTR_NOTES, "")
        
        storage = await _get_storage_for_baby(hass, baby_name)
        if storage:
            await storage.async_add_activity(
                ACTIVITY_MOOD,
                {
                    "mood_type": mood_type,
                    "notes": notes
                }
            )
            _LOGGER.info(f"Logged mood for {baby_name}: {mood_type}")
    
    async def log_environmental(call: ServiceCall) -> None:
        """Handle environmental conditions logging service call."""
        baby_name = call.data[ATTR_BABY_NAME]
        room_temp = call.data.get(ATTR_ROOM_TEMPERATURE, 0)
        humidity = call.data.get(ATTR_HUMIDITY, 0)
        notes = call.data.get(ATTR_NOTES, "")
        
        storage = await _get_storage_for_baby(hass, baby_name)
        if storage:
            await storage.async_add_activity(
                ACTIVITY_ENVIRONMENTAL,
                {
                    "room_temperature": room_temp,
                    "humidity": humidity,
                    "notes": notes
                }
            )
            _LOGGER.info(f"Logged environmental conditions for {baby_name}: {room_temp}°C, {humidity}%")
    
    async def log_caregiver(call: ServiceCall) -> None:
        """Handle caregiver change logging service call."""
        baby_name = call.data[ATTR_BABY_NAME]
        caregiver_name = call.data[ATTR_CAREGIVER_NAME]
        notes = call.data.get(ATTR_NOTES, "")
        
        storage = await _get_storage_for_baby(hass, baby_name)
        if storage:
            await storage.async_add_activity(
                ACTIVITY_CAREGIVER,
                {
                    "caregiver_name": caregiver_name,
                    "notes": notes
                }
            )
            _LOGGER.info(f"Logged caregiver change for {baby_name}: {caregiver_name}")
    
    # Register services
    hass.services.async_register(
        DOMAIN, SERVICE_LOG_DIAPER_CHANGE, log_diaper_change, SERVICE_LOG_DIAPER_CHANGE_SCHEMA
    )
    hass.services.async_register(
        DOMAIN, SERVICE_LOG_FEEDING, log_feeding, SERVICE_LOG_FEEDING_SCHEMA
    )
    hass.services.async_register(
        DOMAIN, SERVICE_LOG_SLEEP, log_sleep, SERVICE_LOG_SLEEP_SCHEMA
    )
    hass.services.async_register(
        DOMAIN, SERVICE_LOG_TEMPERATURE, log_temperature, SERVICE_LOG_TEMPERATURE_SCHEMA
    )
    hass.services.async_register(
        DOMAIN, SERVICE_LOG_WEIGHT, log_weight, SERVICE_LOG_WEIGHT_SCHEMA
    )
    hass.services.async_register(
        DOMAIN, SERVICE_LOG_HEIGHT, log_height, SERVICE_LOG_HEIGHT_SCHEMA
    )
    hass.services.async_register(
        DOMAIN, SERVICE_LOG_MEDICATION, log_medication, SERVICE_LOG_MEDICATION_SCHEMA
    )
    hass.services.async_register(
        DOMAIN, SERVICE_LOG_MILESTONE, log_milestone, SERVICE_LOG_MILESTONE_SCHEMA
    )
    hass.services.async_register(
        DOMAIN, SERVICE_LOG_BATH, log_bath, SERVICE_LOG_BATH_SCHEMA
    )
    hass.services.async_register(
        DOMAIN, SERVICE_LOG_TUMMY_TIME, log_tummy_time, SERVICE_LOG_TUMMY_TIME_SCHEMA
    )
    hass.services.async_register(
        DOMAIN, SERVICE_LOG_CRYING, log_crying, SERVICE_LOG_CRYING_SCHEMA
    )
    hass.services.async_register(
        DOMAIN, SERVICE_LOG_MOOD, log_mood, SERVICE_LOG_MOOD_SCHEMA
    )
    hass.services.async_register(
        DOMAIN, SERVICE_LOG_ENVIRONMENTAL, log_environmental, SERVICE_LOG_ENVIRONMENTAL_SCHEMA
    )
    hass.services.async_register(
        DOMAIN, SERVICE_LOG_CAREGIVER, log_caregiver, SERVICE_LOG_CAREGIVER_SCHEMA
    )


async def async_remove_services(hass: HomeAssistant) -> None:
    """Remove services for Baby Monitor integration."""
    hass.services.async_remove(DOMAIN, SERVICE_LOG_DIAPER_CHANGE)
    hass.services.async_remove(DOMAIN, SERVICE_LOG_FEEDING)
    hass.services.async_remove(DOMAIN, SERVICE_LOG_SLEEP)
    hass.services.async_remove(DOMAIN, SERVICE_LOG_TEMPERATURE)
    hass.services.async_remove(DOMAIN, SERVICE_LOG_WEIGHT)
    hass.services.async_remove(DOMAIN, SERVICE_LOG_HEIGHT)
    hass.services.async_remove(DOMAIN, SERVICE_LOG_MEDICATION)
    hass.services.async_remove(DOMAIN, SERVICE_LOG_MILESTONE)
    hass.services.async_remove(DOMAIN, SERVICE_LOG_BATH)
    hass.services.async_remove(DOMAIN, SERVICE_LOG_TUMMY_TIME)
    hass.services.async_remove(DOMAIN, SERVICE_LOG_CRYING)
    hass.services.async_remove(DOMAIN, SERVICE_LOG_MOOD)
    hass.services.async_remove(DOMAIN, SERVICE_LOG_ENVIRONMENTAL)
    hass.services.async_remove(DOMAIN, SERVICE_LOG_CAREGIVER)


async def _get_storage_for_baby(hass: HomeAssistant, baby_name: str):
    """Get storage instance for the specified baby."""
    for entry_id, data in hass.data.get(DOMAIN, {}).items():
        if "storage" in data:
            storage = data["storage"]
            if storage._baby_name == baby_name:
                return storage
    return None


async def _update_sensors(hass: HomeAssistant, baby_name: str) -> None:
    """Trigger sensor updates for the specified baby."""
    # Get entity registry
    ent_reg = async_get_entity_registry(hass)
    
    # Find all sensors for this baby
    baby_id = baby_name.lower().replace(" ", "_")
    
    # Update all entities for this baby
    for entity in ent_reg.entities.values():
        if entity.unique_id and entity.unique_id.startswith(f"{baby_id}_"):
            if entity.domain == "sensor":
                # Trigger entity update
                await async_update_entity(hass, entity.entity_id)