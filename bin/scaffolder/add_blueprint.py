#!/usr/bin/env python3
"""
Universal Blueprint Scaffolder
Installs ready-to-use, decoupled Flutter/Dart building blocks into host projects.
Uses Python Standard Library only (zero pip dependencies).
"""

import sys
import os
import argparse
from pathlib import Path

# Registry mapping alias -> (template_rel_path, default_target_path, description)
BLUEPRINT_REGISTRY = {
    "button": (
        "templates/blueprints/ui/app_button.dart.template",
        "lib/common/widgets/app_button.dart",
        "Universal customizable button with loading spinner & icon slots",
    ),
    "app_button": (
        "templates/blueprints/ui/app_button.dart.template",
        "lib/common/widgets/app_button.dart",
        "Universal customizable button with loading spinner & icon slots",
    ),
    "text_field": (
        "templates/blueprints/ui/app_text_field.dart.template",
        "lib/common/widgets/app_text_field.dart",
        "Universal form text field with obscure toggle and error handling",
    ),
    "app_text_field": (
        "templates/blueprints/ui/app_text_field.dart.template",
        "lib/common/widgets/app_text_field.dart",
        "Universal form text field with obscure toggle and error handling",
    ),
    "input": (
        "templates/blueprints/ui/app_text_field.dart.template",
        "lib/common/widgets/app_text_field.dart",
        "Universal form text field with obscure toggle and error handling",
    ),
    "image": (
        "templates/blueprints/ui/app_image.dart.template",
        "lib/common/widgets/app_image.dart",
        "Multi-source image renderer (network/asset/svg/file) with error fallbacks",
    ),
    "app_image": (
        "templates/blueprints/ui/app_image.dart.template",
        "lib/common/widgets/app_image.dart",
        "Multi-source image renderer (network/asset/svg/file) with error fallbacks",
    ),
    "back_button": (
        "templates/blueprints/ui/app_back_button.dart.template",
        "lib/common/widgets/app_back_button.dart",
        "Adaptive RTL/LTR back navigation button",
    ),
    "app_back_button": (
        "templates/blueprints/ui/app_back_button.dart.template",
        "lib/common/widgets/app_back_button.dart",
        "Adaptive RTL/LTR back navigation button",
    ),
    "dropdown": (
        "templates/blueprints/ui/app_dropdown.dart.template",
        "lib/common/widgets/app_dropdown.dart",
        "Searchable bottom-sheet dropdown selection widget",
    ),
    "app_dropdown": (
        "templates/blueprints/ui/app_dropdown.dart.template",
        "lib/common/widgets/app_dropdown.dart",
        "Searchable bottom-sheet dropdown selection widget",
    ),
    "phone_field": (
        "templates/blueprints/ui/app_phone_field.dart.template",
        "lib/common/widgets/app_phone_field.dart",
        "Phone number field with country code selection and validation",
    ),
    "app_phone_field": (
        "templates/blueprints/ui/app_phone_field.dart.template",
        "lib/common/widgets/app_phone_field.dart",
        "Phone number field with country code selection and validation",
    ),
    "phone": (
        "templates/blueprints/ui/app_phone_field.dart.template",
        "lib/common/widgets/app_phone_field.dart",
        "Phone number field with country code selection and validation",
    ),
    "currency_price": (
        "templates/blueprints/ui/currency_price_text.dart.template",
        "lib/common/widgets/currency_price_text.dart",
        "Price text widget with discount strike-through and currency format",
    ),
    "currency_price_text": (
        "templates/blueprints/ui/currency_price_text.dart.template",
        "lib/common/widgets/currency_price_text.dart",
        "Price text widget with discount strike-through and currency format",
    ),
    "price": (
        "templates/blueprints/ui/currency_price_text.dart.template",
        "lib/common/widgets/currency_price_text.dart",
        "Price text widget with discount strike-through and currency format",
    ),
    "fail_widget": (
        "templates/blueprints/ui/app_fail_widget.dart.template",
        "lib/common/widgets/app_fail_widget.dart",
        "Failure / error presentation widget with retry action",
    ),
    "app_fail_widget": (
        "templates/blueprints/ui/app_fail_widget.dart.template",
        "lib/common/widgets/app_fail_widget.dart",
        "Failure / error presentation widget with retry action",
    ),
    "error_widget": (
        "templates/blueprints/ui/app_fail_widget.dart.template",
        "lib/common/widgets/app_fail_widget.dart",
        "Failure / error presentation widget with retry action",
    ),
    "empty_widget": (
        "templates/blueprints/ui/app_empty_widget.dart.template",
        "lib/common/widgets/app_empty_widget.dart",
        "Empty state placeholder with title, icon, and optional action button",
    ),
    "app_empty_widget": (
        "templates/blueprints/ui/app_empty_widget.dart.template",
        "lib/common/widgets/app_empty_widget.dart",
        "Empty state placeholder with title, icon, and optional action button",
    ),
    "shimmer": (
        "templates/blueprints/ui/shimmer_skeleton.dart.template",
        "lib/common/widgets/shimmer_skeleton.dart",
        "Standalone shimmer skeleton animation loader (zero external packages)",
    ),
    "shimmer_skeleton": (
        "templates/blueprints/ui/shimmer_skeleton.dart.template",
        "lib/common/widgets/shimmer_skeleton.dart",
        "Standalone shimmer skeleton animation loader (zero external packages)",
    ),
    "skeleton": (
        "templates/blueprints/ui/shimmer_skeleton.dart.template",
        "lib/common/widgets/shimmer_skeleton.dart",
        "Standalone shimmer skeleton animation loader (zero external packages)",
    ),
    "payment_webview": (
        "templates/blueprints/ui/payment_webview_page.dart.template",
        "lib/features/payment/presentation/payment_webview_page.dart",
        "In-app payment gateway webview with URL interceptors",
    ),
    "payment": (
        "templates/blueprints/ui/payment_webview_page.dart.template",
        "lib/features/payment/presentation/payment_webview_page.dart",
        "In-app payment gateway webview with URL interceptors",
    ),
    "observer": (
        "templates/blueprints/patterns/observer_hub.dart.template",
        "lib/core/events/observer_hub.dart",
        "Decoupled event bus / observer hub for cross-feature notifications",
    ),
    "observer_hub": (
        "templates/blueprints/patterns/observer_hub.dart.template",
        "lib/core/events/observer_hub.dart",
        "Decoupled event bus / observer hub for cross-feature notifications",
    ),
    "event_bus": (
        "templates/blueprints/patterns/observer_hub.dart.template",
        "lib/core/events/observer_hub.dart",
        "Decoupled event bus / observer hub for cross-feature notifications",
    ),
    "pagination": (
        "templates/blueprints/patterns/paginated_list_view.dart.template",
        "lib/common/widgets/paginated_list_view.dart",
        "Infinite scroll list view with pull-to-refresh, bottom loader, and retry",
    ),
    "paginated_list_view": (
        "templates/blueprints/patterns/paginated_list_view.dart.template",
        "lib/common/widgets/paginated_list_view.dart",
        "Infinite scroll list view with pull-to-refresh, bottom loader, and retry",
    ),
    "async_state": (
        "templates/blueprints/patterns/async_state.dart.template",
        "lib/core/state/async_state.dart",
        "Dart 3 Sealed Classes AsyncState<T> with exhaustive pattern matching",
    ),
    "state": (
        "templates/blueprints/patterns/async_state.dart.template",
        "lib/core/state/async_state.dart",
        "Dart 3 Sealed Classes AsyncState<T> with exhaustive pattern matching",
    ),
    "guest_guard": (
        "templates/blueprints/patterns/guest_guard.dart.template",
        "lib/common/guards/guest_guard.dart",
        "Action interceptor checking auth status and showing login bottom sheet",
    ),
    "guard": (
        "templates/blueprints/patterns/guest_guard.dart.template",
        "lib/common/guards/guest_guard.dart",
        "Action interceptor checking auth status and showing login bottom sheet",
    ),
    "use_case": (
        "templates/blueprints/patterns/use_case.dart.template",
        "lib/core/domain/use_case.dart",
        "Clean Architecture UseCase contract with sealed Result<T>",
    ),
    "usecase": (
        "templates/blueprints/patterns/use_case.dart.template",
        "lib/core/domain/use_case.dart",
        "Clean Architecture UseCase contract with sealed Result<T>",
    ),
    "stepped_wizard": (
        "templates/blueprints/patterns/stepped_wizard.dart.template",
        "lib/common/widgets/stepped_wizard_view.dart",
        "Multi-step flow manager with step progress indicator and validation",
    ),
    "stepper": (
        "templates/blueprints/patterns/stepped_wizard.dart.template",
        "lib/common/widgets/stepped_wizard_view.dart",
        "Multi-step flow manager with step progress indicator and validation",
    ),
    "wizard": (
        "templates/blueprints/patterns/stepped_wizard.dart.template",
        "lib/common/widgets/stepped_wizard_view.dart",
        "Multi-step flow manager with step progress indicator and validation",
    ),
    "chaos_interceptor": (
        "templates/blueprints/patterns/qa_chaos_interceptor.dart.template",
        "lib/core/network/qa_chaos_interceptor.dart",
        "Debug-only Dio chaos interceptor for QA state testing (Loading, Empty, 500, Offline)",
    ),
    "qa_chaos_interceptor": (
        "templates/blueprints/patterns/qa_chaos_interceptor.dart.template",
        "lib/core/network/qa_chaos_interceptor.dart",
        "Debug-only Dio chaos interceptor for QA state testing (Loading, Empty, 500, Offline)",
    ),
    "context_ext": (
        "templates/blueprints/utils/context_extensions.dart.template",
        "lib/core/extensions/context_extensions.dart",
        "Concise BuildContext extensions for theme, size, navigation, SnackBars",
    ),
    "context_extensions": (
        "templates/blueprints/utils/context_extensions.dart.template",
        "lib/core/extensions/context_extensions.dart",
        "Concise BuildContext extensions for theme, size, navigation, SnackBars",
    ),
    "validator": (
        "templates/blueprints/utils/form_validator.dart.template",
        "lib/core/utils/form_validator.dart",
        "Fluent chainable form validator and static validation helpers",
    ),
    "form_validator": (
        "templates/blueprints/utils/form_validator.dart.template",
        "lib/core/utils/form_validator.dart",
        "Fluent chainable form validator and static validation helpers",
    ),
}

