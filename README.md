
## Unit Converter (Python)
![unit-converter](./unit-converter.jpg)
### Overview
- 사용자가 입력한 길이(`단위:값`)를 기반으로, 해당 값을 다른 모든 단위로 변환해 출력하는 프로그램.
- 새로운 단위를 추가할 때 기존 코드의 변경이 최소화되도록 설계한다.
- 각 단위 변환 로직은 테스트 코드로 검증한다.

### 가상환경 설정 및 실행
```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 가상환경 활성화 (macOS/Linux)
source venv/bin/activate

# 개발 의존성 (pytest — 테스트 실행에 필요)
pip install pytest
# 또는: pip install -e ".[dev]"

# 테스트
python -m pytest tests/ -v

# 실행
python UnitConverter.py

# 가상환경 비활성화
deactivate
```

### 기본 요구사항
1. 사용자 입력 예시:
   ```
   meter:2.5
   ```
   → 출력:
   ```
   2.5 meter = 8.2 feet
   2.5 meter = 2.7 yard
   ...
   ```

2. 현재 지원 단위:
   - meter
   - feet
   - yard

3. 새로운 단위가 추가될 때도 기존 코드의 변경이 최소화되도록 할 것.

4. 각 단위 간 변환이 정확히 계산되도록 테스트 코드를 작성할 것.

### 비즈니스 로직
- `1 meter = 3.28084 feet`
- `1 meter = 1.09361 yard`
- feet/yard 간의 비율은 meter 기반으로 계산.

### 품질 요구사항
- OCP를 만족하는 설계
- SRP를 만족하는 클래스 구성
- 입력 값 검증 (음수, 잘못된 형식, 없는 단위)

### 추가 요구사항
- **설정 외부화**
   - 변환 비율을 외부 설정 파일(JSON/YAML)에서 로드
- **동적으로 단위와 비율을 등록할 수 있도록 한다**
   - 사용자 입력으로 `1 cubit = 0.4572 meter`를 등록하고 사용 가능
- **출력 포맷 선택 기능** 
   - JSON / CSV / 표 형태 출력

---

## 문서 · 한 줄 요약

**“단위 변환 앱을 만든다”가 아니라**, meter / feet / yard 견적·도면을 **같은 비율·같은 결과**로 환산할 수 있는 **계약**을 고정한다.

**Mom Test 근거:** *견적은 meter, 도면은 feet라서 반나절 · 3.28 vs 3.28084로 재단 · yard는 변환표에 없음.*

| 문서 | 용도 |
|------|------|
| [Mom Test 보고서](Report/01.REPORT.md) | 인터뷰·증거·진짜/표면 문제 (STEP 1) |
| [문제 정의 보고서](Report/01.UnitConverter_ProblemDefinition_Report.md) | Invariant, R-G-I-O, 세션 3 범위 |
| [Harness · Cursor 설계](Report/02.REPORT.md) | 세션 3 — Harness · Rule · Hook |
| [RED 스켈레톤](Report/03.REPORT.md) | 세션 4 — D/U RED · 테스트 스켈레톤 |
| [GREEN · CLI](Report/04.REPORT.md) | 세션 5 — Logic+UI GREEN · P1-04 CLI |
| [Golden Master](Report/04.REPORT-GoldenMaster.md) | U-004 stdout 기준선 · `tests/_approval.py` |
| [REFACTOR 스멜 스캔](Report/05.REPORT-refactor-smell.md) | P0/P1/P2 스멜 · `/refactor-safe` 후보 |
| [PRD](docs/PRD.md) | 입·출력, 오류 코드, Phase 로드맵, 수용 기준 (SSoT) |
| [테스트 플랜](docs/TEST_PLAN.md) | Dual-Track TDD · D-*/U-* · RED/GREEN/REFACTOR 순서 |
| [Golden Master Command](.cursor/commands/golden-master.md) | `/golden-master` — 기준선 캡처·검증 |
| [Prompt Export](Prompting/05.REPORT-refactor-smell-Prompt.md) | 최신 Cursor 대화 기록 |

---

## PRD 기반 — 해야 할 목록

