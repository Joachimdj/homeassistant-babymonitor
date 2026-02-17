"""Data storage helper for Baby Monitor integration."""
from __future__ import annotations

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

STORAGE_VERSION = 1


class BabyMonitorStorage:
    """Storage helper for baby monitor data."""
    
    def __init__(self, hass: HomeAssistant, baby_name: str) -> None:
        """Initialize storage."""
        self.hass = hass
        self.baby_name = baby_name
        self._store = Store(
            hass, 
            STORAGE_VERSION, 
            f"{DOMAIN}_{baby_name.lower().replace(' ', '_')}_data"
        )
        self._data: dict[str, Any] = {}
    
    async def async_load(self) -> None:
        """Load data from storage."""
        data = await self._store.async_load()
        if data is None:
            self._data = {
                "activities": [],
                "stats": {
                    "total_diaper_changes": 0,
                    "total_feedings": 0,
                    "total_sleep_sessions": 0,
                    "last_diaper_change": None,
                    "last_feeding": None,
                    "last_sleep": None,
                    "average_sleep_duration": 0,
                    "average_feeding_amount": 0,
                }
            }
        else:
            self._data = data
    
    async def async_save(self) -> None:
        """Save data to storage."""
        await self._store.async_save(self._data)
    
    async def async_add_activity(self, activity_type: str, data: dict[str, Any]) -> None:
        """Add a new activity."""
        activity = {
            "type": activity_type,
            "timestamp": datetime.now().isoformat(),
            "data": data
        }
        
        self._data["activities"].append(activity)
        await self._update_stats(activity_type, data)
        await self.async_save()
    
    async def _update_stats(self, activity_type: str, data: dict[str, Any]) -> None:
        """Update statistics."""
        stats = self._data["stats"]
        
        if activity_type == "diaper_change":
            stats["total_diaper_changes"] += 1
            stats["last_diaper_change"] = datetime.now().isoformat()
        
        elif activity_type == "feeding":
            stats["total_feedings"] += 1
            stats["last_feeding"] = datetime.now().isoformat()
            
            # Update average feeding amount
            total_amount = 0
            feeding_count = 0
            for activity in self._data["activities"]:
                if (activity["type"] == "feeding" and 
                    "feeding_amount" in activity["data"]):
                    total_amount += activity["data"]["feeding_amount"]
                    feeding_count += 1
            
            if feeding_count > 0:
                stats["average_feeding_amount"] = total_amount / feeding_count
        
        elif activity_type == "sleep":
            if data.get("sleep_type") == "end":
                stats["total_sleep_sessions"] += 1
                stats["last_sleep"] = datetime.now().isoformat()
                
                # Calculate average sleep duration
                sleep_durations = []
                for activity in self._data["activities"]:
                    if (activity["type"] == "sleep" and 
                        "duration" in activity["data"]):
                        sleep_durations.append(activity["data"]["duration"])
                
                if sleep_durations:
                    stats["average_sleep_duration"] = sum(sleep_durations) / len(sleep_durations)
    
    def get_activities_by_type(self, activity_type: str, limit: int = None) -> list[dict]:
        """Get activities filtered by type."""
        activities = [
            activity for activity in self._data["activities"] 
            if activity["type"] == activity_type
        ]
        
        # Sort by timestamp (newest first)
        activities.sort(key=lambda x: x["timestamp"], reverse=True)
        
        if limit:
            activities = activities[:limit]
        
        return activities
        
        return activities
    
    def get_activities_by_date_range(self, start_date: str, end_date: str) -> list[dict]:
        """Get activities within a date range."""
        return [
            activity for activity in self._data["activities"]
            if start_date <= activity["timestamp"] <= end_date
        ]
    
    def get_stats(self) -> dict[str, Any]:
        """Get current statistics."""
        return self._data["stats"].copy()
    
    def get_recent_activities(self, limit: int = 10) -> list[dict]:
        """Get recent activities."""
        activities = self._data["activities"].copy()
        activities.sort(key=lambda x: x["timestamp"], reverse=True)
        return activities[:limit]
    
    def get_activities_since_days(self, days: int) -> list[dict]:
        """Get activities from the last N days."""
        cutoff_date = datetime.now() - timedelta(days=days)
        return [
            activity for activity in self._data["activities"]
            if datetime.fromisoformat(activity["timestamp"]) >= cutoff_date
        ]