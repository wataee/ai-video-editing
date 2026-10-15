# Typography Scale & Font Hierarchy (1080 × 1920 Vertical Canvas)

## 1. Safe Zone Positioning Bounds

In 9:16 mobile feeds (TikTok, Instagram Reels, YouTube Shorts), typography must be placed strictly within validated safe coordinates:

```
Canvas: 1080w × 1920h
Top Exclusion Zone:          y: 0 to 200px (Status bar, Search, Back buttons)
Top Buffer Zone:             y: 200 to 320px (Topic pills, chapter tags)
Data & Card Hero Zone:       y: 400 to 1120px (Mockups, charts, graphic lockups)
Dynamic Caption Sweet Spot:  y: 1120 to 1380px (1–3 word kinetic karaoke subtitles)
Bottom Exclusion Zone:       y: 1480 to 1920px (Username, captions, audio marquee)
Right Rail Exclusion Zone:   x: 940 to 1080px (Like, comment, share buttons)
Left Buffer Zone:            x: 0 to 60px (Screen bezel clipping)
Guaranteed Visible Box:      x: 60..940px, y: 220..1480px
```

---

## 2. 1080 × 1920 Type Scale & Metrics

| Element Role | Font Size (px) | Line Height | Tracking (Letter Spacing) | Max Line Length | Optimal Font Pairing |
|---|---|---|---|---|---|
| **Giant Karaoke Hero** | `88px – 108px` | `1.05` | `+0.02em` | 1–3 words (10–14 chars) | Montserrat Black / The Bold Font |
| **Section Header (Punch)** | `68px – 84px` | `1.10` | `-0.025em` | 3–4 words (16–22 chars) | Oswald Bold / Canela Serif |
| **Card / Modal Headline** | `48px – 56px` | `1.20` | `-0.015em` | 4–6 words (24–30 chars) | Inter Bold / SF Pro Display |
| **Data Metric / Big Number** | `72px – 96px` | `1.00` | `-0.03em` | 6–10 chars (tabular) | Space Mono / JetBrains Mono |
| **Body Subtext / Explainer** | `32px – 40px` | `1.35` | `0em` | 6–8 words (32–40 chars) | Inter Medium / SF Pro Text |
| **Pill Tag / Category Badge** | `24px – 28px` | `1.00` | `+0.05em` | 2–3 words (uppercase) | Inter SemiBold / Space Mono |
| **Archival Timestamp / Footnote** | `20px – 24px` | `1.20` | `+0.08em` | Single line | Monospace regular |

---

## 3. The 3-Tier Font Pairing Rules

Never combine random arbitrary fonts. Use one of these validated 3-tier formulas:

### Pairing Formula A: Tech / Modern SaaS (Devin Jatho / Apple)
- **Tier 1 (Hero & Modals)**: `Inter-Bold` / `PP Neue Montreal` (High geometric clarity, tight negative tracking `-0.02em`).
- **Tier 2 (Body & Explanations)**: `Inter-Medium` (Neutral, highly legible on OLED screens).
- **Tier 3 (Data & Metrics)**: `Space Mono` / `SF Mono` (Tabular numbers for tickers and charts).

### Pairing Formula B: Viral Reel Lockup (Mahabur Rahman / Iman Gadzhi)
- **Tier 1 (Punch Headline)**: `Montserrat-Black` (ALL CAPS, beveled 3D look or heavy drop shadow, neon red `#FF1429` or pure white).
- **Tier 2 (Signature Accent)**: `Caveat-Bold` / `SegoeScript-Bold` (Italic cursive script, warm gold `#E8C872`, tilted -8° to -12°, overlapping bottom-right of primary word).
- **Tier 3 (Subtitles & Body)**: `Inter-Medium` (Clean sans).

### Pairing Formula C: Investigative Editorial (Vox / Johnny Harris)
- **Tier 1 (Headline Box)**: `Oswald-Bold` / `Franklin Gothic Heavy` (ALL CAPS, enclosed inside a solid `#FFE600` canary yellow rectangle with black text).
- **Tier 2 (Narrative Body)**: `Rubik-Regular` / `Inter-Medium`.
- **Tier 3 (Map & Coordinate Stamps)**: `Space Mono` / `Courier Prime` (Letter spaced `+0.08em`).

---

## 4. Legibility & Anti-Clipping Standards

1. **Outer Stroke for Variable Footage**:
   - Spoken subtitles displayed directly over talking head or street footage must have:
     `-webkit-text-stroke: 8px to 10px #000000; paint-order: stroke fill;`
   - Paired with drop shadow `0 10px 24px rgba(0, 0, 0, 0.95)`.
2. **Backing Cards for Dense Information**:
   - Graphs, tables, and multi-line explanations must never float directly over footage.
   - Enclose inside a frosted glass modal (`backdrop-filter: blur(24px); background: rgba(18, 22, 31, 0.65)`).
3. **Word-by-Word Color States**:
   - Inactive incoming word: `#FFFFFF` (opacity 0.65, scale 1.0).
   - Active spoken word: Neon Yellow `#FFFD38` or Cyber Green `#00FF66` (scale 1.18 with spring pop).
   - Completed past word: `#D1D5DB` (opacity 0.50, scale 1.0).
