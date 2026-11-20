#!/usr/bin/env python3
"""
Universal AI Toolkit v2 — Smart Package Sync Engine
Reads architectural decisions from project_profile.yaml and synchronizes
required dependencies and dev_dependencies from pub.dev at their latest compatible versions.
Uses Python Standard Library ONLY (zero pip dependencies).
"""

import sys
import os
import re
import json
import shutil
import subprocess
import urllib.request
from pathlib import Path

# Mapping of profile decisions to packages
PACKAGE_MAP = {
    "state_management": {
        "bloc_cubit": (["flutter_bloc"], []),
        "riverpod": (["flutter_riverpod", "riverpod_annotation"], ["riverpod_generator", "build_runner"]),
        "provider": (["provider"], []),
        "signals": (["signals_flutter"], []),
        "mobx": (["mobx", "flutter_mobx"], ["mobx_codegen", "build_runner"]),
        "none": ([], [])
    },
    "network_client": {
        "dio": (["dio", "pretty_dio_logger"], []),
        "retrofit": (["dio", "retrofit"], ["retrofit_generator", "build_runner"]),
        "http": (["http"], []),
        "graphql": (["graphql_flutter"], []),
        "none": ([], [])
    },
    "dependency_injection": {
        "injectable_get_it": (["get_it", "injectable"], ["injectable_generator", "build_runner"]),
        "get_it": (["get_it"], []),
        "riverpod": ([], []),
        "none_manual": ([], [])
    },
    "navigation": {
        "go_router": (["go_router"], []),
        "auto_route": (["auto_route"], ["auto_route_generator", "build_runner"]),
        "navigator_2": ([], []),
        "getx_nav": ([], [])
    },
    "localization": {
        "arb_gen_l10n": (["intl"], []),
        "easy_localization_json": (["easy_localization"], []),
        "slang": (["slang", "slang_flutter"], ["slang_build_runner"]),
        "none": ([], [])
    },
    "storage": {
        "secure_and_prefs": (["shared_preferences", "flutter_secure_storage"], []),
        "shared_preferences": (["shared_preferences"], []),
        "flutter_secure_storage": (["flutter_secure_storage"], []),
        "hive": (["hive", "hive_flutter"], ["hive_generator", "build_runner"]),
        "none": ([], [])
    }
}

# Standard recommended foundation packages
STANDARD_DEPS = ["flutter_svg", "equatable"]
STANDARD_DEV_DEPS = ["flutter_lints"]

