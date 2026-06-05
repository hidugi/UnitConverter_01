---
name: unit-converter-tdd
description: UnitConverter_01 Dual-Track TDD·ECB 개발 시 Agent가 따를 절차. Use when implementing convert_length, writing pytest tests, RED/GREEN/REFACTOR, entity/control/boundary layers, or Logic/UI Track work in this repo.
---

# UnitConverter TDD Skill

## 언제 이 Skill을 켜는지

다음 중 **하나라도** 해당하면 이 Skill을 적용한다.

- `convert_length`, 단위 환산, entity/control/boundary 구현·테스트 요청
- RED / GREEN / REFACTOR, TDD, `pytest`, `test_d_*`, `test_u_*` 언급
- Dual-Track, Logic Track, UI Track, ECB 레이어 작업
- Phase 1 구현·리팩터 (PRD INV, SC-1~3)

**켜지 않는 경우:** Mom Test·보고서만, git commit(사용자 미요청), OOS(GUI·설정·동적 단위), Command 파일 생성.

작업 시작 시 한 줄 선언:

`Phase {N} / Layer {entity|control|boundary} / Track {Logic|UI} / {RED|GREEN|REFACTOR}`

SSoT: `docs/PRD.md`, `.cursorrules`. D-* 목록: [reference.md](reference.md).

---

## Logic Track vs UI Track

| 항목 | Logic Track | UI Track |
|------|-------------|----------|
| **레이어** | `entity`, `control` | `boundary` |
| **src** | `src/entity/`, `src/control/` | `src/boundary/` |
| **tests** | `tests/entity/`, `tests/control/` | `tests/boundary/` |
| **테스트 ID** | `D-*` | `U-*` |
| **파일명** | `test_d_*.py` | `test_u_*.py` |
| **Domain Mock** | **금지** | 해당 없음 |
| **I/O Mock** | 금지 (순수 로직) | **허용** (stdin/stdout, 포맷터) |
| **RED 대상** | 비율·검증·`convert_length` 계약 | CLI·출력 문자열·에러 표시 |
| **pytest 범위** | `pytest tests/entity tests/control -v` | `pytest tests/boundary -v` |

**한 세션에 Logic + UI 트랙 혼합 금지** (E006).

---

## ECB · Mock · E001~E007

### ECB 의존 (허용 방향만)

`boundary → control → entity` — 역방향·건너뛰기 import 금지.

| 레이어 | 허용 | 금지 |
|--------|------|------|
| entity | 표준 라이브러리만 | control/boundary import (**E001**) |
| control | entity | boundary import, I/O |
| boundary | control | entity 직접 import (**E002**) |

### Mock 정책

| Mock 종류 | Logic Track | UI Track |
|-----------|:-----------:|:----------:|
| Domain·비율·변환 로직 Mock | ❌ E004 | — |
| `convert_length` 결과 Mock (boundary 테스트) | — | ✅ |
| stdin/stdout/capsys Mock | ❌ | ✅ |

### E001~E007 — Agent 위반 코드

| 코드 | 의미 | 조치 |
|------|------|------|
| **E001** | entity가 상위 레이어 import | import 제거, 의존 역전 |
| **E002** | boundary가 entity 직접 호출 | control 경유로 수정 |
| **E003** | ECB 역방향 의존 (기타) | 레이어 재배치 |
| **E004** | Logic Track에서 Domain Mock 사용 | Mock 제거, 실구현 검증 |
| **E005** | assert 완화·skip·xfail·테스트 삭제로 green | 원복 후 최소 구현 |
| **E006** | Logic/UI Track 또는 RED/GREEN 단계 혼합 | 요청 분리 |
| **E007** | PRD 위반 (`3.28`, yard 누락, OOS 구현) | PRD·INV에 맞게 수정 |

---

## RED — 6단계 (실패 테스트만)

1. `@docs/PRD.md`에서 Rule ID·대상 Layer 확인.
2. `Phase / Layer / Track / RED` 선언.
3. **Logic:** `tests/{entity|control}/test_d_*.py` · **UI:** `tests/boundary/test_u_*.py` 에 테스트만 추가.
4. 함수명·주석에 `D-*` 또는 `U-*` + PRD Rule ID 기록.
5. 구현 코드(`src/`)·기존 테스트 수정 **금지**.
6. `pytest` 실행 → **의도적 FAIL** 확인 후 실패 요약 보고.

---

## GREEN — 6단계 (최소 구현)

1. `Phase / Layer / Track / GREEN` 선언.
2. 직전 RED의 failing 목록만 범위로 확정.
3. **Logic:** `src/entity/` 또는 `src/control/`만 수정 · **UI:** `src/boundary/`만 수정.
4. 통과에 필요한 **최소** 코드만 작성 (OOS·선행 리팩터 금지).
5. Track별 `pytest` → **전부 PASS** 확인.
6. 새 실패 없음·E001~E007 미발생 확인 후 보고.

---

## REFACTOR — 7단계 (구조만)

1. `Phase / Layer / Track / REFACTOR` 선언.
2. GREEN 직후·동일 Track 내에서만 진행.
3. 공개 API·`ConversionResult` 계약·assertion **변경 금지** (E005).
4. 상수 추출·함수 분리·import 정리 등 구조 개선만 수행.
5. ECB 의존 방향 재검증 (E001~E003).
6. `pytest tests/ -v` 전체 회귀 → PASS 유지 (SC-3).
7. 변경 요약·회귀 결과 보고.

---

## Test / Review Loop — pytest 실행 시점

| 시점 | 명령 | 기대 |
|------|------|------|
| RED 직후 | Track별 narrow: `pytest tests/entity tests/control -v` 또는 `pytest tests/boundary -v` | **FAIL** (신규 테스트) |
| GREEN 직후 | 동일 narrow 범위 | **PASS** |
| REFACTOR 각 저장 후 | `pytest tests/ -v` | **PASS** (회귀) |
| Phase 1 Logic 완료 시 | `pytest tests/entity tests/control -v` | 전체 Logic PASS |
| boundary 착수 전 | Logic 전체 green 확인 | UI는 Logic 미완 시 시작 금지 |
| 세션 종료 전 | `pytest tests/ -v` | 0 failed |

Review: RED에서 실패 메시지가 Rule ID와 일치하는지, GREEN 후 E007(비율·전 단위) 재검토.

---

## 완료 보고 항목

작업 종료 시 아래를 포함한다.

- **선언:** Phase / Layer / Track / 단계(RED|GREEN|REFACTOR)
- **변경 파일:** `src/…`, `tests/…` 목록
- **테스트 ID:** 추가·수정한 `D-*` 또는 `U-*`
- **pytest 결과:** 명령 + passed/failed 수
- **Rule 추적:** PRD Rule ID ↔ 테스트 매핑
- **ECB 점검:** E001~E007 해당 없음(또는 수정 내역)
- **미완:** 다음 단계·블로커 (있을 때만)

---

## 금지 (Skill 전역)

- assert 완화, `skip`, `xfail`, 실패 테스트 삭제 (E005)
- Logic Track Domain Mock (E004)
- RED와 GREEN 동시 요청 (E006)
- git commit/push (사용자 명시 요청 전)
- `.cursor/commands/` 생성 (별도 지시 전)
