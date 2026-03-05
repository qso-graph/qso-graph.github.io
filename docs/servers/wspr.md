# wspr-mcp

**WSPR beacon analytics — spots, band activity, top paths, and propagation analysis.**

```bash
pip install wspr-mcp
```

[GitHub](https://github.com/qso-graph/wspr-mcp) · [PyPI](https://pypi.org/project/wspr-mcp/)

---

## Tools

All 5 tools are **public** — no credentials needed.

| Tool | Description |
|------|-------------|
| `wspr_spots` | Recent WSPR spots |
| `wspr_activity` | Activity summary for a callsign |
| `wspr_band_activity` | Per-band activity overview |
| `wspr_top_paths` | Longest/best paths in last 24 hours |
| `wspr_propagation` | Band-by-band propagation between two grids |

---

## Tool Reference

### wspr_spots

Get recent WSPR spots. Each spot is a 2-minute integration proving a propagation path exists.

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `callsign` | str | No | Filter by TX or RX callsign |
| `band` | str | No | Filter by band (e.g., "20m", "40m") |
| `limit` | int | No | Maximum spots to return. Default: 50, max: 200 |

Returns list of spots with TX/RX callsigns, grids, SNR, distance, and band.

### wspr_activity

Get WSPR activity summary for a callsign. Shows TX/RX spot counts, active bands, unique reporters, maximum distance, and best SNR.

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `callsign` | str | Yes | Callsign to look up (e.g., KI7MT, K9AN) |

### wspr_band_activity

Get current per-band WSPR activity summary. Shows how many spots, TX stations, and RX stations are active on each band, with average path distance. No parameters.

### wspr_top_paths

Get the longest/best WSPR paths in the last 24 hours. Long paths prove the band is open.

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `band` | str | No | Filter by band (e.g., "20m") |
| `limit` | int | No | Maximum paths to return. Default: 20 |

Returns list of top paths with TX/RX callsigns, grids, band, SNR, and distance.

### wspr_propagation

Get WSPR-derived propagation between two grid squares. Shows which bands have been open between two locations in the last 24 hours, with spot counts, average SNR, best SNR, and hours of opening.

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `tx_grid` | str | Yes | Transmitter grid square (e.g., DN13, FN31) |
| `rx_grid` | str | Yes | Receiver grid square (e.g., JN48, IO91) |

Returns per-band propagation data with spot counts, SNR stats, and open hours.

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
