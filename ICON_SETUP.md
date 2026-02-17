# Baby Monitor Integration Icon Setup

## Icon Requirements

To add the baby monitor icon with white background to this Home Assistant integration:

### Option 1: Material Design Icon (Current Setup)
The manifest.json currently uses `mdi:baby-face-outline` as a fallback icon.

### Option 2: Custom Icon (Recommended)
1. Convert the baby monitor image to PNG format with white background
2. Create two sizes:
   - `icon.png` (60x60 pixels)
   - `icon@2x.png` (120x120 pixels)
3. Save both files in the root directory
4. Update manifest.json to reference the custom icon:

```json
{
  "icon": "mdi:baby-face-outline"
}
```

or remove the icon field to let Home Assistant auto-detect icon.png

### Manual Setup Steps:
1. Save the baby monitor SVG/image as PNG with white background
2. Resize to 60x60 and 120x120 pixels
3. Name them `icon.png` and `icon@2x.png`
4. Place in the integration root directory
5. Commit and push to GitHub

The icon will then appear in:
- Home Assistant integrations list
- HACS custom repositories
- Device & Services page
- Integration cards and entities

## Current Status
- ✅ Manifest updated with fallback Material Design icon
- ⏳ Custom PNG icon needs to be added manually
- ⏳ Icon files need to be created and committed to Git

The baby monitor icon with camera and happy baby face will be perfect for this integration!