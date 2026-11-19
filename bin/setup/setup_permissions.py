#!/usr/bin/env python3
"""
Universal AI Toolkit v2 — Granular Permissions, Maps & Deep Linking Setup Engine
Configures AndroidManifest.xml permissions, <queries>, Google Maps, Deep Linking,
iOS Info.plist UsageDescriptions, AppDelegate.swift GMSServices, and iOS Podfile macros.
Uses Python Standard Library ONLY (zero pip dependencies).
"""

import sys
import os
import re
import argparse
import subprocess
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
            '<uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />'
        ],
        "android_queries": None,
        "ios_plist": {
            "NSLocationWhenInUseUsageDescription": "App requires your location to display nearby places, branches, or delivery addresses."
        },
        "podfile_macros": ["PERMISSION_LOCATION=1"]
    },
    "live_tracking": {
        "section_header": "<!-- LIVE TRACKING & FOREGROUND SERVICE PERMISSION START -->",
        "section_footer": "<!-- LIVE TRACKING & FOREGROUND SERVICE PERMISSION END -->",
        "android_permissions": [
            '<uses-permission android:name="android.permission.FOREGROUND_SERVICE" />',
            '<uses-permission android:name="android.permission.FOREGROUND_SERVICE_LOCATION" />',
            '<uses-permission android:name="android.permission.ACCESS_BACKGROUND_LOCATION" />'
        ],
        "android_queries": None,
        "ios_plist": {
            "NSLocationAlwaysAndWhenInUseUsageDescription": "App requires continuous location access for live tracking and navigation."
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

def extract_sha256_fingerprints(target_path: Path):
    """
    Attempts to extract SHA-256 certificate fingerprints using `./gradlew signingReport`.
    Works across macOS, Linux, and Windows.
    """
    results = {
        "debug": None,
        "release": None,
        "all": []
    }
    android_dir = target_path / "android"
    if not android_dir.exists():
        return results

    gradlew_bin = android_dir / ("gradlew.bat" if os.name == "nt" else "gradlew")
    if not gradlew_bin.exists():
        return results

    try:
        if os.name != "nt":
            os.chmod(gradlew_bin, 0o755)

        proc = subprocess.run(
            [str(gradlew_bin.resolve()), "signingReport"],
            cwd=str(android_dir),
            capture_output=True,
            text=True,
            timeout=45
        )
        output = proc.stdout or ""

        # Parse variants
        blocks = re.split(r'-{5,}', output)
        for b in blocks:
            v_match = re.search(r'Variant:\s*([a-zA-Z0-9_]+)', b)
            sha_match = re.search(r'SHA-256:\s*([0-9A-F:]{50,})', b, re.IGNORECASE)
            if sha_match:
                sha_val = sha_match.group(1).strip().upper()
                if sha_val not in results["all"]:
                    results["all"].append(sha_val)
                if v_match:
                    var_name = v_match.group(1).lower()
                    if "debug" in var_name and not results["debug"]:
                        results["debug"] = sha_val
                    elif "release" in var_name and not results["release"]:
                        results["release"] = sha_val
    except Exception:
        pass

    return results

def detect_app_identifiers(target_path: Path):
    """Auto-detects package name (Android), bundle ID (iOS), and Apple Team ID."""
    info = {
        "package_name": "app-package-name",
        "bundle_id": "app-bundle-id",
        "team_id": "team-id",
    }

    # 1. Check project_profile.yaml
    profile_path = target_path / "project_profile.yaml"
    if profile_path.exists():
        try:
            with open(profile_path, "r", encoding="utf-8") as f:
                content = f.read()
                m_pkg = re.search(r'(?:android_package|package_name)\s*:\s*["\']?([^"\'\n]+)["\']?', content)
                if m_pkg: info["package_name"] = m_pkg.group(1).strip()
                m_bid = re.search(r'(?:ios_bundle_id|bundle_id)\s*:\s*["\']?([^"\'\n]+)["\']?', content)
                if m_bid: info["bundle_id"] = m_bid.group(1).strip()
                m_tid = re.search(r'(?:apple_team_id|team_id)\s*:\s*["\']?([^"\'\n]+)["\']?', content)
                if m_tid: info["team_id"] = m_tid.group(1).strip()
        except Exception:
            pass

    # 2. Check Android gradle (build.gradle.kts or build.gradle)
    for g_path in [target_path / "android" / "app" / "build.gradle.kts", target_path / "android" / "app" / "build.gradle"]:
        if g_path.exists():
            try:
                with open(g_path, "r", encoding="utf-8") as f:
                    txt = f.read()
                    m_ns = re.search(r'(?:namespace|applicationId)\s*[=\s]\s*["\']([^"\']+)["\']', txt)
                    if m_ns and info["package_name"] == "app-package-name":
                        info["package_name"] = m_ns.group(1).strip()
                        break
            except Exception:
                pass

    # 3. Check AndroidManifest.xml package attribute
    manifest_path = target_path / "android" / "app" / "src" / "main" / "AndroidManifest.xml"
    if manifest_path.exists() and info["package_name"] == "app-package-name":
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                m_man = re.search(r'package\s*=\s*["\']([^"\']+)["\']', f.read())
                if m_man: info["package_name"] = m_man.group(1).strip()
        except Exception:
            pass

    # 4. Check iOS project.pbxproj
    pbxproj = target_path / "ios" / "Runner.xcodeproj" / "project.pbxproj"
    if pbxproj.exists():
        try:
            with open(pbxproj, "r", encoding="utf-8") as f:
                txt = f.read()
                if info["bundle_id"] == "app-bundle-id":
                    m_bid = re.search(r'PRODUCT_BUNDLE_IDENTIFIER\s*=\s*([^;]+);', txt)
                    if m_bid:
                        bid = m_bid.group(1).strip().strip('"\'')
                        if bid and not bid.startswith("$("):
                            info["bundle_id"] = bid
                if info["team_id"] == "team-id":
                    m_team = re.search(r'DEVELOPMENT_TEAM\s*=\s*([^;]+);', txt)
                    if m_team:
                        tid = m_team.group(1).strip().strip('"\'')
                        if tid and tid != '""':
                            info["team_id"] = tid
        except Exception:
            pass

    # Fallback sync between bundle_id and package_name if one was found and other wasn't
    if info["bundle_id"] == "app-bundle-id" and info["package_name"] != "app-package-name":
        info["bundle_id"] = info["package_name"]
    elif info["package_name"] == "app-package-name" and info["bundle_id"] != "app-bundle-id":
        info["package_name"] = info["bundle_id"]

    return info

def setup_permissions(target_dir=".", active_modules=None, live_tracking=False, maps_api_key=None, deep_link_domain=None, package_name=None, bundle_id=None, team_id=None):
    target_path = Path(target_dir).resolve()
    android_manifest = target_path / "android" / "app" / "src" / "main" / "AndroidManifest.xml"
    ios_plist = target_path / "ios" / "Runner" / "Info.plist"
    ios_app_delegate = target_path / "ios" / "Runner" / "AppDelegate.swift"
    podfile = target_path / "ios" / "Podfile"

    if active_modules is None:
        active_modules = ["core"]
    elif isinstance(active_modules, str):
        active_modules = [m.strip().lower() for m in active_modules.split(",") if m.strip()]

    # Interactive prompt if running in terminal and no specific flags were provided
    if (active_modules == ["core"] and not live_tracking and maps_api_key is None and deep_link_domain is None) and sys.stdin.isatty():
        print("\n" + "🛡️"*35)
        print("  UNIVERSAL AI TOOLKIT v2 — CAPABILITIES & PERMISSIONS WIZARD")
        print("🛡️"*35)
        print("  [1] Camera & Audio / Chat & QR (الكاميرا والمايك للشات، الملاحظات الصوتية ومسح QR)")
        print("  [2] Location (الموقع الجغرافي والخرائط)")
        print("  [3] Notifications (الإشعارات والتنبيهات)")
        ans = input("👉 Select permissions to enable [e.g. 1,2,3 or Enter for core only]: ").strip()
        if ans:
            active_modules = ["core"]
            sel = [s.strip() for s in ans.replace(" ", ",").split(",") if s.strip()]
            if "1" in sel: active_modules.append("media")
            if "2" in sel: active_modules.append("location")
            if "3" in sel: active_modules.append("notifications")

        if "location" in active_modules:
            lt_ans = input("👉 Does this app require Background Live Tracking (تتبع مباشر في الخلفية كباتن/توصيل)؟ [y/N]: ").strip().lower()
            if lt_ans in ["y", "yes"]:
                live_tracking = True

        maps_ans = input("👉 Does this app use Google Maps (خرائط جوجل)؟ [y/N]: ").strip().lower()
        if maps_ans in ["y", "yes"]:
            k_input = input("   Enter Google Maps API Key [or press Enter to leave empty]: ").strip()
            maps_api_key = k_input

        dl_ans = input("👉 Does this app require Deep Linking / App Links؟ [y/N]: ").strip().lower()
        if dl_ans in ["y", "yes"]:
            d_input = input("   Enter your domain [e.g. example.com or press Enter to leave empty]: ").strip()
            deep_link_domain = d_input

            detected = detect_app_identifiers(target_path)
            
            p_in = input(f"   Enter Android Package Name [press Enter for '{detected['package_name']}']: ").strip()
            package_name = p_in if p_in else detected["package_name"]

            b_in = input(f"   Enter iOS Bundle ID [press Enter for '{detected['bundle_id']}']: ").strip()
            bundle_id = b_in if b_in else detected["bundle_id"]

            t_in = input(f"   Enter Apple Team ID [press Enter for '{detected['team_id']}']: ").strip()
            team_id = t_in if t_in else detected["team_id"]

    # Resolve app identifiers if not already resolved
    detected_info = detect_app_identifiers(target_path)
    if not package_name:
        package_name = detected_info["package_name"]
    if not bundle_id:
        bundle_id = detected_info["bundle_id"]
    if not team_id:
        team_id = detected_info["team_id"]

    # Core is always included
    if "core" not in active_modules:
        active_modules.insert(0, "core")

    # Add live tracking module if enabled
    if live_tracking and "live_tracking" not in active_modules:
        active_modules.append("live_tracking")

    print("\n" + "🛡️"*35)
    print("  UNIVERSAL AI TOOLKIT v2 — GRANULAR PERMISSIONS SETUP")
    print("🛡️"*35)
    print(f"📂 Project Root: {target_path}")
    print(f"🧩 Active Permission Modules: {', '.join(active_modules)}")
    if live_tracking:
        print("📍 Live Background Tracking: Enabled")
    if maps_api_key is not None:
        key_display = maps_api_key[:8] + "..." if maps_api_key else "(empty)"
        print(f"🗺️ Google Maps API Key: Configured {key_display}")
    if deep_link_domain is not None:
        domain_display = deep_link_domain if deep_link_domain else "(empty)"
        print(f"🔗 Deep Linking Domain: {domain_display}")
        print(f"📦 Package Name: {package_name}")
        print(f"🍎 iOS Bundle ID: {bundle_id}")
        print(f"👥 Apple Team ID: {team_id}")

    # 1. Update AndroidManifest.xml
    if not android_manifest.exists() and (target_path / "android").exists():
        android_manifest.parent.mkdir(parents=True, exist_ok=True)
        with open(android_manifest, "w", encoding="utf-8") as f:
            f.write('<manifest xmlns:android="http://schemas.android.com/apk/res/android">\n    <application>\n        <activity android:name=".MainActivity">\n        </activity>\n    </application>\n</manifest>\n')

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
            m_content = re.sub(r"(\s*<\/manifest>)", "\n" + MODULES["core"]["android_queries"] + r"\1", m_content, count=1)

        # Google Maps Meta-Data
        if maps_api_key is not None and "com.google.android.geo.API_KEY" not in m_content:
            maps_block = f"""
        <!-- Google Maps API Key -->
        <meta-data
            android:name="com.google.android.geo.API_KEY"
            android:value="{maps_api_key}" />"""
            m_content = re.sub(r"(\s*<\/application>)", maps_block + r"\1", m_content, count=1)
            print("   ✅ Injected Google Maps meta-data into AndroidManifest.xml")

        # Deep Linking Intent-Filter & Meta-Data
        if deep_link_domain is not None:
            if "android:host=" not in m_content:
                dl_filter = f"""
            <!-- Deep Linking / App Links -->
            <intent-filter android:autoVerify="true">
                <action android:name="android.intent.action.VIEW" />
                <category android:name="android.intent.category.DEFAULT" />
                <category android:name="android.intent.category.BROWSABLE" />
                <data android:scheme="http" android:host="{deep_link_domain}" />
                <data android:scheme="https" android:host="{deep_link_domain}" />
            </intent-filter>"""
                # Insert inside the activity tag
                if "</activity>" in m_content:
                    m_content = re.sub(r"(\s*<\/activity>)", dl_filter + r"\1", m_content, count=1)
                else:
                    m_content = re.sub(r"(\s*<\/application>)", dl_filter + r"\1", m_content, count=1)
                print(f"   ✅ Injected App Links intent-filter for '{deep_link_domain}' into AndroidManifest.xml")

            if "flutter_deeplinking_enabled" not in m_content:
                dl_meta = """
        <!-- Flutter Deep Linking Routing Control (false = handled via app_links/uni_links) -->
        <meta-data android:name="flutter_deeplinking_enabled" android:value="false" />"""
                m_content = re.sub(r"(\s*<\/application>)", dl_meta + r"\1", m_content, count=1)
                print("   ✅ Injected flutter_deeplinking_enabled meta-data into AndroidManifest.xml")

        with open(android_manifest, "w", encoding="utf-8") as f:
            f.write(m_content)
        print(f"   ✅ Updated AndroidManifest.xml with {total_added} permissions & <queries>")

        # Generate deeplink-assets/ folder with assetlinks.json and apple-app-site-association
        if deep_link_domain is not None:
            deeplink_dir = target_path / "deeplink-assets"
            deeplink_dir.mkdir(parents=True, exist_ok=True)

            # Auto-infer SHA-256 fingerprints via `./gradlew signingReport`
            extracted_shas = extract_sha256_fingerprints(target_path)
            shas = []
            if extracted_shas["all"]:
                shas.extend(extracted_shas["all"])
                if "play-store-release" not in shas:
                    shas.append("play-store-release")
                print(f"   🔑 Inferred {len(extracted_shas['all'])} SHA-256 fingerprint(s) via ./gradlew signingReport")
            else:
                shas = [
                    "device-release",
                    "play-store-release",
                    "device-debug"
                ]

            sha_json_lines = ",\n        ".join([f'"{s}"' for s in shas])

            assetlinks_content = f"""[
  {{
    "relation": ["delegate_permission/common.handle_all_urls"],
    "target": {{
      "namespace": "android_app",
      "package_name": "{package_name}",
      "sha256_cert_fingerprints": [
        {sha_json_lines}
      ]
    }}
  }}
]
"""
            apple_site_assoc = f"""{{
  "applinks": {{
    "apps": [],
    "details": [
      {{
        "appIDs": [
          "{team_id}.{bundle_id}"
        ],
        "paths": [
          "*"
        ],
        "components": [
          {{
            "/": "/*"
          }}
        ]
      }}
    ]
  }},
  "webcredentials": {{
    "apps": [
      "{team_id}.{bundle_id}"
    ]
  }}
}}
"""
            with open(deeplink_dir / "assetlinks.json", "w", encoding="utf-8") as f:
                f.write(assetlinks_content)
            with open(deeplink_dir / "apple-app-site-association", "w", encoding="utf-8") as f:
                f.write(apple_site_assoc)
            print("   ✅ Generated deeplink-assets/assetlinks.json & apple-app-site-association")

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

        # Live tracking iOS Background Modes
        if live_tracking and "UIBackgroundModes" not in p_content:
            added_plist.append("\t<key>UIBackgroundModes</key>\n\t<array>\n\t\t<string>location</string>\n\t</array>")

        # Deep Linking for iOS (CFBundleURLTypes + FlutterDeepLinkingEnabled)
        if deep_link_domain is not None:
            if "CFBundleURLTypes" not in p_content:
                dl_ios_block = f"""\t<key>CFBundleURLTypes</key>
\t<array>
\t\t<dict>
\t\t\t<key>CFBundleTypeRole</key>
\t\t\t<string>Editor</string>
\t\t\t<key>CFBundleURLName</key>
\t\t\t<string>{deep_link_domain}</string>
\t\t\t<key>CFBundleURLSchemes</key>
\t\t\t<array>
\t\t\t\t<string>https</string>
\t\t\t\t<string>http</string>
\t\t\t</array>
\t\t</dict>
\t</array>"""
                added_plist.append(dl_ios_block)

            if "FlutterDeepLinkingEnabled" not in p_content:
                added_plist.append("\t<key>FlutterDeepLinkingEnabled</key>\n\t<false/>")

        if added_plist:
            plist_block = "\n" + "\n".join(added_plist)
            p_content = re.sub(r"(<dict>)", r"\1" + plist_block, p_content, count=1)
            with open(ios_plist, "w", encoding="utf-8") as f:
                f.write(p_content)
            print(f"   ✅ Updated ios/Runner/Info.plist with {len(added_plist)} keys & UsageDescriptions")

    # 3. Update iOS AppDelegate.swift for Google Maps
    if maps_api_key is not None and ios_app_delegate.exists():
        with open(ios_app_delegate, "r", encoding="utf-8") as f:
            app_del = f.read()

        changed_del = False
        if "import GoogleMaps" not in app_del:
            app_del = re.sub(r"(import Flutter\s*)", r"\1import GoogleMaps\n", app_del, count=1)
            changed_del = True

        if "GMSServices.provideAPIKey" not in app_del:
            gms_call = f'    GMSServices.provideAPIKey("{maps_api_key}")\n'
            if "GeneratedPluginRegistrant.register" in app_del:
                app_del = app_del.replace("GeneratedPluginRegistrant.register", gms_call + "    GeneratedPluginRegistrant.register", 1)
                changed_del = True

        if changed_del:
            with open(ios_app_delegate, "w", encoding="utf-8") as f:
                f.write(app_del)
            print("   ✅ Configured GMSServices.provideAPIKey in ios/Runner/AppDelegate.swift")

    # 4. Update Podfile macros for permission_handler
    if podfile.exists():
        needed_macros = []
        for mod in active_modules:
            if mod in MODULES:
                needed_macros.extend(MODULES[mod]["podfile_macros"])

        if needed_macros:
            with open(podfile, "r", encoding="utf-8") as f:
                pod_content = f.read()

            macros_code = "\n".join([f"        '{m}'," for m in set(needed_macros)])
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

    print("\n🎉 Permissions, Maps & Deep Linking setup completed successfully!")
    print("="*70 + "\n")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Universal AI Toolkit Permissions Setup")
    parser.add_argument("target", nargs="?", default=".", help="Target project root directory")
    parser.add_argument("--modules", default="core", help="Comma-separated modules: core, media, location, notifications")
    parser.add_argument("--live-tracking", action="store_true", help="Enable background live tracking permissions")
    parser.add_argument("--maps-key", help="Google Maps API Key")
    parser.add_argument("--deep-link-domain", help="Deep linking domain (e.g. pays-you.com)")
    parser.add_argument("--package-name", help="Android Package Name")
    parser.add_argument("--bundle-id", help="iOS Bundle ID")
    parser.add_argument("--team-id", help="Apple Team ID")
    args = parser.parse_args()

    setup_permissions(
        args.target,
        active_modules=args.modules,
        live_tracking=args.live_tracking,
        maps_api_key=args.maps_key,
        deep_link_domain=args.deep_link_domain,
        package_name=args.package_name,
        bundle_id=args.bundle_id,
        team_id=args.team_id
    )
