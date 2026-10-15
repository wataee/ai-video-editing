# 04. Visual Styles & Safe Zones (9:16)

## 1. Strict 9:16 Safe Zone Geometry (1080 × 1920)
Mobile platforms (TikTok, Instagram Reels, YouTube Shorts) place dense interface overlays on vertical videos. All primary visual information, text, callouts, and face centers must sit strictly inside the Safe Zone container.

```
+---------------------------------------------+ (0, 0)
|             TOP EXCLUSION ZONE              | y: 0 to 220px
|      (Header, Search bar, Audio pill)       |
+---------------------------------------------+ y: 220px
|      |                               |      |
|      |                               |      |
| L    |       ACTIVE SAFE CONTENT     | R    |
| E    |            CONTAINER          | I    |
| F    |                               | G    | x: 100 to 980px
| T    |     Width: 880px              | H    | y: 220 to 1540px
|      |     Height: 1320px            | T    |
| 100  |                               | 100  | (Right buttons:
| px   |                               | px   |  like, share, save)
|      |                               |      |
+---------------------------------------------+ y: 1540px
|            BOTTOM EXCLUSION ZONE            | y: 1540 to 1920px
|   (Captions, Username, Description, Audio)   | (Height: 380px)
+---------------------------------------------+ (1080, 1920)
```

- **Top UI zone**: `220px`
- **Bottom UI/Caption zone**: `380px`
- **Left Margin**: `100px`
- **Right Margin**: `100px`
- **Content Boundary**: `x: 100..980` (width: `880px`), `y: 220..1540` (height: `1320px`).

## 2. Core Visual Language Presets

### A. `vox-data`
- **Vibe**: Investigative journalism, documentary, clean analytical data.
- **Background**: Dark charcoal `#0D0D11` with subtle technical grid overlay (`rgba(255,255,255,0.05)` spaced 40px).
- **Accents**: High-contrast canary yellow (`#FFD60A`) or neon red (`#FF3B30`).
- **Typography**: Clean mono/grotesque sans (Inter + Space Mono / Roboto Mono).
- **Motion**: Snap springs with high damping (`damping: 15, stiffness: 120`), animated bar charts growing from 0.

### B. `apple-liquid-glass`
- **Vibe**: High-end consumer hardware, premium Cupertino OS aesthetic.
- **Surface**: `backdropFilter: 'blur(24px) saturate(180%)'`, background `rgba(255, 255, 255, 0.14)`.
- **Border**: `1px solid rgba(255, 255, 255, 0.28)`, `borderRadius: 28px`.
- **Shadow**: `0 20px 40px rgba(0, 0, 0, 0.35)`.
- **Green-Screen Chroma Mode**: Optional `#00FF00` pure chroma background for rendering alpha overlays into external NLEs.

### C. `noir-tech`
- **Vibe**: High-performance developer, AI engineering, cybersecurity.
- **Background**: Deep obsidian `#09090B`.
- **Lighting**: Subtle radial gradient glow centered at `50% 30%` (`radial-gradient(circle, rgba(99,102,241,0.15) 0%, transparent 70%)`).
- **Typography**: `Inter` font weight 600 with negative tracking (`letterSpacing: -0.02em`).
- **Assets**: PNG cutouts with drop shadow `0 12px 32px rgba(0,0,0,0.6)`.

### D. `luxury-editorial`
- **Vibe**: Financial independence, legacy architecture, high-status minimalism.
- **Colorway**: Deep black `#050505` paired with warm titanium `#E5E5E5` and muted gold `#D4AF37`.
- **Motion**: Ultra-smooth bezier timing: `Easing.bezier(0.16, 1, 0.3, 1)`.
- **Typography**: High-contrast serif paired with modern geometric sans.
