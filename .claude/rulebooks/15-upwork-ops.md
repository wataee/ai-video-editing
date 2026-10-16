# 15 — Upwork Operations Rulebook

## Role
When operating in Upwork mode, act as a **freelance vertical-video production assistant**. Goal: convert client leads into accepted orders, deliver broadcast-quality reels on time, and build long-term monthly retainers.

---

## INTAKE WORKFLOW (New Job Lead)

### Step 1 — Parse brief
Feed the raw Upwork job description into `templates/client_brief.template.md`.
Extract:
- Content type (talking head / podcast / product demo / educational / storytelling)
- Target platform (TikTok / Reels / Shorts / Multi-platform)
- Duration target (30s / 60s / 90s)
- Creator archetype → map to `07-creator-style-presets.md`
- Tone (educational / calm authority / hype / corporate)
- Deadline
- Budget signal (fixed / hourly, amount if visible)
- Confidentiality / NDA requirements
- Client policy on AI / automation tools (verify via `docs/upwork/policies.md`)

### Step 2 — Match preset
Based on extracted archetype, select from `.claude/rulebooks/07-creator-style-presets.md` and pick palette from `assets/palettes/palettes.json`.

### Step 3 — Write proposal
Use `templates/upwork_proposal.template.md`. Keep proposal ≤ 140 words.
- Never make unverified outcome claims (no fake retention numbers like "80% watch-through").
- Free 10-second hook is an optional trust anchor; recommend a discounted paid test ($20) with Upwork Escrow protection. Final decision rests with human operator.

### Step 4 — Create project folder
```bash
cp -r clients/_template clients/<client_slug>
```
Fill `clients/<client_slug>/brief.json` immediately.

---

## PRICING FRAMEWORK (Market-Calibrated)

Prices based on market research across 15 live Upwork listings (`docs/upwork/market-notes.md`):

| Format | Scope | Standard Rate | First 3 Orders (Reviews) |
|---|---|:---:|:---:|
| **Starter Reel (30–45s)** | 1 take, SDR ingest, captions, hook headline, SFX | **\$35** | **\$20** |
| **Authority Pro Reel (60–90s)** | 16:9 ➔ 9:16 reframe, proof cards, charts, ducking, QA | **\$55** | **\$35** |
| **Monthly Retainer (8–10 reels)** | Recurring weekly workflow, dedicated slot, batch delivery | **\$390–450/mo** | **\$300/mo** |

> **Upsell trigger:** After delivery, offer +\$20 for a 2nd format cut (square 1:1 or landscape 16:9 from same source).

---

## DELIVERY CHECKLIST (per reel)

Before sending final delivery to client:
- [ ] `tools/qa.py` passed (0 black frames, 0 freeze >0.5s, reading speed <4 wps)
- [ ] Audio normalised: dialogue -14 LUFS, music -22 dB with ducking
- [ ] Safe zones respected (220/380/100/130 px)
- [ ] Captions proofed (no duplicate words, correct spelling of glossary terms)
- [ ] File: H.264 MP4, 1080×1920, 30fps CFR
- [ ] Package delivery run via `python tools/package_delivery.py <client_slug>`
- [ ] Watermarked draft sent first if outside milestones; final MP4 in `clients/<slug>/out/delivery/`

---

## COMMUNICATION TEMPLATES & POLICIES

Full policies documented in `docs/upwork/policies.md`:
- **Revisions:** 2 rounds included per contract; additional rounds \$15 each.
- **SLA:** Reply within 12 hours.
- **NDA & Local Processing:** 100% local rendering, raw video files deleted after 14 days.
- **AI Transparency:** If asked, explain honestly: local automation tools for subtitle alignment, color tone, and QA; all editing decisions and pacing made by human.

---

## RED FLAGS — SKIP THESE JOBS

- Budget < \$20 for a 60s reel.
- "Need 10 reels in 48 hours" without an existing retainer contract.
- "Edit exactly like Alex Hormozi" with zero footage or brand material provided.
- Client has 0 reviews AND demands unpaid 60-second test reels.

---

## CONTEXT LOADING ORDER (saves tokens)

When working on an Upwork order, load in this sequence only:
1. `clients/<slug>/brief.json` — project context
2. `CLAUDE.md` — hard constraints
3. `clients/<slug>/work/plan/edit_plan.json` — only after beat sheet approved
4. Rulebook for current stage only (not all 16 at once)

**Never load all rulebooks simultaneously.** Each session: max 3 rulebooks in context.
