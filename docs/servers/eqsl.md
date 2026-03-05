# eqsl-mcp

**eQSL.cc integration — inbox, verification, AG status, and upload tracking.**

```bash
pip install eqsl-mcp
```

[GitHub](https://github.com/qso-graph/eqsl-mcp) · [PyPI](https://pypi.org/project/eqsl-mcp/)

---

## Tools

| Tool | Auth | Description |
|------|:----:|-------------|
| `eqsl_inbox` | Yes | Download incoming eQSLs |
| `eqsl_verify` | No | Check if a specific QSO exists in eQSL |
| `eqsl_ag_check` | No | Check Authenticity Guaranteed status |
| `eqsl_last_upload` | No | Check when a persona last uploaded |

---

## Tool Reference

### eqsl_inbox

Download incoming eQSLs (confirmations others have sent you).

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `persona` | str | Yes | Persona name configured in adif-mcp |
| `since` | str | No | Only records since this date (YYYY-MM-DD). Default: last 30 days |
| `confirmed_only` | bool | No | Only confirmed-back records. Default: false |
| `unconfirmed_only` | bool | No | Only unconfirmed records. Default: false |
| `qth_nickname` | str | No | QTH profile name (for multi-QTH callsigns) |

Returns total count, confirmed count, band breakdown, and QSO records.

### eqsl_verify

Check if a specific QSO exists in eQSL (public, no authentication required).

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `from_call` | str | Yes | Sender's callsign |
| `to_call` | str | Yes | Receiver's callsign |
| `band` | str | Yes | Band (e.g., "20m") |
| `qso_date` | str | Yes | QSO date (YYYY-MM-DD) |
| `mode` | str | No | Mode (exact match — use "USB" not "SSB", "PSK31" not "PSK") |

### eqsl_ag_check

Check if a callsign has Authenticity Guaranteed (AG) status. Uses a cached copy of the AG member list (refreshed every 4 hours).

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `callsign` | str | Yes | Callsign to check |

### eqsl_last_upload

Check when a persona last uploaded QSOs to eQSL.

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `persona` | str | Yes | Persona name configured in adif-mcp |

---

## Credential Setup

```bash
pip install adif-mcp
adif-mcp creds set --persona ki7mt --provider eqsl --password YOUR_EQSL_PASSWORD
```

---

## Known Quirks

- **Mode matching is exact**: eQSL requires "USB" not "SSB", "PSK31" not "PSK". If verification fails, try the specific sub-mode.
- **AG cache**: The AG member list is cached at `~/.cache/eqsl-mcp/ag_members.txt` with a 4-hour TTL.
- **Inbox download**: Uses a two-step HTML-then-ADIF flow with fallback to direct ADIF download.

---

## Mock Mode

```bash
# Run with mock data (no credentials needed)
EQSL_MCP_MOCK=1 eqsl-mcp

# Use custom ADIF file for mock data
EQSL_MCP_MOCK=1 EQSL_MCP_ADIF=/path/to/test.adi eqsl-mcp
```

## MCP Inspector

```bash
eqsl-mcp --transport streamable-http --port 8001
```
