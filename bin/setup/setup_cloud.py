#!/usr/bin/env python3
"""
Universal AI Toolkit v2 — Cloud & Store Provisioning Engine
Automates Firebase project creation, Apple App Store registration,
and Google Play Console readiness with Fastlane metadata from a single command.
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

def print_banner():
    print("\n" + "☁️ "*35)
    print("  UNIVERSAL AI TOOLKIT v2 — CLOUD & STORE PROVISIONING ENGINE")
    print("☁️ "*35)

def extract_project_metadata(target_path: Path):
    """Auto-detects project name, package name (Android), and bundle ID (iOS)."""
    meta = {
        "name": "my_flutter_app",
        "android_package": "com.example.app",
        "ios_bundle_id": "com.example.app",
        "description": "Flutter Application",
    }

    # 1. Try project_profile.yaml
    profile_path = target_path / "project_profile.yaml"
    if profile_path.exists():
        try:
            with open(profile_path, "r", encoding="utf-8") as f:
                content = f.read()
                m_name = re.search(r'project_name\s*:\s*["\']?([^"\'\n]+)["\']?', content)
                if m_name:
                    meta["name"] = m_name.group(1).strip()
                m_pkg = re.search(r'android_package\s*:\s*["\']?([^"\'\n]+)["\']?', content)
                if m_pkg:
                    meta["android_package"] = m_pkg.group(1).strip()
                m_bundle = re.search(r'ios_bundle_id\s*:\s*["\']?([^"\'\n]+)["\']?', content)
                if m_bundle:
                    meta["ios_bundle_id"] = m_bundle.group(1).strip()
        except Exception:
            pass

    # 2. Try pubspec.yaml
    pubspec_path = target_path / "pubspec.yaml"
    if pubspec_path.exists():
        try:
            with open(pubspec_path, "r", encoding="utf-8") as f:
                content = f.read()
                m = re.search(r'^name\s*:\s*([a-zA-Z0-9_]+)', content, re.MULTILINE)
                if m and meta["name"] == "my_flutter_app":
                    meta["name"] = m.group(1).strip()
                m_desc = re.search(r'^description\s*:\s*["\']?([^"\'\n]+)["\']?', content, re.MULTILINE)
                if m_desc:
                    meta["description"] = m_desc.group(1).strip()
        except Exception:
            pass

    # 3. Detect Android package/namespace
    app_gradle = target_path / "android" / "app" / "build.gradle"
    app_gradle_kts = target_path / "android" / "app" / "build.gradle.kts"
    for g_path in [app_gradle_kts, app_gradle]:
        if g_path.exists():
            try:
                with open(g_path, "r", encoding="utf-8") as f:
                    txt = f.read()
                    m_ns = re.search(r'(?:namespace|applicationId)\s*[=\s]\s*["\']([^"\']+)["\']', txt)
                    if m_ns:
                        meta["android_package"] = m_ns.group(1).strip()
                        break
            except Exception:
                pass

    # 4. Detect iOS Bundle ID
    pbxproj = target_path / "ios" / "Runner.xcodeproj" / "project.pbxproj"
    if pbxproj.exists():
        try:
            with open(pbxproj, "r", encoding="utf-8") as f:
                txt = f.read()
                m_bid = re.search(r'PRODUCT_BUNDLE_IDENTIFIER\s*=\s*([^;]+);', txt)
                if m_bid:
                    bid = m_bid.group(1).strip().strip('"\'')
                    if bid and not bid.startswith("$("):
                        meta["ios_bundle_id"] = bid
        except Exception:
            pass

    # Fallback sync
    if meta["ios_bundle_id"] == "com.example.app" and meta["android_package"] != "com.example.app":
        meta["ios_bundle_id"] = meta["android_package"]
    elif meta["android_package"] == "com.example.app" and meta["ios_bundle_id"] != "com.example.app":
        meta["android_package"] = meta["ios_bundle_id"]

    # 5. Detect Moltaqa enterprise context
    meta["is_moltaqa"] = (
        "moltaqa" in meta["name"].lower() or
        "moltaqa" in meta["android_package"].lower() or
        "moltaqa" in meta["ios_bundle_id"].lower()
    )
    if profile_path.exists():
        try:
            with open(profile_path, "r", encoding="utf-8") as f:
                content = f.read()
                if 'preset: "moltaqa"' in content or 'preset: moltaqa' in content or 'moltaqa' in content.lower():
                    meta["is_moltaqa"] = True
        except Exception:
            pass

    return meta

def run_cmd(cmd_list, dry_run=False, check=True):
    """Executes a command list safely with dry-run support."""
    cmd_str = " ".join(cmd_list)
    if dry_run:
        print(f"      [DRY-RUN] Executing: {cmd_str}")
        return True, ""
    try:
        proc = subprocess.run(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=check)
        return True, proc.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr or e.stdout
    except FileNotFoundError:
        return False, f"Command not found: {cmd_list[0]}"

# ==============================================================================
# 1. FIREBASE PROVISIONING
# ==============================================================================
def setup_firebase(target_path: Path, meta: dict, project_id: str = None, dry_run: bool = False):
    print("\n" + "🔥 "*20)
    print("  STAGE 1: FIREBASE CLOUD INITIALIZATION")
    print("🔥 "*20)

    # 1. Tool verification
    firebase_cli = shutil.which("firebase")
    flutterfire_cli = shutil.which("flutterfire")

    if not firebase_cli:
        print("   ⚠️  Firebase CLI (`firebase`) is not installed or not in PATH.")
        print("      To install Firebase CLI, run:")
        print("      👉 npm install -g firebase-tools  OR  curl -sL https://firebase.tools | bash\n")
        return False

    if not flutterfire_cli:
        print("   ⚠️  FlutterFire CLI (`flutterfire`) is not installed or not in PATH.")
        print("      To install FlutterFire CLI, run:")
        print("      👉 dart pub global activate flutterfire_cli\n")
        return False

    # Check Firebase Auth
    ok, auth_out = run_cmd(["firebase", "login:list"], dry_run=dry_run, check=False)
    if not ok or "No authorized" in auth_out:
        print("   ⚠️  You are not logged in to Firebase.")
        print("      Please run: 👉 firebase login\n")
        return False

    # Compute project ID
    sanitized_name = re.sub(r'[^a-z0-9\-]', '-', meta["name"].lower().replace('_', '-'))
    pid = project_id or f"{sanitized_name}-app"
    display_name = meta["name"].replace('_', ' ').title()

    print(f"   📋 Project ID:   {pid}")
    print(f"   📋 Display Name: {display_name}")
    print(f"   📱 Android Pkg:  {meta['android_package']}")
    print(f"   🍏 iOS Bundle:   {meta['ios_bundle_id']}")

    # 2. Create Firebase Project
    print(f"\n   ⚙️  Checking/Creating Firebase project `{pid}`...")
    create_cmd = ["firebase", "projects:create", pid, "--display-name", display_name]
    ok, out = run_cmd(create_cmd, dry_run=dry_run, check=False)
    if ok:
        print("   ✅ Firebase project created successfully!")
    else:
        if "already exists" in out or "already in use" in out:
            print(f"   ℹ️  Firebase project `{pid}` already exists, proceeding to configure...")
        else:
            print(f"   ⚠️  Firebase project creation note: {out.strip() or 'Continuing to configure'}")

    # 3. Configure Flutter app with FlutterFire
    print("\n   ⚙️  Configuring Flutter app with `flutterfire configure`...")
    cfg_cmd = [
        "flutterfire", "configure",
        f"--project={pid}",
        f"--android-package-name={meta['android_package']}",
        f"--ios-bundle-id={meta['ios_bundle_id']}",
        "--yes",
        "--platforms=android,ios"
    ]
    ok_cfg, cfg_out = run_cmd(cfg_cmd, dry_run=dry_run, check=False)
    if ok_cfg or dry_run:
        print("   ✅ FlutterFire configuration completed successfully!")
        print(f"      - Generated: lib/firebase_options.dart")
        print(f"      - Android:   android/app/google-services.json")
        print(f"      - iOS:       ios/Runner/GoogleService-Info.plist")
        print(f"      🔗 Firebase Console: https://console.firebase.google.com/project/{pid}/overview")
        if meta.get("is_moltaqa"):
            print("      🔔 Moltaqa APNs & Firebase Cloud Messaging (FCM) Credentials:")
            print("         - Key ID:  4A9WV94BJ9")
            print("         - Team ID: Q57RLVXT2A")
            print("         - AuthKey: templates/signing/moltaqa/apple/AuthKey_4A9WV94BJ9.p8")
        return True
    else:
        print(f"   ❌ FlutterFire configure encountered an issue:\n{cfg_out}")
        return False

# ==============================================================================
# 2. APPLE APP STORE CONNECT PROVISIONING
# ==============================================================================
def setup_appstore(target_path: Path, meta: dict, apple_id: str = None, team_id: str = None, dry_run: bool = False):
    print("\n" + "🍏 "*20)
    print("  STAGE 2: APPLE APP STORE CONNECT REGISTRATION")
    print("🍏 "*20)

    fastlane_cli = shutil.which("fastlane")
    ios_dir = target_path / "ios"
    fastlane_dir = ios_dir / "fastlane"

    if not fastlane_cli:
        print("   ⚠️  Fastlane is not installed or not in PATH.")
        print("      To install Fastlane for iOS automation, run:")
        print("      👉 brew install fastlane  OR  gem install fastlane\n")
        return False

    fastlane_dir.mkdir(parents=True, exist_ok=True)

    app_name = meta["name"].replace('_', ' ').title()
    bundle_id = meta["ios_bundle_id"]
    sku = f"{bundle_id.replace('.', '_')}_sku"

    if not team_id and meta.get("is_moltaqa"):
        team_id = "Q57RLVXT2A"
        print("   🏢 Using Moltaqa Apple Team ID: Q57RLVXT2A (Key ID: 4A9WV94BJ9)")

    print(f"   📋 App Name:     {app_name}")
    print(f"   🍏 Bundle ID:    {bundle_id}")
    print(f"   🏷️ SKU:          {sku}")

    # 1. Create/Update Appfile
    appfile_path = fastlane_dir / "Appfile"
    if not appfile_path.exists() or not appfile_path.read_text(encoding="utf-8").strip():
        appfile_content = f"""# Apple App Store Connect Configuration
