#!/usr/bin/env bash
set -euo pipefail
VERSION="${BLENDER_VERSION:-5.2.3}"
PLATFORM="linux-x64"
BASE_URL="https://download.blender.org/release/Blender5.2"
ARCHIVE="blender-${VERSION}-${PLATFORM}.tar.xz"
CHECKSUM_FILE="blender-${VERSION}.sha256"
CACHE_ROOT="${BLENDER_CACHE_DIR:-$HOME/.cache/nolane-video-toolchain}"
DEST="$CACHE_ROOT/blender-${VERSION}-${PLATFORM}"

if [[ "$VERSION" != "5.2.3" ]]; then
  echo "Only Blender ${VERSION} is configured in the validated toolchain; update manifest and tests before changing it." >&2
  exit 2
fi
if [[ -x "$DEST/blender" ]]; then
  "$DEST/blender" --background --version | head -n 2
  if [[ -n "${GITHUB_PATH:-}" ]]; then echo "$DEST" >> "$GITHUB_PATH"; fi
  echo "$DEST"
  exit 0
fi
mkdir -p "$CACHE_ROOT"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
curl --fail --location --retry 3 --retry-all-errors "$BASE_URL/$ARCHIVE" -o "$TMP/$ARCHIVE"
curl --fail --location --retry 3 --retry-all-errors "$BASE_URL/$CHECKSUM_FILE" -o "$TMP/$CHECKSUM_FILE"
line="$(grep -E "[[:space:]]${ARCHIVE//./\\.}$" "$TMP/$CHECKSUM_FILE" | head -n 1 || true)"
if [[ -z "$line" ]]; then
  echo "Official checksum file does not contain $ARCHIVE" >&2
  exit 3
fi
printf '%s\n' "$line" | (cd "$TMP" && sha256sum --check --status -) || {
  echo "Blender archive SHA-256 verification failed" >&2
  exit 3
}
tar -xJf "$TMP/$ARCHIVE" -C "$TMP"
extracted="$TMP/blender-${VERSION}-${PLATFORM}"
test -x "$extracted/blender"
rm -rf "$DEST"
mv "$extracted" "$DEST"
"$DEST/blender" --background --version | head -n 2
if [[ -n "${GITHUB_PATH:-}" ]]; then echo "$DEST" >> "$GITHUB_PATH"; fi
printf '%s\n' "$DEST"
