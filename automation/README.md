# GitHub Actions로 돌리는 지식 베이스 작업

claude.ai 스케줄 작업으로 돌던 세 작업(수집 · 기초 문헌 · 주간 리포트)을 **GitHub Actions 크론 + Claude Code 헤드리스 모드**로 옮긴 것이다. 레포 연결 단계가 없어진다. 워크플로가 레포를 체크아웃한 상태에서 에이전트를 실행하기 때문이다.

워크플로는 처음에 **꺼진 상태**로 들어 있다. 저장소 변수 `KB_AUTOMATION_ENABLED`를 `true`로 바꿔야 일정대로 돈다. 수동 실행(Run workflow)은 언제나 할 수 있다.

## 한눈에 보기

| 작업 | 워크플로 | 일정 (cron은 UTC) | 미국 중부 시각 | 프롬프트 |
|---|---|---|---|---|
| 수집 (AI 보안 리서치 조교) | `.github/workflows/kb-collect.yml` | `19 * * * *` | 매시간 깨우고, 실제 실행은 약 5~6시간마다 | `automation/prompts/collect.md` |
| 기초 문헌 수집 | `.github/workflows/kb-foundation.yml` | `45 14,15,16,17 * * 2,5` | 화·금 09:45 CDT부터, 하루 한 번만 실제 실행 | `automation/prompts/foundation.md` |
| 주간 심층 리포트 | `.github/workflows/kb-weekly.yml` | `44 12,13,14,15,16 * * 1` | 월 07:44 CDT부터, 리포트가 생기면 그날 나머지는 건너뜀 | `automation/prompts/weekly.md` |

세 워크플로 모두 공통 워크플로 `.github/workflows/kb-agent.yml`을 부른다. 모든 프롬프트 앞에는 `automation/prompts/_ci.md`(CI 공통 규칙)가 붙는다. GitHub cron은 UTC로 고정이라 11월 첫 일요일(서머타임 종료)부터는 중부 시각이 한 시간 당겨진다. 3월에 다시 원래 시각으로 돌아온다.

### 크론이 늦거나 빠질 때

GitHub은 크론 일정을 보장하지 않는다. 붐비면 몇 시간씩 늦추거나 건너뛴다. 운영 첫날에도 19:19 CT 예정 실행이 23:47에 돌았고, 01:19 CT 예정 실행은 아예 돌지 않았다. 그래서 일정은 자주 깨우고, 실행 첫 단계("Decide whether to run")에서 실제로 돌지 정한다.

- 기준은 이 작업이 마지막으로 **실제로** 돈 시각이다. 실제로 돈 실행만 `kb-<작업>-<run id>` 아티팩트를 남기므로, 그 아티팩트의 생성 시각을 본다. 건너뛴 실행은 아티팩트를 남기지 않는다.
- 수집은 마지막 실제 실행이 5시간 안이면 건너뛴다. 기초 문헌은 20시간, 주간 리포트는 72시간이 기준이다. 주간 리포트는 이번 주 파일이 이미 있어도 건너뛴다.
- 건너뛰는 실행은 Claude를 부르지 않고 30초 안에 끝난다. 수동 실행은 이 검사를 하지 않는다.

## 한 번의 실행은 이렇게 흐른다

1. 레포 체크아웃 → Hugo·PyYAML·Node·Claude Code 설치
2. 실행 시각을 `TZ=America/Chicago date`로 계산 (날짜를 모델이 추론하지 않게 프롬프트에 직접 넣는다)
3. 주간 리포트는 이번 주 파일이 이미 있으면 건너뛴다 (수동 실행의 `force`로 강제 가능)
4. 프롬프트 조립: `_ci.md` + 작업 프롬프트. `@@KB_...@@` 자리표시자를 실제 값으로 바꾼다
5. `claude -p` 실행. 권한 모드는 `dontAsk`이고, `automation/claude-settings.json`에 적힌 허용 목록에 있는 도구만 쓴다. 에이전트는 **파일만 고친다**
6. **경로 검사**: `content/items/`, `content/digest/`, `content/weekly/`, `data/state.yaml` 밖이 바뀌었거나 파일이 지워졌으면 실패로 끝낸다(커밋하지 않음)
7. `./scripts/check.sh` → 통과해야 커밋한다
8. 커밋 메시지는 CLAUDE.md 규칙대로 워크플로가 만든다 (`digest: … — N건 추가`, `foundation: …`, `weekly: …`, `items: 원문 확인 보완 (…)`). 푸시가 거절되면 rebase 후 최대 3번 재시도한다
9. 배포 워크플로(`deploy.yml`)를 직접 호출한다. `GITHUB_TOKEN`으로 한 푸시는 push 이벤트를 만들지 않기 때문이다
10. 보고: 에이전트가 쓴 보고 파일을 실행 요약(Summary)에 붙인다. `KB_NOTIFY_ISSUE=true`면 `kb-report` 라벨 이슈도 연다(GitHub 알림 메일이 온다)
11. 실행 기록(transcript), 보고, 조사 노트를 7일 보관 아티팩트로 올린다

