"""Support for Modbus electricity meter sensors."""
import logging
import struct
from datetime import timedelta
from typing import Any

import voluptuous as vol
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException

from homeassistant.components.sensor import (
    PLATFORM_SCHEMA,
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import (
    CONF_NAME,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfFrequency,
    UnitOfPower,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import (
    CONF_MODBUS_HOST,
    CONF_MODBUS_PORT,
    CONF_REGISTER_ADDRESS,
    CONF_REGISTER_COUNT,
    CONF_REGISTER_DEVICE_CLASS,
    CONF_REGISTER_NAME,
    CONF_REGISTER_SCALE,
    CONF_REGISTER_TYPE,
    CONF_REGISTER_UNIT,
    CONF_REGISTERS,
    CONF_SCAN_INTERVAL,
    CONF_SLAVE_ID,
    DEFAULT_PORT,
    DEFAULT_REGISTER_COUNT,
    DEFAULT_REGISTER_SCALE,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_SLAVE_ID,
    DEVICE_CLASS_CURRENT,
    DEVICE_CLASS_ENERGY,
    DEVICE_CLASS_FREQUENCY,
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_POWER_FACTOR,
    DEVICE_CLASS_VOLTAGE,
    REGISTER_TYPE_HOLDING,
    REGISTER_TYPE_INPUT,
)

_LOGGER = logging.getLogger(__name__)

REGISTER_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_REGISTER_NAME): cv.string,
        vol.Required(CONF_REGISTER_ADDRESS): cv.positive_int,
        vol.Optional(CONF_REGISTER_TYPE, default=REGISTER_TYPE_INPUT): vol.In(
            [REGISTER_TYPE_HOLDING, REGISTER_TYPE_INPUT]
        ),
        vol.Optional(CONF_REGISTER_COUNT, default=DEFAULT_REGISTER_COUNT): vol.In(
            [1, 2, 4]
        ),
        vol.Optional(CONF_REGISTER_SCALE, default=DEFAULT_REGISTER_SCALE): vol.Coerce(
            float
        ),
        vol.Optional(CONF_REGISTER_UNIT): cv.string,
        vol.Optional(CONF_REGISTER_DEVICE_CLASS): cv.string,
    }
)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_MODBUS_HOST): cv.string,
        vol.Optional(CONF_MODBUS_PORT, default=DEFAULT_PORT): cv.port,
        vol.Optional(CONF_SLAVE_ID, default=DEFAULT_SLAVE_ID): cv.positive_int,
        vol.Optional(
            CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL
        ): cv.positive_int,
        vol.Required(CONF_REGISTERS): vol.All(cv.ensure_list, [REGISTER_SCHEMA]),
        vol.Optional(CONF_NAME, default="Modbus Meter"): cv.string,
    }
)


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the Modbus electricity meter sensor platform."""
    host = config[CONF_MODBUS_HOST]
    port = config[CONF_MODBUS_PORT]
    slave_id = config[CONF_SLAVE_ID]
    scan_interval = timedelta(seconds=config[CONF_SCAN_INTERVAL])
    registers = config[CONF_REGISTERS]
    meter_name = config[CONF_NAME]

    # Create Modbus client
    client = ModbusTcpClient(host=host, port=port)

    # Create data coordinator
    coordinator = ModbusMeterCoordinator(
        hass, client, slave_id, registers, scan_interval
    )

    # Fetch initial data
    await coordinator.async_config_entry_first_refresh()

    # Create sensor entities
    entities = []
    for register_config in registers:
        entities.append(
            ModbusMeterSensor(
                coordinator,
                meter_name,
                register_config,
            )
        )

    async_add_entities(entities)


class ModbusMeterCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Modbus data."""

    def __init__(
        self,
        hass: HomeAssistant,
        client: ModbusTcpClient,
        slave_id: int,
        registers: list[dict[str, Any]],
        scan_interval: timedelta,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="Modbus Meter",
            update_interval=scan_interval,
        )
        self.client = client
        self.slave_id = slave_id
        self.registers = registers

    async def _async_update_data(self) -> dict[str, float | None]:
        """Fetch data from Modbus device."""
        data = {}

        def read_modbus():
            """Read data from Modbus (blocking I/O)."""
            if not self.client.connect():
                _LOGGER.error("Failed to connect to Modbus device")
                return {}

            result = {}
            try:
                for register in self.registers:
                    register_name = register[CONF_REGISTER_NAME]
                    address = register[CONF_REGISTER_ADDRESS]
                    register_type = register[CONF_REGISTER_TYPE]
                    count = register[CONF_REGISTER_COUNT]
                    scale = register[CONF_REGISTER_SCALE]

                    try:
                        if register_type == REGISTER_TYPE_HOLDING:
                            response = self.client.read_holding_registers(
                                address=address, count=count, slave=self.slave_id
                            )
                        else:  # INPUT
                            response = self.client.read_input_registers(
                                address=address, count=count, slave=self.slave_id
                            )

                        if response.isError():
                            _LOGGER.error(
                                "Error reading register %s at address %s",
                                register_name,
                                address,
                            )
                            result[register_name] = None
                            continue

                        # Parse the register value based on count
                        if count == 1:
                            # 16-bit unsigned integer
                            value = response.registers[0]
                        elif count == 2:
                            # 32-bit float or integer
                            # Combine two 16-bit registers into 32-bit value
                            bytes_data = struct.pack(">HH", *response.registers[:2])
                            value = struct.unpack(">f", bytes_data)[0]
                        elif count == 4:
                            # 64-bit float
                            bytes_data = struct.pack(">HHHH", *response.registers[:4])
                            value = struct.unpack(">d", bytes_data)[0]
                        else:
                            value = response.registers[0]

                        # Apply scale factor
                        result[register_name] = value * scale

                    except ModbusException as ex:
                        _LOGGER.error(
                            "Modbus exception reading %s: %s", register_name, ex
                        )
                        result[register_name] = None
                    except Exception as ex:
                        _LOGGER.error(
                            "Unexpected error reading %s: %s", register_name, ex
                        )
                        result[register_name] = None

            finally:
                self.client.close()

            return result

        # Run blocking Modbus I/O in executor
        data = await self.hass.async_add_executor_job(read_modbus)
        return data


class ModbusMeterSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Modbus electricity meter sensor."""

    def __init__(
        self,
        coordinator: ModbusMeterCoordinator,
        meter_name: str,
        register_config: dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._register_name = register_config[CONF_REGISTER_NAME]
        self._meter_name = meter_name

        # Set up entity attributes
        self._attr_name = f"{meter_name} {self._register_name}"
        self._attr_unique_id = (
            f"modbus_meter_{meter_name}_{self._register_name}".lower().replace(
                " ", "_"
            )
        )

        # Set unit of measurement
        if CONF_REGISTER_UNIT in register_config:
            self._attr_native_unit_of_measurement = register_config[
                CONF_REGISTER_UNIT
            ]

        # Set device class
        if CONF_REGISTER_DEVICE_CLASS in register_config:
            device_class_str = register_config[CONF_REGISTER_DEVICE_CLASS]
            self._attr_device_class = self._map_device_class(device_class_str)
            self._attr_state_class = SensorStateClass.MEASUREMENT

            # Set default unit based on device class if not specified
            if CONF_REGISTER_UNIT not in register_config:
                self._attr_native_unit_of_measurement = self._get_default_unit(
                    device_class_str
                )

    def _map_device_class(self, device_class_str: str) -> SensorDeviceClass | None:
        """Map string device class to SensorDeviceClass."""
        mapping = {
            DEVICE_CLASS_ENERGY: SensorDeviceClass.ENERGY,
            DEVICE_CLASS_POWER: SensorDeviceClass.POWER,
            DEVICE_CLASS_VOLTAGE: SensorDeviceClass.VOLTAGE,
            DEVICE_CLASS_CURRENT: SensorDeviceClass.CURRENT,
            DEVICE_CLASS_FREQUENCY: SensorDeviceClass.FREQUENCY,
            DEVICE_CLASS_POWER_FACTOR: SensorDeviceClass.POWER_FACTOR,
        }
        return mapping.get(device_class_str)

    def _get_default_unit(self, device_class_str: str) -> str | None:
        """Get default unit for device class."""
        mapping = {
            DEVICE_CLASS_ENERGY: UnitOfEnergy.KILO_WATT_HOUR,
            DEVICE_CLASS_POWER: UnitOfPower.WATT,
            DEVICE_CLASS_VOLTAGE: UnitOfElectricPotential.VOLT,
            DEVICE_CLASS_CURRENT: UnitOfElectricCurrent.AMPERE,
            DEVICE_CLASS_FREQUENCY: UnitOfFrequency.HERTZ,
            DEVICE_CLASS_POWER_FACTOR: None,
        }
        return mapping.get(device_class_str)

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        if self.coordinator.data:
            return self.coordinator.data.get(self._register_name)
        return None

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return (
            self.coordinator.last_update_success
            and self.coordinator.data is not None
            and self._register_name in self.coordinator.data
        )
