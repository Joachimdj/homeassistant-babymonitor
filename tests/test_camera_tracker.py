"""Tests for camera crying tracker."""
from __future__ import annotations

import pytest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch, call

from homeassistant.const import STATE_ON, STATE_OFF
from homeassistant.core import Event

from custom_components.babymonitor import CameraCryingTracker
from custom_components.babymonitor.const import ACTIVITY_CRYING, CRYING_MODERATE


class TestCameraCryingTracker:
    """Test CameraCryingTracker class."""

    @pytest.fixture
    def mock_storage(self):
        """Create mock storage."""
        storage = MagicMock()
        storage.async_add_activity = AsyncMock()
        return storage

    @pytest.fixture
    def tracker(self, mock_hass, mock_storage):
        """Create a tracker instance."""
        return CameraCryingTracker(
            mock_hass,
            "TestBaby",
            mock_storage,
            "binary_sensor.test_camera_crying"
        )

    @pytest.mark.asyncio
    async def test_initialization(self, tracker):
        """Test tracker initialization."""
        assert tracker._baby_name == "TestBaby"
        assert tracker._camera_entity == "binary_sensor.test_camera_crying"
        assert tracker._crying_start_time is None
        assert tracker._unsub is None

    @pytest.mark.asyncio
    async def test_async_start(self, tracker):
        """Test starting the tracker."""
        with patch("custom_components.babymonitor.async_track_state_change_event") as mock_track:
            mock_track.return_value = MagicMock()
            
            await tracker.async_start()
            
            assert tracker._unsub is not None
            mock_track.assert_called_once()
            call_args = mock_track.call_args
            assert call_args[0][1] == ["binary_sensor.test_camera_crying"]

    @pytest.mark.asyncio
    async def test_crying_start_detection(self, tracker, mock_storage):
        """Test detection of crying start."""
        # Create mock event for state change to ON
        event = MagicMock(spec=Event)
        event.data = {
            "new_state": MagicMock(state=STATE_ON),
            "old_state": MagicMock(state=STATE_OFF)
        }
        
        await tracker._handle_camera_state_change(event)
        
        # Should log crying start
        assert tracker._crying_start_time is not None
        mock_storage.async_add_activity.assert_called_once()
        
        call_args = mock_storage.async_add_activity.call_args
        assert call_args[0][0] == ACTIVITY_CRYING
        assert call_args[0][1]["crying_intensity"] == CRYING_MODERATE
        assert call_args[0][1]["duration"] == 0
        assert "Auto-detected" in call_args[0][1]["notes"]

    @pytest.mark.asyncio
    async def test_crying_end_detection(self, tracker, mock_storage):
        """Test detection of crying end with duration calculation."""
        # First, simulate crying start
        start_event = MagicMock(spec=Event)
        start_event.data = {
            "new_state": MagicMock(state=STATE_ON),
            "old_state": MagicMock(state=STATE_OFF)
        }
        await tracker._handle_camera_state_change(start_event)
        
        # Reset mock to clear start call
        mock_storage.async_add_activity.reset_mock()
        
        # Now simulate crying end
        end_event = MagicMock(spec=Event)
        end_event.data = {
            "new_state": MagicMock(state=STATE_OFF),
            "old_state": MagicMock(state=STATE_ON)
        }
        await tracker._handle_camera_state_change(end_event)
        
        # Should log crying end with duration
        mock_storage.async_add_activity.assert_called_once()
        
        call_args = mock_storage.async_add_activity.call_args
        assert call_args[0][0] == ACTIVITY_CRYING
        assert call_args[0][1]["crying_intensity"] == CRYING_MODERATE
        assert call_args[0][1]["duration"] >= 0
        assert "Auto-detected" in call_args[0][1]["notes"]
        
        # Start time should be cleared
        assert tracker._crying_start_time is None

    @pytest.mark.asyncio
    async def test_no_state_change_ignored(self, tracker, mock_storage):
        """Test that non-state-changes are ignored."""
        event = MagicMock(spec=Event)
        event.data = {
            "new_state": MagicMock(state=STATE_ON),
            "old_state": MagicMock(state=STATE_ON)  # Same state
        }
        
        await tracker._handle_camera_state_change(event)
        
        # Should not log anything
        mock_storage.async_add_activity.assert_not_called()

    @pytest.mark.asyncio
    async def test_none_state_ignored(self, tracker, mock_storage):
        """Test that None states are ignored."""
        event = MagicMock(spec=Event)
        event.data = {
            "new_state": None,
            "old_state": MagicMock(state=STATE_OFF)
        }
        
        await tracker._handle_camera_state_change(event)
        
        # Should not log anything
        mock_storage.async_add_activity.assert_not_called()

    @pytest.mark.asyncio
    async def test_stop_tracker(self, tracker):
        """Test stopping the tracker."""
        # Start tracker first
        with patch("custom_components.babymonitor.async_track_state_change_event") as mock_track:
            mock_unsub = MagicMock()
            mock_track.return_value = mock_unsub
            
            await tracker.async_start()
            
            # Now stop it
            tracker.stop()
            
            mock_unsub.assert_called_once()
            assert tracker._unsub is None

    @pytest.mark.asyncio
    async def test_crying_end_without_start(self, tracker, mock_storage):
        """Test that crying end without start is handled gracefully."""
        # Simulate crying end without a start
        event = MagicMock(spec=Event)
        event.data = {
            "new_state": MagicMock(state=STATE_OFF),
            "old_state": MagicMock(state=STATE_ON)
        }
        
        # Should not raise an exception
        await tracker._handle_camera_state_change(event)
        
        # Should not log anything since there's no start time
        mock_storage.async_add_activity.assert_not_called()

    @pytest.mark.asyncio
    async def test_duration_calculation_accuracy(self, tracker, mock_storage):
        """Test that duration is calculated correctly."""
        import time
        
        # Start crying
        start_event = MagicMock(spec=Event)
        start_event.data = {
            "new_state": MagicMock(state=STATE_ON),
            "old_state": MagicMock(state=STATE_OFF)
        }
        await tracker._handle_camera_state_change(start_event)
        
        # Wait a bit
        time.sleep(0.1)
        
        # Reset mock
        mock_storage.async_add_activity.reset_mock()
        
        # End crying
        end_event = MagicMock(spec=Event)
        end_event.data = {
            "new_state": MagicMock(state=STATE_OFF),
            "old_state": MagicMock(state=STATE_ON)
        }
        await tracker._handle_camera_state_change(end_event)
        
        # Check duration is reasonable (should be 0 minutes for such short duration)
        call_args = mock_storage.async_add_activity.call_args
        duration = call_args[0][1]["duration"]
        assert duration >= 0
        assert duration < 5  # Should be less than 5 minutes
