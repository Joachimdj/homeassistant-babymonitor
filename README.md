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

1. Copy the `custom_components/babymonitor` folder to your Home Assistant `custom_components` directory
2. Restart Home Assistant
3. Add the integration via Configuration → Integrations → Add Integration → Baby Monitor
4. Enter your baby's name to create the monitoring instance

## Configuration

The integration is configured through the UI. You can add multiple babies by adding the integration multiple times with different names.

## Entities Created

For a baby named "Emma", the following entities will be created:

### Sensors
- `sensor.emma_last_diaper_change` - Last diaper change time and details
- `sensor.emma_last_feeding` - Last feeding time and details  
- `sensor.emma_last_sleep` - Last sleep session details
- `sensor.emma_total_diaper_changes` - Total diaper changes with daily breakdown
- `sensor.emma_total_feedings` - Total feedings with daily statistics
- `sensor.emma_total_sleep_sessions` - Total completed sleep sessions
- `sensor.emma_average_sleep_duration` - Average sleep duration in minutes
- `sensor.emma_average_feeding_amount` - Average feeding amount in ml
- `sensor.emma_temperature` - Current/last recorded temperature
- `sensor.emma_daily_summary` - Today's activity summary
- `sensor.emma_weekly_summary` - Last 7 days activity summary

### Buttons (Quick Actions)
- `button.emma_quick_wet_diaper` - Log wet diaper change
- `button.emma_quick_dirty_diaper` - Log dirty diaper change
- `button.emma_quick_wet_dirty_diaper` - Log wet & dirty diaper change
- `button.emma_quick_bottle_feeding` - Log bottle feeding (120ml, 15min)
- `button.emma_quick_breast_feeding_left` - Log left breast feeding (15min)
- `button.emma_quick_breast_feeding_right` - Log right breast feeding (15min)
- `button.emma_quick_breast_feeding_both` - Log both breasts feeding (25min)
- `button.emma_start_sleep` - Start sleep tracking
- `button.emma_end_sleep` - End sleep tracking with duration calculation

## Services

All services require the `baby_name` parameter to specify which baby the activity applies to.

### babymonitor.log_diaper_change
Log a diaper change with type and optional notes.
```yaml
service: babymonitor.log_diaper_change
data:
  baby_name: "Emma"
  diaper_type: "wet"  # or "dirty" or "both"
  notes: "First change of the day"
```

### babymonitor.log_feeding
Log a feeding session with details.
```yaml
service: babymonitor.log_feeding
data:
  baby_name: "Emma"
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
  baby_name: "Emma"
  sleep_type: "start"
  notes: "Put down for nap"

# End sleep (automatically calculates duration)
service: babymonitor.log_sleep
data:
  baby_name: "Emma"
  sleep_type: "end"
  notes: "Woke up refreshed"
```

### babymonitor.log_temperature
Record baby's temperature.
```yaml
service: babymonitor.log_temperature
data:
  baby_name: "Emma"
  temperature: 36.5
  notes: "Measured after bath"
```

### babymonitor.log_weight
Record baby's weight.
```yaml
service: babymonitor.log_weight
data:
  baby_name: "Emma"
  weight: 4.2  # kg
  notes: "Doctor visit checkup"
```

### babymonitor.log_height
Record baby's height.
```yaml
service: babymonitor.log_height
data:
  baby_name: "Emma"
  height: 52.0  # cm
  notes: "3 month checkup"
```

### babymonitor.log_medication
Log medication administration.
```yaml
service: babymonitor.log_medication
data:
  baby_name: "Emma"
  medication_name: "Paracetamol"
  medication_dosage: "2.5ml"
  notes: "For fever"
```

### babymonitor.log_milestone
Record developmental milestones.
```yaml
service: babymonitor.log_milestone
data:
  baby_name: "Emma"
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
        command: "Log wet diaper for Emma"
    action:
      - service: babymonitor.log_diaper_change
        data:
          baby_name: "Emma"
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
          {{ (as_timestamp(now()) - as_timestamp(states('sensor.emma_last_feeding'))) > 10800 }}
    condition:
      - condition: time
        after: "06:00:00"
        before: "22:00:00"
    action:
      - service: notify.mobile_app_your_phone
        data:
          message: "It's been 3 hours since Emma's last feeding"
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
            Today's summary for Emma:
            {{ state_attr('sensor.emma_daily_summary', 'diaper_changes') }} diaper changes
            {{ state_attr('sensor.emma_daily_summary', 'feedings') }} feedings
            {{ state_attr('sensor.emma_daily_summary', 'total_sleep_formatted') }} total sleep
          title: "Daily Baby Report"
```

### Sleep Duration Alert
```yaml
# Alert if sleep session is very short
automation:
  - alias: "Short Sleep Alert"
    trigger:
      - platform: state
        entity_id: sensor.emma_last_sleep
    condition:
      - condition: template
        value_template: >
          {{ state_attr('sensor.emma_last_sleep', 'duration_minutes') | int < 30 }}
    action:
      - service: notify.mobile_app_your_phone
        data:
          message: "Emma's last sleep was only {{ state_attr('sensor.emma_last_sleep', 'duration_formatted') }}"
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
title: Emma - Quick Actions
entities:
  - button.emma_quick_wet_diaper
  - button.emma_quick_dirty_diaper  
  - button.emma_quick_bottle_feeding
  - button.emma_quick_breast_feeding_both
  - button.emma_start_sleep
  - button.emma_end_sleep
```

### Summary Card
```yaml
type: entities
title: Emma - Current Status
entities:
  - sensor.emma_last_diaper_change
  - sensor.emma_last_feeding
  - sensor.emma_last_sleep
  - sensor.emma_temperature
  - sensor.emma_daily_summary
```

### Statistics Card
```yaml
type: statistics-graph
title: Emma - Feeding Amounts
entities:
  - sensor.emma_average_feeding_amount
period: day
days_to_show: 7
```

## Support

For issues, feature requests, or questions, please visit the GitHub repository.

## License

This project is licensed under the MIT License.