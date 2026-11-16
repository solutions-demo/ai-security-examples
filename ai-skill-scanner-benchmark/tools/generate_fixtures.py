#!/usr/bin/env python3
"""Generate the benchmark fixtures that contain secret-shaped values.

The repository only stores templates, because credential-shaped strings
are blocked by secret scanning on most Git hosts. Run this script before
publishing the skills. Every run produces new random values that are not
valid for any account or service.

Usage: python3 tools/generate_fixtures.py
"""
import base64
import secrets
import string
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ALNUM = string.ascii_letters + string.digits
UPPER_DIGITS = string.ascii_uppercase + string.digits


def rand(n: int, alphabet: str = ALNUM) -> str:
    return "".join(secrets.choice(alphabet) for _ in range(n))


def private_key() -> str:
    """Return a PEM RSA private key; fall back to PEM-framed random data without openssl."""
    for cmd in (["openssl", "genrsa", "-traditional", "2048"], ["openssl", "genrsa", "2048"]):
        try:
            out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode().strip()
        except (OSError, subprocess.CalledProcessError):
            continue
        if out.startswith("-----BEGIN RSA PRIVATE KEY-----"):
            return out
    body = base64.encodebytes(secrets.token_bytes(1190)).decode().strip()
    return f"-----BEGIN RSA PRIVATE KEY-----\n{body}\n-----END RSA PRIVATE KEY-----"


def render(template: Path, values: dict, target: Path) -> None:
    text = template.read_text()
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text)
    print(f"wrote {target.relative_to(ROOT)}")


def main() -> None:
    values = {
        "AWS_ACCESS_KEY_ID": "AKIA" + rand(16, UPPER_DIGITS),
        "AWS_SECRET_ACCESS_KEY": rand(40),
        "GITHUB_TOKEN": "ghp_" + rand(36),
        "STRIPE_API_KEY": "sk_live_" + rand(24),
        "SLACK_BOT_TOKEN": f"xoxb-{rand(12, string.digits)}-{rand(13, string.digits)}-{rand(24)}",
        "DB_PASSWORD": rand(16),
        "PRIVATE_KEY": private_key(),
    }
    render(
        ROOT / "templates/scanner-benchmark-02/credentials.py.tmpl",
        values,
        ROOT / "skills/scanner-benchmark-02/scripts/credentials.py",
    )


if __name__ == "__main__":
    main()
