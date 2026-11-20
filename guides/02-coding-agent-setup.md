# 2. Coding agent setup

Push the JFrog plugin to the developer's coding agent and restrict the agent to MCP servers approved in
JFrog.

> [!NOTE]
> For a POC, you apply this configuration in your own user settings. In production, the same configuration
> is generated under **Administration → AI/ML Settings → Coding Assistants** and rolled out centrally to
> developer machines through MDM or enterprise settings.

The configuration refers to a JFrog CLI server ID, written as `<YOUR-SERVER>` below. You create it in the
[next guide](03-access-and-auth.md). Use your SaaS prefix: if your instance is `mycompany.jfrog.io`, use
`mycompany`.

Pick the section for your agent.

## VS Code (GitHub Copilot Chat)

Requires VS Code 1.133 or later.

1. Press <kbd>Ctrl</kbd>/<kbd>Cmd</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd> and run **Preferences: Open User Settings (JSON)**.
2. Add the following at the root of the file. Replace `<YOUR-SERVER>` with your server ID and
   `<your-instance-prefix>` with your instance prefix:

   ```json
   "chat.mcp.allowedServers": [
     {
       "serverCommand": [
         "npx", "--yes",
         "--registry", "https://releases.jfrog.io/artifactory/api/npm/coding-agents-npm/",
         "@jfrog/agent-guard",
         "--server", "<YOUR-SERVER>"
       ]
     },
     { "serverUrl": "https://<your-instance-prefix>.jfrog.io/mcp" }
   ],
   "chat.plugins.enabled": true,
   "chat.plugins.marketplaces": ["jfrog/vscode-plugin"]
   ```

3. Save, then run **Developer: Reload Window**.

From now on, VS Code blocks any MCP server that doesn't match these entries from installing or starting.

## Claude Code

1. In the JFrog UI, open **All Projects → Administration → AI/ML Settings → Coding Assistants** (bottom
   left).
2. Select **Claude** and copy the generated configuration.
3. Paste it into your Claude Code settings: `~/.claude/settings.json` for all projects, or
   `.claude/settings.json` inside a single project.

## Cursor

Follow [Enforce JFrog-governed MCP usage in Cursor](https://docs.jfrog.com/ai-ml/docs/cursor-enforce-jfrog-governed-mcp-usage).

---

**Previous:** [← 1. Prerequisites](01-prerequisites.md) · **Next:** [3. Access and authentication →](03-access-and-auth.md)
