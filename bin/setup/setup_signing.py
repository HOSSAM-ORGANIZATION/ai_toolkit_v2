#!/usr/bin/env python3
"""
Universal AI Toolkit v2 — Release Signing & ProGuard Setup Engine
Configures secure Android keystore properties, Gradle release signing,
and production-ready ProGuard / R8 code shrinking and resource optimization.
Uses Python Standard Library ONLY (zero pip dependencies).
"""

import sys
import os
import re
import shutil
import argparse
from pathlib import Path

TOOLKIT_ROOT = Path(__file__).resolve().parent.parent.parent

def detect_moltaqa_context(target_path: Path) -> bool:
    """Detects whether target project is configured with Moltaqa preset or naming."""
    profile = target_path / "project_profile.yaml"
    if profile.exists():
        try:
            content = profile.read_text(encoding="utf-8")
            if 'preset: "moltaqa"' in content or 'preset: moltaqa' in content or 'moltaqa' in content.lower():
                return True
        except Exception:
            pass

    pubspec = target_path / "pubspec.yaml"
    if pubspec.exists():
        try:
            content = pubspec.read_text(encoding="utf-8")
            if "moltaqa" in content.lower():
                return True
        except Exception:
            pass

    # Check build.gradle namespace / applicationId
    app_dir = target_path / "android" / "app"
    for g in [app_dir / "build.gradle.kts", app_dir / "build.gradle"]:
        if g.exists():
            try:
                if "moltaqa" in g.read_text(encoding="utf-8").lower():
                    return True
            except Exception:
                pass

    return False

