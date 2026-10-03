#!/usr/bin/env python3
"""IssuePilot stdlib HTTP server + CLI.

Mock mode when NEBIUS_API_KEY is unset/placeholder.
Live mode calls Nebius Token Factory chat completions (Nemotron).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

APP_DIR = Path(__file__).resolve().parent
ROOT = APP_DIR.parent
sys.path.insert(0, str(APP_DIR))

from planner import footer_text, has_api_key, plan_issue  # noqa: E402


def _load_dotenv() -> None:
    env_path = ROOT / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k, v = k.strip(), v.strip().strip('"').strip("'")
        if k and k not in os.environ:
            os.environ[k] = v


def _static(name: str) -> bytes:
    path = APP_DIR / "static" / name
    return path.read_bytes()


class Handler(BaseHTTPRequestHandler):
    def _send(self, code: int, body: bytes, content_type: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, code: int, payload: object) -> None:
        data = json.dumps(payload, indent=2).encode("utf-8")
        self._send(code, data, "application/json; charset=utf-8")

    def do_OPTIONS(self) -> None:  # noqa: N802
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path in ("/", "/index.html"):
            self._send(200, _static("index.html"), "text/html; charset=utf-8")
            return
        if path == "/health":
            live = has_api_key()
            self._send_json(
                200,
                {
                    "ok": True,
                    "service": "issuepilot",
                    "mode": "live" if live else "mock",
                    "model": (os.environ.get("NEBIUS_MODEL") or None) if live else None,
                    "footer": footer_text(),
                },
            )
            return
        if path == "/sample-issue":
            sample = APP_DIR / "samples" / "sample_issue.txt"
            self._send(200, sample.read_bytes(), "text/plain; charset=utf-8")
            return
        self._send_json(404, {"error": "not found"})

    def do_POST(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length) if length else b"{}"
        try:
            body = json.loads(raw.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            self._send_json(400, {"error": "invalid json"})
            return
        if path == "/api/plan":
            issue = body.get("issue") or body.get("text") or ""
            if not str(issue).strip():
                self._send_json(400, {"error": "issue text required"})
                return
            plan = plan_issue(str(issue))
            self._send_json(200, plan)
            return
        self._send_json(404, {"error": "not found"})

    def log_message(self, fmt: str, *args) -> None:
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))


def run_cli(path: str | None, text: str | None) -> None:
    if path:
        issue = Path(path).read_text(encoding="utf-8")
    elif text:
        issue = text
    else:
        issue = sys.stdin.read()
    print(json.dumps(plan_issue(issue), indent=2))


def main() -> None:
    _load_dotenv()
    p = argparse.ArgumentParser(description="IssuePilot server / CLI")
    p.add_argument("--cli", action="store_true", help="Print plan JSON and exit")
    p.add_argument("-f", "--file", help="Issue text file")
    p.add_argument("--text", help="Issue text")
    p.add_argument("--host", default=os.environ.get("HOST", "127.0.0.1"))
    p.add_argument("--port", type=int, default=int(os.environ.get("PORT", "8787")))
    args = p.parse_args()
    if args.cli:
        run_cli(args.file, args.text)
        return
    httpd = ThreadingHTTPServer((args.host, args.port), Handler)
    mode = "live" if has_api_key() else "mock"
    print(f"IssuePilot ({mode}) http://{args.host}:{args.port}/", flush=True)
    print("  GET  /health   POST /api/plan", flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
