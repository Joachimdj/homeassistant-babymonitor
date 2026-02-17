"""Sensor platform for Baby Monitor integration."""
from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Any

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.restore_state import RestoreEntity

from .const import (
    DOMAIN, 
    ATTR_BABY_NAME,
    ACTIVITY_DIAPER_CHANGE,
    ACTIVITY_FEEDING,
    ACTIVITY_SLEEP,
    ACTIVITY_TEMPERATURE,
)
from .storage import BabyMonitorStorage

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Baby Monitor sensors from a config entry."""
    baby_name = config_entry.data[ATTR_BABY_NAME]
    
    # Initialize storage
    storage = BabyMonitorStorage(hass, baby_name)
    await storage.async_load()
    
    # Store storage instance for use by other platforms
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}
    hass.data[DOMAIN][config_entry.entry_id] = {"storage": storage}
    
    sensors = [
        LastDiaperChangeSensor(baby_name, storage),
        LastFeedingSensor(baby_name, storage),
        LastSleepSensor(baby_name, storage),
        TotalDiaperChangesSensor(baby_name, storage),
        TotalFeedingsSensor(baby_name, storage),
        TotalSleepSessionsSensor(baby_name, storage),
        AverageSleepDurationSensor(baby_name, storage),
        AverageFeedingAmountSensor(baby_name, storage),
        DailySummaryDisplaySensor(baby_name, storage),
        WeeklySummaryDisplaySensor(baby_name, storage),
        CurrentTemperatureSensor(baby_name, storage),
    ]
    
    async_add_entities(sensors, True)


class BabyMonitorSensorBase(SensorEntity, RestoreEntity):
    """Base class for Baby Monitor sensors."""
    
    def __init__(self, baby_name: str, storage: BabyMonitorStorage) -> None:
        """Initialize the sensor."""
        self._baby_name = baby_name
        self._storage = storage
        self._attr_name = f"{baby_name} {self._sensor_name}"
        self._attr_unique_id = f"{baby_name.lower().replace(' ', '_')}_{self._sensor_id}"
    
    @property
    def device_info(self) -> dict[str, Any]:
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self._baby_name)},
            "name": f"{self._baby_name} Monitor",
            "manufacturer": "Baby Monitor",
            "model": "Baby Care Tracker",
        }


class LastDiaperChangeSensor(BabyMonitorSensorBase):
    """Sensor for last diaper change time."""
    
    _sensor_name = "Last Diaper Change"
    _sensor_id = "last_diaper_change"
    
    @property
    def state(self) -> str | None:
        """Return the state of the sensor."""
        stats = self._storage.get_stats()
        last_change = stats.get("last_diaper_change")
        if last_change:
            dt = datetime.fromisoformat(last_change)
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        return "Never"
    
    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes."""
        activities = self._storage.get_activities_by_type(ACTIVITY_DIAPER_CHANGE, 1)
        if activities:
            return {
                "diaper_type": activities[0]["data"].get("diaper_type", "unknown"),
                "notes": activities[0]["data"].get("notes", ""),
                "time_ago": self._get_time_ago(activities[0]["timestamp"])
            }
        return {}
    
    def _get_time_ago(self, timestamp: str) -> str:
        """Get human readable time ago."""
        dt = datetime.fromisoformat(timestamp)
        diff = datetime.now() - dt
        
        if diff.days > 0:
            return f"{diff.days} days ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hours ago"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} minutes ago"
        else:
            return "Just now"


