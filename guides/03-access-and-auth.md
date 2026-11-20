# 3. Access and authentication

Create a scoped developer user, connect the JFrog CLI with it, and confirm the coding agent can reach
JFrog.

Use a dedicated user with limited privileges rather than an administrator account. That way you see
permissions, tool discovery and security controls the way a real developer would. Skill scanning also
requires it.

## Create the developer user

1. In the JFrog UI, open **All Projects → Administration → User Management → Users → New User**.
2. Create a user such as `dev-user` or `ai-user`. Don't give it any global permissions or admin roles.
3. Open your evaluation project and go to **Administration → User Management → Members → Add Members**.
4. Add the new user with the **Developer** and **Model Developer** project roles.

## Generate an access token

1. Go to **All Projects → Administration → User Management → Access Tokens → Generate Token**.
2. Under **Token Scope**, select **User** and pick the developer user.
3. Generate the token and store it somewhere safe.

## Connect the JFrog CLI

If you didn't install the JFrog CLI yourself, run `/jfrog:jfrog-init` in your coding agent first: the
JFrog plugin installs the CLI during initialization. Then add your server:

```bash
jf config add --interactive
```

- **Server ID:** your SaaS prefix (for `mycompany.jfrog.io`, use `mycompany`).
- **URL:** the full URL of your instance.
- **Authentication:** choose **Access Token** and paste the token from the previous step.

> [!IMPORTANT]
> The server ID must exactly match the one in the settings you pushed in
> [coding agent setup](02-coding-agent-setup.md) (`<YOUR-SERVER>`). If they differ, the agent won't
> recognize the MCP servers as allowed.

## Verify from your coding agent

In your coding agent, run:

```text
/jfrog:jfrog-init
```

Follow the prompts. The skill checks your CLI setup, server reachability, project binding and AI Security
entitlement, and walks you through anything that's missing.

---

**Previous:** [← 2. Coding agent setup](02-coding-agent-setup.md) · **Next:** [4. MCP servers →](04-mcp-servers.md)
