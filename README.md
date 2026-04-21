# ocs

OpenCode Sessions Manager - Enhanced OpenCode session manager with detailed statistics and management tools.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-1.2.0-blue)](https://github.com/kis-sik/opencode-sessions/releases/tag/v1.2.0)

## Features

- 📊 **Table output** with token, cost, and message statistics
- 🔄 **Sorting** by date, tokens, cost, messages
- 🗑️ **Session deletion** by name or UUID
- ✏️ **Session renaming** - rename sessions by name or UUID
- 📈 **Detailed statistics** per project
- 🐟 **Autocompletion** for Fish shell
- 🔧 **Self-installation** - script installs itself
- 🎯 **claude-sessions interface** - familiar UX
- 🔌 **OpenCode plugin** - integrates with OpenCode TUI

## What's New in v1.2.0

- **Session renaming**: `ocs --rename <old> <new>` - rename sessions by name or UUID
- **Improved help**: Updated usage documentation with new commands
- **Better installation**: Fixed completion file paths and script naming
- **Unified naming**: All references updated from `opencode-sessions` to `ocs`
- **Modern Python tools**: Full support for `uv` and `uvx`
- **Proper package structure**: `src/` layout with dynamic versioning

## Installation

### Quick installation (recommended)

#### Using uv (modern & fast)
```bash
# Run without installation
uvx ocs --help

# Install globally
uvx --from ocs --global
```

#### Using pip (traditional)
```bash
pip install ocs
```

#### One-command install
```bash
curl -sL https://raw.githubusercontent.com/kis-sik/opencode-sessions/main/install.sh | bash
```

### From source
```bash
# Clone repository
git clone https://github.com/kis-sik/opencode-sessions.git
cd opencode-sessions

# Install in development mode
pip install -e .

# Or install globally
pip install .
```

### Manual installation
```bash
# Install via pip
pip install ocs

# Or install Fish autocompletion manually
cp ocs.fish ~/.config/fish/completions/
source ~/.config/fish/config.fish
```

## Uninstallation
```bash
# Uninstall via pip
pip uninstall ocs

# Remove Fish completion
rm ~/.config/fish/completions/ocs.fish 2>/dev/null || true
```

## Usage

```
ocs                    # sessions for current directory
ocs --print-all        # all sessions
ocs --sort-date        # sort by date (newest first)
ocs --sort-tokens      # sort by token count (highest first)
ocs --sort-cost        # sort by cost (highest first)
ocs --sort-messages    # sort by message count (highest first)
ocs --stats            # session count per project
ocs --delete <name>    # delete by name or UUID
ocs --delete-unnamed   # delete all without custom name
ocs --rename <old> <new> # rename session
```

## Examples

```bash
# Show sessions for current project
ocs

# Show all sessions sorted by tokens
ocs --print-all --sort-tokens

# Delete session by name
ocs --delete "Firewall"

# Rename a session
ocs --rename "old name" "new name"

# Show statistics
ocs --stats
```

## Autocompletion in Fish

After installation:
- `ocs <Tab>` - option hints
- `ocs --delete <Tab>` - list of available sessions
- Works with all flags

## OpenCode Plugin Integration

The package includes an OpenCode plugin that adds enhanced session commands to the OpenCode TUI:

### Install as OpenCode plugin

```bash
# Copy plugin to OpenCode plugins directory
cp ocs-plugin.js ~/.config/opencode/plugins/
```

### Plugin commands in OpenCode TUI:
```
/ocs-stats                 - Show detailed session statistics
/ocs-list                  - Show sessions with token/cost metrics
  Options: --all, --sort-tokens, --sort-cost, --sort-date, --sort-messages
/ocs-delete <name|id>      - Delete session by name or ID
  Options: --interactive, --unnamed
```

## Development

### Project Structure
```
ocs/
├── src/                        # Python source code
│   └── ocs/                   # Main package
│       ├── __init__.py        # Package metadata
│       └── main.py            # CLI entry point
├── pyproject.toml             # Python package configuration
├── ocs.fish                   # Fish shell autocompletion
├── ocs-plugin.js              # OpenCode plugin
├── LICENSE                    # MIT License
└── README.md                  # This file
```

### Local Development
```bash
# Install in development mode
pip install -e .

# Run tests (when added)
pytest

# Build package
python -m build

# Install from local build
pip install dist/opencode_sessions-*.whl
```

### Publishing to PyPI
```bash
# Build package (with uv)
uv build

# Or with traditional tools
python -m build

# Upload to PyPI
uv publish
# or
python -m twine upload dist/*
```

## License

MIT License - see [LICENSE](LICENSE) file