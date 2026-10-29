# qso-graph-auth

**Foundation package — OS keyring credential management, persona CRUD, and provider management.**

```bash
uv tool install qso-graph-auth
```

[GitHub](https://github.com/qso-graph/qso-graph-auth) · [PyPI](https://pypi.org/project/qso-graph-auth/)

---

## What It Does

qso-graph-auth manages credentials for all authenticated QSO Graph servers. It provides:

- **Persona management** — named identities (callsign + date range) stored in `~/.config/adif-mcp/personas.json`
- **Credential storage** — passwords and API keys stored in your OS keyring (never in config files)
- **Provider management** — enable/disable services per persona
- **Health check** — `creds doctor` verifies all credentials are wired up
- **CLI** — `qso-graph-auth` command for all operations

!!! note "The command was renamed in 0.5.0"
    It used to be `qso-auth`, which did not match the package you installed.
    `qso-auth` still works and prints a note saying where it went, so anything
    already in a script keeps running; it will be removed in a later release.

All authenticated MCP servers (`eqsl-mcp`, `qrz-mcp`, `lotw-mcp`, `hamqth-mcp`) depend on this package.

---

## Quick Start

```bash
# Install
uv tool install qso-graph-auth

# Create a persona (your callsign identity)
qso-graph-auth persona add --name ki7mt --callsign KI7MT --start 2020-01-01

# Enable each service for the persona, then store its credentials (prompts interactively)
qso-graph-auth provider enable ki7mt eqsl
qso-graph-auth provider enable ki7mt lotw
qso-graph-auth provider enable ki7mt qrz
qso-graph-auth provider enable ki7mt qrz_logbook
qso-graph-auth provider enable ki7mt hamqth
qso-graph-auth creds set ki7mt eqsl
qso-graph-auth creds set ki7mt lotw
qso-graph-auth creds set ki7mt qrz
qso-graph-auth creds set ki7mt qrz_logbook
qso-graph-auth creds set ki7mt hamqth

# List what's stored
qso-graph-auth creds doctor
```

See the [Credential Setup Guide](../credentials.md) for full details, per-server examples, and troubleshooting.

---

## CLI Reference

### Persona Commands

| Command | Description |
|---------|-------------|
| `qso-graph-auth persona add --name NAME --callsign CALL --start YYYY-MM-DD` | Create a persona |
| `qso-graph-auth persona list` | List all personas |
| `qso-graph-auth persona list --verbose` | List with callsign and date range |
| `qso-graph-auth persona show NAME` | Show persona details |
| `qso-graph-auth persona set-active NAME` | Set the active persona |
| `qso-graph-auth persona remove NAME` | Delete a persona |

### Credential Commands

| Command | Description |
|---------|-------------|
| `qso-graph-auth creds set PERSONA PROVIDER` | Store credentials (interactive prompt) |
| `qso-graph-auth creds get PERSONA PROVIDER` | Show what is stored (secrets shown as `•••`) |
| `qso-graph-auth creds delete PERSONA PROVIDER` | Remove credentials from keyring |
| `qso-graph-auth creds doctor` | Check all personas for missing credentials |

### Provider Commands

| Command | Description |
|---------|-------------|
| `qso-graph-auth provider list` | List supported providers |
| `qso-graph-auth provider enable PERSONA PROVIDER` | Enable a provider for a persona |
| `qso-graph-auth provider disable PERSONA PROVIDER` | Disable a provider for a persona |

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
