#!/usr/bin/env python3
"""
Universal AI Toolkit v2 — Automated Font Provisioner & Typography Engine
Provisions bundled fonts to Flutter projects, supports multi-font selection (e.g. Arabic + English + Currency),
configures pubspec.yaml fonts section directly in <project_root>/assets/fonts/,
and supports importing NEW custom fonts directly into the toolkit's persistent catalog.
Uses Python Standard Library ONLY (zero pip dependencies).
"""

import sys
import os
import re
import json
import shutil
import argparse
from pathlib import Path

# Weight detection pattern for imported fonts
WEIGHT_PATTERNS = [
    (r"(?i)(thin|hairline|w100|100)", 100),
    (r"(?i)(extralight|ultra_?light|w200|200)", 200),
    (r"(?i)(light|w300|300)", 300),
    (r"(?i)(regular|normal|book|w400|400)", 400),
    (r"(?i)(medium|w500|500)", 500),
    (r"(?i)(semibold|semi_?bold|demibold|w600|600)", 600),
    (r"(?i)(bold|w700|700)", 700),
    (r"(?i)(extrabold|extra_?bold|heavy|ultra_?bold|w800|800)", 800),
    (r"(?i)(black|w900|900)", 900),
]

def find_toolkit_root():
    """Finds the root directory of the ai_toolkit containing templates/."""
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / "templates" / "assets" / "fonts").exists():
            return current
        current = current.parent
    return None

def get_catalog_path():
    toolkit_root = find_toolkit_root()
    if not toolkit_root:
        return None
    return toolkit_root / "templates" / "assets" / "fonts" / "catalog.json"

