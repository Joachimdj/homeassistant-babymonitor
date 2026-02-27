# Camera Auto-Tracking Quick Setup Guide

## What is Camera Auto-Tracking?

Camera Auto-Tracking automatically detects when your baby is crying using your camera's built-in crying detection sensor. No manual button presses needed!

When enabled:
- ✅ Crying episodes are logged automatically
- ✅ Duration is calculated automatically  
- ✅ All sensors update in real-time
- ✅ Statistics track crying patterns over time

---

## Setup (3 Easy Steps)

### Step 1: Find Your Camera's Crying Sensor

1. Go to **Developer Tools → States** in Home Assistant
2. Search for your camera name (e.g., "baby camera", "nursery", etc.)
3. Look for a **binary_sensor** that detects crying:
   - `binary_sensor.baby_camera_crying_detected`
   - `binary_sensor.nursery_camera_sound`
   - `binary_sensor.wyze_cam_baby_crying`
   - Or similar name

**Example entities:**
- Nest Cam: `binary_sensor.nest_cam_baby_crying`
- Eufy: `binary_sensor.eufy_baby_monitor_crying`
- Wyze: `binary_sensor.wyze_cam_baby_sound`
- Generic: `binary_sensor.camera_baby_crying_detected`

**Can't find it?** Check your camera's integration documentation to see if it supports crying detection.

---

### Step 2: Enable Camera Auto-Tracking

1. Go to **Settings → Devices & Services**
2. Find **Baby Monitor** integration
3. Click **Configure** on your baby's entry (e.g., "Baby Monitor - Anika")
4. Scroll down to the camera options:
   - Toggle **Camera Auto-Tracking** to **ON**
   - Select your camera's crying sensor from the **Camera Crying Entity** dropdown
5. Click **Submit**

---

### Step 3: Verify It's Working

1. Test by making a crying sound near your camera (or wait for baby to cry)
2. Check the sensor updates:
   - Go to **Developer Tools → States**
   - Search for `sensor.{baby_name}_crying_analysis`
   - Verify it updates when crying is detected
3. Check your logs:
   - Go to **Settings → System → Logs**
   - Search for "Camera detected crying"
   - You should see automatic logging messages

---

## Dashboard Cards

Add these cards to monitor camera crying detection:

### Simple Status Card
```yaml
type: entities
title: Camera Crying Detection
entities:
  - entity: binary_sensor.baby_camera_crying_detected
    name: Camera Status
  - entity: sensor.anika_total_crying_episodes
    name: Total Episodes Today
  - entity: sensor.anika_crying_analysis
    name: Current Status
```

### Complete Monitoring Dashboard
```yaml
type: vertical-stack
cards:
  # Camera Feed
  - type: picture-entity
    entity: camera.baby_monitor
    name: Baby Monitor Camera
    show_state: true

  # Crying Status
  - type: glance
    title: Crying Detection
    entities:
      - entity: binary_sensor.baby_camera_crying_detected
        name: Camera
      - entity: sensor.anika_total_crying_episodes
        name: Episodes
      - entity: sensor.anika_total_crying_episodes
        name: Duration
        attribute: total_duration_minutes

  # History Graph
  - type: history-graph
    title: Crying History (24h)
    entities:
      - entity: binary_sensor.baby_camera_crying_detected
        name: Camera Detection
      - entity: sensor.anika_total_crying_episodes
        name: Episode Count
    hours_to_show: 24
```

---

## How It Works

**When Crying Starts:**
1. Camera detects crying sound
2. Camera's binary sensor changes to "on"
3. Integration automatically logs crying start
4. Start timestamp is recorded internally

**When Crying Stops:**
1. Camera stops detecting crying
2. Camera's binary sensor changes to "off"
3. Integration calculates duration (stop time - start time)
4. Final crying episode is logged with actual duration
5. All sensors update automatically

**What Gets Logged:**
- **Intensity:** Moderate (default, can be customized in advanced setup)
- **Duration:** Automatically calculated in minutes
- **Notes:** "Auto-detected by camera (X min)"
- **Timestamp:** Exact time crying started

