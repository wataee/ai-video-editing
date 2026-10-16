# 13. After Effects ExtendScript (Secondary Engine Standard)

## 1. Role of After Effects in Pipeline
- **Strictly Secondary**: Remotion is the primary engine. After Effects is used ONLY when an editable `.aep` project file is requested or for specialized complex motion graphics that cannot be created parametrically in React.
- **Monolithic Script Execution**: Interaction with After Effects is performed EXCLUSIVELY by generating a self-contained ExtendScript file (`scripts/build_ae_project.jsx`). The user executes the script manually via `File -> Scripts -> Run Script File...`.
- **Mandatory Undo Group**: All ExtendScript code must be wrapped in `app.beginUndoGroup("AI Video Build")` and `app.endUndoGroup()`.
- **No MCP Bridge**: Standalone MCP servers, background daemons, or socket bridges for AE are disabled.
- **Mandatory Approval First**: No After Effects composition may be assembled without an approved `beat_sheet.json` or `edit_plan.json` (`approved: true`).

## 2. Ingest & Color Grading Rules
- **No Exposure Fix Layer**: Fixing blown-out iPhone HDR (HLG/PQ) via an `Exposure -2.2` or `Gamma 0.92` adjustment layer across the whole frame is **strictly forbidden**.
- **Mandatory Pre-Ingest**: All raw footage must first pass `tools/ingest.py` (hardware tonemapped to SDR Rec.709, CFR 30 fps) before being imported into After Effects.
- **No Dark Vignettes**: Dimming the whole frame with dark feathered vignettes (30%+) to mask overexposure is forbidden.

## 3. Safe Zone Enforcement in AE
- Vertical 9:16 (`1080 x 1920`):
  - Top margin: `220 px`
  - Bottom margin: `380 px`
  - Left margin: `100 px`
  - Right margin: `130 px`
  - Captions zone: `y = 1120..1380 px`

## 4. Scripting Standards & Plugin Fallbacks
- All scripts must use relative paths or dynamic project paths (`File($.fileName).parent.parent`). Absolute hardcoded user paths are forbidden.
- **Universal matchName**: Never use localized effect names (e.g., Russian UI names). Always apply effects via internal `matchName` (e.g., `ADBE Glo2`, `ADBE Gaussian Blur 2`).
- **Safe Plugin Fallbacks**: Use `safeApplyEffect(layer, primaryMatchName, fallbackMatchName, params)` from `scripts/ae_helpers.jsx` so missing third-party plugins cleanly fall back to native AE effects without crashing.
