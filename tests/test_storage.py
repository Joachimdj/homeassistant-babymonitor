"""Tests for storage.py"""
from __future__ import annotations

import pytest
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

from custom_components.babymonitor.storage import BabyMonitorStorage
from custom_components.babymonitor.const import (
    ACTIVITY_DIAPER_CHANGE,
    ACTIVITY_FEEDING,
    ACTIVITY_CRYING,
    ACTIVITY_TEMPERATURE,
)


class TestBabyMonitorStorage:
    """Test BabyMonitorStorage class."""

    @pytest.mark.asyncio
    async def test_initialization(self, mock_hass, mock_storage_load):
        """Test storage initialization."""
        storage = BabyMonitorStorage(mock_hass, "TestBaby")
        
        assert storage.baby_name == "TestBaby"
        assert storage._hass == mock_hass
        assert storage._data is not None

    @pytest.mark.asyncio
    async def test_async_load_new_storage(self, mock_hass, mock_storage_load):
        """Test loading when no existing data."""
        mock_storage_load.return_value = None
        
        storage = BabyMonitorStorage(mock_hass, "TestBaby")
        await storage.async_load()
        
        assert storage._data["baby_name"] == "TestBaby"
        assert storage._data["activities"] == []

    @pytest.mark.asyncio
    async def test_async_load_existing_storage(self, mock_hass, mock_storage_load):
        """Test loading existing data."""
        existing_data = {
            "baby_name": "TestBaby",
            "activities": [
                {
                    "type": ACTIVITY_DIAPER_CHANGE,
                    "timestamp": "2026-01-01T10:00:00",
                    "data": {"diaper_type": "wet"}
                }
            ]
        }
        mock_storage_load.return_value = existing_data
        
        storage = BabyMonitorStorage(mock_hass, "TestBaby")
        await storage.async_load()
        
        assert len(storage._data["activities"]) == 1
        assert storage._data["activities"][0]["type"] == ACTIVITY_DIAPER_CHANGE

    @pytest.mark.asyncio
    async def test_async_add_activity(self, mock_hass, mock_storage_load, mock_storage_save):
        """Test adding an activity."""
        mock_storage_load.return_value = None
        
        storage = BabyMonitorStorage(mock_hass, "TestBaby")
        await storage.async_load()
        
        await storage.async_add_activity(
            ACTIVITY_FEEDING,
            {"feeding_type": "bottle", "amount": 120}
        )
        
        assert len(storage._data["activities"]) == 1
        assert storage._data["activities"][0]["type"] == ACTIVITY_FEEDING
        assert storage._data["activities"][0]["data"]["amount"] == 120
        assert "timestamp" in storage._data["activities"][0]
        
        mock_storage_save.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_activities_by_type(self, mock_hass, mock_storage_load):
        """Test filtering activities by type."""
        existing_data = {
            "baby_name": "TestBaby",
            "activities": [
                {
                    "type": ACTIVITY_DIAPER_CHANGE,
                    "timestamp": "2026-02-27T10:00:00",
                    "data": {"diaper_type": "wet"}
                },
                {
                    "type": ACTIVITY_FEEDING,
                    "timestamp": "2026-02-27T11:00:00",
                    "data": {"feeding_type": "bottle"}
                },
                {
                    "type": ACTIVITY_DIAPER_CHANGE,
                    "timestamp": "2026-02-27T12:00:00",
                    "data": {"diaper_type": "dirty"}
                },
            ]
        }
        mock_storage_load.return_value = existing_data
        
        storage = BabyMonitorStorage(mock_hass, "TestBaby")
        await storage.async_load()
        
        diaper_activities = storage.get_activities_by_type(ACTIVITY_DIAPER_CHANGE)
        assert len(diaper_activities) == 2
        assert all(a["type"] == ACTIVITY_DIAPER_CHANGE for a in diaper_activities)

    @pytest.mark.asyncio
    async def test_get_activities_by_type_with_limit(self, mock_hass, mock_storage_load):
        """Test getting limited activities."""
        existing_data = {
            "baby_name": "TestBaby",
            "activities": [
                {
                    "type": ACTIVITY_CRYING,
                    "timestamp": f"2026-02-27T{10+i}:00:00",
                    "data": {"crying_intensity": "moderate"}
                }
                for i in range(5)
            ]
        }
        mock_storage_load.return_value = existing_data
        
        storage = BabyMonitorStorage(mock_hass, "TestBaby")
        await storage.async_load()
        
        activities = storage.get_activities_by_type(ACTIVITY_CRYING, limit=2)
        assert len(activities) == 2

    @pytest.mark.asyncio
    async def test_get_daily_activities_today(self, mock_hass, mock_storage_load):
        """Test getting today's activities only."""
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        
        existing_data = {
            "baby_name": "TestBaby",
            "activities": [
                {
                    "type": ACTIVITY_DIAPER_CHANGE,
                    "timestamp": today.isoformat(),
                    "data": {"diaper_type": "wet"}
                },
                {
                    "type": ACTIVITY_FEEDING,
                    "timestamp": yesterday.isoformat(),
                    "data": {"feeding_type": "bottle"}
                },
                {
                    "type": ACTIVITY_TEMPERATURE,
                    "timestamp": today.isoformat(),
                    "data": {"temperature": 37.0}
                },
            ]
        }
        mock_storage_load.return_value = existing_data
        
        storage = BabyMonitorStorage(mock_hass, "TestBaby")
        await storage.async_load()
        
        daily_activities = storage.get_daily_activities()
        
        # Should only return today's activities
        assert len(daily_activities) == 2
        assert all(
            datetime.fromisoformat(a["timestamp"]).date() == today.date()
            for a in daily_activities
        )

    @pytest.mark.asyncio
    async def test_get_all_activities(self, mock_hass, mock_storage_load):
        """Test getting all activities."""
        existing_data = {
            "baby_name": "TestBaby",
            "activities": [
                {
                    "type": ACTIVITY_DIAPER_CHANGE,
                    "timestamp": "2026-02-27T10:00:00",
                    "data": {}
                },
                {
                    "type": ACTIVITY_FEEDING,
                    "timestamp": "2026-02-27T11:00:00",
                    "data": {}
                },
            ]
        }
        mock_storage_load.return_value = existing_data
        
        storage = BabyMonitorStorage(mock_hass, "TestBaby")
        await storage.async_load()
        
        all_activities = storage.get_all_activities()
        assert len(all_activities) == 2

    @pytest.mark.asyncio
    async def test_activity_ordering(self, mock_hass, mock_storage_load):
        """Test that activities are ordered newest first."""
        existing_data = {
            "baby_name": "TestBaby",
            "activities": [
                {
                    "type": ACTIVITY_CRYING,
                    "timestamp": "2026-02-27T10:00:00",
                    "data": {}
                },
                {
                    "type": ACTIVITY_CRYING,
                    "timestamp": "2026-02-27T12:00:00",
                    "data": {}
                },
                {
                    "type": ACTIVITY_CRYING,
                    "timestamp": "2026-02-27T11:00:00",
                    "data": {}
                },
            ]
        }
        mock_storage_load.return_value = existing_data
        
        storage = BabyMonitorStorage(mock_hass, "TestBaby")
        await storage.async_load()
        
        activities = storage.get_activities_by_type(ACTIVITY_CRYING)
        
        # Should be in descending order (newest first)
        timestamps = [a["timestamp"] for a in activities]
        assert timestamps == sorted(timestamps, reverse=True)
