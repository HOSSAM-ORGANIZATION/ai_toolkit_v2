#!/usr/bin/env bash
# Universal AI Toolkit v2 — Setup and Integrity Verification
set -e

TOOLKIT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "🔍 Running Universal AI Toolkit v2 Integrity Verification..."
echo "📂 Toolkit root: $TOOLKIT_DIR"

ERRORS=0
WARNINGS=0

# 1. Check Schema & Presets
if [ -f "$TOOLKIT_DIR/schema/project_profile.schema.json" ]; then
  echo "✅ Schema present (project_profile.schema.json)"
else
  echo "❌ Missing schema/project_profile.schema.json"
  ERRORS=$((ERRORS + 1))
fi

for preset in enterprise_clean_bloc modern_modular_riverpod lean_mvp; do
  if [ -f "$TOOLKIT_DIR/presets/${preset}.yaml" ]; then
    echo "✅ Preset verified: $preset"
  else
    echo "❌ Missing preset: presets/${preset}.yaml"
    ERRORS=$((ERRORS + 1))
  fi
done

# 2. Check Core Bin Executables
for b in toolkit check-profile plan-splitter l10n-sync.py toolkit-context.py wizard/init_profile.py scaffolder/add_blueprint.py; do
  if [ -x "$TOOLKIT_DIR/bin/$b" ]; then
    echo "✅ Executable tool verified: bin/$b"
  else
    echo "❌ Missing or non-executable: bin/$b"
    ERRORS=$((ERRORS + 1))
  fi
done

# Check Blueprints Catalog
if [ -f "$TOOLKIT_DIR/templates/blueprints/CATALOG.md" ]; then
  echo "✅ Blueprints catalog verified (CATALOG.md)"
else
  echo "❌ Missing templates/blueprints/CATALOG.md"
  ERRORS=$((ERRORS + 1))
fi

# 3. Check LOADMAP.md & Agent Cards
if [ -f "$TOOLKIT_DIR/LOADMAP.md" ]; then
  echo "✅ LOADMAP.md present"
else
  echo "❌ Missing LOADMAP.md"
  ERRORS=$((ERRORS + 1))
fi

# Check Agent Cards in rules/
for rule_file in "$TOOLKIT_DIR"/rules/*/*.md; do
  if [ -f "$rule_file" ]; then
    rel_path="${rule_file#$TOOLKIT_DIR/}"
    if head -n 10 "$rule_file" | grep -q "## Agent card"; then
      echo "✅ Agent Card verified: $rel_path"
    else
      echo "⚠️ Missing '## Agent card' header in first 10 lines: $rel_path"
      WARNINGS=$((WARNINGS + 1))
    fi
  fi
done

# 4. Check Workflows
for wf in session/bootstrap-session.md \
          feature-delivery/make-plan.md \
          feature-delivery/implement-phase.md \
          feature-delivery/verify-and-pr.md \
          feature-delivery/autopilot-phases.md \
          feature-delivery/screen-states-protocol.md \
          product-analysis/design-ingestion.md \
          maintenance/collaborative-problem-solving.md \
          maintenance/bugfix.md; do
  if [ -f "$TOOLKIT_DIR/workflows/$wf" ]; then
    echo "✅ Workflow verified: workflows/$wf"
  else
    echo "❌ Missing workflow: workflows/$wf"
    ERRORS=$((ERRORS + 1))
  fi
done

# 5. Check Universal Makefile Template
if [ -f "$TOOLKIT_DIR/templates/root/Makefile.universal" ]; then
  echo "✅ Universal Makefile template present"
else
  echo "❌ Missing templates/root/Makefile.universal"
  ERRORS=$((ERRORS + 1))
fi

echo "======================================================================"
if [ $ERRORS -eq 0 ]; then
  echo "🎉 Toolkit verification PASSED with 0 errors and $WARNINGS warning(s)!"
  exit 0
else
  echo "🛑 Toolkit verification FAILED with $ERRORS error(s) and $WARNINGS warning(s)!"
  exit 1
fi