def load_simple_profile(profile_path):
    """Loads key-value pairs from project_profile.yaml."""
    data = {}
    if not profile_path.exists():
        return data
    with open(profile_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            m = re.match(r"^([a-zA-Z0-9_\-]+)\s*:\s*(.*)", line)
            if m:
                k = m.group(1)
                v = m.group(2).strip().strip("'\"")
                data[k] = v
            # check localization engine
            if "engine:" in line:
                eng = line.split("engine:")[1].strip().strip("'\"")
                data["localization_engine"] = eng
    return data

def parse_existing_pubspec(pubspec_path):
    """Parses existing dependencies and dev_dependencies from pubspec.yaml."""
    deps = set()
    dev_deps = set()
    if not pubspec_path.exists():
        return deps, dev_deps
    
    current_section = None
    with open(pubspec_path, "r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.rstrip()
            if not line or line.strip().startswith("#"):
                continue
            if line.startswith("dependencies:"):
                current_section = "deps"
                continue
            elif line.startswith("dev_dependencies:"):
                current_section = "dev_deps"
                continue
            elif not raw_line.startswith(" ") and not raw_line.startswith("\t"):
                current_section = None
                continue
            
            # Sub-key inside section
            m = re.match(r"^\s+([a-zA-Z0-9_\-]+)\s*:", line)
            if m:
                pkg_name = m.group(1)
                if current_section == "deps":
                    deps.add(pkg_name)
                elif current_section == "dev_deps":
                    dev_deps.add(pkg_name)
    return deps, dev_deps

def fetch_latest_pub_version(pkg_name):
    """Fallback: queries pub.dev official API for latest stable version."""
    url = f"https://pub.dev/api/packages/{pkg_name}"
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Universal-AI-Toolkit-v2/1.0"}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                body = json.loads(response.read().decode("utf-8"))
                return body.get("latest", {}).get("version")
    except Exception:
        pass
    return None

def sync_packages(target_dir=".", dry_run=False):
    target_path = Path(target_dir).resolve()
    profile_path = target_path / "project_profile.yaml"
    pubspec_path = target_path / "pubspec.yaml"

    if not profile_path.exists():
        print(f"❌ Error: {profile_path} not found. Run 'toolkit init' first.")
        return False

    if not pubspec_path.exists():
        print(f"⚠️ Warning: {pubspec_path} not found. Skipping package synchronization.")
        return False

    profile = load_simple_profile(profile_path)
    existing_deps, existing_dev_deps = parse_existing_pubspec(pubspec_path)

    # Collect target packages based on profile
    target_deps = set(STANDARD_DEPS)
    target_dev_deps = set(STANDARD_DEV_DEPS)

    for category, choices in PACKAGE_MAP.items():
        if category == "localization":
            val = profile.get("localization_engine", "arb_gen_l10n")
        else:
            val = profile.get(category, "")
        
        if val in choices:
            d, dev = choices[val]
            target_deps.update(d)
            target_dev_deps.update(dev)

    # Filter out already installed packages
    needed_deps = [p for p in target_deps if p not in existing_deps]
    needed_dev_deps = [p for p in target_dev_deps if p not in existing_dev_deps and p not in existing_deps]

    print("\n" + "📦"*35)
    print("  UNIVERSAL AI TOOLKIT v2 — SMART PACKAGE SYNC")
    print("📦"*35)
    print(f"📂 Project Root: {target_path}")
    print(f"🔍 Architecture: {profile.get('architecture', 'unknown')}")
    print(f"⚙️ State Management: {profile.get('state_management', 'unknown')}")
    print(f"🌐 Network Client: {profile.get('network_client', 'unknown')}")
    print(f"💉 Dependency Injection: {profile.get('dependency_injection', 'unknown')}")
    print(f"🧭 Navigation: {profile.get('navigation', 'unknown')}")

    if not needed_deps and not needed_dev_deps:
        print("\n✅ All required packages are already installed in pubspec.yaml!")
        print("="*70 + "\n")
        return True

    print(f"\n📥 Required Dependencies to add ({len(needed_deps)}):")
    for p in sorted(needed_deps):
        print(f"   • {p}")

    print(f"\n🛠️ Required Dev Dependencies to add ({len(needed_dev_deps)}):")
    for p in sorted(needed_dev_deps):
        print(f"   • {p}")

    if dry_run:
        print("\n🔎 Dry-run enabled: No changes applied.")
        return True

    # Check if flutter CLI is available
    flutter_bin = shutil.which("flutter")
    if flutter_bin:
        print("\n🚀 Resolving latest compatible versions via Flutter CLI...")
        success = True
        if needed_deps:
            cmd = ["flutter", "pub", "add"] + needed_deps
            print(f"👉 Running: {' '.join(cmd)}")
            res = subprocess.run(cmd, cwd=target_path)
            if res.returncode != 0:
                success = False

        if needed_dev_deps:
            cmd = ["flutter", "pub", "add", "-d"] + needed_dev_deps
            print(f"👉 Running: {' '.join(cmd)}")
            res = subprocess.run(cmd, cwd=target_path)
            if res.returncode != 0:
                success = False

        if success:
            print("\n🎉 Packages synchronized and resolved successfully at their latest compatible versions!")
        else:
            print("\n⚠️ Note: Some packages could not be resolved automatically. Check pubspec.yaml constraints.")
        print("="*70 + "\n")
        return success
    else:
        # Fallback to direct pub.dev API query and writing into pubspec.yaml
        print("\n🌐 Flutter binary not in PATH. Fetching latest stable versions from pub.dev API...")
        resolved_deps = {}
        resolved_dev = {}
        for p in needed_deps:
            v = fetch_latest_pub_version(p)
            resolved_deps[p] = f"^{v}" if v else "any"
            print(f"   • {p}: {resolved_deps[p]}")

        for p in needed_dev_deps:
            v = fetch_latest_pub_version(p)
            resolved_dev[p] = f"^{v}" if v else "any"
            print(f"   • {p} (dev): {resolved_dev[p]}")

        # Inject into pubspec.yaml
        with open(pubspec_path, "r", encoding="utf-8") as f:
            content = f.read()

        if resolved_deps:
            deps_block = "\n".join([f"  {k}: {v}" for k, v in resolved_deps.items()])
            content = re.sub(r"(dependencies:\s*\n)", r"\1" + deps_block + "\n", content, count=1)

        if resolved_dev:
            dev_block = "\n".join([f"  {k}: {v}" for k, v in resolved_dev.items()])
            content = re.sub(r"(dev_dependencies:\s*\n)", r"\1" + dev_block + "\n", content, count=1)

        with open(pubspec_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"\n🎉 Successfully added packages directly to {pubspec_path}!")
        print("💡 Run 'flutter pub get' once Flutter is available.")
        print("="*70 + "\n")
        return True

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "."
    dry = "--dry-run" in sys.argv
    sync_packages(target, dry_run=dry)
