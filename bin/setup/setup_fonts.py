#!/usr/bin/env python3
"""
Universal AI Toolkit v2 — Automated Font Provisioner & Typography Engine
Provisions fonts (bundled or custom) directly into Flutter projects:
- Copies TTF/OTF directly to <project_root>/assets/fonts/
- Strictly adheres to Flutter Docs & Alzoq Alraqi pubspec.yaml layout order:
    flutter:
      uses-material-design: true
      assets:
        - assets/images/
        ...
      fonts:
        - family: Cairo
          fonts: (expanded 100..900 ladder)
- Safely auto-reorders and fixes broken or misplaced sections in pubspec.yaml
- Scaffolds AppFonts and TextStyles with the direct sized scale (light8..bold32)
- Automatically updates Project Memory & Living Docs (ai_docs/memory.md, conventions.md, project_profile.yaml, README.md)
Uses Python Standard Library ONLY (zero pip dependencies).
"""

import sys
import os
import re
import json
import shutil
import argparse
from pathlib import Path

# Weight detection pattern for custom imported fonts
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

def normalize_font_name(name: str, catalog: dict):
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
    return 400

def expand_weights_ladder(weights: list) -> list:
    """
    Expands weights list to cover the full 100..900 ladder
    by mapping each step to the closest available asset file (exact Alzoq Alraqi pattern).
    """
    if not weights:
        return []
    if len(weights) == 1:
        # Icon / Symbol font
        return weights

    by_weight = {w["weight"]: w["asset"] for w in weights}
    available = sorted(by_weight.keys())
    ladder = []
    for tw in [100, 200, 300, 400, 500, 600, 700, 800, 900]:
        closest = min(available, key=lambda w: abs(w - tw))
        ladder.append({"asset": by_weight[closest], "weight": tw})
    return ladder

def resolve_project_root(target_dir: Path) -> Path:
    curr = target_dir.resolve()
    while curr != curr.parent:
        if (curr / "pubspec.yaml").exists() or (curr / "project_profile.yaml").exists():
            return curr
        curr = curr.parent
    return target_dir.resolve()

def load_simple_profile(profile_path: Path):
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

def detect_part_of_core(tokens_base: Path) -> bool:
    """Checks if the project uses monolithic 'part of core;' architecture (like Alzoq Alraqi)."""
    search_dirs = [tokens_base, tokens_base.parent, tokens_base.parent.parent]
    for d in search_dirs:
        if d.exists():
            for f in d.glob("*.dart"):
                try:
                    head = f.read_text(encoding="utf-8")[:300]
                    if re.search(r"^\s*part\s+of\s+core\s*;", head, re.MULTILINE):
                        return True
                except Exception:
                    pass
    return False

def reorder_flutter_section(content: str) -> str:
    """
    Ensures pubspec.yaml flutter: block strictly follows the canonical Flutter docs & Alzoq Alraqi order:
      1. uses-material-design: true / generate: true
      2. assets:
      3. fonts:
    Auto-corrects if fonts: was mistakenly placed before assets: or before uses-material-design:.
    """
    m = re.search(r"^flutter:\s*$", content, re.MULTILINE)
    if not m:
        return content

    flutter_start = m.start()
    rest = content[m.end():]
    next_key_m = re.search(r"^[a-zA-Z0-9_\-]+:", rest, re.MULTILINE)
    flutter_end = m.end() + next_key_m.start() if next_key_m else len(content)

    flutter_body = content[m.end():flutter_end]

    assets_m = re.search(r"^  assets:\s*$", flutter_body, re.MULTILINE)
    fonts_m = re.search(r"^  fonts:\s*$", flutter_body, re.MULTILINE)

    # If fonts: is placed before assets:, we swap and reorder them
    if assets_m and fonts_m and fonts_m.start() < assets_m.start():
        f_start = fonts_m.start()
        next_after_fonts = re.search(r"^  [a-zA-Z0-9_\-]+:\s*", flutter_body[fonts_m.end():], re.MULTILINE)
        f_end = fonts_m.end() + next_after_fonts.start() if next_after_fonts else len(flutter_body)
        fonts_block = flutter_body[f_start:f_end].strip()

        new_body = flutter_body[:f_start] + flutter_body[f_end:]

        a_m = re.search(r"^  assets:\s*$", new_body, re.MULTILINE)
        next_after_assets = re.search(r"^  [a-zA-Z0-9_\-]+:\s*", new_body[a_m.end():], re.MULTILINE)
        a_end = a_m.end() + next_after_assets.start() if next_after_assets else len(new_body)

        new_body = new_body[:a_end].rstrip() + "\n\n  " + fonts_block.lstrip() + "\n\n" + new_body[a_end:].lstrip()
        return content[:m.end()] + new_body + content[flutter_end:]

    return content

