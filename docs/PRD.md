# Unit Converter — 제품 요구사항 (PRD)

| 항목 | 내용 |
|------|------|
| 프로젝트 | UnitConverter_01 |
| 버전 | 0.1 (초안) |
| 작성일 | 2026-06-05 |
| 문서 상태 | 초안 |
| 문제 정의 | [`Report/01.UnitConverter_ProblemDefinition_Report.md`](../Report/01.UnitConverter_ProblemDefinition_Report.md) |
| Mom Test | [`Report/01.REPORT.md`](../Report/01.REPORT.md) |
| 실습 README | [`README.md`](../README.md) |

---

## 1. 배경 · Mom Test

### 1.1 페르소나

소규모 **인테리어·리모델링 업체 현장 소장** — 국내·해외 견적과 현장 도면의 **길이 단위**가 섞인다.

### 1.2 진짜 문제 (한 문장)

해외·국내 견적의 길이 단위가 현장에서 쓰는 단위와 다를 때마다, 사람마다 다른 방식으로 환산하다가 **오차·재작업·일정 지연**이 실제로 발생한다.

**Mom Test 증거:**

- *“견적은 **meter**, 도면은 **feet**라서 치수 맞추느라 **반나절**.”*
- *“**3.28** vs **3.28084** → **2cm** 차이, **재단**.”*
- *“변환표에 **yard** 없어서 **또 따로** 찾아봤어요.”*

### 1.3 제품 방향 (솔루션 최소화)

1차 목표는 **“완성 앱”** 이 아니라 **반복 가능한 길이 환산 계약**이다.  
설정 외부화·동적 단위·출력 포맷·GUI는 **후속 Phase**.

---

## 2. 목표 · 비목표

### 2.1 목표 (Phase 1 — 세션 3)

| ID | 목표 |
|----|------|
| **G-01** | meter / feet / yard 입력에 대해 **Rule(INV)** 기반 **전 단위 환산** 제공 |
| **G-02** | 잘못된 입력·미지 단위·음수에 **명시적 실패** 반환 |
| **G-03** | **Test Loop**로 환산 **회귀 보호** (SC-1~3) |

### 2.2 비목표 (표면 문제 — 하지 않음)

| ID | 비목표 | 이유 |
|----|--------|------|
| **OOS-01** | “**단위 변환 앱·웹**” | Mom Test 표면 문제 |
| **OOS-02** | **GUI / 모바일 / 견적서 PDF** | Phase 1 Output 아님 |
| **OOS-03** | **JSON·YAML 설정·동적 cubit 등록** | README 추가 요구 — 후속 |
| **OOS-04** | **JSON / CSV / 표 출력 포맷 선택** | 후속 Phase |
| **OOS-05** | **inch, cm 등 전 단위 일반화** | 3단위 계약 우선 |
| **OOS-06** | OCP/SRP/TDD를 **제품 목표**로 기재 | 방법론 ≠ 사용자 고통 |

---

## 3. 도메인 규칙

### 3.1 용어

| 용어 | 정의 |
|------|------|
| **기준 단위** | **meter** — 모든 환산의 허브 |
| **지원 단위** | `meter`, `feet`, `yard` |
| **입력 문자열** | `단위:숫자` — 예: `meter:2.5` |
| **전 단위 출력** | 입력값을 meter·feet·yard **모두**로 표현한 결과 |

### 3.2 Invariant (SSoT)

| ID | 규칙 |
|----|------|
| **INV-01** | 기준 단위 = **meter** |
| **INV-02** | `1 meter = 3.28084 feet` |
| **INV-03** | `1 meter = 1.09361 yard` |
| **INV-04** | 입력: `unit:value`, `:` 필수, `value`는 `float` 파싱 가능 |
| **INV-05** | `unit` ∈ {`meter`, `feet`, `yard`} |
| **INV-06** | `value < 0` → 거부 |
| **INV-07** | 성공 시 **meter·feet·yard** 변환값 **전부** 포함 |
| **INV-08** | 동일 입력 → 동일 출력 |

### 3.3 환산 공식

```
meter_value = 입력을 meter로 정규화
  - meter: value
  - feet:  value / 3.28084
  - yard:  value / 1.09361

출력:
  meter = meter_value
  feet  = meter_value * 3.28084
  yard  = meter_value * 1.09361
```

---

## 4. R-G-I-O (Phase 1)

| | 내용 |
|---|---|
| **Role** | 현장 소장 / 호출자 — 견적·도면 **단위 불일치** 환산 필요 |
| **Goal** | SC-1~3 충족하는 **convert_length** |
| **Input** | `input_str: str` — `unit:value` |
| **Output** | `ConversionResult` — 아래 §6.1 |

---

## 5. 기능 · Command (Phase 1)

### 5.1 `convert_length(input_str) -> ConversionResult`

