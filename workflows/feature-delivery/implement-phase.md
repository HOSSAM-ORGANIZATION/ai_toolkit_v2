# Feature Delivery: Implement Phase Workflow

> Executes a single phase from `plan.md` using Lean Loading cards and strict Clean Code rules.

---

## 1. Phase Preflight
1. Read the current phase block from `ai_specs/features/<feature>/plan.md`.
2. Extract the `Load:` tags declared in the phase (e.g. `Load: [ui, state, design-system]`).
3. Consult `LOADMAP.md` and read **lines 1–60** of each leaf file matching those tags.
4. Verify that you have NOT loaded untagged rules or indexes.

---

## 2. Implementation Rules of Engagement
1. **Design System Enforcement:**
   - Consume colors, typography, and dimensions from tokens only.
   - Zero hardcoded colors or magic numbers.
2. **Modern Dart 3+ in UI:**
   - Use `sealed class` for UI states.
   - Use `Records` for transient data pairs.
   - Provide a 1-sentence rationale for key architectural decisions.
3. **Memory & Performance:**
   - Dispose all controllers and streams in stateful widgets.
   - Wrap animated widgets in `RepaintBoundary`.
4. **Clean Code & Patterns:**
   - Single responsibility per class. Decompose large widgets into sub-widgets.
   - Keep domain pure Dart; no UI imports in domain.

---

## 3. Post-Phase Verification
1. Run static analysis:
   ```bash
   make analyze
   ```
2. Run code generation if models, DI, or serializers were altered:
   ```bash
   make codegen
   ```
3. Run tests if `testing_gate: strict`:
   ```bash
   make test
   ```
4. Mark phase tasks `[x]` in `plan.md`.
5. Rotate to `history.md` if `plan.md` exceeds 8KB:
   ```bash
   python3 ai_toolkit/bin/plan-splitter ai_specs/features/<feature>/plan.md
   ```
