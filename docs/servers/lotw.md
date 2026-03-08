# lotw-mcp

**Logbook of The World integration — confirmations, QSOs, DXCC credits, and user activity.**

```bash
pip install lotw-mcp
```

[GitHub](https://github.com/qso-graph/lotw-mcp) · [PyPI](https://pypi.org/project/lotw-mcp/)

---

## Tools

| Tool | Auth | Description |
|------|:----:|-------------|
| `lotw_confirmations` | Yes | Query confirmed QSL records |
| `lotw_qsos` | Yes | Query all uploaded QSOs |
| `lotw_dxcc_credits` | Yes | Query DXCC award credits |
| `lotw_user_activity` | No | Check if a callsign uses LoTW |
| `lotw_download` | Yes | Download LoTW log data in ADIF format |

---

## Tool Reference

### lotw_confirmations

Query confirmed QSL records from LoTW.

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `persona` | str | Yes | Persona name configured in qso-graph-auth |
| `since` | str | No | QSLs received since this date (YYYY-MM-DD). Default: last 30 days |
| `band` | str | No | Filter by band (e.g., "20M") |
| `mode` | str | No | Filter by mode (e.g., "FT8") |
| `callsign` | str | No | Filter by worked station |
| `dxcc` | int | No | Filter by DXCC entity code |
| `detail` | bool | No | Include QSL station location data. Default: true |

### lotw_qsos

Query all uploaded QSOs from LoTW (confirmed and unconfirmed).

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `persona` | str | Yes | Persona name configured in qso-graph-auth |
| `since` | str | No | QSOs uploaded since this date (YYYY-MM-DD). Default: last 30 days |
| `band` | str | No | Filter by band (e.g., "20M") |
| `mode` | str | No | Filter by mode (e.g., "FT8") |
| `start_date` | str | No | QSO date range start (YYYY-MM-DD) |
| `end_date` | str | No | QSO date range end (YYYY-MM-DD) |

### lotw_dxcc_credits

Query DXCC award credits from LoTW confirmations.

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `persona` | str | Yes | Persona name configured in qso-graph-auth |
| `entity` | int | No | Filter by DXCC entity code |

Returns total credits and list of credited QSOs with award details.

### lotw_user_activity

Check if a callsign uses LoTW and when they last uploaded. Uses a locally cached copy of the LoTW user activity CSV (refreshed weekly). Public — no authentication required.

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `callsign` | str | Yes | Callsign to check |

---

## Credential Setup

```bash
pip install qso-graph-auth
qso-auth creds set ki7mt lotw
```

---

## Known Quirks

- **LoTW is read-only** — uploads require TQSL digital signatures and are out of scope for this server.
- **Slow responses** — LoTW can take 30-60 seconds for large queries. lotw-mcp uses 120-second timeouts.
- **Use date filters** — always provide `since` or `start_date` to limit result sets. Unbounded queries can be very slow.
- **Legacy passwords** — pre-September 2019 LoTW accounts may require lowercase passwords. Avoid special characters.
- **User activity cache** — the CSV file has a 7-day TTL.

---

## Mock Mode

```bash
LOTW_MCP_MOCK=1 lotw-mcp
```

## MCP Inspector

```bash
lotw-mcp --transport streamable-http --port 8004
```
