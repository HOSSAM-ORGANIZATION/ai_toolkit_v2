#!/usr/bin/env python3
"""
Universal AI Toolkit v2 — Granular Permissions & iOS Podfile Setup Engine
Configures AndroidManifest.xml permissions, <queries>, iOS Info.plist UsageDescriptions,
and iOS Podfile GCC_PREPROCESSOR_DEFINITIONS macros strictly per requested modules.
Uses Python Standard Library ONLY (zero pip dependencies).
"""

import sys
import os
import re
import argparse
from pathlib import Path

# Granular definitions
MODULES = {
    "core": {
        "section_header": "<!-- INTERNET AND NETWORK -->",
        "section_footer": None,
        "android_permissions": [
            '<uses-permission android:name="android.permission.INTERNET" />',
            '<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />'
        ],
        "android_queries": """    <queries>
        <intent>
            <action android:name="android.intent.action.PROCESS_TEXT" />
            <data android:mimeType="text/plain" />
        </intent>
        <!-- If your app checks for SMS support -->
        <intent>
            <action android:name="android.intent.action.VIEW" />
            <data android:scheme="sms" />
        </intent>
        <!-- If your app checks for call support -->
        <intent>
            <action android:name="android.intent.action.VIEW" />
            <data android:scheme="tel" />
        </intent>
        <!-- If your application checks for inAppBrowserView launch mode support -->
        <intent>
            <action android:name="android.support.customtabs.action.CustomTabsService" />
        </intent>
        <intent>
            <action android:name="android.intent.action.VIEW" />
            <category android:name="android.intent.category.BROWSABLE" />
            <data android:scheme="https" />
        </intent>
    </queries>""",
        "ios_plist": {},
        "podfile_macros": []
    },
    "notifications": {
        "section_header": "<!-- NOTIFICATION PERMISSION START -->",
        "section_footer": "<!-- NOTIFICATION PERMISSION END -->",
        "android_permissions": [
            '<uses-permission android:name="android.permission.POST_NOTIFICATIONS" />',
            '<uses-permission android:name="android.permission.RECEIVE_BOOT_COMPLETED" />',
            '<uses-permission android:name="android.permission.VIBRATE" />'
        ],
        "android_queries": None,
        "ios_plist": {},
        "podfile_macros": ["PERMISSION_NOTIFICATIONS=1"]
    },
    "location": {
        "section_header": "<!-- LOCATION PERMISSION START -->",
        "section_footer": "<!-- LOCATION PERMISSION END -->",
        "android_permissions": [
            '<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />',
            '<uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />',
            '<uses-permission android:name="android.permission.FOREGROUND_SERVICE" />'
        ],
        "android_queries": None,
        "ios_plist": {
            "NSLocationWhenInUseUsageDescription": "App requires your location to display nearby places, branches, or delivery addresses.",
            "NSLocationAlwaysAndWhenInUseUsageDescription": "App requires your location to provide accurate navigation and tracking."
        },
        "podfile_macros": ["PERMISSION_LOCATION=1"]
    },
    "media": {
        "section_header": "<!-- CAMERA & AUDIO (CHAT / QR / ATTACHMENTS) PERMISSION START -->",
        "section_footer": "<!-- CAMERA & AUDIO (CHAT / QR / ATTACHMENTS) PERMISSION END -->",
        "android_permissions": [
            '<uses-permission android:name="android.permission.CAMERA" />',
            '<uses-permission android:name="android.permission.RECORD_AUDIO" />',
            '<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" android:maxSdkVersion="32" />',
            '<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" android:maxSdkVersion="28" />'
        ],
        "android_queries": None,
        "ios_plist": {
            "NSCameraUsageDescription": "App requires access to the camera to scan QR codes and capture photos.",
            "NSMicrophoneUsageDescription": "App requires access to the microphone for recording audio and voice notes in chat.",
            "NSPhotoLibraryUsageDescription": "App requires access to your photo library to select images and chat attachments."
        },
        "podfile_macros": ["PERMISSION_CAMERA=1", "PERMISSION_MICROPHONE=1", "PERMISSION_PHOTOS=1"]
    }
}