def build_font_yaml_entry(family: str, weights: list, dest_subpath: str) -> str:
    expanded = expand_weights_ladder(weights)
    lines = [
        f"    - family: {family}",
        "      fonts:",
    ]
    for w in expanded:
        asset_file = w["asset"]
        w_val = w.get("weight", 400)
        lines.append(f"        - asset: {dest_subpath}/{asset_file}")
        lines.append(f"          weight: {w_val}")
    return "\n".join(lines)

def inject_pubspec_font(pubspec_path: Path, family: str, weights_list: list, dest_subpath: str, project_root: Path):
    content = pubspec_path.read_text(encoding="utf-8")

    # 1. First reorder any existing out-of-order flutter: section
    content = reorder_flutter_section(content)

    # 2. Check if family is already registered
    if re.search(rf"-\s+family:\s+{re.escape(family)}\b", content):
        print(f"  ℹ️ Font '{family}' already registered in pubspec.yaml.")
        pubspec_path.write_text(content, encoding="utf-8")
        return

    font_entry = build_font_yaml_entry(family, weights_list, dest_subpath)
    lines = content.splitlines()

    # Find flutter: line
    flutter_idx = -1
    for i, line in enumerate(lines):
        if re.match(r"^flutter:\s*$", line):
            flutter_idx = i
            break

    if flutter_idx == -1:
        # No flutter: section, append canonically formatted flutter block
        new_content = content.rstrip() + f"\n\nflutter:\n  uses-material-design: true\n\n  fonts:\n{font_entry}\n"
        pubspec_path.write_text(new_content, encoding="utf-8")
        print(f"  ✅ Added flutter and fonts section with '{family}' to {pubspec_path.name}")
        return

    # Find where flutter: section ends
    flutter_end_idx = len(lines)
    for i in range(flutter_idx + 1, len(lines)):
        l = lines[i]
        if l.strip() and not l.startswith(" ") and not l.startswith("\t") and not l.startswith("#"):
            flutter_end_idx = i
            break

    flutter_lines = lines[flutter_idx:flutter_end_idx]

    # Check if uncommented "  fonts:" exists
    fonts_rel_idx = -1
    for i, l in enumerate(flutter_lines):
        if re.match(r"^  fonts:\s*$", l):
            fonts_rel_idx = i
            break

    if fonts_rel_idx != -1:
        # fonts: exists! Find the end of existing fonts: block to append cleanly
        insert_rel_idx = len(flutter_lines)
        for i in range(fonts_rel_idx + 1, len(flutter_lines)):
            l = flutter_lines[i]
            if re.match(r"^  [a-zA-Z0-9_\-]+:\s*", l):
                insert_rel_idx = i
                break

        abs_insert_idx = flutter_idx + insert_rel_idx
        while abs_insert_idx > flutter_idx + fonts_rel_idx + 1 and not lines[abs_insert_idx - 1].strip():
            abs_insert_idx -= 1

        font_lines_to_add = [""] + [line for line in font_entry.splitlines() if line.strip()]
        lines[abs_insert_idx:abs_insert_idx] = font_lines_to_add
        updated_content = "\n".join(lines) + "\n"
        pubspec_path.write_text(reorder_flutter_section(updated_content), encoding="utf-8")
        print(f"  ✅ Appended '{family}' to fonts section in {pubspec_path.name}")
        return

    # fonts: does NOT exist! Check if "  assets:" exists
    assets_rel_idx = -1
    for i, l in enumerate(flutter_lines):
        if re.match(r"^  assets:\s*$", l):
            assets_rel_idx = i
            break

    if assets_rel_idx != -1:
        # assets: exists! Place fonts: directly AFTER assets: block
        insert_rel_idx = len(flutter_lines)
        for i in range(assets_rel_idx + 1, len(flutter_lines)):
            l = flutter_lines[i]
            if re.match(r"^  [a-zA-Z0-9_\-]+:\s*", l):
                insert_rel_idx = i
                break

        abs_insert_idx = flutter_idx + insert_rel_idx
        while abs_insert_idx > flutter_idx + assets_rel_idx + 1 and not lines[abs_insert_idx - 1].strip():
            abs_insert_idx -= 1

        block_to_insert = ["", "  fonts:"] + [line for line in font_entry.splitlines() if line.strip()]
        lines[abs_insert_idx:abs_insert_idx] = block_to_insert
        updated_content = "\n".join(lines) + "\n"
        pubspec_path.write_text(reorder_flutter_section(updated_content), encoding="utf-8")
        print(f"  ✅ Added fonts section with '{family}' (placed after assets:) in {pubspec_path.name}")
        return

    # Neither fonts: nor assets: exists
    # Place after uses-material-design: true
    mat_rel_idx = -1
    for i, l in enumerate(flutter_lines):
        if "uses-material-design:" in l:
            mat_rel_idx = i
            break

    if mat_rel_idx != -1:
        abs_insert_idx = flutter_idx + mat_rel_idx + 1
    else:
        abs_insert_idx = flutter_end_idx

    block_to_insert = ["", "  fonts:"] + [line for line in font_entry.splitlines() if line.strip()]
    lines[abs_insert_idx:abs_insert_idx] = block_to_insert
    updated_content = "\n".join(lines) + "\n"
    pubspec_path.write_text(reorder_flutter_section(updated_content), encoding="utf-8")
    print(f"  ✅ Added fonts section with '{family}' in {pubspec_path.name}")

