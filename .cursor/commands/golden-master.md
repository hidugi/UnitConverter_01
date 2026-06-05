# Golden Master — 동작 기준선 고정

UnitConverter_01 Phase 1 **GREEN PASS 이후** 사용자 가시 출력·`ConversionResult` 계약을 golden 파일로 고정한다.  
SSoT: `@docs/PRD.md` §6, `@docs/TEST_PLAN.md` §12.2, `.cursor/skills/unit-converter-tdd/SKILL.md`.

**선행 조건:** `pytest tests/ -v` → **21 passed** (GP-01~GP-03). RED·REFACTOR와 **혼합 금지** (E006).

## 필수 선언

응답 **첫 줄**:

```
Phase: green | Layer: {boundary|control} | Track: {UI|Logic} | Golden Master
```

이어서 대상 테스트 ID(`U-*` 또는 `D-*`)와 golden 상대 경로를 한 줄로 명시한다.

## 대상 (Phase 1 기본)

| 우선 | ID | Layer | Track | 테스트 | golden 파일 | 캡처 내용 |
|:----:|----|-------|-------|--------|-------------|-----------|
| **1** | **U-004** | boundary | UI | `tests/boundary/test_u_e2e_smoke.py` | `tests/golden/u004_meter_25_stdout.approved.txt` | `meter:2.5` CLI stdout (Mock **금지**, real `convert_length`) |
| 2 | D-005 | control | Logic | `tests/control/test_d_convert.py` | `tests/golden/d005_meter_25_result.approved.json` | `convert_length("meter:2.5")` 성공 `ConversionResult` (선택) |

**기본 세션:** U-004 stdout golden **1건**만 구축. D-005는 Logic 계약 스냅샷이 필요할 때만 추가.

## 절차

1. **PASS 확인** — 대상 테스트가 green인지 narrow pytest로 확인.
2. **`tests/_approval.py`** — 없으면 생성. `assert_matches_golden(actual: str, relative: str)` 제공.
   - `relative`는 `tests/golden/` 기준 상대 경로 (예: `u004_meter_25_stdout.approved.txt`).
   - `UPDATE_GOLDEN=1`(또는 PowerShell `$env:UPDATE_GOLDEN=1`)일 때만 `.approved.*` **생성·갱신**.
   - 그 외에는 golden과 **정규화 후 exact match**; 불일치 시 diff 요약과 함께 FAIL.
3. **테스트 연결** — 기존 assertion **삭제·완화하지 않음** (E005). golden assert **추가** 또는 e2e 테스트를 golden 전용 함수로 분리.
4. **기준 파일 생성** — `UPDATE_GOLDEN=1`로 1회 실행.
5. **검증** — `UPDATE_GOLDEN` 없이 재실행 → **matched** 확인.
6. **회귀** — `pytest tests/ -v` 전체 PASS 유지.

## Golden 포맷 규칙 (UnitConverter_01)

### U-004 — CLI stdout (`.approved.txt`)

- 입력: `meter:2.5` · `boundary.cli.run` · Domain Mock **금지**
- 줄 순서: entity 변환 순서 고정 — `meter` → `feet` → `yard`
- 줄 형식 (PRD §5.1 · `src/boundary/cli.py`):

  ```
  {source_value} {source_unit} = {value} {unit}
  ```

- 기준 예시 (소수 1자리, INV-02/INV-03):

  ```
  2.5 meter = 2.5 meter
  2.5 meter = 8.2 feet
  2.5 meter = 2.7 yard
  ```

- 줄 끝: `\n` · trailing blank line 없음 · 비교 전 `\r\n` → `\n` 정규화

### D-005 — ConversionResult (`.approved.json`, 선택)

- PRD §6.1 키 순서·타입 고정: `ok`, `source`, `conversions`
- `conversions` 항목 순서: meter → feet → yard
- 오류 코드는 PRD §6.3 **문자열** 4종만: `FORMAT_INVALID`, `VALUE_NOT_NUMBER`, `UNKNOWN_UNIT`, `NEGATIVE_VALUE`  
  *(다른 프로젝트의 int[6] 1-index 코드 **사용 안 함**)*
- JSON: `sort_keys=True`, `indent=2`, trailing newline 1개

## pytest 예시

### U-004 — 캡처 (bash)

```bash
UPDATE_GOLDEN=1 python -m pytest tests/boundary/test_u_e2e_smoke.py::test_u004_golden_meter_25_stdout -v
```

### U-004 — 검증 (bash)

```bash
python -m pytest tests/boundary/test_u_e2e_smoke.py::test_u004_golden_meter_25_stdout -v
```

### U-004 — PowerShell (Windows)

```powershell
$env:UPDATE_GOLDEN=1; python -m pytest tests/boundary/test_u_e2e_smoke.py::test_u004_golden_meter_25_stdout -v
python -m pytest tests/boundary/test_u_e2e_smoke.py::test_u004_golden_meter_25_stdout -v
Remove-Item Env:UPDATE_GOLDEN -ErrorAction SilentlyContinue
```

### 전체 회귀

```bash
pytest tests/ -v
```

## `_approval.py` 계약 (요약)

```python
# tests/_approval.py — assert_matches_golden(actual, relative)
# - GOLDEN_DIR = tests/golden/
# - UPDATE_GOLDEN truthy → write GOLDEN_DIR / relative
# - else → read golden, normalize(actual) == normalize(golden) or pytest.fail with diff
```

## 금지

- golden 파일 **수동 편집**으로 테스트 통과 우회
- assert 완화·skip·xfail·기존 U-004/D-005 테스트 삭제 (E005)
- U-004 golden 캡처 시 `convert_length` **Mock** (E004 해당 패턴)
- `src/` 로직 변경 (golden은 **테스트·기준 파일만**)
- git commit (사용자 명시 요청 전)

## 보고

- **대상 ID:** U-004 (또는 D-005)
- **golden 경로:** `tests/golden/…`
- **matched:** yes / no
- **diff 요약:** 불일치 시 변경 줄·필드만 (전문 dump 생략)
- **pytest:** narrow 명령 + passed/failed · `pytest tests/ -v` 회귀 결과
- **다음:** REFACTOR(P1-11) · `/review-ecb`
