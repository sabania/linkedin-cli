#!/usr/bin/env bash
set -euo pipefail

REPO="sabania/linkedin-cli"
INSTALL_DIR="$HOME/.local/share/linkedin-cli"
BIN_DIR="$HOME/.local/bin"

# Uninstall mode
if [[ "${1:-}" == "--uninstall" ]]; then
    rm -rf "$INSTALL_DIR"
    rm -f "$BIN_DIR/linkedin-cli"
    echo "linkedin-cli uninstalled. Restart your terminal."
    exit 0
fi

# Detect OS
OS=$(uname -s)
case "$OS" in
    Linux*)  ZIP_NAME="linkedin-cli-linux.zip";  BIN_NAME="linkedin-cli-linux" ;;
    Darwin*) ZIP_NAME="linkedin-cli-macos.zip";   BIN_NAME="linkedin-cli-macos" ;;
    *)       echo "Unsupported OS: $OS"; exit 1 ;;
esac

# Get latest release version
echo "Fetching latest release..."
LATEST=$(curl -fsSL "https://api.github.com/repos/$REPO/releases/latest" | grep '"tag_name"' | head -1 | cut -d'"' -f4)
URL="https://github.com/$REPO/releases/download/$LATEST/$ZIP_NAME"

# Download
TMP=$(mktemp -d)
echo "Downloading linkedin-cli $LATEST..."
curl -fsSL -o "$TMP/$ZIP_NAME" "$URL"

# Clean previous install
rm -rf "$INSTALL_DIR"
mkdir -p "$INSTALL_DIR"

# Extract
echo "Installing to $INSTALL_DIR..."
unzip -q "$TMP/$ZIP_NAME" -d "$INSTALL_DIR"
rm -rf "$TMP"

# Flatten if nested in a subdirectory
if [ -d "$INSTALL_DIR/$BIN_NAME" ]; then
    mv "$INSTALL_DIR/$BIN_NAME"/* "$INSTALL_DIR/"
    rmdir "$INSTALL_DIR/$BIN_NAME" 2>/dev/null || true
fi

# Fix permissions
chmod +x "$INSTALL_DIR/$BIN_NAME"
find "$INSTALL_DIR" -name "selenium-manager" -exec chmod +x {} +
find "$INSTALL_DIR" -name "*.so" -exec chmod +x {} + 2>/dev/null || true

# macOS: remove quarantine attribute
if [ "$OS" = "Darwin" ]; then
    xattr -dr com.apple.quarantine "$INSTALL_DIR" 2>/dev/null || true
fi

# Create symlink (normalizes binary name to "linkedin-cli")
mkdir -p "$BIN_DIR"
ln -sf "$INSTALL_DIR/$BIN_NAME" "$BIN_DIR/linkedin-cli"

# Check PATH
if ! echo "$PATH" | tr ':' '\n' | grep -qx "$BIN_DIR"; then
    for rc in "$HOME/.bashrc" "$HOME/.zshrc" "$HOME/.bash_profile"; do
        if [ -f "$rc" ]; then
            echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$rc"
            echo "  Added ~/.local/bin to PATH in $(basename "$rc")"
        fi
    done
fi

echo ""
echo "linkedin-cli $LATEST installed successfully!"
echo "Restart your terminal, then run: linkedin-cli --help"
echo ""
echo "Prerequisite: Google Chrome must be installed."
