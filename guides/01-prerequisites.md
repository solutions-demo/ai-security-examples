# 1. Prerequisites

Before you test anything, a few things need to be switched on. They happen in three places: with your
JFrog account team, in MyJFrog, and in the JFrog Platform. Most are one-time steps for an administrator,
and every later guide assumes they're done.

## With your JFrog account team

Ask your account team to confirm two things on your instance:

- **AI scanning is enabled.** The skill scanner in guide 5 depends on it.
- **JFrog Curation is active.** JFrog AI Security enforces its decisions through Curation: when a model is
  blocked, it's Curation that refuses the download. Curation is required for the trial, so if it isn't
  active, ask your customer success manager or account manager to help.

## In MyJFrog

You'll need the MyJFrog **Primary Admin** for the first step, since only they can accept the AI Addendum.

### Accept the AI Addendum

Without it, skills are registered but never scanned.

1. In [MyJFrog](https://my.jfrog.com), go to **Settings → AI**.
2. Approve the **AI Addendum**. JFrog AI is now enabled on all your instances.

If **Require JPD level activation** is selected on that page, also click **Ask AI** in the top bar of your
JFrog Platform and approve JFrog AI there. If there's no AI page in MyJFrog, for example on a self-hosted
instance, ask your account team how to enable it.
See [Enable JFrog AI](https://docs.jfrog.com/setup/docs/jfrog-ai-assistant).

### Turn on Skills enforcement

Skills enforcement is a preview feature. Without it, skill policies exist but never block anything.

1. In MyJFrog, go to **Settings → Preview** and turn on **Enable Preview**.
2. Accept the Preview Terms of Service and click **Agree and Enable**.
3. In the list of preview features, turn on **Skills enforcement**.

See [JFrog Preview](https://docs.jfrog.com/administration/docs/preview-jfrog-features).

## In the JFrog Platform

These steps need a Platform Admin.

### Turn on Curation

Go to **Administration → Curation → General** and turn the **Curation** switch on. Connecting your
Hugging Face repositories to it comes later, in [guide 6](06-governed-models.md).
See [Enable the Curation service](https://docs.jfrog.com/security/docs/general).

### Enable the MCP Registry

Go to **Administration → AI/ML Settings → Coding Assistants**, click **Enable MCP Registry** at the top
of the page, then **Activate**.

### Create an evaluation project

MCP servers, skills and models are all allowed per JFrog Project, so the evaluation happens inside one.
Create a new project for it, even if your organization already uses projects, so its policies don't
affect anyone else.

1. Go to **Administration → All Projects** and click **+ Create New**.
2. Enter a **Project Name** and a **Project Key**, for example `ai-poc`. The key is 2 to 32 lowercase
   letters, digits and hyphens, starting with a letter, and it prefixes the project's resources. The
   skills repository in guide 5, for example, will be `ai-poc-skills-local`.
3. Under **Project Admins**, add yourself and anyone else running the evaluation.
4. Leave the rest as it is and click **Create**.

You'll add the developer user to the project in [guide 3](03-access-and-auth.md).
See [Create a project](https://docs.jfrog.com/projects/docs/create-a-project).

## What you'll need on your machine

A [supported coding agent](https://docs.jfrog.com/ai-ml/docs/supported-coding-agents-and-deployments):
VS Code with GitHub Copilot Chat, Claude Code, or Cursor. Guide 2 connects it to JFrog.

You don't need to install the JFrog CLI. The JFrog plugin installs it when you initialize the plugin in
[guide 3](03-access-and-auth.md). To install it yourself instead, see
[JFrog CLI](https://docs.jfrog.com/getting-started/docs/jfrog-cli).

---

**Next:** [2. Coding agent setup →](02-coding-agent-setup.md)
