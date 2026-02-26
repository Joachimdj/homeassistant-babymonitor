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
    ACTIVITY_DIAPER_CHANGE,
    ACTIVITY_FEEDING,
    ACTIVITY_SLEEP,
    ACTIVITY_TEMPERATURE,
    CONF_MIN_DIAPERS_PER_DAY,
    CONF_MIN_WET_DIAPERS_PER_DAY,
    CONF_MIN_FEEDINGS_PER_DAY,
    CONF_MIN_SLEEP_HOURS_PER_DAY,
    CONF_TARGET_TUMMY_TIME_MINUTES,
    DEFAULT_MIN_DIAPERS_PER_DAY,
    DEFAULT_MIN_WET_DIAPERS_PER_DAY,
    DEFAULT_MIN_FEEDINGS_PER_DAY,
    DEFAULT_MIN_SLEEP_HOURS_PER_DAY,
    DEFAULT_TARGET_TUMMY_TIME_MINUTES,
)
from .storage import BabyMonitorStorage

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Baby Monitor sensors from a config entry."""
    # Get storage and baby name from data set up in __init__.py
    data = hass.data[DOMAIN][config_entry.entry_id]
    baby_name = data["baby_name"]
    storage = data["storage"]
    options = data["options"]
    
    sensors = [
        LastDiaperChangeSensor(baby_name, storage, options),
        LastFeedingSensor(baby_name, storage, options),
        LastSleepSensor(baby_name, storage, options),
        TotalDiaperChangesSensor(baby_name, storage, options),
        TotalFeedingsSensor(baby_name, storage, options),
        TotalSleepSessionsSensor(baby_name, storage, options),
        AverageSleepDurationSensor(baby_name, storage, options),
        AverageFeedingAmountSensor(baby_name, storage, options),
        DailySummaryDisplaySensor(baby_name, storage, options),
        WeeklySummaryDisplaySensor(baby_name, storage, options),
        CurrentTemperatureSensor(baby_name, storage, options),
        LastBathSensor(baby_name, storage, options),
        TummyTimeTodaySensor(baby_name, storage, options),
        SleepQualityScoreSensor(baby_name, storage, options),
        GrowthPercentileSensor(baby_name, storage, options),
        NextFeedingPredictionSensor(baby_name, storage, options),
        MoodAnalysisSensor(baby_name, storage, options),
        CryingAnalysisSensor(baby_name, storage, options),
        EnvironmentalConditionsSensor(baby_name, storage, options),
        CurrentCaregiverSensor(baby_name, storage, options),
        GrowthVelocitySensor(baby_name, storage, options),
        SleepRegressionIndicatorSensor(baby_name, storage, options),
        DiaperChangeFrequencySensor(baby_name, storage, options),
        FeedingEfficiencySensor(baby_name, storage, options),
    ]
    
    async_add_entities(sensors, True)


class BabyMonitorSensorBase(SensorEntity, RestoreEntity):
    """Base class for Baby Monitor sensors."""
    
    def __init__(self, baby_name: str, storage: BabyMonitorStorage, options: dict[str, Any]) -> None:
        """Initialize the sensor."""
        self._baby_name = baby_name
        self._storage = storage
        self._options = options
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
    _attr_icon = "mdi:baby-bottle"
    
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
        activities = self._storage.get_activities_by_type(ACTIVITY_DIAPER_CHANGE, limit=1)
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
        activities = self._storage.get_activities_by_type(ACTIVITY_FEEDING, limit=1)
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
        activities = self._storage.get_activities_by_type(ACTIVITY_SLEEP, limit=5)
        
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
        
        today_count = len(today_diaper_changes)
        wet_today = len([a for a in today_diaper_changes if a["data"].get("diaper_type") in ["wet", "both"]])
        dirty_today = len([a for a in today_diaper_changes if a["data"].get("diaper_type") in ["dirty", "both"]])
        
        # Get configured thresholds
        min_diapers = self._options.get(CONF_MIN_DIAPERS_PER_DAY, DEFAULT_MIN_DIAPERS_PER_DAY)
        min_wet_diapers = self._options.get(CONF_MIN_WET_DIAPERS_PER_DAY, DEFAULT_MIN_WET_DIAPERS_PER_DAY)
        
        # Calculate status
        diaper_status = "Meeting goal" if today_count >= min_diapers else "Below goal"
        wet_status = "Meeting goal" if wet_today >= min_wet_diapers else "Below goal"
        
        return {
            "today_count": today_count,
            "wet_today": wet_today,
            "dirty_today": dirty_today,
            "min_diapers_goal": min_diapers,
            "min_wet_diapers_goal": min_wet_diapers,
            "diaper_status": diaper_status,
            "wet_diaper_status": wet_status,
            "progress_percentage": round((today_count / min_diapers * 100), 0) if min_diapers > 0 else 100,
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
        today_count = len(today_feedings)
        
        # Get configured threshold
        min_feedings = self._options.get(CONF_MIN_FEEDINGS_PER_DAY, DEFAULT_MIN_FEEDINGS_PER_DAY)
        
        # Calculate status
        feeding_status = "Meeting goal" if today_count >= min_feedings else "Below goal"
        
        return {
            "today_count": today_count,
            "total_amount_today_ml": total_amount_today,
            "bottle_feedings_today": len([f for f in today_feedings if f["data"].get("feeding_type") == "bottle"]),
            "breast_feedings_today": len([f for f in today_feedings if "breast" in f["data"].get("feeding_type", "")]),
            "min_feedings_goal": min_feedings,
            "feeding_status": feeding_status,
            "progress_percentage": round((today_count / min_feedings * 100), 0) if min_feedings > 0 else 100,
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
    _attr_state_class = SensorStateClass.MEASUREMENT
    
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
    _attr_state_class = SensorStateClass.MEASUREMENT
    
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
    _attr_state_class = SensorStateClass.MEASUREMENT
    
    @property
    def state(self) -> float | None:
        """Return the state of the sensor."""
        activities = self._storage.get_activities_by_type(ACTIVITY_TEMPERATURE, limit=1)
        if activities:
            return activities[0]["data"].get("temperature")
        return None
    
    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes."""
        activities = self._storage.get_activities_by_type(ACTIVITY_TEMPERATURE, limit=1)
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


