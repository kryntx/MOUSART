#!/bin/bash
# Build Windows EXE using PyInstaller
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

echo "=== Building MOUSART Windows EXE ==="

# Install PyInstaller if needed
pip3 install pyinstaller --quiet

# Clean previous build
rm -rf build/ dist/

# Build
pyinstaller pyinstaller.spec --noconfirm

# Create release directory and copy
mkdir -p release
cp dist/MOUSART.exe release/MOUSART-v3.0.0-windows-x86_64.exe

echo "=== Build complete: release/MOUSART-v3.0.0-windows-x86_64.exe ==="
