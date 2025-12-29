"""Constants for the Modbus Electricity Meter integration."""

DOMAIN = "modbus_meter"

# Configuration keys
CONF_MODBUS_HOST = "host"
CONF_MODBUS_PORT = "port"
CONF_SLAVE_ID = "slave_id"
CONF_SCAN_INTERVAL = "scan_interval"
CONF_REGISTERS = "registers"

# Register configuration keys
CONF_REGISTER_ADDRESS = "address"
CONF_REGISTER_NAME = "name"
CONF_REGISTER_TYPE = "type"
CONF_REGISTER_COUNT = "count"
CONF_REGISTER_SCALE = "scale"
CONF_REGISTER_UNIT = "unit"
CONF_REGISTER_DEVICE_CLASS = "device_class"

# Register types
REGISTER_TYPE_HOLDING = "holding"
REGISTER_TYPE_INPUT = "input"

# Default values
DEFAULT_PORT = 502
DEFAULT_SLAVE_ID = 1
DEFAULT_SCAN_INTERVAL = 30
DEFAULT_REGISTER_COUNT = 2
DEFAULT_REGISTER_SCALE = 1.0

# Supported device classes
DEVICE_CLASS_ENERGY = "energy"
DEVICE_CLASS_POWER = "power"
DEVICE_CLASS_VOLTAGE = "voltage"
DEVICE_CLASS_CURRENT = "current"
DEVICE_CLASS_FREQUENCY = "frequency"
DEVICE_CLASS_POWER_FACTOR = "power_factor"
