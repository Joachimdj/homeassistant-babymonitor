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
ACTIVITY_BATH = "bath"
ACTIVITY_TUMMY_TIME = "tummy_time"
ACTIVITY_CRYING = "crying"
ACTIVITY_MOOD = "mood"
ACTIVITY_ENVIRONMENTAL = "environmental"
ACTIVITY_CAREGIVER = "caregiver"

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
SERVICE_LOG_BATH = "log_bath"
SERVICE_LOG_TUMMY_TIME = "log_tummy_time"
SERVICE_LOG_CRYING = "log_crying"
SERVICE_LOG_MOOD = "log_mood"
SERVICE_LOG_ENVIRONMENTAL = "log_environmental"
SERVICE_LOG_CAREGIVER = "log_caregiver"

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
ATTR_DURATION = "duration"
ATTR_CRYING_INTENSITY = "crying_intensity"
ATTR_MOOD_TYPE = "mood_type"
ATTR_ROOM_TEMPERATURE = "room_temperature"
ATTR_HUMIDITY = "humidity"
ATTR_CAREGIVER_NAME = "caregiver_name"
ATTR_BATH_TYPE = "bath_type"

# Mood types
MOOD_HAPPY = "happy"
MOOD_FUSSY = "fussy"
MOOD_CALM = "calm"
MOOD_SLEEPY = "sleepy"
MOOD_ALERT = "alert"

# Crying intensity levels
CRYING_LIGHT = "light"
CRYING_MODERATE = "moderate"
CRYING_INTENSE = "intense"

# Bath types
BATH_FULL = "full_bath"
BATH_SPONGE = "sponge_bath"
BATH_HAIR_WASH = "hair_wash"

# Configuration options
CONF_MIN_DIAPERS_PER_DAY = "min_diapers_per_day"
CONF_MIN_WET_DIAPERS_PER_DAY = "min_wet_diapers_per_day"
CONF_MIN_FEEDINGS_PER_DAY = "min_feedings_per_day"
CONF_MIN_SLEEP_HOURS_PER_DAY = "min_sleep_hours_per_day"
CONF_TARGET_TUMMY_TIME_MINUTES = "target_tummy_time_minutes"
CONF_FEEDING_REMINDER_HOURS = "feeding_reminder_hours"
CONF_DIAPER_REMINDER_HOURS = "diaper_reminder_hours"
CONF_CAMERA_CRYING_ENTITY = "camera_crying_entity"
CONF_CAMERA_AUTO_TRACKING = "camera_auto_tracking"

# Default values for configuration options
DEFAULT_MIN_DIAPERS_PER_DAY = 6
DEFAULT_MIN_WET_DIAPERS_PER_DAY = 4
DEFAULT_MIN_FEEDINGS_PER_DAY = 6
DEFAULT_MIN_SLEEP_HOURS_PER_DAY = 12
DEFAULT_TARGET_TUMMY_TIME_MINUTES = 15
DEFAULT_FEEDING_REMINDER_HOURS = 3
DEFAULT_DIAPER_REMINDER_HOURS = 4

# Camera tracking
CAMERA_TRACKING_HELPER_PREFIX = "baby_crying_tracker"