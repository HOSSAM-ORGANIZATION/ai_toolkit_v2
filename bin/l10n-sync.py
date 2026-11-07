#!/usr/bin/env python3
"""
Universal AI Toolkit v2 — Universal Localization Synchronizer
Adds keys and messages across ARB, JSON, and Slang translation files.
Standard library ONLY.
"""

import sys
import os
import json
import argparse
import subprocess
from pathlib import Path

def add_arb_key(arb_dir, key, en_text, ar_text, run_gen=True):
    en_file = Path(arb_dir) / "app_en.arb"
    ar_file = Path(arb_dir) / "app_ar.arb"

    if not en_file.exists() or not ar_file.exists():
        print(f"⚠️ ARB files not found in {arb_dir}. Checking for *.arb...")
        arbs = list(Path(arb_dir).glob("*.arb"))
        if not arbs:
            print(f"❌ No ARB files located in {arb_dir}.")
            return False

    # Read and update English ARB
    with open(en_file, "r", encoding="utf-8") as f:
        en_data = json.load(f)
    en_data[key] = en_text
    with open(en_file, "w", encoding="utf-8") as f:
        json.dump(en_data, f, ensure_ascii=False, indent=2)
    print(f"✅ Added '{key}': '{en_text}' -> {en_file.name}")

    # Read and update Arabic ARB
    with open(ar_file, "r", encoding="utf-8") as f:
        ar_data = json.load(f)
    ar_data[key] = ar_text
    with open(ar_file, "w", encoding="utf-8") as f:
        json.dump(ar_data, f, ensure_ascii=False, indent=2)
    print(f"✅ Added '{key}': '{ar_text}' -> {ar_file.name}")

    if run_gen:
        print("⚙️ Running flutter gen-l10n...")
        try:
            subprocess.run(["flutter", "gen-l10n"], check=True)
            print("🎉 flutter gen-l10n completed successfully!")
        except Exception as e:
            print(f"⚠️ flutter gen-l10n failed or not installed in PATH: {e}")

    return True

def add_json_key(json_dir, key, en_text, ar_text):
    en_file = Path(json_dir) / "en.json"
    ar_file = Path(json_dir) / "ar.json"

    for file_path, text in [(en_file, en_text), (ar_file, ar_text)]:
        if not file_path.exists():
            data = {}
        else:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        data[key] = text
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ Added '{key}': '{text}' -> {file_path.name}")
    return True

def main():
    parser = argparse.ArgumentParser(description="Universal AI Toolkit Localization Synchronizer")
    parser.add_argument("--key", required=True, help="Message key (camelCase)")
    parser.add_argument("--en", required=True, help="English translation string")
    parser.add_argument("--ar", required=True, help="Arabic translation string")
    parser.add_argument("--type", choices=["arb", "json"], default="arb", help="Localization engine format")
    parser.add_argument("--dir", default="lib/core/localization/l10n", help="Directory holding translation files")
    parser.add_argument("--no-gen", action="store_true", help="Skip flutter gen-l10n")
    args = parser.parse_args()

    if args.type == "arb":
        add_arb_key(args.dir, args.key, args.en, args.ar, run_gen=not args.no_gen)
    else:
        add_json_key(args.dir, args.key, args.en, args.ar)

if __name__ == "__main__":
    main()
