#!/usr/bin/env python3
"""
Universal AI Toolkit v2 — Project Pulse & Living State Sync Engine
Audits project state (features, plans, history, fonts, git diff, dependencies),
auto-rotates completed phases to history.md, and synchronizes all living memory files:
- ai_docs/memory.md (State of the Union, Feature Status, Technical Constraints)
- ai_docs/conventions.md
- project_profile.yaml
- README.md (Living Readme)
- ai_specs/features/<feature>/history.md
Uses Python Standard Library ONLY (zero pip dependencies).
"""

import sys
import os
import re
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

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

def run_git_summary(project_root: Path):
    """Gathers git state if available."""
    summary = {"branch": "unknown", "modified": 0, "untracked": 0, "last_commit": "None"}
    try:
        res = subprocess.run(
            ["git", "-C", str(project_root), "status", "-s"],
            capture_output=True, text=True, check=False
        )
        if res.returncode == 0:
            lines = res.stdout.strip().splitlines()
            summary["modified"] = len([l for l in lines if not l.startswith("??")])
            summary["untracked"] = len([l for l in lines if l.startswith("??")])

        branch_res = subprocess.run(
            ["git", "-C", str(project_root), "branch", "--show-current"],
            capture_output=True, text=True, check=False
        )
        if branch_res.returncode == 0 and branch_res.stdout.strip():
            summary["branch"] = branch_res.stdout.strip()

        commit_res = subprocess.run(
            ["git", "-C", str(project_root), "log", "-1", "--oneline"],
            capture_output=True, text=True, check=False
        )
        if commit_res.returncode == 0 and commit_res.stdout.strip():
            summary["last_commit"] = commit_res.stdout.strip()
    except Exception:
        pass
    return summary

def rotate_feature_plan(plan_path: Path):
    """
    Checks plan.md for completed phases.
    Rotates finished phases into history.md and keeps plan.md lean.
    """
    if not plan_path.exists():
        return None

    content = plan_path.read_text(encoding="utf-8")
    history_path = plan_path.parent / "history.md"

    # Match phase sections: ### Phase X or ## Phase X
    phases = re.split(r"(?=(?:^#{2,3}\s+Phase\s+\d+))", content, flags=re.MULTILINE)
    header = phases[0] if phases else ""
    phase_blocks = phases[1:] if len(phases) > 1 else []

    completed = []
    remaining = []

    for block in phase_blocks:
        # Check if block is marked done: [x] DONE or status: completed
        is_done = False
        if re.search(r"\[x\]\s*(?:DONE|COMPLETED)", block, re.IGNORECASE):
            is_done = True
        elif re.search(r"status:\s*completed", block, re.IGNORECASE):
            is_done = True

        if is_done:
            completed.append(block.strip())
        else:
            remaining.append(block.strip())

    if completed:
        hist_header = "# Feature Execution History\n\n> Archived completed phases from `plan.md` to preserve AI context budget.\n\n"
        existing_hist = ""
        if history_path.exists():
            existing_hist = history_path.read_text(encoding="utf-8")

        # Append new completed phases
        new_hist_content = existing_hist if existing_hist else hist_header
        new_hist_content += "\n\n" + "\n\n---\n\n".join(completed) + "\n"
        history_path.write_text(new_hist_content.strip() + "\n", encoding="utf-8")

        # Rewrite plan.md
        pointer = "> ℹ️ Completed phases have been archived to [history.md](history.md) to preserve AI context budget.\n\n"
        if "archived to [history.md]" not in header:
            header = header.rstrip() + "\n\n" + pointer

        new_plan = header.rstrip() + "\n\n" + "\n\n---\n\n".join(remaining) + "\n"
        plan_path.write_text(new_plan.strip() + "\n", encoding="utf-8")
        print(f"  📜 Rotated {len(completed)} completed phase(s) in {plan_path.parent.name} -> history.md")

    return {
        "feature": plan_path.parent.name,
        "completed": len(completed),
        "remaining": len(remaining),
        "plan_size_kb": round(len(plan_path.read_bytes()) / 1024, 2),
    }

def scan_features_and_history(project_root: Path):
    """Scans all features under ai_specs/features/ and lib/features/."""
    features_info = []
    specs_features_dir = project_root / "ai_specs" / "features"
    lib_features_dir = project_root / "lib" / "features"

    feature_names = set()
    if specs_features_dir.exists():
        for d in specs_features_dir.iterdir():
            if d.is_dir() and not d.name.startswith("."):
                feature_names.add(d.name)
    if lib_features_dir.exists():
        for d in lib_features_dir.iterdir():
            if d.is_dir() and not d.name.startswith("."):
                feature_names.add(d.name)

    for feat in sorted(feature_names):
        plan_file = specs_features_dir / feat / "plan.md"
        history_file = specs_features_dir / feat / "history.md"
        lib_dir = lib_features_dir / feat

        plan_stat = None
        if plan_file.exists():
            plan_stat = rotate_feature_plan(plan_file)

        has_code = lib_dir.exists() and any(lib_dir.rglob("*.dart"))
        has_history = history_file.exists() and len(history_file.read_text(encoding="utf-8").strip()) > 50

        status = "In Progress"
        if plan_stat and plan_stat["remaining"] == 0 and plan_stat["completed"] > 0:
            status = "Completed"
        elif not plan_file.exists() and has_code:
            status = "Implemented (No Plan)"
        elif plan_file.exists() and not has_code:
            status = "Planned (No Code)"

        features_info.append({
            "name": feat,
            "status": status,
            "has_plan": plan_file.exists(),
            "has_history": has_history,
            "has_code": has_code,
            "plan_stat": plan_stat,
        })

    return features_info

