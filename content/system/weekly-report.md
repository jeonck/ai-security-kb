---
title: "AI 보안 주간 심층 리포트 — 종합 작업"
description: "매주 월요일 deep-research 방식으로 한 주를 종합하는 작업의 일정과 프롬프트 전문"
weight: 30
updated: "2026-10-20"
---

## 한눈에 보기

| 항목 | 값 |
|---|---|
| 일정 | 매주 월요일 07:44 CT (`CRON_TZ=America/Chicago 44 7 * * 1`) |
| 첫 실행 | 2026-10-26 (2026-W44) |
| 입력 | 지난 7일의 다이제스트와 전체 목록 |
| 방식 | deep-research 스킬 — 흐름별 리서처 3~4명이 근거 보강·반론·후속을 조사하고, 리포트 작성자가 종합 |
| 출력 | `content/weekly/YYYY-Www.md` → 사이트 [주간 리포트](../../weekly/) + 프로젝트 사본 |
| 알림 | 푸시 + 이메일 |

## 수집 작업과 무엇이 다른가

수집 작업은 "무슨 일이 있었나"를 빠르게 쌓는다. 주간 리포트는 쌓인 항목을 출발점으로 "이번 주를 관통하는 흐름이 무엇이고, 내 플랫폼에서 무엇을 해야 하나"를 답한다. 그래서 리서처에게 이미 수집된 항목을 다시 찾지 말고, 그 항목들 밖의 **추가 근거·반론·후속 상황**을 찾게 한다.

리포트는 다섯 부분으로 짠다: 핵심 흐름 2~4개(동작 원리 포함), 흐름별 추가 근거·반론, Kubernetes·CI/CD·에이전트 플랫폼 팀의 이번 주 점검 항목, **책 관점**(근거가 늘어난 장, 매트릭스 변화, 목차 구조 제안 — 제안만), 다음 주 지켜볼 것.

## 현재 프롬프트 (v3)

공개 사이트라 git 설정의 이메일 주소만 `<repo-owner-email>`로 가렸다.

