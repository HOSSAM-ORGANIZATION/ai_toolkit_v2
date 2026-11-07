# AI Agent Configuration & Guidelines

This codebase uses **Universal AI Toolkit v2**.

## Golden Rules for Agents:
1. **Mandatory Profile Gate:** Never implement features or refactors without `project_profile.yaml` present.
2. **Lean Loading Protocol:** Read only lines 1–60 of tagged rule files in `ai_toolkit/rules/`. Do not ingest untagged files or browse indexes.
3. **Design System Adherence:** Never hardcode literal hex colors (`Color(0xFF...)`), magic numbers, or arbitrary font sizes. Consume `AppColors`, `TextStyles`, and `Dimensions` tokens.
4. **Dart 3+ Presentation:** Use `sealed class` for UI states and `Records` for transient tuples.
5. **Memory Leak Prevention:** Always dispose animation controllers, tickers, scroll controllers, and stream subscriptions.
6. **Plan Size Guard:** Keep `plan.md` < 8KB. When a phase is completed, rotate it to `history.md` via `toolkit plan-split`.