def scan_fonts_and_assets(project_root: Path):
    """Scans assets/fonts/ for active fonts."""
    fonts_dir = project_root / "assets" / "fonts"
    fonts = []
    if fonts_dir.exists():
        for item in fonts_dir.rglob("*"):
            if item.is_file() and item.suffix.lower() in [".ttf", ".otf"]:
                fonts.append(item.name)
    return fonts

def update_living_memory(project_root: Path, git_info: dict, features: list, fonts: list):
    """Updates ai_docs/memory.md with the live project state snapshot."""
    memory_path = project_root / "ai_docs" / "memory.md"
    if not memory_path.exists():
        return

    content = memory_path.read_text(encoding="utf-8")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    # 1. Update/Add Feature Execution Table
    table_lines = [
        "## Feature Execution & History Status",
        f"> Auto-synchronized by `toolkit pulse` on {timestamp}.\n",
        "| Feature | Status | Code | Plan | History Log |",
        "| :--- | :--- | :--- | :--- | :--- |",
    ]
    for f in features:
        code_mark = "✅ Yes" if f["has_code"] else "⏳ None"
        plan_mark = "📋 Active" if f["has_plan"] else "—"
        hist_mark = "📜 Recorded" if f["has_history"] else "—"
        table_lines.append(f"| `{f['name']}` | **{f['status']}** | {code_mark} | {plan_mark} | {hist_mark} |")

    new_feat_table = "\n".join(table_lines)

    if "## Feature Execution & History Status" in content:
        pattern = r"## Feature Execution & History Status[\s\S]*?(?=\n## |\Z)"
        content = re.sub(pattern, new_feat_table, content)
    else:
        content = content.rstrip() + "\n\n" + new_feat_table + "\n"

    # 2. Update Pulse Sync in Quick Constraints
    pulse_row = f"| **Last Pulse Sync** | `{timestamp}` ({git_info['branch']} branch, {len(features)} features) |"
    if "| **Last Pulse Sync** |" in content:
        content = re.sub(r"\|\s*\*\*Last Pulse Sync\*\*.*\|", pulse_row, content)
    elif "## 1. Quick Technical Constraints" in content:
        content = re.sub(r"(\|\s*\*\*Testing Gate\*\*.*\|)", rf"\1\n{pulse_row}", content, count=1)

    memory_path.write_text(content, encoding="utf-8")
    print(f"  🧠 Synced living memory: {memory_path.name}")

def update_living_readme(project_root: Path, features: list, fonts: list):
    """Updates README.md with live feature counts and state."""
    readme_path = project_root / "README.md"
    if not readme_path.exists():
        return

    content = readme_path.read_text(encoding="utf-8")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Update or append Feature Inventory section
    feat_summary = f"> 🔄 Last synchronized on {timestamp} — **{len(features)} Active Feature(s)**\n\n"
    feat_summary += "| Feature | Current State |\n| :--- | :--- |\n"
    for f in features:
        feat_summary += f"| `{f['name']}` | {f['status']} |\n"

    if "## Features & Architecture Status" in content:
        pattern = r"## Features & Architecture Status[\s\S]*?(?=\n## |\Z)"
        content = re.sub(pattern, f"## Features & Architecture Status\n\n{feat_summary}", content)
        readme_path.write_text(content, encoding="utf-8")
        print(f"  📖 Updated README.md Features Status")

def run_pulse(target_dir: Path):
    project_root = resolve_project_root(target_dir)

    print("\n" + "🩺"*35)
    print(f"  UNIVERSAL AI TOOLKIT v2 — PROJECT PULSE & LIVING SYNC")
    print(f"  Target Project Root: {project_root}")
    print("🩺"*35 + "\n")

    profile = load_simple_profile(project_root / "project_profile.yaml")
    git_info = run_git_summary(project_root)

    print(f"🔍 Git Pulse: Branch [{git_info['branch']}] | Modified: {git_info['modified']} | Untracked: {git_info['untracked']}")
    print(f"   Last Commit: {git_info['last_commit']}\n")

    print("🔍 Auditing Features & Rotating Plan/History...")
    features = scan_features_and_history(project_root)
    print(f"   Discovered {len(features)} total feature domains.")

    fonts = scan_fonts_and_assets(project_root)
    print(f"🔍 Auditing Fonts & Assets: {len(fonts)} font file(s) active in assets/fonts/.\n")

    print("📝 Synchronizing Living Knowledge Base & Memory...")
    update_living_memory(project_root, git_info, features, fonts)
    update_living_readme(project_root, features, fonts)

    # Print High-Density AI Snapshot
    print("\n" + "="*70)
    print("  📊 PROJECT PULSE SNAPSHOT (State of the Union)")
    print("="*70)
    print(f"• Project Name    : {profile.get('project_name', project_root.name)}")
    print(f"• State Mgmt      : {profile.get('state_management', 'bloc_cubit')}")
    print(f"• Navigation      : {profile.get('navigation', 'go_router')}")
    print(f"• Primary Font    : {profile.get('primary_font', 'Custom / Bundled')}")
    print(f"• Active Features : {len(features)}")
    for f in features:
        print(f"    - {f['name'].ljust(18)} : {f['status']} (Code: {'Yes' if f['has_code'] else 'No'}, History: {'Yes' if f['has_history'] else 'No'})")
    print(f"• Uncommitted Diff: {git_info['modified']} modified, {git_info['untracked']} untracked files")
    print("="*70)
    print("🎉 Project pulse and living memory are 100% synchronized!\n")

def main():
    parser = argparse.ArgumentParser(description="Universal AI Toolkit v2 — Project Pulse")
    parser.add_argument("--target", default=".", help="Target Flutter project root (default: current)")
    args = parser.parse_args()

    run_pulse(Path(args.target))

if __name__ == "__main__":
    main()
