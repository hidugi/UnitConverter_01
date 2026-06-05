#!/usr/bin/env bash
# Cursor hook helper — read JSON from stdin, emit validated JSON to stdout.
set -euo pipefail

PYTHON=""
for cmd in python3 python; do
  if command -v "$cmd" >/dev/null 2>&1; then
    PYTHON="$cmd"
    break
  fi
done

if [[ -z "$PYTHON" ]]; then
  printf '%s\n' '{"additional_context":"[UnitConverter_01 hook] python not found"}'
  exit 0
fi

exec "$PYTHON" -c '
import json
import sys

ALLOWED = frozenset({"additional_context", "env", "continue", "user_message"})

try:
    data = json.load(sys.stdin)
except json.JSONDecodeError:
    data = {"additional_context": "[hook] invalid JSON on stdin"}

if not isinstance(data, dict):
    data = {"additional_context": str(data)}

out = {k: v for k, v in data.items() if k in ALLOWED}
json.dump(out, sys.stdout, ensure_ascii=False)
sys.stdout.write("\n")
'
