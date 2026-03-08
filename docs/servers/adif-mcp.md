# adif-mcp

**Foundation package — ADIF 3.1.6 spec engine, validation, parsing, enumerations, and geospatial.**

```bash
pip install adif-mcp
```

[GitHub](https://github.com/qso-graph/adif-mcp) · [PyPI](https://pypi.org/project/adif-mcp/)

---

## What It Does

adif-mcp provides ADIF specification tools for parsing, validation, and geospatial calculations:

- **ADIF 3.1.6 specification** — 186 fields, 26 enumerations (4,427+ records), 28 data types, all bundled as JSON
- **Record validation** — enum membership, compound CreditList format, conditional Submode checks, import-only detection
- **Log parsing** — streaming parser for large `.adi` files with pagination
- **Geospatial** — Great Circle distance and beam heading between Maidenhead grids

Credential management is handled by [qso-graph-auth](qso-graph-auth.md).

All tools run locally against the bundled spec data. No network calls required.

---

## Tools

| Tool | Description |
|------|-------------|
| `validate_adif_record` | Validate ADIF records against the 3.1.6 spec |
| `parse_adif` | Stream and paginate ADIF log files |
| `list_enumerations` | List all 26 enumerations with record counts |
| `search_enumerations` | Search across enumerations by keyword |
| `read_specification_resource` | Load any spec module as JSON |
| `calculate_distance` | Great Circle distance between grids |
| `calculate_heading` | Beam heading between grids |
| `get_version_info` | Service and spec version |

Plus 1 MCP resource: `adif://system/version`

---

## Tool Reference

### validate_adif_record

Validates an ADIF record string against the 3.1.6 specification. Checks field names, data types (Number validation), and enum membership for all 43 enum-typed fields across 26 enumerations.

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `adif_string` | str | Yes | Raw ADIF record text |

**Ask your agent:**

> "Validate this ADIF record: `<CALL:5>KI7MT <BAND:3>20m <MODE:3>FT8 <FREQ:6>14.074 <QSO_DATE:8>20250315 <EOR>`"

**Returns:**

```json
{
  "status": "success",
  "errors": [],
  "warnings": [],
  "record": {
    "CALL": "KI7MT",
    "BAND": "20m",
    "MODE": "FT8",
    "FREQ": "14.074",
    "QSO_DATE": "20250315"
  }
}
```

**Validation catches real defects:**

> "Validate this: `<MODE:3>FT4 <BAND:3>20m <EOR>`"

```json
{
  "status": "invalid",
  "errors": ["Field 'MODE': value 'FT4' is not valid in the Mode enumeration."]
}
```

FT4 must be `MODE=MFSK + SUBMODE=FT4` per ADIF 3.1.6 — unlike FT8 which was grandfathered as a MODE.

### parse_adif

Streaming parser for large ADIF files with record seeking and pagination.

| Parameter | Type | Required | Default | Description |
|-----------|------|:--------:|---------|-------------|
| `file_path` | str | Yes | — | Absolute path to the `.adi` file |
| `start_at` | int | No | 1 | First record to return (1-based) |
| `limit` | int | No | 20 | Maximum records to return |

**Ask your agent:**

> "Parse my ADIF log at /home/ki7mt/logs/field-day-2025.adi and show the first 5 records"

> "Show me records 100 through 110 from that log"

### list_enumerations

Lists all 25 ADIF 3.1.6 enumerations with record counts, import-only counts, and searchable fields.

**Parameters:** None

**Ask your agent:**

> "What enumerations are in the ADIF spec?"

**Returns:** Enumeration names with metadata — Mode (90 records, 42 import-only), Band (33 records), DXCC Entity Code (395 records), Contest_ID (431 records), and 21 more.

### search_enumerations

Search across all 26 enumerations or filter to a specific one. Case-insensitive matching on all searchable fields.

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `search_term` | str | Yes | Keyword to search (case-insensitive) |
| `enumeration` | str | No | Limit to a specific enumeration name |

**Ask your agent:**

> "Search the ADIF spec for FT8"

> "What are the valid QSL_RCVD values?"

> "Find all DXCC entities matching 'United States'"

### read_specification_resource

Loads a named ADIF 3.1.6 spec module as raw JSON. Covers fields, data types, and all 26 enumerations.

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `resource_name` | str | Yes | Spec module name (e.g., `band`, `mode`, `fields`) |

### calculate_distance

Great Circle distance in kilometers between two Maidenhead grid locators using the Haversine formula.

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `start` | str | Yes | Maidenhead grid (e.g., `DN13`, `FN31pr`) |
| `end` | str | Yes | Maidenhead grid |

**Ask your agent:**

> "How far is it from DN13 in Idaho to JN48 in central Europe?"

### calculate_heading

Initial beam heading (azimuth) from one grid to another.

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `start` | str | Yes | Your QTH grid locator |
| `end` | str | Yes | Target station grid locator |

**Ask your agent:**

> "What heading should I point my antenna from DN13 to work Japan?"

### get_version_info

Returns the service version and ADIF spec version.

**Parameters:** None

---

## Credential Management

Credential management has moved to [qso-graph-auth](qso-graph-auth.md). See the [Credential Setup Guide](../credentials.md) for instructions.

---

## Validation Coverage

adif-mcp v1.0.0 validates against all 26 ADIF 3.1.6 enumerations with 48 automated tests:

| Category | Tests | Status |
|----------|:-----:|--------|
| Enumeration listing | 3 | PASS |
| Enumeration search | 6 | PASS |
| Simple enum validation | 6 | PASS |
| Compound enum validation | 3 | PASS |
| Conditional enum validation | 2 | PASS |
| Regression | 1 | PASS |
| Official ADIF 3.1.6 test corpus (6,191 records) | 2 | PASS |
| KI7MT forensic hard tests (real operator data) | 12 | PASS |
| Security audit (source code) | 6 | PASS |
| **Total** | **48** | **48/48 PASS** |

See [Testing & Validation](../testing.md) for the full test register.

---

## Known Quirks

- **FT4 is not a MODE**: Per ADIF 3.1.6, FT4 must be `MODE=MFSK + SUBMODE=FT4`. FT8 was grandfathered as a MODE before the policy. The validator correctly rejects `MODE=FT4`.
- **LoTW uppercase bands**: LoTW exports `BAND=15M` (uppercase). The validator handles this — ADIF values are case-insensitive.
- **Import-only values**: 42 deprecated Mode values (AMTORFEC, etc.) produce warnings, not errors. Historical QSO data is preserved.
- **Deleted DXCC entities**: 62 geopolitically merged entities pass silently. These are valid historical entity codes.

---

## MCP Inspector

```bash
adif-mcp --transport streamable-http --port 8000
```
