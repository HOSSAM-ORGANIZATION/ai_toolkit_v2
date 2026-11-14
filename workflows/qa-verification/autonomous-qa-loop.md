# Autonomous QA & Verification Loop Workflow

> Automated verification loop for Flutter features using Maestro declarative flows, screen state matrix testing, layout overflow detection, and self-healing agent corrections.

---

## 1. Objective & Philosophy

Traditional unit and widget tests cannot easily detect real-device visual regressions, screen orientation glitches, or unhandled async layout shifts.
The **Autonomous QA Loop** runs after completing feature implementation, executing real-device flows with **zero token replay costs** and delivering a compact **Lean QA Summary Card** (< 1KB) to the agent.

---

## 2. The Verification Pipeline

Follow this sequence for every completed feature:

```text
[ Feature Implemented ]
          │
          ▼
1. Generate / Verify Flow: `toolkit qa gen <feature>`
          │
          ▼
2. Execute QA Suite: `toolkit qa run <feature>`
          │
          ├───► ✅ ALL PASSED ──► Proceed to `verify-and-pr.md`
          │
          └───► ❌ FAILED ──► Read Lean QA Summary Card
                                    │
                                    ▼
                         3. Surgical Fix (Auto-Fix Loop)
                                    │
                                    ▼
                         4. Record in `ai_docs/memory.md`
                                    │
                                    ▼
                         5. Re-run `toolkit qa run <feature>` (Max 3 retries)
```

---

## 3. Step-by-Step Execution Guide

### Step 1: Ensure Flow Coverage
Verify that a declarative flow exists in `test/qa_flows/<feature>_flow.yaml`. If missing:
```bash
toolkit qa gen <feature>
```
Ensure the flow exercises the critical states defined in [`workflows/feature-delivery/screen-states-protocol.md`](../feature-delivery/screen-states-protocol.md):
- **Default / Loaded State:** Verifies primary content renders.
- **Loading State:** Verifies shimmer or loader visibility.
- **Empty State:** Verifies empty placeholder and actionable CTA button.
- **Error State:** Verifies error presentation and retry action.
- **Orientation & Overflow Check:** Switches orientation to verify zero `RenderFlex overflow`.

### Step 2: Execute Autonomous QA
```bash
toolkit qa run <feature>
# Or via Makefile:
make qa-feature FEATURE=<feature>
```

### Step 3: Consume Lean QA Summary Card
The QA engine prints a compact summary (< 1KB). Inspect the failure block:
- **Failed Step:** Exactly where the flow broke.
- **Error:** Specific assertion failure or pixel overflow amount.
- **Suspected Area:** Relevant widget / file.
- **Evidence Screenshot:** Local snapshot path for inspection.

### Step 4: Surgical Self-Healing Fix
Apply targeted repairs based on the failure category:
1. **RenderFlex Overflow:**
   - Wrap unbounded Column/Row children in `Expanded` or `Flexible`.
   - Wrap scrolling surfaces in `SingleChildScrollView` or `CustomScrollView`.
2. **Missing Element / Timeout:**
   - Verify async state machine transitions to loaded state.
   - Check widget semantics keys (`Key('...')`).
3. **Empty / Error State Failure:**
   - Install `chaos_interceptor` blueprint (`toolkit add chaos_interceptor`).
   - Ensure the UI handles empty collections (`[]`) without throwing `RangeError`.

### Step 5: Living Memory Synchronization
Whenever a real layout bug or gotcha is resolved, append an entry to `ai_docs/memory.md`:
```markdown
- **[UI Layout]**: Feature `<feature>` caused a RenderFlex overflow of 18px in landscape mode due to fixed height on header. Resolved with `LayoutBuilder` and `Flexible`.
```

---

## 4. Git Commit & Regression Suite
All `.yaml` flows in `test/qa_flows/` must be committed to Git:
```bash
git add test/qa_flows/<feature>_flow.yaml
git commit -m "test(<feature>): add autonomous maestro QA verification flow"
```
These flows form the permanent, token-free regression suite executed in CI/CD.
