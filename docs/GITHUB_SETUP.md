# GitHub Repository Setup Guide

## To publish this to GitHub:

### 1. Create a GitHub Repository

1. Go to [GitHub](https://github.com) and log in
2. Click "New repository" or go to [Create New Repository](https://github.com/new)
3. Repository name: `homeassistant-babymonitor`
4. Description: "Baby Monitor integration for Home Assistant - Track diaper changes, feeding, sleep patterns, and more"
5. Make it **Public** (required for HACS)
6. **Don't** initialize with README (we already have one)
7. Click "Create repository"

### 2. Push to GitHub

```bash
# If you haven't set the remote origin yet:
git remote add origin https://github.com/YOUR_USERNAME/homeassistant-babymonitor.git

# Push to GitHub
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username.

### 3. Enable GitHub Pages (Optional)

1. Go to your repository Settings
2. Scroll down to "Pages"
3. Source: "Deploy from a branch"
4. Branch: `main` / `root`
5. This will make your README.md visible as a website

### 4. Create a Release (Recommended)

1. Go to your repository on GitHub
2. Click "Releases" → "Create a new release"
3. Tag: `v1.0.0`
4. Title: `Initial Release - Baby Monitor v1.0.0`
5. Description: Copy from the commit message
6. Click "Publish release"

## Installation for Users:

### Via HACS (Recommended):
1. HACS → Integrations → ⋮ → Custom repositories
2. Add: `https://github.com/Joachimdj/homeassistant-babymonitor`
3. Category: Integration
4. Install "Baby Monitor"

### Via Git Clone:
```bash
cd /config/custom_components/
git clone https://github.com/Joachimdj/homeassistant-babymonitor.git babymonitor
```

### Manual Download:
1. Download ZIP from GitHub
2. Extract all Python files to `/config/custom_components/babymonitor/`

## Repository Features:

✅ **HACS Compatible** - Users can install via HACS  
✅ **MIT Licensed** - Open source and free to use  
✅ **Comprehensive Documentation** - README with examples  
✅ **Example Files** - Lovelace dashboards and automations  
✅ **Git Ready** - Proper .gitignore and structure  
✅ **Release Ready** - Tagged versions for stability  

## File Structure:
```
homeassistant-babymonitor/          # Repository root
├── __init__.py                     # Main integration setup
├── manifest.json                   # Integration metadata
├── const.py                        # Constants
├── config_flow.py                  # Configuration UI
├── storage.py                      # Data storage
├── sensor.py                       # Sensor entities
├── button.py                       # Button entities
├── services.py                     # Service implementations
├── services.yaml                   # Service definitions
├── README.md                       # Main documentation
├── LICENSE                         # MIT License
├── hacs.json                       # HACS configuration
├── .gitignore                      # Git ignore file
├── lovelace_examples.yaml          # Dashboard examples
└── example_automations.yaml        # Automation examples
```

## Next Steps:

1. **Create the GitHub repo** and push your code
2. **Test the installation** in your own Home Assistant
3. **Submit to HACS** (optional) - [HACS Default Repositories](https://github.com/hacs/default)
4. **Share with the community** on [Home Assistant Community Forum](https://community.home-assistant.io/)

Your integration is now ready for distribution! 🎉