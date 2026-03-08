# qso-graph-auth

**Foundation package — OS keyring credential management, persona CRUD, and provider management.**

```bash
pip install qso-graph-auth
```

[GitHub](https://github.com/qso-graph/qso-graph-auth) · [PyPI](https://pypi.org/project/qso-graph-auth/)

---

## What It Does

qso-graph-auth manages credentials for all authenticated QSO-Graph servers. It provides:

- **Persona management** — named identities (callsign + date range) stored in `~/.config/adif-mcp/personas.json`
- **Credential storage** — passwords and API keys stored in your OS keyring (never in config files)
- **Provider management** — enable/disable services per persona
- **Health check** — `creds doctor` verifies all credentials are wired up
- **CLI** — `qso-auth` command for all operations

All authenticated MCP servers (`eqsl-mcp`, `qrz-mcp`, `lotw-mcp`, `hamqth-mcp`) depend on this package.

---

## Quick Start

```bash
# Install
pip install qso-graph-auth

# Create a persona (your callsign identity)
qso-auth persona add --name ki7mt --callsign KI7MT --start 2020-01-01

# Store credentials for each service (prompts interactively)
qso-auth creds set ki7mt eqsl
qso-auth creds set ki7mt lotw
qso-auth creds set ki7mt qrz
qso-auth creds set ki7mt qrz_logbook
qso-auth creds set ki7mt hamqth

# Verify everything is wired up
qso-auth creds doctor
```

See the [Credential Setup Guide](../credentials.md) for full details, per-server examples, and troubleshooting.

---

## CLI Reference

### Persona Commands

| Command | Description |
|---------|-------------|
| `qso-auth persona add --name NAME --callsign CALL --start YYYY-MM-DD` | Create a persona |
| `qso-auth persona list` | List all personas |
| `qso-auth persona list --verbose` | List with callsign and date range |
| `qso-auth persona show NAME` | Show persona details |
| `qso-auth persona set-active NAME` | Set the active persona |
| `qso-auth persona remove NAME` | Delete a persona |

### Credential Commands

| Command | Description |
|---------|-------------|
| `qso-auth creds set PERSONA PROVIDER` | Store credentials (interactive prompt) |
| `qso-auth creds get PERSONA PROVIDER` | Show credentials (redacted) |
| `qso-auth creds get PERSONA PROVIDER --raw` | Show credentials (unmasked) |
| `qso-auth creds delete PERSONA PROVIDER` | Remove credentials from keyring |
| `qso-auth creds doctor` | Check all personas for missing credentials |

### Provider Commands

| Command | Description |
|---------|-------------|
| `qso-auth provider list` | List supported providers |
| `qso-auth provider enable PERSONA PROVIDER` | Enable a provider for a persona |
| `qso-auth provider disable PERSONA PROVIDER` | Disable a provider for a persona |

---

## Supported Providers

| Provider | Auth Type | Used By |
|----------|-----------|---------|
| `eqsl` | username + password | eqsl-mcp |
| `lotw` | username + password | lotw-mcp |
| `qrz` | username + password | qrz-mcp (XML API) |
| `qrz_logbook` | username + API key | qrz-mcp (Logbook API) |
| `hamqth` | username + password | hamqth-mcp |

---

## Python API

Authenticated MCP servers use `PersonaManager` to read credentials at runtime:

```python
from qso_graph_auth.identity import PersonaManager

pm = PersonaManager()
creds = pm.require("ki7mt", "eqsl")
# creds.username, creds.password
```

---

## Where Credentials Are Stored

| OS | Keyring Backend |
|----|----------------|
| macOS | Keychain Access |
| Windows | Credential Manager |
| Linux (desktop) | GNOME Keyring or KWallet |
| Linux (headless) | `keyrings.alt` encrypted file |

Credentials are stored under the service name `adif_mcp` with the key format `persona:provider`. The keyring service name uses an underscore for backwards compatibility.

---

## Security

- Credentials never appear in logs, tool results, or error messages
- No subprocess, no shell=True, no eval/exec
- 6 automated security tests in `test_security.py`
- Security gate blocks PyPI publish on failure
