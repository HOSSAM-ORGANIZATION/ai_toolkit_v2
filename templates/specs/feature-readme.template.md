# Feature: {{FEATURE_NAME}}

> Portable Feature Documentation & Integration Guide.
> Designed for instant reuse in other codebases with zero token waste.

---

## 1. Overview & Purpose
- **What this feature does:** {{FEATURE_PURPOSE}}
- **Target Flavors:** {{TARGET_FLAVORS}}
- **Domain Scope:** {{DOMAIN_SCOPE}}

---

## 2. Architecture Map & File Structure

```text
{{FEATURE_ROOT_PATH}}/
├── data/
│   ├── api/                   # Endpoint paths & contracts
│   ├── datasources/           # Remote & Local datasources
│   ├── models/                # DTOs & JSON serialization
│   └── repositories/          # Repository implementations
├── domain/
│   ├── entities/              # Business entities
│   ├── repositories/          # Repository contracts
│   └── use_cases/             # Executable use cases
└── presentation/
    ├── controllers/           # BLoC / Riverpod / Cubit
    ├── pages/                 # Full screen widgets
    └── widgets/               # Feature-specific reusable UI components
```

---

## 3. External Dependencies & Requirements
- **Required Packages (from pubspec.yaml):**
{{PACKAGES_LIST}}
- **Shared Core Dependencies:**
  - Network client (`DioHelper` or equivalent)
  - DI container (`GetIt` or Riverpod)
  - Design system tokens (Colors, Typography, Dimensions)

---

## 4. Screen States Matrix

| Screen / Flow | Loading | Error | Empty | Success / Loaded | Overlays (Dialog / Sheet / Toast) |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `{{MAIN_SCREEN_NAME}}` | [x] | [x] | [x] | [x] | Bottom sheet for filters, Toast on action |

---

## 5. Plug & Play Export Guide (Reusing in Another Project)

To export and use this feature in another Flutter application:

1. **Copy Feature Directory:**
   ```bash
   cp -r lib/features/{{FEATURE_SLUG}} <target_project>/lib/features/
   ```
2. **Register Dependencies in DI:**
   - Add feature data source and repository to `di.dart` or trigger code generation:
     ```bash
     make codegen
     ```
3. **Register Navigation Route:**
   - Add route definition to the target `AppRouter`:
     ```dart
     GoRoute(
       path: '/{{FEATURE_SLUG}}',
       builder: (context, state) => const {{FEATURE_MAIN_PAGE}}(),
     ),
     ```
4. **Localization Keys:**
   - Ensure the required keys from `{{FEATURE_SLUG}}` are present in target ARB/JSON files.
