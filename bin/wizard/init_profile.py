#!/usr/bin/env python3
"""
Universal AI Toolkit v2 — Interactive Project Profile Wizard
Generates and validates `project_profile.yaml` for any codebase.
Supports PRD/BRD auto-inference, pre-packaged presets, smart AI recommendations,
and trade-off explanations.
"""

import sys
import os
import re
import json
import argparse
from pathlib import Path

PRESETS = {
    "1": ("enterprise_clean_bloc", "Enterprise Clean Arch + BLoC + Dio + GetIt + ARB (RTL/LTR)"),
    "2": ("modern_modular_riverpod", "Modern Modular + Riverpod + Retrofit + GoRouter + Slang"),
    "3": ("lean_mvp", "Lean MVP + Provider/Signals + Http + Easy Localization"),
    "4": ("moltaqa", "Moltaqa Enterprise (Single/Multi-Flavor) + BLoC + Dio + Injectable + ARB RTL")
}

def detect_flavors_from_dir(target_dir):
    """Auto-detects active flavors from project structure (main_*.dart, apps/_*_app.dart, launcher icons)."""
    flavors = []
    target_path = Path(target_dir)
    # 1. flutter_launcher_icons-*.yaml
    for f in target_path.glob("flutter_launcher_icons-*.yaml"):
        m = re.search(r"flutter_launcher_icons-([a-zA-Z0-9_\-]+)\.yaml", f.name)
        if m:
            flavors.append(m.group(1))
    # 2. main_*.dart
    lib_dir = target_path / "lib"
    if lib_dir.exists():
        for f in lib_dir.glob("main_*.dart"):
            m = re.search(r"main_([a-zA-Z0-9_\-]+)\.dart", f.name)
            if m:
                flavors.append(m.group(1))
        # 3. lib/apps/_*_app.dart
        apps_dir = lib_dir / "apps"
        if apps_dir.exists():
            for f in apps_dir.glob("_*_app.dart"):
                m = re.search(r"_([a-zA-Z0-9_\-]+)_app\.dart", f.name)
                if m:
                    flavors.append(m.group(1))
    
    unique_flavors = []
    for fl in flavors:
        if fl not in unique_flavors:
            unique_flavors.append(fl)
    return unique_flavors

def apply_topology_to_preset(preset_content, project_type, flavors_list, project_name=None):
    """Injects dynamic project_type and flavors into a preset YAML string."""
    content = preset_content
    # Replace project_type
    content = re.sub(r'project_type\s*:\s*["\']?[a-zA-Z0-9_\-]+["\']?', f'project_type: "{project_type}"', content)
    # Replace project_name if provided
    if project_name:
        content = re.sub(r'project_name\s*:\s*["\']?[a-zA-Z0-9_\-]+["\']?', f'project_name: "{project_name}"', content)
    # Replace flavors
    if project_type == "multi_flavor" and flavors_list:
        flavors_yaml = "flavors:\n" + "\n".join([f'  - "{fl}"' for fl in flavors_list])
    else:
        flavors_yaml = "flavors: []"
    content = re.sub(r'flavors\s*:\s*(\[\]|(?:\n(?:\s*-\s*[^\n]+)+))', flavors_yaml, content)
    return content

def resolve_topology_interactive(target_dir, args_single=False, args_flavors=None, prompt_if_interactive=True):
    """Resolves whether the project is single_app or multi_flavor with specific flavors."""
    if args_single:
        return "single_app", []
    if args_flavors:
        fls = [f.strip() for f in args_flavors.split(",") if f.strip()]
        return "multi_flavor", fls

    detected = detect_flavors_from_dir(target_dir)

    # Non-interactive or suppressed prompt
    if not prompt_if_interactive or not sys.stdin.isatty():
        if detected:
            return "multi_flavor", detected
        return "single_app", []

    print("\n" + "🏢"*35)
    print("  PROJECT TOPOLOGY & FLAVORS CONFIGURATION")
    print("🏢"*35)
    print("  [1] Single App (تطبيق واحد)")
    print("  [2] 2 Apps / Flavors (e.g. User & Provider)")
    print("  [3] 3 Apps / Flavors (e.g. User, Provider & Delivery)")
    if detected:
        print(f"  [4] Auto-detected from files: {', '.join(detected)}")
        print("  [5] Custom Flavors (حدد الفليفرز يدوياً)")
    else:
        print("  [4] Custom Flavors (حدد الفليفرز يدوياً)")

    choice = input("👉 Select topology [1-4, default: 1]: ").strip()
    if choice == "2":
        f_in = input("👉 Enter 2 flavor names [default: user,provider]: ").strip()
        fls = [f.strip() for f in f_in.split(",")] if f_in else ["user", "provider"]
        return "multi_flavor", fls
    elif choice == "3":
        f_in = input("👉 Enter 3 flavor names [default: user,provider,delivery]: ").strip()
        fls = [f.strip() for f in f_in.split(",")] if f_in else ["user", "provider", "delivery"]
        return "multi_flavor", fls
    elif choice == "4" and detected:
        return "multi_flavor", detected
    elif (choice == "4" and not detected) or choice == "5":
        f_in = input("👉 Enter flavor names separated by comma: ").strip()
        fls = [f.strip() for f in f_in.split(",") if f.strip()]
        if fls:
            return "multi_flavor", fls
        return "single_app", []
    else:
        return "single_app", []

