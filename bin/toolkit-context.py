#!/usr/bin/env python3
"""
Universal AI Toolkit v2 — Context Budget Calculator
Measures resolved token size for feature plans and LOADMAP tags.
Standard library ONLY.
"""

import sys
import os
import re
from pathlib import Path

def estimate_tokens(byte_count):
    # Standard rule of thumb: ~4 bytes per token for code/markdown
    return byte_count // 4

def parse_loadmap_tags(toolkit_dir):
    loadmap_file = Path(toolkit_dir) / "LOADMAP.md"
    if not loadmap_file.exists():
        return {}
    
    tags = {}
    with open(loadmap_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith("| `"):
                parts = [p.strip() for p in line.split("|") if p.strip()]
                if len(parts) >= 3:
                    tag_name = parts[0].replace("`", "").strip()
                    file_list = [f.strip().replace("`", "") for f in parts[2].split(",")]
                    tags[tag_name] = file_list
    return tags

def measure_tags(tags_to_load, toolkit_dir):
    tag_map = parse_loadmap_tags(toolkit_dir)
    total_bytes = 0
    resolved_files = set()

    for tag in tags_to_load:
        files = tag_map.get(tag, [])
        for f in files:
            p = Path(toolkit_dir) / f
            if p.exists() and p not in resolved_files:
                resolved_files.add(p)
                # Count only lines 1-60 (the Agent Card)
                with open(p, "r", encoding="utf-8") as fp:
                    lines = [fp.readline() for _ in range(60)]
                    card_content = "".join(lines)
                    total_bytes += len(card_content.encode("utf-8"))

    tokens = estimate_tokens(total_bytes)
    return total_bytes, tokens, len(resolved_files)

def main():
    if len(sys.argv) < 2:
        print("Usage: toolkit context <feature_name> [phase_number] | <tag1,tag2,...>")
        sys.exit(0)

    arg = sys.argv[1]
    toolkit_dir = Path(__file__).resolve().parents[1]

    if "," in arg or not arg.startswith("ai_specs"):
        # Direct tags list
        tags = [t.strip() for t in arg.split(",") if t.strip()]
        b, t, count = measure_tags(tags, toolkit_dir)
        print(f"📊 Lean Loading Budget for tags {tags}:")
        print(f"   Files: {count} card(s)")
        print(f"   Size:  {b} bytes (~{t} tokens)")
        print(f"   Status: {'✅ Well within 4KB budget' if b < 4096 else '⚠️ Exceeds 4KB budget'}")

if __name__ == "__main__":
    main()
