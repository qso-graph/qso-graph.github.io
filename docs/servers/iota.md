# iota-mcp

**Islands on the Air integration — group lookup, island search, DXCC mapping, nearby groups, programme statistics.**

```bash
pip install iota-mcp
```

[GitHub](https://github.com/qso-graph/iota-mcp) · [PyPI](https://pypi.org/project/iota-mcp/)

---

## Tools

All 6 tools are **public** — no credentials needed.

| Tool | Description |
|------|-------------|
| `iota_lookup` | Look up an IOTA group by reference number |
| `iota_search` | Search groups and islands by name |
| `iota_islands` | List all islands and subgroups in a group |
| `iota_dxcc` | Bidirectional DXCC-to-IOTA mapping |
| `iota_stats` | Programme summary statistics |
| `iota_nearby` | Find IOTA groups nearest to a location |

---

## Tool Reference

### iota_lookup

Look up an IOTA group by reference number.

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `refno` | str | Yes | IOTA reference number (e.g., "NA-005", "EU-005", "OC-019") |

Returns group name, DXCC entity, bounding box, center coordinates, credit percentage, and island count.

### iota_search

Search IOTA groups and islands by name.

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `query` | str | Yes | Search text (e.g., "Hawaii", "Shetland", "Comoro") |
| `limit` | int | No | Maximum results to return (default 25) |

Searches both group names and individual island names. Results are deduplicated by IOTA reference number.

### iota_islands

List all islands and subgroups in an IOTA group.

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `refno` | str | Yes | IOTA reference number (e.g., "EU-005") |

Returns the full hierarchy: subgroups containing individual islands with names and IDs.

### iota_dxcc

Bidirectional DXCC-to-IOTA mapping.

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `dxcc_num` | str | No | DXCC entity number (e.g., "291" for USA, "223" for England) |
| `refno` | str | No | IOTA reference number (e.g., "EU-005") |

Provide either `dxcc_num` to find all IOTA groups for a DXCC entity, or `refno` to find which DXCC entities an IOTA group belongs to.

### iota_stats

Get IOTA programme summary statistics. No parameters.

Returns total groups and islands, breakdown by continent, DXCC entity count, and most/least credited groups.

### iota_nearby

Find IOTA groups nearest to a location.

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `latitude` | float | Yes | Latitude in decimal degrees (e.g., 43.6 for Boise) |
| `longitude` | float | Yes | Longitude in decimal degrees (e.g., -116.2 for Boise) |
| `limit` | int | No | Maximum results to return (default 20) |

Returns IOTA groups sorted by great-circle distance from the given coordinates.

---

## Data Source

Data comes from the official [IOTA website](https://www.iota-world.org/) JSON downloads — refreshed daily at 00:00 UTC:

- **fulllist.json** (~1.3 MB) — complete group/subgroup/island hierarchy (1,178 groups, 13,020 islands)
- **dxcc_matches_one_iota.json** (~3.5 KB) — 1:1 DXCC-to-IOTA mapping

Data is downloaded once on first use and cached in memory for 24 hours.

---

## No Credential Setup Needed

IOTA data is completely public. Just install and start using it — no `adif-mcp` dependency, no persona setup.

---

## Mock Mode

```bash
IOTA_MCP_MOCK=1 iota-mcp
```

## MCP Inspector

```bash
iota-mcp --transport streamable-http --port 8010
```
