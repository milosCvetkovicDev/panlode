#!/usr/bin/env bash
# Render the PNG assets from the HTML sources next to this script with headless Chrome.
#   .github/assets/src/render.sh [path-to-chrome]
# Writes .github/assets/social-preview.png (1280x640), .claude-plugin/icon.png and docs/assets copies.
set -euo pipefail
src="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
assets="$(dirname "$src")"
repo="$(cd "$assets/../.." && pwd)"
chrome="${1:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
shot() { # html width height out
  "$chrome" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
    --default-background-color=00000000 --window-size="$2,$3" --screenshot="$4" "file://$src/$1" >/dev/null 2>&1
}
shot social-preview.html 1280 640 "$assets/social-preview.png"
shot icon.html 512 512 "$repo/.claude-plugin/icon.png"
mkdir -p "$repo/docs/assets"
cp "$assets/social-preview.png" "$repo/docs/assets/social-preview.png"
cp "$assets/logo.svg" "$repo/docs/assets/logo.svg"
echo "rendered: social-preview.png, .claude-plugin/icon.png, docs/assets/"
