"""Tests for sensor.py"""
from __future__ import annotations

import pytest
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

from homeassistant.components.sensor import SensorStateClass

from custom_components.babymonitor.sensor import (
    TotalCryingEpisodesToday,
    CurrentTemperatureSensor,
    LastDiaperChangeSensor,
)
from custom_components.babymonitor.const import (
    ACTIVITY_CRYING,
    ACTIVITY_TEMPERATURE,
    ACTIVITY_DIAPER_CHANGE,
    CRYING_MODERATE,
    CRYING_INTENSE,
)


class TestTotalCryingEpisodesToday:
    """Test TotalCryingEpisodesToday sensor."""

    @pytest.fixture
    def mock_storage(self):
        """Create mock storage."""
        storage = MagicMock()
        return storage

    @pytest.fixture
    def sensor(self, mock_storage):
        """Create sensor instance."""
        return TotalCryingEpisodesToday(
            "TestBaby",
            mock_storage,
            {}
        )

    def test_sensor_properties(self, sensor):
        """Test sensor basic properties."""
        assert sensor._sensor_name == "Total Crying Episodes"
        assert sensor._sensor_id == "total_crying_episodes"
        assert sensor._attr_state_class == SensorStateClass.TOTAL_INCREASING
        assert sensor._attr_icon == "mdi:emoticon-sad-outline"

    def test_native_value_no_crying(self, sensor, mock_storage):
        """Test native value when no crying episodes."""
        mock_storage.get_daily_activities.return_value = []
        
        value = sensor.native_value
        
        assert value == 0

    def test_native_value_with_crying(self, sensor, mock_storage):
        """Test native value with crying episodes."""
        today = datetime.now()
        mock_storage.get_daily_activities.return_value = [
            {
                "type": ACTIVITY_CRYING,
                "timestamp": today.isoformat(),
                "data": {"crying_intensity": CRYING_MODERATE, "duration": 5}
            },
            {
                "type": ACTIVITY_CRYING,
                "timestamp": today.isoformat(),
                "data": {"crying_intensity": CRYING_INTENSE, "duration": 10}
            },
            {
                "type": ACTIVITY_DIAPER_CHANGE,  # Different activity type
                "timestamp": today.isoformat(),
                "data": {}
            },
        ]
        
        value = sensor.native_value
        
        # Should only count crying activities
        assert value == 2

    def test_extra_state_attributes(self, sensor, mock_storage):
        """Test extra state attributes calculation."""
        today = datetime.now()
        mock_storage.get_daily_activities.return_value = [
            {
                "type": ACTIVITY_CRYING,
                "timestamp": (today - timedelta(hours=2)).isoformat(),
                "data": {"crying_intensity": CRYING_MODERATE, "duration": 10}
            },
            {
                "type": ACTIVITY_CRYING,
                "timestamp": (today - timedelta(hours=1)).isoformat(),
                "data": {"crying_intensity": CRYING_INTENSE, "duration": 20}
            },
        ]
        
        attrs = sensor.extra_state_attributes
        
        assert "total_duration_minutes" in attrs
        assert attrs["total_duration_minutes"] == 30
        
        assert "average_episode_duration" in attrs
        assert attrs["average_episode_duration"] == 15
        
        assert "intensity_breakdown" in attrs
        assert attrs["intensity_breakdown"]["moderate"] == 1
        assert attrs["intensity_breakdown"]["intense"] == 1
        
        assert "last_episode" in attrs


