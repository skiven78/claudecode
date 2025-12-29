#!/bin/bash
# Installation script for Siemens Electricity Meter integration

echo "=== Installing Siemens Electricity Meter Integration ==="
echo ""

# Remove old installation
echo "1. Removing old installation..."
rm -rf /config/custom_components/siemens_meter
rm -rf /config/custom_components/modbus_meter

# Create directory
echo "2. Creating directory..."
mkdir -p /config/custom_components/siemens_meter
mkdir -p /config/custom_components/siemens_meter/translations

# Download files
echo "3. Downloading files..."
cd /config/custom_components/siemens_meter

BASE_URL="https://raw.githubusercontent.com/skiven78/claudecode/claude/add-siemens-meter-integration-0AKus/custom_components/siemens_meter"

echo "   - manifest.json"
wget -q -O manifest.json "$BASE_URL/manifest.json"

echo "   - __init__.py"
wget -q -O __init__.py "$BASE_URL/__init__.py"

echo "   - config_flow.py"
wget -q -O config_flow.py "$BASE_URL/config_flow.py"

echo "   - const.py"
wget -q -O const.py "$BASE_URL/const.py"

echo "   - sensor.py"
wget -q -O sensor.py "$BASE_URL/sensor.py"

echo "   - strings.json"
wget -q -O strings.json "$BASE_URL/strings.json"

echo "   - info.md"
wget -q -O info.md "$BASE_URL/info.md"

echo "   - translations/en.json"
wget -q -O translations/en.json "$BASE_URL/translations/en.json"

# Verify files
echo ""
echo "4. Verifying installation..."
REQUIRED_FILES="__init__.py config_flow.py const.py manifest.json sensor.py strings.json info.md translations/en.json"
ALL_PRESENT=true

for file in $REQUIRED_FILES; do
    if [ -f "$file" ]; then
        echo "   ✅ $file"
    else
        echo "   ❌ $file MISSING!"
        ALL_PRESENT=false
    fi
done

echo ""
if [ "$ALL_PRESENT" = true ]; then
    echo "✅ Installation successful!"
    echo ""
    echo "Next steps:"
    echo "1. Restart Home Assistant"
    echo "2. Go to Settings → Devices & Services → Add Integration"
    echo "3. Search for 'Siemens Electricity Meter'"
    echo ""
else
    echo "❌ Installation failed - some files are missing!"
    exit 1
fi

# Show file sizes
echo "Installed files:"
ls -lh /config/custom_components/siemens_meter/

echo ""
echo "=== Installation Complete ==="