def resolve_capabilities_interactive(args, prompt_if_interactive=False):
    """Resolves optional capabilities based on CLI flags or interactive questionnaire."""
    caps = {
        "release_signing": bool(args.with_signing or args.all_capabilities),
        "icons_and_splash": bool(args.with_icons_splash or args.all_capabilities),
        "network_interceptors": bool(args.with_network or args.all_capabilities),
        "permissions": {
            "media": False,
            "location": False,
            "notifications": False,
        },
        "store_updater": bool(args.with_updater or args.all_capabilities)
    }

    if args.with_permissions:
        perms = [p.strip().lower() for p in args.with_permissions.split(",")]
        caps["permissions"]["media"] = "media" in perms or "all" in perms
        caps["permissions"]["location"] = "location" in perms or "all" in perms
        caps["permissions"]["notifications"] = "notifications" in perms or "all" in perms
    elif args.all_capabilities:
        caps["permissions"]["media"] = True
        caps["permissions"]["location"] = True
        caps["permissions"]["notifications"] = True

    if not prompt_if_interactive or not sys.stdin.isatty():
        return caps

    print("\n" + "🧩"*35)
    print("  OPTIONAL CAPABILITIES & MODULES")
    print("🧩"*35)
    print("  [1] Release Signing Setup (key.properties + Gradle release signing)")
    print("  [2] Multi-Flavor Icons & Native Splash (YAMLs + Assets directories)")
    print("  [3] Core Network Interceptors (ApiHeaders + 401 Auto-Logout + Failures)")
    print("  [4] Mobile Permissions & iOS Podfile (Media, Location, Notifications)")
    print("  [5] Force Update Engine (StoreUpdater - Version check against server)")

    ans = input("👉 Select capabilities [e.g. 1,2,3 or Enter for none]: ").strip()
    if ans:
        selected = [s.strip() for s in ans.replace(" ", ",").split(",") if s.strip()]
        if "1" in selected: caps["release_signing"] = True
        if "2" in selected: caps["icons_and_splash"] = True
        if "3" in selected: caps["network_interceptors"] = True
        if "5" in selected: caps["store_updater"] = True
        if "4" in selected:
            print("\n  📱 Which permissions does this app need?")
            print("    [1] Camera & Audio / Chat & QR (الكاميرا والمايك للشات، الملاحظات الصوتية، ومسح الـ QR)")
            print("    [2] Location (الموقع الجغرافي والخرائط)")
            print("    [3] Notifications (الإشعارات والتنبيهات)")
            p_ans = input("  👉 Select [e.g. 1,3 or Enter for none]: ").strip()
            if p_ans:
                p_sel = [s.strip() for s in p_ans.replace(" ", ",").split(",") if s.strip()]
                if "1" in p_sel: caps["permissions"]["media"] = True
                if "2" in p_sel: caps["permissions"]["location"] = True
                if "3" in p_sel: caps["permissions"]["notifications"] = True

    return caps

def format_capabilities_yaml(caps):
    """Formats capabilities dictionary into a clean YAML block."""
    p = caps.get("permissions", {})
    return f"""
# Optional Capabilities & Baseline Infrastructure
capabilities:
  release_signing: {str(caps.get('release_signing', False)).lower()}
  icons_and_splash: {str(caps.get('icons_and_splash', False)).lower()}
  network_interceptors: {str(caps.get('network_interceptors', False)).lower()}
  permissions:
    media: {str(p.get('media', False)).lower()}
    location: {str(p.get('location', False)).lower()}
    notifications: {str(p.get('notifications', False)).lower()}
  store_updater: {str(caps.get('store_updater', False)).lower()}
"""

def execute_capabilities_setup(target_dir, caps, toolkit_dir):
    """Executes the setup scripts for each enabled capability."""
    sys.path.insert(0, str(Path(toolkit_dir) / "bin"))

    if caps.get("release_signing"):
        try:
            from setup.setup_signing import setup_signing
            setup_signing(target_dir)
        except Exception as e:
            print(f"⚠️ Signing setup error: {e}")

    if caps.get("icons_and_splash"):
        try:
            from setup.setup_icons_splash import setup_icons_and_splash
            setup_icons_and_splash(target_dir)
        except Exception as e:
            print(f"⚠️ Icons/Splash setup error: {e}")

    if caps.get("network_interceptors"):
        try:
            from setup.setup_network import setup_network_interceptors
            setup_network_interceptors(target_dir)
        except Exception as e:
            print(f"⚠️ Network setup error: {e}")

    # Permissions
    perm_cfg = caps.get("permissions", {})
    active_perms = ["core"]
    if perm_cfg.get("media"): active_perms.append("media")
    if perm_cfg.get("location"): active_perms.append("location")
    if perm_cfg.get("notifications"): active_perms.append("notifications")

    if len(active_perms) > 1 or caps.get("release_signing"):
        try:
            from setup.setup_permissions import setup_permissions
            setup_permissions(target_dir, active_modules=active_perms)
        except Exception as e:
            print(f"⚠️ Permissions setup error: {e}")

    if caps.get("store_updater"):
        try:
            from setup.setup_updater import setup_store_updater
            setup_store_updater(target_dir)
        except Exception as e:
            print(f"⚠️ Store updater setup error: {e}")

