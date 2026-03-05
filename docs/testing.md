# Testing & Validation

**Every qso-graph package ships with automated security tests and must pass an independent security audit before PyPI publication.**

---

## Fleet Test Summary

| Package | Version | Security Tests | CI Gate | Audit |
|---------|---------|:--------------:|:-------:|:-----:|
| [adif-mcp](servers/adif-mcp.md) | v0.7.0 | 6 | Yes | PASS |
| [eqsl-mcp](servers/eqsl.md) | v0.1.1 | 6 | Yes | PASS |
| [qrz-mcp](servers/qrz.md) | v0.1.1 | 6 | Yes | PASS |
| [clublog-mcp](servers/clublog.md) | v0.1.1 | 6 | Yes | PASS |
| [lotw-mcp](servers/lotw.md) | v0.1.1 | 6 | Yes | PASS |
| [hamqth-mcp](servers/hamqth.md) | v0.1.1 | 6 | Yes | PASS |
| [pota-mcp](servers/pota.md) | v0.1.0 | 6 | Yes | PASS |
| [sota-mcp](servers/sota.md) | v0.1.0 | 6 | Yes | PASS |
| [solar-mcp](servers/solar.md) | v0.1.0 | 6 | Yes | PASS |
| [wspr-mcp](servers/wspr.md) | v0.1.0 | 6 | Yes | PASS |
| **Total** | — | **60** | **10/10** | **10/10 PASS** |

---

## Security Test Suite (All 10 Packages)

Every package includes `test_security.py` with 6 source-code audit tests. These are not runtime tests — they scan all Python source files for forbidden patterns:

| # | Test | What It Catches |
|---|------|-----------------|
| 1 | `test_no_print_credentials` | `print()` calls containing password/secret/api_key/token |
| 2 | `test_no_logging_credentials` | `logging.*()` calls containing credential keywords |
| 3 | `test_no_subprocess` | Any use of `subprocess` or `shell=True` (command injection) |
| 4 | `test_all_urls_https` | Hardcoded `http://` URLs (except localhost) |
| 5 | `test_error_messages_safe` | Exception messages that could expose credentials |
| 6 | `test_no_eval_exec` | Any use of `eval()` or `exec()` (code injection) |

These tests run in CI on every push and must pass before any PyPI publish.

---

## CI Security Gate

Every package's GitHub Actions publish workflow includes a mandatory security job:

```yaml
jobs:
  security:
    name: Security gate
    steps:
      - Security tests (pytest test_security.py)
      - Static analysis (grep for forbidden patterns)

  publish:
    needs: security    # blocked until security passes
    steps:
      - Build and publish to PyPI
```

If the security gate fails, the publish job is **blocked**. No exceptions.

---

## adif-mcp Validation (v0.7.0)

adif-mcp is the foundation package. Beyond the standard 6 security tests, it carries a comprehensive validation test suite against the ADIF 3.1.6 specification:

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

### Enumeration Coverage

adif-mcp v0.7.0 validates all 25 ADIF 3.1.6 enumerations across 43 enum-typed fields:

| Enumeration | Records | Import-Only | Fields Using It |
|-------------|--------:|:-----------:|-----------------|
| Mode | 90 | 42 | MODE |
| Submode | 108 | 0 | SUBMODE (conditional on MODE) |
| Band | 33 | 0 | BAND, BAND_RX |
| DXCC Entity Code | 395 | 0 | DXCC, MY_DXCC |
| Contest_ID | 431 | 0 | CONTEST_ID |
| Continent | 6 | 0 | CONT, MY_CONT |
| Credit | 25 | 0 | CREDIT_SUBMITTED, CREDIT_GRANTED |
| ARRL Section | 84 | 0 | ARRL_SECT, MY_ARRL_SECT |
| Propagation Mode | 19 | 0 | PROP_MODE |
| QSL_Rcvd | 5 | 0 | QSL_RCVD, EQSL_QSL_RCVD, LOTW_QSL_RCVD |
| QSL_Sent | 4 | 0 | QSL_SENT, EQSL_QSL_SENT, LOTW_QSL_SENT |
| QSL_Via | 5 | 2 | QSL_SENT_VIA, QSL_RCVD_VIA |
| QSL Medium | 4 | 0 | Used in CreditList format |
| QSO_Complete | 6 | 0 | QSO_COMPLETE |
| EQSL_AG | 3 | 0 | APP_EQSL_AG |
| + 10 more | — | — | See ADIF 3.1.6 spec |

### Validation Logic

Enum validation handles several complex ADIF patterns:

- **Simple membership**: Uppercase-normalized lookup (e.g., `cw` → `CW` → valid Mode)
- **Compound CreditList**: `CREDIT_SUBMITTED=DXCC:CARD&LOTW` — split on comma, validate credit name against Credit enum, validate each medium against QSL_Medium enum
- **Conditional Submode**: `SUBMODE=USB` checks membership in Submode enum, then warns if parent mode (SSB) doesn't match the record's MODE field
- **Import-only detection**: Deprecated values produce warnings, not errors — historical QSO data is preserved
- **Empty value rejection**: Empty or whitespace-only values for enum fields produce errors

---

## Running Tests

### adif-mcp (full suite)

```bash
cd adif-mcp
.venv/bin/python -m pytest test/ -v
```

### Any server (security tests)

```bash
cd eqsl-mcp  # or any server
.venv/bin/python -m pytest tests/test_security.py -v
```

### All servers at once

```bash
for pkg in eqsl-mcp qrz-mcp clublog-mcp lotw-mcp hamqth-mcp pota-mcp sota-mcp solar-mcp wspr-mcp; do
  echo "=== $pkg ==="
  cd /path/to/$pkg && .venv/bin/python -m pytest tests/test_security.py -v
done
```

---

## Audit Process

The qso-graph release process requires three rounds of review before any PyPI publication:

1. **Bob** (Claude-9975) — **Writer** — writes code and runs all tests locally
2. **Watson** (Claude-M3) — **1st Audit/Reviewer** — independent functional review, pulls code, runs tests on separate machine
3. **Patton** (Claude Desktop) — **2nd Audit/Reviewer** — failure analysis and security audit, reviews all source files for credential leaks, injection surfaces, and error message safety

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
