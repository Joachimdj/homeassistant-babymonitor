"""Fixtures for Baby Monitor tests."""
from __future__ import annotations

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from homeassistant.core import HomeAssistant


@pytest.fixture
def mock_hass():
    """Create a mock Home Assistant instance."""
    hass = MagicMock(spec=HomeAssistant)
    hass.data = {}
    hass.states = MagicMock()
    hass.config_entries = MagicMock()
    hass.async_create_task = lambda coro: coro
    return hass


@pytest.fixture
def mock_storage_save():
    """Mock the storage save method."""
    with patch("homeassistant.helpers.storage.Store.async_save") as mock:
        yield mock


@pytest.fixture
def mock_storage_load():
    """Mock the storage load method."""
    with patch("homeassistant.helpers.storage.Store.async_load") as mock:
        mock.return_value = None
        yield mock
