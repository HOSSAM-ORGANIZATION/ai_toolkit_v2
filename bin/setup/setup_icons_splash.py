#!/usr/bin/env python3
"""
Universal AI Toolkit v2 — Launcher Icons & Native Splash Setup Engine
Configures flutter_launcher_icons and flutter_native_splash for single-app or multi-flavor projects.
Uses Python Standard Library ONLY (zero pip dependencies).
"""

import sys
import os
import re
from pathlib import Path

def load_simple_profile(profile_path):
    """Simple parser extracting top-level keys and list items."""
    data = {}
    if not profile_path.exists():
        return data
    with open(profile_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    current_key = None
    for raw in lines:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        top = re.match(r"^([a-zA-Z0-9_\-]+)\s*:\s*(.*)", line)
        if top and not raw.startswith(" ") and not raw.startswith("\t"):
            k = top.group(1)
            v = top.group(2).strip().strip("'\"")
            current_key = k
            data[k] = v if v else []
            continue
        lm = re.match(r"^\s*-\s*[\"']?([a-zA-Z0-9_\-]+)[\"']?", line)
        if lm and current_key and isinstance(data.get(current_key), list):
            data[current_key].append(lm.group(1).strip())
    return data

def setup_icons_and_splash(target_dir="."):
    target_path = Path(target_dir).resolve()
    profile_path = target_path / "project_profile.yaml"
    profile = load_simple_profile(profile_path)

    proj_type = profile.get("project_type", "single_app")
    flavors = profile.get("flavors", [])
    if isinstance(flavors, str) and flavors:
        flavors = [flavors]
    elif not isinstance(flavors, list):
        flavors = []

    print("\n" + "🎨"*35)
    print("  UNIVERSAL AI TOOLKIT v2 — ICONS & SPLASH SETUP")
    print("🎨"*35)
    print(f"📂 Project Root: {target_path}")
    print(f"🏢 Project Type: {proj_type}")

    assets_dir = target_path / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)

    if proj_type == "multi_flavor" and flavors:
        print(f"🏷️ Configuring Multi-Flavor Icons & Splash for: {', '.join(flavors)}")
        for fl in flavors:
            # 1. Directories
            icon_dir = assets_dir / "launcher_icon" / fl
            splash_dir = assets_dir / "native_splash" / fl
            icon_dir.mkdir(parents=True, exist_ok=True)
            splash_dir.mkdir(parents=True, exist_ok=True)

            # 2. flutter_launcher_icons-<flavor>.yaml
            icon_yaml = target_path / f"flutter_launcher_icons-{fl}.yaml"
            if not icon_yaml.exists():
                with open(icon_yaml, "w", encoding="utf-8") as f:
                    f.write(f"""# Launcher Icon Configuration for flavor '{fl}'
# Run: dart run flutter_launcher_icons -f flutter_launcher_icons-{fl}.yaml
flutter_launcher_icons:
  android: "ic_launcher"
  ios: true
  remove_alpha_ios: true
  image_path: "assets/launcher_icon/{fl}/app_launcher.png"
  adaptive_icon_background: "#FFFFFF"
  adaptive_icon_foreground: "assets/launcher_icon/{fl}/app_launcher.png"
""")
                print(f"   ✅ Created: flutter_launcher_icons-{fl}.yaml")

            # 3. flutter_native_splash-<flavor>.yaml
            splash_yaml = target_path / f"flutter_native_splash-{fl}.yaml"
            if not splash_yaml.exists():
                with open(splash_yaml, "w", encoding="utf-8") as f:
                    f.write(f"""# Native Splash Configuration for flavor '{fl}'
# Run: dart run flutter_native_splash:create --flavor {fl}
flutter_native_splash:
  color: "#FFFFFF"
  color_dark: "#121212"
  image: "assets/native_splash/{fl}/native_splash.png"
  android_12:
    color: "#FFFFFF"
    color_dark: "#121212"
    image: "assets/native_splash/{fl}/native_splash.png"
  fullscreen: true
  android: true
  ios: true
  web: false
""")
                print(f"   ✅ Created: flutter_native_splash-{fl}.yaml")
    else:
        print("📱 Configuring Single-App Icons & Splash")
        icon_dir = assets_dir / "launcher_icon"
        splash_dir = assets_dir / "native_splash"
        icon_dir.mkdir(parents=True, exist_ok=True)
        splash_dir.mkdir(parents=True, exist_ok=True)

        icon_yaml = target_path / "flutter_launcher_icons.yaml"
        if not icon_yaml.exists():
            with open(icon_yaml, "w", encoding="utf-8") as f:
                f.write("""flutter_launcher_icons:
  android: "ic_launcher"
  ios: true
  remove_alpha_ios: true
  image_path: "assets/launcher_icon/app_launcher.png"
  adaptive_icon_background: "#FFFFFF"
  adaptive_icon_foreground: "assets/launcher_icon/app_launcher.png"
""")
            print("   ✅ Created: flutter_launcher_icons.yaml")

        splash_yaml = target_path / "flutter_native_splash.yaml"
        if not splash_yaml.exists():
            with open(splash_yaml, "w", encoding="utf-8") as f:
                f.write("""flutter_native_splash:
  color: "#FFFFFF"
  color_dark: "#121212"
  image: "assets/native_splash/native_splash.png"
  android_12:
    color: "#FFFFFF"
    color_dark: "#121212"
    image: "assets/native_splash/native_splash.png"
  fullscreen: true
  android: true
  ios: true
  web: false
""")
            print("   ✅ Created: flutter_native_splash.yaml")

    print("\n🎉 Launcher Icons & Native Splash setup completed successfully!")
    print("💡 Place your PNG artwork in assets/launcher_icon/ and assets/native_splash/")
    print("💡 Run 'make icons' and 'make splash' to generate them across platforms.")
    print("="*70 + "\n")
    return True

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "."
    setup_icons_and_splash(target)