## 준비 (순서대로)

### 1. OAuth 토큰 만들기 (내 컴퓨터에서)

```bash
claude setup-token
```

- Claude Pro·Max·Team·Enterprise 구독이 필요하다. 토큰은 **1년** 유효하다. 만료 전에 다시 만들어 시크릿을 갈아 끼운다.
- 토큰은 만든 사람의 구독 사용량을 쓴다. 6시간 수집이 하루 4번, 주간 리포트가 주 1번 돌면 그만큼 사용량이 나간다.
- 무인 정기 실행이 구독 약관상 허용되는지는 문서에 명시돼 있지 않다. 필요하면 Anthropic 약관이나 지원팀에 확인한다.

### 2. 시크릿 등록

GitHub 레포 → Settings → Secrets and variables → Actions → **New repository secret**

| 이름 | 값 |
|---|---|
| `CLAUDE_CODE_OAUTH_TOKEN` | 1에서 만든 토큰 |

또는 `gh secret set CLAUDE_CODE_OAUTH_TOKEN` (값을 붙여 넣는다).

`ANTHROPIC_API_KEY`는 등록하지 않는다. 둘 다 있으면 Claude Code는 API 키를 쓴다. 워크플로는 둘 중 하나만 넘기며, OAuth 토큰을 먼저 쓴다.

### 3. 저장소 변수 (Settings → Secrets and variables → Actions → Variables)

| 이름 | 값 | 필수 |
|---|---|---|
| `KB_AUTOMATION_ENABLED` | `true`로 두면 일정 실행이 켜진다. **시험이 끝날 때까지 만들지 않는다** | 켤 때 |
| `KB_NOTIFY_ISSUE` | `true`면 실행마다 보고 이슈를 연다 (알림용) | 선택 |
| `KB_MODEL` | 기본값 `claude-opus-5-5` | 선택 |
| `CLAUDE_CODE_VERSION` | 기본값 `latest`. 재현성이 필요하면 특정 버전으로 고정한다 | 선택 |

```bash
gh variable set KB_NOTIFY_ISSUE --body true
```

### 4. Actions 권한

Settings → Actions → General에서 Actions 실행이 허용되어 있는지 확인한다. 쓰기 권한(contents·actions·issues)은 워크플로 파일에서 작업 단위로 요청하므로 기본 "Workflow permissions"는 읽기 전용이어도 된다. 조직 정책이 쓰기 권한 요청을 막고 있으면 풀어야 한다.

### 5. 수동 시험

```bash
gh workflow run kb-collect.yml          # 또는 Actions 탭 → KB collect → Run workflow
gh run watch
```

확인할 것:

- 실행 요약(Summary)에 보고가 붙었는가
- 새 항목이 있으면 `digest: …` 커밋이 생겼는가
- 이어서 "Deploy site" 실행이 성공했는가
- 아티팩트 `kb-collect-<run id>`에 transcript와 노트가 있는가

주간 리포트를 이번 주에 다시 시험하려면 `gh workflow run kb-weekly.yml -f force=true` 로 실행한다(`<주차>-2.md`로 저장된다).

### 6. 일정 켜기

```bash
gh variable set KB_AUTOMATION_ENABLED --body true
```

### 7. claude.ai 스케줄 작업 끄기

같은 일이 두 번 돌지 않게 claude.ai의 "AI 보안 리서치 조교", "AI 보안 기초 문헌 수집", "AI 보안 주간 심층 리포트"를 끈다(삭제하지 않고 꺼 두면 되돌리기 쉽다).

## 보안 설계

이 작업은 웹에서 읽은 글을 다루므로 프롬프트 인젝션을 전제로 설계했다. 책이 말하는 원칙을 그대로 적용한 것이다.

