"""Support for Siemens electricity meter sensors."""
import logging
import struct
from datetime import timedelta
from typing import Any

from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME, UnitOfEnergy, UnitOfPower
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import (
    CONF_HOST,
    CONF_PORT,
    CONF_SCAN_INTERVAL,
    CONF_SLAVE_ID,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_SLAVE_ID,
    DOMAIN,
    REGISTER_COUNT,
    REGISTER_ENERGY,
    REGISTER_POWER,
    SENSOR_ENERGY,
    SENSOR_POWER,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Siemens meter sensors from a config entry."""
    host = config_entry.data[CONF_HOST]
    port = config_entry.data[CONF_PORT]
    slave_id = config_entry.data.get(CONF_SLAVE_ID, DEFAULT_SLAVE_ID)
    scan_interval = timedelta(
        seconds=config_entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
    )
    meter_name = config_entry.data.get(CONF_NAME, "Siemens Meter")

    # Create Modbus client
    client = ModbusTcpClient(host=host, port=port)

    # Create data coordinator
    coordinator = SiemensMeterCoordinator(hass, client, slave_id, scan_interval)

    # Fetch initial data
    await coordinator.async_config_entry_first_refresh()

    # Create sensor entities
    entities = [
        SiemensMeterSensor(
            coordinator,
            meter_name,
            SENSOR_ENERGY,
            SensorDeviceClass.ENERGY,
            UnitOfEnergy.KILO_WATT_HOUR,
        ),
        SiemensMeterSensor(
            coordinator,
            meter_name,
            SENSOR_POWER,
            SensorDeviceClass.POWER,
            UnitOfPower.WATT,
        ),
    ]

    async_add_entities(entities)


class SiemensMeterCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Siemens meter data."""

    def __init__(
        self,
        hass: HomeAssistant,
        client: ModbusTcpClient,
        slave_id: int,
        scan_interval: timedelta,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="Siemens Meter",
            update_interval=scan_interval,
        )
        self.client = client
        self.slave_id = slave_id

    async def _async_update_data(self) -> dict[str, float | None]:
        """Fetch data from Siemens Modbus device."""

        def read_modbus():
            """Read data from Modbus (blocking I/O)."""
            if not self.client.connect():
                _LOGGER.error("Failed to connect to Siemens meter")
                return {}

            result = {}
            try:
                # Read energy register (FC3 4131)
                try:
                    response = self.client.read_holding_registers(
                        address=REGISTER_ENERGY,
                        count=REGISTER_COUNT,
                        slave=self.slave_id,
                    )

                    if response.isError():
                        _LOGGER.error("Error reading energy register")
                        result[SENSOR_ENERGY] = None
                    else:
                        # Parse 32-bit float from two 16-bit registers
                        bytes_data = struct.pack(">HH", *response.registers[:2])
                        value = struct.unpack(">f", bytes_data)[0]
                        result[SENSOR_ENERGY] = value

                except ModbusException as ex:
                    _LOGGER.error("Modbus exception reading energy: %s", ex)
                    result[SENSOR_ENERGY] = None
                except Exception as ex:
                    _LOGGER.error("Unexpected error reading energy: %s", ex)
                    result[SENSOR_ENERGY] = None

                # Read power register (FC3 4157)
                try:
                    response = self.client.read_holding_registers(
                        address=REGISTER_POWER,
                        count=REGISTER_COUNT,
                        slave=self.slave_id,
                    )

                    if response.isError():
                        _LOGGER.error("Error reading power register")
                        result[SENSOR_POWER] = None
                    else:
                        # Parse 32-bit float from two 16-bit registers
                        bytes_data = struct.pack(">HH", *response.registers[:2])
                        value = struct.unpack(">f", bytes_data)[0]
                        result[SENSOR_POWER] = value

                except ModbusException as ex:
                    _LOGGER.error("Modbus exception reading power: %s", ex)
                    result[SENSOR_POWER] = None
                except Exception as ex:
                    _LOGGER.error("Unexpected error reading power: %s", ex)
                    result[SENSOR_POWER] = None

            finally:
                self.client.close()

            return result

        # Run blocking Modbus I/O in executor
        data = await self.hass.async_add_executor_job(read_modbus)
        return data


class SiemensMeterSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Siemens meter sensor."""

    def __init__(
        self,
        coordinator: SiemensMeterCoordinator,
        meter_name: str,
        sensor_type: str,
        device_class: SensorDeviceClass,
        unit: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor_type = sensor_type
        self._meter_name = meter_name

        # Set up entity attributes
        self._attr_name = f"{meter_name} {sensor_type}"
        self._attr_unique_id = (
            f"siemens_meter_{meter_name}_{sensor_type}".lower().replace(" ", "_")
        )
        self._attr_device_class = device_class
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = unit

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        if self.coordinator.data:
            return self.coordinator.data.get(self._sensor_type)
        return None

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return (
            self.coordinator.last_update_success
            and self.coordinator.data is not None
            and self._sensor_type in self.coordinator.data
        )