class LastFeedingSensor(BabyMonitorSensorBase):
    """Sensor for last feeding time."""
    
    _sensor_name = "Last Feeding"
    _sensor_id = "last_feeding"
    
    @property
    def state(self) -> str | None:
        """Return the state of the sensor."""
        stats = self._storage.get_stats()
        last_feeding = stats.get("last_feeding")
        if last_feeding:
            dt = datetime.fromisoformat(last_feeding)
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        return "Never"
    
    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes."""
        activities = self._storage.get_activities_by_type(ACTIVITY_FEEDING, 1)
        if activities:
            data = activities[0]["data"]
            return {
                "feeding_type": data.get("feeding_type", "unknown"),
                "amount_ml": data.get("feeding_amount", 0),
                "duration_minutes": data.get("feeding_duration", 0),
                "notes": data.get("notes", ""),
                "time_ago": self._get_time_ago(activities[0]["timestamp"])
            }
        return {}
    
    def _get_time_ago(self, timestamp: str) -> str:
        """Get human readable time ago."""
        dt = datetime.fromisoformat(timestamp)
        diff = datetime.now() - dt
        
        if diff.days > 0:
            return f"{diff.days} days ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hours ago"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} minutes ago"
        else:
            return "Just now"


class LastSleepSensor(BabyMonitorSensorBase):
    """Sensor for last sleep session."""
    
    _sensor_name = "Last Sleep"
    _sensor_id = "last_sleep"
    
    @property
    def state(self) -> str | None:
        """Return the state of the sensor."""
        stats = self._storage.get_stats()
        last_sleep = stats.get("last_sleep")
        if last_sleep:
            dt = datetime.fromisoformat(last_sleep)
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        return "Never"
    
    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes."""
        activities = self._storage.get_activities_by_type(ACTIVITY_SLEEP, 5)
        
        # Find the latest completed sleep session
        for activity in activities:
            if activity["data"].get("sleep_type") == "end":
                duration = activity["data"].get("duration", 0)
                hours = duration // 60
                minutes = duration % 60
                return {
                    "duration_minutes": duration,
                    "duration_formatted": f"{hours}h {minutes}m",
                    "notes": activity["data"].get("notes", ""),
                    "time_ago": self._get_time_ago(activity["timestamp"])
                }
        return {}
    
    def _get_time_ago(self, timestamp: str) -> str:
        """Get human readable time ago."""
        dt = datetime.fromisoformat(timestamp)
        diff = datetime.now() - dt
        
        if diff.days > 0:
            return f"{diff.days} days ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hours ago"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} minutes ago"
        else:
            return "Just now"


class TotalDiaperChangesSensor(BabyMonitorSensorBase):
    """Sensor for total diaper changes."""
    
    _sensor_name = "Total Diaper Changes"
    _sensor_id = "total_diaper_changes"
    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    
    @property
    def state(self) -> int:
        """Return the state of the sensor."""
        stats = self._storage.get_stats()
        return stats.get("total_diaper_changes", 0)
    
    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes."""
        today = datetime.now().date()
        today_start = datetime.combine(today, datetime.min.time()).isoformat()
        today_end = datetime.combine(today, datetime.max.time()).isoformat()
        
        today_changes = self._storage.get_activities_by_date_range(today_start, today_end)
        today_diaper_changes = [a for a in today_changes if a["type"] == ACTIVITY_DIAPER_CHANGE]
        
        return {
            "today_count": len(today_diaper_changes),
            "wet_today": len([a for a in today_diaper_changes if a["data"].get("diaper_type") in ["wet", "both"]]),
            "dirty_today": len([a for a in today_diaper_changes if a["data"].get("diaper_type") in ["dirty", "both"]]),
        }


class TotalFeedingsSensor(BabyMonitorSensorBase):
    """Sensor for total feedings."""
    
    _sensor_name = "Total Feedings"
    _sensor_id = "total_feedings"
    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    
    @property
    def state(self) -> int:
        """Return the state of the sensor."""
        stats = self._storage.get_stats()
        return stats.get("total_feedings", 0)
    
    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes."""
        today = datetime.now().date()
        today_start = datetime.combine(today, datetime.min.time()).isoformat()
        today_end = datetime.combine(today, datetime.max.time()).isoformat()
        
        today_activities = self._storage.get_activities_by_date_range(today_start, today_end)
        today_feedings = [a for a in today_activities if a["type"] == ACTIVITY_FEEDING]
        
        total_amount_today = sum(f["data"].get("feeding_amount", 0) for f in today_feedings)
        
        return {
            "today_count": len(today_feedings),
            "total_amount_today_ml": total_amount_today,
            "bottle_feedings_today": len([f for f in today_feedings if f["data"].get("feeding_type") == "bottle"]),
            "breast_feedings_today": len([f for f in today_feedings if "breast" in f["data"].get("feeding_type", "")]),
        }


