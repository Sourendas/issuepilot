#!/usr/bin/env python3
"""Offline mock checks. Does not call Token Factory."""

from __future__ import annotations

import json
import os
import sys
import urllib.request
from pathlib import Path

APP = Path(__file__).resolve().parent
sys.path.insert(0, str(APP))

os.environ.pop("NEBIUS_API_KEY", None)

import planner  # noqa: E402


def main() -> None:
    called = {"n": 0}
    real = urllib.request.urlopen

    def boom(*_a, **_k):
        called["n"] += 1
        raise AssertionError("live HTTP must not run in the mock test")

    urllib.request.urlopen = boom  # type: ignore[assignment]
    try:
        assert planner.has_api_key() is False
        assert planner.footer_text() == "Mock planner (no API key)"
        issue = (APP / "samples" / "sample_issue.txt").read_text(encoding="utf-8")
        plan = planner.plan_issue(issue)
    finally:
        urllib.request.urlopen = real  # type: ignore[assignment]

    assert called["n"] == 0
    for key in (
        "version",
        "severity",
        "summary",
        "repro_gaps",
        "fix_plan",
        "test_ideas",
        "pr_title",
        "pr_body",
        "labels",
    ):
        assert key in plan, key
    assert plan["meta"]["mode"] == "mock"
    assert plan["meta"]["footer"] == "Mock planner (no API key)"
    # Title says "crashes" so the mock marks high severity.
    assert plan["severity"] == "high"
    assert plan["fix_plan"]
    assert "sku" in issue.lower() or "SKU" in issue
    out = APP / "samples" / "sample_plan.json"
    out.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
    print("mock ok", plan["severity"], "gaps", len(plan["repro_gaps"]), "->", out.name)


if __name__ == "__main__":
    main()
