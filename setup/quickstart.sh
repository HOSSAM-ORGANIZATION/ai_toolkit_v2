#!/usr/bin/env bash
# Universal AI Toolkit v2 — One-Shot Quickstart & Setup Script
# Runs the entire setup in a single unified command:
# 1. Copies Adaptive Makefile
# 2. Runs Interactive Profile Wizard (if not already created)
# 3. Deploys Cursor rules, skills, and VS Code search exclusions
# 4. Verifies setup integrity

set -e

TOOLKIT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HOST_DIR="$(pwd)"

if [ "$HOST_DIR" = "$TOOLKIT_DIR" ]; then
  HOST_DIR="$(dirname "$TOOLKIT_DIR")"
fi

echo ""
echo "======================================================================"
echo " 🚀 Universal AI Toolkit v2 — Complete One-Shot Setup"
echo "======================================================================"
echo "📂 Project root: $HOST_DIR"
echo "📂 Toolkit path: $TOOLKIT_DIR"
echo ""

# 1. Setup Universal Makefile & Project Wrapper
if [ ! -f "$HOST_DIR/Makefile" ]; then
  echo "📄 [1/4] Deploying Universal Adaptive Makefile..."
  cp -f "$TOOLKIT_DIR/templates/root/Makefile.universal" "$HOST_DIR/Makefile"
  echo "   ✅ Created $HOST_DIR/Makefile"
else
  echo "📄 [1/4] Makefile already present in host project."
fi

if [ ! -f "$HOST_DIR/toolkit" ]; then
  cp -f "$TOOLKIT_DIR/templates/root/toolkit" "$HOST_DIR/toolkit"
  chmod +x "$HOST_DIR/toolkit"
  echo "   ✅ Created $HOST_DIR/toolkit (Project CLI wrapper)"
fi

# 2. Project Profile (Gatekeeper)
if [ ! -f "$HOST_DIR/project_profile.yaml" ]; then
  echo ""
  echo "⚙️ [2/4] Launching Interactive Project Profile Wizard..."
  python3 "$TOOLKIT_DIR/bin/wizard/init_profile.py" --target-dir "$HOST_DIR"
else
  echo ""
  echo "⚙️ [2/4] project_profile.yaml already exists. Validating..."
  python3 "$TOOLKIT_DIR/bin/check-profile" "$HOST_DIR"
fi

# 3. Deploy IDE Rules, Skills, and Search Exclusions
echo ""
echo "💻 [3/4] Deploying IDE rules, skills, and configuration..."
bash "$TOOLKIT_DIR/setup/install.sh"

# 4. Run Integrity Check
echo ""
echo "🔍 [4/4] Running setup integrity check..."
bash "$TOOLKIT_DIR/setup/verify-setup.sh"

echo ""
echo "======================================================================"
echo " 🎉 ALL SET! Your project is fully configured and ready to go."
echo "======================================================================"
echo "Next steps:"
echo "  - Run 'make help' to see customized commands for your project."
echo "  - Run 'make run' (or 'make <flavor> run') to launch your app."
echo "======================================================================"
echo ""
