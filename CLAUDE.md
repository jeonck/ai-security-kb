# AI Security KB — 작업 사양

이 레포는 AI 보안 뉴스·연구를 자동 수집·요약해 쌓는 지식 베이스이자 Hugo 사이트
(https://jeonck.github.io/ai-security-kb/)다. 두 스케줄 작업이 이 문서를 읽고 따른다.
**이 문서가 형식·규칙의 원본이다.** claude.ai 프로젝트 "리서치"의 `ai-security/` 문서는 이 레포의 사본이다.

| 작업 | 주기 | 하는 일 |
|---|---|---|
| AI 보안 리서치 조교 | 6시간마다 | 4개 도메인 병렬 수집 → 검증·중복 제거 → `content/digest/`, `content/catalog.md` 갱신 → 커밋·푸시 → 프로젝트 사본 갱신 |
| AI 보안 주간 심층 리포트 | 매주 월 07:44 CT | 지난 7일 다이제스트 기반 심층 리서치 → `content/weekly/` → 커밋·푸시 → 프로젝트 사본 갱신 |

## 파일 구조

| 경로 | 역할 |
|---|---|
| `content/catalog.md` | 지금까지 수집한 모든 항목의 표(최신순)와 "후속 추적 목록". **중복 판정 기준** |
| `content/digest/YYYY-MM-DD.md` | 그날 수집한 항목. 같은 날 여러 번 실행되면 같은 파일에 이어 붙인다 |
| `content/weekly/YYYY-Www.md` | 주간 심층 리포트 (ISO 주차) |
| `content/system/` | 시스템 설명·프롬프트·구축 기록 페이지. 사람이 관리하며 **스케줄 작업은 수정하지 않는다** |
| `layouts/`, `static/`, `hugo.toml`, `.github/`, `scripts/` | 사이트 틀. **스케줄 작업은 수정하지 않는다** |

## 날짜

- 날짜는 반드시 명령 출력으로 정한다: `TZ=America/Chicago date +%F`, `TZ=America/Chicago date +%Y-%m-%dT%H:%M:%S%:z`, 주차는 `TZ=America/Chicago date +%G-W%V`.
- 샌드박스 시계는 UTC라 저녁에는 하루 앞서 있다. 파일명·커밋 이력·추론으로 날짜를 정하지 않는다.

## 카테고리 (7개, front matter의 categories에 이 문자열 그대로)

1. `프롬프트 인젝션` — 직접/간접 인젝션, 데이터 유출 체인
2. `에이전트·MCP 보안` — 코딩 에이전트, 도구 호출, MCP 서버/SDK, 인증·권한
3. `모델 공격 연구` — 탈옥, 적대적 예제, 백도어, 모델 추출, 정렬 우회 (주로 arXiv)
4. `AI 공급망` — 악성 모델/패키지, 모델 레지스트리, 직렬화 취약점
5. `개인정보·데이터 유출` — 학습 데이터·대화 로그 노출, AI 기업발 유출, 프라이버시 기법
6. `AI 악용 공격` — 공격자가 AI를 무기로 쓴 사건 (자동화 침투, 딥페이크, 피싱)
7. `규제·표준·거버넌스` — EU AI Act, NIST, CISA, OWASP, 각국 정책, 벤더 보안 정책

## digest 문서 형식

새 파일:

```
---
title: "AI 보안 다이제스트 — YYYY-MM-DD"
date: <TZ=America/Chicago date +%Y-%m-%dT%H:%M:%S%:z 출력>
slug: "YYYY-MM-DD"
description: "<가장 큰 2~3건을 언급한 한 문장> 등 N건"
items: N
categories: [이 문서에 등장한 카테고리들]
tags: [주요 태그 5~8개, 소문자-하이픈]
---

## 이번 수집의 큰 그림

- 항목들을 관통하는 흐름 2~3줄 (직관적으로)

---

### [카테고리] 한 줄 제목
- **날짜**: 원문 발행일 · **유형**: 뉴스 | 연구 | 권고 | 사고 | 표준·정책
- **요약**: 무슨 일인지 2~3문장 (원문을 옮기지 말고 새로 쓴다)
- **동작 원리/핵심**: 공격·발견의 메커니즘을 직관적으로 1~2문장
- **플랫폼 엔지니어 관점**: 내 인프라에서 무엇을 점검/바꿔야 하는지 1~2문장
- **태그**: #cve #mcp ...
- **출처**: [매체/저자](URL)
```

같은 날 이미 파일이 있으면: 맨 끝에 `## 추가 수집 (HH:MM CT)` 섹션을 붙이고 그 아래 항목을 쓴다. front matter의 `items`(누적), `description`, `categories`, `tags`를 갱신하고 `date`는 바꾸지 않는다.

## catalog.md 형식

- 표 헤더 바로 아래에 새 행을 최신순으로 추가: `| 원문 발행일 | 카테고리 | 제목 | [링크](URL) | [YYYY-MM-DD](../digest/YYYY-MM-DD/) |`
- 맨 위 "마지막 실행"(YYYY-MM-DD HH:MM CT)과 "누적 항목" 갱신
- "후속 추적 목록" 정리: 해결된 건 삭제, 새로 생긴 건 추가
- front matter(`layout: "catalog"` 포함)와 표의 열 구성은 바꾸지 않는다. 사이트의 검색·필터·페이징이 이 표를 그대로 읽는다
- 기존 행은 지우지 않는다. 예외: "(원문 미확인)" 항목을 확인했으면 그 행의 제목에서 표시를 지우고 digest 본문도 보완한다
- 맨 아래 `## 주간 리포트` 섹션: 주간 작업이 `- [YYYY-Www](../weekly/YYYY-Www/) — 한 줄 요약`을 맨 위에 추가

## weekly 문서 형식

```
---
title: "AI 보안 주간 심층 리포트 — YYYY-Www"
date: <date 명령 출력>
slug: "YYYY-Www"
description: "<이번 주 핵심 흐름을 한 문장으로>"
categories: [다룬 카테고리들]
tags: [...]
---

## 이번 주 한눈에 보기
(5줄 이내)

## 핵심 흐름 1: ...
(동작 원리, 이번 주 근거, 추가 근거·반론·후속)

...

## 이번 주 점검 항목
(Kubernetes / CI·CD / 에이전트 플랫폼 운영 팀 기준, 구체 행동)

## 다음 주 지켜볼 것

## Sources
```

## 수집 규칙

- 대상 기간: catalog.md의 "마지막 실행" 이후 발행된 자료
- 중복 제거: catalog.md에 같은 URL이 있거나 같은 사건(같은 CVE/같은 제품의 같은 취약점)이 있으면 제외. 패치·CVE 부여·실제 악용 확인 같은 중요한 후속은 제목에 "후속:"을 붙여 새 항목으로
- 1차 출처 우선: 벤더 보안 권고, GHSA/CVE, arXiv, 연구 기관 블로그 > 전문 보안 매체 > 집계 블로그
- 모든 사실·수치·링크는 실제로 읽은 페이지에서 나온 것만 쓴다. 확인이 안 되면 제목에 "(원문 미확인)"을 붙이거나 버린다
- 웹 접근: WebFetch가 거절(429 요청 제한, 차단, 법적 사유)하면 그 페이지를 재시도하거나 curl·스크립트·캐시·미러·아카이브·브라우저 위장 등으로 우회하지 않는다. 다른 공개 출처로 교차 확인한다
- 저작권: 원문 문장을 옮기지 않고 요약한다. 인용은 출처당 1회, 15단어 미만
- 실행당 최대 12개. 새 자료가 없으면 아무 파일도 바꾸지 않고 커밋하지 않는다

## 검증과 커밋

1. `./scripts/check.sh` 실행 — front matter 날짜가 미래가 아닌지, catalog URL 중복이 없는지, `hugo` 빌드가 되는지(hugo가 없으면 빌드 단계는 건너뜀) 확인. **OK가 나와야 커밋한다.** 실패하면 콘텐츠를 고쳐 다시 실행한다. 스크립트를 고쳐서 통과시키지 않는다.
2. 바꾼 콘텐츠 파일만 `git add` 한다 (`content/` 아래).
3. 커밋 메시지: 수집은 `digest: YYYY-MM-DD HH:MM CT — N건 추가`, 주간은 `weekly: YYYY-Www`. 미확인 항목 보완만 있으면 `digest: 원문 확인 보완 (...)`.
4. `main`에 푸시. GitHub Actions가 사이트를 배포한다.

## claude.ai 프로젝트 사본

푸시 후 Projects 도구의 `project_write`로 같은 내용을 올린다(`local_path` 사용):
- `content/digest/YYYY-MM-DD.md` → `ai-security/digest/YYYY-MM-DD.md`
- `content/weekly/YYYY-Www.md` → `ai-security/weekly/YYYY-Www.md`
- `content/catalog.md` → `ai-security/index.md`
- 이 파일 `CLAUDE.md`는 바뀌었을 때만 → `ai-security/README.md`

Projects 도구를 쓸 수 없으면 레포 커밋은 그대로 두고 보고에 "프로젝트 사본 갱신 실패"를 적는다. 레포가 원본이다.
