#!/usr/bin/env python3
"""
Universal AI Toolkit v2 — Automated Font Provisioner & Typography Engine
Provisions bundled fonts (Cairo, Inter, Public Sans, Roboto, Tajawal) to Flutter projects,
configures pubspec.yaml fonts section, and scaffolds AppFonts and TextStyles with the direct sized scale.
Uses Python Standard Library ONLY (zero pip dependencies).
"""

import sys
import os
import re
import shutil
import argparse
from pathlib import Path

# Supported bundled fonts catalog
BUNDLED_FONTS = {
    "cairo": {
        "family": "Cairo",
        "dir": "cairo",
        "primary_language": "ar/en",
        "weights": [
            {"asset": "Cairo-Light.ttf", "weight": 300},
            {"asset": "Cairo-Regular.ttf", "weight": 400},
            {"asset": "Cairo-Medium.ttf", "weight": 500},
            {"asset": "Cairo-SemiBold.ttf", "weight": 600},
            {"asset": "Cairo-Bold.ttf", "weight": 700},
            {"asset": "Cairo-Black.ttf", "weight": 900},
        ],
        "default_height": 1.4,
    },
    "inter": {
        "family": "Inter",
        "dir": "inter",
        "primary_language": "en",
        "weights": [
            {"asset": "Inter_18pt-Light.ttf", "weight": 300},
            {"asset": "Inter_18pt-Regular.ttf", "weight": 400},
            {"asset": "Inter_18pt-Medium.ttf", "weight": 500},
            {"asset": "Inter_18pt-SemiBold.ttf", "weight": 600},
            {"asset": "Inter_18pt-Bold.ttf", "weight": 700},
        ],
        "default_height": 1.3,
    },
    "public_sans": {
        "family": "PublicSans",
        "dir": "public_sans",
        "primary_language": "en",
        "weights": [
            {"asset": "PublicSans-Light.ttf", "weight": 300},
            {"asset": "PublicSans-Regular.ttf", "weight": 400},
            {"asset": "PublicSans-Medium.ttf", "weight": 500},
            {"asset": "PublicSans-SemiBold.ttf", "weight": 600},
            {"asset": "PublicSans-Bold.ttf", "weight": 700},
        ],
        "default_height": 1.3,
    },
    "roboto": {
        "family": "Roboto",
        "dir": "roboto",
        "primary_language": "en",
        "weights": [
            {"asset": "Roboto-Light.ttf", "weight": 300},
            {"asset": "Roboto-Regular.ttf", "weight": 400},
            {"asset": "Roboto-Medium.ttf", "weight": 500},
            {"asset": "Roboto-SemiBold.ttf", "weight": 600},
            {"asset": "Roboto-Bold.ttf", "weight": 700},
        ],
        "default_height": 1.3,
    },
    "tajawal": {
        "family": "Tajawal",
        "dir": "tajawal",
        "primary_language": "ar/en",
        "weights": [
            {"asset": "Tajawal-Light.ttf", "weight": 300},
            {"asset": "Tajawal-Regular.ttf", "weight": 400},
            {"asset": "Tajawal-Medium.ttf", "weight": 500},
            {"asset": "Tajawal-Bold.ttf", "weight": 700},
        ],
        "default_height": 1.4,
    },
}

def normalize_font_name(name: str):
    """Normalizes noisy font names from Figma/Stitch (e.g. 'Cairo-Bold' -> 'cairo')."""
    if not name:
        return ""
    clean = re.sub(r"[-_](bold|medium|regular|light|semibold|black|thin|italic)", "", name, flags=re.IGNORECASE)
    clean = re.sub(r"[^a-zA-Z0-9]", "", clean).lower()
    for key in BUNDLED_FONTS:
        key_clean = key.replace("_", "")
        if key_clean in clean or clean in key_clean:
            return key
    return None

def find_toolkit_root():
    """Finds the root directory of the ai_toolkit containing templates/."""
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / "templates" / "assets" / "fonts").exists():
            return current
        current = current.parent
    return None

