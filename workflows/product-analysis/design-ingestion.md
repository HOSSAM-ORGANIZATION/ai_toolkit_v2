# Unified Design Ingestion & Design System Extractor

> Supports Google Stitch & Figma via either MCP Server or Local Folder.
> Extracts colors, typography, spacing, radii, and component themes into `DESIGN_SYSTEM.md` and generates Flutter token code.
> **Synergy:** Triggered directly or orchestrated by [`design-analysis.md`](design-analysis.md) (Step 10).

---

## 1. Input Sources & Modes

### Source A: Google Stitch
- **Mode 1 (Stitch MCP):** Query Stitch MCP tools (`get_stitch_components`, `get_stitch_tokens`) to stream screen structures and JSON layout trees.
- **Mode 2 (Local Folder):** Inspect local directory (e.g. `design_export/stitch/` or `ai_specs/design/source/`) containing exported Stitch JSON definitions, component specs, and asset previews.

### Source B: Figma
- **Mode 1 (Figma MCP):** Query Figma MCP tools (`get_figma_data`, `download_figma_images`) using file key and node IDs.
- **Mode 2 (Local Folder):** Inspect local directory containing exported design screenshots (`*.png`, `*.svg`) and exported tokens JSON (`tokens.json` from Tokens Studio or Figma Variables).

---

## 2. Ingestion & Extraction Protocol

### Step 1: Detect Directionality & Locale
1. Scan dominant language and layout in screen frames:
   - Dominant Arabic / RTL script -> mark `directionality: rtl_first`.
   - Dominant Latin / LTR script -> mark `directionality: ltr_first`.
2. Verify semantic directional intent: Back buttons and chevrons must be mirrored; horizontal margins must use start/end.

### Step 2: Extract Design Tokens
Parse the raw design data into five distinct token categories:
1. **Color Palette:**
   - Primary, Secondary, Background, Surface, Card Background.
   - Semantic Status: Success, Warning, Error, Info.
   - Text Colors: Primary Text, Subtitle Text, Disabled Text.
2. **Typography Scale & Font Matching:**
   - Scan font family, weights, font sizes, and line heights.
   - Run font matcher: `python3 bin/setup/setup_fonts.py --match "<FontName>"`
     - **Matched:** Auto-provisions TTF assets, registers in `pubspec.yaml`, and scaffolds `fonts.dart` and `text_styles.dart`:
       `python3 bin/setup/setup_fonts.py --fonts <font_key1,font_key2>`
     - **Not Matched:** Alert developer:
       1. Map to bundled font (`cairo`, `tajawal`, `inter`, `somarsans`, `public_sans`, `roboto`).
       2. Or import custom font permanently into toolkit library:
          `python3 bin/setup/setup_fonts.py --import /path/to/font_folder --name "MyFont"`
          (The font will be permanently saved to the toolkit and auto-provisioned).
   - Adhere strictly to the **Direct Sized Scale** (`light12`, `regular14`, `medium16`, `semiBold16`, `bold18`...) with `height: 1.4` for Arabic clipping prevention.
3. **Spacing & Dimensions:**
   - Standard grid steps (e.g. 4, 8, 12, 16, 20, 24, 32, 48).
4. **Border Radii & Shapes:**
   - Small (e.g. 4px), Medium (e.g. 8px), Large (e.g. 16px), Pill/Circular.
5. **Elevation & Shadows:**
   - Card shadow, modal/bottom sheet shadow, app bar elevation.

### Step 3: Write `ai_specs/design/DESIGN_SYSTEM.md`
Store the extracted tokens in a structured markdown contract:
```markdown
# Design System Specification
## Colors
- Primary: #1E3A8A (AppColors.primary)
- Surface: #F8FAFC (AppColors.surface)

## Typography
- Headline Large: 24sp / Bold (TextStyles.headlineLarge)
- Body Medium: 14sp / Regular (TextStyles.bodyMedium)

## Spacing
- p4: 4px, p8: 8px, p16: 16px, p24: 24px
```

### Step 4: Scaffold Flutter Token Code
Generate or update the token classes inside `tokens_path` (from `project_profile.yaml`):
- `colors.dart`: `abstract final class AppColors { ... }`
- `text_styles.dart`: `abstract final class TextStyles { ... }`
- `dimensions.dart`: `abstract final class Dimensions { ... }`
- `app_theme.dart`: `ThemeData` builder binding the tokens to Material 3.

### Step 5: Preserve Reference Frames for QA Verification
Save screenshot exports of screen frames to:
`ai_docs/qa/designs/<feature>.png`
These assets are used during [Autonomous QA Loop](../qa-verification/autonomous-qa-loop.md) for visual layout and hierarchy comparison.

---

## 3. Strict Verification Gate
Verify that generated token classes strictly prohibit magic literals:
- Ensure all screens reference `AppColors` and `Dimensions`.
- Run `flutter analyze` or verification script to ensure zero hardcoded color hexes.
