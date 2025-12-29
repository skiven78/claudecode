#!/bin/bash
# Diagnostic script for Siemens Electricity Meter integration

echo "=== Siemens Integration Diagnostics ==="
echo ""

echo "1. Checking if siemens_meter files exist..."
if [ -d "/config/custom_components/siemens_meter" ]; then
    echo "✅ Directory exists"
    ls -la /config/custom_components/siemens_meter/
else
    echo "❌ Directory does NOT exist!"
    exit 1
fi

echo ""
echo "2. Checking critical files..."
for file in __init__.py config_flow.py const.py manifest.json sensor.py strings.json; do
    if [ -f "/config/custom_components/siemens_meter/$file" ]; then
        echo "✅ $file exists"
    else
        echo "❌ $file MISSING!"
    fi
done

echo ""
echo "3. Checking manifest.json content..."
cat /config/custom_components/siemens_meter/manifest.json

echo ""
echo "4. Checking if async_setup exists in __init__.py..."
if grep -q "async def async_setup" /config/custom_components/siemens_meter/__init__.py; then
    echo "✅ async_setup function found"
else
    echo "❌ async_setup function MISSING!"
fi

echo ""
echo "5. Checking Home Assistant logs for siemens_meter errors..."
if [ -f "/config/home-assistant.log" ]; then
    echo "Recent errors:"
    grep -i "siemens" /config/home-assistant.log | tail -20
else
    echo "Log file not found"
fi

echo ""
echo "6. Checking loaded custom components..."
if [ -f "/config/home-assistant.log" ]; then
    grep "Loaded.*siemens_meter" /config/home-assistant.log | tail -5
fi

echo ""
echo "=== End of Diagnostics ==="
