# Universal AI Toolkit v2

**Universal AI Toolkit v2** is a modular, codebase-agnostic, multi-IDE software engineering accelerator for AI coding agents.

It decouples agent execution logic from concrete codebase naming, enabling seamless operation across Single-App, Multi-Flavor, and Multi-Packaging projects regardless of state management (`BLoC`, `Riverpod`, `Provider`) or architecture (`Clean Architecture`, `Modular`, `Layer-First`).

---

## 🌟 Key Highlights

1. **Mandatory Project Profiling (`project_profile.yaml`):**
   - Locks project architectural decisions with an interactive wizard (`toolkit init`).
   - Supports PRD/BRD auto-inference, pre-packaged presets, and smart AI recommendations.
2. **Zero Codebase Assumptions:**
   - Adapts to any state management, network client, routing library, and folder layout.
3. **Strict Design System Enforcement:**
   - Zero tolerance for hardcoded color hexes, arbitrary font sizes, or ad-hoc padding literals.
   - Dual-mode ingestion for **Google Stitch** and **Figma** (via MCP Server or Local Folder/Files).
4. **Modern Dart 3+ Clean Presentation:**
   - Enforces **Sealed Classes** for exhaustive UI state pattern matching.
   - Enforces **Records** for lightweight transient tuples.
   - Enforces clear architectural rationales and transparent trade-offs.
5. **Collaborative Problem Solving & Impact Analysis:**
   - Socratic inquiry with Fast-Track skip for trivial tweaks.
   - Mandatory blast radius assessment before touching code.
   - Simplicity-First gate (Occam's razor).
6. **Screen States Matrix & Proactive Scenarios:**
   - Structured state suite (Loading, Error, Loaded, Empty, Refreshing).
   - Proactive edge cases (Offline-first caching, network retry, empty CTAs, session timeouts).
7. **Performance & Memory Management:**
   - Mandatory disposal of animation controllers, tickers, scroll controllers, and streams.
   - `RepaintBoundary` isolation and full mathematical transparency for `CustomPainter`.
8. **Lean Loading & Budget Protection:**
   - 60-line Agent Cards indexed by universal tags in `LOADMAP.md`.
   - Automatic plan splitting (`toolkit plan-split`) keeping plans < 8KB.
9. **Universal Adaptive Makefile:**
   - Self-adapts between Single App and Multi-Flavor / Multi-Packaging modes.
   - Configurable private Git remote.
10. **Multi-IDE Portability:**
    - One-click setup across Cursor, Claude Code, Antigravity, Windsurf, and VS Code.

---

## 🚀 Quickstart for Any Host Project (One-Liner)

To set up the entire toolkit in any project in **one single command**:

```bash
git submodule add <your-private-toolkit-repo-url> ai_toolkit && bash ai_toolkit/setup/quickstart.sh
```

### What this single command does automatically:
1. Registers the toolkit submodule.
2. Copies the **Universal Adaptive Makefile** to your project root.
3. Launches the **Interactive Profile Wizard** to lock project architecture and constraints.
4. Deploys **Cursor rules**, **skills**, **ignore files**, and **VS Code search exclusions**.
5. Runs an integrity check to verify everything is 100% green.

---

### Manual Setup (Alternative Step-by-Step)

### 3. Install IDE Rules & Exclusions
```bash
bash ai_toolkit/setup/install.sh
```

### 4. Copy Universal Makefile
```bash
cp ai_toolkit/templates/root/Makefile.universal Makefile
```

Now run `make help` to inspect your customized development targets!
