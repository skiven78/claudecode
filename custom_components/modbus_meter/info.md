# Modbus Electricity Meter

Generisk Home Assistant integration för att läsa elmätare via Modbus TCP/IP med flexibel YAML-konfiguration.

## Funktioner

- **Flexibel konfiguration** - Stöd för alla typer av elmätare
- **Holding & Input registers** - Stöd för både registertyper
- **Olika datatyper** - 16-bit, 32-bit och 64-bit värden
- **Skalfaktorer** - Anpassa värden med skalfaktorer
- **Device classes** - Automatisk mappning av enheter och device classes

## Installation

1. Installera via HACS
2. Starta om Home Assistant
3. Lägg till konfiguration i `configuration.yaml`
4. Starta om Home Assistant igen

## Konfiguration

Exempel på konfiguration i `configuration.yaml`:

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
        device_class: power
```

## Stödda elmätare

- Eastron SDM630
- ABB B-Series
- Siemens elmätare
- Och alla andra Modbus-kompatibla elmätare

Se README för fler exempel och detaljerad dokumentation.