class LastBathSensor(BabyMonitorSensorBase):
    """Sensor for last bath time."""
    
    _sensor_name = "Last Bath"
    _sensor_id = "last_bath"
    
    @property
    def native_value(self) -> str | None:
        activities = self._storage.get_activities_by_type("bath")
        if not activities:
            return "Never"
        
        last_activity = activities[-1]
        last_time = datetime.fromisoformat(last_activity["timestamp"])
        return last_time.strftime("%Y-%m-%d %H:%M")
    
    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        activities = self._storage.get_activities_by_type("bath")
        if not activities:
            return {}
        
        last_activity = activities[-1]
        last_time = datetime.fromisoformat(last_activity["timestamp"])
        time_since = datetime.now() - last_time
        
        return {
            "timestamp": last_activity["timestamp"],
            "bath_type": last_activity["data"].get("bath_type", "full_bath"),
            "hours_since": round(time_since.total_seconds() / 3600, 1),
            "days_since": round(time_since.days, 1),
            "notes": last_activity["data"].get("notes", "")
        }


class TummyTimeTodaySensor(BabyMonitorSensorBase):
    """Sensor for today's tummy time duration."""
    
    _sensor_name = "Tummy Time Today"
    _sensor_id = "tummy_time_today"
    _attr_unit_of_measurement = "min"
    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    
    @property
    def native_value(self) -> int:
        today_activities = self._storage.get_daily_activities()
        tummy_time_activities = [a for a in today_activities if a["type"] == "tummy_time"]
        total_minutes = sum(a["data"].get("duration", 0) for a in tummy_time_activities)
        return total_minutes
    
    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        today_activities = self._storage.get_daily_activities()
        tummy_time_activities = [a for a in today_activities if a["type"] == "tummy_time"]
        
        # Get configured target
        target_minutes = self._options.get(CONF_TARGET_TUMMY_TIME_MINUTES, DEFAULT_TARGET_TUMMY_TIME_MINUTES)
        
        # Calculate status
        tummy_time_status = "Meeting goal" if self.native_value >= target_minutes else "Below goal"
        
        return {
            "sessions_today": len(tummy_time_activities),
            "target_daily_minutes": target_minutes,
            "progress_percentage": min(100, round((self.native_value / target_minutes) * 100, 0)) if target_minutes > 0 and self.native_value else 0,
            "tummy_time_status": tummy_time_status,
        }