- **에이전트에게 푸시 권한을 주지 않는다.** git commit·push는 거부 목록에 있다. 커밋은 경로 검사와 `check.sh`를 통과한 뒤 워크플로가 한다.
- **허용 목록 방식.** `dontAsk` 모드라 허용 목록에 없는 도구 호출은 모두 거부된다. Bash는 `kb.py`, `check.sh`, `date`, `ls` 같은 몇 가지 명령만 열었다. curl·wget·env·printenv와 `/proc`, `~/.ssh`, `~/.claude` 읽기는 따로 막았다.
- **쓰기 경로 제한을 두 겹으로 둔다.** 설정의 Edit 거부 규칙이 1차이고, 워크플로의 경로 검사가 2차다.
- **시크릿은 하나만, 실행 단계에만.** 토큰은 Claude 실행 단계의 환경에만 들어간다. 다른 단계와 아티팩트에는 들어가지 않는다.
- **웹 내용은 데이터.** 공통 규칙(`_ci.md`)이 페이지 안의 지시를 따르지 말라고 명시하고, 리서처에게도 같은 규칙을 넘기게 한다.
- **남는 위험.** 허용된 도구(WebFetch)로 외부에 요청을 보낼 수 있으므로 정보 유출 경로가 완전히 닫힌 것은 아니다. 러너가 일회용이고 토큰 외의 비밀이 없다는 점으로 피해 범위를 줄였다. 공개 레포의 아티팩트는 레포를 읽을 수 있는 사람이 내려받을 수 있다. transcript에는 시크릿이 들어가지 않지만, 꺼리면 업로드 단계를 지운다.

## claude.ai 스케줄 작업과 다른 점

| | claude.ai 스케줄 작업 | GitHub Actions |
|---|---|---|
| 레포 접근 | add_repo로 연결 후 클론 (실패하면 건너뜀) | 체크아웃된 상태에서 시작 |
| 커밋·푸시 | 에이전트가 직접 | 워크플로가 검증 후 (`github-actions[bot]`) |
| 배포 | 푸시가 배포를 띄움 | 워크플로가 `deploy.yml`을 호출 |
| claude.ai 프로젝트 사본 | 자동 갱신 | **없음.** 필요하면 채팅에서 "프로젝트 사본 갱신해줘" |
| 알림 | 푸시·이메일 | 실행 요약 + (선택) 이슈 알림 메일 |
| 주간 리포트의 딥 리서치 | `anthropic-skills:deep-research` | 레포 스킬 `.claude/skills/kb-deep-research` |
| 실행 기록 | 볼 수 없음 | transcript 아티팩트 (7일) |

## 문제 해결

| 증상 | 확인할 곳 |
|---|---|
| 요약에 "보고 파일 없음" | 아티팩트의 `transcript.jsonl` 마지막 부분. 턴 한도(`max_turns`)나 시간 한도(90분)에 걸렸을 수 있다 |
| "허용되지 않은 변경" | 에이전트가 허용 경로 밖을 고쳤다. 커밋은 되지 않았다. transcript에서 어떤 지시로 고쳤는지 본다 |
| `check.sh` 실패 | 콘텐츠 형식 오류. 커밋은 되지 않았다. 다음 실행이 다시 시도한다 |
| 401·인증 오류 | 토큰 만료(1년) 또는 시크릿 오타. `claude setup-token`으로 다시 만든다 |
| 일정 실행이 안 돈다 | `KB_AUTOMATION_ENABLED` 변수 확인. 공개 레포는 60일 동안 활동이 없으면 일정 실행이 꺼진다 |
| 실행 목록에 몇 초짜리 성공이 많다 | 정상이다. 매시간 깨운 실행이 "최근에 이미 돌았다"며 건너뛴 것이다. 요약에 건너뛴 이유가 적힌다 |
| 주간 리포트가 건너뛰어짐 | 이번 주 파일이 이미 있다. 수동 실행에서 `force`를 켠다 |

## 파일

| 파일 | 역할 |
|---|---|
| `.github/workflows/kb-agent.yml` | 공통 실행 워크플로 (설치 → 실행 → 검사 → 커밋 → 배포 → 보고) |
| `.github/workflows/kb-collect.yml`, `kb-foundation.yml`, `kb-weekly.yml` | 일정과 수동 실행 입구 |
| `automation/prompts/_ci.md` | CI 공통 규칙 (모든 프롬프트 앞에 붙음) |
| `automation/prompts/collect.md`, `foundation.md`, `weekly.md` | 작업 프롬프트 (claude.ai 프롬프트 v4.1·v1.1·v3.1을 CI용으로 고친 것) |
| `automation/claude-settings.json` | 도구 허용·거부 목록, 자동 업데이트 끄기 |
| `.claude/skills/kb-deep-research/SKILL.md` | 주간 리포트가 쓰는 병렬 조사·종합 절차 |