상세 계약·오류 코드는 [`docs/PRD.md`](docs/PRD.md) 참고.

### Phase 1 — Rule · Command · Test Loop *(현재)*

**목표:** G-01 전 단위 환산 · G-02 명시적 실패 · G-03 Test Loop 회귀 보호

#### `convert_length` 구현

- [x] **P1-01** — `convert_length(input_str)` API 정의 (`ConversionResult` 계약)
- [x] **P1-02** — meter 기준 정규화 (INV-01) · `3.28084` / `1.09361` 비율 (INV-02, INV-03)
- [x] **P1-03** — 성공 시 **meter·feet·yard 전부** 출력 (INV-07)
- [x] **P1-04** — `UnitConverter.py` `main()`에서 `convert_length` 호출로 연결

#### 입력 검증 · 오류 코드

- [x] **P1-05** — `:` 없음 → `FORMAT_INVALID`
- [x] **P1-06** — 숫자 파싱 실패 → `VALUE_NOT_NUMBER`
- [x] **P1-07** — 미지 단위 → `UNKNOWN_UNIT`
- [x] **P1-08** — 음수 → `NEGATIVE_VALUE`

#### RED 단계 — Logic Track *(tests만 작성, `src/` 수정 금지)*

상세: [`docs/TEST_PLAN.md`](docs/TEST_PLAN.md) · 선언: `Phase 1 / Layer {entity|control} / Track Logic / RED`

**공통 (RED마다)**

- [x] **RED-00** — `@docs/PRD.md` Rule ID 확인 후 `tests/{entity|control}/test_d_*.py`에 **실패 테스트만** 추가
- [x] **RED-00** — 함수명·주석에 `D-*` + Rule ID 기록 · Domain Mock 사용 금지 (E004)
- [x] **RED-00** — `pytest tests/entity tests/control -v` 실행 → **의도적 FAIL** 확인

**검증 · 오류 (`tests/control/`)**

- [x] **D-001** — `FORMAT_INVALID` — `meter2.5`, `:2.5`, `meter:` → `ok=False`, `error="FORMAT_INVALID"` (`test_d_format.py`)
- [x] **D-002** — `VALUE_NOT_NUMBER` — `meter:abc`, `feet:2.5.3` → `error="VALUE_NOT_NUMBER"` (`test_d_format.py`)
- [x] **D-003** — `UNKNOWN_UNIT` — `cubit:1.0`, `inch:10` → `error="UNKNOWN_UNIT"`, message에 unit 포함 (`test_d_units.py`)
- [x] **D-004** — `NEGATIVE_VALUE` — `meter:-1`, `feet:-0.1` → `error="NEGATIVE_VALUE"` (`test_d_validation.py`)

**정상 환산 · 수용 기준**

- [x] **D-005** — INV-07, SC-1 — 픽스처 `meter:2.5` / `feet:8.2` / `yard:2.7` → conversions에 **meter·feet·yard 3개** (`test_d_convert.py`)
- [x] **D-006** — INV-02, SC-2 — entity 상수 `3.28084` / `1.09361` assert · `meter:2.5` → feet=`8.2`, yard=`2.7` · **3.28 사용 시 불일치** (`test_d_ratios.py`)
- [x] **D-007** — INV-08, SC-3 — 동일 `input_str` 2회 호출 → `ConversionResult` 완전 동일 (`test_d_idempotent.py`)

```bash
pytest tests/entity tests/control -v   # GREEN: 17 passed
```

#### GREEN 단계 — Logic Track *(src/entity · src/control)*

선언: `Phase 1 / Layer {entity|control} / Track Logic / GREEN`

- [x] **D-001 GREEN** — `FORMAT_INVALID` 검증 (`src/control/convert_length.py`)
- [x] **D-002 GREEN** — `VALUE_NOT_NUMBER` 검증 (`src/control/convert_length.py`)
- [x] **D-003 GREEN** — `UNKNOWN_UNIT` 검증 (`src/control/convert_length.py`)
- [x] **D-004 GREEN** — `NEGATIVE_VALUE` 검증 (`src/control/convert_length.py`)
- [x] **D-005 GREEN** — 3 픽스처 전 단위 환산 (`src/entity/convert_length.py`, `src/control/convert_length.py`)
- [x] **D-006 GREEN** — 비율 상수 `3.28084` / `1.09361` (`src/entity/ratios.py`)
- [x] **D-007 GREEN** — 결정적 `ConversionResult` (`src/control/convert_length.py`)

