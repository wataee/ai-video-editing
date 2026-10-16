# 04. Visual Styles & Safe Zones (9:16)

## 1. Strict 9:16 Safe Zone Geometry (1080 × 1920)
Mobile platforms (TikTok, Instagram Reels, YouTube Shorts) place dense interface overlays on vertical videos. All primary visual information, text, callouts, and face centers must sit strictly inside the Safe Zone container.

```
+---------------------------------------------+ (0, 0)
|             TOP EXCLUSION ZONE              | y: 0 to 220px
|      (Header, Search bar, Audio pill)       | (Height: 220px)
+---------------------------------------------+ y: 220px
|      |                               |      |
|      |                               |      |
| L    |       ACTIVE SAFE CONTENT     | R    |
| E    |            CONTAINER          | I    |
| F    |                               | G    | x: 100 to 950px
| T    |     Width: 850px              | H    | y: 220 to 1540px
|      |     Height: 1320px            | T    |
| 100  |                               | 130  | (Right buttons:
| px   |                               | px   |  like, share, save)
|      |                               |      |
+---------------------------------------------+ y: 1540px
|            BOTTOM EXCLUSION ZONE            | y: 1540 to 1920px
|   (Captions, Username, Description, Audio)   | (Height: 380px)
+---------------------------------------------+ (1080, 1920)
```

### Exact Safe Zone Dimensions:
- **Top Exclusion Zone**: `220 px`
- **Bottom Exclusion Zone**: `380 px`
- **Left Margin**: `100 px`
- **Right Margin**: `130 px`
- **Active Content Container**: `x: 100..950 px`, `y: 220..1540 px` (Width: 850px, Height: 1320px).
- **Default Subtitle / Caption Zone**: strictly `y: 1120..1380 px`.

## 2. Visual Principles (From Senior Editors)
1. **Never dark-vignette the whole frame**: Aggressive dark vignettes make footage muddy and amateur. Keep lighting natural.
2. **Face Protection**: Captions and graphics must NEVER cover the speaker's mouth or eyes.
3. **Proof-Driven B-Roll**: Use real screenshots, real screen recordings, code editors, or product close-ups instead of generic abstract stock footage.
4. **Movement References Only**: References are used to analyze rhythm, camera speed, and layout balance — not to copy someone's graphic or voiceover.
