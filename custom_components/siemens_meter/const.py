"""Constants for the Siemens Electricity Meter integration."""

DOMAIN = "siemens_meter"

# Configuration keys
CONF_HOST = "host"
CONF_PORT = "port"
CONF_SLAVE_ID = "slave_id"
CONF_SCAN_INTERVAL = "scan_interval"

# Default values
DEFAULT_PORT = 502
DEFAULT_SLAVE_ID = 1
DEFAULT_SCAN_INTERVAL = 30

# Siemens meter register addresses (Modbus holding registers)
REGISTER_ENERGY = 4131  # FC3 4131 - Energy
REGISTER_POWER = 4157   # FC3 4157 - Power

# Register count (32-bit values = 2 registers)
REGISTER_COUNT = 2

# Sensor names
SENSOR_ENERGY = "Energy"
SENSOR_POWER = "Power"
