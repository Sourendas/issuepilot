"""IssuePilot plan JSON shape (mock + live)."""

from __future__ import annotations

from typing import Any

PLAN_VERSION = "1.0"

REQUIRED_KEYS = (
    "version",
    "severity",
    "summary",
    "repro_gaps",
    "fix_plan",
    "test_ideas",
    "pr_title",
    "pr_body",
    "labels",
)


def empty_plan() -> dict[str, Any]:
    return {
        "version": PLAN_VERSION,
        "severity": "medium",
        "summary": "",
        "repro_gaps": [],
        "fix_plan": [],
        "test_ideas": [],
        "pr_title": "",
        "pr_body": "",
        "labels": [],
        "meta": {"mode": "mock", "model": None},
    }


SYSTEM_PROMPT = """You are IssuePilot, a senior triage engineer.
Given a GitHub issue (title + body), respond with ONE JSON object only:
{
  "version": "1.0",
  "severity": "low|medium|high|critical",
  "summary": "1-3 sentence understanding",
  "repro_gaps": ["what is missing to reproduce"],
  "fix_plan": ["ordered implementation steps"],
  "test_ideas": ["how to verify"],
  "pr_title": "conventional commit style title",
  "pr_body": "markdown PR description",
  "labels": ["bug"|"enhancement"|...]
}
Be concrete and practical. No markdown fences.
"""