def scaffold_fonts_dart(dest_path: Path, primary_family: str, secondary_family: str = None, extra_families: list = None, is_part_of_core: bool = False):
    code_lines = []
    if is_part_of_core:
        code_lines.append("part of core;\n")
        code_lines.append("abstract class AppFonts {")
        code_lines.append("  const AppFonts._();")
    else:
        code_lines.append("// Generated by Universal AI Toolkit v2 (setup_fonts.py)")
        code_lines.append("abstract final class AppFonts {")

    primary_slug = re.sub(r"[^a-zA-Z0-9]", "", primary_family)
    primary_var = primary_slug[0].lower() + primary_slug[1:] if primary_slug else "main"

    code_lines.append(f"  static const String main = '{primary_family}';")
    code_lines.append(f"  static const String {primary_var} = '{primary_family}';")

    if secondary_family:
        sec_slug = re.sub(r"[^a-zA-Z0-9]", "", secondary_family)
        sec_var = sec_slug[0].lower() + sec_slug[1:] if sec_slug else "secondary"
        code_lines.append(f"  static const String secondary = '{secondary_family}';")
        code_lines.append(f"  static const String {sec_var} = '{secondary_family}';")

    if extra_families:
        for ef in extra_families:
            ef_slug = re.sub(r"[^a-zA-Z0-9]", "", ef)
            ef_var = ef_slug[0].lower() + ef_slug[1:] if ef_slug else "extra"
            code_lines.append(f"  static const String {ef_var} = '{ef}';")

    code_lines.append("}\n")
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    dest_path.write_text("\n".join(code_lines), encoding="utf-8")
    print(f"  ✅ Scaffolding AppFonts -> {dest_path}")

