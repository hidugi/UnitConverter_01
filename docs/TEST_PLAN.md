# Unit Converter — 테스트 플랜 (Dual-Track)

| 항목 | 내용 |
|------|------|
| 프로젝트 | UnitConverter_01 |
| 버전 | 0.1 (초안) |
| 작성일 | 2026-06-05 |
| SSoT | [`docs/PRD.md`](PRD.md) |
| 방법론 | Dual-Track TDD · ECB · RED → GREEN → REFACTOR |
| Skill | [`.cursor/skills/unit-converter-tdd/SKILL.md`](../.cursor/skills/unit-converter-tdd/SKILL.md) |

---

## 1. 목적 · 범위

### 1.1 목적

PRD Phase 1 목표(G-01~G-03)를 **Dual-Track TDD**로 검증한다.

| PRD 목표 | 테스트로 보호하는 것 |
|----------|---------------------|
| **G-01** | meter/feet/yard **전 단위** 환산 (INV-07) |
| **G-02** | 잘못된 입력·미지 단위·음수 **명시적 실패** |
| **G-03** | SC-1~3 **회귀** — refactor 후에도 동일 결과 (INV-08) |

### 1.2 Mom Test → 수용 기준 추적

| Mom Test 증거 | PRD | 테스트 ID |
|---------------|-----|-----------|
| meter 견적 vs feet 도면 → 반나절 | SC-1, G-01 | D-005, U-001 |
| 3.28 vs 3.28084 → 2cm·재단 | INV-02, SC-2 | D-006 |
| 변환표에 yard 없음 | INV-07, SC-2 | D-005 |
| 팀원마다 다른 계산 | INV-08, SC-3 | D-007 |

### 1.3 Phase 1 범위 · OOS

**포함:** `convert_length`, Rule 검증, Logic Track 전체, boundary 최소 연동(UI Track)  
**제외(OOS):** GUI, JSON/YAML 설정, 동적 cubit, inch/cm, 출력 포맷 선택(Phase 4)

---

## 2. Dual-Track 구조

```
Track 1 (명세)          Track 2 (구현 + 검증)
─────────────────       ─────────────────────────────────────
PRD INV·SC·오류코드  →   Logic Track  → entity + control  (D-*)
     고정                  ↓ Logic green 후
                     UI Track     → boundary            (U-*)
```

| Track | 레이어 | tests 경로 | 테스트 ID | Mock |
|-------|--------|------------|-----------|------|
| **Logic** | `entity`, `control` | `tests/entity/`, `tests/control/` | `D-*` | **Domain Mock 금지** (E004) |
| **UI** | `boundary` | `tests/boundary/` | `U-*` | stdin/stdout·포맷터 Mock **허용** |

**세션 규칙 (E006):** Logic Track과 UI Track을 **한 RED/GREEN 사이클에 섞지 않는다.**  
**선행 조건:** UI Track 착수 전 Logic Track 전체 green.

---

## 3. ECB · 레이어 책임

```
boundary  →  control  →  entity
   U-*         D-*        D-006(비율)
```

| 레이어 | 책임 | Phase 1 테스트 배치 |
|--------|------|---------------------|
| **entity** | 비율 상수(INV-02, INV-03), meter 정규화·전 단위 환산 | D-006 |
| **control** | `convert_length` — 검증 순서, `ConversionResult` 조립 | D-001~D-005, D-007 |
| **boundary** | CLI 입출력, control 호출 (entity 직접 호출 금지 E002) | U-001~U-004 |

---

## 4. Logic Track — D-* 테스트 카탈로그

파일명: `test_d_*.py` · 함수명·주석에 `D-*` + PRD Rule ID 기록.

### 4.1 검증 · 오류 (control)

| ID | Rule ID | Given | When | Then | 파일(권장) |
|----|---------|-------|------|------|------------|
| **D-001** | `FORMAT_INVALID` | `meter2.5`, `:2.5`, `meter:`, `:2.5`(빈 unit) | `convert_length` | `ok=False`, `error="FORMAT_INVALID"` | `tests/control/test_d_format.py` |
| **D-002** | `VALUE_NOT_NUMBER` | `meter:abc`, `feet:2.5.3` | `convert_length` | `ok=False`, `error="VALUE_NOT_NUMBER"` | `tests/control/test_d_format.py` |
| **D-003** | `UNKNOWN_UNIT` | `cubit:1.0`, `inch:10` | `convert_length` | `ok=False`, `error="UNKNOWN_UNIT"`, message에 unit 포함 | `tests/control/test_d_units.py` |
| **D-004** | `NEGATIVE_VALUE` | `meter:-1`, `feet:-0.1` | `convert_length` | `ok=False`, `error="NEGATIVE_VALUE"` | `tests/control/test_d_validation.py` |

