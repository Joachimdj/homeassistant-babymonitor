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

### 🎥 Camera Auto-Tracking (NEW!)
- **Automatic crying detection** from camera sensors
- No manual logging needed - works hands-free
- Auto-calculates crying episode duration
- Real-time sensor updates
- Simple 3-step setup in integration settings
- Works with any Home Assistant-compatible baby camera

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

### Configuring Daily Goals and Thresholds

After setting up the integration, you can customize daily goals and thresholds:

1. Go to **Settings → Devices & Services**
2. Find the **Baby Monitor** integration
3. Click **Configure** (or the three dots menu → **Configure**)
4. Adjust the following settings:

**Daily Care Goals:**
- **Minimum diaper changes per day** (default: 6) - Total expected diaper changes
- **Minimum wet diapers per day** (default: 4) - Monitors hydration levels
- **Minimum feedings per day** (default: 6) - Expected feeding frequency
- **Minimum sleep hours per day** (default: 12) - Total sleep target
- **Target tummy time** (default: 15 minutes) - Daily tummy time goal

**Reminder Intervals:**
- **Feeding reminder interval** (default: 3 hours) - Time between feedings
- **Diaper change reminder interval** (default: 4 hours) - Max time between changes

These settings help sensors provide status information like "Meeting goal" or "Below goal" in their attributes, making it easy to track if your baby is meeting care recommendations.

**Example:**
- Set minimum wet diapers to 4
- Check `sensor.anika_total_diaper_changes` attributes
- View `wet_diaper_status`: "Meeting goal" or "Below goal"
- View `progress_percentage` to see progress toward goal

## Entities Created

For a baby named "Anika", the following entities will be created:

### Sensors
- `sensor.anika_last_diaper_change` - Last diaper change time and details
- `sensor.anika_last_feeding` - Last feeding time and details  
- `sensor.anika_last_sleep` - Last sleep session details
- `sensor.anika_total_diaper_changes` - Total diaper changes with daily breakdown (includes `wet_today`, `dirty_today`, `diaper_status`, and `progress_percentage` attributes)
- `sensor.anika_total_feedings` - Total feedings with daily statistics (includes `feeding_status` and `progress_percentage` based on configured goals)
- `sensor.anika_total_sleep_sessions` - Total completed sleep sessions
- `sensor.anika_average_sleep_duration` - Average sleep duration in minutes
- `sensor.anika_average_feeding_amount` - Average feeding amount in ml
- `sensor.anika_temperature` - Current/last recorded temperature
- `sensor.anika_tummy_time_today` - Today's tummy time with `tummy_time_status` and `progress_percentage`
- `sensor.anika_daily_summary` - Today's activity summary
- `sensor.anika_weekly_summary` - Last 7 days activity summary

**Note:** Many sensors include status attributes (e.g., "Meeting goal" or "Below goal") based on your configured daily goals. Use these for monitoring and automations.

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

### Diaper Change Alert
```yaml
# Alert if wet diaper count is low (possible dehydration indicator)
automation:
  - alias: "Low Wet Diaper Alert"
    trigger:
      - platform: time
        at: "18:00:00"
    condition:
      - condition: template
        value_template: >
          {{ state_attr('sensor.anika_total_diaper_changes', 'wet_today') | int < 4 }}
    action:
      - service: notify.mobile_app_your_phone
        data:
          message: >
            Anika has only had {{ state_attr('sensor.anika_total_diaper_changes', 'wet_today') }} wet diapers today.
            Wet: {{ state_attr('sensor.anika_total_diaper_changes', 'wet_today') }}, 
            Dirty: {{ state_attr('sensor.anika_total_diaper_changes', 'dirty_today') }}
          title: "Low Wet Diaper Count"
```

### Goal Status Alert
```yaml
# Alert when daily goals are not being met
automation:
  - alias: "Daily Care Goals Check"
    trigger:
      - platform: time
        at: "17:00:00"
    action:
      - choose:
          # Check diaper goal
          - conditions:
              - condition: template
                value_template: >
                  {{ state_attr('sensor.anika_total_diaper_changes', 'diaper_status') == 'Below goal' }}
            sequence:
              - service: notify.mobile_app_your_phone
                data:
                  message: >
                    Anika's diaper changes are below goal today.
                    Current: {{ state_attr('sensor.anika_total_diaper_changes', 'today_count') }}
                    Goal: {{ state_attr('sensor.anika_total_diaper_changes', 'min_diapers_goal') }}
                  title: "⚠️ Diaper Goal Not Met"
          
          # Check feeding goal
          - conditions:
              - condition: template
                value_template: >
                  {{ state_attr('sensor.anika_total_feedings', 'feeding_status') == 'Below goal' }}
            sequence:
              - service: notify.mobile_app_your_phone
                data:
                  message: >
                    Anika's feedings are below goal today.
                    Current: {{ state_attr('sensor.anika_total_feedings', 'today_count') }}
                    Goal: {{ state_attr('sensor.anika_total_feedings', 'min_feedings_goal') }}
                  title: "⚠️ Feeding Goal Not Met"
          
          # Check tummy time goal
          - conditions:
              - condition: template
                value_template: >
                  {{ state_attr('sensor.anika_tummy_time_today', 'tummy_time_status') == 'Below goal' }}
            sequence:
              - service: notify.mobile_app_your_phone
                data:
                  message: >
                    Don't forget tummy time today!
                    Current: {{ states('sensor.anika_tummy_time_today') }} min
                    Goal: {{ state_attr('sensor.anika_tummy_time_today', 'target_daily_minutes') }} min
                  title: "⚠️ Tummy Time Goal Not Met"
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

### Simple Diaper Count Display (Copy & Paste Ready)
```yaml
# Shows today's wet and dirty diaper counts
type: entities
title: Today's Diapers
entities:
  - entity: sensor.anika_total_diaper_changes
    name: Total Changes
    type: attribute
    attribute: today_count
  - entity: sensor.anika_total_diaper_changes
    name: Wet Diapers
    type: attribute
    attribute: wet_today
  - entity: sensor.anika_total_diaper_changes
    name: Dirty Diapers
    type: attribute
    attribute: dirty_today
