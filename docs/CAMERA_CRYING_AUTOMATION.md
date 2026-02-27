# Camera-Based Automatic Crying Detection

## 🚀 Quick Setup (Built-in Feature)

**NEW!** The Baby Monitor integration now includes built-in camera crying detection. No automations needed!

### Easy 3-Step Setup:

1. **Find your camera's crying sensor:**
   - Go to **Developer Tools → States**
   - Search for your camera's crying detection binary sensor
   - Example: `binary_sensor.baby_camera_crying_detected`

2. **Enable in integration settings:**
   - Go to **Settings → Devices & Services → Baby Monitor**
   - Click **Configure** on your baby's entry
   - Toggle **Camera Auto-Tracking** to ON
   - Select your camera's crying sensor from the dropdown
   - Click **Submit**

3. **Done!** The integration will now:
   - ✅ Automatically detect when crying starts
   - ✅ Automatically detect when crying stops
   - ✅ Calculate duration automatically
   - ✅ Update sensors in real-time
   - ✅ Track all statistics

**That's it!** No helper entities or automations required. Everything works out of the box.

### Quick Dashboard Card

Add this card to see today's total crying episodes:

```yaml
type: entity
entity: sensor.anika_total_crying_episodes
name: Today's Total Cries
icon: mdi:emoticon-sad-outline
```