def load_preset(preset_name, toolkit_dir):
    preset_file = Path(toolkit_dir) / "presets" / f"{preset_name}.yaml"
    if not preset_file.exists():
        return None
    with open(preset_file, "r", encoding="utf-8") as f:
        return f.read()

def parse_prd(prd_path):
    """Simple heuristic parser to infer tech stack from a PRD or BRD file."""
    if not os.path.exists(prd_path):
        return {}
    with open(prd_path, "r", encoding="utf-8") as f:
        content = f.read().lower()
    
    inferred = {}
    # Project name
    match = re.search(r"#+\s*(project|app)?\s*name\s*[:\-]?\s*([a-zA-Z0-9_\-]+)", content)
    if match:
        inferred["project_name"] = match.group(2)
        
    # State management
    if "riverpod" in content:
        inferred["state_management"] = "riverpod"
    elif "bloc" in content or "cubit" in content:
        inferred["state_management"] = "bloc_cubit"
    elif "provider" in content:
        inferred["state_management"] = "provider"
        
    # Architecture
    if "clean architecture" in content or "feature-first" in content:
        inferred["architecture"] = "feature_first_clean"
    elif "modular" in content or "monorepo" in content:
        inferred["architecture"] = "modular"
        
    # Network
    if "retrofit" in content:
        inferred["network_client"] = "retrofit"
    elif "dio" in content:
        inferred["network_client"] = "dio"
        
    # Localization & Direction
    if "arabic" in content or "rtl" in content:
        inferred["directionality"] = "rtl_first"
        inferred["default_locale"] = "ar"
    else:
        inferred["directionality"] = "ltr_first"
        inferred["default_locale"] = "en"
        
    return inferred

def inspect_pubspec(target_dir):
    """Detects dependencies from an existing pubspec.yaml if present."""
    pubspec = Path(target_dir) / "pubspec.yaml"
    detected = {}
    if not pubspec.exists():
        return detected
    with open(pubspec, "r", encoding="utf-8") as f:
        content = f.read().lower()
        
    if "flutter_bloc:" in content or "bloc:" in content:
        detected["state_management"] = "bloc_cubit"
    elif "flutter_riverpod:" in content or "riverpod:" in content:
        detected["state_management"] = "riverpod"
    elif "provider:" in content:
        detected["state_management"] = "provider"
        
    if "dio:" in content:
        detected["network_client"] = "dio"
    elif "http:" in content and "dio:" not in content:
        detected["network_client"] = "http"
        
    if "get_it:" in content:
        detected["dependency_injection"] = "injectable_get_it"
        
    if "go_router:" in content:
        detected["navigation"] = "go_router"
    elif "auto_route:" in content:
        detected["navigation"] = "auto_route"
        
    if "easy_localization:" in content:
        detected["localization_engine"] = "easy_localization_json"
    elif "slang:" in content:
        detected["localization_engine"] = "slang"
    elif "flutter_localizations:" in content:
        detected["localization_engine"] = "arb_gen_l10n"
        
    return detected

def ask_question(question, options, default, explanation, ai_recommendation):
    print("\n" + "="*70)
    print(f"❓ {question}")
    print("="*70)
    for idx, (key, label) in enumerate(options.items(), 1):
        is_default = " (Default)" if key == default else ""
        print(f"  [{idx}] {label}{is_default}")
    print("  [s] Skip (Use Default)")
    print("  [?] I Don't Know (Explain trade-offs)")
    print("  [b] Choose the Best (AI Recommendation)")
    
    while True:
        choice = input("\n👉 Your selection: ").strip().lower()
        if choice in ['s', 'skip', '']:
            return default
        elif choice == '?':
            print("\n💡 TRADE-OFF EXPLANATION:")
            print(explanation)
            continue
        elif choice in ['b', 'best']:
            rec_val, rec_reason = ai_recommendation
            print(f"\n🤖 AI RECOMMENDATION: '{rec_val}'")
            print(f"   Reasoning: {rec_reason}")
            confirm = input("   Accept this recommendation? [Y/n]: ").strip().lower()
            if confirm in ['y', 'yes', '']:
                return rec_val
            continue
            
        # Match option number or key
        option_keys = list(options.keys())
        if choice.isdigit() and 1 <= int(choice) <= len(option_keys):
            return option_keys[int(choice) - 1]
        elif choice in options:
            return choice
        else:
            print("⚠️ Invalid choice. Please enter a valid number, option key, 's', '?', or 'b'.")

