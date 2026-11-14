#!/usr/bin/env bash
# Universal AI Toolkit v2 — One-Line Cloud Installer
# Installs or updates the toolkit CLI globally on any macOS/Linux machine.
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/<USER>/<REPO>/main/setup/install-cli.sh | bash

set -e

REPO_URL="${TOOLKIT_REPO:-https://github.com/HOSSAM-ORGANIZATION/ai_toolkit_v2.git}"
INSTALL_DIR="$HOME/.ai_toolkit"
BIN_DIR="$HOME/.local/bin"

echo ""
echo "======================================================================"
echo " 🚀 Universal AI Toolkit v2 — Global Installer"
echo "======================================================================"
echo ""

# 1. Clone or Update Toolkit Repository
if [ -d "$INSTALL_DIR/.git" ]; then
  echo "📦 Updating existing toolkit installation in $INSTALL_DIR..."
  git -C "$INSTALL_DIR" pull --ff-only || {
    echo "⚠️ Git pull failed. Fetching latest main..."
    git -C "$INSTALL_DIR" fetch origin main
    git -C "$INSTALL_DIR" reset --hard origin/main
  }
else
  echo "📦 Cloning AI Toolkit from $REPO_URL to $INSTALL_DIR..."
  rm -rf "$INSTALL_DIR"
  git clone --depth 1 "$REPO_URL" "$INSTALL_DIR"
fi

# Ensure all scripts are executable
chmod +x "$INSTALL_DIR"/bin/* "$INSTALL_DIR"/setup/*.sh 2>/dev/null || true

# 2. Symlink binary to a standard system path
mkdir -p "$BIN_DIR"

ln -sf "$INSTALL_DIR/bin/toolkit" "$BIN_DIR/toolkit"
echo "✅ Linked binary to $BIN_DIR/toolkit"

# Try /usr/local/bin if writable as well for convenience
if [ -w "/usr/local/bin" ]; then
  ln -sf "$INSTALL_DIR/bin/toolkit" "/usr/local/bin/toolkit" 2>/dev/null || true
fi

# 3. Verify PATH availability
echo ""
echo "🔍 Verifying PATH setup..."
if command -v toolkit >/dev/null 2>&1; then
  echo "🎉 SUCCESS: 'toolkit' is immediately available in your PATH!"
else
  # Check if ~/.local/bin is in PATH
  if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    PROFILE_FILE=""
    if [ -n "$ZSH_VERSION" ] || [ "$SHELL" = "*/zsh" ] || [ -f "$HOME/.zshrc" ]; then
      PROFILE_FILE="$HOME/.zshrc"
    elif [ -f "$HOME/.bashrc" ]; then
      PROFILE_FILE="$HOME/.bashrc"
    elif [ -f "$HOME/.bash_profile" ]; then
      PROFILE_FILE="$HOME/.bash_profile"
    fi

    if [ -n "$PROFILE_FILE" ]; then
      if ! grep -q 'export PATH=.*\.local/bin' "$PROFILE_FILE"; then
        echo "export PATH=\"\$HOME/.local/bin:\$PATH\"" >> "$PROFILE_FILE"
        echo "⚙️ Added \$HOME/.local/bin to $PROFILE_FILE"
      fi
    fi
    echo "💡 Note: Run 'source $PROFILE_FILE' or reopen terminal if command is not recognized yet."
  fi
fi

echo ""
echo "======================================================================"
echo " 🎉 Installation Complete! You can now run 'toolkit' anywhere."
echo "======================================================================"
echo "Try running:"
echo "  toolkit --help"
echo "  toolkit setup"
echo "======================================================================"
echo ""
