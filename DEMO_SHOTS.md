# IssuePilot — ≤3 min demo shot list (sourendas0 YouTube later)

Record on the machine that already has this folder. Zero spend. **Never show `.env`, API keys, or Token Factory secrets on camera.**

Public repo: https://github.com/Sourendas/issuepilot  
Local: `/workspace/money-ops/contests/nebius-nvidia/`

## Setup (10s, off camera or first frame)

```bash
cd /workspace/money-ops/contests/nebius-nvidia
# Prefer live footer if .env already has NEBIUS_API_KEY (do not open or paste the file on camera).
# If no key: mock mode is fine for the video (Load sample still works).
python3 app/server.py
```

Browser: http://127.0.0.1:8787/

Checked-in samples (use these; do not invent live API output on the fly):

- Issue: `app/samples/sample_issue.txt` (CSV export / blank SKU)
- Mock plan reference: `app/samples/sample_plan.json` (`meta.mode=mock`)
- Prior live plan on disk (optional cutaway, already saved): `app/samples/sample_plan_live.json` (`meta.mode=live`, model `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, severity high) — open in an editor only if needed; do not re-call the API unless the keyed server is already running.

## Shots

1. **0:00–0:20** Title: IssuePilot · issue → fix plan. Badges: Nebius Token Factory, NVIDIA Nemotron, offline mock OK. Say: paste a messy GitHub issue, get severity, repro gaps, fix plan, tests, and a draft PR.
2. **0:20–0:50** Click **Load sample**. Show the CSV-export / blank-SKU issue in the left panel (matches `sample_issue.txt`).
3. **0:50–1:40** Click **Plan issue**. Right panel: severity **high**, summary, repro gaps, fix plan, tests, PR title. Footer should read either live Token Factory + model name, or `Mock planner (no API key)` — both are honest.
4. **1:40–2:20** Scroll the JSON pre: point at `severity`, `fix_plan`, `test_ideas`, `pr_title`, and `meta.mode` / `meta.model` (if live). Optional: flash `sample_plan_live.json` in an editor to show a prior live Nemotron run without typing a key.
5. **2:20–2:50** Optional terminal: `python3 app/server.py --cli -f app/samples/sample_issue.txt` and/or `python3 app/test_mock.py`. Close: track Best Apps and Agents; free Token Factory credits; MIT repo.

## Still not this step

- YouTube upload (needs sourendas0@gmail.com)
- Devpost submit form
- Committing `.env` or printing secrets
