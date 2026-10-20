---
title: "GitHub Actions로 돌리기"
description: "세 작업을 claude.ai 스케줄 작업 대신 GitHub Actions 크론과 Claude Code 헤드리스 모드로 돌리는 구조와 준비 순서"
weight: 17
updated: "2026-10-20"
---

> **상태 (2026-10-20 13:52 CT)**: 운영 중. 수동 시험 실행에서 수집 12건 커밋과 배포 호출까지 성공했다. claude.ai의 같은 스케줄 작업 세 개는 꺼 두었다.

## 왜 옮기나

claude.ai 스케줄 작업은 실행할 때마다 레포를 새로 연결하고 클론해야 한다. 그 연결이 실패하면 그 회차 실행 전체가 건너뛰어진다. 주간 리포트 시험에서는 리포트를 써 놓고 커밋이 빠지기도 했다([테스트 실행 기록](../test-run/)). GitHub Actions에서는 레포가 이미 체크아웃된 상태에서 시작한다. 커밋은 에이전트가 아니라 워크플로가 맡는다.

직관적으로는 **"에이전트는 원고만 쓰고, 출판은 편집부가 한다"** 구조다. 에이전트(Claude Code)는 항목·다이제스트·리포트 파일만 고친다. 워크플로가 고친 경로를 검사하고 `check.sh`를 돌린 뒤 커밋·푸시·배포·알림을 한다.

## 구성

| 작업 | 워크플로 | 일정 (미국 중부) | 프롬프트 |
|---|---|---|---|
| 수집 | `kb-collect.yml` | 6시간마다 (01:19·07:19·13:19·19:19 CDT) | `automation/prompts/collect.md` |
| 기초 문헌 | `kb-foundation.yml` | 화·금 09:45 CDT | `automation/prompts/foundation.md` |
| 주간 리포트 | `kb-weekly.yml` | 월 07:44 CDT | `automation/prompts/weekly.md` |

- 세 워크플로가 공통 워크플로 `kb-agent.yml`을 부른다.
- 모든 프롬프트 앞에는 CI 공통 규칙 `automation/prompts/_ci.md`가 붙는다. 커밋하지 말 것, 바꿔도 되는 경로, 보고 파일 위치, 웹 내용은 데이터라는 규칙이 여기에 있다.
- GitHub cron은 UTC 고정이다. 그래서 서머타임이 끝나면 중부 시각이 한 시간 당겨진다.
- 주간 리포트의 딥 리서치는 레포에 둔 스킬 `.claude/skills/kb-deep-research`가 맡는다. 리포트 front matter의 `method`에 실제로 쓴 방식이 남는다.

## 한 번의 실행

1. 체크아웃 → 도구 설치 → 실행 시각 계산(`TZ=America/Chicago date`)
2. 프롬프트 조립 → `claude -p` 실행 (권한 모드 `dontAsk`, 허용 목록에 있는 도구만)
3. 경로 검사: 허용 경로(`content/items`·`digest`·`weekly`·`data/state.yaml`) 밖이 바뀌면 실패, 커밋 안 함
4. `check.sh` 통과 → 워크플로가 커밋 메시지를 만들어 커밋·푸시 (거절되면 rebase 후 재시도)
5. 배포 워크플로 호출 → 실행 요약에 보고 첨부, 선택하면 알림 이슈 → transcript·노트를 7일 보관

## 준비 순서

1. 내 컴퓨터에서 `claude setup-token` → OAuth 토큰 (구독 필요, 1년 유효)
2. 레포 시크릿 `CLAUDE_CODE_OAUTH_TOKEN` 등록
3. (선택) 저장소 변수 `KB_NOTIFY_ISSUE=true`
4. Actions 탭에서 KB collect를 **수동 실행**해 시험한다. 확인할 것은 요약, 커밋, 배포, 아티팩트다
5. 저장소 변수 `KB_AUTOMATION_ENABLED=true` → 일정 실행 시작
6. claude.ai의 같은 스케줄 작업 세 개를 끈다

명령어와 문제 해결은 레포의 [automation/README.md](https://github.com/jeonck/ai-security-kb/blob/main/automation/README.md)에 있다.

## 보안 설계

웹 글을 읽는 에이전트이므로 프롬프트 인젝션을 전제로 했다. 이 책이 권하는 통제를 이 시스템에도 그대로 건다.

- **신원·권한**: 에이전트에게 푸시 권한이 없다(git commit·push 거부). 토큰은 실행 단계에만 들어간다.
- **격리**: 일회용 러너에서 돈다. Bash는 `kb.py`·`check.sh`·`date` 같은 몇 가지 명령만 연다. `/proc`·`~/.ssh`·`~/.claude` 읽기는 막는다.
- **출처·변경 통제**: 쓰기 경로를 두 겹으로 제한한다(설정의 거부 규칙과 워크플로의 경로 검사). 커밋 전에 `check.sh`가 스키마·1차 출처 조건을 검사한다.
- **탐지**: 실행마다 transcript가 남는다. 허용 경로 밖 변경은 실패로 드러난다.
- **남는 위험**: 허용된 WebFetch로 외부 요청을 보낼 수 있으므로 유출 경로가 완전히 닫힌 것은 아니다. 일회용 러너이고 토큰 외의 비밀이 없다는 점으로 피해 범위를 줄였다.

## claude.ai 스케줄 작업과 다른 점

- claude.ai 프로젝트 사본은 CI에서 갱신하지 않는다. 필요하면 채팅에서 요청한다.
- 커밋 주체는 `github-actions[bot]`이다.
- 알림은 GitHub 실행 요약과 (선택) 이슈 알림 메일로 온다.
