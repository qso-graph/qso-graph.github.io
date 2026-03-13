# Testing & Validation

**Every QSO-Graph server is tested across four independent layers before release.** Each layer catches different failure modes. All four must pass before a fleet-wide release.

| Layer | Name | What It Catches | Blocking? |
|-------|------|-----------------|-----------|
| **L1** | Security Audit | Credential leaks, injection, unsafe patterns | Hard stop |
| **L2** | Unit Tests (Mock Mode) | Tool logic, parameter handling, return shapes | Hard stop |
| **L3** | Integration Tests (Live) | API connectivity, auth flows, data correctness | Pre-release gate |
| **L4** | Fleet Composition | Tool name collisions, schema conflicts, cross-server consistency | Fleet releases |

---

## Fleet Overview

**12 servers, 82 tools, 4 test layers.**

| Package | Version | Tools | L1 Security | L2 Unit | L3 Live | L4 Fleet |
|---------|---------|:-----:|:-----------:|:-------:|:-------:|:--------:|
| [adif-mcp](servers/adif-mcp.md) | 1.0.1 | 8 | 6 PASS | 48 PASS | CI/CD | PASS |
| [eqsl-mcp](servers/eqsl.md) | 0.3.1 | 5 | 6 PASS | 45 PASS | Auth | PASS |
| [qrz-mcp](servers/qrz.md) | 0.3.1 | 5 | 6 PASS | 38 PASS | Auth | PASS |
| [lotw-mcp](servers/lotw.md) | 0.3.1 | 5 | 6 PASS | 38 PASS | Auth | PASS |
| [hamqth-mcp](servers/hamqth.md) | 0.4.0 | 7 | 6 PASS | 39 PASS | 10 PASS | PASS |
| [pota-mcp](servers/pota.md) | 0.2.0 | 7 | 6 PASS | 45 PASS | 15 PASS | PASS |
| [sota-mcp](servers/sota.md) | 0.1.4 | 4 | 6 PASS | 33 PASS | 10 PASS | PASS |
| [solar-mcp](servers/solar.md) | 0.2.0 | 6 | 6 PASS | 43 PASS | 15 PASS | PASS |
| [wspr-mcp](servers/wspr.md) | 0.3.0 | 8 | 6 PASS | 40 PASS | 12 PASS | PASS |
| [iota-mcp](servers/iota.md) | 0.1.0 | 6 | 6 PASS | 46 PASS | 12 PASS | PASS |
| [n1mm-mcp](servers/n1mm-mcp.md) | 0.1.4 | 8 | 6 PASS | 59 PASS | Local | PASS |
| [ionis-mcp](https://github.com/qso-graph/ionis-mcp) | 1.2.8 | 11 | 6 PASS | — | Local | PASS |
| **Total** | — | **82** | **72** | **474+** | **74** | **20** |

!!! note "L3 Live column notes"
    - **Auth** — requires OS keyring credentials (eQSL, QRZ, LoTW accounts)
    - **Local** — requires local infrastructure (N1MM Logger+, SQLite datasets)
    - **CI/CD** — tested in GitHub Actions pipeline

---

## L1: Security Audit

Every package includes `test_security.py` with 6 source-code audit tests. These scan all Python source files for forbidden patterns — they are not runtime tests.

| # | Test | What It Catches |
|---|------|-----------------|
| S1 | `test_no_print_credentials` | `print()` calls containing password, secret, api_key, or token |
| S2 | `test_no_logging_credentials` | `logging.*()` calls containing credential keywords |
| S3 | `test_no_subprocess` | Any use of `subprocess` or `shell=True` (command injection) |
| S4 | `test_all_urls_https` | Hardcoded `http://` URLs (except localhost) |
| S5 | `test_error_messages_safe` | Exception messages that could expose credentials |
| S6 | `test_no_eval_exec` | Any use of `eval()` or `exec()` (code injection) |

These tests run in CI on every push and must pass before any PyPI publish. If the security gate fails, the publish job is **blocked**. No exceptions.

---

## L2: Unit Tests (Mock Mode)

Each server supports a mock mode (`{SERVER}_MCP_MOCK=1`) that replaces HTTP calls with embedded test fixtures. L2 tests verify tool logic, parameter handling, return shapes, parser correctness, and helper functions without making any API calls.

| Category | What's Tested | Example |
|----------|---------------|---------|
| **Parser/Helper Functions** | ADIF parsing, frequency conversion, date normalization, grid validation | `parse_adif()`, `freq_to_band()`, `to_yyyymmddhhmm()` |
| **Tool Return Shapes** | Every tool returns expected fields, types, and structures | `eqsl_inbox()` returns `total`, `records`, `by_band` |
| **Parameter Handling** | Filters, defaults, edge cases, invalid input | Band filter, callsign uppercase, empty string handling |
| **Caching** | TTL expiry, cache hits, overwrites | `_cache_set()` / `_cache_get()` with timed expiry |
| **Data Models** | Dataclass immutability, field defaults, type conversions | `FetchResult(records=[])` is frozen |

```bash
# Run L2 tests for any server (no network needed)
cd solar-mcp
pytest tests/test_tools.py -v
```

---

## L3: Live Integration Tests

L3 tests hit real APIs with known-good reference values. They verify that external services are responding correctly and that our client code handles real-world responses.

Tests are gated behind a `--live` flag and skipped by default. This keeps CI fast and avoids hammering volunteer-run services.

| Server | Tests | APIs Hit | Reference Values |
|--------|:-----:|----------|------------------|
| solar-mcp | 15 | NOAA SWPC | SFI 50-400, Kp 0-9, flare class A-X, 10 HF bands |
| pota-mcp | 15 | POTA API | US-0001 (Acadia NP), K4SWL, US-ME parks |
| sota-mcp | 10 | SOTA API | W7I/CU-001 (Borah Peak, Idaho) |
| wspr-mcp | 12 | wspr.live ClickHouse | DN13→JN48 path, JO62 grid, 20m band activity |
| iota-mcp | 12 | iota-world.org | OC-001 (Australia), 1000+ groups in programme |
| hamqth-mcp | 10 | HamQTH (public) | W1AW DXCC=291, DX cluster spots, RBN decodes |

```bash
# Run L3 live tests (requires network)
cd solar-mcp
pytest tests/test_live.py --live -v
```

!!! warning "Rate Limiting"
    WSPR and HamQTH L3 tests include a 1-second pause between requests to respect volunteer-run services. Tests take longer but avoid API bans.

---

## L4: Fleet Composition Tests

L4 tests verify that all 12 servers work correctly when loaded together. They import every server's MCP object, enumerate all tools, and check for cross-server conflicts.

| Category | Tests | What's Verified |
|----------|:-----:|-----------------|
| **F1: Tool Name Uniqueness** | 5 | No unexpected name collisions, snake_case convention, server namespacing, tool counts |
| **F2: Schema Validity** | 7 | Non-empty descriptions, typed properties, required fields exist, description length bounds |
| **F3: Fleet Inventory** | 5 | All 12 servers loaded, expected tools present, no empty servers |
| **F4: Cross-Server Consistency** | 3 | Band parameter types, callsign naming, limit parameter types |

### Known Findings

| Finding | Status | Detail |
|---------|--------|--------|
| `solar_conditions` name collision | **Resolved** | ionis-mcp v1.2.8 renamed to `solar_history`. No more collision. |
| Null defaults from `Optional` params | Tracked | FastMCP generates `{"default": null}` from Python `Optional[str] = None`. Valid JSON Schema but may affect some local LLM tool parsers. |
| Band parameter type split | By design | qso-graph servers use string band names (`"20M"`), ionis-mcp uses integer ADIF band IDs (`107`). |

```bash
# Run L4 fleet tests (all 12 servers must be installed)
cd ionis-devel
EQSL_MCP_MOCK=1 HAMQTH_MCP_MOCK=1 LOTW_MCP_MOCK=1 QRZ_MCP_MOCK=1 \
  pytest tests/test_fleet.py -v
```

---

## adif-mcp Validation (v1.0.0)

adif-mcp is the foundation package. Beyond the standard security and unit tests, it carries a comprehensive validation suite against the ADIF 3.1.6 specification:

### Test Matrix — 48/48 PASS

| Category | ID Prefix | Tests | Status |
|----------|-----------|:-----:|--------|
| Enumeration Listing | ADIF-ENL | 3 | 3/3 PASS |
| Enumeration Search | ADIF-ENS | 6 | 6/6 PASS |
| Enum Validation — Simple | ADIF-EVS | 6 | 6/6 PASS |
| Enum Validation — Compound | ADIF-EVC | 3 | 3/3 PASS |
| Enum Validation — Conditional | ADIF-EVX | 2 | 2/2 PASS |
| Enum Validation — Regression | ADIF-EVR | 1 | 1/1 PASS |
| Official ADIF 3.1.6 Test Corpus | ADIF-TCR | 2 | 2/2 PASS |
| Enum JSON Parity | ADIF-TCR | 1 | 1/1 PASS |
| Security Audit | — | 6 | 6/6 PASS |
| KI7MT Forensic Hard Tests | KI7MT-FRN | 12 | 12/12 PASS |
| Empty Value Handling | ADIF-EVS | 2 | 2/2 PASS |
| **Total** | — | **48** | **48/48 PASS** |

### Official ADIF 3.1.6 Test Corpus

The gold standard for ADIF validation. The [official test file](https://adif.org.uk/316/resources) from G3ZOD's `CreateADIFTestFiles` contains **6,191 QSO records** exercising every enumeration value in the specification.

| Test | Records | Result |
|------|--------:|--------|
| Zero false errors on all official records | 6,191 | **PASS — 0 errors** |
| All warnings are correct behavior | 6,191 | **PASS — 39 warnings** (23 user-defined fields + 16 import-only values) |
| Enum JSON files match official exports | 25 files | **PASS — all identical** |

**Rule:** If our validator rejects an official ADIF test record, our validator is wrong.

### KI7MT Forensic Hard Tests

12 tests derived from forensic analysis of **110,761 real QSO records** across three logger dialects (eQSL, QRZ, LoTW). Every test has a documented real-world source — no arbitrary tests.

| ID | Test | Source | Why It Matters |
|----|------|--------|----------------|
| FRN-001 | Bread-and-butter FT8 QSO (9 enum fields) | QRZ — 15,000+ FT8 QSOs | FT8 is 88.7% of PSK Reporter spots. If this fails, everything fails. |
| FRN-002 | MODE=FT4 correctly errors | QRZ — 2 of 49,233 records | FT4 must be MODE=MFSK + SUBMODE=FT4 per spec policy |
| FRN-003 | Multi-field contest QSO (8+ enums) | QRZ — CQ WW DX CW logs | Contest logs have highest enum density |
| FRN-004 | LoTW uppercase band (15M) | LoTW — 37,651 records | LoTW exports uppercase; case-insensitive matching required |
| FRN-005 | QSL_VIA=M import-only warning | QRZ — pre-internet QSOs | Deprecated "manager" value must warn, not reject |
| FRN-006 | Six QSL status fields in one record | QRZ — modern multi-service logs | QSL_RCVD + QSL_SENT + EQSL + LOTW — no cross-interference |
| FRN-007 | Deleted DXCC entity (Aldabra) | DXCC enum — 62 deleted entities | Geopolitical mergers are valid historical data |
| FRN-008 | PROP_MODE=SAT (satellite QSO) | QRZ — ISS/satellite contacts | Propagation_Mode enum rarely tested but critical |
| FRN-009 | Credit:CARD&LOTW (& separator) | LoTW DXCC credits | Multi-medium compound format parsing |
| FRN-010 | Freeform CONTEST_ID errors | eQSL — 470 invalid of 23,877 | "CQWW 2021" is not a valid Contest_ID |
| FRN-011 | SUBMODE without MODE field | eQSL — incomplete records | Graceful handling of missing parent field |
| FRN-012 | EQSL_AG=Y (Authenticity Guaranteed) | eQSL — AG status for DXCC | 3-value enum critical for DXCC credit eligibility |

---

## Running Tests

### Single server — security only

```bash
cd eqsl-mcp
pytest tests/test_security.py -v
```

### Single server — full mock suite

```bash
cd solar-mcp
pytest tests/ -v
```

### Single server — including live API tests

```bash
cd solar-mcp
pytest tests/ -v --live
```

### All servers — security sweep

```bash
for repo in adif-mcp eqsl-mcp qrz-mcp lotw-mcp hamqth-mcp pota-mcp \
            sota-mcp solar-mcp wspr-mcp iota-mcp n1mm-mcp ionis-mcp; do
    echo "=== $repo ==="
    (cd $repo && pytest tests/test_security.py -v) 2>&1
done
```

### Fleet composition tests

```bash
cd ionis-devel
EQSL_MCP_MOCK=1 HAMQTH_MCP_MOCK=1 LOTW_MCP_MOCK=1 QRZ_MCP_MOCK=1 \
  pytest tests/test_fleet.py -v
```

---

## Audit Process

The QSO-Graph release process requires three rounds of review before any PyPI publication:

1. **Writer** — writes code and runs all tests locally
2. **1st Audit/Reviewer** — independent functional review, pulls code, runs tests on separate machine
3. **2nd Audit/Reviewer** — failure analysis and security audit, reviews all source files for credential leaks, injection surfaces, and error message safety

All three must pass before the tag is created.

---

## References

| Resource | URL |
|----------|-----|
| ADIF 3.1.6 Specification | [adif.org/316](https://adif.org/316/ADIF_316.htm) |
| Official Test Corpus (G3ZOD) | [adif.org.uk/316/resources](https://adif.org.uk/316/resources) |
| CreateADIFTestFiles | [github.com/g3zod/CreateADIFTestFiles](https://github.com/g3zod/CreateADIFTestFiles) |
| K1MU ADIF Validator | [rickmurphy.net/adifvalidator.html](https://www.rickmurphy.net/adifvalidator.html) |
| adif-multitool (flwyd) | [github.com/flwyd/adif-multitool](https://github.com/flwyd/adif-multitool) |
| MCP Security Best Practices | [modelcontextprotocol.io](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices) |
| QSO-Graph Test Framework (internal) | [ionis-devel/planning/QSO-GRAPH-TEST-FRAMEWORK.md](https://github.com/IONIS-AI/ionis-devel) |
