# D-* Logic 테스트 ID (Phase 1)

| ID | Rule / SC | 요지 |
|----|-----------|------|
| D-001 | FORMAT_INVALID | `:` 없음·빈 단위/값 |
| D-002 | VALUE_NOT_NUMBER | 숫자 파싱 실패 |
| D-003 | UNKNOWN_UNIT | meter/feet/yard 외 |
| D-004 | NEGATIVE_VALUE | `value < 0` |
| D-005 | INV-07, SC-1 | `meter:2.5` 전 단위 환산 |
| D-006 | INV-02, SC-2 | `3.28084` 비율·`3.28` 사용 시 실패 |
| D-007 | INV-08, SC-3 | 동일 입력 → 동일 출력 (refactor 회귀) |

파일명: `tests/entity/test_d_*.py`, `tests/control/test_d_*.py`