def load_catalog():
    cat_path = get_catalog_path()
    if cat_path and cat_path.exists():
        try:
            with open(cat_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ Warning: Failed to parse catalog.json: {e}")
    return {}

def save_catalog(catalog: dict):
    cat_path = get_catalog_path()
    if not cat_path:
        print("❌ Error: Could not determine catalog path.")
        return False
    with open(cat_path, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)
    return True

def normalize_font_name(name: str, catalog: dict):
    """Normalizes noisy font names from Figma/Stitch (e.g. 'Cairo-Bold' -> 'cairo')."""
    if not name:
        return ""
    clean = re.sub(r"[-_](bold|medium|regular|light|semibold|black|thin|italic)", "", name, flags=re.IGNORECASE)
    clean = re.sub(r"[^a-zA-Z0-9]", "", clean).lower()
    for key in catalog:
        key_clean = key.replace("_", "")
        if key_clean in clean or clean in key_clean:
            return key
    return None

def detect_weight_from_filename(filename: str) -> int:
    stem = Path(filename).stem
    for pattern, weight in WEIGHT_PATTERNS:
        if re.search(pattern, stem):
            return weight
    return 400  # Default to regular if indeterminate

def import_custom_font(source_path: Path, family_name: str = None, primary_lang: str = "ar/en"):
    """Imports a local folder or font file into the toolkit's persistent font library."""
    toolkit_root = find_toolkit_root()
    if not toolkit_root:
        print("❌ Error: Could not find toolkit root.")
        sys.exit(1)

    catalog = load_catalog()

    if not source_path.exists():
        print(f"❌ Error: Source font path not found: {source_path}")
        sys.exit(1)

    # Gather font files
    if source_path.is_file():
        font_files = [source_path]
        default_name = source_path.stem
    else:
        font_files = list(source_path.glob("*.ttf")) + list(source_path.glob("*.otf"))
        default_name = source_path.name

    if not font_files:
        print(f"❌ Error: No .ttf or .otf files found in {source_path}")
        sys.exit(1)

    family = family_name.strip() if family_name else default_name.replace("-", " ").title().replace(" ", "")
    slug = re.sub(r"[^a-zA-Z0-9_]", "", family.lower().replace(" ", "_"))

    dest_dir = toolkit_root / "templates" / "assets" / "fonts" / slug
    dest_dir.mkdir(parents=True, exist_ok=True)

    weights_list = []
    seen_weights = set()

    print(f"\n📥 Importing font '{family}' into toolkit catalog ({dest_dir})...")
    for f in sorted(font_files):
        w_val = detect_weight_from_filename(f.name)
        # Avoid duplicate weights collision
        if w_val in seen_weights:
            w_val = min(900, w_val + 50)
        seen_weights.add(w_val)

        shutil.copy2(f, dest_dir / f.name)
        weights_list.append({"asset": f.name, "weight": w_val})
        print(f"  • {f.name} -> weight: {w_val}")

    default_height = 1.4 if ("ar" in primary_lang.lower()) else 1.3

    catalog[slug] = {
        "family": family,
        "dir": slug,
        "primary_language": primary_lang,
        "default_height": default_height,
        "weights": weights_list,
    }

    if save_catalog(catalog):
        print(f"\n🎉 Successfully saved '{family}' (key: '{slug}') to toolkit's font library!")
        print(f"Now you can use: python3 bin/setup/setup_fonts.py --fonts {slug} anywhere!\n")
    else:
        print("❌ Failed to update catalog.json")

def load_simple_profile(profile_path):
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
    content = pubspec_path.read_text(encoding="utf-8")
    family = font_info["family"]

    if re.search(rf"-\s+family:\s+{re.escape(family)}\b", content):
        print(f"  ℹ️ Font '{family}' already registered in pubspec.yaml.")
        return

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
        pattern = r"(  fonts:)"
        new_content = re.sub(pattern, rf"\1{yaml_block}", content, count=1)
    elif "flutter:" in content:
        new_block = "  fonts:" + yaml_block
        pattern = r"(flutter:)"
        new_content = re.sub(pattern, rf"\1\n{new_block}", content, count=1)
    else:
        new_content = content.rstrip() + f"\n\nflutter:\n  fonts:{yaml_block}\n"

    pubspec_path.write_text(new_content, encoding="utf-8")
    print(f"  ✅ Added '{family}' to fonts section in {pubspec_path.name}")

def scaffold_fonts_dart(dest_path: Path, primary_family: str, secondary_family: str = None, extra_families: list = None):
    code_lines = [
        "// Generated by Universal AI Toolkit v2 (setup_fonts.py)",
        "abstract final class AppFonts {",
        f"  static const String main = '{primary_family}';",
    ]
    if secondary_family:
        code_lines.append(f"  static const String secondary = '{secondary_family}';")

    if extra_families:
        for ef in extra_families:
            slug = re.sub(r"[^a-zA-Z0-9]", "", ef.lower())
            code_lines.append(f"  static const String {slug} = '{ef}';")

    code_lines.append("}\n")
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    dest_path.write_text("\n".join(code_lines), encoding="utf-8")
    print(f"  ✅ Scaffolding AppFonts -> {dest_path}")

def scaffold_text_styles_dart(dest_path: Path, height: float = 1.4):
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

def provision_fonts(font_keys: list, target_dir: Path, main_key: str = None):
    catalog = load_catalog()
    toolkit_root = find_toolkit_root()
    if not toolkit_root:
        print("❌ Error: Could not locate ai_toolkit root containing templates/assets/fonts/.")
        sys.exit(1)

    # Validate keys
    resolved_info = []
    for k in font_keys:
        k_clean = k.strip().lower()
        if k_clean not in catalog:
            print(f"❌ Error: Font '{k_clean}' not found in toolkit catalog.")
            print(f"Available fonts: {list(catalog.keys())}")
            print(f"💡 You can import it using: python3 bin/setup/setup_fonts.py --import /path/to/font_dir --name '{k_clean.title()}'")
            sys.exit(1)
        resolved_info.append(catalog[k_clean])

    # Resolve target project root
    curr = target_dir
    resolved_root = target_dir
    while curr != curr.parent:
        if (curr / "pubspec.yaml").exists() or (curr / "project_profile.yaml").exists():
            resolved_root = curr
            break
        curr = curr.parent
    target_dir = resolved_root

    # Destination: ALWAYS <project_root>/assets/fonts/
    dest_subpath = "assets/fonts"
    dest_font_dir = target_dir / dest_subpath
    dest_font_dir.mkdir(parents=True, exist_ok=True)

    pubspec_path = target_dir / "pubspec.yaml"

    primary_info = resolved_info[0]
    if main_key and main_key.strip().lower() in catalog:
        for info in resolved_info:
            if info["family"].lower() == catalog[main_key.strip().lower()]["family"].lower():
                primary_info = info
                break

    secondary_info = resolved_info[1] if len(resolved_info) > 1 else None
    extra_families = [info["family"] for info in resolved_info[2:]] if len(resolved_info) > 2 else None

    print(f"\n📦 Provisioning fonts to {dest_font_dir}...")
    for info in resolved_info:
        src_font_dir = toolkit_root / "templates" / "assets" / "fonts" / info["dir"]
        for w in info["weights"]:
            f_name = w["asset"]
            src_file = src_font_dir / f_name
            if src_file.exists():
                shutil.copy2(src_file, dest_font_dir / f_name)
            else:
                print(f"  ⚠️ Warning: {f_name} not found in template source.")

        if pubspec_path.exists():
            inject_pubspec_font(pubspec_path, info, dest_subpath)

    profile = load_simple_profile(target_dir / "project_profile.yaml")
    tokens_base = target_dir / profile.get("tokens_path", "lib/core/configs/values")

    scaffold_fonts_dart(
        tokens_base / "fonts.dart",
        primary_info["family"],
        secondary_info["family"] if secondary_info else None,
        extra_families,
    )
    scaffold_text_styles_dart(tokens_base / "text_styles.dart", primary_info.get("default_height", 1.4))

    print(f"\n🎉 Successfully provisioned {[info['family'] for info in resolved_info]}!\n")

def main():
    parser = argparse.ArgumentParser(description="Universal AI Toolkit v2 — Font Provisioner & Library")
    parser.add_argument("--fonts", "--font", help="Comma-separated fonts to install (e.g. cairo,inter,tajawal)")
    parser.add_argument("--main-font", help="Primary font if multiple are selected (defaults to the first)")
    parser.add_argument("--match", help="Match a raw font name from design against saved fonts catalog")
    parser.add_argument("--list", action="store_true", help="List all available fonts in toolkit catalog")
    parser.add_argument("--import", dest="import_path", help="Path to a local font folder or TTF file to register in toolkit")
    parser.add_argument("--name", help="Display/Family name when importing (e.g. 'SomarSans')")
    parser.add_argument("--lang", default="ar/en", help="Primary language when importing (ar/en, en, etc.)")
    parser.add_argument("--target", default=".", help="Target app directory (default: current)")

    args = parser.parse_args()
    catalog = load_catalog()

    if args.list:
        print("\n🔤 Saved Fonts Library in Toolkit:")
        for k, v in catalog.items():
            print(f"  • {k.ljust(14)} -> {v['family'].ljust(14)} ({v.get('primary_language', 'any')}) [{len(v.get('weights', []))} weights]")
        print()
        return

    if args.import_path:
        src = Path(args.import_path).resolve()
        import_custom_font(src, family_name=args.name, primary_lang=args.lang)
        return

    if args.match:
        matched = normalize_font_name(args.match, catalog)
        if matched:
            print(f"MATCH:{matched}:{catalog[matched]['family']}")
        else:
            print(f"NO_MATCH:{args.match}")
        return

    font_arg = args.fonts
    if font_arg:
        keys = [k.strip() for k in font_arg.split(",") if k.strip()]
        target_path = Path(args.target).resolve()
        provision_fonts(keys, target_path, main_key=args.main_font)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