def scaffold_text_styles_dart(dest_path: Path, height: float = 1.4, is_part_of_core: bool = False):
    header = ""
    class_def = ""
    if is_part_of_core:
        header = "part of core;\n"
        class_def = """abstract class TextStyles {
  const TextStyles._();
  static const String _fontFamily = AppFonts.main;
"""
    else:
        header = """// Generated by Universal AI Toolkit v2 (setup_fonts.py)
import 'package:flutter/widgets.dart';
import 'fonts.dart';
"""
        class_def = """abstract final class TextStyles {
  static const String _fontFamily = AppFonts.main;
"""

    body = f"""  // ---------------------------------------------------------------------------
  // Light (FontWeight.w300)
  // ---------------------------------------------------------------------------
  static const TextStyle light8 = TextStyle(fontSize: 8, fontWeight: FontWeight.w300, fontFamily: _fontFamily, height: {height});
  static const TextStyle light10 = TextStyle(fontSize: 10, fontWeight: FontWeight.w300, fontFamily: _fontFamily, height: {height});
  static const TextStyle light12 = TextStyle(fontSize: 12, fontWeight: FontWeight.w300, fontFamily: _fontFamily, height: {height});
  static const TextStyle light14 = TextStyle(fontSize: 14, fontWeight: FontWeight.w300, fontFamily: _fontFamily, height: {height});
  static const TextStyle light16 = TextStyle(fontSize: 16, fontWeight: FontWeight.w300, fontFamily: _fontFamily, height: {height});

  // ---------------------------------------------------------------------------
  // Regular (FontWeight.w400)
  // ---------------------------------------------------------------------------
  static const TextStyle regular8 = TextStyle(fontSize: 8, fontWeight: FontWeight.w400, fontFamily: _fontFamily, height: {height});
  static const TextStyle regular10 = TextStyle(fontSize: 10, fontWeight: FontWeight.w400, fontFamily: _fontFamily, height: {height});
  static const TextStyle regular12 = TextStyle(fontSize: 12, fontWeight: FontWeight.w400, fontFamily: _fontFamily, height: {height});
  static const TextStyle regular13 = TextStyle(fontSize: 13, fontWeight: FontWeight.w400, fontFamily: _fontFamily, height: {height});
  static const TextStyle regular14 = TextStyle(fontSize: 14, fontWeight: FontWeight.w400, fontFamily: _fontFamily, height: {height});
  static const TextStyle regular15 = TextStyle(fontSize: 15, fontWeight: FontWeight.w400, fontFamily: _fontFamily, height: {height});
  static const TextStyle regular16 = TextStyle(fontSize: 16, fontWeight: FontWeight.w400, fontFamily: _fontFamily, height: {height});
  static const TextStyle regular18 = TextStyle(fontSize: 18, fontWeight: FontWeight.w400, fontFamily: _fontFamily, height: {height});
  static const TextStyle regular20 = TextStyle(fontSize: 20, fontWeight: FontWeight.w400, fontFamily: _fontFamily, height: {height});
  static const TextStyle regular24 = TextStyle(fontSize: 24, fontWeight: FontWeight.w400, fontFamily: _fontFamily, height: {height});

  // ---------------------------------------------------------------------------
  // Medium (FontWeight.w500)
  // ---------------------------------------------------------------------------
  static const TextStyle medium10 = TextStyle(fontSize: 10, fontWeight: FontWeight.w500, fontFamily: _fontFamily, height: {height});
  static const TextStyle medium12 = TextStyle(fontSize: 12, fontWeight: FontWeight.w500, fontFamily: _fontFamily, height: {height});
  static const TextStyle medium13 = TextStyle(fontSize: 13, fontWeight: FontWeight.w500, fontFamily: _fontFamily, height: {height});
  static const TextStyle medium14 = TextStyle(fontSize: 14, fontWeight: FontWeight.w500, fontFamily: _fontFamily, height: {height});
  static const TextStyle medium15 = TextStyle(fontSize: 15, fontWeight: FontWeight.w500, fontFamily: _fontFamily, height: {height});
  static const TextStyle medium16 = TextStyle(fontSize: 16, fontWeight: FontWeight.w500, fontFamily: _fontFamily, height: {height});
  static const TextStyle medium18 = TextStyle(fontSize: 18, fontWeight: FontWeight.w500, fontFamily: _fontFamily, height: {height});
  static const TextStyle medium20 = TextStyle(fontSize: 20, fontWeight: FontWeight.w500, fontFamily: _fontFamily, height: {height});
  static const TextStyle medium24 = TextStyle(fontSize: 24, fontWeight: FontWeight.w500, fontFamily: _fontFamily, height: {height});
  static const TextStyle medium32 = TextStyle(fontSize: 32, fontWeight: FontWeight.w500, fontFamily: _fontFamily, height: {height});

  // ---------------------------------------------------------------------------
  // SemiBold (FontWeight.w600)
  // ---------------------------------------------------------------------------
  static const TextStyle semiBold10 = TextStyle(fontSize: 10, fontWeight: FontWeight.w600, fontFamily: _fontFamily, height: {height});
  static const TextStyle semiBold12 = TextStyle(fontSize: 12, fontWeight: FontWeight.w600, fontFamily: _fontFamily, height: {height});
  static const TextStyle semiBold14 = TextStyle(fontSize: 14, fontWeight: FontWeight.w600, fontFamily: _fontFamily, height: {height});
  static const TextStyle semiBold16 = TextStyle(fontSize: 16, fontWeight: FontWeight.w600, fontFamily: _fontFamily, height: {height});
  static const TextStyle semiBold18 = TextStyle(fontSize: 18, fontWeight: FontWeight.w600, fontFamily: _fontFamily, height: {height});
  static const TextStyle semiBold20 = TextStyle(fontSize: 20, fontWeight: FontWeight.w600, fontFamily: _fontFamily, height: {height});
  static const TextStyle semiBold24 = TextStyle(fontSize: 24, fontWeight: FontWeight.w600, fontFamily: _fontFamily, height: {height});

  // ---------------------------------------------------------------------------
  // Bold (FontWeight.w700)
  // ---------------------------------------------------------------------------
  static const TextStyle bold10 = TextStyle(fontSize: 10, fontWeight: FontWeight.w700, fontFamily: _fontFamily, height: {height});
  static const TextStyle bold12 = TextStyle(fontSize: 12, fontWeight: FontWeight.w700, fontFamily: _fontFamily, height: {height});
  static const TextStyle bold14 = TextStyle(fontSize: 14, fontWeight: FontWeight.w700, fontFamily: _fontFamily, height: {height});
  static const TextStyle bold16 = TextStyle(fontSize: 16, fontWeight: FontWeight.w700, fontFamily: _fontFamily, height: {height});
  static const TextStyle bold18 = TextStyle(fontSize: 18, fontWeight: FontWeight.w700, fontFamily: _fontFamily, height: {height});
  static const TextStyle bold20 = TextStyle(fontSize: 20, fontWeight: FontWeight.w700, fontFamily: _fontFamily, height: {height});
  static const TextStyle bold24 = TextStyle(fontSize: 24, fontWeight: FontWeight.w700, fontFamily: _fontFamily, height: {height});
  static const TextStyle bold32 = TextStyle(fontSize: 32, fontWeight: FontWeight.w700, fontFamily: _fontFamily, height: {height});
}}
"""
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    dest_path.write_text(header + class_def + body, encoding="utf-8")
    print(f"  ✅ Scaffolding TextStyles (direct scale light8..bold32) -> {dest_path}")

