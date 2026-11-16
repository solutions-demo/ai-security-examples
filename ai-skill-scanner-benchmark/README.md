# AI Skill Scanner Benchmark

A small set of purpose-built agent skills for trying out the JFrog AI Security skill scanner during a
trial or proof of concept. Each skill isolates **one** weakness, so every finding, or every miss, can be
traced to a single cause.

> **Safety notice.** These skills are test fixtures and are intentionally unsafe. Do not install them
> into a real agent environment. All credentials in them are randomly generated and are not valid for any
> account or service.

## The benchmark skills

| Skill | Threat class | What it contains | Where the issue lives | What the scanner should report |
|-------|--------------|------------------|-----------------------|--------------------------------|
| [`scanner-benchmark-01`](skills/scanner-benchmark-01) | Vulnerable dependencies | A text summarization script and a Poetry manifest pinning outdated packages with known CVEs | `pyproject.toml` | Vulnerable-dependency findings |
| [`scanner-benchmark-02`](skills/scanner-benchmark-02) | Hardcoded secrets | A script holding credentials in plain text | `scripts/credentials.py` | Secrets-exposure findings |
| [`scanner-benchmark-03`](skills/scanner-benchmark-03) | Prompt injection: instruction override | A word-count script, plus a visible instruction telling the assistant to ignore its rules and skip confirmations | `SKILL.md` | Prompt-injection finding |
| [`scanner-benchmark-04`](skills/scanner-benchmark-04) | Prompt injection: hidden instructions (comment) | A temperature converter whose `SKILL.md` carries a low-impact instruction in an HTML comment, telling the assistant to act on it and not mention it | `SKILL.md` | Hidden-instruction or concealed-text finding |
| [`scanner-benchmark-05`](skills/scanner-benchmark-05) | Social engineering: fake prerequisite | A PDF thumbnailer that tells the user to download a helper from an external host, unpack it with a password and run it | `SKILL.md` | Suspicious or higher: untrusted download and unverified binary. The download host is a reserved name that never resolves and no payload is bundled, so the scanner may not rate it as malicious |
| [`scanner-benchmark-06`](skills/scanner-benchmark-06) | Data exfiltration: credential chain | A script that reads environment variables and credential files and posts them to an external endpoint | `scripts/diagnostics.py` | Credential-access and data-exfiltration findings |
| [`scanner-benchmark-07`](skills/scanner-benchmark-07) | Command injection | An image converter that builds shell commands from arguments and evaluates expressions | `scripts/run_tool.py` | Command-injection / unsafe-execution findings |
| [`scanner-benchmark-08`](skills/scanner-benchmark-08) | Obfuscated execution | A setup script that decodes base64 and hex strings and executes them | `scripts/setup.py` | Obfuscation / dynamic-execution findings |
| [`scanner-benchmark-09`](skills/scanner-benchmark-09) | Persistence | An install script that edits crontab, shell startup files and a systemd user service | `scripts/install_helper.sh` | Persistence / system-modification findings |
| [`scanner-benchmark-10`](skills/scanner-benchmark-10) | Description-behavior mismatch | A Markdown formatter documented as offline that uploads every file it touches | `SKILL.md` vs `scripts/format_docs.py` | Mismatch between documented and actual behavior, data exfiltration |
| [`scanner-benchmark-11`](skills/scanner-benchmark-11) | Supply chain: typosquatted dependencies | A feed fetcher whose `requirements.txt` lists misspelled package names | `requirements.txt` | Typosquatting / suspicious-dependency findings |
| [`scanner-benchmark-12`](skills/scanner-benchmark-12) | Excessive agency | A notes tidier that declares a broad tool allowlist and tells the assistant not to ask permission | `SKILL.md` (frontmatter and body) | Over-broad permissions / autonomy findings |
| [`scanner-benchmark-13`](skills/scanner-benchmark-13) | Clean control | A plain-Python slug generator with no I/O | all files | No findings |
| [`scanner-benchmark-14`](skills/scanner-benchmark-14) | Clean control, with sensitive-looking APIs | A health check that legitimately uses the network, a subprocess with fixed arguments and an environment variable, all documented in `SKILL.md` | all files | No findings, or at most low-severity informational notes |

