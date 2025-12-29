# Home Assistant Modbus Electricity Meter Integrations

Ett anpassat Home Assistant-plugin för att läsa elmätare via Modbus TCP/IP.

A custom Home Assistant integration for reading electricity meters via Modbus TCP/IP.

## Integrationer / Integrations

Detta repository innehåller två integrationer:

This repository contains two integrations:

### 1. Modbus Electricity Meter (`modbus_meter`)
Generisk Modbus-integration med konfiguration via `configuration.yaml`. Stödjer alla typer av elmätare med flexibel registerkonfiguration.

Generic Modbus integration configured via `configuration.yaml`. Supports all types of electricity meters with flexible register configuration.

### 2. Siemens Electricity Meter (`siemens_meter`)
Dedikerad integration för Siemens elmätare med UI-baserad konfiguration (config flow). Enkel installation direkt via Home Assistant gränssnittet.

Dedicated integration for Siemens electricity meters with UI-based configuration (config flow). Easy installation directly through Home Assistant interface.

## Funktioner / Features

### Modbus Electricity Meter
- Läser data från elmätare via Modbus TCP
- Stödjer både holding och input registers
- Konfigurerbar skanningsintervall
- Stöd för olika datatyper (16-bit, 32-bit float, 64-bit float)
- Stöd för skalfaktorer
- Automatisk enhets- och device class-mappning
- Konfiguration via `configuration.yaml`

### Siemens Electricity Meter
- UI-baserad konfiguration (config flow)
- Förkonfigurerade register för Siemens elmätare
- Energi (FC3 4131) och Effekt (FC3 4157)
- Automatisk enhetsmappning
- Enkel installation via Home Assistant UI

---

### Modbus Electricity Meter
- Reads data from electricity meters via Modbus TCP
- Supports both holding and input registers
- Configurable scan interval
- Support for different data types (16-bit, 32-bit float, 64-bit float)
- Support for scale factors
- Automatic unit and device class mapping
- Configuration via `configuration.yaml`

### Siemens Electricity Meter
- UI-based configuration (config flow)
- Pre-configured registers for Siemens meters
- Energy (FC3 4131) and Power (FC3 4157)
- Automatic unit mapping
- Easy installation via Home Assistant UI

## Installation

### HACS (Rekommenderat / Recommended)

1. Lägg till detta repository som en custom repository i HACS
2. Sök efter "Modbus Electricity Meter" eller "Siemens Electricity Meter" och installera
3. Starta om Home Assistant

### Manuell Installation / Manual Installation

#### För Modbus Electricity Meter
1. Kopiera mappen `custom_components/modbus_meter` till din Home Assistant `custom_components` katalog
2. Starta om Home Assistant

```bash
cd /config
mkdir -p custom_components
cp -r custom_components/modbus_meter /config/custom_components/
```

#### För Siemens Electricity Meter
1. Kopiera mappen `custom_components/siemens_meter` till din Home Assistant `custom_components` katalog
2. Starta om Home Assistant

```bash
cd /config
mkdir -p custom_components
cp -r custom_components/siemens_meter /config/custom_components/
```

## Konfiguration / Configuration

---

## 🔧 Siemens Electricity Meter - Config Flow Setup

Siemens-integrationen konfigureras enkelt via Home Assistant UI:

The Siemens integration is easily configured via Home Assistant UI:

### Installation / Setup

1. Gå till **Inställningar** → **Enheter & tjänster** → **Lägg till integration**
2. Sök efter "**Siemens Electricity Meter**"
3. Fyll i följande information:
   - **Namn**: Ett valfritt namn för din elmätare (t.ex. "Siemens Huvudmätare")
   - **IP-adress**: IP-adressen till din Siemens elmätare
   - **Port**: Modbus TCP port (standard: 502)
   - **Slave ID**: Modbus slave ID (standard: 1)
   - **Uppdateringsintervall**: Hur ofta data ska hämtas i sekunder (standard: 30)

4. Klicka på **Skicka**