class TestCurrentTemperatureSensor:
    """Test CurrentTemperatureSensor."""

    @pytest.fixture
    def mock_storage(self):
        """Create mock storage."""
        storage = MagicMock()
        return storage

    @pytest.fixture
    def sensor(self, mock_storage):
        """Create sensor instance."""
        return CurrentTemperatureSensor(
            "TestBaby",
            mock_storage,
            {}
        )

    def test_sensor_properties(self, sensor):
        """Test sensor basic properties."""
        assert sensor._sensor_name == "Current Temperature"
        assert sensor._sensor_id == "current_temperature"
        assert sensor._attr_state_class == SensorStateClass.MEASUREMENT
        assert sensor._attr_native_unit_of_measurement == "°C"

    def test_native_value_no_temperature(self, sensor, mock_storage):
        """Test native value when no temperature recorded."""
        mock_storage.get_activities_by_type.return_value = []
        
        value = sensor.native_value
        
        assert value is None

    def test_native_value_with_temperature(self, sensor, mock_storage):
        """Test native value with temperature."""
        mock_storage.get_activities_by_type.return_value = [
            {
                "type": ACTIVITY_TEMPERATURE,
                "timestamp": datetime.now().isoformat(),
                "data": {"temperature": 37.5}
            }
        ]
        
        value = sensor.native_value
        
        assert value == 37.5

    def test_gets_latest_temperature(self, sensor, mock_storage):
        """Test that it returns the most recent temperature."""
        today = datetime.now()
        mock_storage.get_activities_by_type.return_value = [
            {
                "type": ACTIVITY_TEMPERATURE,
                "timestamp": today.isoformat(),
                "data": {"temperature": 37.5}
            },
            {
                "type": ACTIVITY_TEMPERATURE,
                "timestamp": (today - timedelta(hours=1)).isoformat(),
                "data": {"temperature": 37.0}
            },
        ]
        
        value = sensor.native_value
        
        # Should return the first one (most recent)
        assert value == 37.5


class TestLastDiaperChangeSensor:
    """Test LastDiaperChangeSensor."""

    @pytest.fixture
    def mock_storage(self):
        """Create mock storage."""
        storage = MagicMock()
        return storage

    @pytest.fixture
    def sensor(self, mock_storage):
        """Create sensor instance."""
        return LastDiaperChangeSensor(
            "TestBaby",
            mock_storage,
            {}
        )

    def test_sensor_properties(self, sensor):
        """Test sensor basic properties."""
        assert sensor._sensor_name == "Last Diaper Change"
        assert sensor._sensor_id == "last_diaper_change"

    def test_native_value_no_diaper_change(self, sensor, mock_storage):
        """Test when no diaper changes."""
        mock_storage.get_activities_by_type.return_value = []
        
        value = sensor.native_value
        
        assert value == "Never"

    def test_native_value_with_diaper_change(self, sensor, mock_storage):
        """Test with recent diaper change."""
        recent_time = datetime.now() - timedelta(minutes=30)
        mock_storage.get_activities_by_type.return_value = [
            {
                "type": ACTIVITY_DIAPER_CHANGE,
                "timestamp": recent_time.isoformat(),
                "data": {"diaper_type": "wet"}
            }
        ]
        
        value = sensor.native_value
        
        # Should return a human-readable time difference
        assert "ago" in value or "minute" in value


class TestSensorIntegration:
    """Integration tests for sensors."""

    @pytest.mark.asyncio
    async def test_sensors_update_after_activity(self):
        """Test that sensors reflect new activities."""
        from custom_components.babymonitor.storage import BabyMonitorStorage
        
        with patch("homeassistant.helpers.storage.Store.async_save") as mock_save, \
             patch("homeassistant.helpers.storage.Store.async_load") as mock_load:
            
            mock_load.return_value = None
            mock_hass = MagicMock()
            
            # Create storage and add activity
            storage = BabyMonitorStorage(mock_hass, "TestBaby")
            await storage.async_load()
            
            # Add crying episode
            await storage.async_add_activity(
                ACTIVITY_CRYING,
                {"crying_intensity": CRYING_MODERATE, "duration": 5}
            )
            
            # Create sensor
            sensor = TotalCryingEpisodesToday("TestBaby", storage, {})
            
            # Sensor should reflect the added activity
            assert sensor.native_value == 1