class TotalSleepSessionsSensor(BabyMonitorSensorBase):
    """Sensor for total sleep sessions."""
    
    _sensor_name = "Total Sleep Sessions"
    _sensor_id = "total_sleep_sessions"
    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    
    @property
    def state(self) -> int:
        """Return the state of the sensor."""
        stats = self._storage.get_stats()
        return stats.get("total_sleep_sessions", 0)


class AverageSleepDurationSensor(BabyMonitorSensorBase):
    """Sensor for average sleep duration."""
    
    _sensor_name = "Average Sleep Duration"
    _sensor_id = "average_sleep_duration"
    _attr_unit_of_measurement = "minutes"
    
    @property
    def state(self) -> float:
        """Return the state of the sensor."""
        stats = self._storage.get_stats()
        return round(stats.get("average_sleep_duration", 0), 1)


class AverageFeedingAmountSensor(BabyMonitorSensorBase):
    """Sensor for average feeding amount."""
    
    _sensor_name = "Average Feeding Amount"
    _sensor_id = "average_feeding_amount"
    _attr_unit_of_measurement = "ml"
    
    @property
    def state(self) -> float:
        """Return the state of the sensor."""
        stats = self._storage.get_stats()
        return round(stats.get("average_feeding_amount", 0), 1)


class CurrentTemperatureSensor(BabyMonitorSensorBase):
    """Sensor for current/last recorded temperature."""
    
    _sensor_name = "Temperature"
    _sensor_id = "current_temperature"
    _attr_unit_of_measurement = "°C"
    _attr_device_class = "temperature"
    
    @property
    def state(self) -> float | None:
        """Return the state of the sensor."""
        activities = self._storage.get_activities_by_type(ACTIVITY_TEMPERATURE, 1)
        if activities:
            return activities[0]["data"].get("temperature")
        return None
    
    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes."""
        activities = self._storage.get_activities_by_type(ACTIVITY_TEMPERATURE, 1)
        if activities:
            return {
                "last_recorded": activities[0]["timestamp"],
                "notes": activities[0]["data"].get("notes", ""),
                "time_ago": self._get_time_ago(activities[0]["timestamp"])
            }
        return {}
    
    def _get_time_ago(self, timestamp: str) -> str:
        """Get human readable time ago."""
        dt = datetime.fromisoformat(timestamp)
        diff = datetime.now() - dt
        
        if diff.days > 0:
            return f"{diff.days} days ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hours ago"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} minutes ago"
        else:
            return "Just now"


class DailySummaryDisplaySensor(BabyMonitorSensorBase):
    """Display sensor with daily summary information."""
    
    _sensor_name = "Daily Summary"
    _sensor_id = "daily_summary"
    
    @property
    def state(self) -> str:
        """Return a summary state."""
        today = datetime.now().date()
        today_start = datetime.combine(today, datetime.min.time()).isoformat()
        today_end = datetime.combine(today, datetime.max.time()).isoformat()
        
        today_activities = self._storage.get_activities_by_date_range(today_start, today_end)
        
        diaper_count = len([a for a in today_activities if a["type"] == ACTIVITY_DIAPER_CHANGE])
        feeding_count = len([a for a in today_activities if a["type"] == ACTIVITY_FEEDING])
        sleep_count = len([a for a in today_activities if a["type"] == ACTIVITY_SLEEP and a["data"].get("sleep_type") == "end"])
        
        return f"D:{diaper_count} F:{feeding_count} S:{sleep_count}"
    
    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return detailed daily summary."""
        today = datetime.now().date()
        today_start = datetime.combine(today, datetime.min.time()).isoformat()
        today_end = datetime.combine(today, datetime.max.time()).isoformat()
        
        today_activities = self._storage.get_activities_by_date_range(today_start, today_end)
        
        diaper_changes = [a for a in today_activities if a["type"] == ACTIVITY_DIAPER_CHANGE]
        feedings = [a for a in today_activities if a["type"] == ACTIVITY_FEEDING]
        sleep_sessions = [a for a in today_activities if a["type"] == ACTIVITY_SLEEP and a["data"].get("sleep_type") == "end"]
        
        total_feeding_amount = sum(f["data"].get("feeding_amount", 0) for f in feedings)
        total_sleep_minutes = sum(s["data"].get("duration", 0) for s in sleep_sessions)
        
        return {
            "date": today.isoformat(),
            "diaper_changes": len(diaper_changes),
            "wet_diapers": len([d for d in diaper_changes if d["data"].get("diaper_type") in ["wet", "both"]]),
            "dirty_diapers": len([d for d in diaper_changes if d["data"].get("diaper_type") in ["dirty", "both"]]),
            "feedings": len(feedings),
            "total_feeding_amount_ml": total_feeding_amount,
            "sleep_sessions": len(sleep_sessions),
            "total_sleep_minutes": total_sleep_minutes,
            "total_sleep_formatted": f"{total_sleep_minutes // 60}h {total_sleep_minutes % 60}m"
        }


