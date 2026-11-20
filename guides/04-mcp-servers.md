# 4. MCP servers

MCP servers give coding agents new tools: a browser, your issue tracker, your database. Each one can
read data and take actions with the developer's permissions. In this guide you put them under governance.
You register servers in the JFrog MCP Registry, decide which tools agents may call, and install them
from the coding agent. Every server is blocked until an admin allows it for a project, and Agent Guard
enforces your policy on every tool call.

> [!IMPORTANT]
> Before you start, complete [coding agent setup](02-coding-agent-setup.md) and
> [access and authentication](03-access-and-auth.md), and enable the MCP Registry
> ([prerequisites](01-prerequisites.md)). The agent needs the JFrog plugin, and its server ID must match
> your JFrog CLI server ID, or none of the servers below will show up as allowed.

## Two kinds of MCP servers

| | Third-party | Custom |
|---|---|---|
| **What** | Public servers from the JFrog Marketplace, scanned for malware and license issues before you allow them | Servers your team owns: a remote endpoint you already use, or an npm/PyPI package in your Artifactory |
| **Where** | **AI/ML → AI Catalog → Marketplace → MCP Servers** | **AI/ML → AI Catalog → Registry → Add AI Asset → Add MCP Server** |
| **Try it with** | Chrome DevTools (part 1) | A remote server you use today (part 3) |

## Part 1: Add a third-party server (Chrome DevTools)

Start with Chrome DevTools. It runs locally, needs no login, and has many tools to experiment with in
part 2.

**In the JFrog UI:**

1. Go to **AI/ML → AI Catalog → Marketplace → MCP Servers** and search for **Chrome DevTools**.
2. Click **Add to Registry** and select your evaluation project.
3. For the tool policy, keep **Allow all tools** for now.
4. Click **Next**, then **Save configuration**.

**In your coding agent:**

1. Ask: *"List all available MCP servers in the JFrog AI Catalog."* Chrome DevTools should be listed
   under **Available from JFrog**.
2. Ask: *"Add the Chrome DevTools MCP server."*
3. Start a new session so the agent loads it.
4. Try it: *"Open https://jfrog.com and take a screenshot."*

## Part 2: Restrict its tools

Tool policies decide which of a server's tools agents may call, per server and per project. Changes reach
developers' agents right away.

1. Go to **AI/ML → AI Catalog → Registry**, open Chrome DevTools, and select your project.
2. On the **MCP Server Info** tab, click **Edit**, then **Select tools manually**.
3. Choose a list type and add entries, either exact tool names or regular expressions:
   - **Allow List:** only the listed tools work; everything else is blocked.
   - **Block List:** the listed tools are blocked; everything else works.
4. Click **Next**, then **Save Configuration**.

Some policies to try on Chrome DevTools:

| Goal | List | Entry | Effect |
|------|------|-------|--------|
| Block running arbitrary code and uploading local files | Block | `^(evaluate_script\|upload_file)$` | Everything else still works |
| Read-only browsing | Allow | `^(navigate_page\|list_.*\|get_.*\|take_.*)$` | The agent can open pages, read console and network logs and take screenshots, but can't type, click or run scripts |

Then check the policy from your agent. With the block list in place, ask *"Run `document.title` as
JavaScript on the current page"*: the agent can't. Ask for a screenshot: it still works.

> [!TIP]
> Patterns use RE2 syntax. Anchor them with `^` and `$`: a loose pattern like `get` also matches any tool
> with "get" anywhere in its name.

## Part 3: Add a remote server you already use

Now register a server your team relies on today, such as your issue tracker, wiki or an internal MCP
gateway, and include its authentication.

1. Go to **AI/ML → AI Catalog → Registry → Add AI Asset → Add MCP Server** and open the
   **Remote (Endpoint)** tab.
2. Fill in **Project**, **MCP Server Name**, **Endpoint URL**, **Transport Protocol** (**SSE** or
   **Streamable HTTP**) and **Description**. The JFrog Platform must be able to reach the endpoint.
3. Click **Next** and set a tool policy, as in part 2.
4. Configure authentication (see below), then click **Complete Registration**.
5. Install it from your agent as in part 1.

**Authentication options:**

- **OAuth (easiest).** Nothing to configure during registration. When a developer first uses the server,
  the agent asks to connect and opens a browser for login. Agent Guard stores and refreshes the token.
  This requires the server to support Dynamic Client Registration (DCR). To log in, ask the agent
  (*"Log in to the Jira MCP server"*); don't use the IDE's own **MCP Auth** button.
- **Token header.** For servers that use an API key or bearer token. In the **Configuration** step,
  click **Add Header** and define it, for example **Header name** `Authorization`, with **Required** and
  **Secret** turned on. The registry stores only the header definition. Each developer supplies their own
  value when connecting, and the agent gives them a terminal command for secret values rather than asking
  for them in chat.

> [!NOTE]
> You can also register a local custom server packaged as npm or PyPI in an Artifactory local repository.
> See [Register local custom MCP servers](https://docs.jfrog.com/ai-ml/docs/local-custom-mcp-servers).

## Troubleshooting

- **A server isn't listed in the agent:** check it's allowed for your project and ask the agent
  *"Which project am I working in?"*. Then compare the server ID in your coding agent settings from
  [guide 2](02-coding-agent-setup.md) with the `--server` value in the project's MCP config file
  (`.vscode/mcp.json`, `.cursor/mcp.json` or `.mcp.json`). They must match.
- **A local server won't start:** Agent Guard doesn't install runtimes. Make sure Node.js 18+ with `npx`,
  or Python, is installed.
- **VS Code:** press <kbd>Ctrl</kbd>/<kbd>Cmd</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd>, run
  **MCP: List Servers**, start the server and watch the **Output** panel.
- **Claude Code:** MCP logs don't appear in the session. Run `claude --debug mcp` and ask the agent where
  the error log is.

See also: [MCP Registry overview](https://docs.jfrog.com/ai-ml/docs/mcp-registry-overview) ·
[Tool policies](https://docs.jfrog.com/ai-ml/docs/configure-tool-policies) ·
[Remote server authentication](https://docs.jfrog.com/ai-ml/docs/authenticate-remote-mcp-tools-in-agent-guard) ·
[Troubleshooting](https://docs.jfrog.com/ai-ml/docs/mcp-registry-troubleshoot)

---

**Previous:** [← 3. Access and authentication](03-access-and-auth.md) · **Next:** [5. Agent skills →](05-agent-skills.md)
