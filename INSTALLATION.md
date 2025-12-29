# Siemens Electricity Meter - Installationsguide

## Metod 1: Installation via HACS (Enklast)

### Steg 1: Lägg till Custom Repository i HACS
1. Öppna Home Assistant
2. Gå till **HACS** (i sidomenyn)
3. Klicka på **Integrations**
4. Klicka på de tre prickarna (⋮) uppe till höger
5. Välj **Custom repositories**
6. I formuläret som dyker upp:
   - **Repository**: `https://github.com/skiven78/claudecode`
   - **Category**: Välj `Integration`
7. Klicka på **ADD**

### Steg 2: Installera Siemens Electricity Meter
1. Fortfarande i HACS → Integrations
2. Klicka på **+ EXPLORE & DOWNLOAD REPOSITORIES** (blå knapp nere till höger)
3. I sökfältet, skriv: `Siemens`
4. Du borde se **Siemens Electricity Meter**
5. Klicka på den
6. Klicka på **DOWNLOAD** (eller **DOWNLOAD THIS REPOSITORY WITH HACS**)
7. Välj senaste versionen
8. Klicka **DOWNLOAD**
9. **VIKTIGT**: Starta om Home Assistant
   - Gå till **Inställningar** → **System** → **Starta om**
   - Vänta tills Home Assistant har startat om (kan ta 1-2 minuter)

### Steg 3: Lägg till Integrationen
1. Efter omstart, gå till **Inställningar** → **Enheter & tjänster**
2. Klicka på **+ LÄGG TILL INTEGRATION** (nere till höger)
3. Sök efter: `Siemens`
4. Du borde nu se **Siemens Electricity Meter**
5. Klicka på den och följ konfigurationsguiden

---

## Metod 2: Manuell Installation (om HACS inte fungerar)

### Via SSH eller Terminal:

```bash
# 1. SSH till Home Assistant eller öppna Terminal i File Editor

# 2. Gå till config-katalogen
cd /config

# 3. Skapa custom_components om den inte finns
mkdir -p custom_components

# 4. Ladda ner integrationen
cd custom_components
wget https://github.com/skiven78/claudecode/archive/refs/heads/claude/add-siemens-meter-integration-0AKus.zip
unzip claude/add-siemens-meter-integration-0AKus.zip
cp -r claudecode-claude-add-siemens-meter-integration-0AKus/custom_components/siemens_meter .
rm -rf claudecode-claude-add-siemens-meter-integration-0AKus*

# 5. Kontrollera att filerna finns
ls -la siemens_meter/
```

### Via File Editor (Enklast för manuell installation):

1. Installera **File Editor** addon i Home Assistant om du inte har det
2. Ladda ner ZIP-filen från GitHub:
   - Gå till: `https://github.com/skiven78/claudecode`
   - Klicka på **Code** → **Download ZIP**
3. Packa upp ZIP-filen på din dator
4. Kopiera mappen `custom_components/siemens_meter` till Home Assistant:
   - Öppna File Editor
   - Navigera till `/config/custom_components/`
   - Skapa mappen om den inte finns
   - Ladda upp hela `siemens_meter` mappen

### Efter manuell installation:

1. **Starta om Home Assistant**
   - Inställningar → System → Starta om
2. Vänta tills systemet har startat om (1-2 minuter)
3. Gå till **Inställningar** → **Enheter & tjänster** → **+ LÄGG TILL INTEGRATION**
4. Sök efter `Siemens`

---

## Felsökning

### "Kan inte hitta Siemens i Lägg till integration"

**Orsak**: Integrationen är inte installerad än eller Home Assistant har inte startat om.

**Lösning**:
1. Kontrollera att filen finns: `/config/custom_components/siemens_meter/manifest.json`
2. Kontrollera Home Assistant loggar:
   - Inställningar → System → Loggar
   - Sök efter "siemens_meter"
3. Starta om Home Assistant igen

### "HACS visar inte Siemens Electricity Meter"

**Lösning**:
1. Kontrollera att du lagt till repository som **Custom repository** först
2. Tryck på F5/uppdatera sidan i webbläsaren
3. Stäng och öppna HACS igen
4. Om det fortfarande inte fungerar, använd manuell installation

### "Integration läser inte värden från mätaren"

**Lösning**:
1. Kontrollera att IP-adress och port är korrekt
2. Kontrollera att Modbus TCP är aktiverat på mätaren
3. Testa anslutning med verktyg som `modpoll`
4. Aktivera debug-loggning (se README)

---

## Konfiguration efter installation

När du väl har lagt till integrationen, fyll i:

- **Namn**: T.ex. "Siemens Huvudmätare"
- **IP-adress**: Din elmätares IP (t.ex. 192.168.1.100)
- **Port**: 502 (standard för Modbus TCP)
- **Slave ID**: 1 (om inte annat är konfigurerat)
- **Uppdateringsintervall**: 30 sekunder (rekommenderat)

Integrationen skapar automatiskt två sensorer:
- **Energy** (kWh) - från register 4131
- **Power** (W) - från register 4157