---

## Troubleshooting

### Camera sensor not appearing in dropdown
- Verify your camera is integrated into Home Assistant
- Check if your camera supports crying detection
- Look for binary sensors with "crying", "sound", or "audio" in the name
- Restart Home Assistant and try again

### Crying not being detected
- Check camera sensitivity settings in your camera's app
- Verify the binary sensor state changes: Developer Tools → States
- Check integration logs: Settings → System → Logs → Search "babymonitor"
- Ensure Camera Auto-Tracking is enabled (toggle is ON)

### False detections (too many episodes)
- Adjust your camera's crying detection sensitivity (usually in camera app)
- Consider disabling auto-tracking during noisy times
- For advanced filtering, use manual automations (see CAMERA_CRYING_AUTOMATION.md)

### Duration always shows 0 or incorrect
- This is normal for the "start" entry (duration = 0)
- The "stop" entry should show actual duration
- Check the notes field: "Auto-detected by camera (X min)"
- Verify your camera stays in "on" state during crying (check history)

### Integration not updating after enabling
- Reload the integration: Settings → Devices & Services → Baby Monitor → Reload
- Or restart Home Assistant completely
- Check logs for any errors

---

## Advanced Features

For advanced users who want more control:

### Custom Automations
See [CAMERA_CRYING_AUTOMATION.md](CAMERA_CRYING_AUTOMATION.md) for manual automation setup with:
- Notifications when crying detected
- Smart home actions (lights, music pause)
- Intensity detection based on sound level
- Multi-camera support
- Time-of-day adjustments

### Disable Auto-Tracking Temporarily
1. Go to Settings → Devices & Services → Baby Monitor → Configure
2. Toggle **Camera Auto-Tracking** to OFF
3. Click Submit

The integration will stop monitoring camera state changes immediately.

---

## Configuration Options

### Camera Auto-Tracking (bool)
- **Default:** OFF
- **Description:** Enable automatic crying detection from camera
- **When to use:** When you have a camera with crying detection

### Camera Crying Entity (entity selector)
- **Default:** (empty)
- **Domain:** binary_sensor
- **Description:** Select your camera's crying detection sensor
- **Required:** Only if Camera Auto-Tracking is enabled

---

## FAQ

**Q: Does this work with all cameras?**
A: It works with any camera that provides a binary sensor for crying detection in Home Assistant. Check your camera integration's documentation.

**Q: Can I use multiple cameras?**
A: Currently, you can configure one camera per baby. For multi-camera setups, see the advanced automations guide.

**Q: Does this replace the manual buttons?**
A: No! You can use both. Auto-tracking is great for hands-free monitoring, but manual buttons are still useful for when you're not near the camera.

**Q: Will this drain my camera battery?**
A: No, the integration only reads the camera's existing crying detection sensor. It doesn't control the camera or increase its power usage.

**Q: Can I customize the crying intensity?**
A: The built-in feature uses "moderate" intensity. For custom intensity based on sound level, see the manual automations guide.

**Q: What if I don't have a crying detection camera?**
A: You can still use all the manual logging features (buttons and services). Camera auto-tracking is an optional enhancement.

---

## Next Steps

Once camera auto-tracking is working:

1. **Add Dashboard Cards** - Use the examples above to visualize crying patterns
2. **Review Statistics** - Check long-term trends: sensor.{baby}_total_crying_episodes
3. **Set Up Notifications** - Use automations to get alerts (see advanced guide)
4. **Explore Other Features** - Temperature tracking, feeding logs, sleep monitoring, etc.

---

## Support

For issues or questions:
- Check Home Assistant logs: Settings → System → Logs
- Review camera integration documentation
- See [CAMERA_CRYING_AUTOMATION.md](CAMERA_CRYING_AUTOMATION.md) for advanced setup
- Report issues on GitHub

---

**Enjoy hands-free baby monitoring!** 🎥👶
