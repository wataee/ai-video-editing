# 08. Typography Scale & Pairing Matrix (9:16)

## 1. 1080x1920 Type Scale
Vertical video demands large, instantly legible type. Never set body text under 36px.

| Role | Font Size | Line Height | Tracking (Letter Spacing) | Weight |
|---|---|---|---|---|
| **Mega Hook** | `96px - 120px` | `1.05` | `-0.03em` | `900` (Black) |
| **Headline / Stat** | `72px - 88px` | `1.15` | `-0.02em` | `800` (ExtraBold) |
| **Section Header** | `48px - 60px` | `1.20` | `-0.01em` | `700` (Bold) |
| **Captions (Karaoke)** | `44px - 56px` | `1.25` | `0` | `800` (ExtraBold) |
| **Subtext / Detail** | `32px - 38px` | `1.35` | `+0.01em` | `500` (Medium) |

## 2. Approved Font Pairings
Available in `assets/02_FONTS/`:

### Pairing 1: The Viral Reel Power Pair (Mahabur Rahman / Gadzhi)
- **Primary / Hook**: `Montserrat-Black` (All caps, beveled or high drop shadow, neon/red or white).
- **Secondary / Accent**: `Caveat-Bold` or `SegoeScript-Bold` (Italic handwritten signature, warm gold `#FFD700` or white, overlapping bottom-right of primary).

### Pairing 2: Modern Tech & Interface (Apple / Vercel)
- **Primary**: `Inter-Bold` / `Inter-ExtraBold`.
- **Secondary**: `Inter-Medium` (Clean, neutral, perfect UI legibility).

### Pairing 3: High-Impact Editorial (Vox / Documentary)
- **Primary**: `Oswald-Bold` (Condensed vertical strength).
- **Secondary**: `Rubik-Medium` or monospace numbers.

## 3. Formatting & Legibility Rules
- Maximum **3 to 5 words per line** on mobile.
- Use uppercase for single emphatic punchlines; use sentence case for multi-line storytelling.
- Add subtle text-shadow on light text over variable backgrounds:
  `textShadow: '0 4px 16px rgba(0, 0, 0, 0.7)'`.