def setup_permissions(target_dir=".", active_modules=None):
    target_path = Path(target_dir).resolve()
    android_manifest = target_path / "android" / "app" / "src" / "main" / "AndroidManifest.xml"
    ios_plist = target_path / "ios" / "Runner" / "Info.plist"
    podfile = target_path / "ios" / "Podfile"

    if active_modules is None:
        active_modules = ["core"]
    elif isinstance(active_modules, str):
        active_modules = [m.strip().lower() for m in active_modules.split(",") if m.strip()]

    # Interactive prompt if only core or unspecified and run in terminal
    if (active_modules == ["core"]) and sys.stdin.isatty():
        print("\n  📱 Select which optional permission modules to configure:")
        print("    [1] Camera & Audio / Chat & QR (الكاميرا والمايك للشات، الملاحظات الصوتية ومسح QR)")
        print("    [2] Location (الموقع الجغرافي والخرائط)")
        print("    [3] Notifications (الإشعارات والتنبيهات)")
        ans = input("  👉 Select [e.g. 1,3 or Enter for core network only]: ").strip()
        if ans:
            active_modules = ["core"]
            sel = [s.strip() for s in ans.replace(" ", ",").split(",") if s.strip()]
            if "1" in sel: active_modules.append("media")
            if "2" in sel: active_modules.append("location")
            if "3" in sel: active_modules.append("notifications")

    # Core is always included
    if "core" not in active_modules:
        active_modules.insert(0, "core")

    print("\n" + "🛡️"*35)
    print("  UNIVERSAL AI TOOLKIT v2 — GRANULAR PERMISSIONS SETUP")
    print("🛡️"*35)
    print(f"📂 Project Root: {target_path}")
    print(f"🧩 Active Permission Modules: {', '.join(active_modules)}")

    # 1. Update AndroidManifest.xml
    if not android_manifest.exists() and (target_path / "android").exists():
        android_manifest.parent.mkdir(parents=True, exist_ok=True)
        with open(android_manifest, "w", encoding="utf-8") as f:
            f.write('<manifest xmlns:android="http://schemas.android.com/apk/res/android">\n    <application>\n    </application>\n</manifest>\n')

    if android_manifest.exists():
        with open(android_manifest, "r", encoding="utf-8") as f:
            m_content = f.read()

        total_added = 0
        section_blocks = []
        for mod in active_modules:
            if mod in MODULES:
                needed = []
                for perm in MODULES[mod]["android_permissions"]:
                    m_perm = re.search(r'android:name="([^"]+)"', perm)
                    if m_perm and m_perm.group(1) not in m_content:
                        needed.append(perm)
                        total_added += 1

                if needed:
                    lines = []
                    header = MODULES[mod].get("section_header")
                    footer = MODULES[mod].get("section_footer")
                    if header and header not in m_content:
                        lines.append(header)
                    lines.extend(needed)
                    if footer and footer not in m_content:
                        lines.append(footer)
                    section_blocks.append("\n    ".join(lines))

        if section_blocks:
            perms_text = "\n\n    " + "\n\n    ".join(section_blocks)
            m_content = re.sub(r"(<manifest[^\>]*\>)", r"\1" + perms_text, m_content, count=1)

        # Queries
        if "<queries>" not in m_content and MODULES["core"]["android_queries"]:
            # Insert before </manifest>
            m_content = re.sub(r"(\s*<\/manifest>)", "\n" + MODULES["core"]["android_queries"] + r"\1", m_content, count=1)

        with open(android_manifest, "w", encoding="utf-8") as f:
            f.write(m_content)
        print(f"   ✅ Updated AndroidManifest.xml with {total_added} permissions & <queries>")

    # 2. Update Info.plist
    if ios_plist.exists():
        with open(ios_plist, "r", encoding="utf-8") as f:
            p_content = f.read()

        added_plist = []
        for mod in active_modules:
            if mod in MODULES:
                for k, desc in MODULES[mod]["ios_plist"].items():
                    if f"<key>{k}</key>" not in p_content:
                        added_plist.append(f"\t<key>{k}</key>\n\t<string>{desc}</string>")

        if added_plist:
            plist_block = "\n" + "\n".join(added_plist)
            p_content = re.sub(r"(<dict>)", r"\1" + plist_block, p_content, count=1)
            with open(ios_plist, "w", encoding="utf-8") as f:
                f.write(p_content)
            print(f"   ✅ Updated ios/Runner/Info.plist with {len(added_plist)} UsageDescriptions")

    # 3. Update Podfile macros for permission_handler
    if podfile.exists():
        needed_macros = []
        for mod in active_modules:
            if mod in MODULES:
                needed_macros.extend(MODULES[mod]["podfile_macros"])

        if needed_macros:
            with open(podfile, "r", encoding="utf-8") as f:
                pod_content = f.read()

            macros_code = "\n".join([f"        '{m}'," for m in needed_macros])
            if "PERMISSION_" not in pod_content:
                post_install_block = f"""
post_install do |installer|
  installer.pods_project.targets.each do |target|
    flutter_additional_ios_build_settings(target)
    target.build_configurations.each do |config|
      config.build_settings['GCC_PREPROCESSOR_DEFINITIONS'] ||= ['$(inherited)']
      config.build_settings['GCC_PREPROCESSOR_DEFINITIONS'] += [
{macros_code}
      ]
    end
  end
end
"""
                with open(podfile, "a", encoding="utf-8") as f:
                    f.write(post_install_block)
                print(f"   ✅ Injected GCC_PREPROCESSOR_DEFINITIONS ({len(needed_macros)} macros) into ios/Podfile")

    print("\n🎉 Granular permissions setup completed successfully!")
    print("="*70 + "\n")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Universal AI Toolkit Permissions Setup")
    parser.add_argument("target", nargs="?", default=".", help="Target project root directory")
    parser.add_argument("--modules", default="core", help="Comma-separated modules: core, media, location, notifications")
    args = parser.parse_args()

    setup_permissions(args.target, active_modules=args.modules)
