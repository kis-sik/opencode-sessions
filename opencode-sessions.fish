# Fish shell completion for opencode-sessions
# Place in ~/.config/fish/completions/opencode-sessions.fish

function __opencode_sessions_complete_options
    echo --help
    echo --print-all
    echo --sort-date
    echo --sort-tokens
    echo --sort-cost
    echo --sort-messages
    echo --stats
    echo --delete
    echo --delete-unnamed
end

function __opencode_sessions_complete_sessions
    # Get current directory sessions
    if command -q opencode-sessions
        opencode-sessions 2>/dev/null | awk 'NR>3 && /^  / {print $NF}' | head -20
    end
end

complete -c opencode-sessions -f

# Basic options
complete -c opencode-sessions -n "not __fish_seen_subcommand_from (__opencode_sessions_complete_options)" \
    -a "(__opencode_sessions_complete_options)"

# Delete command with session completion
complete -c opencode-sessions -n "__fish_seen_subcommand_from --delete" \
    -a "(__opencode_sessions_complete_sessions)"

# Help flag
complete -c opencode-sessions -s h -l help -d "Show help"

# Print all sessions
complete -c opencode-sessions -l print-all -d "Show all sessions from all projects"

# Sort options
complete -c opencode-sessions -l sort-date -d "Sort by date (newest first)"
complete -c opencode-sessions -l sort-tokens -d "Sort by token count (highest first)"
complete -c opencode-sessions -l sort-cost -d "Sort by cost (highest first)"
complete -c opencode-sessions -l sort-messages -d "Sort by message count (highest first)"

# Stats
complete -c opencode-sessions -l stats -d "Show detailed statistics"

# Delete options
complete -c opencode-sessions -l delete -d "Delete sessions by name or UUID" -x
complete -c opencode-sessions -l delete-unnamed -d "Delete all sessions without custom name"