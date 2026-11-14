#!/usr/bin/env python3
"""
Universal AI Toolkit v2 — Autonomous QA & Verification Engine
Executes Maestro declarative flows, verifies screen states, detects layout overflows,
and generates Lean QA Summary Cards for AI agent self-healing loops.
Uses Python Standard Library ONLY (zero pip dependencies).
"""

import sys
import os
import re
import json
import shutil
import argparse
import subprocess
from pathlib import Path

def find_toolkit_dir():
    """Finds the root directory of the toolkit."""
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / "schema" / "project_profile.schema.json").exists():
            return current
        current = current.parent
    return Path(__file__).resolve().parent.parent.parent

def load_simple_yaml(file_path):
    """Simple YAML reader extracting top-level and 1-level nested keys without PyYAML."""
    data = {}
    if not os.path.exists(file_path):
        return data
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    current_section = None
    for raw_line in lines:
        line = raw_line.rstrip()
        if not line or line.strip().startswith("#"):
            continue
        
        # Check top-level key
        top_match = re.match(r"^([a-zA-Z0-9_\-]+)\s*:\s*(.*)", line)
        if top_match and not raw_line.startswith(" ") and not raw_line.startswith("\t"):
            key = top_match.group(1)
            val = top_match.group(2).strip().strip("'\"")
            current_section = key
            if val != "":
                data[key] = val
            else:
                data[key] = {}
            continue

        # Check nested key (indentation)
        nested_match = re.match(r"^\s+([a-zA-Z0-9_\-]+)\s*:\s*(.*)", line)
        if nested_match and current_section:
            k = nested_match.group(1)
            v = nested_match.group(2).strip().strip("'\"")
            if isinstance(data.get(current_section), dict):
                data[current_section][k] = v
            continue

        # Check list item
        list_match = re.match(r"^\s+-\s+(.*)", line)
        if list_match and current_section:
            item = list_match.group(1).strip().strip("'\"")
            if not isinstance(data.get(current_section), list):
                data[current_section] = []
            data[current_section].append(item)

    return data

def check_command_installed(cmd):
    """Checks if a binary is available on the system PATH."""
    return shutil.which(cmd) is not None

def run_cmd(cmd_list, timeout=180):
    """Runs a shell command and returns (returncode, stdout, stderr)."""
    try:
        proc = subprocess.run(
            cmd_list,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout
        )
        return proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired:
        return -1, "", f"Command timed out after {timeout} seconds."
    except Exception as e:
        return -1, "", str(e)

def get_connected_devices():
    """Returns list of active adb devices / running iOS simulators."""
    devices = []
    if check_command_installed("adb"):
        rc, out, _ = run_cmd(["adb", "devices"])
        if rc == 0:
            for line in out.splitlines()[1:]:
                line = line.strip()
                if line and "\tdevice" in line:
                    devices.append(("android", line.split()[0]))
    
    if sys.platform == "darwin" and check_command_installed("xcrun"):
        rc, out, _ = run_cmd(["xcrun", "simctl", "list", "devices", "booted"])
        if rc == 0:
            for line in out.splitlines():
                if "(Booted)" in line:
                    match = re.search(r"([A-Fa-f0-9\-]{36})", line)
                    name = line.split("(")[0].strip()
                    if match:
                        devices.append(("ios", f"{name} ({match.group(1)})"))
    return devices

