---
name: scanner-benchmark-14
description: Benchmark skill for evaluating the JFrog AI Security skill scanner. Checks whether an HTTPS endpoint responds and reports the current git revision.
version: 1.0.1
---

# Scanner Benchmark 14

Benchmark fixture used to evaluate the AI Security skill scanner. It is not intended for real workloads.

## Usage

Run `python scripts/healthcheck.py https://service.example/health`.

## What this skill does on your machine

- **Network:** sends one HTTPS GET request to the URL you pass, and nothing else. Other schemes are rejected. Redirects are never followed, so the token can't be carried to a different host.
- **Subprocess:** runs `git rev-parse --short HEAD` with fixed arguments to label the report.
- **Environment:** if `HEALTHCHECK_TOKEN` is set, it is sent as a bearer token to the URL you passed, and only over HTTPS.
- **Files:** reads and writes nothing.