class SleepQualityScoreSensor(BabyMonitorSensorBase):
    """Sensor for sleep quality analysis."""
    
    _sensor_name = "Sleep Quality Score"
    _sensor_id = "sleep_quality_score"
    _attr_unit_of_measurement = "%"
    _attr_state_class = SensorStateClass.MEASUREMENT
    
    @property
    def native_value(self) -> int:
        """Calculate sleep quality score based on recent patterns."""
        recent_activities = self._storage.get_activities_since_days(3)
        sleep_activities = [a for a in recent_activities if a["type"] == ACTIVITY_SLEEP]
        
        if len(sleep_activities) < 4:  # Need some data
            return 50
        
        # Analyze sleep sessions (pairs of start/end)
        sleep_sessions = []
        start_activity = None
        
        for activity in sleep_activities:
            if activity["data"].get("sleep_type") == "start":
                start_activity = activity
            elif activity["data"].get("sleep_type") == "end" and start_activity:
                duration = activity["data"].get("duration", 0)
                sleep_sessions.append({
                    "duration": duration,
                    "start_time": start_activity["timestamp"],
                    "end_time": activity["timestamp"]
                })
                start_activity = None
        
        if not sleep_sessions:
            return 50
        
        # Calculate quality factors
        avg_duration = sum(s["duration"] for s in sleep_sessions) / len(sleep_sessions)
        
        # Quality factors (0-100 each)
        duration_score = min(100, (avg_duration / 60) * 100)  # 60 min = perfect
        consistency_score = max(0, 100 - (len(sleep_sessions) - 6) * 10)  # 6 sessions ideal
        
        overall_score = (duration_score * 0.6 + consistency_score * 0.4)
        return round(overall_score)
    
    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        recent_activities = self._storage.get_activities_since_days(3)
        sleep_activities = [a for a in recent_activities if a["type"] == ACTIVITY_SLEEP]
        
        # Calculate sessions
        sleep_sessions = []
        start_activity = None
        
        for activity in sleep_activities:
            if activity["data"].get("sleep_type") == "start":
                start_activity = activity
            elif activity["data"].get("sleep_type") == "end" and start_activity:
                duration = activity["data"].get("duration", 0)
                sleep_sessions.append(duration)
                start_activity = None
        
        if not sleep_sessions:
            return {"analysis": "Insufficient data"}
        
        avg_duration = sum(sleep_sessions) / len(sleep_sessions)
        longest_session = max(sleep_sessions)
        
        return {
            "average_session_duration": f"{int(avg_duration)}min",
            "longest_session": f"{int(longest_session)}min",
            "sessions_in_3_days": len(sleep_sessions),
            "analysis_period": "3 days"
        }


class GrowthPercentileSensor(BabyMonitorSensorBase):
    """Sensor for growth percentile tracking."""
    
    _sensor_name = "Growth Percentile"
    _sensor_id = "growth_percentile"
    _attr_unit_of_measurement = "%"
    _attr_state_class = SensorStateClass.MEASUREMENT
    
    @property
    def native_value(self) -> int | None:
        """Calculate approximate growth percentile."""
        weight_activities = self._storage.get_activities_by_type("weight")
        height_activities = self._storage.get_activities_by_type("height")
        
        if not weight_activities or not height_activities:
            return None
        
        # Get latest measurements
        latest_weight = weight_activities[-1]["data"].get("weight", 0)
        latest_height = height_activities[-1]["data"].get("height", 0)
        
        # Simplified percentile calculation (would need proper WHO charts in real implementation)
        # This is a mock calculation for demo purposes
        if latest_weight > 0 and latest_height > 0:
            # Mock percentile based on ratio (simplified)
            ratio = latest_weight / (latest_height / 100) ** 2  # Simple BMI-like calculation
            if ratio < 12:
                return 10
            elif ratio < 14:
                return 25
            elif ratio < 16:
                return 50
            elif ratio < 18:
                return 75
            else:
                return 90
        
        return 50  # Default middle percentile
    
    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        weight_activities = self._storage.get_activities_by_type("weight")
        height_activities = self._storage.get_activities_by_type("height")
        
        latest_weight = weight_activities[-1]["data"].get("weight", 0) if weight_activities else 0
        latest_height = height_activities[-1]["data"].get("height", 0) if height_activities else 0
        
        return {
            "latest_weight_kg": latest_weight,
            "latest_height_cm": latest_height,
            "chart_reference": "WHO Growth Standards",
            "note": "Consult pediatrician for official growth assessment"
        }