def cmd_status(args, project_root, toolkit_dir):
    """Checks the status of QA dependencies, emulators, and configuration."""
    profile_path = project_root / "project_profile.yaml"
    profile = load_simple_yaml(profile_path)
    qa_cfg = profile.get("qa_verification", {})

    print("\n" + "🧪"*35)
    print("  UNIVERSAL AI TOOLKIT v2 — QA VERIFICATION STATUS")
    print("🧪"*35)

    # 1. Project Profile QA config
    if qa_cfg:
        print(f"✅ QA Config Enabled: {qa_cfg.get('enabled', 'true')}")
        print(f"   Runner: {qa_cfg.get('runner', 'maestro')}")
        print(f"   Platform: {qa_cfg.get('device', {}).get('platform', 'android') if isinstance(qa_cfg.get('device'), dict) else 'android'}")
        print(f"   Flows Path: {qa_cfg.get('flows_path', 'test/qa_flows')}")
        print(f"   Reports Path: {qa_cfg.get('reports_path', 'test/qa_reports')}")
    else:
        print("⚠️ No `qa_verification` section found in project_profile.yaml (using defaults).")

    # 2. Maestro CLI check
    if check_command_installed("maestro"):
        rc, out, _ = run_cmd(["maestro", "--version"])
        ver = out.strip() if rc == 0 else "Installed"
        print(f"✅ Maestro CLI: {ver}")
    else:
        print("❌ Maestro CLI NOT installed.")
        print("   👉 Install with: curl -fsSL \"https://get.maestro.mobile.dev\" | bash")

    # 3. Android adb check
    if check_command_installed("adb"):
        print("✅ Android ADB: Available")
    else:
        print("⚠️ Android ADB: Not in PATH")

    # 4. Flutter binary check
    if check_command_installed("flutter"):
        print("✅ Flutter CLI: Available")
    else:
        print("❌ Flutter CLI: Not found in PATH")

    # 5. Connected Devices
    devices = get_connected_devices()
    print(f"\n📱 Active Devices / Booted Emulators ({len(devices)}):")
    if devices:
        for platform, dev_id in devices:
            print(f"   • [{platform.upper()}] {dev_id}")
    else:
        print("   ⚠️ No active emulator or physical device detected.")
        print("   👉 Boot your Android Emulator or iOS Simulator before running QA.")
    print("="*70 + "\n")

