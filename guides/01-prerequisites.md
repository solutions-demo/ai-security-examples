# 1. Prerequisites

Before you test anything, a few things need to be switched on. Some are a request to your JFrog account
team, some are one-time admin setup, and the rest is on the developer's machine. Every later guide
assumes they're done.

| | Requirement | What it takes | Why |
|---|---|---|---|
| Required | AI scanning enabled | JFrog team request | The skill scanner in guide 5 depends on it |
| Required | JFrog Curation active | JFrog team request | Curation enforces JFrog AI Security's decisions, for example refusing a blocked model's download |
| Required | [AI Addendum accepted](#accept-the-ai-addendum) | Admin setup in MyJFrog | Without it, skills are never scanned |
| Required | [Skills enforcement preview](#turn-on-skills-enforcement) | Admin setup in MyJFrog | Without it, skill policies never block anything |
| Required | [Curation turned on](#turn-on-curation) | Admin setup in the JFrog Platform | Activates Curation on your instance |
| Required | [MCP Registry enabled](#enable-the-mcp-registry) | Admin setup in the JFrog Platform | Needed to govern MCP servers in guide 4 |
| Required | [Evaluation project](#create-an-evaluation-project) | Admin setup in the JFrog Platform | MCP servers, skills and models are all allowed per project |
| Required | [Supported coding agent](https://docs.jfrog.com/ai-ml/docs/supported-coding-agents-and-deployments) | Install on your machine | VS Code with GitHub Copilot Chat, Claude Code or Cursor, connected in guide 2 |
| *Optional* | [JFrog CLI](https://docs.jfrog.com/getting-started/docs/jfrog-cli) | Install on your machine | The JFrog plugin installs it for you in guide 3 |

## JFrog team requests

Ask your JFrog account team to confirm that AI scanning is enabled and Curation is active on your
instance. Curation is required for the trial: if it isn't active, your customer success manager or
account manager can help.

## Admin setup

### Accept the AI Addendum

Only the MyJFrog **Primary Admin** can do this.

1. In [MyJFrog](https://my.jfrog.com), go to **Settings → AI**.
2. Approve the **AI Addendum**. JFrog AI is now enabled on all your instances.

If **Require JPD level activation** is selected on that page, also click **Ask AI** in the top bar of your
JFrog Platform and approve JFrog AI there. If there's no AI page in MyJFrog, for example on a self-hosted
instance, ask your account team how to enable it.
See [Enable JFrog AI](https://docs.jfrog.com/setup/docs/jfrog-ai-assistant).

### Turn on Skills enforcement

1. In MyJFrog, go to **Settings → Preview** and turn on **Enable Preview**.
2. Accept the Preview Terms of Service and click **Agree and Enable**.
3. In the list of preview features, turn on **Skills enforcement**.

See [JFrog Preview](https://docs.jfrog.com/administration/docs/preview-jfrog-features).

### Turn on Curation

In the JFrog Platform, go to **Administration → Curation → General** and turn the **Curation** switch on.
Connecting your Hugging Face repositories to it comes later, in [guide 6](06-governed-models.md).
See [Enable the Curation service](https://docs.jfrog.com/security/docs/general).

### Enable the MCP Registry

In the JFrog Platform, go to **Administration → AI/ML Settings → Coding Assistants**, click
**Enable MCP Registry** at the top of the page, then **Activate**.

### Create an evaluation project

Create a new project for the evaluation, even if your organization already uses projects, so its
policies don't affect anyone else. You need to be a Platform Admin.

1. In the JFrog Platform, go to **Administration → All Projects** and click **+ Create New**.
2. Enter a **Project Name** and a **Project Key**, for example `ai-poc`. The key is 2 to 32 lowercase
   letters, digits and hyphens, starting with a letter, and it prefixes the project's resources. The
   skills repository in guide 5, for example, will be `ai-poc-skills-local`.
3. Under **Project Admins**, add yourself and anyone else running the evaluation.
4. Leave the rest as it is and click **Create**.

You'll add the developer user to the project in [guide 3](03-access-and-auth.md).
See [Create a project](https://docs.jfrog.com/projects/docs/create-a-project).

---

**Next:** [2. Coding agent setup →](02-coding-agent-setup.md)
