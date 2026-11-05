#!/usr/bin/env bash
# Собирает два архива в dist/: скилл для claude.ai и плагин для Claude Code.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
P="$ROOT/plugins/evidence-based-tutor"
VER="$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["version"])' "$P/.claude-plugin/plugin.json")"
OUT="$ROOT/dist"; rm -rf "$OUT"; mkdir -p "$OUT"
EXCL=(-x '*__pycache__*' -x '*.pyc' -x '*.DS_Store')
(cd "$P/skills" && zip -qr "$OUT/evidence-based-tutor-skill-$VER.zip" evidence-based-tutor "${EXCL[@]}")
(cd "$P" && zip -qr "$OUT/evidence-based-tutor-plugin-$VER.zip" .claude-plugin hooks skills "${EXCL[@]}")
ls -l "$OUT"
