# Crying Times & Analysis - User Guide

## Overview

The Baby Monitor tracks all crying episodes and provides detailed analysis including:
- Number of crying episodes today
- Total duration of crying
- Average duration per episode
- Intensity breakdown (light, moderate, intense)
- Status summary (Peaceful day, Minimal crying, Normal fussiness, Fussy day)

---

## Logging Crying

### Quick Button Method (Easiest)

1. Go to your Home Assistant Dashboard
2. Find the **"Start Crying"** button in your Baby Monitor device
3. Click to log a crying episode

The button automatically logs:
- Crying intensity: Moderate
- Duration: 0 (updates when ended)
- Timestamp: Current time

### Via Service Call (For Automations)

```yaml
service: babymonitor.log_crying
data:
  baby_name: "Anika"
  crying_intensity: "moderate"
  duration: 5
  notes: "Teething discomfort"
```

**Crying Intensity Options:**
- `light` - Fussing, minor crying
- `moderate` - Normal crying (default)
- `intense` - Intense, prolonged crying

**Duration:** Minutes of crying

---

## Dashboard Cards

### Option 1: Simple List (Most Detail)

Shows all crying metrics in a clean list:

```yaml
type: entities
title: 😢 Crying Today
entities:
  - entity: sensor.anika_crying_analysis
    name: Crying Status
  - entity: sensor.anika_crying_analysis
    name: Episodes Today
    type: attribute
    attribute: episodes_today
  - entity: sensor.anika_crying_analysis
    name: Total Duration
    type: attribute
    attribute: total_duration_minutes
    icon: mdi:clock
  - entity: sensor.anika_crying_analysis
    name: Average Episode
    type: attribute
    attribute: average_episode_duration
    icon: mdi:timer-outline
  - entity: sensor.anika_crying_analysis
    name: Intensity Breakdown
    type: attribute
    attribute: intensity_breakdown
```

### Option 2: Markdown Summary

Clean formatted card with emoji:

```yaml
type: markdown
content: |
  ### 😢 Crying Summary Today
  
  **Status:** {{ states('sensor.anika_crying_analysis') }}
  
  **Episodes:** {{ state_attr('sensor.anika_crying_analysis', 'episodes_today') }} times
  
  **Total Duration:** {{ state_attr('sensor.anika_crying_analysis', 'total_duration_minutes') }} minutes
  
  **Average Episode:** {{ state_attr('sensor.anika_crying_analysis', 'average_episode_duration') }} minutes
  
  **Intensity:**
  - Light: {{ state_attr('sensor.anika_crying_analysis', 'intensity_breakdown').get('light', 0) }}
  - Moderate: {{ state_attr('sensor.anika_crying_analysis', 'intensity_breakdown').get('moderate', 0) }}
  - Intense: {{ state_attr('sensor.anika_crying_analysis', 'intensity_breakdown').get('intense', 0) }}
```

### Option 3: Status Card Only

Just show the crying status summary:

```yaml
type: entities
title: 😢 Crying Status
entities:
  - entity: sensor.anika_crying_analysis
    name: Today's Status
```

**Status Values:**
- ✅ **Peaceful day** - No crying
- 😊 **Minimal crying** - ≤2 episodes, ≤30 minutes total
- 😐 **Normal fussiness** - ≤5 episodes, ≤60 minutes total
- 😢 **Fussy day** - More than 5 episodes or >60 minutes

### Option 4: Stack Card (All Metrics)

Combine status and details in a vertical stack:

```yaml
type: vertical-stack
cards:
  - type: entities
    title: 😢 Crying Status
    entities:
      - entity: sensor.anika_crying_analysis
        name: Today's Status

  - type: markdown
    content: |
      **Episodes:** {{ state_attr('sensor.anika_crying_analysis', 'episodes_today') }}
      
      **Total Time:** {{ state_attr('sensor.anika_crying_analysis', 'total_duration_minutes') }} min
      
      **Average:** {{ state_attr('sensor.anika_crying_analysis', 'average_episode_duration') }} min/episode
```

---

## Adding Crying Button to UI

The "Start Crying" button is automatically available in your Baby Monitor device. To add it to a dashboard card:

```yaml
type: horizontal-stack
cards:
  - type: button
    entity: button.anika_quick_crying
    name: Log Crying
    icon: mdi:emoticon-sad-outline
    
  - type: glance
    entities:
      - entity: sensor.anika_crying_analysis
        name: Status
```

---

## Advanced: Automation on High Crying

Create an automation that alerts you if baby cries excessively:

**Automation YAML:**

```yaml
alias: Alert on High Crying Duration
description: Notify when crying exceeds 30 minutes today
trigger:
  - platform: time_pattern
    minutes: /30  # Check every 30 minutes
condition:
  - condition: numeric_state
    entity_id: sensor.anika_crying_analysis
    attribute: total_duration_minutes
    above: 30
action:
  - service: notify.notify
    data:
      message: |
        Baby has been crying for {{ state_attr('sensor.anika_crying_analysis', 'total_duration_minutes') }} 
        minutes today with {{ state_attr('sensor.anika_crying_analysis', 'episodes_today') }} episodes.
      title: Extended Crying Alert
mode: single
```

---

## Sensor Attributes Reference

The `sensor.anika_crying_analysis` sensor provides:

| Attribute | Type | Description | Example |
|-----------|------|-------------|---------|
| `state` | string | Overall crying status | "Normal fussiness" |
| `episodes_today` | number | Total crying episodes | 3 |
| `total_duration_minutes` | number | Total crying time | 25 |
| `average_episode_duration` | float | Avg duration per episode | 8.3 |
| `intensity_breakdown` | dict | Count by intensity | `{light: 1, moderate: 2, intense: 0}` |
| `last_episode` | datetime | When last crying occurred | 14:23:45 |

---

## Understanding the Status Values

### Status Determination Logic

- **Peaceful day** → No crying
- **Minimal crying** → ≤2 episodes AND ≤30 minutes
- **Normal fussiness** → ≤5 episodes AND ≤60 minutes
- **Fussy day** → >5 episodes OR >60 minutes

This helps determine if today's crying is within normal ranges or if there might be an issue (teething, hunger, discomfort, etc.)

---

## Tips for Tracking

1. **Log intensity accurately:**
   - Light = fussing/whining without real tears
   - Moderate = normal crying with emotion
   - Intense = prolonged, distressed crying

2. **Use notes for context:**
   ```yaml
   service: babymonitor.log_crying
   data:
     baby_name: "Anika"
     crying_intensity: "intense"
     duration: 15
     notes: "Appears to be teething discomfort"
   ```

3. **Track patterns:**
   - Review crying history in your database
   - Note times of day when baby cries most
   - Identify triggers (hunger, tiredness, hunger)

4. **Set reasonable goals:**
   - Newborns (0-3 months): 2-3 hours of crying normal
   - Infants (3-6 months): 1-2 hours of crying normal
   - Older babies (6+ months): 30 minutes - 1 hour normal

---

## Troubleshooting

**Crying button doesn't appear:**
- Restart Home Assistant
- Clear browser cache
- Check Settings → Devices & Services → Baby Monitor

**Crying count not updating:**
- Check that the service call completed
- Verify baby name matches exactly
- Check Home Assistant logs for errors

**Data looks wrong:**
- Make sure duration was set correctly when logging
- Check that crying type (light/moderate/intense) is accurate
- Review recent activity logs in storage