**Want more display options?** See [Today's Total Cries Cards](TODAYS_TOTAL_CRIES_CARDS.md) for 8+ dashboard card styles.

---

## Manual Automation Setup (Alternative)

If you prefer more control or need advanced features like notifications, you can still create custom automations. See below for detailed instructions.

---

## Overview

This guide shows how to automatically track crying episodes when your baby monitor camera detects crying sounds. The integration will:
- Start tracking when camera detects crying
- Stop tracking when crying ends
- Calculate duration automatically
- Update dashboard in real-time

---

## Prerequisites

- A baby monitor camera with crying detection (e.g., Nest Cam, Eufy, Wyze, etc.)
- The camera integrated into Home Assistant
- A binary sensor that shows crying state (example: `binary_sensor.baby_camera_crying_detected`)

---

## Step 1: Find Your Camera's Crying Sensor

1. Go to **Developer Tools → States**
2. Search for your camera entity
3. Look for binary sensors related to:
   - `crying_detected`
   - `sound_detected`
   - `baby_crying`
   - Or similar

**Example entities:**
- `binary_sensor.baby_camera_crying_detected`
- `binary_sensor.nursery_camera_sound`
- `binary_sensor.wyze_cam_baby_crying`

---

## Step 2: Create Helper Input

We need a helper to track if we're currently tracking a crying episode:

1. Go to **Settings → Devices & Services → Helpers**
2. Click **Create Helper → Toggle**
3. Fill in:
   - **Name:** Baby Crying Tracker Active
   - **Icon:** mdi:emoticon-sad-outline
4. Click **Create**

This creates `input_boolean.baby_crying_tracker_active`

---

## Step 3: Create Crying Start Automation

**Automation YAML:**

```yaml
alias: Auto-Track Crying Start (Camera)
description: Automatically start tracking when camera detects crying
trigger:
  - platform: state
    entity_id: binary_sensor.baby_camera_crying_detected
    to: "on"
condition:
  - condition: state
    entity_id: input_boolean.baby_crying_tracker_active
    state: "off"
action:
  # Mark that we're tracking
  - service: input_boolean.turn_on
    target:
      entity_id: input_boolean.baby_crying_tracker_active
  
  # Log crying start
  - service: babymonitor.log_crying
    data:
      baby_name: Anika
      crying_intensity: moderate
      duration: 0
      notes: "Auto-detected by camera"
  
  # Optional: Send notification
  - service: notify.notify
    data:
      title: "Baby Crying Detected"
      message: "Camera detected crying at {{ now().strftime('%H:%M') }}"
mode: single
icon: mdi:emoticon-sad-outline
```

---

## Step 4: Create Crying End Automation

**Automation YAML:**

```yaml
alias: Auto-Track Crying End (Camera)
description: Automatically stop tracking when crying ends
trigger:
  - platform: state
    entity_id: binary_sensor.baby_camera_crying_detected
    to: "off"
    for:
      seconds: 10  # Wait 10 seconds to avoid false stops
condition:
  - condition: state
    entity_id: input_boolean.baby_crying_tracker_active
    state: "on"
action:
  # Calculate duration
  - variables:
      start_time: "{{ states.input_boolean.baby_crying_tracker_active.last_changed }}"
      end_time: "{{ now() }}"
      duration_seconds: "{{ (as_timestamp(end_time) - as_timestamp(start_time)) | int }}"
      duration_minutes: "{{ (duration_seconds / 60) | round(0) }}"
  
  # Mark that we're done tracking
  - service: input_boolean.turn_off
    target:
      entity_id: input_boolean.baby_crying_tracker_active
  
  # Log final crying episode with duration
  - service: babymonitor.log_crying
    data:
      baby_name: Anika
      crying_intensity: moderate
      duration: "{{ duration_minutes }}"
      notes: "Auto-detected by camera ({{ duration_minutes }} min)"
  
  # Optional: Send notification
  - service: notify.notify
    data:
      title: "Baby Stopped Crying"
      message: "Crying episode ended. Duration: {{ duration_minutes }} minutes"
mode: single
icon: mdi:emoticon-happy-outline
```

---

## Step 5: Add Dashboard Status Card

**Show when crying detection is active:**

```yaml
type: entities
title: 🎥 Camera Crying Detection
entities:
  - entity: binary_sensor.baby_camera_crying_detected
    name: Camera Detecting Crying
    icon: mdi:camera
  
  - entity: input_boolean.baby_crying_tracker_active
    name: Tracking Active
    icon: mdi:record-circle-outline
  
  - entity: sensor.anika_total_crying_episodes
    name: Total Cries Today
  
  - entity: sensor.anika_total_crying_episodes
    name: Total Duration
    type: attribute
    attribute: total_duration_minutes
    icon: mdi:clock
```

---

## Step 6: Advanced - Intensity Detection

If your camera provides sound level data, you can adjust crying intensity:

```yaml
alias: Auto-Track Crying with Intensity
description: Track crying with intensity based on sound level
trigger:
  - platform: state
    entity_id: binary_sensor.baby_camera_crying_detected
    to: "on"
condition:
  - condition: state
    entity_id: input_boolean.baby_crying_tracker_active
    state: "off"
action:
  - service: input_boolean.turn_on
    target:
      entity_id: input_boolean.baby_crying_tracker_active
  
  # Determine intensity based on sound level
  - variables:
      sound_level: "{{ states('sensor.baby_camera_sound_level') | float }}"
      intensity: >
        {% if sound_level < 60 %}
          light
        {% elif sound_level < 80 %}
          moderate
        {% else %}
          intense
        {% endif %}
  
  - service: babymonitor.log_crying
    data:
      baby_name: Anika
      crying_intensity: "{{ intensity }}"
      duration: 0
      notes: "Auto-detected ({{ sound_level }} dB)"
mode: single
```

---

## Alternative: Simple State-Based Tracking

If you prefer simpler tracking without duration calculation:

```yaml
alias: Simple Camera Crying Logger
description: Log each crying detection as separate episode
trigger:
  - platform: state
    entity_id: binary_sensor.baby_camera_crying_detected
    to: "on"
action:
  - service: babymonitor.log_crying
    data:
      baby_name: Anika
      crying_intensity: moderate
      duration: 5  # Assume 5 minutes per detection
      notes: "Camera detected"
mode: single
```

---

## Dashboard with Camera Integration

**Complete monitoring dashboard:**

```yaml
type: vertical-stack
cards:
  # Camera Status
  - type: picture-entity
    entity: camera.baby_monitor
    name: Baby Monitor
    show_state: true

  # Crying Status
  - type: horizontal-stack
    cards:
      - type: entity
        entity: binary_sensor.baby_camera_crying_detected
        name: Crying
        icon: mdi:emoticon-sad-outline
      
      - type: entity
        entity: input_boolean.baby_crying_tracker_active
        name: Tracking
        icon: mdi:record-circle

  # Today's Stats
  - type: glance
    entities:
      - entity: sensor.anika_total_crying_episodes
        name: Episodes
      - entity: sensor.anika_total_crying_episodes
        name: Duration
        attribute: total_duration_minutes
      - entity: sensor.anika_crying_analysis
        name: Status

  # History
  - type: history-graph
    title: Crying Detection History
    entities:
      - entity: binary_sensor.baby_camera_crying_detected
        name: Camera
      - entity: sensor.anika_total_crying_episodes
        name: Episodes
    hours_to_show: 24
```

---

## Troubleshooting

**Automation doesn't trigger:**
- Check camera entity name matches exactly
- Verify binary sensor state changes in Developer Tools → States
- Check automation is enabled (Settings → Automations)

**False detections:**
- Adjust `for:` delay in trigger (e.g., `for: {seconds: 15}`)
- Filter out brief sounds with condition on duration
- Check camera sensitivity settings

**Duration calculation issues:**
- Ensure input_boolean helper exists
- Verify automation saves last_changed timestamp
- Add logging to debug: `service: system_log.write` with message

**Multiple cameras:**
- Create separate automations for each camera
- Use different input_boolean helpers per camera
- Or use camera name in automation variables

---

## Advanced: Multi-Camera Support

If you have multiple cameras monitoring different areas:

```yaml
alias: Multi-Camera Crying Detection
description: Track crying from any camera
trigger:
  - platform: state
    entity_id:
      - binary_sensor.nursery_camera_crying
      - binary_sensor.bedroom_camera_crying
      - binary_sensor.living_room_camera_crying
    to: "on"
action:
  - variables:
      camera_name: "{{ trigger.to_state.attributes.friendly_name }}"
  
  - service: babymonitor.log_crying
    data:
      baby_name: Anika
      crying_intensity: moderate
      duration: 5
      notes: "Detected by {{ camera_name }}"
mode: queued
max: 10
```

---

## Example: Time-of-Day Adjustments

Adjust intensity assumption based on time of day:

```yaml
alias: Smart Crying Detection
trigger:
  - platform: state
    entity_id: binary_sensor.baby_camera_crying_detected
    to: "on"
action:
  - variables:
      hour: "{{ now().hour }}"
      # Night crying might be more intense
      intensity: >
        {% if hour >= 22 or hour < 6 %}
          intense
        {% else %}
          moderate
        {% endif %}
  
  - service: babymonitor.log_crying
    data:
      baby_name: Anika
      crying_intensity: "{{ intensity }}"
      duration: 0
      notes: "Auto-detected at {{ now().strftime('%H:%M') }}"
```

---

## Notification Examples

**Push notification with actionable buttons:**

```yaml
action:
  - service: notify.mobile_app_your_phone
    data:
      title: "Baby Crying Detected"
      message: "Camera detected crying at {{ now().strftime('%H:%M') }}"
      data:
        actions:
          - action: "DISMISS_CRYING"
            title: "Dismiss"
          - action: "VIEW_CAMERA"
            title: "View Camera"
        tag: "baby_crying"
        importance: high
        notification_icon: mdi:emoticon-sad-outline
```

---

## Best Practices

1. **Test thoroughly:** Run automations manually first to verify behavior
2. **Add delays:** Use `for:` in triggers to avoid false positives
3. **Log everything:** Add notes field with camera name and timestamp
4. **Monitor accuracy:** Compare camera detections with manual observations
5. **Adjust sensitivity:** Tune camera settings and automation conditions
6. **Battery backup:** Ensure camera has power backup for 24/7 monitoring
7. **Review data:** Check statistics to identify patterns and optimize

---

## Integration with Other Systems

**Example: Turn on night light when crying detected:**

```yaml
alias: Night Light on Crying
trigger:
  - platform: state
    entity_id: binary_sensor.baby_camera_crying_detected
    to: "on"
condition:
  - condition: sun
    after: sunset
    before: sunrise
action:
  - service: light.turn_on
    target:
      entity_id: light.nursery_night_light
    data:
      brightness: 50
      color_name: red
```

**Example: Pause music when crying:**

```yaml
alias: Pause Music on Crying
trigger:
  - platform: state
    entity_id: binary_sensor.baby_camera_crying_detected
    to: "on"
action:
  - service: media_player.media_pause
    target:
      entity_id: media_player.nursery_speaker
```

---

## Summary

With camera-based crying detection, you get:
- ✅ Automatic crying episode tracking
- ✅ Real-time dashboard updates
- ✅ Duration calculation without manual logging
- ✅ Historical trends and statistics
- ✅ Notifications when baby needs attention
- ✅ Integration with smart home actions

Replace `Anika` with your baby's name and adjust entity names to match your camera setup!
