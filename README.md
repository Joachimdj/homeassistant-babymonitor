# Baby Monitor for Home Assistant

A comprehensive Home Assistant integration for monitoring and tracking baby care activities. Track diaper changes, feedings, sleep patterns, temperature, growth metrics, medications, and developmental milestones with detailed historical data.

## Features

### Activity Tracking
- **Diaper Changes**: Track wet, dirty, or both types of diaper changes
- **Feeding**: Monitor bottle feeding (with amounts), breastfeeding (left/right/both sides), and solid food
- **Sleep**: Track sleep start/end times with automatic duration calculation
- **Temperature**: Record baby's temperature readings
- **Weight & Height**: Track growth metrics over time
- **Medications**: Log medications with dosage information
- **Milestones**: Record developmental milestones and achievements

### Quick Action Buttons
- Instant logging buttons for common activities
- Pre-configured with reasonable defaults
- Perfect for quick logging during busy times

### Comprehensive Sensors
- **Last Activity Sensors**: Show when activities last occurred with time elapsed
- **Total Counters**: Track total counts of all activities
- **Daily/Weekly Summaries**: Get overview of recent activity patterns
- **Average Calculations**: Monitor feeding amounts and sleep durations
- **Growth Tracking**: Latest temperature, weight, and height readings

### Historical Data
- All activities stored with timestamps
- Daily and weekly summary statistics
- Trend analysis capabilities
- Data persistence across Home Assistant restarts

### Services for Automation
- Detailed services for logging all activity types
- Integration with automations and scripts
- Voice assistant compatibility
- Mobile app integration

## Installation

### Option 1: HACS Installation (Recommended)

1. **Install HACS** if you haven't already: [HACS Installation Guide](https://hacs.xyz/docs/setup/prerequisites)

2. **Add this repository to HACS:**
   - Go to HACS → Integrations
   - Click the three dots menu (⋮) → Custom repositories
   - Add repository URL: `https://github.com/Joachimdj/homeassistant-babymonitor`
   - Category: Integration
   - Click ADD

3. **Install the integration:**
   - Search for "Baby Monitor" in HACS
   - Click DOWNLOAD
   - Restart Home Assistant

4. **Add the integration:**
   - Go to Settings → Devices & Services → Add Integration
   - Search for "Baby Monitor"
   - Enter your baby's name (e.g., "Anika")

### Option 2: Manual Installation via Git

1. **Clone the repository** to your Home Assistant custom_components directory:
   ```bash
   cd /config/custom_components/
   git clone https://github.com/Joachimdj/homeassistant-babymonitor.git babymonitor
   ```

2. **Restart Home Assistant**

3. **Add the integration** via Settings → Devices & Services → Add Integration → Baby Monitor

### Option 3: Manual Installation via Download

1. **Download the repository** as a ZIP file from GitHub
2. **Extract** the ZIP file
3. **Copy** all the Python files to your Home Assistant `custom_components/babymonitor/` directory:
   ```
   /config/custom_components/babymonitor/
   ├── __init__.py
   ├── manifest.json
   ├── const.py
   ├── config_flow.py
   ├── storage.py
   ├── sensor.py
   ├── button.py
   ├── services.py
   └── services.yaml
   ```
4. **Restart Home Assistant**
5. **Add the integration** via Settings → Devices & Services

### Verification

After installation, your directory structure should look like:
```
/config/
├── custom_components/
│   └── babymonitor/
│       ├── __init__.py
│       ├── manifest.json
│       ├── const.py
│       ├── config_flow.py
│       ├── storage.py
│       ├── sensor.py
│       ├── button.py
│       ├── services.py
│       └── services.yaml
└── configuration.yaml
```

## Configuration

The integration is configured through the UI. You can add multiple babies by adding the integration multiple times with different names.

## Entities Created

For a baby named "Anika", the following entities will be created:

### Sensors
- `sensor.anika_last_diaper_change` - Last diaper change time and details
- `sensor.anika_last_feeding` - Last feeding time and details  
- `sensor.anika_last_sleep` - Last sleep session details
- `sensor.anika_total_diaper_changes` - Total diaper changes with daily breakdown
- `sensor.anika_total_feedings` - Total feedings with daily statistics
- `sensor.anika_total_sleep_sessions` - Total completed sleep sessions
- `sensor.anika_average_sleep_duration` - Average sleep duration in minutes
- `sensor.anika_average_feeding_amount` - Average feeding amount in ml
- `sensor.anika_temperature` - Current/last recorded temperature
- `sensor.anika_daily_summary` - Today's activity summary
- `sensor.anika_weekly_summary` - Last 7 days activity summary

### Buttons (Quick Actions)
- `button.anika_quick_wet_diaper` - Log wet diaper change
- `button.anika_quick_dirty_diaper` - Log dirty diaper change
- `button.anika_quick_wet_dirty_diaper` - Log wet & dirty diaper change
- `button.anika_quick_bottle_feeding` - Log bottle feeding (120ml, 15min)
- `button.anika_quick_breast_feeding_left` - Log left breast feeding (15min)
- `button.anika_quick_breast_feeding_right` - Log right breast feeding (15min)
- `button.anika_quick_breast_feeding_both` - Log both breasts feeding (25min)
- `button.anika_start_sleep` - Start sleep tracking
- `button.anika_end_sleep` - End sleep tracking with duration calculation

## Services

All services require the `baby_name` parameter to specify which baby the activity applies to.

