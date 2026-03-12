# hamqth-mcp

**HamQTH.com integration — callsign lookup, DX cluster spots, Reverse Beacon Network, DXCC resolution, and more.**

```bash
pip install hamqth-mcp
```

[GitHub](https://github.com/qso-graph/hamqth-mcp) · [PyPI](https://pypi.org/project/hamqth-mcp/)

---

## Tools

| Tool | Auth | Description |
|------|:----:|-------------|
| `hamqth_lookup` | Yes | Look up a callsign (free, no subscription) |
| `hamqth_dxcc` | No | Resolve DXCC entity from callsign or code |
| `hamqth_bio` | Yes | Fetch operator biography |
| `hamqth_activity` | Yes | Recent DX cluster, RBN, and logbook activity |
| `hamqth_dx_spots` | No | Live DX cluster spots — filter by band and/or callsign |
| `hamqth_rbn` | No | Reverse Beacon Network decodes — filter by band, mode, continent, callsign |
| `hamqth_verify_qso` | No | Verify a QSO via HamQTH SAVP protocol |

---

## Tool Reference

### hamqth_lookup

Look up a callsign on HamQTH. Returns name, grid, DXCC, coordinates, QSL preferences, and more. **Free** — no subscription required, just a HamQTH account. Field availability depends on what the operator has published.

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `persona` | str | Yes | Persona name configured in qso-graph-auth |
| `callsign` | str | Yes | Callsign to look up (e.g., OK2CQR) |

### hamqth_dxcc

Resolve a DXCC entity from a callsign or ADIF entity code. Public endpoint — no authentication required.

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `query` | str | Yes | Callsign (e.g., VP8PJ) or ADIF entity code (e.g., 291) |

Returns DXCC entity details: name, continent, CQ/ITU zones, coordinates.

### hamqth_bio

Fetch an operator's biography from HamQTH.

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `persona` | str | Yes | Persona name configured in qso-graph-auth |
| `callsign` | str | Yes | Callsign to look up |

Returns callsign and biography text (HTML stripped).

### hamqth_activity

Get recent DX cluster, RBN, and logbook activity for a callsign.

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `persona` | str | Yes | Persona name configured in qso-graph-auth |
| `callsign` | str | Yes | Callsign to check |

Returns list of recent activity items (spots, RBN decodes, logbook entries).

### hamqth_dx_spots

Live DX cluster spots from HamQTH. Public endpoint — no authentication required. Spots update every ~15 seconds.

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `limit` | int | No | Number of spots to return (default 60, max 200) |
| `band` | str | No | ADIF band filter (e.g., "20M", "40M") |
| `call` | str | No | Callsign filter — matches spotted call or spotter (e.g., "3Y0K") |

When `call` is provided, automatically fetches the maximum 200 spots and filters client-side. Case-insensitive substring match.

### hamqth_rbn

Reverse Beacon Network decodes from HamQTH. Public endpoint — no authentication required.

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `band` | str | No | ADIF band numbers, comma-separated (e.g., "20,40") |
| `mode` | str | No | Filter by mode (CW, RTTY, PSK31, PSK63) |
| `cont` | str | No | Spotted station's continent (e.g., "EU", "NA") |
| `fromcont` | str | No | Receiver/skimmer continent (e.g., "EU", "NA") |
| `age` | int | No | Maximum age in seconds |
| `call` | str | No | Callsign filter — matches spotted station (e.g., "3Y0K") |

Returns decodes with call, freq, mode, age, and listener dB values (which skimmers heard the station and at what SNR).

### hamqth_verify_qso

Verify a QSO via the HamQTH SAVP protocol. Public endpoint — no authentication required.

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `mycall` | str | Yes | Your callsign (e.g., "KI7MT") |
| `hiscall` | str | Yes | Other station's callsign (e.g., "OK2CQR") |
| `date` | str | Yes | QSO date in YYYYMMDD format (e.g., "20260305") |
| `band` | str | Yes | Band (e.g., "20M", "40M") |

---

## Credential Setup

HamQTH is **free** — no paid subscription needed. Just create an account at [hamqth.com](https://www.hamqth.com/):

```bash
pip install qso-graph-auth
qso-auth creds set ki7mt hamqth
```

---

## Known Quirks

- **Free alternative to QRZ** — created by Petr, OK2CQR. No paid tier required for callsign lookups.
- **XML session auth** — sessions refresh every 55 minutes automatically.
- **DXCC endpoint is public** — uses a separate JSON API, completely independent of the XML session.

---

## Mock Mode

```bash
HAMQTH_MCP_MOCK=1 hamqth-mcp
```

## MCP Inspector

```bash
hamqth-mcp --transport streamable-http --port 8005
```
