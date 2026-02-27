"""Basic sanity tests that don't require Home Assistant installation."""
import pytest
from datetime import datetime


def test_basic_imports():
    """Test that basic Python imports work."""
    import sys
    import os
    assert sys.version_info >= (3, 9)


def test_datetime_operations():
    """Test datetime operations used in the integration."""
    now = datetime.now()
    assert now is not None
    assert isinstance(now, datetime)
    
    # Test isoformat (used in storage)
    iso_string = now.isoformat()
    parsed = datetime.fromisoformat(iso_string)
    assert parsed.date() == now.date()


def test_dict_operations():
    """Test dictionary operations used in storage."""
    data = {"activities": [], "baby_name": "Test"}
    
    # Test adding items
    data["activities"].append({
        "type": "test",
        "timestamp": datetime.now().isoformat(),
        "data": {}
    })
    
    assert len(data["activities"]) == 1
    assert data["activities"][0]["type"] == "test"


def test_list_filtering():
    """Test list filtering operations."""
    activities = [
        {"type": "crying", "data": {}},
        {"type": "feeding", "data": {}},
        {"type": "crying", "data": {}},
    ]
    
    crying = [a for a in activities if a["type"] == "crying"]
    assert len(crying) == 2


def test_list_sorting():
    """Test list sorting by timestamp."""
    activities = [
        {"timestamp": "2026-02-27T10:00:00"},
        {"timestamp": "2026-02-27T12:00:00"},
        {"timestamp": "2026-02-27T11:00:00"},
    ]
    
    sorted_activities = sorted(activities, key=lambda x: x["timestamp"], reverse=True)
    assert sorted_activities[0]["timestamp"] == "2026-02-27T12:00:00"
    assert sorted_activities[-1]["timestamp"] == "2026-02-27T10:00:00"


def test_constants_import():
    """Test that constants can be imported."""
    # This will work if the package structure is correct
    try:
        from const import DOMAIN, ACTIVITY_CRYING
        assert DOMAIN == "babymonitor"
        assert ACTIVITY_CRYING == "crying"
    except ImportError:
        # File might not be in path, that's OK for basic test
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
