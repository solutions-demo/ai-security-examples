# AI Security Examples

Guides and ready-made examples for evaluating JFrog AI Security in a trial or proof of concept: governing
the MCP servers, agent skills and AI models your developers' coding agents use.

## POC guides

Work through them in order. Each guide builds on the previous ones.

| # | Guide | What you'll show |
|---|-------|------------------|
| 1 | [Prerequisites](guides/01-prerequisites.md) | The platform is ready for AI Security |
| 2 | [Coding agent setup](guides/02-coding-agent-setup.md) | The JFrog plugin on the developer's agent, restricted to approved MCP servers |
| 3 | [Access and authentication](guides/03-access-and-auth.md) | A scoped developer user, connected through the JFrog CLI and verified from the agent |
| 4 | [MCP servers](guides/04-mcp-servers.md) | Registering MCP servers and installing them from the agent |
| 5 | [Agent skills](guides/05-agent-skills.md) | Skills scanned automatically, published, and governed by allow-list policy |
| 6 | [Governed AI models](guides/06-governed-models.md) | Shadow models detected, blocked, and brought under governance |

**Coming soon:** agent plugins, and APM (Agent Package Manager) with Artifactory.

## Examples

| Example | Use it to |
|---------|-----------|
| [Skill Scanner Benchmark](examples/skill-scanner-benchmark/README.md) | Test the skill scanner against 14 skills, each built around one specific attack technique |

## Help

See the [JFrog AI/ML documentation](https://docs.jfrog.com/ai-ml/docs), or contact your JFrog account team.