```
**Note:** Replace `anika` with your baby's name (lowercase).

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

### Diaper Tracking Card (Wet & Dirty Counts)
```yaml
type: entities
title: Today's Diaper Changes
entities:
  # Total diaper changes today
  - type: attribute
    entity: sensor.anika_total_diaper_changes
    attribute: today_count
    name: Total Changes Today
    icon: mdi:baby-carriage
  # Wet diapers today
  - type: attribute
    entity: sensor.anika_total_diaper_changes
    attribute: wet_today
    name: Wet Diapers
    icon: mdi:water
  # Dirty diapers today
  - type: attribute
    entity: sensor.anika_total_diaper_changes
    attribute: dirty_today
    name: Dirty Diapers
    icon: mdi:delete-variant
```

**Accessing diaper counts in templates:**
```yaml
# Get today's wet diaper count
{{ state_attr('sensor.anika_total_diaper_changes', 'wet_today') }}

# Get today's dirty diaper count
{{ state_attr('sensor.anika_total_diaper_changes', 'dirty_today') }}

# Get total changes today
{{ state_attr('sensor.anika_total_diaper_changes', 'today_count') }}
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

## Development & Testing

### Running Tests

This project includes comprehensive unit tests with automatic pre-push testing to ensure code quality.

**Run all tests:**
```bash
./run_tests.sh
```

This will:
- Create a virtual environment if needed
- Install test dependencies
- Run all tests with coverage reporting
- Generate a coverage report in `htmlcov/`

**Run specific tests:**
```bash
# Activate virtual environment
source venv/bin/activate

# Run specific test file
pytest tests/test_storage.py

# Run with verbose output
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=custom_components/babymonitor --cov-report=html
```

### Automatic Pre-Push Testing

Tests run automatically before every `git push`. The pre-push hook is installed at `.git/hooks/pre-push`.

When you push:
- ✅ Tests pass → Push proceeds
- ❌ Tests fail → Push is blocked

To skip pre-push checks (not recommended):
```bash
git push --no-verify
```

### Test Coverage

The test suite covers:
- ✅ Storage functionality (add/retrieve activities)
- ✅ Camera crying detection and tracking
- ✅ Sensor state calculations and attributes
- ✅ Daily activity filtering
- ✅ Duration calculations
- ✅ Error handling

For detailed testing documentation, see [tests/README.md](tests/README.md).

### Contributing

When contributing:
1. Write tests for new features
2. Ensure all tests pass before committing
3. Maintain test coverage above 80%
4. Follow existing code style
5. Update documentation as needed

## Support

For issues, feature requests, or questions, please visit the GitHub repository.

## Additional Resources

- [Lovelace Dashboard Examples](docs/lovelace_examples.yaml) - Complete dashboard configurations
- [Simple Diaper Card Example](docs/simple_diaper_card_example.yaml) - Ready-to-use diaper tracking card
- [Today's Total Cries Cards](docs/TODAYS_TOTAL_CRIES_CARDS.md) - 8+ dashboard card styles for crying statistics
- [Camera Auto-Tracking Setup](docs/CAMERA_AUTO_TRACKING_SETUP.md) - Easy 3-step camera crying detection setup
- [Camera Crying Automation](docs/CAMERA_CRYING_AUTOMATION.md) - Advanced automation examples with notifications
- [Example Automations](docs/example_automations.yaml) - Ready-to-use automation examples
- [Installation Guide](docs/GITHUB_SETUP.md) - Detailed setup instructions
- [Testing Guide](tests/README.md) - Comprehensive testing documentation

## Troubleshooting

### Diaper counts not showing in dashboard

If you're trying to display dirty/wet diaper counts and they're not showing or updating:

1. **Check your sensor name** - Make sure you're using the correct baby name (lowercase with underscores):
   - ✅ Correct: `sensor.anika_total_diaper_changes`
   - ❌ Wrong: `sensor.Anika_total_diaper_changes`

2. **Verify the sensor exists** - Go to Developer Tools → States and search for your sensor

3. **Check the attributes** - In Developer Tools → States, click on `sensor.BABYNAME_total_diaper_changes` and verify these attributes exist:
   - `today_count`
   - `wet_today`
   - `dirty_today`

4. **Log some activities** - Use the quick action buttons to log a few diaper changes, then check if the counts update
   - **Note**: As of the latest version, sensors automatically update when you log activities via buttons or services

5. **Restart Home Assistant** - After installation, a restart may be needed for entities to appear
   - After updating to newer versions with auto-update features, restart to activate the fix

6. **Clear browser cache** - Sometimes the dashboard caches old values
   - Hold Shift and click Reload in your browser
   - Or press Ctrl+Shift+R (Windows/Linux) or Cmd+Shift+R (Mac)

### Example test template
Test in Developer Tools → Template:
```yaml
{% set sensor = 'sensor.anika_total_diaper_changes' %}
Today: {{ state_attr(sensor, 'today_count') }}
Wet: {{ state_attr(sensor, 'wet_today') }}
Dirty: {{ state_attr(sensor, 'dirty_today') }}
```

## License

This project is licensed under the MIT License.