# Typography Scale & Font Hierarchy (1080 × 1920 Vertical Canvas)

## 1. Safe Zone Positioning Bounds

In 9:16 mobile feeds (TikTok, Instagram Reels, YouTube Shorts), typography must be placed strictly within validated safe coordinates:

```
Canvas: 1080w × 1920h
Top Exclusion Zone:          y: 0 to 220px (Status bar, Search, Back buttons)
Top Buffer Zone:             y: 220 to 340px (Topic pills, chapter tags)
Data & Card Hero Zone:       y: 400 to 1120px (Mockups, charts, graphic lockups)
Dynamic Caption Sweet Spot:  y: 1120 to 1380px (1–3 word kinetic karaoke subtitles)
Bottom Exclusion Zone:       y: 1540 to 1920px (Username, captions, audio marquee - 380px height)
Left Exclusion Zone:         x: 0 to 100px (100px margin)
Right Exclusion Zone:        x: 950 to 1080px (130px margin for like/comment/share buttons)
Guaranteed Visible Box:      x: 100..950px, y: 220..1540px
```

---

## 2. 1080 × 1920 Type Scale & Metrics

| Element Role | Font Size (px) | Line Height | Tracking (Letter Spacing) | Max Line Length | Optimal Font Pairing |
|---|---|---|---|---|---|
| **Giant Karaoke Hero** | `88px – 108px` | `1.05` | `+0.02em` | 1–3 words (10–14 chars) | Montserrat Black / ExtraBold |
| **Section Header (Punch)** | `68px – 84px` | `1.10` | `-0.025em` | 3–4 words (16–22 chars) | Montserrat ExtraBold / Oswald Bold |
| **Card / Modal Headline** | `48px – 56px` | `1.20` | `-0.015em` | 4–6 words (24–30 chars) | Manrope SemiBold / Inter Bold |
| **Data Metric / Big Number** | `72px – 96px` | `1.00` | `-0.03em` | 6–10 chars (tabular) | Montserrat ExtraBold / Space Mono |
| **Body Subtext / Explainer** | `32px – 40px` | `1.35` | `0em` | 6–8 words (32–40 chars) | Manrope Regular / Inter Medium |
| **Pill Tag / Category Badge** | `24px – 28px` | `1.00` | `+0.05em` | 2–3 words (uppercase) | Inter SemiBold / Manrope Medium |
| **Archival Timestamp / Footnote** | `20px – 24px` | `1.20` | `+0.08em` | Single line | Monospace regular |

---

## 3. Approved Font Pairing Rules

Never combine random arbitrary fonts. Use one of these validated formulas (TheBoldFont is strictly forbidden):

### Pairing Formula A: Universal Expert Grotesque (Recommended)
- **Tier 1 (Headlines & Hook Punch)**: `Montserrat` (Black / ExtraBold) — all caps or title case.
- **Tier 2 (Body, Captions & Subtitles)**: `Manrope` or `Inter` (Regular / Medium / SemiBold) — excellent Cyrillic legibility.
- **Tier 3 (Signature Accent - 2nd Layer Only)**: `Caveat` (Bold) — tilted cursive script for emphasis.

### Pairing Formula B: Modern Tech / Interface
- **Tier 1 (Headline)**: `Montserrat` (ExtraBold) or `Inter` (ExtraBold).
- **Tier 2 (Body & Captions)**: `Inter` (Medium / Regular).
- **Tier 3 (Data & Metrics)**: Monospace or tabular figures.

---

## 4. Legibility & Anti-Clipping Standards

1. **Outer Stroke for Variable Footage**:
   - Spoken subtitles displayed directly over footage must have:
     `-webkit-text-stroke: 8px to 10px #000000; paint-order: stroke fill;`
   - Paired with drop shadow `0 10px 24px rgba(0, 0, 0, 0.95)`.
2. **Backing Cards for Dense Information**:
   - Graphs, tables, and multi-line explanations must never float directly over footage.
   - Enclose inside a frosted glass modal (`backdrop-filter: blur(24px); background: rgba(18, 22, 31, 0.65)`).
3. **Word-by-Word Color States**:
   - Inactive incoming word: `#FFFFFF` (opacity 0.65, scale 1.0).
   - Active spoken word: Gold `#FFD700` or Vivid Accent (scale 1.12 with smooth spring pop).
   - Completed past word: `#D1D5DB` (opacity 0.50, scale 1.0).