def load_simple_profile(profile_path):
    """Simple parser extracting top-level keys."""
    data = {}
    if not profile_path.exists():
        return data
    with open(profile_path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            m = re.match(r"^([a-zA-Z0-9_\-]+)\s*:\s*(.*)", line)
            if m and not raw.startswith(" ") and not raw.startswith("\t"):
                k = m.group(1)
                v = m.group(2).strip().strip("'\"")
                data[k] = v
    return data

def inject_pubspec_font(pubspec_path: Path, font_info: dict, dest_subpath: str):
    """Safely updates or injects fonts block in pubspec.yaml without breaking formatting."""
    content = pubspec_path.read_text(encoding="utf-8")
    family = font_info["family"]

    # Check if family is already registered
    if re.search(rf"-\s+family:\s+{re.escape(family)}\b", content):
        print(f"  ℹ️ Font '{family}' already registered in pubspec.yaml.")
        return

    # Prepare yaml font block
    font_lines = [
        f"    - family: {family}",
        "      fonts:",
    ]
    for w in font_info["weights"]:
        asset_file = w["asset"]
        weight_val = w["weight"]
        font_lines.append(f"        - asset: {dest_subpath}/{asset_file}")
        font_lines.append(f"          weight: {weight_val}")

    yaml_block = "\n" + "\n".join(font_lines)

    if "  fonts:" in content:
        # Append under existing fonts:
        pattern = r"(  fonts:)"
        new_content = re.sub(pattern, rf"\1{yaml_block}", content, count=1)
    elif "flutter:" in content:
        # Append fonts: under flutter:
        new_block = "  fonts:" + yaml_block
        pattern = r"(flutter:)"
        new_content = re.sub(pattern, rf"\1\n{new_block}", content, count=1)
    else:
        # Add flutter: section at bottom
        new_content = content.rstrip() + f"\n\nflutter:\n  fonts:{yaml_block}\n"

    pubspec_path.write_text(new_content, encoding="utf-8")
    print(f"  ✅ Added '{family}' to fonts section in {pubspec_path.name}")

def scaffold_fonts_dart(dest_path: Path, font_family: str):
    """Generates AppFonts class."""
    code = f"""// Generated by Universal AI Toolkit v2 (setup_fonts.py)
abstract final class AppFonts {{
  static const String main = '{font_family}';
}}
"""
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    dest_path.write_text(code, encoding="utf-8")
    print(f"  ✅ Scaffolding AppFonts -> {dest_path}")

def scaffold_text_styles_dart(dest_path: Path, height: float = 1.4):
    """Generates TextStyles class using the direct sized scale."""
    code = f"""// Generated by Universal AI Toolkit v2 (setup_fonts.py)
import 'package:flutter/widgets.dart';

abstract final class TextStyles {{
  // ---------------------------------------------------------------------------
  // Light (FontWeight.w300)
  // ---------------------------------------------------------------------------
  static const TextStyle light10 = TextStyle(fontSize: 10, fontWeight: FontWeight.w300, height: {height});
  static const TextStyle light12 = TextStyle(fontSize: 12, fontWeight: FontWeight.w300, height: {height});
  static const TextStyle light14 = TextStyle(fontSize: 14, fontWeight: FontWeight.w300, height: {height});
  static const TextStyle light16 = TextStyle(fontSize: 16, fontWeight: FontWeight.w300, height: {height});

  // ---------------------------------------------------------------------------
  // Regular (FontWeight.w400)
  // ---------------------------------------------------------------------------
  static const TextStyle regular10 = TextStyle(fontSize: 10, fontWeight: FontWeight.w400, height: {height});
  static const TextStyle regular12 = TextStyle(fontSize: 12, fontWeight: FontWeight.w400, height: {height});
  static const TextStyle regular14 = TextStyle(fontSize: 14, fontWeight: FontWeight.w400, height: {height});
  static const TextStyle regular16 = TextStyle(fontSize: 16, fontWeight: FontWeight.w400, height: {height});
  static const TextStyle regular18 = TextStyle(fontSize: 18, fontWeight: FontWeight.w400, height: {height});
  static const TextStyle regular20 = TextStyle(fontSize: 20, fontWeight: FontWeight.w400, height: {height});
  static const TextStyle regular24 = TextStyle(fontSize: 24, fontWeight: FontWeight.w400, height: {height});

  // ---------------------------------------------------------------------------
  // Medium (FontWeight.w500)
  // ---------------------------------------------------------------------------
  static const TextStyle medium12 = TextStyle(fontSize: 12, fontWeight: FontWeight.w500, height: {height});
  static const TextStyle medium14 = TextStyle(fontSize: 14, fontWeight: FontWeight.w500, height: {height});
  static const TextStyle medium16 = TextStyle(fontSize: 16, fontWeight: FontWeight.w500, height: {height});
  static const TextStyle medium18 = TextStyle(fontSize: 18, fontWeight: FontWeight.w500, height: {height});
  static const TextStyle medium20 = TextStyle(fontSize: 20, fontWeight: FontWeight.w500, height: {height});

  // ---------------------------------------------------------------------------
  // SemiBold (FontWeight.w600)
  // ---------------------------------------------------------------------------
  static const TextStyle semiBold12 = TextStyle(fontSize: 12, fontWeight: FontWeight.w600, height: {height});
  static const TextStyle semiBold14 = TextStyle(fontSize: 14, fontWeight: FontWeight.w600, height: {height});
  static const TextStyle semiBold16 = TextStyle(fontSize: 16, fontWeight: FontWeight.w600, height: {height});
  static const TextStyle semiBold18 = TextStyle(fontSize: 18, fontWeight: FontWeight.w600, height: {height});
  static const TextStyle semiBold20 = TextStyle(fontSize: 20, fontWeight: FontWeight.w600, height: {height});
  static const TextStyle semiBold24 = TextStyle(fontSize: 24, fontWeight: FontWeight.w600, height: {height});

  // ---------------------------------------------------------------------------
  // Bold (FontWeight.w700)
  // ---------------------------------------------------------------------------
  static const TextStyle bold14 = TextStyle(fontSize: 14, fontWeight: FontWeight.w700, height: {height});
  static const TextStyle bold16 = TextStyle(fontSize: 16, fontWeight: FontWeight.w700, height: {height});
  static const TextStyle bold18 = TextStyle(fontSize: 18, fontWeight: FontWeight.w700, height: {height});
  static const TextStyle bold20 = TextStyle(fontSize: 20, fontWeight: FontWeight.w700, height: {height});
  static const TextStyle bold24 = TextStyle(fontSize: 24, fontWeight: FontWeight.w700, height: {height});
  static const TextStyle bold32 = TextStyle(fontSize: 32, fontWeight: FontWeight.w700, height: {height});
}}
"""
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    dest_path.write_text(code, encoding="utf-8")
    print(f"  ✅ Scaffolding TextStyles (direct scale) -> {dest_path}")

def provision_font(font_key: str, target_dir: Path):
    if font_key not in BUNDLED_FONTS:
        print(f"❌ Error: Font '{font_key}' is not available in bundled fonts catalog.")
        print(f"Available fonts: {list(BUNDLED_FONTS.keys())}")
        sys.exit(1)

    font_info = BUNDLED_FONTS[font_key]
    toolkit_root = find_toolkit_root()
    if not toolkit_root:
        print("❌ Error: Could not locate ai_toolkit root containing templates/assets/fonts/.")
        sys.exit(1)

    src_font_dir = toolkit_root / "templates" / "assets" / "fonts" / font_info["dir"]
    if not src_font_dir.exists():
        print(f"❌ Error: Source font directory not found: {src_font_dir}")
        sys.exit(1)

    # Destination in app
    dest_subpath = f"assets/fonts/{font_info['dir']}"
    dest_font_dir = target_dir / dest_subpath
    dest_font_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n📦 Copying {font_info['family']} font files to {dest_font_dir}...")
    for w in font_info["weights"]:
        f_name = w["asset"]
        src_file = src_font_dir / f_name
        if src_file.exists():
            shutil.copy2(src_file, dest_font_dir / f_name)
        else:
            print(f"  ⚠️ Warning: {f_name} not found in template source.")

    # Update pubspec.yaml
    pubspec_path = target_dir / "pubspec.yaml"
    if pubspec_path.exists():
        inject_pubspec_font(pubspec_path, font_info, dest_subpath)
    else:
        print(f"  ⚠️ pubspec.yaml not found at {pubspec_path}, skipped font injection.")

    # Determine token paths
    profile = load_simple_profile(target_dir / "project_profile.yaml")
    tokens_base = target_dir / profile.get("tokens_path", "lib/core/configs/values")

    scaffold_fonts_dart(tokens_base / "fonts.dart", font_info["family"])
    scaffold_text_styles_dart(tokens_base / "text_styles.dart", font_info["default_height"])

    print(f"\n🎉 Font '{font_info['family']}' setup complete!\n")

def main():
    parser = argparse.ArgumentParser(description="Universal AI Toolkit v2 — Font Provisioner")
    parser.add_argument("--font", help="Bundled font key to install (cairo, inter, public_sans, roboto, tajawal)")
    parser.add_argument("--match", help="Match a raw font name from design against bundled fonts")
    parser.add_argument("--list", action="store_true", help="List all available bundled fonts")
    parser.add_argument("--target", default=".", help="Target app directory (default: current)")

    args = parser.parse_args()

    if args.list:
        print("\n🔤 Available Bundled Fonts in Toolkit:")
        for k, v in BUNDLED_FONTS.items():
            print(f"  • {k.ljust(12)} -> {v['family']} ({v['primary_language']})")
        print()
        return

    if args.match:
        matched = normalize_font_name(args.match)
        if matched:
            print(f"MATCH:{matched}:{BUNDLED_FONTS[matched]['family']}")
        else:
            print(f"NO_MATCH:{args.match}")
        return

    if args.font:
        target_path = Path(args.target).resolve()
        provision_font(args.font.lower().strip(), target_path)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
