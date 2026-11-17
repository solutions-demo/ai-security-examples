# AI Skill Scanner Benchmark

*Part of [AI Security Examples](../README.md).*

A set of purpose-built agent skills for trying out the JFrog AI Security skill scanner during a trial or
proof of concept. Each skill is built to test exactly one weakness, with a neutral name and description,
so the scanner has to find the problem in the content rather than being told what to look for.

> **Safety notice.** These skills are test fixtures and are intentionally unsafe. Do not install them
> into a real agent environment. All credentials in them are randomly generated and are not valid for any
> account or service.

## Skills

| Skill | Threat class | What it contains | Where the issue lives | What the scanner should report |
|-------|--------------|------------------|-----------------------|--------------------------------|
| [`scanner-benchmark-01`](skills/scanner-benchmark-01) | Vulnerable dependencies | A text summarization script with a Poetry manifest pinning outdated packages with known CVEs (no `poetry.lock` included) | `pyproject.toml` | Vulnerable-dependency findings |
| [`scanner-benchmark-02`](skills/scanner-benchmark-02) | Hardcoded secrets | A script holding credentials in plain text, generated from a template at build time (see Usage) | `scripts/credentials.py` (generated; see `templates/`) | Secrets-exposure findings |
| [`scanner-benchmark-03`](skills/scanner-benchmark-03) | Prompt injection: instruction override | A word-count script, plus a visible instruction telling the assistant to ignore its rules and skip confirmations | `SKILL.md` | Prompt-injection finding |
| [`scanner-benchmark-04`](skills/scanner-benchmark-04) | Prompt injection: hidden instructions (comment) | A temperature converter whose `SKILL.md` carries a low-impact instruction in an HTML comment, telling the assistant to act on it and not mention it | `SKILL.md` | Hidden-instruction or concealed-text finding |
| [`scanner-benchmark-05`](skills/scanner-benchmark-05) | Social engineering: fake prerequisite | A PDF thumbnailer that tells the user to download a helper from an external host, unpack it with a password and run it | `SKILL.md` | Untrusted download / unverified binary finding (the host is reserved and never resolves, so severity may land lower) |
| [`scanner-benchmark-06`](skills/scanner-benchmark-06) | Data exfiltration: credential chain | A script that reads environment variables and credential files and posts them to an external endpoint | `scripts/diagnostics.py` | Credential-access and data-exfiltration findings |
| [`scanner-benchmark-07`](skills/scanner-benchmark-07) | Command injection | An image converter that builds shell commands from arguments and evaluates expressions | `scripts/run_tool.py` | Command-injection / unsafe-execution findings |
| [`scanner-benchmark-08`](skills/scanner-benchmark-08) | Obfuscated credential disclosure | A setup script that decodes a base64 payload which reads and prints a local SSH private key | `scripts/setup.py` | Obfuscation finding that resolves to a credential-disclosure path, not just "uses base64" |
| [`scanner-benchmark-09`](skills/scanner-benchmark-09) | Persistence | An install script that edits crontab, shell startup files and a systemd user service | `scripts/install_helper.sh` | Persistence / system-modification findings |
| [`scanner-benchmark-10`](skills/scanner-benchmark-10) | Description-behavior mismatch | A Markdown formatter documented as offline that uploads every file it touches | `SKILL.md` vs `scripts/format_docs.py` | Mismatch between documented and actual behavior, data exfiltration |
| [`scanner-benchmark-11`](skills/scanner-benchmark-11) | Supply chain: typosquatted dependencies | A feed fetcher whose `requirements.txt` lists misspelled package names | `requirements.txt` | Typosquatting / suspicious-dependency findings |
| [`scanner-benchmark-12`](skills/scanner-benchmark-12) | Excessive agency | A notes tidier that declares a broad tool allowlist and tells the assistant not to ask permission | `SKILL.md` | Over-broad permissions / autonomy findings |
| [`scanner-benchmark-13`](skills/scanner-benchmark-13) | Clean control | A plain slug generator with no I/O | — | No findings |
| [`scanner-benchmark-14`](skills/scanner-benchmark-14) | Clean control, with sensitive-looking APIs | A health check that legitimately uses the network, a subprocess with fixed arguments and an environment variable (and refuses redirects), all documented in `SKILL.md` | — | No findings, or at most low-severity informational notes |

13 and 14 are controls, for checking false positives: 13 shows an unremarkable skill is left alone, and 14
shows a skill that legitimately touches the network, subprocess and environment is judged on its actual
behavior rather than flagged for using sensitive-looking APIs. 04's hidden instruction is deliberately
low-impact, so a finding there reflects detection of the concealment itself rather than the severity of
the payload. Skills 04, 05, 06, 09 and 11 don't contain any real credentials or malware — hosts use
reserved names that never resolve, and the scripts aren't meant to be run.

Results can vary slightly in wording and severity between scans, since the scanner uses AI-based analysis
— what matters is whether each skill's intended weakness gets caught at all.

## Usage

1. Generate the fixtures that contain secret-shaped values. The repository stores only a template for
   these, because Git hosts block credential-shaped strings. Each run writes new random values that are
   valid nowhere (requires Python 3; uses `openssl` for the private key when available):
   ```bash
   python3 tools/generate_fixtures.py
   ```
2. Publish each skill folder to a skills repository in your JFrog Platform:
   ```bash
   jf skills publish ./skills/scanner-benchmark-01 --server-id <server-id> --repo <skills-repo>
   jf skills publish ./skills/scanner-benchmark-02 --server-id <server-id> --repo <skills-repo>
   ```
3. Open the scan results for each published skill in your platform and compare them with the table above.
