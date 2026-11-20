"""Check whether an HTTPS endpoint responds and report the current git revision."""
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request


class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # Refuse to follow redirects, so the Authorization header can never
        # reach a host other than the one the caller explicitly passed in.
        return None


def current_revision() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout.strip() or "unknown"


def check(url: str) -> int:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValueError("url must be an https URL")
    request = urllib.request.Request(url, method="GET")
    token = os.environ.get("HEALTHCHECK_TOKEN")
    if token:
        request.add_header("Authorization", f"Bearer {token}")
    opener = urllib.request.build_opener(NoRedirectHandler)
    try:
        with opener.open(request, timeout=10) as response:
            return response.status
    except urllib.error.HTTPError as error:
        if 300 <= error.code < 400:
            raise ValueError(
                f"refusing to follow redirect from {url} (status {error.code})"
            ) from error
        raise


if __name__ == "__main__":
    print(f"revision {current_revision()}: HTTP {check(sys.argv[1])}")
