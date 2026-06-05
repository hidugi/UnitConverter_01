#!/usr/bin/env bash
# UnitConverter_01 sessionStart — inject Rule SSOT + Dual-Track TDD + ECB context.
set -euo pipefail

HOOK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Consume sessionStart input (session_id, composer_mode, …)
cat >/dev/null || true

PYTHON=""
for cmd in python3 python; do
  if command -v "$cmd" >/dev/null 2>&1; then
    PYTHON="$cmd"
    break
  fi
done

if [[ -z "$PYTHON" ]]; then
  printf '%s\n' '{"additional_context":"[UnitConverter_01] session-init: python required"}'
  exit 0
fi

"$PYTHON" - <<'PY' | "$HOOK_DIR/_python.sh"
import json

additional_context = """# UnitConverter_01 — Session Context (sessionStart)

## 프로젝트
- **UnitConverter_01**: meter / feet / yard 길이 **unit converter**
- **Dual-Track TDD**: Track 1 = PRD·Rule 고정 / Track 2 = RED→GREEN→REFACTOR + pytest
- **ECB**: `boundary → control → entity` (entity→상위 import 금지)

## SSOT (Rule)
- **`.cursorrules`** — Agent 헌법: ECB, Mock, TDD 금지, D-*/U-* 테스트 ID
- **`docs/PRD.md`** — INV-01~08, 오류 코드, SC-1~3, Phase 1 OOS

## Harness · Test Loop
- `src/{entity,control,boundary}/` · `tests/{entity,control,boundary}/`
- `pytest tests/ -v` (`pyproject.toml`)
- Logic: `tests/entity`, `tests/control` (Domain Mock 금지)
- UI: `tests/boundary` (I/O Mock 허용)

## 슬래시 Commands (등록됨)
- `/tdd-red` — RED만: `tests/` 작성 → pytest **FAIL** 확인, `src/` 수정 금지

## TDD 작업 시 응답 첫 줄
`Phase: {red|green|refactor} | Layer: {entity|control|boundary} | Track: {Logic|UI}`

## 참고
- Skill: `.cursor/skills/unit-converter-tdd/SKILL.md`
- D-* IDs: `.cursor/skills/unit-converter-tdd/reference.md`
- Review: `/review-ecb` (코드 수정 없음)
"""

print(
    json.dumps(
        {
            "additional_context": additional_context,
            "env": {
                "UC01_PROJECT": "UnitConverter_01",
                "UC01_SSOT": ".cursorrules",
                "UC01_PRD": "docs/PRD.md",
                "UC01_ARCH": "ECB",
                "UC01_TRACK": "Dual-Track-TDD",
            },
        },
        ensure_ascii=False,
    )
)
PY