#### RED 단계 — UI Track *(Logic Track 전체 green 이후)*

선언: `Phase 1 / Layer boundary / Track UI / RED` · Logic/UI Track **한 사이클에 섞지 않음** (E006)

- [x] **U-001** — Mock 성공 — CLI stdout에 `8.2 feet`, `2.7 yard` 포함 (`tests/boundary/test_u_cli_success.py`)
- [x] **U-002** — Mock `FORMAT_INVALID` — 형식 오류 안내 출력 (`tests/boundary/test_u_cli_errors.py`)
- [x] **U-003** — Mock `UNKNOWN_UNIT` — `Unknown unit: cubit` 유사 메시지 (`tests/boundary/test_u_cli_errors.py`)
- [x] **U-004** — end-to-end smoke — `meter:2.5` boundary→control, Logic 결과와 CLI 출력 일치 (`tests/boundary/test_u_e2e_smoke.py`)
- [x] **U-004 golden** — Golden Master — `meter:2.5` CLI stdout ↔ `tests/golden/u004_meter_25_stdout.approved.txt` (`test_u004_golden_meter_25_stdout`)

```bash
pytest tests/boundary -v   # GREEN + Golden: 5 passed
```

#### GREEN 단계 — UI Track *(src/boundary)*

선언: `Phase 1 / Layer boundary / Track UI / GREEN`

- [x] **U-001 GREEN** — 성공 CLI stdout (`src/boundary/cli.py`)
- [x] **U-002 GREEN** — `FORMAT_INVALID` 메시지 출력 (`src/boundary/cli.py`)
- [x] **U-003 GREEN** — `UNKNOWN_UNIT` 메시지 출력 (`src/boundary/cli.py`)
- [x] **U-004 GREEN** — boundary→control e2e smoke (`src/boundary/cli.py` → control)

#### GREEN · REFACTOR *(RED 완료 후)*

- [x] **P1-10** — **Green** — D-001~D-007 · U-001~U-004 최소 구현 · `pytest tests/ -v` **21 passed**
- [ ] **P1-11** — **Refactor** — 스멜 기반 구조 개선 · assertion·golden 변경 금지 · `pytest tests/ -v` **22 passed** 유지 (SC-3)

#### GREEN PASS *(Golden Master 선행 · SC-T5)*

Phase 1 **Rule · Command · Test Loop** GREEN PASS 완료.

| ID | 검증 | 결과 |
|----|------|:----:|
| **GP-01** | Logic Track — `pytest tests/entity tests/control -v` | 17 passed |
| **GP-02** | UI Track — `pytest tests/boundary -v` | 5 passed |
| **GP-03** | 전체 회귀 — `pytest tests/ -v` | 22 passed |
| **GP-04** | CLI e2e — `UnitConverter.py` → `boundary.cli.run` (P1-04) | ✅ |
| **GP-05** | SC-1~3 · G-01~03 — D-005~D-007 · U-001 · U-004 | ✅ |
| **SC-T5** | TEST_PLAN §10 Phase 1 GREEN PASS | ✅ |

```bash
pytest tests/entity tests/control -v   # Logic: 17 passed
pytest tests/boundary -v               # UI + golden: 5 passed
pytest tests/ -v                       # 회귀 기준선: 22 passed
python UnitConverter.py                # P1-04 CLI (예: meter:2.5)
```

#### Golden Master *(GREEN PASS 이후 · REFACTOR 전)*

선언: `Phase 1 / Layer boundary / Track UI / Golden Master`

- [x] **GM-01** — `tests/_approval.py` — `assert_matches_golden(actual, relative)`
- [x] **GM-02** — U-004 golden — `test_u004_golden_meter_25_stdout` (Mock 금지 · real e2e)
- [x] **GM-03** — 기준 파일 — `tests/golden/u004_meter_25_stdout.approved.txt`
- [x] **GM-04** — matched 검증 · `pytest tests/ -v` **22 passed**

