# Siemens Electricity Meter

Dedikerad Home Assistant integration för Siemens elmätare med enkel UI-baserad konfiguration.

## Funktioner

- **UI-baserad konfiguration** - Ingen YAML-konfiguration behövs
- **Förkonfigurerade register** - Automatiskt konfigurerad för Siemens elmätare
- **Energiövervakning** - Läser energi (kWh) från register 4131
- **Effektmätning** - Läser effekt (W) från register 4157
- **Modbus TCP** - Kommunicerar via Modbus TCP/IP

## Installation

1. Installera via HACS
2. Starta om Home Assistant
3. Gå till Inställningar → Enheter & tjänster → Lägg till integration
4. Sök efter "Siemens Electricity Meter"
5. Fyll i IP-adress och port för din elmätare

## Konfiguration

Vid installation frågar integrationen efter:
- **Namn** - Ett valfritt namn för din elmätare
- **IP-adress** - Elmätarens IP-adress
- **Port** - Modbus TCP port (standard: 502)
- **Slave ID** - Modbus slave ID (standard: 1)
- **Uppdateringsintervall** - Hur ofta data hämtas (standard: 30 sekunder)

## Sensorer

Integrationen skapar automatiskt två sensorer:
- **Energy** - Energiförbrukning i kWh
- **Power** - Aktuell effekt i W

## Teknisk information

- Använder Modbus holding registers (FC3)
- Energi: Register 4131
- Effekt: Register 4157
- Dataformat: 32-bit float (2 registers)
