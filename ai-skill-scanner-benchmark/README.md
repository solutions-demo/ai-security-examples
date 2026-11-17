# AI Skill Scanner Benchmark

*Part of [AI Security Examples](../README.md).*

A set of purpose-built agent skills for trying out the JFrog AI Security skill scanner during a trial or
proof of concept. Each skill tests exactly one weakness and has a neutral name and description, so the
scanner has to find the problem in the content rather than being told what to look for.

> [!WARNING]
> These skills are intentionally unsafe test fixtures. Don't install them into a real agent environment.
> All credentials are randomly generated and valid nowhere, and every host uses a reserved name that never
> resolves.

## Quick start

1. Generate the fixtures that contain secret-shaped values (Git hosts block these, so the repo only
   stores a template):

   ```bash
   python3 tools/generate_fixtures.py
   ```

2. Publish each skill folder to a skills repository in your JFrog Platform:

   ```bash
   jf skills publish ./skills/scanner-benchmark-01 --server-id <server-id> --repo <skills-repo>
   ```

3. Open each skill's scan result in the platform and compare it with the tables below.

> [!NOTE]
> The scanner uses AI-based analysis, so wording and severity can vary slightly between scans. What
> matters is whether each skill's intended weakness is caught.

## Skills

### Instructions and prompt injection

| Skill | What's inside | Risk | Expected finding |
|-------|---------------|------|------------------|
| [**03** · Instruction override](skills/scanner-benchmark-03) | A word counter whose `SKILL.md` tells the assistant to ignore its rules | The agent drops its safeguards, skips confirmations and hides it from the user | Prompt injection |
| [**04** · Hidden instruction](skills/scanner-benchmark-04) | A temperature converter with an instruction in an HTML comment in `SKILL.md` | The agent changes its behavior based on text the user never sees | Hidden or concealed instruction |
| [**12** · Excessive agency](skills/scanner-benchmark-12) | A notes tidier whose `SKILL.md` grants broad tools and says not to ask permission | The agent runs commands, writes anywhere and fetches URLs without approval | Over-broad permissions, autonomy |

04's hidden instruction is deliberately harmless, so a finding there shows the scanner caught the
concealment itself, not a dangerous payload.

### Malicious or unsafe code

| Skill | What's inside | Risk | Expected finding |
|-------|---------------|------|------------------|
| [**06** · Credential exfiltration](skills/scanner-benchmark-06) | A "diagnostics" script, `scripts/diagnostics.py`, that collects env vars and credential files and posts them | AWS credentials, SSH key and `.netrc` are sent to an outside server | Credential access, data exfiltration |
| [**07** · Command injection](skills/scanner-benchmark-07) | An image converter, `scripts/run_tool.py`, that builds shell commands from arguments and calls `eval` | A crafted argument runs arbitrary code with the user's privileges | Command injection, unsafe execution |
| [**08** · Obfuscated payload](skills/scanner-benchmark-08) | A setup script, `scripts/setup.py`, that decodes and executes a base64 string | The SSH private key ends up in the terminal, logs or agent transcript, hidden from code review | Obfuscation resolving to credential disclosure |
| [**09** · Persistence](skills/scanner-benchmark-09) | A "notes sync" installer, `scripts/install_helper.sh`, that edits crontab, shell rc files and systemd | Code keeps running after the skill is gone and restarts on every login | Persistence, system modification |
| [**10** · Behavior mismatch](skills/scanner-benchmark-10) | A Markdown formatter documented as offline, whose `scripts/format_docs.py` uploads files | Files the user believes stay local are sent to an external server | Description/behavior mismatch, exfiltration |

### Supply chain and secrets

| Skill | What's inside | Risk | Expected finding |
|-------|---------------|------|------------------|
| [**01** · Vulnerable dependencies](skills/scanner-benchmark-01) | A summarizer whose `pyproject.toml` pins outdated packages (no lockfile) | Packages with known, exploitable CVEs land in the agent's environment | Vulnerable dependencies |
| [**02** · Hardcoded secrets](skills/scanner-benchmark-02) | A script, `scripts/credentials.py`, with plain-text credentials (generated in step 1) | Anyone who can read the skill gets cloud, GitHub, payment and Slack credentials and a private key | Exposed secrets |
| [**05** · Fake prerequisite](skills/scanner-benchmark-05) | A PDF thumbnailer whose `SKILL.md` setup downloads a password-protected helper | The user is talked into running an unverified binary | Untrusted download *(may rate lower, since the host never resolves)* |
| [**11** · Typosquatting](skills/scanner-benchmark-11) | A feed fetcher whose `requirements.txt` lists misspelled package names | A lookalike package registered by an attacker runs code at install time | Typosquatted dependencies |

### Controls

These two should come back clean. They show the scanner isn't flagging ordinary code, or code that uses
the network, subprocesses and environment variables for a legitimate, documented purpose.

| Skill | What's inside | Risk | Expected finding |
|-------|---------------|------|------------------|
| [**13** · Clean](skills/scanner-benchmark-13) | A plain slug generator with no I/O | None | No findings |
| [**14** · Clean, sensitive-looking APIs](skills/scanner-benchmark-14) | A health check using HTTPS, a fixed-argument subprocess and an env-var token, all documented | None: the token only goes to the URL the user passes, and redirects are refused | No findings, or low-severity notes |