app_identifier("{bundle_id}")
"""
        if apple_id:
            appfile_content += f'apple_id("{apple_id}")\n'
        if team_id:
            appfile_content += f'team_id("{team_id}")\n'
        appfile_path.write_text(appfile_content, encoding="utf-8")
        print("   ✅ Created: ios/fastlane/Appfile")

    # 2. Create Fastfile if missing
    fastfile_path = fastlane_dir / "Fastfile"
    if not fastfile_path.exists():
        fastfile_content = """default_platform(:ios)

platform :ios do
  desc "Register App ID and App Record on App Store Connect"
  lane :register do
    produce(
      app_name: ENV['APP_NAME'] || '""" + app_name + """',
      app_identifier: '""" + bundle_id + """',
      language: 'English',
      skip_itc: false
    )
  end

  desc "Build and upload iOS Release to TestFlight"
  lane :beta do
    build_app(workspace: "Runner.xcworkspace", scheme: "Runner")
    upload_to_testflight
  end
end
"""
        fastfile_path.write_text(fastfile_content, encoding="utf-8")
        print("   ✅ Created: ios/fastlane/Fastfile with `:register` and `:beta` lanes")

    # 3. Execute fastlane produce
    print(f"\n   ⚙️  Registering App ID & App Store Record via `fastlane produce`...")
    produce_cmd = [
        "fastlane", "produce", "create",
        "--app_identifier", bundle_id,
        "--app_name", app_name,
        "--sku", sku,
        "--language", "English"
    ]
    if apple_id:
        produce_cmd.extend(["--username", apple_id])
    if team_id:
        produce_cmd.extend(["--team_id", team_id])

    ok, out = run_cmd(produce_cmd, dry_run=dry_run, check=False)
    if ok or dry_run:
        print("   ✅ App Store Connect registration command dispatched!")
        print(f"      🔗 App Store Connect: https://appstoreconnect.apple.com/apps")
        return True
    else:
        if "already exists" in out or "taken" in out:
            print(f"   ℹ️  App identifier or record already exists on App Store Connect.")
            print(f"      🔗 App Store Connect: https://appstoreconnect.apple.com/apps")
            return True
        else:
            print(f"   ⚠️  Fastlane produce result:\n{out}")
            print("      Note: Verify your Apple Developer account credentials or API Key.")
            return False

# ==============================================================================
# 3. GOOGLE PLAY STORE READINESS & FASTLANE SUPPLY
# ==============================================================================
def setup_playstore(target_path: Path, meta: dict, dry_run: bool = False, use_moltaqa: bool = False):
    print("\n" + "🤖 "*20)
    print("  STAGE 3: GOOGLE PLAY STORE READINESS & FASTLANE SUPPLY")
    print("🤖 "*20)

    print("   📢 Notice: Google Play Developer Publishing API requires the app record")
    print("      to be registered once via the Google Play Console UI before API uploads.")
    print("      Toolkit prepares all keys, metadata, and Fastlane supply config now!\n")

    android_dir = target_path / "android"
    fastlane_dir = android_dir / "fastlane"
    metadata_dir = fastlane_dir / "metadata" / "android"

    # 1. Verify/Prepare Signing
    key_prop = android_dir / "key.properties"
    is_moltaqa = use_moltaqa or meta.get("is_moltaqa", False)
    if not key_prop.exists():
        print("   🔑 Release keystore not configured yet.")
        setup_signing_script = Path(__file__).parent / "setup_signing.py"
        if setup_signing_script.exists():
            sign_cmd = [sys.executable, str(setup_signing_script), str(target_path)]
            if is_moltaqa:
                sign_cmd.append("--moltaqa")
                print("      Running automated Moltaqa release signing setup...")
            else:
                print("      Running automated release signing config...")
            run_cmd(sign_cmd, dry_run=dry_run, check=False)
    else:
        print("   ✅ Release Keystore configuration found (key.properties)")

    # 2. Generate Fastlane Supply Metadata Structure (English & Arabic)
    app_name = meta["name"].replace('_', ' ').title()
    desc = meta["description"]

    locales = {
        "en-US": {
            "title": app_name,
            "short_description": desc[:80] if len(desc) > 80 else desc,
            "full_description": f"{app_name} - {desc}.\n\nBuilt with modern Flutter architecture.",
        },
        "ar": {
            "title": app_name,
            "short_description": "تطبيق عصري ومتميز مبني بأحدث معايير فلاتر.",
            "full_description": f"تطبيق {app_name}.\n\nتطبيق عصري وسريع يقدم أفضل تجربة للمستخدم بأحدث التقنيات.",
        }
    }

    for loc, texts in locales.items():
        loc_dir = metadata_dir / loc
        loc_dir.mkdir(parents=True, exist_ok=True)
        (loc_dir / "title.txt").write_text(texts["title"], encoding="utf-8")
        (loc_dir / "short_description.txt").write_text(texts["short_description"], encoding="utf-8")
        (loc_dir / "full_description.txt").write_text(texts["full_description"], encoding="utf-8")

    # Changelog placeholder
    changelogs_dir = metadata_dir / "changelogs"
    changelogs_dir.mkdir(parents=True, exist_ok=True)
    (changelogs_dir / "default.txt").write_text("Initial release with core features.", encoding="utf-8")
    print("   ✅ Generated Fastlane Supply metadata (Title, Short & Full Descriptions in en-US and ar)")

    # 3. Create Android Fastlane Appfile & Fastfile
    appfile_path = fastlane_dir / "Appfile"
    if not appfile_path.exists():
        appfile_path.write_text(f"""# Google Play Store Configuration
