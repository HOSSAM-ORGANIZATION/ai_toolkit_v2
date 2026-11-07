# Session Bootstrap Workflow

> Ordered session start for AI agents entering any codebase managed by Universal AI Toolkit v2.

---

## Step 0: Mandatory Profile Gatekeeper (Preflight)

1. Check for `project_profile.yaml` in the project root:
   - Run `python3 ai_toolkit/bin/check-profile .`
   - **If missing or incomplete:** HALT all code execution immediately and run:
     `python3 ai_toolkit/bin/wizard/init_profile.py --target-dir .`
2. Once validated, read `project_profile.yaml` to register:
   - `architecture`, `state_management`, `network_client`, `directionality`, `design_system`.

---

## Step 1: Read Project Living Memory

1. Read `ai_docs/memory.md` (≤ 4 KB):
   - Ingest shared component registry.
   - Note recent gotchas and architectural decisions.
2. Read `ai_docs/conventions.md`:
   - Inspect concrete class mappings for shared UI widgets (`AppButton`, `AppImage`, etc.).

---

## Step 2: Determine Session Mode

- **Lite Mode (Bugfix / Small Edits / Code Review):**
  - Skip reading indexes.
  - Consult `LOADMAP.md` for target tag.
  - Load only the relevant 60-line Agent Cards (e.g. `+ui` or `+data`).
  
- **Full Mode (New Feature / Major Refactor):**
  - Read `ai_specs/INDEX.md` (or feature spec).
  - Review screen states matrix and PRD requirements.
  - Proceed to `workflows/feature-delivery/make-plan.md`.
