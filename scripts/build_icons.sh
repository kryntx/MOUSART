#!/bin/bash
# Generate icon files from SVG source
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

echo "=== Generating MOUSART icons ==="

SIZES="16 24 32 48 64 128 256"
SVG="resources/icons/mousart.svg"

for size in $SIZES; do
    echo "  Generating ${size}x${size} PNG..."
    python3 -c "
import cairosvg
cairosvg.svg2png(url='$SVG', write_to='resources/icons/mousart_${size}.png', output_width=$size, output_height=$size)
"
done

echo "  Generating ICO..."
python3 -c "
from PIL import Image
img = Image.open('resources/icons/mousart_256.png')
img.save('resources/icons/mousart.ico', format='ICO', sizes=[(16,16),(32,32),(48,48),(64,64),(128,128),(256,256)])
"

echo "=== Icons generated ==="
