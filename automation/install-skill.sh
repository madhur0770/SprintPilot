#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET_ROOT="${CODEX_HOME:-$HOME/.codex}/skills"
TARGET_LINK="$TARGET_ROOT/sprintpilot"

mkdir -p "$TARGET_ROOT"

if [[ -d "$TARGET_LINK" && ! -L "$TARGET_LINK" ]]; then
  printf 'Refusing to replace existing directory: %s\n' "$TARGET_LINK" >&2
  exit 1
fi

if [[ -L "$TARGET_LINK" || -f "$TARGET_LINK" ]]; then
  rm -f "$TARGET_LINK"
fi

ln -s "$ROOT_DIR" "$TARGET_LINK"
printf 'Linked %s -> %s\n' "$TARGET_LINK" "$ROOT_DIR"
