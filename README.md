# opencode-sessions

OpenCode Sessions Manager - Enhanced OpenCode session manager with detailed statistics and management tools.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://img.shields.io/pypi/v/opencode-sessions.svg)](https://pypi.org/project/opencode-sessions/)
[![Version](https://img.shields.io/badge/version-1.3.0-blue)](https://github.com/kis-sik/opencode-sessions/releases/tag/v1.3.0)

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

## What's New in v1.3.0

- **Interactive rename with fzf**: `opencode-sessions --rename-fzf` - fuzzy search and interactive selection
- **Session renaming**: `opencode-sessions --rename <old> <new>` - rename sessions by name or UUID
- **Improved help**: Updated usage documentation with new commands
- **Better installation**: Fixed completion file paths and script naming
- **Modern Python tools**: Full support for `uv` and `uvx`
- **Proper package structure**: `src/` layout with dynamic versioning
- **PyPI ready**: Package name: `opencode-sessions`, import: `ocs`

## Installation

### Quick installation (recommended)

#### Using uv (modern & fast)
```bash
# Run without installation
uvx opencode-sessions --help

# Install from PyPI
uvx --from opencode-sessions --global

# Or install locally
uv add opencode-sessions
```

#### From PyPI
```bash
pip install opencode-sessions
# After installation, use: opencode-sessions
# Alias: ocs
```

#### One-command install
```bash
curl -sL https://raw.githubusercontent.com/kis-sik/opencode-sessions/main/install.sh | bash
```

#### Manual installation
```bash
# Install Fish autocompletion manually
cp opencode-sessions.fish ~/.config/fish/completions/
source ~/.config/fish/config.fish
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



## Uninstallation
```bash
# Uninstall via pip
pip uninstall opencode-sessions

# Remove Fish completion
rm ~/.config/fish/completions/opencode-sessions.fish 2>/dev/null || true
```

## Usage

```
opencode-sessions                    # sessions for current directory
opencode-sessions --print-all        # all sessions
opencode-sessions --sort-date        # sort by date (newest first)
opencode-sessions --sort-tokens      # sort by token count (highest first)
opencode-sessions --sort-cost        # sort by cost (highest first)
opencode-sessions --sort-messages    # sort by message count (highest first)
opencode-sessions --stats            # session count per project
opencode-sessions --delete <name>    # delete by name or UUID
opencode-sessions --delete-unnamed   # delete all without custom name
opencode-sessions --rename <old> <new> # rename session
opencode-sessions --rename-fzf       # interactive rename with fzf

# Alias: ocs (same as opencode-sessions)
ocs --help
```

## Examples

```bash
# Show sessions for current project
opencode-sessions

# Show all sessions sorted by tokens
opencode-sessions --print-all --sort-tokens

# Delete session by name
opencode-sessions --delete "Firewall"

# Rename a session
opencode-sessions --rename "old name" "new name"

# Interactive rename with fzf
opencode-sessions --rename-fzf

# Show statistics
opencode-sessions --stats

# Using alias (ocs)
ocs --help
```

## Interactive Selection with fzf

For users with `fzf` installed, `opencode-sessions --rename-fzf` provides an interactive interface:

1. **Fuzzy search** through all sessions
2. **Preview details** - tokens, cost, date
3. **Interactive rename** - select session, enter new name
4. **Confirmation** - confirm before applying changes

Install fzf:
```bash
# macOS
brew install fzf

# Ubuntu/Debian
sudo apt install fzf

# Arch
sudo pacman -S fzf
```

## Autocompletion in Fish

After installation:
- `opencode-sessions <Tab>` - option hints
- `opencode-sessions --delete <Tab>` - list of available sessions
- `ocs <Tab>` - same for alias
- Works with all flags

## OpenCode Plugin Integration

The package includes an OpenCode plugin that adds enhanced session commands to the OpenCode TUI:

### Install as OpenCode plugin

```bash
# Copy plugin to OpenCode plugins directory
cp opencode-sessions-plugin.js ~/.config/opencode/plugins/
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
opencode-sessions/
├── src/                        # Python source code
│   └── ocs/                   # Main package (import name)
│       ├── __init__.py        # Package metadata
│       └── main.py            # CLI entry point
├── pyproject.toml             # Python package configuration
├── opencode-sessions.fish     # Fish shell autocompletion
├── opencode-sessions-plugin.js # OpenCode plugin
├── install.sh                 # One-command installer
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