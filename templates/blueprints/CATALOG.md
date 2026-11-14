# On-Demand Blueprint Catalog

Universal, decoupled, production-grade Flutter building blocks.
Zero hardcoded design tokens. Standalone or adaptive to `project_profile.yaml`.

Install any blueprint directly using:
```bash
toolkit add <blueprint_name> [--name CustomName] [--out <path>]
```

---

## 🎨 UI Blueprints (`templates/blueprints/ui/`)

| Blueprint Name | Default Target Path | Description |
| :--- | :--- | :--- |
| `button` / `app_button` | `lib/common/widgets/app_button.dart` | Universal button supporting Primary, Secondary, Outlined, Danger, Text styles with loading spinner & icon slots. |
| `text_field` / `app_text_field` | `lib/common/widgets/app_text_field.dart` | Form input with prefix/suffix icons, obscure password toggle, error states, and clear button. |
| `image` / `app_image` | `lib/common/widgets/app_image.dart` | Network, asset, SVG, and file image renderer with automatic cache, error fallback, and skeleton shimmer. |
| `back_button` / `app_back_button` | `lib/common/widgets/app_back_button.dart` | Adaptive RTL/LTR back button with circular background or plain icon style. |
| `dropdown` / `app_dropdown` | `lib/common/widgets/app_dropdown.dart` | Searchable bottom-sheet dropdown selection supporting generic items `<T>`. |
| `phone_field` / `app_phone_field` | `lib/common/widgets/app_phone_field.dart` | Phone number input with country selector dialog, flag emoji, and phone format sanitization. |
| `currency_price` / `currency_price_text` | `lib/common/widgets/currency_price_text.dart` | Formatted price display with currency symbol, discount strike-through, and font size variants. |
| `fail_widget` / `app_fail_widget` | `lib/common/widgets/app_fail_widget.dart` | Clean error state widget with illustration/icon, error message, and retry button callback. |
| `empty_widget` / `app_empty_widget` | `lib/common/widgets/app_empty_widget.dart` | Empty state placeholder with customizable title, subtitle, icon, and call-to-action button. |
| `shimmer` / `shimmer_skeleton` | `lib/common/widgets/shimmer_skeleton.dart` | Standalone shimmer animation loader for cards, avatars, and text skeletons. Zero external packages. |
| `payment_webview` / `payment_webview_page` | `lib/features/payment/presentation/payment_webview_page.dart` | In-app payment gateway webview with success/failure redirect URL interceptors. |

---

## 🏗️ Pattern Blueprints (`templates/blueprints/patterns/`)

| Blueprint Name | Default Target Path | Description |
| :--- | :--- | :--- |
| `observer` / `observer_hub` | `lib/core/events/observer_hub.dart` | Lightweight decoupled event bus / observer hub for cross-feature notifications without tight coupling. |
| `pagination` / `paginated_list_view` | `lib/common/widgets/paginated_list_view.dart` | Infinite scroll list view with pull-to-refresh, bottom loader, empty state, and error retry. |
| `async_state` | `lib/core/state/async_state.dart` | Dart 3 Sealed Classes `AsyncState<T>` (`Initial`, `Loading`, `Success`, `Failure`) with exhaustive pattern matching. |
| `guest_guard` | `lib/common/guards/guest_guard.dart` | Action interceptor checking user authentication; prompts login bottom sheet for guests. |
| `use_case` | `lib/core/domain/use_case.dart` | Clean Architecture UseCase interface returning `Result<T>` sealed class or Dart 3 Records. |
| `stepped_wizard` | `lib/common/widgets/stepped_wizard_view.dart` | Multi-step flow controller with step indicator progress bar and navigation transitions. |
| `chaos_interceptor` / `qa_chaos_interceptor` | `lib/core/network/qa_chaos_interceptor.dart` | Debug-only Dio chaos interceptor for autonomous QA state verification (Loading, Empty, 500, Offline). |

---

## 🛠️ Utility Blueprints (`templates/blueprints/utils/`)

| Blueprint Name | Default Target Path | Description |
| :--- | :--- | :--- |
| `context_ext` / `context_extensions` | `lib/core/extensions/context_extensions.dart` | Concise extensions on `BuildContext` for theme, colorScheme, textTheme, screen size, keyboard hiding, and SnackBars. |
| `validator` / `form_validator` | `lib/core/utils/form_validator.dart` | Fluent chainable form validator (`required().email().minLength(8)`) and static convenience helpers. |

---

## 💡 How It Works

1. Run `toolkit add <name>` in any project.
2. The scaffolder locates the corresponding template from the toolkit.
3. If `project_profile.yaml` exists, it resolves your project's custom folders and imports.
4. The blueprint is copied to your destination with clean naming.
5. The blueprint is automatically registered in your `ai_docs/conventions.md` file.
