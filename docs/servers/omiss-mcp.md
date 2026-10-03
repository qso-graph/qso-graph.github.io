---
render_macros: true
---

# omiss-mcp

**OMISS integration — the net schedule, nets on the air, members, check-in history, the Statehood schedule, officers, awards and net statistics.**

```bash
uvx omiss-mcp            # run it; nothing to install
```

[GitHub](https://github.com/qso-graph/omiss-mcp) · [PyPI](https://pypi.org/project/omiss-mcp/)

---

## Tools

All {{ tools("omiss-mcp") }} tools are **public** — no login or API key needed. Data comes from the public pages at [omiss.net](https://www.omiss.net/); nets on the air come from NetLogger.

| Tool | Description |
|------|-------------|
| `omiss_net_schedule` | Every net's band, UTC time, frequency, days and band coordinator; holiday dates |
| `omiss_nets_on_air` | OMISS nets on the air now, from NetLogger |
| `omiss_member_lookup` | One member: OM number, call, name, status, grid, state, county, last check-in |
| `omiss_checkin_history` | Past nets, newest first, optionally only a member's, a band's or a date's |
| `omiss_net_checkins` | One past net: net control, relays, notes, and the check-in list |
| `omiss_statehood_schedule` | 40m net dates and their free-call states, and the next one |
| `omiss_officers` | Officers, band coordinators, committees, appointees, past presidents |
| `omiss_awards` | The awards, with the IDs the other award tools take |
| `omiss_award_rules` | An award's rules, or every award's summary |
| `omiss_award_recipients` | Who holds an award, newest first, or check one member |
| `omiss_net_statistics` | Nets per band, last net per band, leaderboards, last check-in by state |
| `omiss_set_callsign` | Save your callsign, for `omiss_nets_on_air` (asked once) |
| `get_version_info` | Service version + omiss.net layout version (fleet identity attestation) |

---

## Tool Reference

### omiss_member_lookup

Look up one member. Give one of the two.

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `callsign` | str | No | The member's callsign (e.g., KI7MT) |
| `om_number` | int | No | The member's OMISS number (e.g., 7212) |

### omiss_checkin_history

List past nets, newest first. omiss.net shows the latest 100 matches.

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `callsign` | str | No | Only nets this station checked in to |
| `om_number` | int | No | Only nets this member checked in to |
| `band` | str | No | 10m, 12m, 15m, 17m, 20m, 40m, 80m or 160m |
| `date` | str | No | YYYY, YYYY-MM or YYYY-MM-DD (UTC) |
| `net_control` | str | No | Only nets this station ran as net control |

Returns nets with `net_id`, name, time and check-in count.

### omiss_net_checkins

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `net_id` | int | Yes | The net's ID, from `omiss_checkin_history` |

### omiss_award_rules / omiss_award_recipients

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `award_id` | str | Rules: No · Recipients: Yes | The award's ID, from `omiss_awards` (e.g., ALPHABETSOUP) |
| `callsign` | str | No | Recipients only: this station's certificates |
| `om_number` | int | No | Recipients only: this member's certificates |
| `limit` | int | No | Recipients only: at most this many (default 100) |

### omiss_net_statistics

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `state` | str | No | Also this state's last check-in on each band (e.g., ID) |
| `top` | int | No | Leaderboard entries (default 10, at most 50) |

---

## Good Neighbour Policy

omiss.net is a volunteer-run club website, not an API. omiss-mcp makes at most one request every 2 seconds, shared by every copy you run, caches answers (1 hour to 7 days), serves the last answer when the site is down, and backs off for at least a minute when the site says it's busy. `omiss_nets_on_air` keeps to NetLogger's call limits.

## Security and Privacy

Every value is checked before it is sent: callsigns, OM numbers, bands, dates, net IDs, and award IDs from the site's own list. Free text never reaches omiss.net. Postal addresses and email addresses are never returned. Members are looked up one at a time; there's no search by place and no roster download.

---

## Mock Mode

```bash
OMISS_MCP_MOCK=1 omiss-mcp
```

## MCP Inspector

```bash
omiss-mcp --transport streamable-http --port 8015
```
