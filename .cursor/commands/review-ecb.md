# Review ECB — 코드 수정 없이 계약·아키텍처 리뷰

UnitConverter_01 **ECB·Dual-Track·PRD 계약** 위반만 검사한다.  
**코드·테스트·설정 파일 수정 금지** (읽기·분석·표 보고만).

SSoT: `@docs/PRD.md`, `.cursorrules`, `src/`, `tests/`.

## 필수 선언

응답 **첫 줄**:

```
Phase: review | Layer: all | Track: review-ecb
```

## 절차

1. `src/entity/`, `src/control/`, `src/boundary/` 및 대응 `tests/` **읽기만**.
2. import 문·호출 관계·Mock 패턴·PRD Rule(INV, 오류 코드) 대조.
3. 아래 체크표를 채워 **위반만** 기록 (위반 없으면 `없음`).
4. 수정 제안은 **조치 열**에 한 줄만; **파일 편집·커밋 하지 않음**.

## 체크 1 — import 방향 (ECB)

허용: `boundary → control → entity` (단방향). entity는 표준 라이브러리만.

| 파일 | import 대상 | 판정 (OK / 위반) | 위반 코드 | 조치 요약 |
|------|-------------|------------------|-----------|-----------|
| `src/entity/...` | | | E001 등 | |
| `src/control/...` | | | E003 등 | |
| `src/boundary/...` | | | E002 등 | |

**역방향·건너뛰기 예:** entity→control, entity→boundary, boundary→entity, control→boundary.

## 체크 2 — entity 레이어

| 항목 | 기대 | 판정 | 비고 |
|------|------|------|------|
| 외부 레이어 import 없음 | control/boundary 미참조 | | E001 |
| I/O·CLI·포맷 없음 | 순수 도메인·비율만 | | |
| `3.28084` / `1.09361` | `3.28` 미사용 | | E007 |
| 표준 라이브러리만 | json/path 등 최소 | | |

## 체크 3 — E001~E007 위반 목록

| 코드 | 검사 내용 | 발견 여부 | 위치 (파일:줄) | 조치 요약 |
|------|-----------|-----------|----------------|-----------|
| E001 | entity → 상위 레이어 import | | | |
| E002 | boundary → entity 직접 호출/import | | | |
| E003 | 기타 ECB 역방향 의존 | | | |
| E004 | Logic Track Domain Mock | | | |
| E005 | assert 완화·skip·xfail·테스트 삭제 | | | |
| E006 | Logic/UI·RED/GREEN 혼합 (코드/테스트 구조) | | | |
| E007 | PRD 위반 (yard 누락, OOS, 오류 코드 불일치) | | | |

## 체크 4 — Logic Track Domain Mock (`tests/entity`, `tests/control`)

| 파일 | Mock 대상 | Track | 판정 | 위반 코드 |
|------|-----------|-------|------|-----------|
| `tests/entity/test_d_*.py` | | Logic | OK / 위반 | E004 |
| `tests/control/test_d_*.py` | | Logic | OK / 위반 | E004 |

**E004 해당 예:** `unittest.mock`·`pytest-mock`으로 비율·`convert_length`·변환 결과를 대체.  
**허용 (UI만):** `tests/boundary/`의 stdin/stdout·capsys Mock.

## 체크 5 — PRD 계약 (요약)

| Rule / SC | 검사 | 판정 | 위반 코드 |
|-----------|------|------|-----------|
| INV-07 | 성공 시 meter·feet·yard 전부 | | E007 |
| §6.3 오류 코드 | 4종만 사용 | | E007 |
| Phase 1 OOS | GUI·설정·동적 단위 없음 | | E007 |

## 보고 형식

- **요약:** 위반 N건 / E001~E007 해당 코드 목록
- **표:** 위 체크표만 출력 (통과 항목은 `OK` 또는 생략 가능)
- **변경 파일:** 없음 (리뷰만 수행)

## 금지

- `src/`, `tests/`, `.cursorrules` 등 **어떤 파일도 수정·생성·삭제**
- 위반 발견 시 **자동 수정·GREEN 진행**
- git commit (사용자 명시 요청 전)
