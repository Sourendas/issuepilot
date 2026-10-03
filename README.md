# IssuePilot — Nebius x NVIDIA Global AI Hackathon

**IssuePilot** turns a pasted GitHub issue / bug report into a structured triage plan:
severity, missing repro gaps, fix plan, test ideas, and a draft PR title/body.

- **Track:** Best Apps and Agents
- **Runtime:** Nebius Token Factory + ≥1 NVIDIA open model (Nemotron)
- **Offline-first MVP:** works with a **mock planner** when `NEBIUS_API_KEY` is unset
- **Zero spend** until free Token Factory credits are applied (browser; not done here)

Entrant: **Souren Das** · `sourendas0@gmail.com`

---

## Quick start (offline mock)

```bash
cd /path/to/nebius-nvidia
cp .env.example .env   # leave placeholders; mock mode activates
python3 app/server.py
```

Open **http://127.0.0.1:8787/** — paste an issue (or **Load sample**) → human summary + plan JSON.

Footer:

- no key: `Mock planner (no API key)`
- key set: `Nebius Token Factory + NVIDIA model` plus `NEBIUS_MODEL`

One-shot (mock when `.env` has no real key):

```bash
python3 app/server.py --cli -f app/samples/sample_issue.txt
python3 app/test_mock.py
```

Checked-in sample pair: `app/samples/sample_issue.txt` → `app/samples/sample_plan.json` (mock). Live `live_plan()` is not called by the test.

---

## Live Token Factory (when key exists)

1. Apply promo / free credits on Nebius Token Factory (browser; do not invent keys).
2. Put the real key in `.env` as `NEBIUS_API_KEY` (never commit `.env`).
3. Confirm model id (`NEBIUS_MODEL`) against Token Factory catalog.
4. Restart `python3 app/server.py` — footer shows model + “Nebius Token Factory”.

### Call shape (OpenAI-compatible chat completions)

```http
POST {NEBIUS_BASE_URL}/chat/completions
Authorization: Bearer {NEBIUS_API_KEY}
Content-Type: application/json

{
  "model": "{NEBIUS_MODEL}",
  "messages": [
    {"role": "system", "content": "<triage system prompt>"},
    {"role": "user", "content": "<issue title+body>"}
  ],
  "temperature": 0.2,
  "response_format": {"type": "json_object"}
}
```

Response content is expected to be JSON matching the IssuePilot plan schema
(see `app/plan_schema.py`). Until a key is set, the server returns a deterministic mock.

---

## Layout

```
nebius-nvidia/
  README.md
  LICENSE
  .env.example
  .gitignore
  IDEA.md / NOTES.md   # local contest notes (not for public push yet)
  app/
    server.py          # stdlib HTTP server + optional urllib Token Factory call
    planner.py         # mock + live planner
    plan_schema.py
    static/index.html
    test_mock.py       # offline mock check; does not call the API
    samples/sample_issue.txt
    samples/sample_plan.json
```

---

## License

MIT
