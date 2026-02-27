# Today's Total Cries - Dashboard Cards

Quick dashboard cards to display today's crying episode count prominently.

## 📊 Simple Count Display

### Option 1: Big Number Card

```yaml
type: entity
entity: sensor.anika_total_crying_episodes
name: Today's Total Cries
icon: mdi:emoticon-sad-outline
```

### Option 2: Statistic Card with Icon

```yaml
type: statistic
entity: sensor.anika_total_crying_episodes
name: Cries Today
icon: mdi:emoticon-cry-outline
period:
  calendar:
    period: day
chart_type: line
stat_types:
  - mean
  - min
  - max
```

### Option 3: Gauge Card (Color-Coded)

```yaml
type: gauge
entity: sensor.anika_total_crying_episodes
name: Cries Today
min: 0
max: 20
needle: true
severity:
  green: 0
  yellow: 5
  orange: 10
  red: 15
```

### Option 4: Entities Card with Details

```yaml
type: entities
title: 😢 Today's Crying Summary
entities:
  - entity: sensor.anika_total_crying_episodes
    name: Total Episodes
    icon: mdi:counter
  
  - type: attribute
    entity: sensor.anika_total_crying_episodes
    attribute: total_duration_minutes
    name: Total Duration (min)
    icon: mdi:clock-outline
  
  - type: attribute
    entity: sensor.anika_total_crying_episodes
    attribute: average_episode_duration
    name: Average Duration (min)
    icon: mdi:chart-timeline-variant
  
  - type: attribute
    entity: sensor.anika_total_crying_episodes
    attribute: last_episode
    name: Last Episode
    icon: mdi:clock-time-eight-outline
```

### Option 5: Markdown Card (Custom Styling)

```yaml
type: markdown
content: |
  # 😢 Today's Cries
  
  ## {{ states('sensor.anika_total_crying_episodes') }}
  
  **Total Duration:** {{ state_attr('sensor.anika_total_crying_episodes', 'total_duration_minutes') }} min
  
  **Average:** {{ state_attr('sensor.anika_total_crying_episodes', 'average_episode_duration') }} min per episode
  
  {% set last = state_attr('sensor.anika_total_crying_episodes', 'last_episode') %}
  **Last Episode:** {{ last if last else 'None today' }}
```

### Option 6: Glance Card (Compact)

```yaml
type: glance
title: Today's Crying Stats
entities:
  - entity: sensor.anika_total_crying_episodes
    name: Episodes
  - entity: sensor.anika_total_crying_episodes
    name: Duration
    attribute: total_duration_minutes
  - entity: sensor.anika_total_crying_episodes
    name: Average
    attribute: average_episode_duration
show_name: true
show_icon: true
show_state: true
```

---

## 🎨 Advanced Styling Options

### Option 7: Custom Button Card (Requires custom:button-card)

```yaml
type: custom:button-card
entity: sensor.anika_total_crying_episodes
name: Cries Today
show_state: true
show_icon: true
icon: mdi:emoticon-cry
styles:
  card:
    - background: |
        [[[
          if (states['sensor.anika_total_crying_episodes'].state >= 10) return 'rgba(255, 0, 0, 0.1)';
          if (states['sensor.anika_total_crying_episodes'].state >= 5) return 'rgba(255, 165, 0, 0.1)';
          return 'rgba(76, 175, 80, 0.1)';
        ]]]
  icon:
    - color: |
        [[[
          if (states['sensor.anika_total_crying_episodes'].state >= 10) return 'red';
          if (states['sensor.anika_total_crying_episodes'].state >= 5) return 'orange';
          return 'green';
        ]]]
    - width: 70px
  name:
    - font-size: 14px
    - font-weight: bold
  state:
    - font-size: 32px
    - font-weight: bold
tap_action:
  action: more-info
```

### Option 8: Mushroom Entity Card (Requires custom:mushroom-entity-card)

```yaml
type: custom:mushroom-entity-card
entity: sensor.anika_total_crying_episodes
name: Cries Today
icon: mdi:emoticon-sad
icon_color: |
  {% if states('sensor.anika_total_crying_episodes') | int >= 10 %}
    red
  {% elif states('sensor.anika_total_crying_episodes') | int >= 5 %}
    orange
  {% else %}
    green
  {% endif %}
primary_info: name
secondary_info: state
tap_action:
  action: more-info
```

---

## 📱 Complete Dashboard Example

### All-in-One Crying Dashboard

