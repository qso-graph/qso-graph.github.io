# clublog-mcp

**Club Log integration — DXCC resolution, expedition logs, activity analysis, and Most Wanted.**

```bash
pip install clublog-mcp
```

[GitHub](https://github.com/qso-graph/clublog-mcp) · [PyPI](https://pypi.org/project/clublog-mcp/)

---

## Tools

| Tool | Auth | Description |
|------|:----:|-------------|
| `clublog_dxcc` | API key | Date-aware DXCC resolution |
| `clublog_search` | API key | Search expedition logs ("am I in the log?") |
| `clublog_activity` | API key | Hour-by-hour propagation activity between DXCC entities |
| `clublog_most_wanted` | Public | Current Most Wanted DXCC list |
| `clublog_expeditions` | Public | Active and recent DXpeditions |
| `clublog_watch` | API key | Monitor real-time activity for a callsign |

---

## Tool Reference

### clublog_dxcc

Resolve a callsign to its DXCC entity. Date-aware — handles historical prefix changes.

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `callsign` | str | Yes | Callsign to resolve (e.g., VP8PJ, 3Y0J) |
| `date` | str | No | Date for resolution (YYYY-MM-DD) |

### clublog_search

Search an expedition or public log for a callsign.

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `callsign` | str | Yes | Your callsign to search for |
| `log` | str | Yes | DX station or expedition log (e.g., 3Y0J) |
| `year` | int | No | Year filter |

Returns whether found, and band x mode breakdown of QSOs.

### clublog_activity

Hour-by-hour propagation activity between two DXCC entities. Source and destination are reciprocal.

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `source` | int | Yes | Source DXCC entity code (e.g., 291 for USA) |
| `dest` | int | Yes | Destination DXCC entity code (e.g., 339 for Japan) |
| `month` | int | No | Month filter (1-12) |
| `last_year_only` | bool | No | Limit to last 12 months. Default: false |
| `sfi_min` | int | No | Minimum SFI filter |
| `sfi_max` | int | No | Maximum SFI filter |

Returns hourly activity proportions per band (normalized to sum 1.0).

### clublog_most_wanted

Get the current Most Wanted DXCC entity list. No parameters — public endpoint, no API key required.

### clublog_expeditions

List active and recent DXpeditions. No parameters — public endpoint, no API key required.

### clublog_watch

Monitor real-time activity for a callsign. Shows 24-hour QSOs by band/mode, grid locator, OQRS status, and expedition flag.

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `callsign` | str | Yes | Callsign to monitor (e.g., 3Y0J) |

---

## Credential Setup

Club Log uses a per-application API key (not per-user credentials):

```bash
export CLUBLOG_API_KEY="your-40-character-hex-key"
```

Get your API key at [clublog.org/getapi.php](https://clublog.org/getapi.php).

!!! warning "API Key Security"
    Club Log auto-revokes API keys found in public repositories (GitHub scanning is active). Never commit your key to source control.

---

## Known Quirks

- **Band normalization**: Club Log uses bare numbers ("20", "40"); clublog-mcp normalizes to ADIF names ("20m", "CW", "Phone", "Data").
- **`clublog_most_wanted` and `clublog_expeditions`** are public — they work without an API key.

---

## Rate Limiting

- 500ms minimum delay between requests
- 30 requests/minute
- 3600-second freeze on HTTP 403

### Response Cache

| Data | TTL |
|------|-----|
| DXCC lookups | 1 hour |
| Most Wanted | 24 hours |
| Activity | 1 hour |
| Watch | 5 minutes |

---

## Mock Mode

```bash
CLUBLOG_MCP_MOCK=1 clublog-mcp
```

## MCP Inspector

```bash
clublog-mcp --transport streamable-http --port 8003
```