class NextFeedingPredictionSensor(BabyMonitorSensorBase):
    """Sensor for predicting next feeding time."""
    
    _sensor_name = "Next Feeding Prediction"
    _sensor_id = "next_feeding_prediction"
    
    @property
    def native_value(self) -> str:
        """Predict next feeding time based on recent patterns."""
        feeding_activities = self._storage.get_activities_by_type(ACTIVITY_FEEDING)
        
        if len(feeding_activities) < 3:
            return "Insufficient data"
        
        # Get last 5 feeding times
        recent_feedings = feeding_activities[-5:]
        intervals = []
        
        for i in range(1, len(recent_feedings)):
            prev_time = datetime.fromisoformat(recent_feedings[i-1]["timestamp"])
            curr_time = datetime.fromisoformat(recent_feedings[i]["timestamp"])
            interval_hours = (curr_time - prev_time).total_seconds() / 3600
            intervals.append(interval_hours)
        
        if not intervals:
            return "Insufficient data"
        
        # Calculate average interval
        avg_interval = sum(intervals) / len(intervals)
        
        # Predict next feeding
        last_feeding_time = datetime.fromisoformat(feeding_activities[-1]["timestamp"])
        predicted_next = last_feeding_time + timedelta(hours=avg_interval)
        
        if predicted_next < datetime.now():
            return "Due now"
        
        return predicted_next.strftime("%H:%M")
    
    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        feeding_activities = self._storage.get_activities_by_type(ACTIVITY_FEEDING)
        
        if len(feeding_activities) < 3:
            return {"status": "Need more feeding data"}
        
        # Calculate intervals
        recent_feedings = feeding_activities[-5:]
        intervals = []
        
        for i in range(1, len(recent_feedings)):
            prev_time = datetime.fromisoformat(recent_feedings[i-1]["timestamp"])
            curr_time = datetime.fromisoformat(recent_feedings[i]["timestamp"])
            interval_hours = (curr_time - prev_time).total_seconds() / 3600
            intervals.append(interval_hours)
        
        avg_interval = sum(intervals) / len(intervals) if intervals else 3
        last_feeding = datetime.fromisoformat(feeding_activities[-1]["timestamp"])
        time_since_last = (datetime.now() - last_feeding).total_seconds() / 3600
        
        return {
            "average_interval_hours": round(avg_interval, 1),
            "hours_since_last_feeding": round(time_since_last, 1),
            "pattern_confidence": "High" if len(intervals) >= 4 else "Medium",
            "last_feeding": last_feeding.strftime("%H:%M")
        }


class MoodAnalysisSensor(BabyMonitorSensorBase):
    """Sensor for mood pattern analysis."""
    
    _sensor_name = "Current Mood"
    _sensor_id = "current_mood"
    
    @property
    def native_value(self) -> str:
        """Get current/latest mood."""
        mood_activities = self._storage.get_activities_by_type("mood")
        
        if not mood_activities:
            return "Unknown"
        
        latest_mood = mood_activities[-1]["data"].get("mood_type", "Unknown")
        return latest_mood.title()
    
    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        today_moods = [a for a in self._storage.get_daily_activities() if a["type"] == "mood"]
        week_moods = [a for a in self._storage.get_activities_since_days(7) if a["type"] == "mood"]
        
        if not today_moods:
            return {"analysis": "No mood data today"}
        
        # Count mood types today
        mood_counts = {}
        for mood in today_moods:
            mood_type = mood["data"].get("mood_type", "unknown")
            mood_counts[mood_type] = mood_counts.get(mood_type, 0) + 1
        
        dominant_mood = max(mood_counts, key=mood_counts.get) if mood_counts else "unknown"
        
        return {
            "dominant_mood_today": dominant_mood.title(),
            "mood_changes_today": len(today_moods),
            "mood_counts_today": mood_counts,
            "mood_stability": "Stable" if len(today_moods) <= 3 else "Variable"
        }