def update_project_docs(target_dir: Path, primary_family: str, secondary_family: str = None):
    # 1. Update project_profile.yaml
    profile_path = target_dir / "project_profile.yaml"
    if profile_path.exists():
        text = profile_path.read_text(encoding="utf-8")
        if "primary_font:" in text:
            text = re.sub(r'primary_font:\s*["\']?[^"\n\r]+["\']?', f'primary_font: "{primary_family}"', text)
        elif "design_system:" in text:
            text = re.sub(r"(design_system:)", rf'\1\n  primary_font: "{primary_family}"', text, count=1)
        profile_path.write_text(text, encoding="utf-8")
        print(f"  📝 Updated project_profile.yaml (primary_font: {primary_family})")

    # 2. Update ai_docs/memory.md
    memory_path = target_dir / "ai_docs" / "memory.md"
    if memory_path.exists():
        text = memory_path.read_text(encoding="utf-8")
        font_row = f"| **Primary Font** | `{primary_family}` (Direct scale, assets/fonts/) |"
        if "| **Primary Font** |" in text:
            text = re.sub(r"\|\s*\*\*Primary Font\*\*.*\|", font_row, text)
        elif "## 1. Quick Technical Constraints" in text:
            text = re.sub(r"(\|\s*\*\*Testing Gate\*\*.*\|)", rf"\1\n{font_row}", text, count=1)
        memory_path.write_text(text, encoding="utf-8")
        print(f"  🧠 Updated ai_docs/memory.md with font technical constraint")

    # 3. Update ai_docs/conventions.md
    conv_path = target_dir / "ai_docs" / "conventions.md"
    if conv_path.exists():
        text = conv_path.read_text(encoding="utf-8")
        if "Typography:" in text:
            text = re.sub(r"- \*\*Typography:\*\*.*", f"- **Typography:** `TextStyles` direct scale using `{primary_family}` (`assets/fonts/`)", text)
            conv_path.write_text(text, encoding="utf-8")
            print(f"  📐 Updated ai_docs/conventions.md typography conventions")

    # 4. Update DESIGN_SYSTEM.md if exists
    ds_path = target_dir / "ai_specs" / "design" / "DESIGN_SYSTEM.md"
    if ds_path.exists():
        text = ds_path.read_text(encoding="utf-8")
        if "## Typography" in text and primary_family not in text:
            text = re.sub(r"(## Typography)", rf"\1\n- Primary Font Family: {primary_family} (Direct Scale)\n", text, count=1)
            ds_path.write_text(text, encoding="utf-8")
            print(f"  🎨 Updated ai_specs/design/DESIGN_SYSTEM.md")

    # 5. Update README.md if contains Typography section
    readme_path = target_dir / "README.md"
    if readme_path.exists():
        text = readme_path.read_text(encoding="utf-8")
        if "### Typography" in text or "## Typography" in text:
            text = re.sub(r"(##+ Typography[^\n]*\n)", rf"\1- Font: **{primary_family}** (configured in `pubspec.yaml` & `AppFonts`)\n", text, count=1)
            readme_path.write_text(text, encoding="utf-8")
            print(f"  📖 Updated README.md typography reference")

