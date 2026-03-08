# pota-mcp

**Parks on the Air integration — live spots, park info, stats, schedules, and park search.**

```bash
pip install pota-mcp
```

[GitHub](https://github.com/qso-graph/pota-mcp) · [PyPI](https://pypi.org/project/pota-mcp/)

---

## Tools

All 6 tools are **public** — no credentials needed.

| Tool | Description |
|------|-------------|
| `pota_spots` | Get current activator spots with filters |
| `pota_park_info` | Detailed park information by reference |
| `pota_park_stats` | Activation and QSO counts for a park |
| `pota_user_stats` | Activator and hunter statistics |
| `pota_scheduled` | Upcoming scheduled activations |
| `pota_location_parks` | List all parks in a state/province/country |

---

## Tool Reference

### pota_spots

Get current POTA activator spots with optional filters.

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `band` | str | No | Filter by band (e.g., "20m", "40m") |
| `mode` | str | No | Filter by mode (e.g., "CW", "FT8", "SSB") |
| `location` | str | No | Filter by location code (e.g., "US-ID", "CA-ON") |
| `program` | str | No | Filter by program prefix (e.g., "US", "VE", "G") |

Returns list of active spots with activator, frequency, park, grid, and coordinates.

### pota_park_info

Get detailed park information by POTA reference code.

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `reference` | str | Yes | Park reference code (e.g., US-0001, CA-5580, G-0001) |

Returns park name, coordinates, grid, type, location, access methods, agencies, website, and first activation info.

### pota_park_stats

Get activation and QSO counts for a park.

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `reference` | str | Yes | Park reference code (e.g., US-0001) |

Returns activation attempts, successful activations, and total contacts.

### pota_user_stats

Get POTA activator and hunter statistics for a callsign.

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `callsign` | str | Yes | Callsign to look up (e.g., K4SWL, KI7MT) |

Returns activator stats (activations, parks, QSOs), hunter stats (parks worked, QSOs), awards, and endorsements.

### pota_scheduled

Get upcoming scheduled POTA activations. No parameters.

Returns list of scheduled activations with activator, park, date, time window, planned frequencies, and comments.

### pota_location_parks

List all POTA parks in a state, province, or country.

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `location` | str | Yes | Location code (e.g., "US-ID" for Idaho, "CA-ON" for Ontario, "G" for England) |

Returns list of parks with reference, name, coordinates, grid, type, and activation/contact counts.

---

## No Credential Setup Needed

POTA's API is completely public. Just install and start using it — no credential setup needed.

---

## Mock Mode

```bash
POTA_MCP_MOCK=1 pota-mcp
```

## MCP Inspector

```bash
pota-mcp --transport streamable-http --port 8006
```