class CryingAnalysisSensor(BabyMonitorSensorBase):
    """Sensor for crying pattern analysis."""
    
    _sensor_name = "Crying Analysis"
    _sensor_id = "crying_analysis"
    
    @property
    def native_value(self) -> str:
        """Get crying status summary."""
        today_crying = [a for a in self._storage.get_daily_activities() if a["type"] == "crying"]
        
        if not today_crying:
            return "No crying recorded"
        
        total_duration = sum(a["data"].get("duration", 0) for a in today_crying)
        episodes = len(today_crying)
        
        if episodes == 0:
            return "Peaceful day"
        elif episodes <= 2 and total_duration <= 30:
            return "Minimal crying"
        elif episodes <= 5 and total_duration <= 60:
            return "Normal fussiness"
        else:
            return "Fussy day"
    
    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        today_crying = [a for a in self._storage.get_daily_activities() if a["type"] == "crying"]
        
        if not today_crying:
            return {"status": "No crying episodes today"}
        
        total_duration = sum(a["data"].get("duration", 0) for a in today_crying)
        intensities = [a["data"].get("crying_intensity", "moderate") for a in today_crying]
        intensity_counts = {}
        
        for intensity in intensities:
            intensity_counts[intensity] = intensity_counts.get(intensity, 0) + 1
        
        return {
            "episodes_today": len(today_crying),
            "total_duration_minutes": total_duration,
            "average_episode_duration": round(total_duration / len(today_crying), 1) if today_crying else 0,
            "intensity_breakdown": intensity_counts,
            "last_episode": today_crying[-1]["timestamp"] if today_crying else None
        }


class EnvironmentalConditionsSensor(BabyMonitorSensorBase):
    """Sensor for environmental monitoring."""
    
    _sensor_name = "Room Conditions"
    _sensor_id = "room_conditions"
    
    @property
    def native_value(self) -> str:
        """Get latest environmental conditions."""
        env_activities = self._storage.get_activities_by_type("environmental")
        
        if not env_activities:
            return "Not monitored"
        
        latest = env_activities[-1]["data"]
        temp = latest.get("room_temperature", 0)
        humidity = latest.get("humidity", 0)
        
        if temp > 0:
            return f"{temp}°C, {humidity}%"
        
        return "No recent data"
    
    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        env_activities = self._storage.get_activities_by_type("environmental")
        
        if not env_activities:
            return {"status": "Environmental monitoring not active"}
        
        latest = env_activities[-1]["data"]
        temp = latest.get("room_temperature", 0)
        humidity = latest.get("humidity", 0)
        
        # Assess conditions
        temp_status = "optimal" if 18 <= temp <= 22 else ("too_warm" if temp > 22 else "too_cool")
        humidity_status = "optimal" if 30 <= humidity <= 60 else ("too_humid" if humidity > 60 else "too_dry")
        
        return {
            "room_temperature": temp,
            "humidity": humidity,
            "temperature_status": temp_status,
            "humidity_status": humidity_status,
            "overall_comfort": "Good" if temp_status == "optimal" and humidity_status == "optimal" else "Needs attention",
            "last_update": env_activities[-1]["timestamp"]
        }


class CurrentCaregiverSensor(BabyMonitorSensorBase):
    """Sensor for tracking current caregiver."""
    
    _sensor_name = "Current Caregiver"
    _sensor_id = "current_caregiver"
    
    @property
    def native_value(self) -> str:
        """Get current caregiver on duty."""
        caregiver_activities = self._storage.get_activities_by_type("caregiver")
        
        if not caregiver_activities:
            return "Unknown"
        
        latest = caregiver_activities[-1]["data"]
        return latest.get("caregiver_name", "Unknown")
    
    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        caregiver_activities = self._storage.get_activities_by_type("caregiver")
        today_activities = self._storage.get_daily_activities()
        
        if not caregiver_activities:
            return {"status": "Caregiver tracking not active"}
        
        # Count activities by caregiver today
        caregiver_stats = {}
        for activity in today_activities:
            if activity["type"] in [ACTIVITY_DIAPER_CHANGE, ACTIVITY_FEEDING]:
                caregiver = "Unknown"  # Would need to track this in activity data
                caregiver_stats[caregiver] = caregiver_stats.get(caregiver, 0) + 1
        
        latest_change = datetime.fromisoformat(caregiver_activities[-1]["timestamp"])
        duration = datetime.now() - latest_change
        
        return {
            "on_duty_since": caregiver_activities[-1]["timestamp"],
            "duration_hours": round(duration.total_seconds() / 3600, 1),
            "shift_changes_today": len([a for a in today_activities if a["type"] == "caregiver"])
        }