def provision_bundled_fonts(font_keys: list, target_dir: Path, main_key: str = None):
    catalog = load_catalog()
    toolkit_root = find_toolkit_root()
    if not toolkit_root:
        print("❌ Error: Could not locate ai_toolkit root containing templates/assets/fonts/.")
        sys.exit(1)

    target_dir = resolve_project_root(target_dir)

    resolved_info = []
    for k in font_keys:
        k_clean = k.strip().lower()
        if k_clean not in catalog:
            print(f"❌ Error: Font '{k_clean}' not found in toolkit catalog.")
            print(f"Available fonts: {list(catalog.keys())}")
            print(f"💡 To supply a custom font directly to this project, use:\n   ./toolkit fonts --custom-font /path/to/fonts_folder --name '{k_clean.title()}'")
            sys.exit(1)
        resolved_info.append(catalog[k_clean])

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
            inject_pubspec_font(pubspec_path, info["family"], info["weights"], dest_subpath, target_dir)

    profile = load_simple_profile(target_dir / "project_profile.yaml")
    tokens_base = target_dir / profile.get("tokens_path", "lib/core/configs/values")

    is_part_of_core = detect_part_of_core(tokens_base)

    scaffold_fonts_dart(
        tokens_base / "fonts.dart",
        primary_info["family"],
        secondary_info["family"] if secondary_info else None,
        extra_families,
        is_part_of_core=is_part_of_core,
    )
    scaffold_text_styles_dart(
        tokens_base / "text_styles.dart",
        primary_info.get("default_height", 1.4),
        is_part_of_core=is_part_of_core,
    )
    update_project_docs(target_dir, primary_info["family"], secondary_info["family"] if secondary_info else None)

    print(f"\n🎉 Successfully provisioned {[info['family'] for info in resolved_info]} and updated project memory!\n")

