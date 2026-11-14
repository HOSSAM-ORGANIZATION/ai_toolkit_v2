# LOADMAP — Universal AI Toolkit v2

Resolve `+tag` / `-tag` / plan `Load:` to **leaf files**. 
Read each leaf’s **`## Agent card`** (lines 1–60). Do **not** browse indexes, read full files, or ingest unrequested modules during a feature phase.

---

## 1. Card Protocol & Token Budget Protection

1. **Tag-Driven Loading:** Open only the files mapped to the requested tags below.
2. **Limit 60 Lines:** Ingest only **lines 1–60** of each leaf file. The Agent Card contains the entire enforceable contract (`Must`, `Must not`, `When to load the rest`).
3. **Read Rest Exception:** Read past line 60 **only** if the card explicitly says `Read rest of this file: yes` or the `When to load the rest` condition triggers.
4. **No Tests Tag:** Do not load testing rules or write automated tests unless the feature plan explicitly specifies `+test` or `project_profile.yaml` sets `testing_gate: strict`.

---

## 2. Universal Tag Taxonomy

| Tag | Topic & Intent | Target Leaf Files (relative to toolkit root) |
| :--- | :--- | :--- |
| `ui` | Component composition, widgets, Modern Dart 3+ UI | `rules/flutter/design-system-enforcement.md`, `rules/dart/presentation-clean-code.md` |
| `design-system` | Zero-hardcoding mandate, tokens, wrappers | `rules/flutter/design-system-enforcement.md` |
| `clean-code` | SOLID, DRY, widget decomposition, reusability | `rules/dart/clean-code-and-patterns.md`, `rules/dart/presentation-clean-code.md` |
| `patterns` | Applied design patterns (Factory, Strategy, Builder, Adapter) | `rules/dart/clean-code-and-patterns.md` |
| `perf` | 60/120 FPS rendering, memory management, zero leaks | `rules/flutter/ui-performance-and-graphics.md` |
| `math` | Canvas, CustomPainter, trigonometric transparency | `rules/flutter/ui-performance-and-graphics.md` |
| `state` | State controller architecture, sealed classes, streams | `rules/dart/presentation-clean-code.md`, `workflows/feature-delivery/screen-states-protocol.md` |
| `data` | HTTP client calls, inline response parsing, zero prints | `rules/flutter/design-system-enforcement.md` |
| `domain` | Use cases, entities, business logic immutability | `rules/dart/clean-code-and-patterns.md` |
| `l10n` | Translation keys, directionality, ARB/JSON/Slang | `rules/flutter/design-system-enforcement.md` |
| `figma` | Figma design analysis, token extraction, RTL | `workflows/product-analysis/design-ingestion.md` |
| `stitch` | Google Stitch analysis (MCP & Local Folder) | `workflows/product-analysis/design-ingestion.md` |
| `qa` | Autonomous Maestro flows, screen state & overflow verification | `workflows/qa-verification/autonomous-qa-loop.md` |
| `codegen` | Build runner, code generation boundaries | `templates/root/Makefile.universal` |
| `flavors` | Multi-flavor & multi-packaging conventions | `templates/root/Makefile.universal` |
| `app-memory` | Project-specific living memory and gotchas | `ai_docs/memory.md` (in host application repo) |

---

## 3. Usage Examples

- **UI Feature:** `Load: [ui, design-system, l10n]` → Loads the 3 corresponding Agent Cards (~1.8 KB total context).
- **Custom Graphics:** `Load: [ui, perf, math]` → Loads UI composition + graphics math cards (~2.2 KB total context).
- **Domain & State Logic:** `Load: [domain, state, clean-code]` → Loads business logic + state patterns cards (~2.5 KB total context).

*Zero wasted tokens. Zero context pollution.*