def setup_signing(target_dir=".", use_moltaqa=False, enable_proguard=True):
    target_path = Path(target_dir).resolve()
    android_dir = target_path / "android"
    app_dir = android_dir / "app"

    print("\n" + "🔐"*35)
    print("  UNIVERSAL AI TOOLKIT v2 — RELEASE SIGNING & PROGUARD SETUP")
    print("🔐"*35)
    print(f"📂 Project Root: {target_path}")

    android_dir.mkdir(parents=True, exist_ok=True)
    app_dir.mkdir(parents=True, exist_ok=True)

    is_moltaqa = use_moltaqa or detect_moltaqa_context(target_path)
    moltaqa_template_dir = TOOLKIT_ROOT / "templates" / "signing" / "moltaqa"

    # 1. Install Keystore & key.properties
    if is_moltaqa and moltaqa_template_dir.exists():
        print("   🏢 Detected Moltaqa Enterprise Environment / Standard Keystore")
        moltaqa_key_prop = moltaqa_template_dir / "key.properties"
        target_key_prop = android_dir / "key.properties"
        if moltaqa_key_prop.exists():
            shutil.copy2(moltaqa_key_prop, target_key_prop)
            print("   ✅ Installed Moltaqa standard: android/key.properties")

        moltaqa_keystore = moltaqa_template_dir / "upload-keystore.jks"
        target_keystore = app_dir / "upload-keystore.jks"
        if moltaqa_keystore.exists():
            shutil.copy2(moltaqa_keystore, target_keystore)
            print("   ✅ Installed Moltaqa upload keystore: android/app/upload-keystore.jks")
    else:
        key_example = android_dir / "key.properties.example"
        key_prop = android_dir / "key.properties"
        if not key_example.exists() and not key_prop.exists():
            with open(key_example, "w", encoding="utf-8") as f:
                f.write("""# Production Keystore Configuration Example
# Copy this file to key.properties and fill with your actual credentials.
# NEVER commit key.properties to version control!
keyAlias=my_key_alias
keyPassword=my_key_password
storeFile=../my_release_key.jks
storePassword=my_store_password
""")
            print("   ✅ Created: android/key.properties.example")

    # 2. Update .gitignore (unless moltaqa where keystore is shared among devs)
    if not is_moltaqa:
        gitignore = target_path / ".gitignore"
        if gitignore.exists():
            with open(gitignore, "r", encoding="utf-8") as f:
                gi_content = f.read()
            needed_ignores = []
            for ign in ["key.properties", "*.jks", "*.keystore"]:
                if ign not in gi_content:
                    needed_ignores.append(ign)
            if needed_ignores:
                with open(gitignore, "a", encoding="utf-8") as f:
                    f.write("\n# Android Release Keystore & Secrets\n" + "\n".join(needed_ignores) + "\n")
                print(f"   ✅ Added keystore files to .gitignore ({', '.join(needed_ignores)})")

    # 3. Setup ProGuard / R8 rules file
    if enable_proguard:
        proguard_template = TOOLKIT_ROOT / "templates" / "android" / "proguard-rules.pro"
        target_proguard = app_dir / "proguard-rules.pro"
        if not target_proguard.exists() and proguard_template.exists():
            shutil.copy2(proguard_template, target_proguard)
            print("   🛡️  Installed ProGuard/R8 rules: android/app/proguard-rules.pro")
        elif target_proguard.exists():
            print("   ℹ️  Existing proguard-rules.pro found in android/app/")

    # 4. Inject safe signing & ProGuard config into Gradle
    kts_file = app_dir / "build.gradle.kts"
    groovy_file = app_dir / "build.gradle"

    proguard_kts_block = """            isMinifyEnabled = true
            isShrinkResources = true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                file("proguard-rules.pro")
            )""" if enable_proguard else ""

    proguard_groovy_block = """            minifyEnabled true
            shrinkResources true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'""" if enable_proguard else ""

    if kts_file.exists():
        with open(kts_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Add keystore loading at the top
        if "keystoreProperties" not in content:
            load_block = """import java.util.Properties
import java.io.FileInputStream

val keystoreProperties = Properties()
val keystorePropertiesFile = rootProject.file("key.properties")
if (keystorePropertiesFile.exists()) {
    keystoreProperties.load(FileInputStream(keystorePropertiesFile))
}

"""
            content = load_block + content

        # Add signingConfigs and buildTypes release config
        if "signingConfigs" not in content and "android {" in content:
            signing_block = f"""    signingConfigs {{
        create("release") {{
            keyAlias = keystoreProperties.getProperty("keyAlias")
            keyPassword = keystoreProperties.getProperty("keyPassword")
            storeFile = keystoreProperties.getProperty("storeFile")?.let {{ file(it) }}
            storePassword = keystoreProperties.getProperty("storePassword")
        }}
    }}

    buildTypes {{
        release {{
            signingConfig = if (keystorePropertiesFile.exists()) {{
                signingConfigs.getByName("release")
            }} else {{
                signingConfigs.getByName("debug")
            }}
{proguard_kts_block}
        }}
    }}
"""
            content = re.sub(r"(android\s*\{)", r"\1\n" + signing_block, content, count=1)
            with open(kts_file, "w", encoding="utf-8") as f:
                f.write(content)
            print("   ✅ Configured release signing & ProGuard in android/app/build.gradle.kts")
    elif groovy_file.exists():
        with open(groovy_file, "r", encoding="utf-8") as f:
            content = f.read()

        if "keystoreProperties" not in content:
            load_block = """def keystoreProperties = new Properties()
def keystorePropertiesFile = rootProject.file('key.properties')
if (keystorePropertiesFile.exists()) {
    keystoreProperties.load(new FileInputStream(keystorePropertiesFile))
}

"""
            content = load_block + content

        if "signingConfigs" not in content and "android {" in content:
            signing_block = f"""    signingConfigs {{
        release {{
            keyAlias keystoreProperties['keyAlias']
            keyPassword keystoreProperties['keyPassword']
            storeFile keystoreProperties['storeFile'] ? file(keystoreProperties['storeFile']) : null
            storePassword keystoreProperties['storePassword']
        }}
    }}

    buildTypes {{
        release {{
            signingConfig = keystorePropertiesFile.exists() ? signingConfigs.release : signingConfigs.debug
{proguard_groovy_block}
        }}
    }}
"""
            content = re.sub(r"(android\s*\{)", r"\1\n" + signing_block, content, count=1)
            with open(groovy_file, "w", encoding="utf-8") as f:
                f.write(content)
            print("   ✅ Configured release signing & ProGuard in android/app/build.gradle")

    print("\n🎉 Release signing & ProGuard setup completed successfully!")
    print("="*70 + "\n")
    return True

def main():
    parser = argparse.ArgumentParser(description="Universal AI Toolkit v2 — Release Signing & ProGuard Setup Engine")
    parser.add_argument("target", nargs="?", default=".", help="Target Flutter project directory (default: .)")
    parser.add_argument("--moltaqa", action="store_true", help="Force install Moltaqa standard release keystore (upload-keystore.jks & key.properties)")
    parser.add_argument("--no-proguard", action="store_true", help="Disable ProGuard / R8 shrinking and obfuscation")
    args = parser.parse_args()

    setup_signing(args.target, use_moltaqa=args.moltaqa, enable_proguard=not args.no_proguard)

if __name__ == "__main__":
    main()