def provision_custom_font(source_path: Path, target_dir: Path, family_name: str = None, lang: str = "ar/en"):
    target_dir = resolve_project_root(target_dir)

    if not source_path.exists():
        print(f"❌ Error: Custom font path not found: {source_path}")
        sys.exit(1)

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

    dest_subpath = "assets/fonts"
    dest_font_dir = target_dir / dest_subpath
    dest_font_dir.mkdir(parents=True, exist_ok=True)

    weights_list = []
    seen_weights = set()

    print(f"\n📦 Adding custom font '{family}' to project ({dest_font_dir})...")
    for f in sorted(font_files):
        w_val = detect_weight_from_filename(f.name)
        if w_val in seen_weights:
            w_val = min(900, w_val + 50)
        seen_weights.add(w_val)

        shutil.copy2(f, dest_font_dir / f.name)
        weights_list.append({"asset": f.name, "weight": w_val})
        print(f"  • {f.name} (weight: {w_val}) -> assets/fonts/{f.name}")

    pubspec_path = target_dir / "pubspec.yaml"
    if pubspec_path.exists():
        inject_pubspec_font(pubspec_path, family, weights_list, dest_subpath, target_dir)

    profile = load_simple_profile(target_dir / "project_profile.yaml")
    tokens_base = target_dir / profile.get("tokens_path", "lib/core/configs/values")

    is_part_of_core = detect_part_of_core(tokens_base)

    default_height = 1.4 if ("ar" in lang.lower()) else 1.3
    scaffold_fonts_dart(tokens_base / "fonts.dart", family, is_part_of_core=is_part_of_core)
    scaffold_text_styles_dart(tokens_base / "text_styles.dart", default_height, is_part_of_core=is_part_of_core)

    update_project_docs(target_dir, family)

    print(f"\n🎉 Custom font '{family}' successfully configured in project and synced with Living Memory!\n")

def main():
    parser = argparse.ArgumentParser(description="Universal AI Toolkit v2 — Project Font Provisioner & Memory Engine")
    parser.add_argument("--fonts", "--font", help="Comma-separated bundled fonts (e.g. cairo,inter,tajawal)")
    parser.add_argument("--main-font", help="Primary font if multiple bundled are selected")
    parser.add_argument("--custom-font", dest="custom_font_path", help="Path to local folder/file of a custom font to add to the PROJECT")
    parser.add_argument("--name", help="Display/Family name for the custom font (e.g. 'SomarSans')")
    parser.add_argument("--lang", default="ar/en", help="Language for custom font (ar/en, en, etc.)")
    parser.add_argument("--match", help="Match a raw font name from design against saved fonts catalog")
    parser.add_argument("--list", action="store_true", help="List all bundled fonts in toolkit")
    parser.add_argument("--target", default=".", help="Target Flutter project directory (default: current)")

    args = parser.parse_args()
    catalog = load_catalog()

    if args.list:
        print("\n🔤 Bundled Starter Fonts in Toolkit:")
        for k, v in catalog.items():
            print(f"  • {k.ljust(14)} -> {v['family'].ljust(14)} ({v.get('primary_language', 'any')}) [{len(v.get('weights', []))} weights]")
        print()
        return

    if args.match:
        matched = normalize_font_name(args.match, catalog)
        if matched:
            print(f"MATCH:{matched}:{catalog[matched]['family']}")
        else:
            print(f"NO_MATCH:{args.match}")
        return

    target_path = Path(args.target).resolve()

    if args.custom_font_path:
        src = Path(args.custom_font_path).resolve()
        provision_custom_font(src, target_path, family_name=args.name, lang=args.lang)
        return

    if args.fonts:
        keys = [k.strip() for k in args.fonts.split(",") if k.strip()]
        provision_bundled_fonts(keys, target_path, main_key=args.main_font)
        return

    parser.print_help()

if __name__ == "__main__":
    main()