**검증 순서 (PRD §5.1):** FORMAT → VALUE → UNIT → NEGATIVE → 환산 — REFACTOR 시 순서 유지.

### 4.2 정상 환산 · 수용 기준 (control + entity)

| ID | Rule / SC | Given | When | Then | 파일(권장) |
|----|-----------|-------|------|------|------------|
| **D-005** | INV-07, SC-1 | 아래 픽스처 3건 | `convert_length` | `ok=True`, conversions에 **meter·feet·yard 3개** | `tests/control/test_d_convert.py` |
| **D-006** | INV-02, SC-2 | `meter:2.5` | `convert_length` | feet=`8.2`, yard=`2.7` (반올림 1자리); entity 상수 `3.28084`/`1.09361` | `tests/entity/test_d_ratios.py` + control |
| **D-007** | INV-08, SC-3 | `meter:2.5` | 동일 입력 2회 호출 | 두 `ConversionResult` **완전 동일** | `tests/control/test_d_idempotent.py` |

### 4.3 고정 픽스처 (SSoT)

내부 계산은 전체 정밀도, **assertion은 소수 1자리 반올림** (PRD §5.3).

| input_str | meter | feet | yard |
|-----------|-------|------|------|
| `meter:2.5` | 2.5 | 8.2 | 2.7 |
| `feet:8.2` | 2.5 | 8.2 | 2.7 |
| `yard:2.7` | 2.5 | 8.2 | 2.7 |

**역방향 픽스처:** feet·yard 입력도 동일 hub(meter=2.5)로 수렴 — SC-1 커버.

### 4.4 D-006 — 3.28 방지 (Mom Test 핵심)

| 케이스 | 의도 |
|--------|------|
| entity 상수 assert | `FEET_PER_METER == 3.28084`, `YARD_PER_METER == 1.09361` |
| 3.28 사용 시 결과 불일치 | `meter:2.5` → feet가 `8.2`가 **아님** (예: 8.0) — 상수 오류 회귀 방지 |
| SC-2 정합 | `meter:2.5` → feet `8.2` **통과** |

> Logic Track에서 Domain Mock 없이 **실제 상수·실제 계산**으로 검증 (E004).

### 4.5 성공 응답 계약 (assertion 체크리스트)

```python
# ok=True 일 때
assert result["ok"] is True
assert result["source"] == {"unit": "meter", "value": 2.5}
units = {c["unit"] for c in result["conversions"]}
assert units == {"meter", "feet", "yard"}
# 각 conversion value는 픽스처와 1자리 반올림 일치
```

```python
# ok=False 일 때
assert result["ok"] is False
assert result["error"] in ("FORMAT_INVALID", "VALUE_NOT_NUMBER", "UNKNOWN_UNIT", "NEGATIVE_VALUE")
assert "message" in result
```

---

## 5. UI Track — U-* 테스트 카탈로그

**착수 조건:** D-001~D-007 Logic Track **전부 PASS**.

파일명: `test_u_*.py` · boundary만 대상 · `convert_length` 결과 Mock **허용**.

| ID | Given | When | Then | 파일(권장) |
|----|-------|------|------|------------|
| **U-001** | Mock: `meter:2.5` 성공 | CLI/boundary 실행 | stdout에 `8.2 feet`, `2.7 yard` 포함 | `tests/boundary/test_u_cli_success.py` |
| **U-002** | Mock: `FORMAT_INVALID` | CLI 실행 | stderr/stdout에 형식 오류 안내 | `tests/boundary/test_u_cli_errors.py` |
| **U-003** | Mock: `UNKNOWN_UNIT` (`cubit`) | CLI 실행 | `Unknown unit: cubit` 유사 메시지 | `tests/boundary/test_u_cli_errors.py` |
| **U-004** | capsys + 실제 control 연동 | `meter:2.5` end-to-end | Logic 결과와 CLI 출력 **일치** (integration smoke) | `tests/boundary/test_u_e2e_smoke.py` |

**U-004 주의:** boundary가 control만 호출(E002 준수). entity 직접 import 금지.

---

## 6. TDD 실행 순서 (Phase 1)

### 6.1 Logic Track — 권장 RED 배치

