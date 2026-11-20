# 4. MCP servers

Register MCP servers in the JFrog AI Security registry, then discover, install and run them from your
coding agent.

## Add servers to the registry

**If you already use MCP servers,** register the ones in your current user or workspace settings:

- **Marketplace servers:** add pre-built servers from the AI Security Marketplace.
- **Custom, local or remote servers:** use **Add AI Asset** to register internal servers or remote
  endpoints, such as an internal MCP gateway.

**If you're starting fresh,** add two test servers:

- **A local server:** install `chrome-devtools` or `playwright-mcp` from the Marketplace.
- **A remote server:** use **Add AI Asset** to configure a remote endpoint.

> [!IMPORTANT]
> Enterprise login (OAuth / OIDC) for remote MCP servers works only if your identity provider supports
> Dynamic Client Registration (DCR). If it doesn't, configure static client credentials or an API key
> header instead.

## Use them from your coding agent

1. **Discover.** Ask your agent: *"List all available MCP servers in the JFrog AI Catalog."* Check that
   the servers you registered appear.
2. **Install.** Ask the agent to install one of them at the project / workspace level.
3. **Check the config.** Open the project's MCP config (`.vscode/mcp.json`, `.cursor/mcp.json` or your
   agent's equivalent) and confirm the command, arguments and environment variables were filled in.
4. **Reload.** Restart the agent or open a new session so it picks up the server.
5. **Start it and watch the logs.**
   - **VS Code:** run **MCP: List Servers**, start the server, and watch the **Output** panel for startup
     logs and the list of tools.
   - **Claude Code:** MCP logs don't appear in the session. If tools are missing, run
     `claude --debug mcp` in a terminal and ask the agent where the error log for that run is.

---

**Previous:** [← 3. Access and authentication](03-access-and-auth.md) · **Next:** [5. Agent skills →](05-agent-skills.md)
