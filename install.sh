#!/bin/bash
# QSO-Graph Installer — Conda-style bootstrap for ham radio MCP servers.
#
# Usage:
#   curl -O https://qso-graph.io/install.sh
#   bash install.sh
#
# Creates ~/.qso-graph/ with a Python venv, installs qso-graph-config
# from PyPI, creates wrapper scripts, and optionally adds to PATH.
#
# Requires: Python 3.11+ (will not attempt to install Python for you)
# License: GPL-3.0-or-later

set -euo pipefail

QSO_GRAPH_HOME="$HOME/.qso-graph"
VENV_DIR="$QSO_GRAPH_HOME/venv"
BIN_DIR="$QSO_GRAPH_HOME/bin"
ETC_DIR="$QSO_GRAPH_HOME/etc"
LOG_DIR="$QSO_GRAPH_HOME/log"
MIN_PYTHON_MAJOR=3
MIN_PYTHON_MINOR=11

# ─── Colors (if terminal supports them) ──────────────────────────────────────

if [ -t 1 ]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    CYAN='\033[0;36m'
    BOLD='\033[1m'
    NC='\033[0m'
else
    RED='' GREEN='' YELLOW='' CYAN='' BOLD='' NC=''
fi

info()  { echo -e "${GREEN}[+]${NC} $*"; }
warn()  { echo -e "${YELLOW}[!]${NC} $*"; }
error() { echo -e "${RED}[ERROR]${NC} $*" >&2; }
banner() { echo -e "${CYAN}${BOLD}$*${NC}"; }

# ─── Python Detection ────────────────────────────────────────────────────────

find_python() {
    # Check versioned names first (most specific), then generic python3
    local candidates=("python3.13" "python3.12" "python3.11" "python3")

    for cmd in "${candidates[@]}"; do
        local path
        path=$(command -v "$cmd" 2>/dev/null) || continue

        # Parse version: "Python 3.13.1" -> major minor
        local version
        version=$("$path" --version 2>&1) || continue
        local major minor
        major=$(echo "$version" | sed -n 's/Python \([0-9]*\)\.\([0-9]*\).*/\1/p')
        minor=$(echo "$version" | sed -n 's/Python \([0-9]*\)\.\([0-9]*\).*/\2/p')

        if [ -z "$major" ] || [ -z "$minor" ]; then
            continue
        fi

        # Check minimum version
        if [ "$major" -gt "$MIN_PYTHON_MAJOR" ] || \
           { [ "$major" -eq "$MIN_PYTHON_MAJOR" ] && [ "$minor" -ge "$MIN_PYTHON_MINOR" ]; }; then
            echo "$path"
            return 0
        fi
    done

    return 1
}

# ─── PATH Setup ──────────────────────────────────────────────────────────────

add_to_path() {
    local shell_rc=""
    local shell_name=""

    # Detect shell
    case "$SHELL" in
        */zsh)
            shell_rc="$HOME/.zshrc"
            shell_name="zsh"
            ;;
        */bash)
            # macOS uses .bash_profile, Linux uses .bashrc
            if [ -f "$HOME/.bash_profile" ] && [ "$(uname)" = "Darwin" ]; then
                shell_rc="$HOME/.bash_profile"
            else
                shell_rc="$HOME/.bashrc"
            fi
            shell_name="bash"
            ;;
        *)
            warn "Unknown shell: $SHELL"
            warn "Add this to your shell config manually:"
            echo "  export PATH=\"\$HOME/.qso-graph/bin:\$PATH\""
            return
            ;;
    esac

    local path_line='export PATH="$HOME/.qso-graph/bin:$PATH"'

    # Check if already added
    if grep -qF '.qso-graph/bin' "$shell_rc" 2>/dev/null; then
        info "PATH already configured in $shell_rc"
        return
    fi

    echo "" >> "$shell_rc"
    echo "# QSO-Graph MCP servers" >> "$shell_rc"
    echo "$path_line" >> "$shell_rc"
    info "Added PATH to $shell_rc"
    info "Run 'source $shell_rc' or open a new terminal to activate."
}

# ─── Main ────────────────────────────────────────────────────────────────────