```yaml
type: vertical-stack
cards:
  # Big number at top
  - type: markdown
    content: |
      <ha-card>
        <div style="text-align: center; padding: 20px;">
          <h1 style="font-size: 3em; margin: 0;">
            {{ states('sensor.anika_total_crying_episodes') }}
          </h1>
          <p style="font-size: 1.2em; color: gray; margin: 5px 0;">
            Crying Episodes Today
          </p>
        </div>
      </ha-card>
  
  # Detailed stats
  - type: entities
    title: Details
    entities:
      - entity: sensor.anika_total_crying_episodes
        name: Total Duration
        type: attribute
        attribute: total_duration_minutes
        icon: mdi:clock
      
      - entity: sensor.anika_total_crying_episodes
        name: Average Per Episode
        type: attribute
        attribute: average_episode_duration
        icon: mdi:chart-line
      
      - entity: sensor.anika_total_crying_episodes
        name: Last Episode
        type: attribute
        attribute: last_episode
        icon: mdi:calendar-clock
  
  # Intensity breakdown
  - type: markdown
    content: |
      ### Intensity Breakdown
      {% set breakdown = state_attr('sensor.anika_total_crying_episodes', 'intensity_breakdown') %}
      {% if breakdown %}
      - **Light:** {{ breakdown.light | default(0) }} episodes
      - **Moderate:** {{ breakdown.moderate | default(0) }} episodes
      - **Intense:** {{ breakdown.intense | default(0) }} episodes
      {% else %}
      No data yet
      {% endif %}
  
  # Quick actions
  - type: horizontal-stack
    cards:
      - type: button
        entity: button.anika_crying_light
        name: Log Light Cry
        icon: mdi:emoticon-neutral
        tap_action:
          action: call-service
          service: button.press
          target:
            entity_id: button.anika_crying_light
      
      - type: button
        entity: button.anika_crying_moderate
        name: Log Moderate
        icon: mdi:emoticon-sad
        tap_action:
          action: call-service
          service: button.press
          target:
            entity_id: button.anika_crying_moderate
      
      - type: button
        entity: button.anika_crying_intense
        name: Log Intense
        icon: mdi:emoticon-cry
        tap_action:
          action: call-service
          service: button.press
          target:
            entity_id: button.anika_crying_intense
```

---

## 🔔 With Threshold Alerts

### Card with Visual Warning

```yaml
type: markdown
content: |
  <ha-card>
    <div style="padding: 20px; text-align: center;">
      {% set count = states('sensor.anika_total_crying_episodes') | int %}
      {% if count >= 10 %}
        <div style="background: rgba(255,0,0,0.2); padding: 15px; border-radius: 10px;">
          <h2 style="color: red; margin: 0;">⚠️ {{ count }} Cries</h2>
          <p style="margin: 5px 0;">High activity today</p>
        </div>
      {% elif count >= 5 %}
        <div style="background: rgba(255,165,0,0.2); padding: 15px; border-radius: 10px;">
          <h2 style="color: orange; margin: 0;">⚡ {{ count }} Cries</h2>
          <p style="margin: 5px 0;">Moderate activity</p>
        </div>
      {% else %}
        <div style="background: rgba(76,175,80,0.2); padding: 15px; border-radius: 10px;">
          <h2 style="color: green; margin: 0;">✅ {{ count }} Cries</h2>
          <p style="margin: 5px 0;">Normal activity</p>
        </div>
      {% endif %}
      
      <div style="margin-top: 15px;">
        <p style="color: gray;">
          Total: {{ state_attr('sensor.anika_total_crying_episodes', 'total_duration_minutes') }} minutes
        </p>
      </div>
    </div>
  </ha-card>
```

---

## 📈 With History Graph

### Card with 24-Hour Trend

```yaml
type: vertical-stack
cards:
  # Current count
  - type: entity
    entity: sensor.anika_total_crying_episodes
    name: Today's Total Cries
    icon: mdi:emoticon-cry-outline
  
  # History graph
  - type: history-graph
    title: Crying Episodes (24h)
    entities:
      - entity: sensor.anika_total_crying_episodes
        name: Episode Count
    hours_to_show: 24
    refresh_interval: 60
```

---

## 🎯 Mobile-Friendly Options

### Compact Mobile Card

```yaml
type: glance
columns: 2
entities:
  - entity: sensor.anika_total_crying_episodes
    name: Today
    icon: mdi:counter
  
  - entity: sensor.anika_total_crying_episodes
    name: Duration
    attribute: total_duration_minutes
    icon: mdi:clock
    
  - entity: sensor.anika_total_crying_episodes
    name: Average
    attribute: average_episode_duration
    icon: mdi:chart-line
  
  - entity: sensor.anika_crying_analysis
    name: Status
    icon: mdi:information
```

---

## 💡 Usage Tips

1. **Replace "anika"** with your baby's name (lowercase)
2. **Sensor entities:**
   - Main count: `sensor.BABYNAME_total_crying_episodes`
   - Analysis: `sensor.BABYNAME_crying_analysis`
3. **Customization:**
   - Adjust color thresholds in gauge cards
   - Change icons to your preference
   - Modify text and styling in markdown cards

---

## 🔄 Auto-Refresh

All cards automatically update when:
- Manual crying is logged via buttons
- Camera detects crying (if auto-tracking enabled)
- Service calls are made

**Refresh rate:** Real-time (1-2 seconds after activity)

---

## 📱 Add to Your Dashboard

1. Go to your Home Assistant dashboard
2. Click **Edit Dashboard** (top right)
3. Click **Add Card**
4. Choose **Manual** at the bottom
5. Paste any card YAML from above
6. Click **Save**

---

**Replace `anika` with your baby's name in all examples!**
