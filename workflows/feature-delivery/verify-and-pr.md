# Feature Delivery: Verify & PR Workflow

> Final quality gate and documentation synchronization before committing and creating a Pull Request.

---

## 1. Automated Quality Gate
Execute the build verification suite:
```bash
# 1. Format code
make format

# 2. Re-run codegen to verify generated files match definitions
make codegen

# 3. Static Analysis (zero warnings/errors permitted)
make analyze

# 4. Test Suite Execution
make test

# 5. Autonomous QA & Visual Verification (Screen States & Overflows)
make qa-feature FEATURE=<feature>
```

> [!NOTE]
> If `make qa-feature` fails or reports a `RenderFlex overflow`, follow the [Autonomous QA Loop](../qa-verification/autonomous-qa-loop.md) self-healing guide before proceeding.

---

## 2. Living Documentation Synchronization

### A. Generate / Update Feature README (`lib/features/<feature>/README.md`)
Using `templates/specs/feature-readme.template.md`:
- Document what the feature does.
- Detail the architecture map (data, domain, presentation).
- Outline required packages and external dependencies.
- Fill in the **Plug & Play Export Guide** (how another developer or agent can copy this feature into another app in 2 minutes).

### B. Update Project Living README (`README.md`)
- Add or update the row in the **Features Catalog** table:
  `| <FeatureName> | lib/features/<feature> | ✅ Done | [Plan](...) | [README](lib/features/<feature>/README.md) |`
- Record any new gotcha or technical learning in `ai_docs/memory.md`.

---

## 3. Git Commit & PR Summary
1. Inspect git diff:
   ```bash
   git status
   git diff --stat
   ```
2. Formulate clean conventional commit:
   `feat(<feature>): implement <feature_description> with full state matrix and design tokens`
3. Draft PR description highlighting:
   - User stories completed.
   - Screen states covered (loading, error, loaded, empty, offline).
   - Design tokens consumed.
   - Blast radius verification (zero regressions).
