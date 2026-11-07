# Maintenance: Bugfix Workflow

> Structured protocol for investigating, diagnosing, testing, and fixing defects with zero side-effect regressions.

---

## 1. Bug Intake & Classification
1. **Intake Source:** Developer prompt, QA tester report, or Sentry/Crashlytics stack trace.
2. **Reproduce & Isolate:**
   - Locate offending file and line.
   - Run `collaborative-problem-solving.md` to check if Fast-Track skip applies.
   - If non-trivial, run Socratic inquiry to identify root cause and **Blast Radius**.

---

## 2. Regression Protection
- Before applying the fix, write a minimal failing test (if `testing_gate` is strict or recommended).
- Ensure the test fails specifically due to the bug (Red state).

---

## 3. Apply Minimal Surgical Fix
- Apply the fix strictly within the offending component.
- Do not introduce unrelated refactoring in a bugfix PR.
- Adhere to **Simplicity First**: select the most direct, elegant fix.

---

## 4. Verification & Closeout
```bash
make analyze
make test
```
- Verify regression test passes (Green state).
- Document root cause and solution in `ai_docs/memory.md` if it represents a repeatable gotcha.
