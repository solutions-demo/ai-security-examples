# 1. Prerequisites

Get the JFrog Platform ready before you start testing. Everything in later guides assumes these are in
place.

| Requirement | What to do |
|-------------|------------|
| **A dedicated JFrog Project** | AI Security is evaluated inside a JFrog Project. If your organization already uses projects, create a new one just for this evaluation. If not, create your first project before continuing. |
| **AI scanning enabled** | Ask your JFrog account team to confirm that AI scanning is enabled on your Artifactory instance. |
| **AI Addendum signed** | In MyJFrog, go to **Settings → AI → Enable AI** and accept the AI Addendum ([docs](https://docs.jfrog.com/setup/docs/jfrog-ai-assistant)). Only the instance's Primary Admin can do this. Without it, skills are registered but never scanned. If the option isn't there, for example on a self-hosted instance, ask your JFrog account team how to enable it in MyJFrog. |
| **Skills enforcement preview** | In MyJFrog, go to **Settings → Preview** and enable **Skills enforcement** ([docs](https://docs.jfrog.com/administration/docs/preview-jfrog-features)). |
| **A supported coding agent** | For example VS Code with GitHub Copilot Chat, Claude Code, or Cursor. See [Supported coding agents and deployments](https://docs.jfrog.com/ai-ml/docs/supported-coding-agents-and-deployments). |
| **JFrog CLI** *(optional)* | Nothing to do up front: the JFrog plugin installs the CLI automatically when you initialize it in [guide 3](03-access-and-auth.md). To install it yourself instead, see [JFrog CLI](https://docs.jfrog.com/getting-started/docs/jfrog-cli). |

---

**Next:** [2. Coding agent setup →](02-coding-agent-setup.md)
