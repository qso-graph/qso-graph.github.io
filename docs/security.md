# Security

**Security is always our #1 priority. If a feature cannot be implemented safely, it will not be implemented.**

---

## 10 Non-Negotiable Guarantees

Every QSO Graph MCP server guarantees:

| # | Guarantee | How It's Verified |
|---|-----------|-------------------|
| 1 | Credentials never in logs | Static analysis + code review |
| 2 | Credentials never in tool results | All return paths traced |
| 3 | Credentials never in error messages | All raise/exception statements audited |
| 4 | Credentials never in config files | OS keyring only (via qso-graph-auth) |
| 5 | No command injection surface | No subprocess, no shell=True, no os.system |
| 6 | No SQL injection surface | Parameterized queries or API-only |
| 7 | HTTPS only for external calls | All URLs audited |
| 8 | Rate limiting implemented | Prevents user account bans |
| 9 | Input validation on all user strings | Regex validation before use |
| 10 | Fail safely | Errors reveal no sensitive information |

---

## Credential Architecture

Credentials flow through the OS keyring and never appear in the MCP protocol:

```
User runs: qso-graph-auth creds set ki7mt qrz
                ↓
        OS Keyring (encrypted by OS)
        - macOS: Keychain
        - Windows: Credential Manager
        - Linux: Secret Service (GNOME Keyring / KWallet)
                ↓
User asks: "Look up W1AW on QRZ"
                ↓
AI calls: qrz_lookup(persona="ki7mt", callsign="W1AW")
                ↓
qrz-mcp: reads credentials from keyring (in-process only)
                ↓
qrz-mcp: HTTPS request to api.qrz.com
                ↓
AI sees: {"call": "W1AW", "name": "ARRL", "grid": "FN31pr", ...}
                ↓
Password NEVER appears in: tool params, tool results, logs, errors
```

### What the AI Can See

- Tool parameters: `persona`, `callsign`, `band`, `mode`, etc.
- Tool results: lookup data, QSO records, statistics
- Error messages: static strings like "Login failed" (never "Login failed with password X")

### What the AI Cannot See

- Passwords
- API keys
- Session tokens
- Any credential values

This is enforced by **architecture**, not policy. Credential values physically do not exist in MCP protocol messages.

---

## Input Validation

All user-provided strings are validated before use:

```python
import re

CALLSIGN_RE = re.compile(r'^[A-Z0-9]{1,3}[0-9][A-Z0-9]{0,4}(/[A-Z0-9]+)?$', re.IGNORECASE)
GRID_RE = re.compile(r'^[A-R]{2}[0-9]{2}([A-X]{2})?$', re.IGNORECASE)
DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')
BAND_RE = re.compile(r'^\d{1,3}[mM]$')
MODE_RE = re.compile(r'^[A-Z0-9]{2,10}$', re.IGNORECASE)
```

Error messages never include the invalid input value — this prevents injection via error reflection.

---

## Forbidden Patterns

The following are absolutely forbidden in any QSO Graph server:

```python
# FORBIDDEN — Command injection
import subprocess
os.system(command)
subprocess.run(command, shell=True)
eval(user_input)
exec(user_input)

# FORBIDDEN — Credential exposure
print(f"Password: {password}")
logging.debug(f"API key: {api_key}")
raise ValueError(f"Auth failed with password {password}")

# FORBIDDEN — Plaintext credential storage
with open("config.json") as f:
    password = json.load(f)["password"]
```

---

## Release Process

No package is published to PyPI without completing the full security pipeline:

Publishing is gated mechanically, in `publish.yml`, and every check either passes
or the release does not happen. There is no human sign-off step, because a step
that depends on somebody being available is not a gate:

1. **The run is from `main`** — enforced by the `pypi` environment's deployment
   branch rule, not only by the workflow file
2. **CI passed on the exact commit being published** — the full test suite, `ruff`,
   `mypy` and CodeQL
3. **The version agrees everywhere** — the typed version, `pyproject.toml` and
   `server.json` must match, and the version must be new on PyPI and untagged
4. **`tests/test_security.py` passes** — the credential, HTTPS and injection checks
   described above
5. **`pip-audit --strict` finds no known vulnerability** in the declared
   dependencies, resolved fresh, and a separate job audits the lockfile weekly
6. **Source greps** — no `subprocess`, no plaintext `http://`, no credential logging
7. **The tag is cut last**, only after PyPI *and* the MCP Registry both serve the
   version, so a green run means published everywhere

Earlier versions of this page described an audit request sent to an internal
message queue and an independent reviewer returning a PASS. That process was
retired: it was not what actually stood between a change and PyPI, and
describing a reviewer who does not exist overstates what a reader is getting.

---

## Security Test Suite

Every server includes automated security tests:

- No print statements containing credential keywords
- No logging statements containing credential keywords
- No subprocess or shell execution
- All external URLs use HTTPS
- No credentials in exception messages

---

## Incident Response

| Severity | Description | Response Time |
|----------|-------------|---------------|
| **Critical** | Credential exposure, RCE | Immediate (hours) |
| **High** | Data leakage, auth bypass | 24 hours |
| **Medium** | Information disclosure | 1 week |
| **Low** | Minor issues | Next release |

### Reporting Vulnerabilities

**Do NOT open public GitHub issues for security vulnerabilities.**

Email: [maintainers@qso-graph.io](mailto:maintainers@qso-graph.io)
Subject: `[SECURITY] QSO Graph vulnerability report`

Include:
- Affected package and version
- Steps to reproduce
- Potential impact
