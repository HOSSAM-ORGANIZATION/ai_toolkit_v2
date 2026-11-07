# {{PROJECT_NAME}}

> Living Project Knowledge Base & Architecture Handbook.
> Automatically maintained by Universal AI Toolkit v2.
> Acts as the single onboarding reference for developers and AI agents.

---

## 1. Technical Stack Snapshot

| Layer | Selection | Reference |
| :--- | :--- | :--- |
| **Archetype** | `{{PROJECT_TYPE}}` | {{FLAVORS_COUNT}} active flavor(s) |
| **Architecture** | `{{ARCHITECTURE}}` | Feature-driven isolation |
| **State Management** | `{{STATE_MANAGEMENT}}` | Predictable reactive pipeline |
| **Networking** | `{{NETWORK_CLIENT}}` | Centralized interceptors & error mappers |
| **Dependency Injection** | `{{DEPENDENCY_INJECTION}}` | Automated service locator / container |
| **Routing** | `{{NAVIGATION}}` | URL-safe declarative navigation |
| **Localization** | `{{L10N_ENGINE}}` (`{{DEFAULT_LOCALE}}`) | `{{DIRECTIONALITY}}` |
| **Design System** | `{{DESIGN_SOURCE}}` | Strict token consumption enforced |

---

## 2. Developer Quickstart (Zero-to-Hero)

### Prerequisites
- Flutter SDK (see `pubspec.yaml` environment constraint)
- Make (recommended for CLI workflow)

### Essential Commands
```bash
# 1. Resolve dependencies
make get

# 2. Run code generation (build_runner)
make codegen

# 3. Launch application
make run                 # for single-app
make <flavor> run        # for multi-flavor (e.g. make dev run)

# 4. Run tests and static analysis
make test
make analyze
```

---

## 3. Features Catalog & Status

| Feature | Directory | Status | Spec / Plan | Feature README |
| :--- | :--- | :---: | :---: | :---: |
| *Authentication* | `lib/features/authentication` | ✅ Done | [Plan](ai_specs/features/authentication/plan.md) | [README](lib/features/authentication/README.md) |
| *Home & Dashboard* | `lib/features/home` | 🚧 In Progress | [Plan](ai_specs/features/home/plan.md) | [README](lib/features/home/README.md) |

---

## 4. Key Architectural Decisions (ADRs) & Gotchas

1. **Clean Presentation & Modern Dart 3+:**
   - Exhaustive pattern matching using **Sealed Classes** for all UI States.
   - **Records** for multiple return values without overhead models.
2. **Strict Design System Enforcement:**
   - Direct color literals (`Color(0xFF...)`) and magic numbers are strictly forbidden. Always import tokens from `{{TOKENS_PATH}}`.
3. **Memory Management:**
   - Always dispose controllers, animation tickers, and stream subscriptions inside `dispose()`.
