# wspr-mcp

**WSPR beacon analytics — live spots, band activity, top beacons, propagation paths, SNR trends, and more.**

Data from [wspr.live](https://wspr.live/) (~2.7 billion spots, 2008-present).

```bash
pip install wspr-mcp
```

[GitHub](https://github.com/qso-graph/wspr-mcp) · [PyPI](https://pypi.org/project/wspr-mcp/)

---

## Tools

All 8 tools are **public** — no credentials needed.

| Tool | Description |
|------|-------------|
| `wspr_spots` | Recent WSPR spots with flexible filtering |
| `wspr_band_activity` | Per-band activity — spots, stations, distances, SNR |
| `wspr_top_beacons` | Top transmitters ranked by spot count or distance |
| `wspr_top_spotters` | Top receivers ranked by spot count or distance |
| `wspr_propagation` | Propagation between two locations (callsign or grid) |
| `wspr_grid_activity` | All WSPR activity in/out of a Maidenhead grid square |
| `wspr_longest_paths` | Longest distance paths in a time window |
| `wspr_snr_trend` | Hourly SNR trend for a specific path over time |

---

## Tool Reference

### wspr_spots

Get recent WSPR spots. Each spot is a 2-minute integration proving a propagation path exists.

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `callsign` | str | No | Filter by TX or RX callsign (e.g., KI7MT) |
| `band` | str | No | Filter by band (e.g., "20m", "40m", "10m") |
| `hours` | int | No | Time window in hours. Default: 24, max: 72 |
| `limit` | int | No | Maximum spots to return. Default: 50, max: 200 |
| `grid` | str | No | Filter by grid square prefix (e.g., DN13). Matches TX or RX |
| `min_snr` | int | No | Minimum SNR in dB (e.g., -20) |
| `max_snr` | int | No | Maximum SNR in dB (e.g., -5) |
| `min_distance` | int | No | Minimum path distance in km (e.g., 5000) |

### wspr_band_activity

Per-band WSPR activity summary. Shows spot counts, TX/RX station counts, average and max distance, and average SNR for each band.

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `hours` | int | No | Time window in hours. Default: 1, max: 6 |

### wspr_top_beacons

Top WSPR transmitters ranked by spot count or maximum distance.

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `band` | str | No | Filter by band (e.g., "20m") |
| `hours` | int | No | Time window in hours. Default: 24, max: 72 |
| `sort_by` | str | No | Ranking: "spots" (default) or "distance" |
| `limit` | int | No | Number of results. Default: 20, max: 50 |

### wspr_top_spotters

Top WSPR receivers ranked by spot count or maximum distance.

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `band` | str | No | Filter by band (e.g., "20m") |
| `hours` | int | No | Time window in hours. Default: 24, max: 72 |
| `sort_by` | str | No | Ranking: "spots" (default) or "distance" |
| `limit` | int | No | Number of results. Default: 20, max: 50 |

### wspr_propagation

Propagation between two locations. Accepts callsigns, grid squares, or a mix. Searches both directions automatically.

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `tx` | str | Yes | First endpoint — callsign (e.g., KI7MT) or grid (e.g., DN13) |
| `rx` | str | Yes | Second endpoint — callsign (e.g., G8JNJ) or grid (e.g., IO91) |
| `band` | str | No | Filter to a specific band (e.g., "20m") |
| `hours` | int | No | Time window in hours. Default: 24, max: 72 |

Returns per-band propagation with spot counts, SNR stats, and UTC hours open.

### wspr_grid_activity

All WSPR activity in or out of a Maidenhead grid square. Use 2-character (e.g., DN) for a wide area or 4-character (e.g., DN13) for a specific region.

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `grid` | str | Yes | Maidenhead grid — 2 char (DN) or 4 char (DN13) |
| `band` | str | No | Filter by band (e.g., "20m") |
| `hours` | int | No | Time window in hours. Default: 24, max: 72 |
| `limit` | int | No | Maximum recent spots to return. Default: 50, max: 200 |

Returns summary stats (totals, stations, bands) plus recent spot list.

### wspr_longest_paths

Longest WSPR paths in the given time window. Long paths prove the band is open.

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `band` | str | No | Filter by band (e.g., "10m") |
| `hours` | int | No | Time window in hours. Default: 24, max: 72 |
| `limit` | int | No | Maximum paths to return. Default: 20, max: 50 |
| `min_distance` | int | No | Minimum distance in km (e.g., 15000 for near-antipodal) |

### wspr_snr_trend

Hourly SNR trend for a specific path. Shows when a band opens/closes and how signal strength varies.

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `tx` | str | Yes | First endpoint — callsign (e.g., K9AN) or grid (e.g., EN50) |
| `rx` | str | Yes | Second endpoint — callsign (e.g., G8JNJ) or grid (e.g., IO91) |
| `band` | str | No | Filter to a specific band (e.g., "20m") |
| `hours` | int | No | Time window in hours. Default: 24, max: 72 |

Returns hourly data points with spot counts, avg/best/worst SNR.

---

## Good Neighbour Policy

wspr.live is a volunteer-run service. We are respectful with our query patterns:

| Measure | Detail |
|---------|--------|
| Rate limiting | 3 seconds between requests (20 req/min) |
| Circuit breaker | Opens after 3 consecutive failures; exponential backoff up to 5 minutes |
| Time-bounded queries | Every query filters by time (max 72 hours) |
| Band filtering | Queries use band indexes when provided |
| Column selection | Only needed columns per query, never `SELECT *` |
| Result limits | All queries cap results (200 spots, 50 leaderboard entries) |
| Response caching | 2-10 minute TTL per tool |
| Request timeout | 20 seconds |
| User-Agent | Every request identifies as `wspr-mcp/{version}` |

---

## What is WSPR?

**WSPR** (Weak Signal Propagation Reporter) is a digital protocol designed to probe HF propagation paths using very low power (typically 200 mW to 5 W). Stations transmit 2-minute beacons that encode callsign, grid square, and power — providing objective, machine-readable propagation measurements.

Unlike QSOs, WSPR spots require no human interaction. A global network of automated receivers provides continuous propagation monitoring across all HF bands, 24/7.

---

## No Credential Setup Needed

WSPR data is publicly available. Just install and start using it.

---

## Mock Mode

```bash
WSPR_MCP_MOCK=1 wspr-mcp
```

## MCP Inspector

```bash
wspr-mcp --transport streamable-http --port 8009
```
