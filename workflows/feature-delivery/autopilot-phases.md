# Autopilot Workflow: Consecutive Phase Execution

> Automates the sequential execution of unfinished phases in `plan.md` under strict quality and context boundaries.

---

## 1. Autopilot Execution Modes

| Mode | Behavior | Best Used When |
| :--- | :--- | :--- |
| **`Direct`** | Executes consecutive phases in the same conversation thread. | Small features with ≤ 3 compact phases. |
| **`Safe`** | Launches an isolated task subagent for each phase; parent thread only reviews and checks off tasks. | Complex multi-layer features; prevents context window drift. |
| **`Cloud`** | Headless remote execution via CI or background task. | Long-running migrations and upgrades. |

---

## 2. Autopilot Loop Protocol

```text
LOOP for each Phase in plan.md where Status == PENDING:
  1. Ingest Phase Load: tags -> Load lines 1-60 of matching Agent Cards via LOADMAP.md.
  2. Execute Phase tasks strictly according to Clean Code & Design System rules.
  3. Run verification: `make analyze` && `make codegen` (&& `make test` if testing_gate == strict).
  4. If verification passes:
     - Mark phase tasks [x] DONE.
     - Trigger automatic plan splitter:
       `python3 ai_toolkit/bin/plan-splitter path/to/plan.md`
  5. If verification fails:
     - STOP autopilot immediately.
     - Report compilation or test failures to the developer.
END LOOP
```

---

## 3. Autopilot Exit Gate
When all phases are marked DONE:
- Trigger `workflows/feature-delivery/verify-and-pr.md`.
- Generate/update the Feature README.
- Update the Project Living README.
- Print ready-for-review summary.