The integration will automatically create two sensors:
- **Energy** (kWh) - Reading from holding register 4131
- **Power** (W) - Reading from holding register 4157

---

## 📝 Modbus Electricity Meter - YAML Configuration

Lägg till följande i din `configuration.yaml`:

Add the following to your `configuration.yaml`:

### Grundläggande exempel / Basic Example

```yaml
modbus_meter:
  - name: "Min Elmätare"
    host: 192.168.1.100
    port: 502
    slave_id: 1
    scan_interval: 30
    registers:
      - name: "Total Energy"
        address: 0
        type: input
        count: 2
        scale: 0.01
        unit: "kWh"
        device_class: energy

      - name: "Current Power"
        address: 12
        type: input
        count: 2
        scale: 1.0
        unit: "W"
        device_class: power

      - name: "Voltage L1"
        address: 20
        type: input
        count: 2
        scale: 0.1
        unit: "V"
        device_class: voltage
```

### Avancerat exempel / Advanced Example

```yaml
modbus_meter:
  - name: "Eastron SDM630"
    host: 192.168.1.100
    port: 502
    slave_id: 1
    scan_interval: 10
    registers:
      # Spänningar / Voltages
      - name: "Voltage L1"
        address: 0
        type: input
        count: 2
        scale: 1.0
        device_class: voltage

      - name: "Voltage L2"
        address: 2
        type: input
        count: 2
        scale: 1.0
        device_class: voltage

      - name: "Voltage L3"
        address: 4
        type: input
        count: 2
        scale: 1.0
        device_class: voltage

      # Strömmar / Currents
      - name: "Current L1"
        address: 6
        type: input
        count: 2
        scale: 1.0
        device_class: current

      - name: "Current L2"
        address: 8
        type: input
        count: 2
        scale: 1.0
        device_class: current

      - name: "Current L3"
        address: 10
        type: input
        count: 2
        scale: 1.0
        device_class: current

      # Effekt / Power
      - name: "Active Power Total"
        address: 52
        type: input
        count: 2
        scale: 1.0
        device_class: power

      # Energi / Energy
      - name: "Total Active Energy"
        address: 342
        type: input
        count: 2
        scale: 1.0
        device_class: energy

      # Frekvens / Frequency
      - name: "Frequency"
        address: 70
        type: input
        count: 2
        scale: 1.0
        device_class: frequency
```

## Konfigurationsparametrar / Configuration Parameters

### Huvudkonfiguration / Main Configuration

| Parameter | Obligatorisk / Required | Standard / Default | Beskrivning / Description |
|-----------|------------------------|-------------------|---------------------------|
| `name` | Nej / No | "Modbus Meter" | Namnet på elmätaren / Name of the meter |
| `host` | Ja / Yes | - | IP-adress till Modbus-enheten / IP address of Modbus device |
| `port` | Nej / No | 502 | Modbus TCP-port / Modbus TCP port |
| `slave_id` | Nej / No | 1 | Modbus slave ID / Modbus slave ID |
| `scan_interval` | Nej / No | 30 | Uppdateringsintervall i sekunder / Update interval in seconds |
| `registers` | Ja / Yes | - | Lista över register att läsa / List of registers to read |

### Registerkonfiguration / Register Configuration

| Parameter | Obligatorisk / Required | Standard / Default | Beskrivning / Description |
|-----------|------------------------|-------------------|---------------------------|
| `name` | Ja / Yes | - | Namn på sensorn / Sensor name |
| `address` | Ja / Yes | - | Modbus-registeradress / Modbus register address |
| `type` | Nej / No | "input" | Registertyp: "input" eller "holding" / Register type: "input" or "holding" |
| `count` | Nej / No | 2 | Antal register (1, 2 eller 4) / Number of registers (1, 2, or 4) |
| `scale` | Nej / No | 1.0 | Skalfaktor för värdet / Scale factor for the value |
| `unit` | Nej / No | - | Måttenhet / Unit of measurement |
| `device_class` | Nej / No | - | Device class för Home Assistant / Device class for Home Assistant |