main() {
    banner ""
    banner "  QSO-Graph Installer"
    banner "  Ham radio MCP servers for AI agents"
    banner ""

    # Check if already installed
    if [ -d "$VENV_DIR" ]; then
        warn "QSO-Graph is already installed at $QSO_GRAPH_HOME"
        echo ""
        echo "To upgrade:   qso-graph-config --upgrade"
        echo "To reinstall: rm -rf $QSO_GRAPH_HOME && bash install.sh"
        echo "To configure: qso-graph-config"
        echo ""
        exit 0
    fi

    # Step 1a: Check for dialog
    if ! command -v dialog >/dev/null 2>&1; then
        error "dialog is required but not installed."
        echo ""
        echo "Install it first:"
        echo "  sudo dnf install dialog       (Fedora / RHEL / Rocky)"
        echo "  sudo apt install dialog       (Ubuntu / Debian)"
        echo "  brew install dialog           (macOS with Homebrew)"
        echo ""
        exit 1
    fi
    info "Found dialog at $(command -v dialog)"

    # Step 1b: Find Python
    info "Looking for Python ${MIN_PYTHON_MAJOR}.${MIN_PYTHON_MINOR}+..."

    PYTHON=$(find_python) || {
        error "Python ${MIN_PYTHON_MAJOR}.${MIN_PYTHON_MINOR}+ is required but not found."
        echo ""
        echo "Install a supported Python version:"
        echo "  brew install python@3.13          (macOS with Homebrew)"
        echo "  sudo dnf install python3.13       (Fedora / RHEL / Rocky)"
        echo "  sudo apt install python3.13       (Ubuntu / Debian)"
        echo "  https://python.org/downloads      (any platform)"
        echo ""
        exit 1
    }

    local py_version
    py_version=$("$PYTHON" --version 2>&1)
    info "Found $py_version at $PYTHON"

    # Step 2: Create directory structure
    info "Creating $QSO_GRAPH_HOME..."
    mkdir -p "$BIN_DIR" "$ETC_DIR" "$LOG_DIR"

    # Step 3: Check venv module is available (Debian/Ubuntu strip it out)
    if ! "$PYTHON" -c "import ensurepip" >/dev/null 2>&1; then
        local py_minor
        py_minor=$("$PYTHON" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
        error "Python venv module is not installed."
        echo ""
        echo "On Ubuntu/Debian, install it with:"
        echo "  sudo apt install python${py_minor}-venv"
        echo ""
        echo "Then re-run this installer."
        # Clean up empty dirs we just created
        rmdir "$LOG_DIR" "$ETC_DIR" "$BIN_DIR" "$QSO_GRAPH_HOME" 2>/dev/null || true
        exit 1
    fi

    # Step 3b: Create venv
    info "Creating Python virtual environment..."
    "$PYTHON" -m venv "$VENV_DIR"

    # Step 4: Upgrade pip (suppress warnings about outdated pip)
    info "Upgrading pip..."
    "$VENV_DIR/bin/pip" install --quiet --upgrade pip 2>&1 | tail -1 || true

    # Step 5: Install qso-graph-config (meta-package — pulls in base MCP servers)
    info "Installing qso-graph-config from PyPI..."
    "$VENV_DIR/bin/pip" install --quiet qso-graph-config 2>&1

    # Step 6: Deploy manager script and create wrappers
    info "Creating wrapper scripts in $BIN_DIR..."
    local count=0

    # Deploy the bash manager script
    local manager_url="https://raw.githubusercontent.com/qso-graph/qso-graph-config/main/qso-graph-config.sh"
    local manager_path="$BIN_DIR/qso-graph-config"
    if command -v curl >/dev/null 2>&1; then
        curl -sL "$manager_url" -o "$manager_path"
    elif command -v wget >/dev/null 2>&1; then
        wget -q "$manager_url" -O "$manager_path"
    else
        error "Neither curl nor wget found — cannot download manager script."
        exit 1
    fi
    chmod 755 "$manager_path"
    count=$((count + 1))

    # Create wrappers for all MCP server entry points
    for entry_point in "$VENV_DIR/bin/"*-mcp "$VENV_DIR/bin/qso-auth" \
                       "$VENV_DIR/bin/ionis-download"; do
        [ -f "$entry_point" ] || continue
        local name
        name=$(basename "$entry_point")
        local wrapper="$BIN_DIR/$name"
        cat > "$wrapper" <<WRAPPER
#!/bin/sh
exec $entry_point "\$@"
WRAPPER
        chmod 755 "$wrapper"
        count=$((count + 1))
    done
    info "Created $count scripts ($((count - 1)) wrappers + manager)."

    # Step 7: Save initial state
    cat > "$ETC_DIR/state.json" <<STATE
{
  "tier": "base",
  "installed_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "last_upgrade": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "python_path": "$PYTHON"
}
STATE

    # Step 8: PATH setup
    add_to_path

    # Done
    echo ""
    banner "  Installation complete!"
    echo ""
    info "Home directory: $QSO_GRAPH_HOME"
    info "Run 'qso-graph-config' to set up MCP servers."
    echo ""
}

main "$@"
