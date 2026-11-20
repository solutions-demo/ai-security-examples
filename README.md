# JFrog AI Security Examples

Guides and ready-made examples for evaluating JFrog AI Security in a trial or proof of concept: governing
the MCP servers, agent skills and AI models your developers' coding agents use.

## Getting started

Clone the repository, so the guides can use the examples locally:

```bash
git clone https://github.com/solutions-demo/ai-security-examples.git
cd ai-security-examples
```

Then open [guide 1](guides/01-prerequisites.md) and work through the guides in order. Each one says what you
need before you start and what you'll have at the end. Run your coding agent from the repository root, so
paths in the guides, such as `examples/skill-scanner-benchmark/skills`, resolve as written.

```
ai-security-examples/
├── guides/      Step-by-step POC guides, numbered in the order to follow them
└── examples/    Ready-made assets the guides use, such as the Skill Scanner Benchmark
```

## POC guides

Each guide builds on the previous ones.

| Guide | Description |
|-------|-------------|
| [1. Prerequisites](guides/01-prerequisites.md) | What you need before testing JFrog AI Security: a dedicated JFrog Project, AI scanning, Curation and the AI Addendum, plus the Skills enforcement preview and the MCP Registry. |
| [2. Coding agent setup](guides/02-coding-agent-setup.md) | Installing the JFrog plugin in each supported coding assistant (VS Code, Claude Code, Cursor), the base of all agent-side governance, and limiting the assistant to MCP servers approved in JFrog. |
| [3. Access and authentication](guides/03-access-and-auth.md) | Creating a developer user with project roles only, connecting the JFrog CLI with it, and checking from the assistant that everything is wired up. |
| [4. MCP server governance](guides/04-mcp-servers.md) | Governing MCP servers: adding one from the Marketplace, restricting its tools with allow and block lists, and registering a remote server you already use, with OAuth or a token header. |
| [5. Agent skill governance](guides/05-agent-skills.md) | Securing agent skills: scanning before a skill runs, publishing to the Skills Registry, testing the scanner with the benchmark, and policies that block malicious skills or allow only approved ones. |
| [6. Package model governance](guides/06-governed-models.md) | Governing package models, such as those from Hugging Face: finding shadow models, blocking them, catching a malicious model and one hidden in a container image, and building an approved model list per project. |

**Coming soon:** agent plugins, and APM (Agent Package Manager) with Artifactory.

## Examples

| Example | Description |
|---------|-------------|
| [Skill Scanner Benchmark](examples/skill-scanner-benchmark/README.md) | 14 purpose-built skills, each using one attack technique, to test what the skill scanner catches. |

## Help and feedback

See the [JFrog AI/ML documentation](https://docs.jfrog.com/ai-ml/docs), or contact your JFrog account team.
Found a step that's out of date or unclear? [Open an issue](https://github.com/solutions-demo/ai-security-examples/issues)
or send a pull request.
