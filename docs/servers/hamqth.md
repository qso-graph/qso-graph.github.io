# hamqth-mcp

**HamQTH.com integration — free callsign lookup, DXCC resolution, biography, and activity.**

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
| `hamqth_dx_spots` | No | Recent DX cluster spots |
| `hamqth_rbn` | No | Reverse Beacon Network spot data |
| `hamqth_verify_qso` | No | Verify a QSO against HamQTH logs |

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
