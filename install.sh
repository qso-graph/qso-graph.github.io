#!/bin/sh
# qso-graph.io/install.sh: RETIRED (2026-10). It used to build a pip environment in ~/.qso-graph.
# QSO Graph's Python tools now run with uv instead: https://qso-graph.io/getting-started/
# This script installs nothing. It prints what to do and exits non-zero, so an old
# "curl ... | bash" line fails visibly instead of seeming to work.
cat >&2 <<'MSG'
qso-graph.io/install.sh is retired: it installs nothing.

QSO Graph's tools run with uv (https://docs.astral.sh/uv/):

  1. Install uv once:
       curl -LsSf https://astral.sh/uv/install.sh | sh
  2. Your MCP client runs each server with uvx, always the current release:
       "command": "uvx", "args": ["pota-mcp"]
  3. Command-line tools:
       uv tool install qso-graph-auth    # credentials (qso-auth)
       uv tool install qsp-client        # the local-LLM relay

Full instructions: https://qso-graph.io/getting-started/
An existing ~/.qso-graph keeps working; remove it when you no longer need it.
MSG
exit 1
