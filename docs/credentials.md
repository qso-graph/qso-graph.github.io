# Credential Setup Guide

## How It Works

QSO-Graph uses two layers for credential management: a **persona index** (non-secret JSON file with your callsign and date range) and the **OS keyring** (where secrets are stored). A persona is your callsign identity; a provider is a service like eQSL or QRZ. Credentials are never stored in config files — only in your operating system's secure keyring.

---

## Quick Start

```bash
# 1. Install the foundation package
pip install qso-graph-auth

# 2. Create a persona (your callsign identity)
qso-auth persona add --name ki7mt --callsign KI7MT --start 2020-01-01

# 3. Store credentials for a service (prompts for username + password)
qso-auth creds set ki7mt eqsl

# 4. Verify everything is wired up
qso-auth creds doctor
```

That's it. The MCP servers will find your credentials automatically.

---

## Per-Server Credential Setup

| Server | Provider | Auth Type | What You Need |
|--------|----------|-----------|---------------|
| eqsl-mcp | `eqsl` | username + password | eQSL.cc login |
| lotw-mcp | `lotw` | username + password | LoTW website login |
| qrz-mcp (lookup) | `qrz` | username + password | QRZ.com login (XML subscription for full data) |
| qrz-mcp (logbook) | `qrz_logbook` | username + API key | QRZ API key from Settings → API |
| hamqth-mcp | `hamqth` | username + password | HamQTH.com login (free account) |
| pota-mcp | — | none | Public API, no setup needed |
| sota-mcp | — | none | Public API, no setup needed |
| iota-mcp | — | none | Public API, no setup needed |
| solar-mcp | — | none | Public API, no setup needed |
| wspr-mcp | — | none | Public API, no setup needed |

!!! note "QRZ has two providers"
    The XML API (callsign lookup, DXCC) uses your **QRZ password** via the `qrz` provider. The Logbook API (fetch QSOs, logbook status) uses a separate **API key** via the `qrz_logbook` provider. You only need `qrz_logbook` if you want logbook tools. Get your API key from QRZ → Settings → API.

### eQSL

```bash
qso-auth creds set ki7mt eqsl
```

```
Username: KI7MT
Password: ********
✓ Stored eqsl credentials for ki7mt
```

### LoTW

```bash
qso-auth creds set ki7mt lotw
```

```
Username: KI7MT
Password: ********
✓ Stored lotw credentials for ki7mt
```

### QRZ (Callsign Lookup)

```bash
qso-auth creds set ki7mt qrz
```

```
Username: KI7MT
Password: ********
✓ Stored qrz credentials for ki7mt
```

### QRZ (Logbook API)

```bash
qso-auth creds set ki7mt qrz_logbook
```

```
Username: KI7MT
API Key: ********
✓ Stored qrz_logbook credentials for ki7mt
```

### HamQTH

```bash
qso-auth creds set ki7mt hamqth
```

```
Username: KI7MT
Password: ********
✓ Stored hamqth credentials for ki7mt
```

---

## Verify Your Setup

Run the doctor command to check all credentials at once:

```bash
qso-auth creds doctor
```

```
Credential Health Check
=======================
✓ ki7mt:eqsl      — stored (username_password)
✓ ki7mt:lotw      — stored (username_password)
✓ ki7mt:qrz       — stored (username_password)
✓ ki7mt:qrz_logbook — stored (api_key)
✓ ki7mt:hamqth    — stored (username_password)

Summary: stored=5, missing=0
```

To check a single persona:

```bash
qso-auth creds doctor --persona ki7mt
```

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

## Multiple Personas

If you have multiple callsigns (contest calls, special events, club stations), create a persona for each:

```bash
# Primary callsign
qso-auth persona add --name ki7mt --callsign KI7MT --start 2020-01-01
qso-auth creds set ki7mt eqsl
qso-auth creds set ki7mt qrz

# Contest callsign (with end date)
qso-auth persona add --name k7mt --callsign K7MT --start 2024-06-01 --end 2024-06-30
qso-auth creds set k7mt eqsl

# Set your primary as active
qso-auth persona set-active ki7mt
```

---

## Troubleshooting

### Keyring backend not found (headless Linux)

On servers or headless Linux systems without a desktop keyring, install the alternative backend:

```bash
pip install keyrings.alt
```

This uses an encrypted file-based keyring instead of GNOME Keyring or KWallet.

### "No credentials found" errors

Run `qso-auth creds doctor` to see which providers are missing credentials. The fix is always:

```bash
qso-auth creds set PERSONA PROVIDER
```

### Wrong username or password

Delete and re-set the credentials:

```bash
qso-auth creds delete ki7mt eqsl
qso-auth creds set ki7mt eqsl
```

### Where are credentials stored?

| OS | Keyring Backend |
|----|----------------|
| macOS | Keychain Access |
| Windows | Credential Manager |
| Linux (desktop) | GNOME Keyring or KWallet |
| Linux (headless) | `keyrings.alt` encrypted file |

Credentials are stored under the service name `adif_mcp` with the key format `persona:provider`. You can view them in your OS keyring manager, but the CLI is the easiest way to manage them.
