# qrz-mcp

**QRZ.com integration — callsign lookup, DXCC resolution, and logbook access.**

```bash
pip install qrz-mcp
```

[GitHub](https://github.com/qso-graph/qrz-mcp) · [PyPI](https://pypi.org/project/qrz-mcp/)

---

## Tools

| Tool | Auth | Description |
|------|:----:|-------------|
| `qrz_lookup` | XML session | Look up a callsign (name, grid, DXCC, QSL info) |
| `qrz_dxcc` | XML session | Resolve a DXCC entity from callsign or code |
| `qrz_logbook_status` | API key | Get logbook statistics |
| `qrz_logbook_fetch` | API key | Query QSOs from a logbook |

---

## Tool Reference

### qrz_lookup

Look up a callsign on QRZ.com. Fields returned depend on subscription tier — free accounts get name and address only; XML Data subscription ($35.95/yr) provides full fields including grid, DXCC, license class, QSL info, and image URL.

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `persona` | str | Yes | Persona name configured in adif-mcp |
| `callsign` | str | Yes | Callsign to look up (e.g., W1AW) |

### qrz_dxcc

Resolve a DXCC entity from a callsign or numeric entity code.

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `persona` | str | Yes | Persona name configured in adif-mcp |
| `query` | str | Yes | Callsign (e.g., VP8PJ) or DXCC code (e.g., 291) |

Returns DXCC entity details: name, continent, CQ/ITU zones, coordinates.

### qrz_logbook_status

Get QRZ logbook statistics.

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `persona` | str | Yes | Persona name configured in adif-mcp |

Returns QSO count, confirmed count, DXCC entities, US states, date range.

### qrz_logbook_fetch

Query QSOs from a QRZ logbook with optional filters. Transparently paginates to collect up to `limit` records.

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `persona` | str | Yes | Persona name configured in adif-mcp |
| `band` | str | No | Filter by band (e.g., "20m") |
| `mode` | str | No | Filter by mode (e.g., "FT8") |
| `callsign` | str | No | Filter by contacted station |
| `dxcc` | int | No | Filter by DXCC entity code |
| `start_date` | str | No | Date range start (YYYY-MM-DD) |
| `end_date` | str | No | Date range end (YYYY-MM-DD) |
| `confirmed_only` | bool | No | Only confirmed QSOs. Default: false |
| `limit` | int | No | Maximum records. Default: 250 |

---

## Credential Setup

QRZ uses **dual authentication** — the XML API and Logbook API have separate credentials:

```bash
pip install adif-mcp

# XML API (callsign lookup + DXCC) — uses your QRZ login
adif-mcp creds set --persona ki7mt --provider qrz --password YOUR_QRZ_PASSWORD

# Logbook API — uses a separate API key from qrz.com/page/xml_data.html
adif-mcp creds set --persona ki7mt --provider qrz --api-key YOUR_QRZ_API_KEY
```

---

## Rate Limiting

QRZ enforces undocumented rate limits that can trigger **24-hour IP bans**. qrz-mcp protects you with:

- 500ms minimum delay between requests
- 35 requests/minute token bucket
- 60-second freeze after authentication failures
- 3600-second freeze if an IP ban is detected

### Response Cache

- Callsign lookups: cached 5 minutes
- DXCC lookups: cached 1 hour

---

## Mock Mode

```bash
QRZ_MCP_MOCK=1 qrz-mcp
```

## MCP Inspector

```bash
qrz-mcp --transport streamable-http --port 8002
```
