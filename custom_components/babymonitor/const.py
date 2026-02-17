"""Constants for the Baby Monitor integration."""
from __future__ import annotations

from typing import Final

DOMAIN: Final = "babymonitor"
DEFAULT_NAME = "Baby Monitor"

# Activity types
ACTIVITY_DIAPER_CHANGE = "diaper_change"
ACTIVITY_FEEDING = "feeding"
ACTIVITY_SLEEP = "sleep"
ACTIVITY_TEMPERATURE = "temperature"
ACTIVITY_WEIGHT = "weight"
ACTIVITY_HEIGHT = "height"
ACTIVITY_MEDICATION = "medication"
ACTIVITY_MILESTONE = "milestone"

# Diaper change types
DIAPER_WET = "wet"
DIAPER_DIRTY = "dirty"
DIAPER_BOTH = "both"

# Feeding types
FEEDING_BOTTLE = "bottle"
FEEDING_BREAST_LEFT = "breast_left"
FEEDING_BREAST_RIGHT = "breast_right"
FEEDING_BREAST_BOTH = "breast_both"
FEEDING_SOLID = "solid"

# Sleep types
SLEEP_START = "start"
SLEEP_END = "end"

# Services
SERVICE_LOG_DIAPER_CHANGE = "log_diaper_change"
SERVICE_LOG_FEEDING = "log_feeding"
SERVICE_LOG_SLEEP = "log_sleep"
SERVICE_LOG_TEMPERATURE = "log_temperature"
SERVICE_LOG_WEIGHT = "log_weight"
SERVICE_LOG_HEIGHT = "log_height"
SERVICE_LOG_MEDICATION = "log_medication"
SERVICE_LOG_MILESTONE = "log_milestone"

# Attributes
ATTR_BABY_NAME = "baby_name"
ATTR_DIAPER_TYPE = "diaper_type"
ATTR_FEEDING_TYPE = "feeding_type"
ATTR_FEEDING_AMOUNT = "feeding_amount"
ATTR_FEEDING_DURATION = "feeding_duration"
ATTR_SLEEP_TYPE = "sleep_type"
ATTR_TEMPERATURE = "temperature"
ATTR_WEIGHT = "weight"
ATTR_HEIGHT = "height"
ATTR_MEDICATION_NAME = "medication_name"
ATTR_MEDICATION_DOSAGE = "medication_dosage"
ATTR_MILESTONE_NAME = "milestone_name"
ATTR_NOTES = "notes"
ATTR_TIMESTAMP = "timestamp"