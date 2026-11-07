## Agent card

**LOADMAP tags:** `patterns`, `clean-code`
**Read rest of this file:** no — this card contains the full enforceable rule.

### Must
- Adhere strictly to Single Responsibility (SRP): a widget or class must have exactly one reason to change.
- Decompose complex screen files (> 200 lines) into focused, private or reusable domain sub-widgets.
- Prefer composition over inheritance in UI construction.
- Apply standard design patterns naturally where they solve concrete structural problems:
  - **Factory Constructors:** for JSON deserialization, DTO mapping, and polymorphic creation.
  - **Strategy Pattern:** for swappable algorithms (e.g. payment processors, validation strategies).
  - **Builder Pattern:** for complex dialogs, multi-step wizards, or dynamic form composition.
  - **Adapter Pattern:** for converting external third-party SDK models into internal domain entities.
- Keep all domain business entities and value objects immutable (`@immutable`, `final` fields).

### Must not
- Create god-widgets containing layout, data fetching, business logic, and error handling in one file.
- Copy-paste or write near-duplicate widgets; extract to reusable components.
- Over-engineer: do not introduce abstract patterns where a simple pure function suffices.
- Leak presentation observers into the domain or data layers.

### When to load the rest
- Only when designing complex polymorphic domain abstractions or refactoring large legacy classes.

### Related (cards first)
- `+domain` for entity rules; `+ui` for widget decomposition; `+state` for controller separation.

# Clean Code, Reusability & Applied Design Patterns

## Purpose
Establishes non-negotiable software craftsmanship standards across all Dart & Flutter layers, guaranteeing that code remains modular, reusable, testable, and comprehensible for both human engineers and AI agents.

## Core Principles

### 1. Single Responsibility Principle (SRP)
- A Page widget is responsible solely for layout structure and routing assembly.
- A Presentation Controller / Cubit / Notifier is responsible solely for UI state flow.
- A Use Case is responsible for orchestrating one specific business interaction.
- A Data Source is responsible for the raw I/O transport (HTTP, local DB).

### 2. Applied Design Patterns Matrix

| Pattern | Preferred Use Case in Flutter / Dart | Practical Example |
| :--- | :--- | :--- |
| **Factory** | JSON parsing, polymorphic DTO creation | `factory UserEntity.fromJson(Map<String, dynamic> json)` |
| **Strategy** | Swappable behaviors without modifying the caller | `PaymentStrategy` with `MadaStrategy`, `ApplePayStrategy` |
| **Adapter** | Isolating external SDK models from internal core | `GooglePlaceAdapter` converting Google Maps model to `AddressEntity` |
| **Builder** | Step-by-step assembly of complex structures | Dynamic form generators, multi-step wizard builders |
| **Observer** | Decoupled presentation state fan-out | Presentation-only broadcast hubs updating UI on cross-screen events |

### 3. Widget Reusability & Granularity
- Extract any child subtree with distinct styling or repeat usage into its own dedicated widget.
- Use `const` constructors aggressively on all immutable widgets to avoid unnecessary framework rebuild passes.