class WeeklySummaryDisplaySensor(BabyMonitorSensorBase):
    """Display sensor with weekly summary information."""
    
    _sensor_name = "Weekly Summary"
    _sensor_id = "weekly_summary"
    
    @property
    def state(self) -> str:
        """Return a summary state."""
        week_start = (datetime.now() - timedelta(days=7)).isoformat()
        week_end = datetime.now().isoformat()
        
        week_activities = self._storage.get_activities_by_date_range(week_start, week_end)
        
        diaper_count = len([a for a in week_activities if a["type"] == ACTIVITY_DIAPER_CHANGE])
        feeding_count = len([a for a in week_activities if a["type"] == ACTIVITY_FEEDING])
        sleep_count = len([a for a in week_activities if a["type"] == ACTIVITY_SLEEP and a["data"].get("sleep_type") == "end"])
        
        return f"7d: D:{diaper_count} F:{feeding_count} S:{sleep_count}"
    
    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return detailed weekly summary."""
        week_start = (datetime.now() - timedelta(days=7)).isoformat()
        week_end = datetime.now().isoformat()
        
        week_activities = self._storage.get_activities_by_date_range(week_start, week_end)
        
        diaper_changes = [a for a in week_activities if a["type"] == ACTIVITY_DIAPER_CHANGE]
        feedings = [a for a in week_activities if a["type"] == ACTIVITY_FEEDING]
        sleep_sessions = [a for a in week_activities if a["type"] == ACTIVITY_SLEEP and a["data"].get("sleep_type") == "end"]
        
        total_feeding_amount = sum(f["data"].get("feeding_amount", 0) for f in feedings)
        total_sleep_minutes = sum(s["data"].get("duration", 0) for s in sleep_sessions)
        
        # Calculate daily averages
        avg_diapers_per_day = len(diaper_changes) / 7
        avg_feedings_per_day = len(feedings) / 7
        avg_sleep_per_day = total_sleep_minutes / 7
        
        return {
            "period_start": week_start,
            "period_end": week_end,
            "total_diaper_changes": len(diaper_changes),
            "total_feedings": len(feedings),
            "total_feeding_amount_ml": total_feeding_amount,
            "total_sleep_sessions": len(sleep_sessions),
            "total_sleep_minutes": total_sleep_minutes,
            "avg_diapers_per_day": round(avg_diapers_per_day, 1),
            "avg_feedings_per_day": round(avg_feedings_per_day, 1),
            "avg_sleep_minutes_per_day": round(avg_sleep_per_day, 1),
            "avg_sleep_per_day_formatted": f"{int(avg_sleep_per_day // 60)}h {int(avg_sleep_per_day % 60)}m"
        }