# Siemens Electricity Meter for Home Assistant

Home Assistant integration för Siemens elmätare via Modbus TCP/IP med enkel UI-konfiguration.

Home Assistant integration for Siemens electricity meters via Modbus TCP/IP with easy UI configuration.

## Funktioner / Features

- ⚡ **UI-baserad konfiguration** - Ingen YAML-konfiguration behövs
- 📊 **Förkonfigurerade register** - Automatiskt konfigurerad för Siemens elmätare
- 🔌 **Energiövervakning** - Läser energi (kWh) från register 4131
- 💡 **Effektmätning** - Läser effekt (W) från register 4157
- 🌐 **Modbus TCP** - Kommunicerar via Modbus TCP/IP
- 🔄 **Automatisk polling** - Konfigurerbart uppdateringsintervall

---

- ⚡ **UI-based configuration** - No YAML configuration needed
- 📊 **Pre-configured registers** - Automatically configured for Siemens meters
- 🔌 **Energy monitoring** - Reads energy (kWh) from register 4131
- 💡 **Power measurement** - Reads power (W) from register 4157
- 🌐 **Modbus TCP** - Communicates via Modbus TCP/IP
- 🔄 **Automatic polling** - Configurable update interval

## Installation

### Via HACS (Rekommenderat / Recommended)

#### Steg 1: Lägg till Custom Repository / Add Custom Repository
1. Öppna HACS i Home Assistant / Open HACS in Home Assistant
2. Klicka på **Integrations**
3. Klicka på menyn (⋮) i övre högra hörnet / Click the menu (⋮) in the top right corner
4. Välj **Custom repositories** / Select **Custom repositories**
5. Lägg till följande / Add the following:
   - **Repository**: `https://github.com/skiven78/claudecode`
   - **Category**: `Integration`
6. Klicka **ADD** / Click **ADD**

#### Steg 2: Installera / Install
1. I HACS, klicka på **+ EXPLORE & DOWNLOAD REPOSITORIES**
2. Sök efter "**Siemens**" eller "**Siemens Electricity Meter**"
3. Klicka på integrationen / Click on the integration
4. Klicka **DOWNLOAD**
5. **Starta om Home Assistant** / **Restart Home Assistant**

### Manuell Installation / Manual Installation

```bash
# Via SSH eller Terminal / Via SSH or Terminal
cd /config/custom_components
wget https://github.com/skiven78/claudecode/archive/refs/heads/claude/add-siemens-meter-integration-0AKus.zip
unzip claude-add-siemens-meter-integration-0AKus.zip
cp -r claudecode-*/custom_components/siemens_meter .
rm -rf claudecode-* claude-add-siemens-meter-integration-0AKus.zip
```

Efter installation, starta om Home Assistant.

After installation, restart Home Assistant.

## Konfiguration / Configuration

### Lägg till integrationen / Add the integration

1. Gå till **Inställningar** → **Enheter & tjänster** → **+ Lägg till integration**
2. Sök efter "**Siemens Electricity Meter**"
3. Fyll i följande information / Fill in the following information:
   - **Namn / Name**: Ett valfritt namn för din elmätare (t.ex. "Siemens Huvudmätare")
   - **IP-adress / IP Address**: IP-adressen till din Siemens elmätare
   - **Port**: 502 (standard för Modbus TCP / default for Modbus TCP)
   - **Slave ID**: 1 (standard / default)
   - **Uppdateringsintervall / Scan Interval**: 30 sekunder (rekommenderat / recommended)
4. Klicka på **Skicka** / Click **Submit**

### Sensorer / Sensors

Integrationen skapar automatiskt två sensorer:

The integration automatically creates two sensors:

- **Energy** (kWh) - Läser från holding register 4131 / Reads from holding register 4131
- **Power** (W) - Läser från holding register 4157 / Reads from holding register 4157

## Teknisk information / Technical Information

### Modbus-register / Modbus Registers

| Sensor | Register | Function Code | Datatyp / Data Type | Enhet / Unit |
|--------|----------|---------------|---------------------|--------------|
| Energy | 4131 | FC3 (Holding) | 32-bit float | kWh |
| Power | 4157 | FC3 (Holding) | 32-bit float | W |

### Systemkrav / System Requirements

- Home Assistant 2023.1.0 eller senare / or later
- Siemens elmätare med Modbus TCP-stöd / Siemens electricity meter with Modbus TCP support
- Nätverksanslutning mellan Home Assistant och elmätaren / Network connection between Home Assistant and meter

## Felsökning / Troubleshooting

### Kan inte ansluta till mätaren / Cannot connect to meter

**Kontrollera / Check:**
1. IP-adress och port är korrekt / IP address and port are correct
2. Modbus TCP är aktiverat på elmätaren / Modbus TCP is enabled on the meter
3. Brandvägg tillåter anslutningar / Firewall allows connections
4. Nätverksanslutning fungerar / Network connection works

**Testa anslutning / Test connection:**
```bash
# Installera modpoll
sudo apt-get install modpoll

# Testa läsning av energi-register
modpoll -m tcp -a 1 -r 4131 -c 2 -t 4 <IP-ADRESS>
```

### Sensorn visar "unavailable"

**Lösningar / Solutions:**
1. Kontrollera Home Assistant-loggar / Check Home Assistant logs:
   - Inställningar → System → Loggar
   - Sök efter "siemens_meter"
2. Öka uppdateringsintervallet / Increase scan interval (t.ex. till / e.g. to 60 sekunder / seconds)
3. Verifiera att Modbus Slave ID är korrekt / Verify Modbus Slave ID is correct

### Felaktiga värden / Incorrect values

**Kontrollera / Check:**
1. Registeradresser i elmätarens manual / Register addresses in meter manual
2. Att rätt data type används (32-bit float) / That correct data type is used (32-bit float)
3. Byteordning (byte order) / Byte order settings

## Aktivera debug-loggning / Enable Debug Logging

Lägg till i `configuration.yaml` / Add to `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.siemens_meter: debug
    pymodbus: debug
```

Starta om Home Assistant för att aktivera / Restart Home Assistant to activate.

## Exempel på automationer / Example Automations

### Notifiering vid hög effekt / Notification on high power

```yaml
automation:
  - alias: "Hög effektförbrukning"
    trigger:
      - platform: numeric_state
        entity_id: sensor.siemens_meter_power
        above: 5000
    action:
      - service: notify.mobile_app
        data:
          message: "Hög effektförbrukning: {{ states('sensor.siemens_meter_power') }} W"
```

### Daglig energirapport / Daily energy report

```yaml
automation:
  - alias: "Daglig energirapport"
    trigger:
      - platform: time
        at: "23:59:00"
    action:
      - service: notify.mobile_app
        data:
          message: "Dagens energiförbrukning: {{ states('sensor.siemens_meter_energy') }} kWh"
```

## Bidra / Contributing

Bidrag är välkomna! Skicka gärna pull requests eller öppna issues.

Contributions are welcome! Feel free to submit pull requests or open issues.

## Licens / License

MIT License

## Support

För support, öppna ett issue på GitHub.

For support, open an issue on GitHub.

## Tack till / Thanks to

- Home Assistant community
- pymodbus-utvecklare / pymodbus developers
