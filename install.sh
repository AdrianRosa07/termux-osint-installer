#!/bin/bash
# Termux OSINT Installer - Shell Wrapper
# This wrapper makes it easier to run the Python installer from anywhere

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/termux_osint_installer.py"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║         Termux OSINT Tools Installer v1.0.0                  ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo

# Check if Python script exists
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo -e "${RED}Error: Python installer not found at $PYTHON_SCRIPT${NC}"
    exit 1
fi

# Check Python availability
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}Python3 not found. Installing...${NC}"
    pkg update && pkg install -y python3
fi

# Make Python script executable
chmod +x "$PYTHON_SCRIPT"

# Run the Python installer with all passed arguments
echo -e "${GREEN}Starting OSINT installer...${NC}"
echo

exec python3 "$PYTHON_SCRIPT" "$@"