#!/usr/bin/env bash
# Universal AI Toolkit v2 — One-Click Host Project Installer
# Installs rules, skills, search exclusions, and ignore configurations into the host app.

set -e

TOOLKIT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HOST_DIR="$(pwd)"

# If run directly inside toolkit dir, look for parent as host
if [ "$HOST_DIR" = "$TOOLKIT_DIR" ]; then
  HOST_DIR="$(dirname "$TOOLKIT_DIR")"
fi

echo "🚀 Installing Universal AI Toolkit v2 into host project: $HOST_DIR"

# 1. Setup Cursor Rules
mkdir -p "$HOST_DIR/.cursor/rules"
echo "⚙️ Installing Cursor rules..."
for rule_tmpl in "$TOOLKIT_DIR"/templates/cursor-rules/*.template; do
  if [ -f "$rule_tmpl" ]; then
    rule_name="$(basename "$rule_tmpl" .template)"
    cp -f "$rule_tmpl" "$HOST_DIR/.cursor/rules/$rule_name"
    echo "   Installed .cursor/rules/$rule_name"
  fi
done

# 2. Setup Cursor Ignore Files
echo "⚙️ Installing Cursor ignore files..."
if [ -f "$TOOLKIT_DIR/templates/cursor-ignore/.cursorignore" ]; then
  cp -f "$TOOLKIT_DIR/templates/cursor-ignore/.cursorignore" "$HOST_DIR/.cursorignore"
  echo "   Installed .cursorignore"
fi

if [ -f "$TOOLKIT_DIR/templates/cursor-ignore/.cursorindexingignore" ]; then
  cp -f "$TOOLKIT_DIR/templates/cursor-ignore/.cursorindexingignore" "$HOST_DIR/.cursorindexingignore"
  echo "   Installed .cursorindexingignore"
fi

# 3. Setup VS Code Search Exclusions
mkdir -p "$HOST_DIR/.vscode"
echo "⚙️ Installing VS Code search exclusions..."
if [ -f "$TOOLKIT_DIR/templates/vscode/search-exclude.json" ]; then
  SETTINGS_FILE="$HOST_DIR/.vscode/settings.json"
  if [ ! -f "$SETTINGS_FILE" ]; then
    cp -f "$TOOLKIT_DIR/templates/vscode/search-exclude.json" "$SETTINGS_FILE"
    echo "   Created .vscode/settings.json"
  else
    echo "   .vscode/settings.json already exists (preserving custom settings)."
  fi
fi

# 4. Setup Universal Agent Entrypoints (CLAUDE.md / AGENTS.md)
echo "⚙️ Checking AI Agent entrypoint files..."
for agent_doc in CLAUDE.md AGENTS.md; do
  if [ ! -f "$HOST_DIR/$agent_doc" ] && [ -f "$TOOLKIT_DIR/templates/app-seed/$agent_doc" ]; then
    cp -f "$TOOLKIT_DIR/templates/app-seed/$agent_doc" "$HOST_DIR/$agent_doc"
    echo "   Created $agent_doc"
  fi
done

# 5. Check Profile Gatekeeper
echo "🔍 Validating project profile..."
if [ -f "$HOST_DIR/project_profile.yaml" ]; then
  python3 "$TOOLKIT_DIR/bin/check-profile" "$HOST_DIR"
else
  echo ""
  echo "⚠️ Notice: project_profile.yaml is not yet created."
  echo "👉 Run 'make toolkit-init' or 'python3 ai_toolkit/bin/wizard/init_profile.py' to lock project identity."
fi

echo ""
echo "🎉 Universal AI Toolkit v2 successfully installed and synchronized!"