**우선순위:** P0 (세션 3 필수)

| 단계 | 검사 / 동작 | Rule ID |
|------|-------------|---------|
| 1 | `:` 존재 | `FORMAT_INVALID` |
| 2 | `value` float 파싱 | `VALUE_NOT_NUMBER` |
| 3 | `unit` 지원 여부 | `UNKNOWN_UNIT` |
| 4 | `value >= 0` | `NEGATIVE_VALUE` |
| 5 | meter 정규화 후 **전 단위** 환산 | `INV-01`~`INV-03`, `INV-07` |

### 5.2 `parse_input(input_str) -> ParsedInput` *(선택 P1)*

- **INV-04~06** 만 검증: `{ unit, value }` 또는 실패.
- `convert_length` 내부 단계로 통합해도 됨.

### 5.3 출력 반올림 정책 (초안)

README 예시는 **소수 1자리** 표시 (`8.2`, `2.7`).  
**내부 계산은 전체 정밀도**, 표시만 반올림 — 구현·테스트에서 **픽스처로 고정**.

---

## 6. 입출력 · 오류 계약

### 6.1 ConversionResult (성공)

```python
{
  "ok": True,
  "source": { "unit": "meter", "value": 2.5 },
  "conversions": [
    { "unit": "meter", "value": 2.5 },
    { "unit": "feet",  "value": 8.2 },
    { "unit": "yard",  "value": 2.7 }
  ]
}
```

### 6.2 ConversionResult (실패)

```python
{
  "ok": False,
  "error": "UNKNOWN_UNIT",   # Rule ID
  "message": "Unknown unit: cubit"
}
```

### 6.3 오류 코드

| 코드 | 조건 |
|------|------|
| `FORMAT_INVALID` | `:` 없음 또는 빈 단위/값 |
| `VALUE_NOT_NUMBER` | 숫자 파싱 실패 |
| `UNKNOWN_UNIT` | meter / feet / yard 외 |
| `NEGATIVE_VALUE` | `value < 0` |

---

## 7. 성공 기준 (수용)

| ID | Given | When | Then | Mom Test |
|----|-------|------|------|----------|
| **SC-1** | `meter:2.5`, `feet:8.2`, `yard:2.7` 픽스처 | `convert_length` | **1초 이내** 전 단위 결과 | 반나절 → 즉시 환산 |
| **SC-2** | `meter:2.5` | `convert_length` | feet=`8.2`(3.28084 기준), yard 포함, **3.28 사용 시 실패 테스트** | 3.28·재단 + yard 누락 방지 |
| **SC-3** | 동일 `input_str` 두 번 | `convert_length` | 동일 결과; refactor 후 pytest green | 팀원마다 다른 계산 → 재현 |

---

## 8. Test Loop (Phase 1)

```
Red   → Rule별 실패 테스트 (FORMAT_INVALID, NEGATIVE_VALUE, UNKNOWN_UNIT, 비율 검증, 정상 1건)
Green → convert_length 최소 구현 (기존 UnitConverter.py 리팩터 또는 대체)
Refactor → 비율 상수·검증 순서 정리, SC-3 유지
```

**산출:** `tests/test_convert_length.py` (또는 동등 경로)

**실행:**

```bash
pytest tests/ -v
```

---

## 9. 비기능 (NFR)

| ID | 요구 |
|----|------|
| **NFR-01** | 환산 로직 **pytest**로 SC-1~3 커버 (Phase 1) |
| **NFR-02** | Rule ID ↔ 테스트 **1:1 추적** |
| **NFR-03** | PRD ↔ Problem Definition **동기** (SSoT: 본 PRD, 서술: Report) |

---

## 10. Phase 로드맵 (초안)

| Phase | 범위 | 산출 |
|-------|------|------|
| **1** (세션 3) | Rule, Command, Test Loop | `convert_length`, tests |
| **2** | OCP/SRP 리팩터, 입력 검증 클래스 분리 | Entity·인터페이스 |
| **3** | 설정 외부화 (JSON/YAML), 동적 단위 등록 | Config 로더 |
| **4** | 출력 포맷 (JSON/CSV/표), CLI polish | Formatter, Boundary |

---

## 11. 추적성

| Mom Test | PRD |
|----------|-----|
| 반나절 치수 맞춤 | SC-1, G-01 |
| 3.28 vs 3.28084 | INV-02, SC-2 |
| yard 변환표 누락 | INV-07, SC-2 |
| 표면(변환 앱) | §2.2 OOS |
| 팀원마다 다른 계산 | INV-08, SC-3, §8 |

---

## 12. 개정 이력

| 버전 | 날짜 | 변경 |
|------|------|------|
| 0.1 | 2026-06-05 | Mom Test·세션 3 초안 — Problem Definition Report와 동시 생성 |

---

*끝.*
