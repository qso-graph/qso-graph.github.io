# solar-mcp

**Space weather integration — real-time solar conditions, forecasts, alerts, solar wind, X-ray flux, and HF band outlook.**

```bash
pip install solar-mcp
```

[GitHub](https://github.com/qso-graph/solar-mcp) · [PyPI](https://pypi.org/project/solar-mcp/)

---

## Tools

All 6 tools are **public** — no credentials needed. Data comes from NOAA Space Weather Prediction Center.

| Tool | Description |
|------|-------------|
| `solar_conditions` | Current SFI, Kp, NOAA scales, band outlook |
| `solar_forecast` | 27-day SFI and Kp forecast |
| `solar_alerts` | Active space weather alerts and warnings |
| `solar_wind` | Real-time DSCOVR L1 solar wind data |
| `solar_xray` | GOES X-ray flux and flare classification |
| `solar_band_outlook` | Per-band HF propagation assessment |

---

## Tool Reference

### solar_conditions

Get current solar conditions — SFI, Kp, and NOAA space weather scales. Includes an HF band outlook derived from current indices. No parameters.

Returns current SFI, Kp, NOAA R/S/G scales, and band-by-band propagation outlook.

### solar_forecast

Get the NOAA 27-day solar flux and geomagnetic forecast. No parameters.

Returns day-by-day forecast with predicted SFI and Kp values for the next 27 days.

### solar_alerts

Get active NOAA space weather alerts and warnings. Shows solar flare alerts, geomagnetic storm warnings, radiation storm alerts, and other SWPC bulletins. No parameters.

Returns list of active alerts with product ID, issue time, and message text.

### solar_wind

Get real-time DSCOVR L1 solar wind data. Shows interplanetary magnetic field (Bz component), solar wind speed, and proton density. Southward Bz (negative values) drives geomagnetic storms. No parameters.

Returns Bz (nT), Bt (nT), wind speed (km/s), density (p/cm^3), and geomagnetic storm assessment.

### solar_xray

Get GOES X-ray flux and solar flare classification. M and X class flares can cause HF radio blackouts (NOAA R1-R5 scale). No parameters.

Returns current flare class, X-ray flux, and HF impact assessment.

### solar_band_outlook

Get HF band-by-band propagation outlook based on current conditions. Derives an assessment for each band (160m through 6m) from current SFI and Kp. No parameters.

Returns per-band condition rating (Poor/Fair/Good/Excellent) with explanation, plus current SFI and Kp values.

---

## Data Sources

All data comes from [NOAA Space Weather Prediction Center](https://www.swpc.noaa.gov/) public JSON endpoints:

| Endpoint | Data |
|----------|------|
| 10cm-flux | Solar Flux Index (SFI) |
| planetary-k-index | Geomagnetic Kp index |
| solar-wind-mag-field | DSCOVR interplanetary Bz |
| plasma-5-minute | Solar wind speed and density |
| alerts | SWPC bulletins and warnings |
| GOES X-ray | Solar flare classification |
| 27-day forecast | Predicted SFI and Kp |

---

## No Credential Setup Needed

All NOAA SWPC endpoints are public. Just install and start using it.

---

## Mock Mode

```bash
SOLAR_MCP_MOCK=1 solar-mcp
```

## MCP Inspector

```bash
solar-mcp --transport streamable-http --port 8008
```
