# AI Assistant Bootstrap (Universal AI Toolkit v2)

Follow this ordered entrypoint for all sessions in this codebase:

1. **Gatekeeper:** Check `project_profile.yaml`. If missing, halt and run `make toolkit-init`.
2. **Session Start:** Read `ai_toolkit/workflows/session/bootstrap-session.md`.
3. **Living Memory:** Ingest `ai_docs/memory.md` (gotchas) and `ai_docs/conventions.md` (shared widget mappings).
4. **Lean Loading:** Consult `ai_toolkit/LOADMAP.md` for requested tags (`Load: [ui, state, ...]`). Read **only lines 1–60** of matching leaf files.
5. **Clean Code & Design System:**
   - Zero hardcoding of colors, font sizes, or paddings.
   - Use Sealed Classes for UI states and Records for transient data.
   - Always verify the blast radius and document the rationale for code choices.
