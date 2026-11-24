# 1. Prerequisites

Get the JFrog Platform ready before you start testing. Most of these are one-time steps for an
administrator, and every later guide assumes they're done.

**Checklist**

- [ ] [Confirm your entitlements with JFrog](#confirm-your-entitlements-with-jfrog)
- [ ] [Sign the AI Addendum](#sign-the-ai-addendum)
- [ ] [Enable the Skills enforcement preview](#enable-the-skills-enforcement-preview)
- [ ] [Turn on Curation](#turn-on-curation)
- [ ] [Create an evaluation project](#create-an-evaluation-project)
- [ ] [Enable the MCP Registry](#enable-the-mcp-registry)
- [ ] [Pick a supported coding agent](#pick-a-supported-coding-agent)

## Confirm your entitlements with JFrog

**Who:** you, with your JFrog account team.

Ask your account team to confirm two things on your instance:

- **AI scanning is enabled.** The skill scanner in guide 5 depends on it.
- **JFrog Curation is active.** JFrog AI Security enforces its decisions through Curation: a blocked model
  or package is refused at download time by Curation. It's required for the trial, so if it isn't active,
  ask your customer success manager or account manager to help.

## Sign the AI Addendum

**Who:** the MyJFrog Primary Admin. No one else can do this.

Without it, skills are registered but never scanned.

1. Go to [MyJFrog](https://my.jfrog.com) and open **Settings → AI**.
2. Approve the **AI Addendum**. JFrog AI is now enabled on all your instances.

If **Require JPD level activation** is selected on that page, also click **Ask AI** in the top bar of your
JFrog Platform and approve JFrog AI there. If the AI settings aren't in MyJFrog, for example on a
self-hosted instance, ask your JFrog account team how to enable them.
[Docs](https://docs.jfrog.com/setup/docs/jfrog-ai-assistant)

## Enable the Skills enforcement preview

**Who:** a MyJFrog admin.

Without it, skill policies exist but never block anything.

1. In MyJFrog, go to **Settings → Preview**.
2. Turn on the **Enable Preview** toggle.
3. Read the **Preview Terms of Service**, select the checkbox and click **Agree and Enable**.
4. In the list of preview features, turn on **Skills enforcement**.

[Docs](https://docs.jfrog.com/administration/docs/preview-jfrog-features)

## Turn on Curation

**Who:** a JFrog Platform admin.

1. In the JFrog Platform, go to **Administration → Curation → General**.
2. Turn the **Curation** switch on.

That's all for now. Connecting your Hugging Face repositories to Curation is part of
[guide 6](06-governed-models.md). [Docs](https://docs.jfrog.com/security/docs/general)

## Create an evaluation project

**Who:** a Platform Admin.

JFrog AI Security is evaluated inside a JFrog Project: MCP servers, skills and models are allowed per
project. Create a new project just for the evaluation, even if your organization already uses projects,
so its policies don't affect anyone else.

1. In the JFrog Platform, go to **Administration → All Projects** and click **+ Create New**.
2. Enter a **Project Name** and a **Project Key**, for example `ai-poc`. The key is 2 to 32 lowercase
   letters, digits and hyphens, and starts with a letter. It's used as a prefix for the project's
   resources: the skills repository in guide 5, for example, is named `<key>-skills-local`.
3. Under **Project Admins**, add yourself and anyone else running the evaluation.
4. Leave the other settings as they are and click **Create**.

The developer user who tests from a coding agent is added to the project in
[guide 3](03-access-and-auth.md). [Docs](https://docs.jfrog.com/projects/docs/create-a-project)

## Enable the MCP Registry

**Who:** a JFrog Platform admin.

1. In the JFrog Platform, go to **Administration → AI/ML Settings → Coding Assistants**.
2. Click **Enable MCP Registry** at the top of the page, then **Activate**.

## Pick a supported coding agent

**Who:** whoever will test as the developer.

Install one of VS Code with GitHub Copilot Chat, Claude Code, or Cursor. Guide 2 connects it to JFrog.
See [Supported coding agents and deployments](https://docs.jfrog.com/ai-ml/docs/supported-coding-agents-and-deployments)
for versions.

> [!NOTE]
> You don't need to install the JFrog CLI. The JFrog plugin installs it when you initialize the plugin in
> [guide 3](03-access-and-auth.md). To install it yourself instead, see
> [JFrog CLI](https://docs.jfrog.com/getting-started/docs/jfrog-cli).

---

**Next:** [2. Coding agent setup →](02-coding-agent-setup.md)
