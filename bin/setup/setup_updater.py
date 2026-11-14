#!/usr/bin/env python3
"""
Universal AI Toolkit v2 — Force Store Update Setup Engine
Scaffolds a clean, lightweight App Version & Force Update service.
Uses Python Standard Library ONLY (zero pip dependencies).
"""

import sys
import os
from pathlib import Path

def setup_store_updater(target_dir="."):
    target_path = Path(target_dir).resolve()
    updater_dir = target_path / "lib" / "core" / "services" / "store_updater"
    updater_dir.mkdir(parents=True, exist_ok=True)

    print("\n" + "🚀"*35)
    print("  UNIVERSAL AI TOOLKIT v2 — STORE UPDATER SETUP")
    print("🚀"*35)
    print(f"📂 Project Root: {target_path}")

    updater_file = updater_dir / "store_updater.dart"
    if not updater_file.exists():
        with open(updater_file, "w", encoding="utf-8") as f:
            f.write("""import 'dart:io';
import 'package:flutter/material.dart';

class StoreUpdater {
  /// Compares semantic versions (e.g., '1.2.0' vs '1.3.0').
  /// Returns:
  /// - Negative if current < minRequired (Update Required)
  /// - Zero if equal
  /// - Positive if current > minRequired
  static int compareVersions(String current, String minRequired) {
    List<int> c = current.split('.').map((e) => int.tryParse(e) ?? 0).toList();
    List<int> m = minRequired.split('.').map((e) => int.tryParse(e) ?? 0).toList();
    
    for (int i = 0; i < 3; i++) {
      int cv = i < c.length ? c[i] : 0;
      int mv = i < m.length ? m[i] : 0;
      if (cv != mv) return cv.compareTo(mv);
    }
    return 0;
  }

  /// Prompts a blocking or dismissible update dialog.
  static void showUpdateDialog(
    BuildContext context, {
    required bool isForceUpdate,
    required String storeUrl,
    String? updateMessage,
  }) {
    showDialog(
      context: context,
      barrierDismissible: !isForceUpdate,
      builder: (ctx) => PopScope(
        canPop: !isForceUpdate,
        child: AlertDialog(
          title: const Text('تحديث جديد متوفر'),
          content: Text(
            updateMessage ??
                'يرجى تحديث التطبيق إلى أحدث إصدار للاستمرار في الاستخدام والاستفادة من التحسينات الجديدة.',
          ),
          actions: [
            if (!isForceUpdate)
              TextButton(
                onPressed: () => Navigator.pop(ctx),
                child: const Text('لاحقاً'),
              ),
            ElevatedButton(
              onPressed: () {
                // Open store URL via url_launcher or native intent
              },
              child: const Text('تحديث الآن'),
            ),
          ],
        ),
      ),
    );
  }
}
""")
        print("   ✅ Created: lib/core/services/store_updater/store_updater.dart")

    print("\n🎉 Store Updater service setup completed successfully!")
    print("="*70 + "\n")
    return True

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "."
    setup_store_updater(target)
