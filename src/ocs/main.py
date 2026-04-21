#!/usr/bin/env python3
"""
Usage:
  opencode-sessions                    # sessions for current directory
  opencode-sessions --print-all        # all sessions
  opencode-sessions --sort-date        # sort by date (newest first)
  opencode-sessions --sort-tokens      # sort by token count (highest first)
  opencode-sessions --sort-cost        # sort by cost (highest first)
  opencode-sessions --sort-messages    # sort by message count (highest first)
  opencode-sessions --stats            # session count per project
  opencode-sessions --delete <name>    # delete by name or UUID
  opencode-sessions --delete-unnamed   # delete all without custom name
  
Installation commands:
  opencode-sessions --install          # install for current user
  opencode-sessions --install-system   # install system-wide (requires sudo)
  opencode-sessions --uninstall        # uninstall from current user
  opencode-sessions --uninstall-system # uninstall system-wide (requires sudo)
"""

import sqlite3
import os
import sys
import json
from datetime import datetime
from collections import Counter

DB_PATH = os.path.expanduser("~/.local/share/opencode/opencode.db")
SESSION_DIFF_DIR = os.path.expanduser("~/.local/share/opencode/storage/session_diff")


def load_sessions():
    """Load all sessions from opencode database with token statistics"""
    sessions = []
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, title, directory, time_created, time_updated 
            FROM session 
            WHERE title IS NOT NULL AND title != ''
            ORDER BY time_created DESC
        """)
        
        for row in cursor.fetchall():
            session_id, title, directory, time_created, time_updated = row
            
            # Get token statistics for this session
            cursor.execute("""
                SELECT data FROM message WHERE session_id = ?
            """, (session_id,))
            
            total_tokens = 0
            total_cost = 0.0
            message_count = 0
            
            for (data_json,) in cursor.fetchall():
                try:
                    data = json.loads(data_json)
                    message_count += 1
                    
                    # Extract tokens
                    if "tokens" in data:
                        tokens = data["tokens"]
                        if isinstance(tokens, dict):
                            if "total" in tokens:
                                total_tokens += tokens["total"]
                            elif "input" in tokens and "output" in tokens:
                                total_tokens += tokens.get("input", 0) + tokens.get("output", 0)
                    
                    # Extract cost
                    if "cost" in data and isinstance(data["cost"], (int, float)):
                        total_cost += float(data["cost"])
                except (json.JSONDecodeError, KeyError, TypeError):
                    continue
            
            sessions.append({
                "id": session_id,
                "title": title,
                "directory": directory,
                "time_created": time_created,
                "time_updated": time_updated,
                "total_tokens": total_tokens,
                "total_cost": total_cost,
                "message_count": message_count,
            })
        
        conn.close()
    except sqlite3.Error as e:
        print(f"Error reading database: {e}", file=sys.stderr)
        sys.exit(1)
    
    return sessions


def delete_session(session):
    """Delete a session from database and files"""
    session_id = session["id"]
    
    # Delete from database
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Delete related records
        cursor.execute("DELETE FROM session WHERE id = ?", (session_id,))
        cursor.execute("DELETE FROM message WHERE session_id = ?", (session_id,))
        cursor.execute("DELETE FROM part WHERE session_id = ?", (session_id,))
        cursor.execute("DELETE FROM todo WHERE session_id = ?", (session_id,))
        cursor.execute("DELETE FROM session_share WHERE session_id = ?", (session_id,))
        cursor.execute("DELETE FROM session_entry WHERE session_id = ?", (session_id,))
        
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Error deleting from database: {e}", file=sys.stderr)
        return False
    
    # Delete session_diff file
    session_file = os.path.join(SESSION_DIFF_DIR, f"{session_id}.json")
    if os.path.exists(session_file):
        try:
            os.remove(session_file)
        except OSError as e:
            print(f"Error deleting session file: {e}", file=sys.stderr)
    
    return True


def confirm(prompt):
    """Ask for confirmation"""
    try:
        return input(prompt).strip().lower() in ("y", "yes")
    except (EOFError, KeyboardInterrupt):
        return False


def format_number(num):
    """Format number with K/M suffix"""
    if num >= 1_000_000:
        return f"{num/1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num/1_000:.1f}K"
    return str(num)


def cmd_print(sessions, show_all, sort_date=False, sort_tokens=False, sort_cost=False, sort_messages=False):
    """Print sessions list in table format with statistics"""
    cwd = os.getcwd()
    
    # Filter sessions
    if show_all:
        filtered = sessions
    else:
        filtered = []
        for s in sessions:
            if s["directory"] and (s["directory"] == cwd or s["directory"].startswith(cwd + "/")):
                filtered.append(s)
    
    if not filtered:
        label = "all projects" if show_all else cwd
        print(f"No sessions for {label}")
        return
    
    # Sort sessions
    if sort_date:
        filtered.sort(key=lambda s: s["time_created"] or 0, reverse=True)
    elif sort_tokens:
        filtered.sort(key=lambda s: s["total_tokens"] or 0, reverse=True)
    elif sort_cost:
        filtered.sort(key=lambda s: s["total_cost"] or 0, reverse=True)
    elif sort_messages:
        filtered.sort(key=lambda s: s["message_count"] or 0, reverse=True)
    else:
        filtered.sort(key=lambda s: s["title"].lower())
    
    # Print header
    label = "all projects" if show_all else cwd
    print(f"Sessions ({label}):\n")
    
    # Calculate column widths
    max_title_len = max(len(s["title"][:40] if s["title"] else "(unnamed)") for s in filtered)
    max_title_len = min(max_title_len, 40)
    
    # Print table header
    print(f"{'Title':<{max_title_len}} {'Tokens':>10} {'Msgs':>6} {'Cost':>10} {'Date':>16}")
    print("-" * (max_title_len + 10 + 6 + 10 + 16 + 4))
    
    # Print table rows
    for s in filtered:
        title = s["title"][:max_title_len] if s["title"] else "(unnamed)"
        
        # Format tokens
        if s["total_tokens"] > 0:
            tokens_str = format_number(s["total_tokens"])
        else:
            tokens_str = "-"
        
        # Format messages
        if s["message_count"] > 0:
            msgs_str = str(s["message_count"])
        else:
            msgs_str = "-"
        
        # Format cost
        if s["total_cost"] > 0:
            cost_str = f"${s['total_cost']:.4f}"
        else:
            cost_str = "-"
        
        # Format date
        date_str = ""
        if s["time_created"]:
            try:
                dt = datetime.fromtimestamp(s["time_created"] / 1000)
                date_str = dt.strftime('%Y-%m-%d %H:%M')
            except Exception:
                date_str = "-"
        
        # Print row
        print(f"{title:<{max_title_len}} {tokens_str:>10} {msgs_str:>6} {cost_str:>10} {date_str:>16}")
    
    # Calculate and print totals
    total_tokens = sum(s["total_tokens"] for s in filtered)
    total_cost = sum(s["total_cost"] for s in filtered)
    total_messages = sum(s["message_count"] for s in filtered)
    
    print("-" * (max_title_len + 10 + 6 + 10 + 16 + 4))
    print(f"{'TOTAL':<{max_title_len}} {format_number(total_tokens):>10} {total_messages:>6} ${total_cost:.4f} {'':>16}")


def cmd_stats(sessions):
    """Show detailed session statistics in table format"""
    counts = Counter(s["directory"] for s in sessions if s["directory"])
    total = len(sessions)
    
    # Calculate totals
    total_tokens = sum(s["total_tokens"] for s in sessions)
    total_cost = sum(s["total_cost"] for s in sessions)
    total_messages = sum(s["message_count"] for s in sessions)
    
    print("OVERALL STATISTICS")
    print("=" * 60)
    print(f"{'Sessions:':<15} {total}")
    print(f"{'Messages:':<15} {total_messages:,}")
    print(f"{'Tokens:':<15} {total_tokens:,}")
    print(f"{'Cost:':<15} ${total_cost:.4f}")
    print()
    
    # Sessions per project table
    print("SESSIONS PER PROJECT")
    print("=" * 60)
    print(f"{'Project':<40} {'Sessions':>8} {'Tokens':>10} {'Cost':>10}")
    print("-" * 60)
    
    for directory, count in sorted(counts.items(), key=lambda x: -x[1]):
        # Calculate stats for this directory
        dir_sessions = [s for s in sessions if s["directory"] == directory]
        dir_tokens = sum(s["total_tokens"] for s in dir_sessions)
        dir_cost = sum(s["total_cost"] for s in dir_sessions)
        
        # Shorten directory path for display
        display_dir = directory
        if len(display_dir) > 37:
            display_dir = "..." + display_dir[-34:]
        
        tokens_str = format_number(dir_tokens)
        cost_str = f"${dir_cost:.4f}" if dir_cost > 0 else "-"
        
        print(f"{display_dir:<40} {count:>8} {tokens_str:>10} {cost_str:>10}")
    
    print()
    
    # Top sessions by tokens table
    print("TOP SESSIONS BY TOKENS")
    print("=" * 60)
    print(f"{'#':<3} {'Title':<40} {'Tokens':>10} {'Cost':>10}")
    print("-" * 60)
    
    top_by_tokens = sorted(sessions, key=lambda s: s["total_tokens"], reverse=True)[:10]
    for i, s in enumerate(top_by_tokens, 1):
        if s["total_tokens"] > 0:
            title = s["title"][:37] if s["title"] else "(unnamed)"
            if len(title) < 37 and s["total_tokens"] > 0:
                title = title.ljust(37)
            
            tokens_str = format_number(s["total_tokens"])
            cost_str = f"${s['total_cost']:.4f}" if s["total_cost"] > 0 else "-"
            
            print(f"{i:>2}. {title:<40} {tokens_str:>10} {cost_str:>10}")
    
    print()
    
    # Top sessions by cost table
    print("TOP SESSIONS BY COST")
    print("=" * 60)
    print(f"{'#':<3} {'Title':<40} {'Cost':>10} {'Tokens':>10}")
    print("-" * 60)
    
    top_by_cost = sorted(sessions, key=lambda s: s["total_cost"], reverse=True)[:10]
    for i, s in enumerate(top_by_cost, 1):
        if s["total_cost"] > 0:
            title = s["title"][:37] if s["title"] else "(unnamed)"
            if len(title) < 37:
                title = title.ljust(37)
            
            cost_str = f"${s['total_cost']:.4f}"
            tokens_str = format_number(s["total_tokens"])
            
            print(f"{i:>2}. {title:<40} {cost_str:>10} {tokens_str:>10}")


def cmd_rm(sessions, query=None):
    """Delete sessions by name or UUID"""
    cwd = os.getcwd()
    
    # Filter sessions for current directory
    pool = [s for s in sessions if s["directory"] and 
            (s["directory"] == cwd or s["directory"].startswith(cwd + "/"))]
    
    if query:
        # Find matching sessions
        matches = []
        for s in pool:
            if (query.lower() in s["title"].lower() if s["title"] else False) or query == s["id"]:
                matches.append(s)
        
        if not matches:
            print(f"No sessions matching: {query}")
            return
    else:
        # Interactive selection with fzf
        lines = [f"{s['title'][:80] if s['title'] else '(unnamed)':<50} {s['id']}" for s in pool]
        if not lines:
            print("No sessions found.")
            return
        
        try:
            import subprocess
            result = subprocess.run(
                ["fzf", "--multi", "--header", "TAB to select, ENTER to confirm, ESC to cancel"],
                input="\n".join(lines),
                capture_output=True,
                text=True,
            )
            
            if result.returncode != 0 or not result.stdout.strip():
                print("Cancelled.")
                return
            
            selected_ids = {line.split()[-1] for line in result.stdout.strip().splitlines()}
            matches = [s for s in pool if s["id"] in selected_ids]
        except ImportError:
            print("Error: fzf not available for interactive selection", file=sys.stderr)
            sys.exit(1)
    
    # Show selected sessions
    print(f"Selected {len(matches)} session(s):\n")
    for s in matches:
        title = s["title"][:80] if s["title"] else "(unnamed)"
        print(f"  {title:<50} {s['id']}")
    print()
    
    # Confirm and delete
    if confirm(f"Delete {len(matches)} session(s)? [y/N] "):
        for s in matches:
            if delete_session(s):
                title = s["title"][:80] if s["title"] else "(unnamed)"
                print(f"Deleted: {title}")
    else:
        print("Cancelled.")


def cmd_rm_unnamed(sessions):
    """Delete all unnamed sessions"""
    # Find sessions with default "New session" titles
    matches = []
    for s in sessions:
        title = s["title"]
        if title and title.startswith("New session - "):
            matches.append(s)
    
    if not matches:
        print("No unnamed sessions found.")
        return
    
    print(f"Sessions without custom name ({len(matches)}):\n")
    for s in matches:
        print(f"  {s['title'][:80]:<50} {s['id']}")
    print()
    
    if confirm(f"Delete {len(matches)} session(s)? [y/N] "):
        for s in matches:
            if delete_session(s):
                print(f"Deleted: {s['title'][:80]}")
    else:
        print("Cancelled.")


def install_script(system=False):
    """Install opencode-sessions"""
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    script_name = os.path.basename(script_path)
    completion_name = "opencode-sessions.fish"
    
    # Installation paths
    if system:
        if os.geteuid() != 0:
            print("System installation requires root privileges. Use sudo.")
            sys.exit(1)
        install_dir = "/usr/local/bin"
        completion_dir = "/etc/fish/completions"
    else:
        install_dir = os.path.expanduser("~/.local/bin")
        completion_dir = os.path.expanduser("~/.config/fish/completions")
    
    print(f"Installing {script_name}...")
    
    # Create directories
    os.makedirs(install_dir, exist_ok=True)
    if os.path.exists(os.path.dirname(completion_dir)):
        os.makedirs(completion_dir, exist_ok=True)
    
    # Install main script
    dest_script = os.path.join(install_dir, script_name)
    print(f"Copying {script_name} to {dest_script}")
    
    # Read current script content
    with open(script_path, 'r') as f:
        script_content = f.read()
    
    # Write to destination
    with open(dest_script, 'w') as f:
        f.write(script_content)
    
    # Make executable
    os.chmod(dest_script, 0o755)
    
    # Install fish completion if available
    completion_src = os.path.join(script_dir, completion_name)
    if os.path.exists(completion_src):
        dest_completion = os.path.join(completion_dir, completion_name)
        print(f"Copying {completion_name} to {dest_completion}")
        with open(completion_src, 'r') as f:
            completion_content = f.read()
        with open(dest_completion, 'w') as f:
            f.write(completion_content)
        print("Fish completion installed. Restart your shell or run: source ~/.config/fish/config.fish")
    
    print(f"\nInstallation complete!")
    print(f"You can now use: {script_name}")
    print(f"Try: {script_name} --help")


def uninstall_script(system=False):
    """Uninstall opencode-sessions"""
    script_name = os.path.basename(__file__)
    completion_name = "opencode-sessions.fish"
    
    # Installation paths
    if system:
        if os.geteuid() != 0:
            print("System uninstallation requires root privileges. Use sudo.")
            sys.exit(1)
        install_dir = "/usr/local/bin"
        completion_dir = "/etc/fish/completions"
    else:
        install_dir = os.path.expanduser("~/.local/bin")
        completion_dir = os.path.expanduser("~/.config/fish/completions")
    
    print(f"Uninstalling {script_name}...")
    
    # Remove main script
    script_path = os.path.join(install_dir, script_name)
    if os.path.exists(script_path):
        print(f"Removing {script_path}")
        os.remove(script_path)
    else:
        print(f"{script_path} not found")
    
    # Remove fish completion
    completion_path = os.path.join(completion_dir, completion_name)
    if os.path.exists(completion_path):
        print(f"Removing {completion_path}")
        os.remove(completion_path)
    else:
        print(f"{completion_path} not found")
    
    print("Uninstallation complete!")


def main():
    args = sys.argv[1:]
    
    # Check for installation commands first
    if "--install" in args:
        install_script(system=False)
        return
    elif "--install-system" in args:
        install_script(system=True)
        return
    elif "--uninstall" in args:
        uninstall_script(system=False)
        return
    elif "--uninstall-system" in args:
        uninstall_script(system=True)
        return
    
    # Load sessions for regular commands
    sessions = load_sessions()
    
    # Check for sort flags
    sort_date = "--sort-date" in args
    sort_tokens = "--sort-tokens" in args
    sort_cost = "--sort-cost" in args
    sort_messages = "--sort-messages" in args
    
    # Handle regular commands
    if "--help" in args or "-h" in args:
        print(__doc__)
    elif "--stats" in args:
        cmd_stats(sessions)
    elif not args or any(arg in args for arg in ["--sort-date", "--sort-tokens", "--sort-cost", "--sort-messages"]):
        cmd_print(sessions, show_all=False, 
                 sort_date=sort_date, sort_tokens=sort_tokens, 
                 sort_cost=sort_cost, sort_messages=sort_messages)
    elif "--print-all" in args:
        cmd_print(sessions, show_all=True,
                 sort_date=sort_date, sort_tokens=sort_tokens,
                 sort_cost=sort_cost, sort_messages=sort_messages)
    elif "--delete-unnamed" in args:
        cmd_rm_unnamed(sessions)
    elif "--delete" in args:
        idx = args.index("--delete")
        rest = args[idx + 1:]
        cmd_rm(sessions, " ".join(rest) if rest else None)
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()