```text
CK(오스틴의 플랫폼 엔지니어, Kubernetes·SRE·보안 전문)가 쓰는 한국어 책(대상: AI 서비스·에이전트를 운영하는 플랫폼 엔지니어·SRE·DevSecOps, 뼈대: 생명주기 × 통제 계층)을 위한 AI 보안 주간 심층 리포트를 만든다. 지난 7일 동안 GitHub 레포 jeonck/ai-security-kb에 쌓인 항목을 출발점으로 deep-research 방식으로 한 주의 흐름을 종합하고, 책 관점에서 무엇이 달라졌는지 정리해 레포에 커밋하고 claude.ai 프로젝트 "리서치" 사본도 갱신한다.

## 0. 준비
- 날짜: `TZ=America/Chicago date +%F`, `TZ=America/Chicago date +%G-W%V`, `TZ=America/Chicago date +%Y-%m-%dT%H:%M:%S%:z` 를 실행해 그 출력만 쓴다.
- 레포 연결: `mcp__claude-code-remote__add_repo`(owner "jeonck", repo "ai-security-kb", access "push") 호출 후 클론. git 사용자 `jeonck` / `<repo-owner-email>`. `python3 -c "import yaml"`이 실패하면 `pip install --break-system-packages -q pyyaml`.
- **`CLAUDE.md`를 먼저 읽고 그 형식·규칙(주간 리포트 형식, 검증, 커밋, 프로젝트 사본)을 따른다.** `content/book/outline.md`, `data/axes.yaml`, 지난 7일 `content/digest/*.md`와 거기 실린 `content/items/*.md`, 가장 최근 `content/weekly/*.md`(있으면)를 읽는다. `python3 scripts/kb.py coverage` 결과를 지난주 리포트의 "책 관점"과 비교할 수 있게 적어 둔다.
- 레포 접근이 실패하면 "레포 접근 실패로 주간 리포트를 건너뜀: <이유>"만 보고하고 끝낸다. 지난 7일 항목이 하나도 없으면 "이번 주 수집 자료가 없어 주간 리포트를 건너뜀"만 보고하고 끝낸다.

## 1. 심층 리서치
Skill 도구로 deep-research 스킬을 불러(스킬 목록에서 이름 확인, 예: `anthropic-skills:deep-research` 또는 `deep-research`) 그 절차를 따른다. 노트·중간 리포트 폴더는 레포 밖(`$HOME`)에 둔다. 사용자 질문으로 다음을 넘긴다:
"지난 7일(<시작일>~<오늘>)의 AI 보안 동향을 플랫폼 엔지니어 관점에서 종합하라. 이번 주 지식 베이스 항목(아래 목록: ID·제목·생명주기·통제·1차 출처 URL)을 출발점으로, (1) 이번 주를 관통하는 2~4개 핵심 흐름과 그 동작 원리, (2) 각 흐름에서 항목 밖의 추가 근거·반론·후속 상황(1차 원문 우선), (3) Kubernetes/CI·CD/에이전트 플랫폼을 운영하는 팀이 이번 주에 점검해야 할 구체 항목, (4) 다음 주에 지켜볼 것을 다룬다. 한국어로 쓰고, 항목을 언급할 때는 ID를 함께 적는다."
- 리서처는 흐름별 3~4명. 이미 수집된 항목을 다시 찾지 말고 근거 보강·반론·후속에 집중시킨다.
- 스킬을 찾을 수 없으면 같은 구조를 직접 재현: Agent 도구(general-purpose, run_in_background=false)로 흐름별 리서처 3~4명을 동시에 띄우고 노트를 모아 리포트를 쓴다.
- 모든 리서처에게 전달할 웹 접근 규칙: WebFetch가 거절(429·차단·법적 사유)하면 재시도·우회(curl·스크립트·캐시·미러·아카이브·브라우저 위장)하지 않는다. 다른 공개 출처로 교차 확인하고, 안 되면 "원문 미확인"으로 표시. 사실·수치·링크는 실제로 읽은 페이지에서 나온 것만. 원문 문장을 옮기지 않고 요약, 인용은 출처당 1회·15단어 미만.

## 2. 책 관점 절 (코디네이터가 직접)
리포트에 `## 책 관점` 절을 넣는다:
- 이번 주 항목이 근거를 보탠 장(outline.md의 장 번호·제목)과 항목 ID
- 매트릭스에서 새로 채워진 칸, 여전히 빈 칸 수(지난주 대비)
- 목차 구조에 대한 제안(새 절 후보, 장 순서·논지 수정 등) — **제안만 쓰고 outline.md·axes.yaml은 고치지 않는다**
- 다음 기초 문헌 작업이 우선 채우면 좋을 칸 2~3개

## 3. 저장·검증·커밋
- CLAUDE.md의 주간 리포트 형식(front matter 포함)으로 `content/weekly/<ISO 주차>.md` 에 쓴다. 이미 있으면 덮어쓰지 말고 `<ISO 주차>-2`.
- hugo가 없으면 `pip install hugo --break-system-packages -q` 후 `./scripts/check.sh`, OK여야 커밋. 실패하면 콘텐츠를 고쳐 재실행(스크립트·레이아웃·설정·book/·system/ 수정 금지).
- 바꾼 파일만 add → 커밋 `weekly: <ISO 주차>` → `main` 푸시(거절되면 `git pull --rebase` 후 재검증·재푸시).
- 프로젝트 사본: `project_write`(local_path)로 weekly → `ai-security/weekly/<ISO 주차>.md`, `python3 scripts/kb.py export-index` 결과 → `ai-security/index.md`. 실패해도 레포 커밋은 유지하고 보고에 적는다.

## 4. 보고 (최종 메시지, 한국어)
첫 줄 "📊 AI 보안 주간 리포트 <ISO 주차> 완성". 핵심 흐름 2~4개 한 줄씩, 이번 주 점검 항목 상위 3개, 책 관점 요약 한 줄(근거가 늘어난 장·남은 빈 칸 수), 사이트 링크 https://jeonck.github.io/ai-security-kb/weekly/<ISO 주차>/, 커밋 해시, Sources.
```

## 버전 변경 이력

| 버전 | 시각 (2026-10-20 CT) | 변경 |
|---|---|---|
| v1 | 07:23 | 신규. 프로젝트의 다이제스트를 읽고 `ai-security/weekly/`에 저장 |
| v2 | 07:32 | 원본을 레포로 전환: 레포 클론·`CLAUDE.md` 준수·`check.sh`·커밋·푸시, 프로젝트는 사본, 레포 접근 실패 시 대체 모드 |
| v3 | 11시경 | 항목 파일·매트릭스 기반으로 전환, "책 관점" 절 추가(목차 구조 변경은 제안만), 프로젝트 대체 모드 제거 |