def resolve_toolkit_root() -> Path:
    """Finds the root directory of ai_toolkit_v2."""
    script_dir = Path(__file__).resolve().parent
    # script is in bin/scaffolder/, root is two levels up
    toolkit_root = script_dir.parent.parent
    if (toolkit_root / "templates" / "blueprints").is_dir():
        return toolkit_root
    
    # Check if run as submodule inside a project (.ai_toolkit/)
    cwd = Path.cwd()
    if (cwd / ".ai_toolkit" / "templates" / "blueprints").is_dir():
        return cwd / ".ai_toolkit"
        
    return toolkit_root

def list_blueprints():
    print("\n📦 AI Toolkit Universal Blueprints Catalog:")
    print("------------------------------------------------------------")
    # Get unique blueprints
    seen_paths = set()
    for name, (tmpl, def_target, desc) in sorted(BLUEPRINT_REGISTRY.items()):
        if tmpl in seen_paths:
            continue
        seen_paths.add(tmpl)
        category = tmpl.split("/")[2].upper()
        print(f"[{category}] {name.ljust(20)} -> {def_target}")
        print(f"    {desc}\n")
    print("Usage: toolkit add <name> [--name CustomName] [--out path] [--force]")

def register_in_conventions(project_root: Path, blueprint_name: str, target_rel_path: str, desc: str):
    """Appends registered blueprint to ai_docs/conventions.md if it exists."""
    conventions_file = project_root / "ai_docs" / "conventions.md"
    if not conventions_file.is_file():
        return

    try:
        content = conventions_file.read_text(encoding="utf-8")
        header = "## Installed On-Demand Blueprints"
        entry = f"- **`{blueprint_name}`** (`{target_rel_path}`): {desc}"

        if header not in content:
            content += f"\n\n{header}\n{entry}\n"
        else:
            if target_rel_path not in content:
                content = content.replace(header, f"{header}\n{entry}")

        conventions_file.write_text(content, encoding="utf-8")
        print(f"📝 Registered '{blueprint_name}' in {conventions_file}")
    except Exception as e:
        print(f"⚠️ Notice: Could not update conventions.md ({e})")

