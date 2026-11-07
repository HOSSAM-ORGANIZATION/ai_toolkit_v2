## Agent card

**LOADMAP tags:** `design-system`, `ui`
**Read rest of this file:** no — this card contains the full enforceable rule.

### Must
- Consume colors exclusively through `AppColors` or `Theme.of(context).colorScheme`.
- Consume typography exclusively through `AppTypography`, `TextStyles`, or `Theme.of(context).textTheme`.
- Consume spacing and padding exclusively through `Dimensions` or `AppSpacing` tokens.
- Use project-standard shared UI wrappers (`AppButton`, `AppImage`, `AppTextField`, `AppBackButton`) documented in `ai_docs/conventions.md`.
- Ensure all directional layouts use semantic Directional APIs (`PaddingDirectional`, `AlignmentDirectional`).

### Must not
- Hardcode literal hex colors (e.g. `Color(0xFF...)`, `Colors.blue`) in screens or widgets.
- Use arbitrary font sizes or ad-hoc weights (`TextStyle(fontSize: 15.3)`).
- Interleave magic numbers in padding or margins (`EdgeInsets.all(13)`).
- Reinvent custom buttons or raw `Image.network` / `SvgPicture` widgets outside the designated shared wrappers.

### When to load the rest
- Only when extending the core Design System token classes or building new token wrappers.

### Related (cards first)
- `+ui` for component composition; `+theme` for ThemeData tokens; `ai_docs/conventions.md` for project wrappers.

### Card protocol
- This card is the authoritative contract. Do not read past line 60 during feature implementation.
- If a token is missing, define it inside the design system token file—never inline it as a magic literal.

# Design System Token Compliance & Zero-Hardcoding Mandate

## Purpose
Ensures complete visual consistency, dark/light theme adaptability, and design-fidelity across all application screens by outlawing magic numbers and hardcoded styling literals.

## Token Mapping Matrix

| Styling Concern | Permitted Consumption Source | Prohibited Anti-Pattern |
| :--- | :--- | :--- |
| **Colors** | `AppColors.<token>` or `Theme.of(context).colorScheme.<token>` | `Color(0xFF123456)` or `Colors.red` |
| **Typography** | `TextStyles.<token>` or `Theme.of(context).textTheme.<token>` | `TextStyle(fontSize: 16, color: ...)` |
| **Spacing / Padding** | `Dimensions.p<token>` or `AppSpacing.<token>` | `EdgeInsets.all(14.0)` |
| **Border Radii** | `Dimensions.r<token>` or `AppRadii.<token>` | `BorderRadius.circular(11.0)` |
| **Elevation / Shadow** | `AppShadows.<token>` | Ad-hoc `BoxShadow(...)` lists |

## Shared UI Wrappers Enforcement
Every application must declare its standard UI components in `ai_docs/conventions.md`. 
Agents must inspect that table and use those concrete widgets exclusively:
- Buttons: Standard elevated button wrapper with built-in loading and disabled states.
- Images: Cached network image wrapper with placeholder shimmer and error icon fallback.
- Icons: Vector SVG icon wrapper with contextual color filtering and auto-mirroring.
- Back Controls: RTL-aware directional back button affordance.
