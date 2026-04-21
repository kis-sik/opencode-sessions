// OpenCode plugin for enhanced session management
// Place in ~/.config/opencode/plugins/ or .opencode/plugins/

export const OCSPlugin = async ({ project, client, $, directory, worktree }) => {
  console.log("OCS Plugin initialized")
  
  return {
    // Add custom commands to opencode
    "tui.command.execute": async (input, output) => {
      const command = input.command.trim()
      
      // Handle custom session commands
      if (command.startsWith("/ocs-stats")) {
        output.handled = true
        
        try {
          // Run our opencode-sessions script
          const result = await $`ocs --stats`
          await client.app.log({
            body: {
              service: "opencode-sessions-plugin",
              level: "info",
              message: "Session statistics generated"
            }
          })
          
          // Return the result to be displayed
          return result.stdout
        } catch (error) {
          await client.app.log({
            body: {
              service: "opencode-sessions-plugin",
              level: "error",
              message: "Failed to get session stats",
              error: error.message
            }
          })
          return `Error getting session stats: ${error.message}`
        }
      }
      
      if (command.startsWith("/ocs-list")) {
        output.handled = true
        
        try {
          // Parse optional arguments
          const args = command.split(" ").slice(1)
          let opencodeArgs = ""
          
          if (args.includes("--all")) {
            opencodeArgs += " --print-all"
          }
          if (args.includes("--sort-tokens")) {
            opencodeArgs += " --sort-tokens"
          }
          if (args.includes("--sort-cost")) {
            opencodeArgs += " --sort-cost"
          }
          if (args.includes("--sort-date")) {
            opencodeArgs += " --sort-date"
          }
          if (args.includes("--sort-messages")) {
            opencodeArgs += " --sort-messages"
          }
          
            const result = await $`ocs ${opencodeArgs}`
          await client.app.log({
            body: {
              service: "ocs-plugin",
              level: "info",
              message: "Detailed session list generated"
            }
          })
          
          return result.stdout
        } catch (error) {
          await client.app.log({
            body: {
              service: "opencode-sessions-plugin",
              level: "error",
              message: "Failed to get session list",
              error: error.message
            }
          })
          return `Error getting session list: ${error.message}`
        }
      }
      
      if (command.startsWith("/ocs-delete")) {
        output.handled = true
        
        try {
          const args = command.split(" ").slice(1)
          if (args.length === 0) {
            return "Usage: /session-delete <session-name-or-id> or /session-delete --interactive"
          }
          
          let opencodeArgs = "--delete"
          if (args[0] === "--interactive" || args[0] === "-i") {
            opencodeArgs = "--delete"
          } else if (args[0] === "--unnamed") {
            opencodeArgs = "--delete-unnamed"
          } else {
            opencodeArgs = `--delete "${args.join(' ')}"`
          }
          
            const result = await $`ocs ${opencodeArgs}`
          await client.app.log({
            body: {
              service: "ocs-plugin",
              level: "info",
              message: "Session deletion executed"
            }
          })
          
          return result.stdout
        } catch (error) {
          await client.app.log({
            body: {
              service: "opencode-sessions-plugin",
              level: "error",
              message: "Failed to delete session",
              error: error.message
            }
          })
          return `Error deleting session: ${error.message}`
        }
      }
    },
    
    // Add help text for our custom commands
    "tui.prompt.append": async (input, output) => {
      output.append(`
Available OCS commands:
  /ocs-stats                 - Show detailed session statistics
  /ocs-list                  - Show sessions with token/cost metrics
    Options: --all, --sort-tokens, --sort-cost, --sort-date, --sort-messages
  /ocs-delete <name|id>      - Delete session by name or ID
    Options: --interactive, --unnamed
      
These commands use the ocs tool for enhanced session management.
`)
    },
    
    // Log when sessions are created/deleted
    "session.created": async ({ event }) => {
      await client.app.log({
        body: {
          service: "ocs-plugin",
          level: "info",
          message: "New session created",
          sessionId: event.session.id,
          title: event.session.title
        }
      })
    },
    
    "session.deleted": async ({ event }) => {
      await client.app.log({
        body: {
          service: "ocs-plugin",
          level: "info",
          message: "Session deleted",
          sessionId: event.session.id
        }
      })
    }
  }
}