# Nebius x NVIDIA — IDEA (Best Apps and Agents)

## Project name
**IssuePilot**

## One-liner
A practical web app/agent that takes a GitHub issue (or pasted bug report), uses **NVIDIA Nemotron** on **Nebius Token Factory** to classify severity, propose a fix plan, and draft a PR description — something a solo developer would actually use.

## Why this track
- Fits **Best Apps and Agents**: real utility, not robotics.
- Satisfies hard requirements: runtime call to **Nebius Token Factory** + ≥1 **NVIDIA open model** (Nemotron Nano/Super for speed; Ultra only if credits allow).
- Solo-buildable; no physical hardware (skip Physical AI).

## User & problem
Indie hackers triage issues slowly. IssuePilot turns a raw issue into a structured plan + draft response using open NVIDIA models on Nebius infra.

## Core features (MVP)
1. Paste issue title/body (optional GitHub URL fetch if free API allows).
2. Token Factory chat completion with Nemotron → JSON: severity, repro steps gaps, fix plan, test ideas, PR title/body.
3. Simple FastAPI + HTML UI; show model id + “served via Nebius Token Factory” in UI footer (for judges).
4. Public repo, MIT, README with setup using env vars for Nebius API key.
5. Demo video ≤3 min + working demo URL (GitHub Pages front + free backend if possible, or recorded local + public instructions).

## Tech stack (free tiers / hackathon credits only)
| Layer | Choice |
| --- | --- |
| Inference | Nebius Token Factory → Nemotron (Nano/Super first) |
| Credits | Free form code `NEBIUS-DEVPOST-GLOBAL26` ($25); optional Builders Program +$25 |
| App | Python FastAPI + static UI |
| Optional | Tavily free/builder credits for “related docs search” (also Best Use of Tavily prize) |
| Hosting | Local + public GitHub; demo URL if free host available without card |

## Out of scope
- Physical AI / robots  
- Paid Nebius beyond free credits  
- Inventing fake API keys — Souren login only if form needs Google/GitHub  

## Demo plan
Live: paste a sample bug → IssuePilot returns plan → show network/log proof of Token Factory model call in README screenshots.
