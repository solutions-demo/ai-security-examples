# AI Skill Scanner Benchmark

*Part of [JFrog AI Security Examples](../../README.md).*

A set of purpose-built agent skills for trying out the JFrog AI Security skill scanner during a trial or
proof of concept. Each skill is a single test case: one specific attack technique, in a neutral wrapper,
so the scanner has to find the problem in the content rather than being told what to look for.

The set isn't exhaustive. It doesn't cover everything the scanner checks for, or every way a skill can be
attacked. Treat it as a starting point for understanding the angles an attack can come from, then try
skills of your own.

Skills are grouped below by **attack surface** — *where* in the skill an attacker would plant something
(the agent's instructions, the runtime code, the dependency manifest, and so on). Within each group, the
**Vector** column names the specific technique: the thing a scanner either does or doesn't detect. Two
skills in the same surface use different vectors on purpose, so the benchmark covers distinct detection
capabilities rather than just repeating "bad behavior in a different wrapper".

**The skills are built to do no real damage.** Every network destination is a reserved `.example` host that
never resolves, so nothing leaves the machine, and every credential is randomly generated and valid nowhere.
What the scanner reacts to, by design, is the attack pattern itself and the mismatch between that pattern
and what the skill says it does: a "temperature converter" carrying hidden instructions, a "notes sync"
helper that installs persistence, an "offline" formatter that uploads files. A scanner that only flagged
skills with a working payload would miss all of these.

> [!WARNING]
> Harmless isn't the same as side-effect free. Run these skills only in a throwaway environment, never in a
> real agent setup: 09 really adds crontab, shell-startup and systemd entries, 08 prints your SSH private key
> to the terminal if one exists, and 10 rewrites the Markdown files you point it at.

## Quick start

1. Generate the fixtures that contain secret-shaped values (Git hosts block these, so the repo only
   stores a template):

   ```bash
   python3 tools/generate_fixtures.py
   ```

2. Publish each skill folder to a skills repository in your JFrog Platform:

   ```bash
   jf agent skills publish ./skills/scanner-benchmark-01 --server-id <server-id> --repo <skills-repo>
   ```

3. Open each skill's scan result in the platform and compare it with the tables below.

> [!NOTE]
> The scanner uses AI-based analysis, so wording and severity can vary slightly between scans. What
> matters is whether each skill's intended weakness is caught. Verdicts below are **Malicious**,
> **Suspicious**, or **Not malicious**, the statuses the platform shows.

## Skills

### Instructions aimed at the agent

**Surface:** text in `SKILL.md` that the agent reads as guidance. Detection needs natural-language
reasoning, not code analysis.

| Skill | Vector | Risk | Expected verdict |
|-------|--------|------|------------------|
| [**03** · Instruction override](skills/scanner-benchmark-03) | Plain visible prose ordering the agent to ignore its rules and skip confirmations | The agent drops its safeguards and hides that from the user | Malicious |
| [**04** · Hidden instruction](skills/scanner-benchmark-04) | HTML comment `<!-- ... -->` — invisible in rendered Markdown but still read by the agent | The agent changes its behavior based on text the user never sees | Malicious |
| [**12** · Excessive agency](skills/scanner-benchmark-12) | `allowed-tools` frontmatter granting broad tool access, plus a body paragraph waiving permission prompts | The agent runs commands, writes anywhere and fetches URLs without approval | Malicious |

### Setup steps aimed at the human

**Surface:** text in `SKILL.md` directed at the person installing the skill. The agent is bypassed; the
victim is the user's shell.

| Skill | Vector | Risk | Expected verdict |
|-------|--------|------|------------------|
| [**05** · Fake prerequisite](skills/scanner-benchmark-05) | A "Prerequisites" block instructing the user to `curl` a password-protected zip, `unzip -P` it and `chmod +x` the result | The user is social-engineered into running an unverified binary | Suspicious *(the host doesn't resolve, so no live payload)* |

### Runtime code behavior

**Surface:** what the skill's scripts actually do when executed. Detection needs control-flow and
data-flow analysis — tracing sources (file reads, env vars) to sinks (network, shell, exec).

| Skill | Vector | Risk | Expected verdict |
|-------|--------|------|------------------|
| [**06** · Credential exfiltration](skills/scanner-benchmark-06) | Reads `os.environ` and `~/.aws/credentials`, `~/.ssh/id_rsa`, `~/.netrc`, then POSTs them via `urllib.request.urlopen` | AWS credentials, SSH key and `.netrc` leave the machine | Malicious |
| [**07** · Command injection](skills/scanner-benchmark-07) | `subprocess.run(shell=True, ...)` with string-concatenated user input, plus `eval()` on an argument | A crafted argument runs arbitrary code with the user's privileges | Suspicious *(the code is exploitable, but no bundled payload)* |
| [**08** · Obfuscated payload](skills/scanner-benchmark-08) | `exec(base64.b64decode("..."))` — the decoded Python reads `~/.ssh/id_rsa` and prints its contents | SSH key ends up in the terminal, logs or agent transcript, hidden from code review | Malicious |
| [**09** · Persistence](skills/scanner-benchmark-09) | Appends to `~/.bashrc`/`~/.zshrc`, installs a `crontab` entry, writes a `systemd --user` service | Code keeps running after the skill is gone and restarts on every login | Malicious |
| [**10** · Behavior mismatch](skills/scanner-benchmark-10) | Code POSTs every Markdown file to an external server, while `SKILL.md` explicitly claims "fully offline, never sends files anywhere" | Files the user believed stayed local are sent off-machine | Malicious |

### Dependency manifest

**Surface:** what the skill pulls in at install time. The skill's own code can look clean; the risk comes
from packages named in a manifest.

| Skill | Vector | Risk | Expected verdict |
|-------|--------|------|------------------|
| [**01** · Vulnerable dependencies](skills/scanner-benchmark-01) | `pyproject.toml` pins outdated versions with known CVEs (`transformers 4.30.0`, `pyyaml 5.3`, `urllib3 1.24.1`, …); no lockfile | Exploitable CVEs land in the agent's environment | Suspicious *(no exploit is shipped, but installing the skill pulls them in)* |
| [**11** · Typosquatting](skills/scanner-benchmark-11) | `requirements.txt` lists `reqeusts`, `python-dateutils`, `numpyy` — one-character variants of the real packages the code actually imports | A lookalike package registered by an attacker runs code at install time | Malicious |

### Embedded data

**Surface:** values hardcoded into source files. Detection is content inspection: recognizing credential
shapes regardless of how the code uses them.

| Skill | Vector | Risk | Expected verdict |
|-------|--------|------|------------------|
| [**02** · Hardcoded secrets](skills/scanner-benchmark-02) | Module-level string constants in format-identifiable shapes: `AKIA…`, `ghp_…`, `sk_live_…`, `xoxb-…`, a Postgres URL with embedded password, a PEM private key block | Anyone who can read the skill gets working-looking cloud, GitHub, Stripe and Slack credentials plus a private key | Malicious |

### Controls

Two negative cases. They test that the scanner isn't flagging ordinary code, or code that uses
sensitive-looking APIs for a legitimate, documented purpose.

| Skill | Vector | Expected verdict |
|-------|--------|------------------|
| [**13** · Clean](skills/scanner-benchmark-13) | Plain string manipulation; no I/O, no subprocess, no network | Not malicious |
| [**14** · Clean, sensitive-looking APIs](skills/scanner-benchmark-14) | HTTPS GET to a caller-supplied URL with an env-var bearer token, plus a fixed-argument `subprocess.run`; redirects are refused and all behavior is documented in `SKILL.md` | Not malicious, or at most a low-severity note |
