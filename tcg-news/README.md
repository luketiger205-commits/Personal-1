# TCG 데일리 브리핑

포켓몬카드 우선의 TCG 소식을 매일 아침 조사해, 마케터 관점의 브리핑으로 보내 주는 알림이입니다.

- **실행:** Claude Code Routine "TCG 데일리 브리핑" (`trig_01N4CuVVtxvxouvReA2zVvvm`)
- **시간:** 매일 07:52 KST (`CRON_TZ=Asia/Seoul 52 7 * * *`)
- **전달:** 푸시 알림과 이메일. 전체 내용은 claude.ai/code 의 해당 세션에서 볼 수 있습니다.
- **지침:** [`BRIEF.md`](BRIEF.md) — 우선순위, 주목도 기준, 출력 형식

## 수정하는 법
- 시간·알림 채널·프롬프트 변경: claude.ai/code → Routines 에서 "TCG 데일리 브리핑"을 편집합니다.
- 관심 키워드나 경쟁사 추가: `BRIEF.md`를 편집하거나 루틴 프롬프트에 직접 추가합니다.

## 예시
- [2026-10-01](reports/2026-10-01.md) — 첫 브리핑(수동 실행)
