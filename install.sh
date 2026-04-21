#!/bin/bash

# Quick install script for ocs
# Usage: curl -sL https://raw.githubusercontent.com/kis-sik/opencode-sessions/main/install.sh | bash

set -e

echo "Installing ocs (OpenCode Sessions Manager)..."

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed"
    exit 1
fi

# Install via uv (preferred, modern & fast)
if command -v uv &> /dev/null; then
    echo "Installing via uv..."
    uvx --from ocs --global
# Install via pip (fallback)
elif command -v pip &> /dev/null || command -v pip3 &> /dev/null; then
    echo "Installing via pip..."
    pip install ocs 2>/dev/null || pip3 install ocs
else
    # Fallback: download and install manually
    echo "pip not found, downloading script..."
    SCRIPT_URL="https://raw.githubusercontent.com/kis-sik/opencode-sessions/main/src/opencode_sessions/main.py"
    INSTALL_DIR="$HOME/.local/bin"
    
    mkdir -p "$INSTALL_DIR"
    curl -sL "$SCRIPT_URL" -o "$INSTALL_DIR/ocs"
    chmod +x "$INSTALL_DIR/ocs"
    
    # Install fish completion if available
    if [ -d "$HOME/.config/fish/completions" ]; then
        COMPLETION_URL="https://raw.githubusercontent.com/kis-sik/opencode-sessions/main/ocs.fish"
        curl -sL "$COMPLETION_URL" -o "$HOME/.config/fish/completions/ocs.fish"
        echo "Fish completion installed"
    fi
fi

echo "Installation complete!"
echo "Run: ocs --help"