class GrowthVelocitySensor(BabyMonitorSensorBase):
    """Sensor for growth velocity tracking."""
    
    _sensor_name = "Growth Velocity"
    _sensor_id = "growth_velocity"
    _attr_unit_of_measurement = "g/day"
    _attr_state_class = SensorStateClass.MEASUREMENT
    
    @property
    def native_value(self) -> float | None:
        """Calculate daily weight gain velocity."""
        weight_activities = self._storage.get_activities_by_type("weight")
        
        if len(weight_activities) < 2:
            return None
        
        # Get last two measurements
        latest = weight_activities[-1]
        previous = weight_activities[-2]
        
        latest_weight = latest["data"].get("weight", 0) * 1000  # Convert to grams
        previous_weight = previous["data"].get("weight", 0) * 1000
        
        latest_time = datetime.fromisoformat(latest["timestamp"])
        previous_time = datetime.fromisoformat(previous["timestamp"])
        
        days_diff = (latest_time - previous_time).total_seconds() / (24 * 3600)
        
        if days_diff > 0:
            velocity = (latest_weight - previous_weight) / days_diff
            return round(velocity, 1)
        
        return None
    
    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        weight_activities = self._storage.get_activities_by_type("weight")
        
        if len(weight_activities) < 2:
            return {"status": "Need more weight measurements"}
        
        velocity = self.native_value
        
        # Typical growth ranges for reference
        if velocity and velocity > 0:
            if 15 <= velocity <= 30:
                growth_assessment = "Normal"
            elif velocity > 30:
                growth_assessment = "Rapid"
            else:
                growth_assessment = "Slow"
        else:
            growth_assessment = "Concerning"
        
        return {
            "growth_assessment": growth_assessment,
            "measurement_count": len(weight_activities),
            "latest_weight_kg": weight_activities[-1]["data"].get("weight", 0),
            "normal_range": "15-30 g/day",
            "note": "Consult pediatrician for growth concerns"
        }


class SleepRegressionIndicatorSensor(BabyMonitorSensorBase):
    """Sensor for detecting sleep pattern disruptions."""
    
    _sensor_name = "Sleep Pattern Status"
    _sensor_id = "sleep_pattern_status"
    
    @property
    def native_value(self) -> str:
        """Analyze recent sleep patterns for regression indicators."""
        recent_activities = self._storage.get_activities_since_days(7)
        older_activities = self._storage.get_activities_since_days(14)
        
        recent_sleep = [a for a in recent_activities if a["type"] == ACTIVITY_SLEEP and a["data"].get("sleep_type") == "end"]
        older_sleep = [a for a in older_activities[-14:-7] if a["type"] == ACTIVITY_SLEEP and a["data"].get("sleep_type") == "end"]
        
        if len(recent_sleep) < 3 or len(older_sleep) < 3:
            return "Insufficient data"
        
        # Compare average sleep duration
        recent_avg = sum(s["data"].get("duration", 0) for s in recent_sleep) / len(recent_sleep)
        older_avg = sum(s["data"].get("duration", 0) for s in older_sleep) / len(older_sleep)
        
        # Check for significant decrease in sleep duration
        decrease_percentage = ((older_avg - recent_avg) / older_avg) * 100 if older_avg > 0 else 0
        
        if decrease_percentage > 25:
            return "Sleep Regression Detected"
        elif decrease_percentage > 15:
            return "Sleep Pattern Disruption"
        elif decrease_percentage < -10:
            return "Sleep Improvement"
        else:
            return "Normal Pattern"
    
    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        recent_activities = self._storage.get_activities_since_days(7)
        recent_sleep = [a for a in recent_activities if a["type"] == ACTIVITY_SLEEP and a["data"].get("sleep_type") == "end"]
        
        if not recent_sleep:
            return {"analysis": "No recent sleep data"}
        
        recent_avg = sum(s["data"].get("duration", 0) for s in recent_sleep) / len(recent_sleep)
        night_wakings = len([s for s in recent_sleep if s["data"].get("duration", 0) < 60])  # Short sleeps indicate wakings
        
        return {
            "recent_average_duration": f"{int(recent_avg)}min",
            "sleep_sessions_this_week": len(recent_sleep),
            "short_sleeps_this_week": night_wakings,
            "pattern_stability": "Stable" if night_wakings <= 7 else "Unstable",
            "analysis_period": "7 days vs previous 7 days"
        }


