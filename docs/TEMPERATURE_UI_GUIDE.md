# Temperature Logging UI - User Guide

## Quick Temperature Button

A "Log Temperature" button has been added to your Baby Monitor integration. This button logs a quick temperature of 37°C (normal body temperature).

**To use it:**
1. Go to Home Assistant Dashboard
2. Find the "Log Temperature" button in your Baby Monitor device
3. Click the button to log a temperature reading

---

## Advanced: Custom Temperature Input UI

For more control, create a custom UI that lets you enter any temperature value. Here's how:

### Step 1: Create Input Number Helper

1. Go to **Settings → Devices & Services → Helpers**
2. Click **Create Helper → Number**
3. Fill in:
   - **Name:** Baby Temperature Input
   - **Unit of measurement:** °C
   - **Min value:** 35
   - **Max value:** 40
   - **Step:** 0.1
   - **Icon:** mdi:thermometer
4. Click **Create**

This creates `input_number.baby_temperature_input`

### Step 2: Create an Automation or Script

**Option A: Using Automation**

1. Go to **Settings → Automations & Scenes → Create Automation**
2. Switch to **Edit in YAML** mode
3. Paste this:

```yaml
alias: Log Baby Temperature
description: Log baby temperature from input helper
trigger:
  - platform: state
    entity_id:
      - input_number.baby_temperature_input
condition: []
action:
  - service: babymonitor.log_temperature
    data:
      baby_name: Anika
      temperature: "{{ states('input_number.baby_temperature_input') | float }}"
      notes: Anal thermometer
mode: single
```

Replace `Anika` with your baby's name.

**Option B: Using Script (Recommended)**

1. Go to **Settings → Developer Tools → Scripts**
2. Create a new script with this YAML:

```yaml
alias: Log Temperature Service
description: Log temperature from input number
sequence:
  - service: babymonitor.log_temperature
    data:
      baby_name: Anika
      temperature: "{{ states('input_number.baby_temperature_input') | float }}"
      notes: Anal thermometer
mode: single
icon: mdi:thermometer
```

Replace `Anika` with your baby's name.

### Step 3: Add to Dashboard

**Option 1: Simple Input Card**

```yaml
type: entities
title: Temperature Logger
entities:
  - entity: input_number.baby_temperature_input
    name: Enter Temperature
  - type: button
    entity: script.log_temperature_service
    name: Log Temperature
    action_name: Log
```

**Option 2: Gauge + Input + Button**

```yaml
type: vertical-stack
cards:
  - type: gauge
    entity: sensor.anika_current_temperature
    title: Baby Temperature
    min: 35
    max: 40
    unit: °C
    segments:
      - from: 35
        color: "#0000ff"
      - from: 36.5
        color: "#00ff00"
      - from: 37.5
        color: "#ffff00"
      - from: 38
        color: "#ff8800"
      - from: 39
        color: "#ff0000"
        
  - type: entities
    entities:
      - entity: input_number.baby_temperature_input
        name: Enter Temperature
      - type: button
        entity: script.log_temperature_service
        name: Log Temperature
        action_name: Log
```

**Option 3: Markdown Card with Instructions**

```yaml
type: markdown
content: |
  ## Temperature Logger
  
  1. Enter temperature value below
  2. Click "Log Temperature" button
  3. Temperature will be saved to your baby's history
  
  **Steps:**
  - [ ] Set temperature value
  - [ ] Press Log button
  - [ ] Check dashboard for update
title: How to Log Temperature
```

### Step 4: Add to a Custom Tab

1. Edit your Lovelace dashboard
2. Create a new tab called "Health & Temperature"
3. Add the cards from above
4. Save

---

## Color Temperature Guide

- **Blue (35-36.5°C):** Hypothermia - Too cold
- **Green (36.5-37.5°C):** Normal - Healthy
- **Yellow (37.5-38°C):** Mild - Slightly elevated
- **Orange (38-39°C):** Fever - Elevated temperature
- **Red (39-40°C):** High Fever - Medical attention needed

---

## Service Call (Advanced Users)

You can also call the service directly in automations:

```yaml
service: babymonitor.log_temperature
data:
  baby_name: "Anika"
  temperature: 37.5
  notes: "Anal thermometer"
```

---

## Troubleshooting

**Button doesn't appear:**
- Restart Home Assistant
- Clear browser cache (Ctrl+Shift+R or Cmd+Shift+R)
- Go to Settings → Devices & Services → Baby Monitor → Check entities

**Temperature doesn't update:**
- Check that the service call completed without errors
- Go to Settings → System → Logs and look for errors
- Verify the baby name matches exactly (case-sensitive for entities)

**Can't create input number:**
- Make sure you have Helper integration enabled
- Check Settings → System → Integrations

