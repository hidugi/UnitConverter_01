# TDD RED — 실패 테스트 먼저

UnitConverter_01 Dual-Track TDD **RED 단계만** 수행한다.  
SSoT: `@docs/PRD.md`, `.cursorrules`. Logic D-*: `.cursor/skills/unit-converter-tdd/reference.md`.

## 필수 선언

응답 **첫 줄**에 반드시 기재:

```
Phase: red | Layer: {entity|control|boundary} | Track: {Logic|UI}
```

이어서 대상 테스트 ID(`D-*` 또는 `U-*`)와 PRD Rule ID를 한 줄로 명시한다.

## 절차

1. **ID 확인** — `docs/PRD.md`에서 Rule ID(INV, 오류 코드)와 테스트 ID 매핑 확인.
   - Logic Track: `D-*`, `tests/entity/test_d_*.py` 또는 `tests/control/test_d_*.py`
   - UI Track: `U-*`, `tests/boundary/test_u_*.py`
2. **AAA 테스트 작성** — Arrange(입력·픽스처) → Act(호출) → Assert(기대 결과·오류 코드).
   - 함수명·주석에 테스트 ID + Rule ID 기록.
   - 아직 없는 API는 import만 두고 **구현은 쓰지 않음**.
3. **`tests/`만 수정** — 신규·수정 파일은 `tests/` 하위만.
4. **pytest FAIL** — Track별 narrow 실행 후 **의도적 실패** 확인.
5. **보고** — 아래 보고 항목으로 마무리.

## pytest 예시 (bash)

Logic Track (entity + control):

```bash
pytest tests/entity tests/control -v
```

UI Track (boundary):

```bash
pytest tests/boundary -v
```

특정 파일만:

```bash
pytest tests/control/test_d_format_invalid.py -v
```

전체 회귀(RED 검증 후 참고용, green 기대하지 않음):

```bash
pytest tests/ -v
```

## 보고

- **테스트 ID:** 추가한 `D-*` 또는 `U-*` 목록
- **FAIL 요약:** 실패 테스트명 + 핵심 assertion/ImportError 메시지
- **변경 파일:** `tests/` 경로만 (예: `tests/control/test_d_unknown_unit.py`)
- **다음 단계:** GREEN 대기 (src/ 수정은 별도 `/tdd-green` 또는 사용자 요청 시)

## 금지

- `src/` 및 `UnitConverter.py` **수정·생성**
- Logic Track에서 **Domain Mock** (비율·`convert_length` 로직 Mock)
- assert 완화, `@pytest.mark.skip`, `xfail`, 실패 테스트 삭제
- RED와 GREEN·REFACTOR **동시 진행**
- git commit (사용자 명시 요청 전)