### Registertyper / Register Types

- `count: 1` - 16-bit unsigned integer
- `count: 2` - 32-bit float (standard för de flesta elmätare / standard for most meters)
- `count: 4` - 64-bit float

### Device Classes

Stödda device classes / Supported device classes:
- `energy` - Energi (kWh)
- `power` - Effekt (W)
- `voltage` - Spänning (V)
- `current` - Ström (A)
- `frequency` - Frekvens (Hz)
- `power_factor` - Effektfaktor

## Vanliga elmätare / Common Electricity Meters

### Siemens Electricity Meters

För Siemens elmätare, använd den dedikerade `siemens_meter` integrationen med config flow (se ovan).

For Siemens electricity meters, use the dedicated `siemens_meter` integration with config flow (see above).

Om du vill använda den generiska `modbus_meter` integrationen istället:

If you want to use the generic `modbus_meter` integration instead:

```yaml
modbus_meter:
  - name: "Siemens Meter"
    host: 192.168.1.100
    port: 502
    slave_id: 1
    scan_interval: 30
    registers:
      - name: "Energy"
        address: 4131
        type: holding
        count: 2
        device_class: energy
        unit: "kWh"
      - name: "Power"
        address: 4157
        type: holding
        count: 2
        device_class: power
        unit: "W"
```

### Eastron SDM630

En populär 3-fas elmätare med Modbus-support.

```yaml
modbus_meter:
  - name: "Eastron SDM630"
    host: 192.168.1.100
    port: 502
    slave_id: 1
    scan_interval: 10
    registers:
      - name: "Voltage L1"
        address: 0
        count: 2
      - name: "Active Power Total"
        address: 52
        count: 2
        device_class: power
      - name: "Total Active Energy"
        address: 342
        count: 2
        device_class: energy
```

### ABB B-Series

```yaml
modbus_meter:
  - name: "ABB B23"
    host: 192.168.1.101
    port: 502
    slave_id: 1
    scan_interval: 30
    registers:
      - name: "Total Energy"
        address: 0x5000
        count: 2
        scale: 0.01
        device_class: energy
      - name: "Active Power"
        address: 0x5B00
        count: 2
        scale: 0.01
        device_class: power
```

## Felsökning / Troubleshooting

### Kan inte ansluta till elmätaren / Cannot connect to meter

1. Kontrollera att IP-adressen är korrekt / Check that the IP address is correct
2. Kontrollera att Modbus TCP är aktiverat på elmätaren / Verify Modbus TCP is enabled on the meter
3. Kontrollera nätverksanslutningen / Check network connection
4. Testa med ett Modbus-testverktyg som `modpoll` / Test with a Modbus testing tool like `modpoll`

```bash
# Testa anslutning / Test connection
modpoll -m tcp -a 1 -r 0 -c 2 -t 4 192.168.1.100
```

### Felaktiga värden / Incorrect values

1. Kontrollera registeradressen i elmätarens manual / Check register address in meter manual
2. Justera `scale`-faktorn / Adjust the `scale` factor
3. Kontrollera `count`-värdet (antal register) / Check the `count` value (number of registers)
4. Testa med `type: holding` istället för `input` / Try `type: holding` instead of `input`

### Sensorn visar "unavailable"

1. Kontrollera Home Assistant-loggar / Check Home Assistant logs
2. Öka `scan_interval` om mätaren är långsam / Increase `scan_interval` if the meter is slow
3. Kontrollera att Modbus slave ID är korrekt / Verify Modbus slave ID is correct

## Aktivera debug-loggning / Enable Debug Logging

Lägg till i `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.modbus_meter: debug
    custom_components.siemens_meter: debug
    pymodbus: debug
```

## Bidra / Contributing

Bidrag är välkomna! Skicka gärna pull requests eller öppna issues.

Contributions are welcome! Feel free to submit pull requests or open issues.

## Licens / License

MIT License

## Support

För support, öppna ett issue på GitHub.

For support, open an issue on GitHub.