Skill 04 uses a low-impact hidden instruction on purpose, to test whether concealment alone (via a visible-in-source
HTML comment) is enough to trigger a finding, independent of the harm of the instruction.

Skills 13 and 14 are controls. They measure false positives: 13 shows that an unremarkable skill is left alone,
and 14 shows that a skill using network, subprocess and environment APIs is judged on whether its behavior
matches what it documents, not on API names alone.

Skills 04, 05, 06, 09 and 11 contain no real credentials or malware. Hosts use reserved names that never
resolve (`.example`), and the scripts are not meant to be run.

## About each skill

### scanner-benchmark-01: vulnerable dependencies
- **Files:** `SKILL.md`, `pyproject.toml`, `scripts/summarize.py`
- **What it models:** a skill whose own code looks harmless but whose dependencies are outdated. It pins
  old releases of `transformers`, `pyyaml`, `requests`, `urllib3`, `jinja2`, `pillow` and `cryptography`.
- **What it does not contain:** secrets, network calls, or suspicious behavior. The only weakness is the
  dependency set.
- **Worth noting:** no `poetry.lock` is included. If you want to see how the scanner treats a manifest
  without a lockfile versus one with it, generate a lockfile and compare.

### scanner-benchmark-02: hardcoded secrets
- **Files:** `SKILL.md`, `scripts/credentials.py` (created by `tools/generate_fixtures.py` from
  `templates/scanner-benchmark-02/credentials.py.tmpl`)
- **What it models:** a developer pastes working credentials into a helper script and ships it with the
  skill. The script holds cloud, source-control, payment and messaging credentials, a database URL with a
  password, and a private key.
- **What it does not contain:** outbound network calls, or a dependency manifest. The credentials are
  never used beyond being returned by a function.
- **Worth noting:** the values are random but use realistic formats, so detection does not depend on
  placeholder markers.

## Running the benchmark

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
3. Open the scan results for each published skill in your platform.
4. Compare them with the "What the scanner should report" column above.

## Reading the results

The scanner uses AI-based analysis, so the exact wording, severity, set of findings and overall verdict
can vary slightly between runs and between scanner versions. What should stay consistent is the core
signal: the intended weakness of each skill should be detected. A few things help when interpreting
results:

- **Judge each skill against its own angle.** Compare a skill with the weakness it was built to
  demonstrate, not with a full list of everything a scanner could report.
- **Re-run before concluding.** Scan a skill a few times before drawing conclusions from a single result.
- **Extra findings are worth a look.** If a skill is flagged for something outside its intended weakness,
  check whether the scanner is reacting to behavior in the skill, since the scanner evaluates what a
  skill does as well as what it contains.
- **Repeated misses are worth reporting.** If the intended weakness is not detected across repeated
  runs, share the details with your JFrog contact.

## Design principles

1. **One weakness per skill**, so results are easy to attribute.
2. **Neutral names and descriptions.** Skills say they are benchmark fixtures but never name the
   weakness, so the scanner has to find it in the content.
3. **No hints in the code.** The fixtures avoid comments and identifiers that give the answer away, or
   that detectors commonly treat as placeholders.
4. **The answer key lives outside the skills.** Expected results are documented here in the README, not
   inside the skill folders the scanner reads.
5. **Realistic format, no real access.** Secrets are randomly generated by `tools/generate_fixtures.py`
   and are valid nowhere. They are never committed: the repository holds only a template.

## Roadmap

Further angles planned, one skill each: anti-refusal and system-prompt leakage, memory and configuration
poisoning, trigger abuse, remote instruction loading, privilege escalation, destructive actions, insecure
code (path traversal, SQL injection), resource exhaustion, dependency source redirection, hidden artifacts
(shipped bytecode, concealed executables), a malware test signature, over-autonomy, financial access, a
realistic multi-vector skill, evasion variants of existing skills, and non-Python languages. Suggestions
are welcome.