### babymonitor.log_diaper_change
Log a diaper change with type and optional notes.
```yaml
service: babymonitor.log_diaper_change
data:
  baby_name: "Anika"
  diaper_type: "wet"  # or "dirty" or "both"
  notes: "First change of the day"
```

### babymonitor.log_feeding
Log a feeding session with details.
```yaml
service: babymonitor.log_feeding
data:
  baby_name: "Anika"
  feeding_type: "bottle"  # or "breast_left", "breast_right", "breast_both", "solid"
  feeding_amount: 120  # ml (for bottle feeding)
  feeding_duration: 15  # minutes
  notes: "Baby was very hungry"
```

### babymonitor.log_sleep
Start or end sleep tracking.
```yaml
# Start sleep
service: babymonitor.log_sleep
data:
  baby_name: "Anika"
  sleep_type: "start"
  notes: "Put down for nap"

# End sleep (automatically calculates duration)
service: babymonitor.log_sleep
data:
  baby_name: "Anika"
  sleep_type: "end"
  notes: "Woke up refreshed"
```

### babymonitor.log_temperature
Record baby's temperature.
```yaml
service: babymonitor.log_temperature
data:
  baby_name: "Anika"
  temperature: 36.5
  notes: "Measured after bath"
```

### babymonitor.log_weight
Record baby's weight.
```yaml
service: babymonitor.log_weight
data:
  baby_name: "Anika"
  weight: 4.2  # kg
  notes: "Doctor visit checkup"
```

### babymonitor.log_height
Record baby's height.
```yaml
service: babymonitor.log_height
data:
  baby_name: "Anika"
  height: 52.0  # cm
  notes: "3 month checkup"
```

### babymonitor.log_medication
Log medication administration.
```yaml
service: babymonitor.log_medication
data:
  baby_name: "Anika"
  medication_name: "Paracetamol"
  medication_dosage: "2.5ml"
  notes: "For fever"
```

### babymonitor.log_milestone
Record developmental milestones.
```yaml
service: babymonitor.log_milestone
data:
  baby_name: "Anika"
  milestone_name: "First smile"
  notes: "Big happy smile during play time"
```

## Example Automations

### Voice Assistant Integration
```yaml
# Automation to log diaper change via voice
automation:
  - alias: "Log Diaper Change via Voice"
    trigger:
      - platform: conversation
        command: "Log wet diaper for Anika"
    action:
      - service: babymonitor.log_diaper_change
        data:
          baby_name: "Anika"
          diaper_type: "wet"
          notes: "Logged via voice command"
```

### Mobile Notification for Feeding Reminders
```yaml
# Send reminder if no feeding in 3 hours
automation:
  - alias: "Feeding Reminder"
    trigger:
      - platform: template
        value_template: >
          {{ (as_timestamp(now()) - as_timestamp(states('sensor.anika_last_feeding'))) > 10800 }}
    condition:
      - condition: time
        after: "06:00:00"
        before: "22:00:00"
    action:
      - service: notify.mobile_app_your_phone
        data:
          message: "It's been 3 hours since Anika's last feeding"
          title: "Feeding Reminder"
```

### Daily Summary Notification
```yaml
# Send daily summary at bedtime
automation:
  - alias: "Daily Baby Summary"
    trigger:
      - platform: time
        at: "20:00:00"
    action:
      - service: notify.mobile_app_your_phone
        data:
          message: >
            Today's summary for Anika:
            {{ state_attr('sensor.anika_daily_summary', 'diaper_changes') }} diaper changes
            {{ state_attr('sensor.anika_daily_summary', 'feedings') }} feedings
            {{ state_attr('sensor.anika_daily_summary', 'total_sleep_formatted') }} total sleep
          title: "Daily Baby Report"
```

### Sleep Duration Alert
```yaml
# Alert if sleep session is very short
automation:
  - alias: "Short Sleep Alert"
    trigger:
      - platform: state
        entity_id: sensor.anika_last_sleep
    condition:
      - condition: template
        value_template: >
          {{ state_attr('sensor.anika_last_sleep', 'duration_minutes') | int < 30 }}
    action:
      - service: notify.mobile_app_your_phone
        data:
          message: "Anika's last sleep was only {{ state_attr('sensor.anika_last_sleep', 'duration_formatted') }}"
          title: "Short Sleep Alert"
```

## Data Storage

All activity data is stored locally in Home Assistant's storage directory. Data includes:
- Timestamps for all activities
- Activity-specific details (amounts, durations, types)
- Custom notes for each entry
- Calculated statistics and averages

The data persists across Home Assistant restarts and can be used with the built-in history and logbook components for long-term trend analysis.

## Lovelace Dashboard Examples

### Quick Actions Card
```yaml
type: entities
title: Anika - Quick Actions
entities:
  - button.anika_quick_wet_diaper
  - button.anika_quick_dirty_diaper  
  - button.anika_quick_bottle_feeding
  - button.anika_quick_breast_feeding_both
  - button.anika_start_sleep
  - button.anika_end_sleep
```

### Summary Card
```yaml
type: entities
title: Anika - Current Status
entities:
  - sensor.anika_last_diaper_change
  - sensor.anika_last_feeding
  - sensor.anika_last_sleep
  - sensor.anika_temperature
  - sensor.anika_daily_summary
```

### Statistics Card
```yaml
type: statistics-graph
title: Anika - Feeding Amounts
entities:
  - sensor.anika_average_feeding_amount
period: day
days_to_show: 7
```

## Support

For issues, feature requests, or questions, please visit the GitHub repository.

## License

This project is licensed under the MIT License.