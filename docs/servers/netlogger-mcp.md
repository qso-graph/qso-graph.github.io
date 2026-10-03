---
render_macros: true
---

# netlogger-mcp

**NetLogger integration — nets on the air, live check-ins and who's up, and past nets.**

```bash
uvx netlogger-mcp            # run it; nothing to install
```

[GitHub](https://github.com/qso-graph/netlogger-mcp) · [PyPI](https://pypi.org/project/netlogger-mcp/)

---

## Tools

All {{ tools("netlogger-mcp") }} tools are **public** — no API key needed. Your callsign is asked for once (see below).

| Tool | Description |
|------|-------------|
| `netlogger_active_nets` | Nets on the air now: frequency, band, mode, net control, logger, monitoring count |
| `netlogger_checkins` | A live net's check-in list, plus the pointer (the station being worked now) |
| `netlogger_past_nets` | Closed nets over the last N days, with the net IDs past check-ins need |
| `netlogger_past_checkins` | A closed net's check-in list |
| `netlogger_set_callsign` | Save your callsign (asked once, on first use) |
| `get_version_info` | Service version + NetLogger API version (fleet identity attestation) |

---

## Tool Reference

### netlogger_active_nets

List nets on the air now.

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `name_like` | str | No | Only nets whose name contains this text, ignoring case (e.g., "ARES") |

Returns nets with server, name, frequency, band, mode, net control, logger, when opened, and how many are monitoring.

### netlogger_checkins

Get a live net's check-in list and the pointer.

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `server_name` | str | Yes | The net's server, from `netlogger_active_nets` (e.g., NETLOGGER2) |
| `net_name` | str | Yes | The net's name, from `netlogger_active_nets` |

Returns check-ins in list order with callsign, name, location, grid, status and remarks; the check-in count; and the pointer.

### netlogger_past_nets

List closed nets, with the net IDs `netlogger_past_checkins` needs.

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `interval_days` | int | No | How many days back. Default: 7. Over 7 needs `name_like` (NetLogger's rule) |
| `name_like` | str | No | Only nets whose name contains this text |

Returns past nets with server, name, net ID, frequency, band, mode, net control, and opened and closed times.

### netlogger_past_checkins

Get a closed net's check-in list.

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `server_name` | str | Yes | The net's server, from `netlogger_past_nets` |
| `net_name` | str | Yes | The net's name, from `netlogger_past_nets` |
| `net_id` | str | Yes | The net ID, from `netlogger_past_nets` |

### netlogger_set_callsign

Save your callsign. Needed once, before the first lookup.

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `callsign` | str | Yes | Your callsign (e.g., KI7MT) |

---

## Your Callsign

Every request tells NetLogger which station is asking, so it can tell one user from another. On first use the assistant asks for your callsign and saves it; you're asked once. To set it yourself: `NETLOGGER_MCP_CALLSIGN=KI7MT`.

## Good Neighbour Policy

NetLogger is a donation-funded service on one server. netlogger-mcp keeps to NetLogger's published call limits (GetActiveNets 1/min, GetCheckins 3/min, GetPastNets 1/min, GetPastNetCheckins 10/min), checked before a request is sent. Every copy you run shares one budget, answers are cached, and a "too many requests" on any call stops all calls for at least a minute.

## Privacy

NetLogger's check-in data includes street addresses and ZIP codes, and past nets include the IP address of whoever opened them. None of these are ever returned.

---

## Mock Mode

```bash
NETLOGGER_MCP_MOCK=1 netlogger-mcp
```

## MCP Inspector

```bash
netlogger-mcp --transport streamable-http --port 8014
```