class DiaperChangeFrequencySensor(BabyMonitorSensorBase):
    """Sensor for diaper change frequency analysis."""
    
    _sensor_name = "Diaper Change Frequency"
    _sensor_id = "diaper_change_frequency"
    _attr_unit_of_measurement = "changes/day"
    _attr_state_class = SensorStateClass.MEASUREMENT
    
    @property
    def native_value(self) -> float:
        """Calculate average diaper changes per day."""
        week_activities = self._storage.get_activities_since_days(7)
        diaper_changes = [a for a in week_activities if a["type"] == ACTIVITY_DIAPER_CHANGE]
        
        return round(len(diaper_changes) / 7, 1)
    
    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        today_activities = self._storage.get_daily_activities()
        week_activities = self._storage.get_activities_since_days(7)
        
        today_changes = [a for a in today_activities if a["type"] == ACTIVITY_DIAPER_CHANGE]
        week_changes = [a for a in week_activities if a["type"] == ACTIVITY_DIAPER_CHANGE]
        
        # Analyze types
        wet_changes = len([a for a in week_changes if a["data"].get("diaper_type") in ["wet", "both"]])
        dirty_changes = len([a for a in week_changes if a["data"].get("diaper_type") in ["dirty", "both"]])
        
        return {
            "changes_today": len(today_changes),
            "changes_this_week": len(week_changes),
            "wet_changes_week": wet_changes,
            "dirty_changes_week": dirty_changes,
            "frequency_status": "Normal" if 4 <= self.native_value <= 12 else ("Low" if self.native_value < 4 else "High"),
            "normal_range": "4-12 changes per day"
        }


class FeedingEfficiencySensor(BabyMonitorSensorBase):
    """Sensor for feeding efficiency analysis."""
    
    _sensor_name = "Feeding Efficiency"
    _sensor_id = "feeding_efficiency"
    _attr_unit_of_measurement = "ml/min"
    _attr_state_class = SensorStateClass.MEASUREMENT
    
    @property
    def native_value(self) -> float | None:
        """Calculate average feeding efficiency."""
        feeding_activities = self._storage.get_activities_by_type(ACTIVITY_FEEDING)
        
        # Only consider bottle feedings with amount and duration
        bottle_feedings = []
        for feeding in feeding_activities:
            if (feeding["data"].get("feeding_type") == "bottle" and 
                feeding["data"].get("feeding_amount", 0) > 0 and 
                feeding["data"].get("feeding_duration", 0) > 0):
                
                amount = feeding["data"]["feeding_amount"]
                duration = feeding["data"]["feeding_duration"]
                efficiency = amount / duration
                bottle_feedings.append(efficiency)
        
        if not bottle_feedings:
            return None
        
        return round(sum(bottle_feedings) / len(bottle_feedings), 1)
    
    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        feeding_activities = self._storage.get_activities_by_type(ACTIVITY_FEEDING)
        
        bottle_feedings = []
        breast_feedings = 0
        
        for feeding in feeding_activities:
            if feeding["data"].get("feeding_type") == "bottle":
                if (feeding["data"].get("feeding_amount", 0) > 0 and 
                    feeding["data"].get("feeding_duration", 0) > 0):
                    bottle_feedings.append(feeding)
            elif "breast" in feeding["data"].get("feeding_type", ""):
                breast_feedings += 1
        
        if not bottle_feedings:
            return {"status": "No bottle feeding data with duration"}
        
        total_amount = sum(f["data"]["feeding_amount"] for f in bottle_feedings)
        total_duration = sum(f["data"]["feeding_duration"] for f in bottle_feedings)
        
        return {
            "bottle_feedings_analyzed": len(bottle_feedings),
            "breast_feedings": breast_feedings,
            "total_bottle_amount_ml": total_amount,
            "total_bottle_duration_min": total_duration,
            "efficiency_trend": "Improving" if self.native_value and self.native_value > 5 else "Normal",
            "analysis_note": "Based on bottle feedings only"
        }