def run_wizard():
    parser = argparse.ArgumentParser(description="Universal AI Toolkit Project Profile Wizard")
    parser.add_argument("--prd", help="Path to PRD or BRD markdown file")
    parser.add_argument("--preset", help="Preset name (enterprise_clean_bloc, modern_modular_riverpod, lean_mvp, moltaqa)")
    parser.add_argument("--target-dir", default=".", help="Target project root directory")
    parser.add_argument("--single", action="store_true", help="Force single app topology (no flavors)")
    parser.add_argument("--flavors", help="Comma-separated list of flavors (e.g. user,provider or dev,staging,prod)")
    parser.add_argument("--sync-deps", action="store_true", help="Automatically sync required packages from pub.dev")
    parser.add_argument("--setup-flavors", action="store_true", help="Automatically setup Android & iOS flavors")
    parser.add_argument("--with-signing", action="store_true", help="Setup release signing config")
    parser.add_argument("--with-icons-splash", action="store_true", help="Setup launcher icons and native splash")
    parser.add_argument("--with-network", action="store_true", help="Setup core network interceptors and failure mappers")
    parser.add_argument("--with-permissions", help="Comma-separated permission modules (core, media, location, notifications)")
    parser.add_argument("--with-updater", action="store_true", help="Setup force store updater service")
    parser.add_argument("--all-capabilities", action="store_true", help="Enable all optional capabilities")
    args = parser.parse_args()

    toolkit_dir = Path(__file__).resolve().parents[2]
    target_dir = Path(args.target_dir).resolve()
    
    print("\n" + "🚀"*35)
    print("  UNIVERSAL AI TOOLKIT v2 — PROJECT PROFILING WIZARD")
    print("🚀"*35)
    
    # Check for direct preset
    if args.preset:
        content = load_preset(args.preset, toolkit_dir)
        if content:
            if args.single or args.flavors:
                proj_type, fl_list = resolve_topology_interactive(target_dir, args.single, args.flavors, prompt_if_interactive=False)
                final_content = apply_topology_to_preset(content, proj_type, fl_list, project_name=target_dir.name)
            else:
                final_content = content
                fl_match = re.search(r"flavors\s*:\s*\n((?:\s*-\s*[^\n]+\n)+)", content)
                fl_list = [l.strip().lstrip("-").strip().strip("\"'") for l in fl_match.group(1).splitlines() if l.strip().startswith("-")] if fl_match else []
                proj_type = "multi_flavor" if fl_list else "single_app"

            # Check CLI capabilities
            caps = resolve_capabilities_interactive(args, prompt_if_interactive=False)
            has_caps = any([caps["release_signing"], caps["icons_and_splash"], caps["network_interceptors"], caps["store_updater"], any(caps["permissions"].values())])
            if has_caps:
                final_content += format_capabilities_yaml(caps)

            out_file = target_dir / "project_profile.yaml"
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(final_content)

            if has_caps:
                execute_capabilities_setup(target_dir, caps, toolkit_dir)

            print(f"✅ Created {out_file} using preset '{args.preset}' (topology: {proj_type}, flavors: {fl_list or 'none'}).")
            generate_project_scaffolding(target_dir, {"project_name": target_dir.name, "architecture": "feature_first_clean", "state_management": "bloc_cubit", "flavors": fl_list, "project_type": proj_type}, toolkit_dir, sync_deps_flag=args.sync_deps, setup_flavors_flag=args.setup_flavors, prompt_optional=False)
            return

    # Check for existing PRD or pubspec
    inferred_prd = parse_prd(args.prd) if args.prd else {}
    detected_pub = inspect_pubspec(target_dir)

    print("\nSelect starting mode:")
    print("  [1] Interactive Setup (Step-by-step with Smart AI guidance)")
    print("  [2] Select from Standard Presets")
    mode = input("👉 Mode [1/2, default: 1]: ").strip()

    if mode == "2":
        print("\nAvailable Presets:")
        for k, (name, desc) in PRESETS.items():
            print(f"  [{k}] {desc}")
        p_choice = input(f"👉 Select preset [1-{len(PRESETS)}]: ").strip()
        selected_preset = PRESETS.get(p_choice, PRESETS["1"])[0]
        content = load_preset(selected_preset, toolkit_dir)

        customize_top = input("\n❓ Do you want to customize project topology (Single App / Multi-Flavor)? [y/N]: ").strip().lower()
        if customize_top in ['y', 'yes']:
            proj_type, fl_list = resolve_topology_interactive(target_dir, args.single, args.flavors, prompt_if_interactive=True)
            final_content = apply_topology_to_preset(content, proj_type, fl_list, project_name=target_dir.name)
        else:
            final_content = content
            fl_match = re.search(r"flavors\s*:\s*\n((?:\s*-\s*[^\n]+)+)", content)
            fl_list = [l.strip().lstrip("-").strip().strip("\"'") for l in fl_match.group(1).splitlines() if l.strip().startswith("-")] if fl_match else []
            proj_type = "multi_flavor" if fl_list else "single_app"

        # Optional capabilities customization
        customize_caps = input("\n❓ Do you want to configure optional capabilities (Signing, Splash/Icons, Network, Permissions)? [y/N]: ").strip().lower()
        has_caps = False
        if customize_caps in ['y', 'yes']:
            caps = resolve_capabilities_interactive(args, prompt_if_interactive=True)
            has_caps = any([caps["release_signing"], caps["icons_and_splash"], caps["network_interceptors"], caps["store_updater"], any(caps["permissions"].values())])
            if has_caps:
                final_content += format_capabilities_yaml(caps)

        out_file = target_dir / "project_profile.yaml"
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(final_content)

        if has_caps:
            execute_capabilities_setup(target_dir, caps, toolkit_dir)

        print(f"\n✅ Created {out_file} from preset '{selected_preset}' (topology: {proj_type}, flavors: {fl_list or 'none'}).")
        generate_project_scaffolding(target_dir, {"project_name": target_dir.name, "architecture": "feature_first_clean", "state_management": "bloc_cubit", "flavors": fl_list, "project_type": proj_type}, toolkit_dir, sync_deps_flag=args.sync_deps, setup_flavors_flag=args.setup_flavors, prompt_optional=True)
        return

    # Step-by-step Interactive Mode
    p_name = inferred_prd.get("project_name", target_dir.name)
    user_name = input(f"\n🏷️ Project Name [{p_name}]: ").strip()
    project_name = user_name if user_name else p_name

    # 1. Project Type
    project_type = ask_question(
        question="What is the archetype and flavor structure of your application?",
        options={
            "single_app": "Single Application (Standard single mobile/web app)",
            "multi_flavor": "Multi-Flavor App (Dev, Staging, Prod or User/Provider/Delivery variants)",
            "multi_package": "Multi-Package Workspace (Multiple apps sharing internal local packages)",
            "monorepo": "Enterprise Monorepo (Melos managed monorepo)"
        },
        default="multi_flavor" if "flavor" in str(detected_pub) else "single_app",
        explanation="Single App is ideal for simple apps. Multi-Flavor is necessary when you deploy separate apps (e.g. User vs Driver) or multiple environment builds. Monorepo is for large teams.",
        ai_recommendation=("multi_flavor", "Multi-flavor provides safe separation of environments (dev/prod) and prevents production data contamination.")
    )

    flavors = []
    if project_type in ["multi_flavor", "multi_package"]:
        fl_input = input("Enter flavor names separated by commas [e.g. dev, staging, prod]: ").strip()
        if fl_input:
            flavors = [f.strip() for f in fl_input.split(",") if f.strip()]
        else:
            flavors = ["dev", "prod"]

    # 2. Architecture
    architecture = ask_question(
        question="What architectural pattern will govern the codebase?",
        options={
            "feature_first_clean": "Feature-First Clean Architecture (domain, data, presentation per feature)",
            "modular": "Modular Architecture (isolated autonomous feature modules)",
            "layer_first": "Layer-First Architecture (controllers, models, views in top-level folders)",
            "custom": "Custom / Legacy Structure"
        },
        default=inferred_prd.get("architecture", "feature_first_clean"),
        explanation="Feature-First Clean Architecture scales best with AI agents because each feature is self-contained with its own models, repositories, and UI.",
        ai_recommendation=("feature_first_clean", "Best industry standard for maintainability, testability, and agent token isolation.")
    )

    # 3. State Management
    state_management = ask_question(
        question="Which state management solution will be used?",
        options={
            "bloc_cubit": "BLoC / Cubit (Predictable event/state streams, strict separation)",
            "riverpod": "Riverpod (Compile-safe, reactive, zero boilerplate provider replacement)",
            "provider": "Provider (Classic, lightweight InheritedWidget wrapper)",
            "mobx": "MobX (Transparent functional reactive programming)",
            "signals": "Signals / ValueNotifiers (Fine-grained reactivity)"
        },
        default=detected_pub.get("state_management", inferred_prd.get("state_management", "bloc_cubit")),
        explanation="BLoC/Cubit enforces strict event/state classes which AI agents follow with high reliability. Riverpod is modern and very type-safe.",
        ai_recommendation=(
            detected_pub.get("state_management", "bloc_cubit"),
            "Detected in existing project or recommended for predictable state pipelines."
        )
    )

    # 4. Network Client
    network_client = ask_question(
        question="Which networking client and HTTP abstraction will you use?",
        options={
            "dio": "Dio (Feature-rich with interceptors, cancellation, transformers)",
            "retrofit": "Retrofit with Dio (Type-safe declarative REST client generation)",
            "http": "Standard Dart 'http' package (Minimalist)",
            "graphql": "GraphQL Flutter"
        },
        default=detected_pub.get("network_client", "dio"),
        explanation="Dio is the Flutter industry standard offering comprehensive interceptor chains, token refresh handling, and error mapping.",
        ai_recommendation=("dio", "Essential for robust interceptors, token caching, and logging.")
    )

    # 5. Dependency Injection
    dependency_injection = ask_question(
        question="How will dependencies be managed and resolved?",
        options={
            "injectable_get_it": "GetIt + Injectable (Annotation-based code-generated service locator)",
            "riverpod": "Riverpod Built-in DI (Providers resolve dependencies automatically)",
            "none_manual": "Manual Constructor Injection (No DI container)"
        },
        default="riverpod" if state_management == "riverpod" else "injectable_get_it",
        explanation="GetIt + Injectable generates compile-safe wiring. If using Riverpod, its built-in provider graph replaces GetIt.",
        ai_recommendation=(
            "riverpod" if state_management == "riverpod" else "injectable_get_it",
            "Aligns seamlessly with your state management choice."
        )
    )

    # 6. Navigation
    navigation = ask_question(
        question="Which routing library will drive screen navigation and deep linking?",
        options={
            "go_router": "GoRouter (Declarative, URL-driven, official Flutter recommendation)",
            "auto_route": "AutoRoute (Annotation-driven, strongly typed arguments)",
            "navigator_2": "Standard Navigator 2.0 (Direct imperative/declarative routing)"
        },
        default=detected_pub.get("navigation", "go_router"),
        explanation="GoRouter is official, handles web/mobile URLs, deep linking, and guards cleanly.",
        ai_recommendation=("go_router", "Official Flutter standard with seamless deep link and guard support.")
    )

    # 7. Localization & Directionality
    localization_engine = ask_question(
        question="Which localization engine will handle translations?",
        options={
            "arb_gen_l10n": "Flutter Official ARB (flutter gen-l10n with type-safe accessors)",
            "easy_localization_json": "Easy Localization (Simple JSON translation files)",
            "slang": "Slang (Type-safe, plural-rich, reactive i18n)",
            "none": "None (Hardcoded strings - not recommended)"
        },
        default=detected_pub.get("localization_engine", "arb_gen_l10n"),
        explanation="Official ARB files integrate directly into Flutter SDK build tooling and ensure type safety.",
        ai_recommendation=("arb_gen_l10n", "Built-in SDK support without extra runtime dependencies.")
    )

    directionality = ask_question(
        question="What is the primary layout directionality for the UI?",
        options={
            "rtl_first": "RTL-First (Arabic / Hebrew primary; English secondary)",
            "ltr_first": "LTR-First (English / European primary)",
            "bi_directional": "Bi-Directional Equal (Strict semantic directional APIs everywhere)"
        },
        default=inferred_prd.get("directionality", "rtl_first"),
        explanation="RTL-First ensures mirrored back buttons, directional padding, and proper Arabic alignment from day 1.",
        ai_recommendation=(inferred_prd.get("directionality", "rtl_first"), "Based on target market requirements.")
    )

    # 8. Design System & Sources
    design_source = ask_question(
        question="How will UI designs, tokens, and screens be ingested?",
        options={
            "figma_folder": "Figma Local Export Folder (Screens, PNGs, Tokens JSON)",
            "figma_mcp": "Figma Cloud via MCP Server (Direct API sync)",
            "google_stitch_folder": "Google Stitch Local Folder (Exported JSON & Screens)",
            "google_stitch_mcp": "Google Stitch via MCP Server",
            "manual": "Manual Developer Specs (No external design tooling)"
        },
        default="figma_folder",
        explanation="Local export folders work 100% offline without API limits or token expiries. MCP connects directly to the design canvas.",
        ai_recommendation=("figma_folder", "Zero network dependency, works offline, and keeps client design assets private.")
    )

    testing_gate = ask_question(
        question="What quality and testing gate policy should be enforced on each feature phase?",
        options={
            "strict": "Strict (Unit/Widget tests are MANDATORY before any phase can be marked DONE)",
            "recommended": "Recommended (Tests written for domain logic and critical state machines)",
            "mvp_disabled": "Fast-Track MVP (Testing disabled; focus on rapid delivery)"
        },
        default="recommended",
        explanation="Strict is recommended for banking/e-commerce. Recommended is standard for startups.",
        ai_recommendation=("recommended", "Balances velocity with solid test coverage for core business logic.")
    )

    # Optional Secrets
    secrets_prompt = input("\n🔐 Would you like to enable environment secrets management (.env / dart-define)? [y/N]: ").strip().lower()
    secrets_enabled = secrets_prompt in ['y', 'yes']
    secrets_strategy = "dart_define" if secrets_enabled else "none"

    # Assemble YAML profile
    flavors_yaml = "\n".join([f"  - '{f}'" for f in flavors]) if flavors else "  []"
    
    profile_data = {
        "project_name": project_name,
        "project_type": project_type,
        "flavors": flavors,
        "architecture": architecture,
        "state_management": state_management,
        "network_client": network_client,
        "dependency_injection": dependency_injection,
        "navigation": navigation,
        "localization": {
            "engine": localization_engine,
            "default_locale": "ar" if directionality == "rtl_first" else "en",
            "supported_locales": ["ar", "en"]
        },
        "directionality": directionality,
        "design_system": {
            "tokens_path": "lib/core/configs/values" if architecture == "feature_first_clean" else "lib/theme",
            "source": design_source,
            "strict_mode": True
        },
        "testing_gate": testing_gate,
        "secrets_management": {
            "enabled": secrets_enabled,
            "strategy": secrets_strategy
        },
        "living_documentation": {
            "living_readme": True,
            "feature_readmes": True
        },
        "custom_tokens": {
            "button": "lib/material/buttons/app_button.dart",
            "back_button": "lib/material/buttons/app_back_button.dart",
            "image": "lib/material/media/app_image.dart",
            "svg_icon": "lib/material/media/svg_icon.dart",
            "text_field": "lib/material/inputs/app_text_form_field.dart",
            "loading_widget": "lib/material/loading/app_loading_widget.dart"
        }
    }

    # Format YAML
    profile_yaml = f"""# Universal Project Profile
# Generated by Universal AI Toolkit v2 Wizard (toolkit init)

project_name: "{profile_data['project_name']}"
project_type: "{profile_data['project_type']}"
flavors:
{flavors_yaml}

# Architecture & Organization
architecture: "{profile_data['architecture']}"

# State Management & Data
state_management: "{profile_data['state_management']}"
network_client: "{profile_data['network_client']}"
dependency_injection: "{profile_data['dependency_injection']}"
navigation: "{profile_data['navigation']}"

# Localization & Direction
localization:
  engine: "{profile_data['localization']['engine']}"
  default_locale: "{profile_data['localization']['default_locale']}"
  supported_locales:
    - "ar"
    - "en"
directionality: "{profile_data['directionality']}"

# Design System & UI Constraints
design_system:
  tokens_path: "{profile_data['design_system']['tokens_path']}"
  source: "{profile_data['design_system']['source']}"
  strict_mode: true

# Quality & Testing Gate
testing_gate: "{profile_data['testing_gate']}"

# Environments & Secrets
secrets_management:
  enabled: {str(profile_data['secrets_management']['enabled']).lower()}
  strategy: "{profile_data['secrets_management']['strategy']}"

# Living Documentation Engine
living_documentation:
  living_readme: true
  feature_readmes: true

# Autonomous QA & Verification Engine
qa_verification:
  enabled: true
  runner: "maestro"
  device:
    platform: "android"
    preferred_avd: "Pixel_7_API_34"
  tolerance: "semantic"
  auto_fix_max_retries: 3
  flows_path: "test/qa_flows"
  reports_path: "test/qa_reports"
  states_to_test:
    - "default"
    - "loading"
    - "empty"
    - "error"
    - "offline"

# Design System Shared Wrappers
custom_tokens:
  button: "{profile_data['custom_tokens']['button']}"
  back_button: "{profile_data['custom_tokens']['back_button']}"
  image: "{profile_data['custom_tokens']['image']}"
  svg_icon: "{profile_data['custom_tokens']['svg_icon']}"
  text_field: "{profile_data['custom_tokens']['text_field']}"
  loading_widget: "{profile_data['custom_tokens']['loading_widget']}"
"""

    # Resolve optional capabilities
    caps = resolve_capabilities_interactive(args, prompt_if_interactive=True)
    if any([caps["release_signing"], caps["icons_and_splash"], caps["network_interceptors"], caps["store_updater"], any(caps["permissions"].values())]):
        profile_yaml += format_capabilities_yaml(caps)

    print("\n" + "📋"*35)
    print("DRAFT PROJECT PROFILE (project_profile.yaml):")
    print("📋"*35)
    print(profile_yaml)
    print("📋"*35)

    confirm = input("\n❓ Does this profile look good to save? [Y/n]: ").strip().lower()
    if confirm in ['y', 'yes', '']:
        out_file = target_dir / "project_profile.yaml"
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(profile_yaml)
        print(f"\n🎉 Successfully created {out_file}!")
        print("💡 The project identity is now locked. Workflows will adhere to this specification.")

        if any([caps["release_signing"], caps["icons_and_splash"], caps["network_interceptors"], caps["store_updater"], any(caps["permissions"].values())]):
            execute_capabilities_setup(target_dir, caps, toolkit_dir)

        # Scaffold ai_docs, ai_specs, and ai_worklog
        generate_project_scaffolding(target_dir, profile_data, toolkit_dir, sync_deps_flag=args.sync_deps, setup_flavors_flag=args.setup_flavors, prompt_optional=True)
    else:
        print("\n❌ Cancelled. No changes saved.")

