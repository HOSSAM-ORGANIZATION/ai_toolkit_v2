# Daily Worklog & Task Tracking Workflow

> Manages daily developer progress, open blocker tracking, and persistent task handoff.

---

## 1. Directory Structure in Host Project
```text
ai_worklog/
├── INDEX.md             # Worklog overview and recent links
├── TODOS.md             # Active cross-feature backlog
└── daily/
    └── YYYY-MM-DD.md    # Daily timestamped log
```

---

## 2. Session Start Protocol
1. Check `ai_worklog/TODOS.md` for prioritized uncompleted tasks.
2. If today's log file (`daily/YYYY-MM-DD.md`) does not exist, create it from template.

---

## 3. Session End / Task Completion
1. Update today's log with:
   - Features / phases completed.
   - PRs created or merged.
   - Any blockers encountered.
2. Check off completed items in `ai_worklog/TODOS.md`.
