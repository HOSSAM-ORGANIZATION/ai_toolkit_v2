# Universal AI Toolkit v2 — Master Index

> Stable entrypoint for AI coding agents across all codebases managed by Universal AI Toolkit v2.

---

## 1. Golden Execution Path

Before taking any action in this repository, follow this exact sequence:

1. **Verify Profile:** Check that `project_profile.yaml` exists in the project root. If absent, HALT and run `make toolkit-init`.
2. **Read Project Identity:** Inspect `project_profile.yaml` to learn the project's state management, architecture, network stack, and design tokens path.
3. **Ingest Living Memory:** Read `ai_docs/memory.md` (gotchas) and `ai_docs/conventions.md` (shared widget mappings).
4. **Lean Loading:** Check `LOADMAP.md` for the tags matching your task. Read **only lines 1–60** of matching leaf rules.
5. **Simplicity First:** Propose the simplest, cleanest solution first. Answer the 3 Impact Analysis questions before executing code.

---

## 2. Task Routing Table

| Task | Workflow / Rule |
| :--- | :--- |
| **Session Start / Resume** | [`workflows/session/bootstrap-session.md`](workflows/session/bootstrap-session.md) |
| **Initialize / Repair Project Profile** | [`bin/wizard/init_profile.py`](bin/wizard/init_profile.py) |
| **Ingest Design (Stitch / Figma)** | [`workflows/product-analysis/design-ingestion.md`](workflows/product-analysis/design-ingestion.md) |
| **Plan a New Feature** | [`workflows/feature-delivery/make-plan.md`](workflows/feature-delivery/make-plan.md) |
| **Evaluate Screen States & Scenarios** | [`workflows/feature-delivery/screen-states-protocol.md`](workflows/feature-delivery/screen-states-protocol.md) |
| **Implement a Single Phase** | [`workflows/feature-delivery/implement-phase.md`](workflows/feature-delivery/implement-phase.md) |
| **Run Autopilot on Remaining Phases** | [`workflows/feature-delivery/autopilot-phases.md`](workflows/feature-delivery/autopilot-phases.md) |
| **Verify Code & Prepare PR** | [`workflows/feature-delivery/verify-and-pr.md`](workflows/feature-delivery/verify-and-pr.md) |
| **Collaborative Bugfix / Inquiry** | [`workflows/maintenance/collaborative-problem-solving.md`](workflows/maintenance/collaborative-problem-solving.md) |
| **Backend API Contract Collaboration** | [`workflows/api-analysis/backend-contract.md`](workflows/api-analysis/backend-contract.md) |
| **Update Daily Worklog & TODOs** | [`workflows/worklog/daily-log.md`](workflows/worklog/daily-log.md) |
| **Split Large Plan Files (< 8KB)** | [`bin/plan-splitter`](bin/plan-splitter) |
| **Sync Localization Keys (ARB/JSON)** | [`bin/l10n-sync.py`](bin/l10n-sync.py) |
| **Verify Toolkit Integrity** | [`setup/verify-setup.sh`](setup/verify-setup.sh) |

---

## 3. Core Rules Quick Reference

- **Design System Enforcement:** [`rules/flutter/design-system-enforcement.md`](rules/flutter/design-system-enforcement.md) (Zero hardcoding).
- **Clean Code & Applied Patterns:** [`rules/dart/clean-code-and-patterns.md`](rules/dart/clean-code-and-patterns.md) (SRP, DRY, Factory/Strategy/Builder).
- **Modern Dart 3+ Presentation:** [`rules/dart/presentation-clean-code.md`](rules/dart/presentation-clean-code.md) (Sealed classes, Records, exhaustiveness).
- **UI Performance & Graphics Math:** [`rules/flutter/ui-performance-and-graphics.md`](rules/flutter/ui-performance-and-graphics.md) (RepaintBoundary, memory leak disposal, math transparency).