json_key_file("fastlane/play_store_key.json")
package_name("{meta['android_package']}")
""", encoding="utf-8")
        print("   ✅ Created: android/fastlane/Appfile")

    fastfile_path = fastlane_dir / "Fastfile"
    if not fastfile_path.exists():
        fastfile_path.write_text("""default_platform(:android)

platform :android do
  desc "Deploy AppBundle to Google Play Internal Sharing Track"
  lane :deploy_internal do
    gradle(task: "bundleRelease", project_dir: "./android")
    upload_to_play_store(track: 'internal')
  end

  desc "Promote Internal to Production"
  lane :promote_production do
    upload_to_play_store(track: 'production')
  end
end
""", encoding="utf-8")
        print("   ✅ Created: android/fastlane/Fastfile with `:deploy_internal` and `:promote_production` lanes")

    # 4. Direct console link and instructions
    print(f"\n   📋 Target Package:  {meta['android_package']}")
    print(f"   🔗 Google Play Console: https://play.google.com/console/u/0/developers/")
    print(f"   💡 Next Step:")
    print(f"      1. Open Play Console and click 'Create app' with package: {meta['android_package']}")
    print(f"      2. Run `flutter build appbundle` and upload the initial release.")
    print(f"      3. Place your Google Play Service Account JSON at `android/fastlane/play_store_key.json`")
    print(f"         for 100% automated CI/CD deployments via `fastlane deploy_internal`.")
    return True

# ==============================================================================
# MAIN ENTRYPOINT & CLI PARSER
# ==============================================================================
def main():
    parser = argparse.ArgumentParser(
        description="Universal AI Toolkit v2 — Cloud & App Stores Provisioning CLI"
    )
    parser.add_argument("target", nargs="?", default=".", help="Target Flutter project directory (default: .)")
    parser.add_argument("-f", "--firebase", action="store_true", help="Provision Firebase project and configure FlutterFire")
    parser.add_argument("-a", "--appstore", action="store_true", help="Register App ID and App Record on Apple App Store Connect")
    parser.add_argument("-p", "--playstore", action="store_true", help="Prepare Google Play Console readiness, Keystore & Fastlane Supply metadata")
    parser.add_argument("--all", action="store_true", help="Run provisioning for all 3 platforms (Firebase, App Store, Play Store)")
    parser.add_argument("--project-id", type=str, help="Custom Firebase Project ID")
    parser.add_argument("--app-name", type=str, help="Custom Application Display Name")
    parser.add_argument("--bundle-id", type=str, help="Custom Package Name / iOS Bundle Identifier")
    parser.add_argument("--apple-id", type=str, help="Apple ID for App Store Connect login")
    parser.add_argument("--team-id", type=str, help="Apple Developer Team ID")
    parser.add_argument("--moltaqa", action="store_true", help="Use Moltaqa standard release keystore (upload-keystore.jks & key.properties)")
    parser.add_argument("--dry-run", action="store_true", help="Simulate provisioning without executing remote network calls")

    args = parser.parse_args()
    target_path = Path(args.target).resolve()

    print_banner()
    print(f"📂 Project Root: {target_path}")

    meta = extract_project_metadata(target_path)
    if args.app_name:
        meta["name"] = args.app_name
    if args.bundle_id:
        meta["android_package"] = args.bundle_id
        meta["ios_bundle_id"] = args.bundle_id

    # Determine which platforms to run
    run_fb = args.firebase or args.all
    run_as = args.appstore or args.all
    run_ps = args.playstore or args.all

    # Interactive mode if no flags specified
    if not (run_fb or run_as or run_ps):
        print("\n✨ Interactive Cloud Provisioning Wizard:")
        print(f"   Detected App Name:    {meta['name']}")
        print(f"   Detected Android Pkg: {meta['android_package']}")
        print(f"   Detected iOS Bundle:  {meta['ios_bundle_id']}\n")

        def prompt_yn(question, default="y"):
            choice = input(f"{question} [{default.upper()}/{'n' if default == 'y' else 'y'}]: ").strip().lower()
            if not choice:
                return default == "y"
            return choice.startswith("y")

        try:
            run_fb = prompt_yn("1. Provision Firebase project & run flutterfire configure?", "y")
            run_as = prompt_yn("2. Register App on Apple App Store Connect (Fastlane produce)?", "y")
            run_ps = prompt_yn("3. Prepare Google Play Console keys, metadata & Fastlane supply?", "y")
        except (KeyboardInterrupt, EOFError):
            print("\n❌ Wizard cancelled by user.")
            sys.exit(0)

    results = {}

    if run_fb:
        results["firebase"] = setup_firebase(target_path, meta, project_id=args.project_id, dry_run=args.dry_run)

    if run_as:
        results["appstore"] = setup_appstore(target_path, meta, apple_id=args.apple_id, team_id=args.team_id, dry_run=args.dry_run)

    if run_ps:
        results["playstore"] = setup_playstore(target_path, meta, dry_run=args.dry_run, use_moltaqa=args.moltaqa)

    # Summary
    print("\n" + "="*70)
    print("  PROVISIONING SUMMARY REPORT")
    print("="*70)
    for service, status in results.items():
        icon = "✅" if status else "⚠️"
        print(f"   {icon} {service.upper():<12}: {'READY / CONFIGURED' if status else 'ACTION REQUIRED / REVIEW OUTPUT'}")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