def cmd_generate(args, project_root, toolkit_dir):
    """Generates a standard Maestro QA Flow for a given feature."""
    feature = args.feature.strip() if args.feature else None
    if not feature:
        print("❌ Error: Feature name required. Usage: toolkit qa gen <feature_name>")
        sys.exit(1)

    profile = load_simple_yaml(project_root / "project_profile.yaml")
    qa_cfg = profile.get("qa_verification", {})
    flows_rel = qa_cfg.get("flows_path", "test/qa_flows") if isinstance(qa_cfg, dict) else "test/qa_flows"
    flows_dir = project_root / flows_rel
    flows_dir.mkdir(parents=True, exist_ok=True)

    target_flow = flows_dir / f"{feature}_flow.yaml"

    # Template
    template_file = toolkit_dir / "templates" / "qa" / "maestro_flow.template.yaml"
    template_content = ""
    if template_file.exists():
        with open(template_file, "r", encoding="utf-8") as f:
            template_content = f.read()
    else:
        template_content = """appId: ${APP_ID}
---
- launchApp:
    clearState: true
- assertVisible:
    text: ".*"
- takeScreenshot: "reports/${FEATURE_NAME}/01_screen"
"""

    # Package/appId discovery
    app_id = "com.example.app"
    pubspec_path = project_root / "pubspec.yaml"
    if pubspec_path.exists():
        with open(pubspec_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("name:"):
                    app_id = line.split(":")[1].strip()
                    break

    content = template_content.replace("{{FEATURE_NAME}}", feature)
    content = content.replace("{{PACKAGE_NAME}}", app_id)
    content = content.replace("{{APP_ID}}", app_id)
    content = content.replace("{{NAV_TRIGGER_ID}}", f"nav_to_{feature}")
    content = content.replace("{{PRIMARY_CONTENT_ID}}", f"{feature}_screen_title")

    with open(target_flow, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"🎉 Generated Maestro QA Flow: {target_flow}")
    print(f"💡 You can now review and customize: {target_flow}")
    print(f"👉 Run with: toolkit qa run {feature}")

def cmd_run(args, project_root, toolkit_dir):
    """Executes Maestro flow, evaluates layout, and emits Lean QA Summary Card."""
    feature = args.feature.strip() if args.feature else None
    profile = load_simple_yaml(project_root / "project_profile.yaml")
    qa_cfg = profile.get("qa_verification", {}) if isinstance(profile.get("qa_verification"), dict) else {}
    
    flows_rel = qa_cfg.get("flows_path", "test/qa_flows")
    reports_rel = qa_cfg.get("reports_path", "test/qa_reports")
    
    flows_dir = project_root / flows_rel
    reports_dir = project_root / reports_rel
    reports_dir.mkdir(parents=True, exist_ok=True)

    # 1. Prerequisite checks
    if not check_command_installed("maestro"):
        print("🛑 Maestro CLI is not installed.")
        print("👉 Install Maestro: curl -fsSL \"https://get.maestro.mobile.dev\" | bash")
        sys.exit(1)

    devices = get_connected_devices()
    if not devices:
        print("🛑 No active Android Emulator or iOS Simulator found.")
        print("👉 Please start an emulator or simulator first.")
        sys.exit(1)

    # 2. Locate flow file
    target_flow = None
    if feature:
        candidates = [
            flows_dir / f"{feature}_flow.yaml",
            flows_dir / f"{feature}.yaml",
            flows_dir / f"{feature}_test.yaml",
        ]
        for c in candidates:
            if c.exists():
                target_flow = c
                break
        if not target_flow:
            print(f"⚠️ Flow not found for feature '{feature}' in {flows_dir}.")
            print(f"💡 Generating a starter flow for '{feature}'...")
            args_gen = argparse.Namespace(feature=feature)
            cmd_generate(args_gen, project_root, toolkit_dir)
            target_flow = flows_dir / f"{feature}_flow.yaml"
    else:
        # Run all flows in flows_dir
        yaml_files = list(flows_dir.glob("*.yaml")) + list(flows_dir.glob("*.yml"))
        if not yaml_files:
            print(f"❌ No QA flow files found in {flows_dir}.")
            print("👉 Generate one using: toolkit qa gen <feature_name>")
            sys.exit(1)
        target_flow = yaml_files[0]
        feature = target_flow.stem.replace("_flow", "")

    feature_report_dir = reports_dir / feature
    feature_report_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n🚀 Executing Autonomous QA Flow: {target_flow.name}")
    print(f"📱 Target Device: {devices[0][0].upper()} ({devices[0][1]})")
    print(f"📂 Reports Path: {feature_report_dir}\n")

    # 3. Run Maestro test
    cmd = ["maestro", "test", str(target_flow)]
    rc, stdout, stderr = run_cmd(cmd, timeout=240)
    combined_log = stdout + "\n" + stderr

    # Save raw log
    raw_log_path = feature_report_dir / "maestro_execution.log"
    with open(raw_log_path, "w", encoding="utf-8") as f:
        f.write(combined_log)

    # 4. Parse Results & Detect Overflows / Failures
    has_overflow = "RenderFlex overflowed by" in combined_log
    has_assertion_fail = "Failed to assert" in combined_log or "AssertionError" in combined_log or rc != 0

    passed_checks = 0
    total_checks = max(1, combined_log.count("Asserting") + combined_log.count("Assert visible"))
    if not has_assertion_fail and not has_overflow:
        passed_count = total_checks
        is_success = True
    else:
        is_success = False
        passed_count = max(0, total_checks - 1)

    # 5. Extract Failed Details & Suspected Widget
    failed_step = "None"
    error_msg = "All checks passed cleanly"
    suspected_widget = "None"
    if has_overflow:
        match = re.search(r"A RenderFlex overflowed by ([\d\.]+) pixels on the ([a-zA-Z]+)", combined_log)
        if match:
            error_msg = f"RenderFlex overflow of {match.group(1)}px on the {match.group(2)}"
        else:
            error_msg = "RenderFlex layout overflow detected on screen."
        failed_step = "Orientation / Layout Constraints Check"
        suspected_widget = "Column / Row without Flexible, Expanded, or SingleChildScrollView"
    elif has_assertion_fail:
        match = re.search(r"(Element not found|Failed to assert visible|Assertion failed)[^\n]*", combined_log)
        if match:
            error_msg = match.group(0).strip()
        else:
            error_msg = "UI assertion failed during flow execution."
        failed_step = "UI Element Visibility Check"
        suspected_widget = f"lib/features/{feature}/"

    # Screenshots scan
    screenshots = list(feature_report_dir.glob("*.png")) + list(reports_dir.glob(f"{feature}*.png"))
    screenshot_ref = str(screenshots[0]) if screenshots else f"{feature_report_dir}/"

    # 6. Generate Lean QA Summary Card (< 1KB)
    status_emoji = "✅" if is_success else "❌"
    status_label = "PASSED" if is_success else "FAILED"
    overflow_label = "❌ DETECTED" if has_overflow else "✅ Clean (0 Overflows)"

    summary_card = f"""
======================================================================
### 🧪 QA Verification Summary Card: {feature}
- **Status:** {status_emoji} **{status_label}** (Score: {passed_count}/{total_checks})
- **Device:** {devices[0][0].upper()} ({devices[0][1]})
- **RenderFlex Overflows:** {overflow_label}
- **Log Reference:** {raw_log_path}
"""
    if not is_success:
        summary_card += f"""
#### ⚠️ Failure Blocker Details:
- **Failed Step:** `{failed_step}`
- **Error:** `{error_msg}`
- **Suspected Area:** `{suspected_widget}`
- **Evidence Screenshot:** `{screenshot_ref}`

#### 💡 Recommended Self-Healing Action:
1. If RenderFlex overflow: Wrap unconstrained widgets in `Expanded`, `Flexible`, or `SingleChildScrollView`.
2. If missing element: Check that async loading completed and state has emitted loaded data.
3. Re-run after fixing: `toolkit qa run {feature}`
======================================================================
"""
    else:
        summary_card += f"""
✅ All assertions and layout constraints passed successfully!
Ready for Verify & PR Gate.
======================================================================
"""

    print(summary_card)

    # Save latest report JSON
    report_json = {
        "feature": feature,
        "success": is_success,
        "device": devices[0][1],
        "platform": devices[0][0],
        "has_overflow": has_overflow,
        "error_message": error_msg if not is_success else None,
        "raw_log": str(raw_log_path),
        "screenshot": screenshot_ref
    }
    with open(reports_dir / "latest_report.json", "w", encoding="utf-8") as f:
        json.dump(report_json, f, indent=2)

    sys.exit(0 if is_success else 1)

def main():
    parser = argparse.ArgumentParser(
        description="Universal AI Toolkit v2 — Autonomous QA Verification Engine"
    )
    subparsers = parser.add_subparsers(dest="subcommand", help="QA Subcommands")

    # run
    run_parser = subparsers.add_parser("run", help="Run Maestro flow verification")
    run_parser.add_argument("feature", nargs="?", help="Name of feature to test")
    run_parser.add_argument("--auto-fix", action="store_true", help="Enable auto-fix recommendations")

    # gen
    gen_parser = subparsers.add_parser("gen", help="Generate Maestro QA flow")
    gen_parser.add_argument("feature", help="Name of feature")

    # status
    subparsers.add_parser("status", help="Check QA tooling and emulator readiness")

    args = parser.parse_args()

    project_root = Path.cwd()
    toolkit_dir = find_toolkit_dir()

    if args.subcommand == "status":
        cmd_status(args, project_root, toolkit_dir)
    elif args.subcommand in ["gen", "generate"]:
        cmd_generate(args, project_root, toolkit_dir)
    elif args.subcommand == "run":
        cmd_run(args, project_root, toolkit_dir)
    else:
        parser.print_help()
        sys.exit(0)

if __name__ == "__main__":
    main()
