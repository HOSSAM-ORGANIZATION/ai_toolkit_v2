# 🚀 Universal AI Toolkit v2

> **The Codebase-Agnostic, Multi-IDE Software Engineering & Execution Engine for AI Coding Agents and Flutter Developers.**

[![Flutter](https://img.shields.io/badge/Flutter-3.10%2B-02569B?logo=flutter)](https://flutter.dev)
[![Dart](https://img.shields.io/badge/Dart-3.0%2B-0175C2?logo=dart)](https://dart.dev)
[![Architecture](https://img.shields.io/badge/Architecture-Clean%20%7C%20Modular%20%7C%20Feature--First-blueviolet)](#-architecture--presets)
[![AI Agents](https://img.shields.io/badge/AI%20Agents-Cursor%20%7C%20Claude%20%7C%20Antigravity%20%7C%20Windsurf-success)](#-multi-ide--ai-agent-portability)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📖 Table of Contents
1. [Overview & Philosophy](#-overview--philosophy)
2. [Key Highlights & Core Pillars](#-key-highlights--core-pillars)
3. [Quickstart & Installation](#-quickstart--installation)
4. [Project Profiling & Presets](#-project-profiling--presets)
5. [Master CLI Reference (`toolkit`)](#-master-cli-reference-toolkit)
6. [On-Demand Blueprint Catalog](#-on-demand-blueprint-catalog)
7. [Universal Adaptive Makefile](#-universal-adaptive-makefile)
8. [Autonomous QA & Verification Engine](#-autonomous-qa--verification-engine)
9. [Feature Delivery Workflows & Protocols](#-feature-delivery-workflows--protocols)
10. [Strict Engineering Rules & Standards](#-strict-engineering-rules--standards)
11. [Living Memory & Token Budget Optimization](#-living-memory--token-budget-optimization)
12. [Multi-IDE & AI Agent Portability](#-multi-ide--ai-agent-portability)

---

## 🎯 Overview & Philosophy

**Universal AI Toolkit v2** decouples AI execution logic from specific codebase conventions. Traditional AI setups hardcode specific class names (`DioHelper`, `AppButton`), forced state management (`Cubit`), and inflexible folder paths. 

**v2 operates as an autonomous engineering layer:**
- **Zero Codebase Assumptions:** Adapts instantly to Single-App, Multi-Flavor, and Multi-Package setups across any state management (`BLoC`, `Riverpod`, `Provider`, `GetX`) and folder architecture (`Clean Architecture`, `Feature-First`, `Modular`).
- **Enforced Architectural Constitution (`project_profile.yaml`):** The AI agent is constrained by a locked project profile and cannot hallucinate patterns or introduce foreign libraries.
- **Strict Quality Gates:** Zero tolerance for hardcoded colors, arbitrary sizes, unhandled edge cases, or memory leaks.

---

## 🌟 Key Highlights & Core Pillars

| Pillar | Capability |
| :--- | :--- |
| **Architectural Gatekeeping** | Interactive wizard or PRD auto-inference generating `project_profile.yaml`. |
| **Strict Design System** | Ingests **Google Stitch** & **Figma** (via MCP or local files). Enforces 100% token usage (zero hex literals). |
| **Modern Dart 3+ Standards** | Enforces **Sealed Classes** for exhaustive UI states, **Records** for lightweight tuples, and clear trade-off documentation. |
| **Lean Token Loading** | 60-line Agent Cards indexed in `LOADMAP.md`. Saves up to 75% context tokens per prompt. |
| **Plan Splitting (< 8KB)** | Autonomously splits large plans (`toolkit plan-split`), archiving finished phases to `history.md`. |
| **Autonomous QA & Maestro** | Generates and executes Maestro UI flows, tests layout overflows, and validates screen state matrices. |
| **Automated Platform Ops** | One-command setup for Flutter flavors, Android keystores, iOS xcconfigs, app permissions, and Fastlane/Firebase provisioning. |

---

## 🚀 Quickstart & Installation

### Option 1: Git Submodule (Recommended for all projects)
Keeps the toolkit synchronized with its upstream repository so your project receives continuous updates without cluttering your main git history.

```bash
# In your host project root:
git submodule add https://github.com/HOSSAM-ORGANIZATION/ai_toolkit_v2.git ai_toolkit
bash ai_toolkit/setup/quickstart.sh
```

#### What `quickstart.sh` does in one pass:
1. Copies the **Universal Adaptive Makefile** and project wrapper (`./toolkit`) to your root.
2. Launches the **Interactive Profile Wizard** to lock your architecture.
3. Installs **Cursor rules**, **Claude/Antigravity system prompts** (`CLAUDE.md`, `AGENTS.md`), and **VS Code search exclusions**.
4. Runs a comprehensive integrity check (`verify-setup.sh`).

---

### Option 2: Global CLI Installation (For your development machine)
Install the `toolkit` binary globally on macOS/Linux:

```bash
curl -fsSL https://raw.githubusercontent.com/HOSSAM-ORGANIZATION/ai_toolkit_v2/main/setup/install-cli.sh | bash
```

Once installed globally, you can initialize any project simply with:
```bash
toolkit setup
```

---

### Option 3: Manual Step-by-Step Installation

```bash
# 1. Clone toolkit into your project
git submodule add https://github.com/HOSSAM-ORGANIZATION/ai_toolkit_v2.git ai_toolkit

# 2. Deploy IDE rules & exclusion filters
bash ai_toolkit/setup/install.sh

# 3. Copy universal Makefile and CLI wrapper
cp ai_toolkit/templates/root/Makefile.universal Makefile
cp ai_toolkit/templates/root/toolkit ./toolkit
chmod +x ./toolkit

# 4. Initialize your project profile
python3 ai_toolkit/bin/wizard/init_profile.py

# 5. Verify integrity
bash ai_toolkit/setup/verify-setup.sh
```

---

## ⚙️ Project Profiling & Presets

The toolkit requires `project_profile.yaml` in the project root. This acts as the constitutional gatekeeper for every AI agent.

```bash
# Interactive wizard:
toolkit init

# Auto-infer profile from PRD/BRD document:
toolkit init --prd docs/prd.md

# Initialize using a pre-packaged architectural preset:
toolkit init --preset enterprise_clean_bloc
```

### Pre-Packaged Architectural Presets (`presets/`)

| Preset Name | State Management | Architecture | Network | Design Tokens |
| :--- | :--- | :--- | :--- | :--- |
| `enterprise_clean_bloc` | Flutter BLoC | Clean Architecture (Domain/Data/Presentation) | Dio + Retrofit | ThemeExtension + AppColors |
| `modern_modular_riverpod` | Riverpod 2.x (Notifier) | Feature-First / Modular | Dio | ThemeData / ColorScheme |
| `lean_mvp` | Provider | Feature-First (UI/Data) | Dio (Interceptors) + GetIt | Global Static Tokens / Theme |
| `moltaqa` | BLoC / Cubit | Enterprise Multi-Package Monorepo | Dio + Custom Interceptors | Dedicated Design System Package |

---

## 🛠️ Master CLI Reference (`toolkit`)

The `toolkit` CLI is zero-dependency, running directly on Python 3 with pure standard libraries.

```
Usage: toolkit <command> [subcommand] [options]
```

### 1. Setup & Platform Operations

| Command | Description |
| :--- | :--- |
| `toolkit quickstart` | Runs the full interactive setup pipeline (Makefile + Profile + Rules + Verification). |
| `toolkit flavors [setup]` | Configures Android productFlavors (Kotlin DSL / Groovy), iOS xcconfigs & schemes, and dynamic entrypoints (`lib/main_<flavor>.dart`). |
| `toolkit permissions [MODULES]` | Injects permissions into `AndroidManifest.xml` and `Info.plist` with Apple review justification strings (e.g. `camera`, `location`, `storage`, `notifications`). |
| `toolkit signing` | Generates Android production Keystores (`upload-keystore.jks`), creates `key.properties`, and hooks signing configs into `build.gradle`. |
| `toolkit icons-splash` | Configures adaptive launcher icons and native splash screens for all defined flavors via `flutter_launcher_icons` and `flutter_native_splash`. |
| `toolkit cloud / register` | Automates Firebase project creation, Fastlane setup, Apple Developer App ID registration, and Google Play Console readiness. |
| `toolkit deps [sync]` | Reads `project_profile.yaml` and synchronizes required pub dependencies with `pubspec.yaml`. |
| `toolkit l10n [sync]` | Validates and synchronizes localization keys across ARB, JSON, and Slang files. |

### 2. Scaffolding & Code Generation

| Command | Description |
| :--- | :--- |
| `toolkit add <blueprint>` | Scaffolds a production-grade UI, Pattern, or Utility blueprint into your project. |
| `toolkit check [PATH]` | Validates `project_profile.yaml` against its JSON schema. |
| `toolkit plan-split [PATH]` | Splits completed phases in `plan.md` into `history.md` to keep context under 8KB. |
| `toolkit context <FEATURE>` | Computes token load budget for feature rules and cards. |
| `toolkit verify` | Validates all rules, templates, symlinks, and configuration files. |

### 3. Autonomous QA & Verification

| Command | Description |
| :--- | :--- |
| `toolkit qa gen <FEATURE>` | Generates Maestro flow (`test/qa_flows/<feature>_flow.yaml`) and QA report card template. |
| `toolkit qa run [FEATURE]` | Executes Maestro automated UI flows and analyzes layout overflows. |
| `toolkit qa status` | Prints recent QA run statuses and overflow diagnostics. |

### 4. Submodule Lifecycle Management

| Command | Description |
| :--- | :--- |
| `toolkit sync` | Checks out the pinned toolkit commit in the host repository. |
| `toolkit pull` | Pulls latest toolkit updates from GitHub and re-synchronizes IDE rules and templates. |
| `toolkit push "MSG"` | Commits and pushes changes made inside the toolkit repository. |
| `toolkit status` | Displays git status of the toolkit submodule. |

---

## 🎨 On-Demand Blueprint Catalog

Install any blueprint instantly using `toolkit add <name>`:

```bash
toolkit add button --name PrimaryAppButton
toolkit add pagination
toolkit add async_state
```

The scaffolder automatically resolves target paths and package imports based on your `project_profile.yaml` and registers newly added widgets in `ai_docs/conventions.md`.

### UI Components (`templates/blueprints/ui/`)

| Blueprint | Default Path | Description |
| :--- | :--- | :--- |
| `button` | `lib/common/widgets/app_button.dart` | Universal button supporting Primary, Secondary, Outlined, Danger, Text styles, icon slots & loading spinner. |
| `text_field` | `lib/common/widgets/app_text_field.dart` | Form input with prefix/suffix icons, obscure password toggle, and validation error presentation. |
| `image` | `lib/common/widgets/app_image.dart` | Network, asset, SVG, and file image renderer with auto-cache, fallback error, and skeleton shimmer. |
| `back_button` | `lib/common/widgets/app_back_button.dart` | Adaptive RTL/LTR back button with circular or minimalist style. |
| `dropdown` | `lib/common/widgets/app_dropdown.dart` | Searchable bottom-sheet generic item selector `<T>`. |
| `phone_field` | `lib/common/widgets/app_phone_field.dart` | Phone number input with country code dialog, flag emojis, and input sanitization. |
| `currency_price`| `lib/common/widgets/currency_price_text.dart` | Price display supporting currency symbols, discounts, and font size variants. |
| `fail_widget` | `lib/common/widgets/app_fail_widget.dart` | Error state widget with illustration, message, and retry button callback. |
| `empty_widget` | `lib/common/widgets/app_empty_widget.dart` | Empty state placeholder with title, subtitle, icon, and call-to-action button. |
| `shimmer` | `lib/common/widgets/shimmer_skeleton.dart` | Standalone shimmer animation loader for cards, avatars, and text skeletons. Zero external packages. |
| `payment_webview`| `lib/features/payment/presentation/payment_webview_page.dart` | Payment gateway webview intercepting success/failure callback URLs. |

### Architectural Patterns & Utilities (`templates/blueprints/patterns/` & `utils/`)

| Blueprint | Default Path | Description |
| :--- | :--- | :--- |
| `async_state` | `lib/core/state/async_state.dart` | Dart 3 Sealed Classes `AsyncState<T>` (`Initial`, `Loading`, `Success`, `Failure`) with exhaustive matching. |
| `pagination` | `lib/common/widgets/paginated_list_view.dart` | Infinite scroll list view with pull-to-refresh, bottom loader, empty state, and retry. |
| `observer` | `lib/core/events/observer_hub.dart` | Decoupled event bus / observer hub for cross-feature communication. |
| `guest_guard` | `lib/common/guards/guest_guard.dart` | Auth guard intercepting restricted actions and prompting login bottom sheets for guests. |
| `use_case` | `lib/core/domain/use_case.dart` | Clean Architecture UseCase interface returning `Result<T>` sealed class or Dart 3 Records. |
| `stepped_wizard`| `lib/common/widgets/stepped_wizard_view.dart` | Multi-step navigation controller with progress indicators and transition animations. |
| `chaos_interceptor`| `lib/core/network/qa_chaos_interceptor.dart` | Debug Dio interceptor simulating latency, offline mode, empty responses, and 500 errors for QA. |
| `context_ext` | `lib/core/extensions/context_extensions.dart` | Convenient `BuildContext` extensions for themes, colors, media queries, keyboard dismissal, and SnackBars. |
| `validator` | `lib/core/utils/form_validator.dart` | Fluent chainable form validator (`required().email().minLength(8)`). |

---

## ⚡ Universal Adaptive Makefile

The toolkit includes an adaptive Makefile that detects whether your project is **Single App** or **Multi-Flavor** based on `project_profile.yaml`.

```bash
# View all available targets customized for your project:
make help
```

### Core Commands

```bash
# Run & Build (Single-App mode):
make run                  # Run app on connected device
make apk                  # Build release APK
make aab                  # Build release App Bundle
make ipa                  # Build release iOS IPA

# Run & Build (Multi-Flavor mode):
make <flavor> run         # Example: make dev run, make prod run
make <flavor> apk         # Example: make staging apk
make <flavor> aab         # Example: make prod aab
make <flavor> ipa         # Example: make prod ipa

# Code Quality & Dependencies:
make get                  # flutter pub get
make codegen              # Run build_runner with conflicting-outputs delete
make clean                # flutter clean and cache cleanup
make analyze              # Run flutter analyze
make format               # dart format . --line-length 80
make test                 # Run test suite

# Automated QA & Maestro:
make qa                   # Run all Maestro QA flows
make qa-feature FEATURE=x # Run QA flow for a specific feature
make qa-gen FEATURE=x     # Generate Maestro flow for a feature
make qa-status            # Show recent QA run results

# Toolkit Lifecycle:
make toolkit-init         # Launch profile wizard
make toolkit-add NAME=btn # Scaffold blueprint
make toolkit-pull         # Pull latest toolkit updates & re-sync IDE rules
make toolkit-sync         # Sync pinned submodule commit
```

---

## 🧪 Autonomous QA & Verification Engine

Located in `bin/qa/qa_engine.py`, the QA Engine provides an autonomous self-healing loop for AI coding agents:

```
┌────────────────────────────────────────────────────────┐
│               Autonomous QA Loop                       │
├─────────────────┐                                      │
│ 1. Run Flow     │ ──> Maestro executes declarative YAML │
│ 2. Analyze      │ ──> Captures RenderFlex Overflows    │
│ 3. Chaos Test   │ ──> Simulates Offline, Empty, 500     │
│ 4. Report Card  │ ──> Generates Markdown report card   │
│ 5. Self-Healing │ ──> AI Agent reads card & fixes code  │
└─────────────────┘                                      │
```

- **Declarative Flows (`templates/qa/maestro_flow.template.yaml`):** Human-readable UI tests checking tap targets, assertions, scroll behaviors, and text assertions.
- **Chaos Interceptor (`qa_chaos_interceptor.dart`):** Verifies that UI behaves gracefully under failure conditions without crashing or getting stuck in loading loops.
- **Report Cards (`templates/qa/qa_report_card.template.md`):** Feeds structured QA results directly to the AI agent.

---

## 🔄 Feature Delivery Workflows & Protocols

All workflows reside in `workflows/` and govern how AI agents plan and implement code:

### 1. Design Ingestion (`workflows/product-analysis/design-ingestion.md`)
- Ingests designs from **Google Stitch** and **Figma** (via MCP Server or exported local folders).
- Extracts design tokens (colors, typography, radii, elevation, spacing) into theme definitions before coding widgets.

### 2. Screen States Protocol (`workflows/feature-delivery/screen-states-protocol.md`)
Every screen must satisfy the **5-State Matrix**:
1. **Loading State:** Shimmer skeleton (never generic full-screen spinners).
2. **Error State:** Human-readable message with clear retry action.
3. **Loaded / Success State:** Rendered content using design system components.
4. **Empty State:** Dedicated illustration/icon, contextual guidance, and a primary CTA.
5. **Refreshing State:** Subtle non-blocking pull-to-refresh.

### 3. Plan & Split (`workflows/feature-delivery/make-plan.md` & `bin/plan-splitter`)
- Features are designed in phases with strict token limits.
- When a phase finishes, `toolkit plan-split` automatically moves completed items to `history.md`, keeping `plan.md` under **8KB** to prevent context window saturation.

### 4. Backend Contract Collaboration (`workflows/api-analysis/backend-contract.md`)
- Detects API gaps and mismatches between frontend models and backend endpoints.
- Generates structured contract request/reply Markdown documents to align frontend and backend teams before implementation.

---

## 📐 Strict Engineering Rules & Standards

Located in `rules/`, these rules are automatically injected into your IDE:

### 1. Design System Enforcement (`rules/flutter/design-system-enforcement.md`)
- **Zero Hardcoding Policy:** Absolute zero tolerance for `Color(0xFF...)`, `fontSize: 16`, or ad-hoc `EdgeInsets.all(12)`.
- All styling must be derived from `Theme.of(context)`, `ColorScheme`, or designated design tokens in `project_profile.yaml`.

### 2. Clean Code & Patterns (`rules/dart/clean-code-and-patterns.md`)
- Single Responsibility Principle (SRP) per widget. Maximum widget depth: 3 levels before decomposition.
- Application of design patterns where appropriate (Strategy for validators, Factory for state builders, Adapter for external APIs).

### 3. Modern Dart 3+ Standards (`rules/dart/presentation-clean-code.md`)
- **Sealed Classes:** Used for presentation states to enforce exhaustive pattern matching via `switch` expressions.
- **Records:** Used for temporary multi-value returns without creating boilerplate data classes.
- **Class Modifiers:** Appropriate use of `interface`, `base`, and `final` classes.

### 4. High-Performance UI & Graphics (`rules/flutter/ui-performance-and-graphics.md`)
- **Zero-Leak Lifecycle:** Mandatory disposal of `AnimationController`, `ScrollController`, `TextEditingController`, and Stream subscriptions in `dispose()`.
- **Render Isolation:** Use `RepaintBoundary` for animations and complex widgets to isolate repaints.
- **Mathematical Transparency:** All `CustomPainter` calculations must have commented geometric equations.

---

## 🧠 Living Memory & Token Budget Optimization

### 1. Living Project Memory (`ai_docs/`)
- `ai_docs/memory.md` : Records project gotchas, library bugs, and specific architectural decisions. The AI checks this before every session to avoid repeating past mistakes.
- `ai_docs/conventions.md` : Automatically registers shared widgets and utilities created in the project so the AI reuses them instead of creating duplicates.

### 2. Lean Token Budgeting (`LOADMAP.md`)
- Rather than dumping hundreds of rule lines into the AI's context window, rules are divided into **60-line Agent Cards**.
- The AI only reads cards associated with active tags (e.g., `+ui`, `+perf`, `+state`), saving up to **75% of context window usage**.

---

## 💻 Multi-IDE & AI Agent Portability

Universal AI Toolkit v2 works out-of-the-box across all leading AI development environments:

| Environment | Supported Configuration Files |
| :--- | :--- |
| **Cursor** | `.cursor/rules/*.mdc`, `.cursorignore`, `.cursorindexingignore` |
| **Claude Code** | `CLAUDE.md`, `ai_docs/memory.md` |
| **Google Antigravity** | `AGENTS.md`, `CLAUDE.md`, Built-in Skills |
| **Windsurf** | `.windsurfrules`, `.cursor/rules/` |
| **VS Code** | `.vscode/settings.json` (Search exclusions to hide heavy generated files) |

---

## 🤝 Contributing

Contributions are welcome! Please ensure:
1. All scripts run on Python 3 Standard Library (zero pip dependencies).
2. Rule files include 60-line Agent Cards conforming to `LOADMAP.md`.
3. Run `toolkit verify` before submitting a Pull Request.

---

## 📄 License

Universal AI Toolkit v2 is licensed under the [MIT License](LICENSE).
