#!/usr/bin/env bash
# Install linkedin-cli from GitHub Releases.
# Used by the setup skill and agents to auto-install the CLI.
# Delegates to the main install.sh script.
set -euo pipefail

REPO_URL="https://raw.githubusercontent.com/sabania/linkedin-cli/master/install.sh"

echo "Installing linkedin-cli..."
curl -fsSL "$REPO_URL" | bash

echo ""
echo "Verify: linkedin-cli --help"