def generate_project_scaffolding(target_dir, profile, toolkit_dir, sync_deps_flag=False, setup_flavors_flag=False, prompt_optional=False):
    """Generates ai_docs, ai_specs, and ai_worklog directories tailored to the project profile."""
    ai_docs = target_dir / "ai_docs"
    ai_specs = target_dir / "ai_specs"
    ai_worklog = target_dir / "ai_worklog"
    
    ai_docs.mkdir(parents=True, exist_ok=True)
    (ai_specs / "features").mkdir(parents=True, exist_ok=True)
    (ai_specs / "design").mkdir(parents=True, exist_ok=True)
    (ai_specs / "api" / "contracts").mkdir(parents=True, exist_ok=True)
    (ai_worklog / "daily").mkdir(parents=True, exist_ok=True)
    (target_dir / "test" / "qa_flows").mkdir(parents=True, exist_ok=True)
    (target_dir / "test" / "qa_reports").mkdir(parents=True, exist_ok=True)
    (ai_docs / "qa").mkdir(parents=True, exist_ok=True)

    templates_dir = Path(toolkit_dir) / "templates" / "app-seed" / "ai_docs"

    # Replacements map
    replacements = {
        "{{PROJECT_NAME}}": str(profile.get("project_name", "")),
        "{{PROJECT_TYPE}}": str(profile.get("project_type", "")),
        "{{FLAVORS_LIST}}": ", ".join(profile.get("flavors", [])) or "None (Single App)",
        "{{ARCHITECTURE}}": str(profile.get("architecture", "")),
        "{{STATE_MANAGEMENT}}": str(profile.get("state_management", "")),
        "{{NETWORK_CLIENT}}": str(profile.get("network_client", "")),
        "{{DEPENDENCY_INJECTION}}": str(profile.get("dependency_injection", "")),
        "{{NAVIGATION}}": str(profile.get("navigation", "")),
        "{{L10N_ENGINE}}": str(profile.get("localization", {}).get("engine", "")),
        "{{DEFAULT_LOCALE}}": str(profile.get("localization", {}).get("default_locale", "")),
        "{{DIRECTIONALITY}}": str(profile.get("directionality", "")),
        "{{DESIGN_SOURCE}}": str(profile.get("design_system", {}).get("source", "")),
        "{{TOKENS_PATH}}": str(profile.get("design_system", {}).get("tokens_path", "")),
        "{{TESTING_GATE}}": str(profile.get("testing_gate", "")),
        "{{TOKEN_BUTTON_NAME}}": "AppButton",
        "{{TOKEN_BUTTON_PATH}}": str(profile.get("custom_tokens", {}).get("button", "lib/common/widgets/app_button.dart")),
        "{{TOKEN_BACK_BUTTON_NAME}}": "AppBackButton",
        "{{TOKEN_BACK_BUTTON_PATH}}": str(profile.get("custom_tokens", {}).get("back_button", "lib/common/widgets/app_back_button.dart")),
        "{{TOKEN_IMAGE_NAME}}": "AppImage",
        "{{TOKEN_IMAGE_PATH}}": str(profile.get("custom_tokens", {}).get("image", "lib/common/widgets/app_image.dart")),
        "{{TOKEN_SVG_NAME}}": "AppSvgIcon",
        "{{TOKEN_SVG_PATH}}": str(profile.get("custom_tokens", {}).get("svg_icon", "lib/common/widgets/svg_icon.dart")),
        "{{TOKEN_TEXT_FIELD_NAME}}": "AppTextFormField",
        "{{TOKEN_TEXT_FIELD_PATH}}": str(profile.get("custom_tokens", {}).get("text_field", "lib/common/widgets/app_text_field.dart")),
        "{{TOKEN_LOADING_NAME}}": "AppLoadingWidget",
        "{{TOKEN_LOADING_PATH}}": str(profile.get("custom_tokens", {}).get("loading_widget", "lib/common/widgets/loading_widget.dart")),
    }

    # Generate ai_docs/
    for doc in ["conventions", "architecture", "memory"]:
        tmpl = templates_dir / f"{doc}.template.md"
        out_doc = ai_docs / f"{doc}.md"
        if tmpl.exists() and not out_doc.exists():
            with open(tmpl, "r", encoding="utf-8") as f:
                content = f.read()
            for k, v in replacements.items():
                content = content.replace(k, v)
            with open(out_doc, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"   ✅ Scaffolded ai_docs/{doc}.md")

    # Generate ai_specs/INDEX.md
    specs_index = ai_specs / "INDEX.md"
    if not specs_index.exists():
        with open(specs_index, "w", encoding="utf-8") as f:
            f.write(f"# Feature Specifications Index — {profile.get('project_name')}\n\n## Active Features\n| Feature | Status | Plan | Spec |\n| :--- | :---: | :---: | :---: |\n")
        print("   ✅ Scaffolded ai_specs/INDEX.md")

    # Generate ai_worklog/TODOS.md
    todos_file = ai_worklog / "TODOS.md"
    if not todos_file.exists():
        with open(todos_file, "w", encoding="utf-8") as f:
            f.write(f"# Project Backlog & Open TODOs — {profile.get('project_name')}\n\n## High Priority\n- [ ] Initialize core modules and design tokens\n")
        print("   ✅ Scaffolded ai_worklog/TODOS.md")

    # Auto Package Sync (if pubspec.yaml exists)
    pubspec_path = target_dir / "pubspec.yaml"
    if pubspec_path.exists():
        do_sync = False
        if sync_deps_flag is True:
            do_sync = True
        elif prompt_optional and sys.stdin.isatty():
            ans = input("\n📦 Would you like to auto-sync required packages from pub.dev now? [Y/n]: ").strip().lower()
            do_sync = (ans in ['y', 'yes', ''])

        if do_sync:
            try:
                sys.path.insert(0, str(Path(toolkit_dir) / "bin"))
                from deps.sync_packages import sync_packages
                sync_packages(target_dir)
            except Exception as e:
                print(f"⚠️ Package sync error: {e}")

    # Auto Modern Flavors Setup (if multi_flavor)
    if profile.get("project_type") == "multi_flavor" and profile.get("flavors"):
        do_flavors = False
        if setup_flavors_flag is True:
            do_flavors = True
        elif prompt_optional and sys.stdin.isatty():
            ans = input("\n🎨 Would you like to setup Android & iOS flavors now? [Y/n]: ").strip().lower()
            do_flavors = (ans in ['y', 'yes', ''])

        if do_flavors:
            try:
                sys.path.insert(0, str(Path(toolkit_dir) / "bin"))
                from flavors.setup_flavors import setup_flavors
                setup_flavors(target_dir)
            except Exception as e:
                print(f"⚠️ Flavors setup error: {e}")

if __name__ == "__main__":
    run_wizard()
