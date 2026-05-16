# n1mm-mcp

**N1MM Logger+ integration — live contest state via UDP broadcast.**

```bash
pip install n1mm-mcp
```

[GitHub](https://github.com/qso-graph/n1mm-mcp) · [PyPI](https://pypi.org/project/n1mm-mcp/)

---

## Tools

All 9 tools are **public** — no credentials needed. N1MM Logger+ broadcasts contest state over UDP on your local network.

| Tool | Description |
|------|-------------|
| `n1mm_current_state` | Station snapshot — connection, contest, operator, radios |
| `n1mm_lookup` | Pre-log callsign (Contest-Copilot trigger) + current band/mode |
| `n1mm_contacts` | QSO log — recent contacts, edits, deletes |
| `n1mm_bandmap` | Live spots, mult targets, band activity |
| `n1mm_performance` | Score, rate, bands, run/S&P, hourly timeline |
| `n1mm_multipliers` | Mult grid, needs, value analysis |
| `n1mm_clock` | Contest timing, off-time, pacing |
| `n1mm_diagnostics` | Server health, parse errors, memory |
| `get_version_info` | Service version + N1MM UDP contract revision (fleet identity attestation) |

---

## Tool Reference

### n1mm_current_state

Station snapshot including connection status, contest info, operator, and radio state. Returns radio frequency, mode, call, antenna, and three-state connection status (connected/stale/disconnected).

Optional parameter: `station_name` (for multi-station setups).

### n1mm_lookup

Returns the last callsign entered in N1MM's call field, plus the current band and mode from the active radio. Designed as the Contest-Copilot trigger — when the operator types a call, the AI gets context.

Optional parameter: `station_name`.

### n1mm_contacts

Recent QSO log with filtering. Returns contacts, edits, and deletes.

Optional parameters: `station_name`, `count` (default 20), `since` (ISO timestamp), `band`, `mode`, `call_pattern`.

### n1mm_bandmap

Live bandmap spots with filtering, mult targets, and band activity summary.

Optional parameters: `station_name`, `band`, `max_age_minutes` (default 30).

### n1mm_performance

Score, rolling rates (10/30/60 min), rate derivative, band/mode breakdown, hourly timeline, and run/S&P split.

Optional parameter: `station_name`.

### n1mm_multipliers

Multiplier status grid, spotted mult needs, and mult value analysis.

Optional parameter: `station_name`.

### n1mm_clock

Contest timing, off-time detection, and pacing information.

Optional parameter: `station_name`.

### n1mm_diagnostics

Server health snapshot — connection status, parse error counters by message type, station details, and uptime.

Optional parameter: `station_name`.

---

## N1MM Setup

1. In N1MM: **Config → Configure Ports → Broadcast Data**
2. Enable all message types (RadioInfo, ContactInfo, Spot, Score, etc.)
3. Set IP to `255.255.255.255` (broadcast) and port to `12060`
4. n1mm-mcp listens on any machine on the same LAN

```
N1MM Logger+ (Windows)
    │ UDP broadcast (port 12060, XML)
    ▼
n1mm-mcp (Python, any OS on same LAN)
    ├── UDP Listener Thread (background)
    ├── State Engine (in-memory, partitioned by StationName)
    │   MCP protocol (stdio)
    ▼
AI Assistant (Claude, qsp-mcp, etc.)
```

---

## No Credential Setup Needed

n1mm-mcp is a passive UDP listener — N1MM doesn't know it exists. No API keys, no accounts, no authentication. Just install and start.

---

## CLI Options

| Option | Default | Description |
|--------|---------|-------------|
| `--port` | `12060` | UDP listen port |
| `--transport` | `stdio` | MCP transport (`stdio` or `streamable-http`) |
| `--heartbeat-timeout` | `60` | Seconds before connection goes stale |
| `--stale-timeout` | `900` | Seconds before connection goes disconnected |
| `--max-spots` | `2000` | Maximum spots in bandmap buffer |
| `--spot-ttl` | `30` | Spot time-to-live in minutes |

---

## Mock Mode

```bash
N1MM_MCP_MOCK=1 n1mm-mcp
```

## MCP Inspector

```bash
n1mm-mcp --transport streamable-http
```
