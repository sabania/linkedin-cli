#!/usr/bin/env bash
# Install linkedin-cli binary from GitHub Releases
set -euo pipefail

REPO="asabani/linkedin-cli"
INSTALL_DIR="${LINKEDIN_CLI_DIR:-$HOME/.linkedin-cli}"
BIN_NAME="linkedin-cli"

# Detect OS and arch
OS="$(uname -s | tr '[:upper:]' '[:lower:]')"
ARCH="$(uname -m)"

case "$OS" in
  linux*)   PLATFORM="linux" ;;
  darwin*)  PLATFORM="macos" ;;
  mingw*|msys*|cygwin*) PLATFORM="windows" ;;
  *)        echo "Unsupported OS: $OS"; exit 1 ;;
esac

case "$ARCH" in
  x86_64|amd64) ARCH="amd64" ;;
  arm64|aarch64) ARCH="arm64" ;;
  *)        echo "Unsupported architecture: $ARCH"; exit 1 ;;
esac

if [ "$PLATFORM" = "windows" ]; then
  ASSET="${BIN_NAME}-${PLATFORM}-${ARCH}.exe"
else
  ASSET="${BIN_NAME}-${PLATFORM}-${ARCH}"
fi

echo "Detecting latest release..."
LATEST=$(curl -sI "https://github.com/${REPO}/releases/latest" | grep -i "^location:" | sed 's/.*tag\///' | tr -d '\r\n')

if [ -z "$LATEST" ]; then
  echo "Could not detect latest release. Check https://github.com/${REPO}/releases"
  exit 1
fi

DOWNLOAD_URL="https://github.com/${REPO}/releases/download/${LATEST}/${ASSET}"

echo "Downloading ${ASSET} (${LATEST})..."
mkdir -p "$INSTALL_DIR"

if command -v curl &>/dev/null; then
  curl -fSL "$DOWNLOAD_URL" -o "${INSTALL_DIR}/${ASSET}"
elif command -v wget &>/dev/null; then
  wget -q "$DOWNLOAD_URL" -O "${INSTALL_DIR}/${ASSET}"
else
  echo "Neither curl nor wget found. Install one and retry."
  exit 1
fi

chmod +x "${INSTALL_DIR}/${ASSET}"

# Create symlink or copy to final name
if [ "$PLATFORM" = "windows" ]; then
  cp "${INSTALL_DIR}/${ASSET}" "${INSTALL_DIR}/${BIN_NAME}.exe"
  echo "Installed to ${INSTALL_DIR}/${BIN_NAME}.exe"
  echo "Add ${INSTALL_DIR} to your PATH if not already there."
else
  ln -sf "${INSTALL_DIR}/${ASSET}" "${INSTALL_DIR}/${BIN_NAME}"
  echo "Installed to ${INSTALL_DIR}/${BIN_NAME}"

  # Add to PATH hint
  if ! echo "$PATH" | grep -q "$INSTALL_DIR"; then
    echo ""
    echo "Add to your PATH:"
    echo "  export PATH=\"${INSTALL_DIR}:\$PATH\""
  fi
fi

echo "Done. Run 'linkedin-cli --help' to verify."
