#!/bin/bash
# Build Debian package
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

echo "=== Building MOUSART Debian Package ==="

# Build the package
dpkg-buildpackage -us -uc -b

# Move to release directory
mkdir -p release
mv ../*.deb release/ 2>/dev/null || true

echo "=== Build complete: release/*.deb ==="
