# Fish shell completion for opencode-sessions
# Place in ~/.config/fish/completions/opencode-sessions.fish

function __ocs_complete_options
    echo --help
    echo --print-all
    echo --sort-date
    echo --sort-tokens
    echo --sort-cost
    echo --sort-messages
    echo --stats
    echo --delete
    echo --delete-unnamed
    echo --rename
    echo --rename-fzf
end

function __ocs_complete_sessions
    # Get current directory sessions
    if command -q opencode-sessions
        opencode-sessions 2>/dev/null | awk 'NR>3 && /^  / {print $NF}' | head -20
    end
end

# Main command completion
complete -c opencode-sessions -f
complete -c opencode-sessions -n "__fish_use_subcommand" -a "(__ocs_complete_options)"
complete -c opencode-sessions -n "__fish_seen_subcommand_from --delete" -a "(__ocs_complete_sessions)"

# Alias completion for ocs
complete -c ocs -f
complete -c ocs -n "__fish_use_subcommand" -a "(__ocs_complete_options)"
complete -c ocs -n "__fish_seen_subcommand_from --delete" -a "(__ocs_complete_sessions)"

# Help
complete -c opencode-sessions -l help -d "Show help"
complete -c ocs -l help -d "Show help"

# Print options
complete -c opencode-sessions -l print-all -d "Show all sessions"
complete -c ocs -l print-all -d "Show all sessions"

# Sort options
complete -c opencode-sessions -l sort-date -d "Sort by date (newest first)"
complete -c ocs -l sort-date -d "Sort by date (newest first)"
complete -c opencode-sessions -l sort-tokens -d "Sort by token count (highest first)"
complete -c ocs -l sort-tokens -d "Sort by token count (highest first)"
complete -c opencode-sessions -l sort-cost -d "Sort by cost (highest first)"
complete -c ocs -l sort-cost -d "Sort by cost (highest first)"
complete -c opencode-sessions -l sort-messages -d "Sort by message count (highest first)"
complete -c ocs -l sort-messages -d "Sort by message count (highest first)"

# Stats
complete -c opencode-sessions -l stats -d "Show detailed statistics"
complete -c ocs -l stats -d "Show detailed statistics"

# Delete options
complete -c opencode-sessions -l delete -d "Delete sessions by name or UUID" -x
complete -c ocs -l delete -d "Delete sessions by name or UUID" -x
complete -c opencode-sessions -l delete-unnamed -d "Delete all sessions without custom name"
complete -c ocs -l delete-unnamed -d "Delete all sessions without custom name"

# Rename options
complete -c opencode-sessions -l rename -d "Rename session" -x
complete -c ocs -l rename -d "Rename session" -x
complete -c opencode-sessions -l rename-fzf -d "Interactive rename with fzf"
complete -c ocs -l rename-fzf -d "Interactive rename with fzf"

# Installation commands
complete -c opencode-sessions -l install -d "Install for current user"
complete -c ocs -l install -d "Install for current user"
complete -c opencode-sessions -l install-system -d "Install system-wide (requires sudo)"
complete -c ocs -l install-system -d "Install system-wide (requires sudo)"
complete -c opencode-sessions -l uninstall -d "Uninstall from current user"
complete -c ocs -l uninstall -d "Uninstall from current user"
complete -c opencode-sessions -l uninstall-system -d "Uninstall system-wide (requires sudo)"
complete -c ocs -l uninstall-system -d "Uninstall system-wide (requires sudo)"