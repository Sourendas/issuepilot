"""Mock planner + optional Nebius Token Factory (Nemotron) call."""

from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
from typing import Any

from plan_schema import SYSTEM_PROMPT, empty_plan

# Placeholders only — real key comes from env after browser apply.
DEFAULT_BASE = "https://api.tokenfactory.nebius.com/v1"
DEFAULT_MODEL = "nvidia/NVIDIA-Nemotron-Nano-9B-v2"


def _env(name: str, default: str = "") -> str:
    return (os.environ.get(name) or default).strip()


def has_api_key() -> bool:
    key = _env("NEBIUS_API_KEY")
    return bool(key) and "your_nebius" not in key.lower() and key != "placeholder"


def footer_text() -> str:
    """Judge-facing line. Never includes the API key."""
    if has_api_key():
        model = _env("NEBIUS_MODEL", DEFAULT_MODEL)
        return f"Nebius Token Factory + NVIDIA model {model}"
    return "Mock planner (no API key)"


def mock_plan(issue_text: str) -> dict[str, Any]:
    text = (issue_text or "").strip()
    title = ""
    body = text
    m = re.match(r"(?is)^\s*title\s*:\s*(.+?)\n\s*body\s*:\s*(.*)$", text)
    if m:
        title, body = m.group(1).strip(), m.group(2).strip()
    elif "\n" in text:
        title, body = text.split("\n", 1)
        title, body = title.strip(), body.strip()
    else:
        title = text[:80] or "Untitled issue"

    lower = text.lower()
    severity = "medium"
    if any(w in lower for w in ("crash", "segfault", "data loss", "security", "rce")):
        severity = "high"
    if any(w in lower for w in ("critical", "production down", "p0")):
        severity = "critical"
    if any(w in lower for w in ("typo", "docs", "nit")):
        severity = "low"

    gaps = []
    if "steps" not in lower and "repro" not in lower:
        gaps.append("Exact repro steps (numbered) are missing")
    if "version" not in lower and "chrome" not in lower and "firefox" not in lower:
        gaps.append("Runtime / browser / OS versions not fully specified")
    if "expected" not in lower:
        gaps.append("Expected vs actual behavior not explicit")
    if not gaps:
        gaps.append("None obvious — clarify edge cases in comments")

    plan = empty_plan()
    plan.update(
        {
            "severity": severity,
            "summary": f"Issue looks like: {title}. "
            f"Mock triage (no NEBIUS_API_KEY). Body length={len(body)} chars.",
            "repro_gaps": gaps,
            "fix_plan": [
                "Reproduce locally with the reported inputs / empty cells if relevant",
                "Add null/empty guards at the reported crash site",
                "Cover the edge case with a unit or integration test",
                "Update user-facing error if stack traces are hidden",
            ],
            "test_ideas": [
                "Fixture with blank SKU / empty rows",
                "Regression: happy-path export still works",
            ],
            "pr_title": f"fix: harden handling for issue — {title[:60]}",
            "pr_body": (
                f"## Summary\n{title}\n\n## Changes\n- Guard empty/undefined fields\n"
                f"- Add tests for reported case\n\n## Test plan\n- [ ] Repro fixed\n"
                f"- [ ] Happy path OK\n"
            ),
            "labels": ["bug"] if severity in ("high", "critical", "medium") else ["enhancement"],
            "meta": {
                "mode": "mock",
                "model": None,
                "footer": footer_text(),
                "note": "Set NEBIUS_API_KEY for live Token Factory + Nemotron",
            },
        }
    )
    return plan


def live_plan(issue_text: str) -> dict[str, Any]:
    """Call Nebius Token Factory chat completions (OpenAI-compatible shape)."""
    api_key = _env("NEBIUS_API_KEY")
    base = _env("NEBIUS_BASE_URL", DEFAULT_BASE).rstrip("/")
    model = _env("NEBIUS_MODEL", DEFAULT_MODEL)
    url = f"{base}/chat/completions"
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": issue_text},
        ],
        "temperature": 0.2,
        "response_format": {"type": "json_object"},
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "IssuePilot/0.1 (Nebius-NVIDIA-hackathon)",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")[:500]
        out = empty_plan()
        out["summary"] = f"Token Factory HTTP {e.code}: {err_body}"
        out["meta"] = {"mode": "error", "model": model, "http_status": e.code}
        return out
    except Exception as e:  # noqa: BLE001
        out = empty_plan()
        out["summary"] = f"Token Factory request failed: {e}"
        out["meta"] = {"mode": "error", "model": model}
        return out

    content = ""
    try:
        content = raw["choices"][0]["message"]["content"]
        parsed = json.loads(content)
    except Exception:  # noqa: BLE001
        out = empty_plan()
        out["summary"] = "Model returned non-JSON; see meta.raw_excerpt"
        out["meta"] = {
            "mode": "live",
            "model": model,
            "raw_excerpt": (content or str(raw))[:800],
        }
        return out

    if not isinstance(parsed, dict):
        out = empty_plan()
        out["summary"] = "Model JSON was not an object"
        out["meta"] = {"mode": "live", "model": model}
        return out

    plan = empty_plan()
    plan.update({k: parsed[k] for k in plan.keys() if k in parsed and k != "meta"})
    plan["meta"] = {
        "mode": "live",
        "model": model,
        "provider": "nebius-token-factory",
        "footer": f"Nebius Token Factory + NVIDIA model {model}",
    }
    return plan


def plan_issue(issue_text: str) -> dict[str, Any]:
    if has_api_key():
        return live_plan(issue_text)
    return mock_plan(issue_text)