```powershell
# 기준 파일 재생성 (Windows)
$env:UPDATE_GOLDEN=1
python -m pytest tests/boundary/test_u_e2e_smoke.py::test_u004_golden_meter_25_stdout -v
```

상세: [`.cursor/commands/golden-master.md`](.cursor/commands/golden-master.md) · [`Report/04.REPORT-GoldenMaster.md`](Report/04.REPORT-GoldenMaster.md)

#### REFACTOR — 스멜 스캔 *(P1-11 선행 · 코드 수정 없음)*

선언: `Phase: refactor | Scope: src/ tests/ | Track: Logic+UI`

- [x] **RF-01** — pytest 전제 — `pytest tests/ -v` **22 passed**
- [x] **RF-02** — 6종 스멜 스캔 — P0 1 · P1 2 · P2 2 · ECB E001~E003 없음
- [x] **RF-03** — `/refactor-safe` 후보 3건 선정 (Budget: 파일≤3 · 메서드≤3)
- [ ] **RF-04** — 후보 1 — `_make_error()` 추출 (`src/control/convert_length.py`)
- [ ] **RF-05** — 후보 2 — 검증 단계 private 함수 분리
- [ ] **RF-06** — 후보 3 — `DECIMAL_PLACES = 1` (`src/entity/convert_length.py`)
- [ ] **RF-07** — REFACTOR 후 golden matched · 22 passed 재확인

상세: [`Report/05.REPORT-refactor-smell.md`](Report/05.REPORT-refactor-smell.md)

**다음:** `/refactor-safe` 후보 1 (`_make_error` 추출) → P1-11 완료 · `/review-ecb`

#### Phase 1 — 하지 않는 것 *(Mom Test 표면 문제)*

- 단위 변환 **웹·모바일 앱** · **GUI** · 견적서 PDF
- JSON/YAML 설정 · 동적 cubit 등록 · 출력 포맷 선택
- inch/cm 등 **전 단위 일반화**

---

### Phase 2 — OCP / SRP 리팩터 *(후속)*

- [ ] **P2-01** — 단위 변환 인터페이스 분리 (OCP)
- [ ] **P2-02** — 입력 검증 / 환산 / 출력 클래스 분리 (SRP)
- [ ] **P2-03** — `parse_input` 분리 또는 내부 모듈화 (선택)
- [ ] **P2-04** — 리팩터 후 SC-3 회귀 테스트 유지

---

### Phase 3 — 설정 외부화 · 동적 단위 *(README 추가 요구)*

- [ ] **P3-01** — 변환 비율 JSON/YAML 로드
- [ ] **P3-02** — 런타임 단위 등록 (`1 cubit = 0.4572 meter` 등)
- [ ] **P3-03** — 동적 단위 등록·로드 TC 작성

---

### Phase 4 — 출력 포맷 · CLI *(후속)*

- [ ] **P4-01** — JSON / CSV / 표 형태 출력 선택
- [ ] **P4-02** — CLI 입출력 polish
- [ ] **P4-03** — 포맷별 TC 작성

---

## 생성형AI를 활용한 Activities (6 시간)

1. 문제 코드 및 기본 요구사항 분석 (0.5시간)
   - 기본 코드구조, 로직 이해
2. 기본 요구사항 및 품질 요구사항 구현 (2시간)
   - OCP를 만족하는 인터페이스 구현 
   - SRP를 만족하도록 클래스 구현 
   - 입력값 검증을 위한 구현
3. TC 구현 (0.5시간)
   - 단위변환 기능 검증 및 입력 값 검증 TC 작성 
4. 추가 요구사항 구현 (2시간)
   - 3개 요구사항 구현 및 TC 작성 
5. 회고 및 발표 (1시간)
   - 실습 목표와 달성도
   - AI를 어떻게 활용했나? 도움이 된 순간과 한계는?
   - TC를 추가해보면서 개선에 미친 영향, TC 작성 팁
   - 클린코드와 리팩토링에서 느낀 장점과 어려운점