| 순서 | RED | Layer | pytest (의도) |
|------|-----|-------|---------------|
| 1 | D-001, D-002 | control | FAIL |
| 2 | GREEN | control | PASS |
| 3 | D-003, D-004 | control | FAIL → GREEN |
| 4 | D-005 | control (+ entity stub) | FAIL → GREEN |
| 5 | D-006 | entity | FAIL → GREEN |
| 6 | D-007 | control | FAIL → GREEN |
| 7 | REFACTOR | entity — 비율 상수 추출, control — 검증 순서 정리 | `pytest tests/ -v` PASS |

각 RED 선언:

`Phase 1 / Layer {entity|control} / Track Logic / RED`

각 GREEN 선언:

`Phase 1 / Layer {entity|control} / Track Logic / GREEN`

### 6.2 UI Track — Logic green 이후

| 순서 | RED | Layer | pytest (의도) |
|------|-----|-------|---------------|
| 1 | U-001, U-002 | boundary | FAIL |
| 2 | GREEN — CLI wrapper | boundary | PASS |
| 3 | U-003 | boundary | FAIL → GREEN |
| 4 | U-004 smoke | boundary | PASS |
| 5 | REFACTOR — 출력 포맷 정리 | boundary | `pytest tests/ -v` PASS |

---

## 7. pytest 명령 · 게이트

| 시점 | 명령 | 기대 |
|------|------|------|
| Logic RED 직후 | `pytest tests/entity tests/control -v` | 신규 테스트 **FAIL** |
| Logic GREEN 직후 | `pytest tests/entity tests/control -v` | **PASS** |
| UI RED/GREEN | `pytest tests/boundary -v` | FAIL → PASS |
| REFACTOR · 세션 종료 | `pytest tests/ -v` | **0 failed** (SC-3) |
| ECB 리뷰 | `/review-ecb` | E001~E007 없음 |

---

## 8. Rule ID ↔ 테스트 1:1 추적 (NFR-02)

| PRD Rule / SC | Logic (D-*) | UI (U-*) |
|---------------|-------------|----------|
| FORMAT_INVALID | D-001 | U-002 |
| VALUE_NOT_NUMBER | D-002 | — |
| UNKNOWN_UNIT | D-003 | U-003 |
| NEGATIVE_VALUE | D-004 | — |
| INV-01~03 | D-006 | — |
| INV-07, SC-1 | D-005 | U-001, U-004 |
| INV-08, SC-3 | D-007 | — |
| SC-2 (3.28084) | D-006 | — |

---

## 9. 금지 · 품질 게이트

| 코드 | 금지 행위 | 테스트 플랜 대응 |
|------|-----------|------------------|
| **E004** | Logic Track Domain Mock | D-*는 실구현·실상수만 |
| **E005** | assert 완화·skip·xfail·테스트 삭제 | REFACTOR 후 assertion 동일 |
| **E006** | Logic/UI Track 혼합 RED | §6 순서 준수 |
| **E007** | `3.28` 사용·yard 누락 | D-005, D-006 필수 |

---

## 10. Phase 2~4 테스트 확장 (참고)

| Phase | 추가 테스트 방향 |
|-------|------------------|
| **2** | entity 인터페이스 분리 후 D-* 회귀 유지 (SC-3) |
| **3** | 설정 로드·동적 cubit — D-008+ (별도 reference 갱신) |
| **4** | JSON/CSV/표 출력 — U-005+ |

Phase 1 완료 기준: **D-001~D-007 PASS + U-001~U-004 PASS + `pytest tests/ -v` green**.

---

## 11. 디렉터리 · 파일 목표 구조

```
tests/
├── entity/
│   └── test_d_ratios.py          # D-006
├── control/
│   ├── test_d_format.py          # D-001, D-002
│   ├── test_d_units.py           # D-003
│   ├── test_d_validation.py      # D-004
│   ├── test_d_convert.py         # D-005
│   └── test_d_idempotent.py      # D-007
└── boundary/
    ├── test_u_cli_success.py     # U-001
    ├── test_u_cli_errors.py      # U-002, U-003
    └── test_u_e2e_smoke.py       # U-004
```

---

## 12. 첫 세션 체크리스트 (세션 4)

- [ ] `Phase 1 / Layer control / Track Logic / RED` — D-001 RED 작성
- [ ] `pytest tests/control -v` → FAIL 확인
- [ ] GREEN — `convert_length` 최소 구현
- [ ] D-002~D-004 RED → GREEN
- [ ] D-005~D-007 RED → GREEN
- [ ] REFACTOR — entity 비율 분리, `pytest tests/ -v` PASS
- [ ] UI Track U-001~U-004
- [ ] `/review-ecb` — E001~E007 점검

---

*끝.*
