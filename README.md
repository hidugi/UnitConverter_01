
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
| [PRD](docs/PRD.md) | 입·출력, 오류 코드, Phase 로드맵, 수용 기준 (SSoT) |
| [Prompt Export](Prompting/01.REPORT-Prompt.md) | Cursor 대화 기록 |

---

## PRD 기반 — 해야 할 목록

상세 계약·오류 코드는 [`docs/PRD.md`](docs/PRD.md) 참고.

### Phase 1 — Rule · Command · Test Loop *(현재)*

**목표:** G-01 전 단위 환산 · G-02 명시적 실패 · G-03 Test Loop 회귀 보호

#### `convert_length` 구현

- [ ] **P1-01** — `convert_length(input_str)` API 정의 (`ConversionResult` 계약)
- [ ] **P1-02** — meter 기준 정규화 (INV-01) · `3.28084` / `1.09361` 비율 (INV-02, INV-03)
- [ ] **P1-03** — 성공 시 **meter·feet·yard 전부** 출력 (INV-07)
- [ ] **P1-04** — `UnitConverter.py` `main()`에서 `convert_length` 호출로 연결

#### 입력 검증 · 오류 코드

- [ ] **P1-05** — `:` 없음 → `FORMAT_INVALID`
- [ ] **P1-06** — 숫자 파싱 실패 → `VALUE_NOT_NUMBER`
- [ ] **P1-07** — 미지 단위 → `UNKNOWN_UNIT`
- [ ] **P1-08** — 음수 → `NEGATIVE_VALUE`

#### Test Loop (`tests/test_convert_length.py`)

- [ ] **P1-09** — **Red** Rule별 실패 테스트 작성 (위 오류 코드 + 정상 1건)
- [ ] **P1-10** — **Green** `convert_length` 최소 구현으로 테스트 통과
- [ ] **P1-11** — **Refactor** 비율 상수·검증 순서 정리, 회귀 유지

#### 성공 기준 (SC-1~3)

- [ ] **SC-1** — `meter:2.5` / `feet:8.2` / `yard:2.7` 픽스처 → **1초 이내** 전 단위 환산
- [ ] **SC-2** — `meter:2.5` → feet `8.2` (3.28084), yard 포함 · **3.28 사용 시 실패** 테스트
- [ ] **SC-3** — 동일 입력 두 번 → 동일 결과 · refactor 후 `pytest` green

```bash
pytest tests/ -v
```

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
