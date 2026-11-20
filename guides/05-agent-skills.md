# 5. Agent skills

Create, scan, publish and govern agent skills through the JFrog Skills Registry.

The Skills Registry is the single place where coding agents publish, discover and install skill bundles.
Skills are versioned, stored immutably in Artifactory, and scanned by JFrog before they can be installed.
Administrators control which skills may run with project-level policies. Agent Guard resolves your active
project and target repository, so you never manage Artifactory paths in the IDE.

> [!IMPORTANT]
> Skill scanning needs the scoped developer user from [guide 3](03-access-and-auth.md) and the signed AI
> Addendum from [guide 1](01-prerequisites.md). Without the addendum, skills register but are never
> scanned.

## 1. Create a local skill and watch it get scanned

1. Ask your agent to create a simple local skill, for example `hello-10-languages`, which says hello in
   ten languages.
2. Invoke it. The agent's hook intercepts the call because the skill hasn't been scanned yet, and submits
   it for scanning automatically.
3. Wait one to two minutes, then invoke it again. Once the scan finds it safe, it runs.

## 2. Publish it

1. Ask your agent: *"Publish the hello-10-languages skill to JFrog AI Security."*
2. When asked about cryptographic evidence, choose **Publish unsigned** for this test.
3. The agent creates a skills repository bound to your project, if there isn't one yet, and uploads the
   skill.

## 3. Check it in the JFrog UI

1. Open **Platform → AI/ML → Registry → Skills** and find the skill.
2. Give the scan a few minutes, then open the skill page. The scan status should read **Not malicious**.

## 4. Add an allow-list policy

See [Skill policies](https://docs.jfrog.com/ai-ml/docs/skill-policies) for the full reference.

1. Go to **AI/ML → Policies → Create new Policy**.
2. Choose a **Project-level** policy. Only project-level policies support allow lists; global policies
   evaluate scan results only.
3. Set the type to **Allow List**, assign it to your evaluation project, then save and activate it.

## 5. See the policy block and then allow the skill

1. On the skill's page, note the **Add to allow list** button, but don't click it yet.
2. Invoke the skill again in your agent (for example `/hello-10-languages`). The hook blocks it with a
   policy error.
3. Back in the UI, click **Add to allow list**, then invoke the skill once more. It now runs.

## Going further

Use the [Skill Scanner Benchmark](../examples/skill-scanner-benchmark/README.md) to see how the scanner
handles skills with prompt injection, obfuscated payloads, credential exfiltration, typosquatted
dependencies and more.

---

**Previous:** [← 4. MCP servers](04-mcp-servers.md) · **Next:** [6. Governed AI models →](06-governed-models.md)
