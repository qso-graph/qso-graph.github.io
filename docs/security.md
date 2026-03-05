# Security

**Security is always our #1 priority. If a feature cannot be implemented safely, it will not be implemented.**

---

## 10 Non-Negotiable Guarantees

Every qso-graph MCP server guarantees:

| # | Guarantee | How It's Verified |
|---|-----------|-------------------|
| 1 | Credentials never in logs | Static analysis + code review |
| 2 | Credentials never in tool results | All return paths traced |
| 3 | Credentials never in error messages | All raise/exception statements audited |
| 4 | Credentials never in config files | OS keyring only (via adif-mcp) |
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
User runs: adif-mcp creds set --persona ki7mt --provider qrz --password ****
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

The following are absolutely forbidden in any qso-graph server:

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

1. **Development** — implement feature, run local security checklist
2. **CI Pipeline** — `pip-audit`, security test suite, static analysis
3. **Security Audit Request** — developer sends request via internal message queue
4. **Security Review** — independent agent reviews all source files, credential flows, error messages, input handling, and dependencies
5. **Release Decision** — PASS required before tagging and publishing

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

Email: [ki7mt@yahoo.com](mailto:ki7mt@yahoo.com)
Subject: `[SECURITY] qso-graph vulnerability report`

Include:
- Affected package and version
- Steps to reproduce
- Potential impact
