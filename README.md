# opencode-sessions

Enhanced OpenCode session manager with detailed statistics and management tools.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- 📊 **Table output** with token, cost, and message statistics
- 🔄 **Sorting** by date, tokens, cost, messages
- 🗑️ **Session deletion** by name or UUID
- 📈 **Detailed statistics** per project
- 🐟 **Autocompletion** for Fish shell
- 🔧 **Self-installation** - script installs itself
- 🎯 **claude-sessions interface** - familiar UX
- 🔌 **OpenCode plugin** - integrates with OpenCode TUI

## Installation

### Quick installation (recommended)
```bash
# Download and install with one command
curl -sL https://raw.githubusercontent.com/yourusername/opencode-sessions/main/opencode-sessions | python3 - --install
```

### From source
```bash
# Clone repository
git clone https://github.com/yourusername/opencode-sessions.git
cd opencode-sessions

# Install for current user
./opencode-sessions --install

# Or install system-wide (for all users)
sudo ./opencode-sessions --install-system
```

### Manual installation
```bash
# Copy script
cp opencode-sessions ~/.local/bin/
chmod +x ~/.local/bin/opencode-sessions

# Install Fish autocompletion
cp opencode-sessions.fish ~/.config/fish/completions/
source ~/.config/fish/config.fish
```

## Uninstallation
```bash
# Uninstall for current user
opencode-sessions --uninstall

# Uninstall system-wide
sudo opencode-sessions --uninstall-system
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
```

## Examples

```bash
# Show sessions for current project
opencode-sessions

# Show all sessions sorted by tokens
opencode-sessions --print-all --sort-tokens

# Delete session by name
opencode-sessions --delete "Firewall"

# Show statistics
opencode-sessions --stats
```

## Autocompletion in Fish

After installation:
- `opencode-sessions <Tab>` - option hints
- `opencode-sessions --delete <Tab>` - list of available sessions
- Works with all flags

## OpenCode Plugin Integration

The package includes an OpenCode plugin that adds enhanced session commands to the OpenCode TUI:

### Install as OpenCode plugin

1. **As npm package** (after publishing):
```json
// Add to your opencode.json
{
  "$schema": "https://opencode.ai/config.json",
  "plugin": ["opencode-sessions"]
}
```

2. **As local plugin**:
```bash
# Copy plugin to OpenCode plugins directory
cp opencode-sessions-plugin.js ~/.config/opencode/plugins/
```

### Plugin commands in OpenCode TUI:
```
/session-stats                 - Show detailed session statistics
/session-list-detailed         - Show sessions with token/cost metrics
  Options: --all, --sort-tokens, --sort-cost, --sort-date, --sort-messages
/session-delete <name|id>      - Delete session by name or ID
  Options: --interactive, --unnamed
```

## Development

### Project Structure
```
opencode-sessions/
├── opencode-sessions           # Main Python script (self-installable)
├── opencode-sessions.fish      # Fish shell autocompletion
├── opencode-sessions-plugin.js # OpenCode plugin
├── package.json                # npm package configuration
├── LICENSE                     # MIT License
└── README.md                   # This file
```

### Publishing to npm
```bash
# Login to npm
npm login

# Publish package
npm publish
```

## License

MIT License - see [LICENSE](LICENSE) file