# 15 — Upwork Operations Rulebook

## Role
When operating in Upwork mode, act as a **freelance vertical-video production assistant**. Goal: convert client briefs into accepted orders, deliver on time, upsell.

---

## INTAKE WORKFLOW (New Job Lead)

### Step 1 — Parse brief
Feed the raw Upwork job description into `templates/client_brief.template.md`.
Extract:
- Content type (talking head / product demo / tutorial / storytelling)
- Target platform (TikTok / Reels / Shorts)
- Duration target (15s / 30s / 60s)
- Creator archetype → map to `07-creator-style-presets.md`
- Tone (educational / hype / calm / authority)
- Deadline
- Budget signal (fixed / hourly, amount if visible)

### Step 2 — Match preset
Based on extracted archetype, select from `.claude/rulebooks/07-creator-style-presets.md` and pick palette from `assets/design-system/palettes.json`.

### Step 3 — Write proposal
Use `templates/upwork_proposal.template.md`. Always offer a free 10-second hook preview (reference `10-hook-patterns.md` archetype #1 or #2). Keep proposal ≤ 150 words.

### Step 4 — Create project folder
```
cp -r clients/_template clients/<client_slug>
```
Fill `clients/<client_slug>/brief.json` immediately.

---

## PRICING FRAMEWORK

| Format | Scope | Rate |
|---|---|---|
| 30s vertical reel (1 take) | transcribe + edit + captions + SFX | \$45–75 |
| 60s vertical reel | full pipeline | \$75–120 |
| Hook-only (10s) | free sample / upsell anchor | \$0 → \$25 |
| Monthly retainer (8 reels) | recurring | \$300–450/mo |

> **Upsell trigger:** After delivery, offer +\$20 for a 2nd format cut (square 1:1 or landscape 16:9 from same source).

---

## DELIVERY CHECKLIST (per reel)

Before sending final file to client:

- [ ] `tools/qa.py` passed (0 black frames, 0 freeze >0.5s, reading speed <4 wps)
- [ ] Audio normalised: voice -14 LUFS, music -22 dB with ducking
- [ ] Safe zones respected (220/380/100/130 px)
- [ ] Captions proofed (no duplicate words, correct speaker)
- [ ] File: H.264 MP4, 1080×1920, 30fps, ≤50MB
- [ ] Watermarked draft sent first, final after payment

---

## COMMUNICATION TEMPLATES

### After client messages (reply within 2h rule)
> "Thanks [Name]! I've reviewed your brief. To get started I need: [1 raw video file / reference link / voice-over audio]. ETA: [X] business days."

### Revision policy (state upfront)
> "Package includes 2 revision rounds. Additional rounds \$15 each."

### When client sends low-quality footage
> "The footage is [dark / shaky / low-res]. I can [color grade / stabilize / upscale] it — this adds [1 day / \$15]. Alternatively, I work with what you have, but results may vary."

---

## RED FLAGS — SKIP THESE JOBS

- Budget < \$25 for a 60s reel
- "Need 10 reels in 3 days" (without retainer)
- "Same style as [competitor]" with zero reference material
- Client has 0 reviews AND fixed budget < \$40

---

## CONTEXT LOADING ORDER (saves tokens)

When working on an Upwork order, load in this sequence only:
1. `clients/<slug>/brief.json` — project context
2. `CLAUDE.md` — hard constraints
3. `clients/<slug>/work/edit_plan.json` — only after beat sheet approved
4. Rulebook for current stage only (not all 14 at once)

**Never load all rulebooks simultaneously.** Each session: max 3 rulebooks in context.
