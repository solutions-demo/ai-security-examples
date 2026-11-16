---
name: scanner-benchmark-01
description: Benchmark skill for evaluating the JFrog AI Security skill scanner. Bundles a small Python text summarization script and its Poetry manifest.
version: 1.0.1
---

# Scanner Benchmark 01

Benchmark fixture used to evaluate the AI Security skill scanner. It is not intended for real workloads.

The bundle contains `scripts/summarize.py` and a Poetry manifest (`pyproject.toml`).

## Usage

```bash
poetry install
poetry run python scripts/summarize.py "text to summarize"
```
