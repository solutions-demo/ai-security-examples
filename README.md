# AI Security Examples

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

| # | Guide | What you'll show |
|---|-------|------------------|
| 1 | [Prerequisites](guides/01-prerequisites.md) | The platform is ready for AI Security |
| 2 | [Coding agent setup](guides/02-coding-agent-setup.md) | The JFrog plugin on the developer's agent, restricted to approved MCP servers |
| 3 | [Access and authentication](guides/03-access-and-auth.md) | A scoped developer user, connected through the JFrog CLI and verified from the agent |
| 4 | [MCP servers](guides/04-mcp-servers.md) | MCP servers registered, restricted by tool policy, and installed from the agent |
| 5 | [Agent skills](guides/05-agent-skills.md) | Skills scanned, published, tested against the benchmark, and governed by policy |
| 6 | [Governed AI models](guides/06-governed-models.md) | Shadow models detected, blocked, and brought under governance |

**Coming soon:** agent plugins, and APM (Agent Package Manager) with Artifactory.

## Examples

| Example | Use it to |
|---------|-----------|
| [Skill Scanner Benchmark](examples/skill-scanner-benchmark/README.md) | Test the skill scanner against 14 skills, each built around one specific attack technique |

## Help and feedback

See the [JFrog AI/ML documentation](https://docs.jfrog.com/ai-ml/docs), or contact your JFrog account team.
Found a step that's out of date or unclear? [Open an issue](https://github.com/solutions-demo/ai-security-examples/issues)
or send a pull request.
