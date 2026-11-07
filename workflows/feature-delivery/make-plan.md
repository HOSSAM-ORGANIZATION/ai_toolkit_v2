# Feature Delivery: Make Plan Workflow

> Translates a feature spec or design into a phased, checkable plan obeying context budget limits (< 8KB).

---

## 1. Preflight Checks
1. Ensure `project_profile.yaml` is validated.
2. Ensure Git working directory is clean (`git status`).
3. Check `workflows/maintenance/collaborative-problem-solving.md` to run Socratic inquiry or verify if Fast-Track skip applies.

---

## 2. Plan Structure Requirements
Write `ai_specs/features/<feature>/plan.md` using this strict structure:

1. **Header & Context Pack:**
   - Feature Name, Target Flavors, Primary Architecture Layer.
   - Tag loadouts: `Load: [ui, state, data, ...]`.
2. **Screen States & Scenarios Checklist:**
   - Ingest from `workflows/feature-delivery/screen-states-protocol.md`.
   - List explicit states: Loading, Error, Loaded, Empty, Refreshing, Offline-first, Retry actions.
3. **Phased Execution Tasks:**
   - Break feature into 2 to 5 discrete phases:
     - *Phase 1: Domain & Contracts (Entities, Use Cases, Repositories)*
     - *Phase 2: Data Layer & Remote/Local Datasources*
     - *Phase 3: Presentation State & Controllers (Sealed classes, BLoC/Riverpod)*
     - *Phase 4: UI Screen & Widgets (Consuming Design System tokens)*
     - *Phase 5: Navigation, Localization & Verification*
   - Each phase must have checkable `- [ ]` tasks, explicit `Inputs`, and `Touches` file lists.

---

## 3. Context Budget Guard
- Keep `plan.md` strictly under 8,192 bytes (8 KB).
- When older phases complete, run `python3 ai_toolkit/bin/plan-splitter` to rotate them to `history.md`.