def main():
    parser = argparse.ArgumentParser(description="Scaffold On-Demand Flutter Blueprints into project.")
    parser.add_argument("blueprint", nargs="?", help="Name of blueprint to install (e.g. button, text_field, pagination)")
    parser.add_argument("--list", "-l", action="store_true", help="List all available blueprints")
    parser.add_argument("--name", help="Custom class or file name")
    parser.add_argument("--out", "-o", help="Custom output relative or absolute file path")
    parser.add_argument("--force", "-f", action="store_true", help="Overwrite target file if it already exists")
    parser.add_argument("--project-root", default=".", help="Target project root directory (defaults to current dir)")

    args = parser.parse_args()

    if args.list or not args.blueprint:
        list_blueprints()
        sys.exit(0)

    blueprint_key = args.blueprint.strip().lower()
    if blueprint_key not in BLUEPRINT_REGISTRY:
        print(f"❌ Error: Unknown blueprint '{args.blueprint}'.")
        print("Run 'toolkit add --list' to view available blueprints.")
        sys.exit(1)

    template_rel, default_target_rel, desc = BLUEPRINT_REGISTRY[blueprint_key]

    toolkit_root = resolve_toolkit_root()
    template_file = toolkit_root / template_rel

    if not template_file.is_file():
        print(f"❌ Error: Template file '{template_file}' not found.")
        sys.exit(1)

    project_root = Path(args.project_root).resolve()
    
    # Determine target path
    if args.out:
        target_path = project_root / args.out
    else:
        target_path = project_root / default_target_rel

    if target_path.is_file() and not args.force:
        print(f"⚠️ Target file already exists: {target_path}")
        print("Use --force / -f to overwrite, or specify a custom destination with --out <path>.")
        sys.exit(1)

    # Read template content
    content = template_file.read_text(encoding="utf-8")

    # If custom name specified, replace class names if applicable
    if args.name:
        default_class = Path(default_target_rel).stem
        # Convert snake_case to PascalCase
        custom_class = "".join(part.capitalize() for part in args.name.split("_"))
        default_pascal = "".join(part.capitalize() for part in default_class.split("_"))
        content = content.replace(default_pascal, custom_class)

    # Create destination parent directory
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(content, encoding="utf-8")

    rel_to_proj = target_path.relative_to(project_root) if target_path.is_relative_to(project_root) else target_path
    print(f"✅ Successfully installed '{blueprint_key}' -> {rel_to_proj}")

    # Register in ai_docs/conventions.md
    register_in_conventions(project_root, blueprint_key, str(rel_to_proj), desc)

if __name__ == "__main__":
    main()
