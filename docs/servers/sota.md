# sota-mcp

**Summits on the Air integration — spots, alerts, summit info, nearby search, and activator stats.**

```bash
pip install sota-mcp
```

[GitHub](https://github.com/qso-graph/sota-mcp) · [PyPI](https://pypi.org/project/sota-mcp/)

---

## Tools

All 5 tools are **public** — no credentials needed.

| Tool | Description |
|------|-------------|
| `sota_spots` | Current and recent SOTA spots |
| `sota_alerts` | Upcoming activation alerts |
| `sota_summit_info` | Detailed summit information |
| `sota_summits_near` | Find summits near a location (geospatial) |
| `sota_activator_stats` | Activator profile and statistics |

---

## Tool Reference

### sota_spots

Get current and recent SOTA spots from SOTALive.

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `hours` | int | No | Time window in hours. Default: 24 |
| `association` | str | No | Filter by SOTA association (e.g., "W7I", "G", "VK") |
| `mode` | str | No | Filter by mode (e.g., "CW", "SSB", "FT8") |

Returns list of spots with activator, summit, frequency, mode, and comments.

### sota_alerts

Get upcoming SOTA activation alerts.

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `hours` | int | No | Look-ahead window in hours. Default: 16 |
| `association` | str | No | Filter by SOTA association (e.g., "W7I") |

Returns list of alerts with activator, summit, planned date/time, frequencies, and comments.

### sota_summit_info

Get detailed summit information by SOTA reference code.

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `summit_code` | str | Yes | SOTA reference (e.g., W7I/SI-001, G/LD-001) |

Returns summit name, altitude, coordinates, grid, points, validity dates, and activation history.

### sota_summits_near

Find SOTA summits near a geographic location. Unique geospatial search capability.

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `latitude` | float | Yes | Center latitude (decimal degrees) |
| `longitude` | float | Yes | Center longitude (decimal degrees) |
| `radius_km` | float | No | Search radius in km. Default: 50.0 |
| `limit` | int | No | Maximum results. Default: 20 |

Returns list of nearby summits sorted by distance with code, name, altitude, points, and activation count.

### sota_activator_stats

Get SOTA activator profile and statistics.

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `callsign` | str | Yes | Callsign to look up (e.g., KI7MT, G4YSS) |

Returns total activations, unique summits, QSO count, points, and recent activation history.

---

## Data Sources

sota-mcp uses two public APIs:

- **SOTLAS** (`api.sotl.as`) — summit data, statistics, geospatial search
- **SOTALive** (`sotalive.tk`) — live spots and alerts

---

## No Credential Setup Needed

SOTA's APIs are completely public. Just install and start using it.

---

## Mock Mode

```bash
SOTA_MCP_MOCK=1 sota-mcp
```

## MCP Inspector

```bash
sota-mcp --transport streamable-http --port 8007
```
