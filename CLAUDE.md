# AI Security KB — 작업 사양

이 레포는 **한국어 책 집필을 위한** AI 보안 지식 베이스이자 Hugo 사이트(https://jeonck.github.io/ai-security-kb/)다.
책의 대상은 AI 서비스·에이전트를 운영하는 플랫폼 엔지니어·SRE·DevSecOps이고, 뼈대는 **생명주기 × 통제 계층** 두 축이다.
스케줄 작업들은 이 문서를 먼저 읽고 따른다. **이 문서가 규칙의 원본이다.** claude.ai 프로젝트 "리서치"의 `ai-security/` 문서는 사본이다.

| 작업 | 주기 | 하는 일 |
|---|---|---|
| AI 보안 리서치 조교 | 6시간마다 | 새 뉴스·연구를 4개 도메인 병렬 수집 → 1차 출처 추적 → 항목 파일 작성 → 다이제스트 → 커밋·푸시 → 프로젝트 사본 |
| AI 보안 기초 문헌 수집 | 매주 화·금 | 집필 매트릭스의 빈 칸·얇은 칸을 채울 기초 문헌(논문·표준·주요 보고서)을 항목으로 추가 |
| AI 보안 주간 심층 리포트 | 매주 월 07:44 CT | 지난 7일 항목을 출발점으로 심층 리서치 → `content/weekly/` (책 관점 절 포함) |

**실행 환경은 두 가지다(2026-10-20부터 GitHub Actions가 운영 중이고 claude.ai 스케줄 작업은 꺼 둠).** (1) claude.ai 스케줄 작업: 에이전트가 레포를 연결해 직접 커밋·푸시하고 프로젝트 사본을 올린다. (2) GitHub Actions(`.github/workflows/kb-*.yml`, 설명은 `automation/README.md`): 레포가 체크아웃된 상태에서 `automation/prompts/<작업>.md`로 실행된다. 이때는 프롬프트 앞에 붙는 `automation/prompts/_ci.md`가 이 문서보다 우선한다. 에이전트는 파일만 고치고, 경로 검사·check.sh·커밋·푸시·배포는 워크플로가 한다. 프로젝트 사본은 건너뛴다.

## 파일 구조

| 경로 | 역할 | 누가 바꾸나 |
|---|---|---|
| `content/items/AISEC-YYYY-NNNN.md` | **항목**: 지식 베이스의 기본 단위. 형식은 `docs/item-format.md` | 스케줄 작업, 저자 |
| `content/digest/YYYY-MM-DD.md` | 그날의 수집 기록: 실행별 "큰 그림" + 항목 목록 (`{{< items ... >}}`) | 스케줄 작업 |
| `content/weekly/YYYY-Www.md` | 주간 심층 리포트 | 주간 작업 |
| `data/state.yaml` | 마지막 수집 시각(`last_run`)과 실행 기록(`runs`) | 수집·기초 문헌 작업 |
| `data/axes.yaml` | 두 축·유형·분류·출처 등급의 정의 | **저자만** |
| `content/book/` | 책 개요·목차(`outline.md`)·목차 설계 근거(`outline-research.md`)·집필 매트릭스 | **저자만** (근거 목록은 자동). 뼈대(두 축 격자)는 저자가 정하고, 목차를 크게 고칠 때는 채팅에서 딥 리서치로 칸을 시험·보강한다 |
| `content/system/` | 시스템 설명·프롬프트·구축 기록 | **저자만** |
| `content/catalog.md`, `content/references.md`, `content/lifecycle/`, `content/controls/` | 자동 생성 페이지의 틀 | **저자만** |
| `layouts/`, `static/`, `hugo.toml`, `.github/`, `scripts/`, `docs/` | 사이트 틀·도구·형식 문서 | **저자만** |
| `automation/`, `.claude/skills/` | GitHub Actions용 프롬프트·도구 권한 설정, 주간 리포트가 쓰는 딥 리서치 스킬 | **저자만** |

스케줄 작업이 바꿔도 되는 것은 `content/items/`, `content/digest/`, `content/weekly/`, `data/state.yaml` 뿐이다.

## 날짜

- 날짜·시각은 반드시 명령 출력으로 정한다: `TZ=America/Chicago date +%F`, `TZ=America/Chicago date '+%F %H:%M'`, `TZ=America/Chicago date +%Y-%m-%dT%H:%M:%S%:z`, 주차 `TZ=America/Chicago date +%G-W%V`.
- 샌드박스 시계는 UTC라 저녁에는 하루 앞서 있다. 파일명·커밋 이력·추론으로 날짜를 정하지 않는다.

## 두 축 (정의는 `data/axes.yaml`)

- **생명주기** (`lifecycle`, 어디서 뚫리나): `data` 데이터 · `training` 학습·튜닝 · `serving` 서빙·추론 · `agent-runtime` 에이전트 런타임 · `supply-chain` 공급망·배포
- **통제 계층** (`controls`, 무엇으로 막나): `identity` 신원·권한 · `network` 네트워크·egress · `isolation` 격리·실행 환경 · `provenance` 공급망·출처 · `detection` 탐지·평가 · `governance` 거버넌스·정책
- 항목마다 생명주기 1~2개(중심 단계 먼저), 통제 1~3개("이 사례가 어떤 통제의 실패 또는 필요성을 보여주는가")를 단다. 거버넌스만 다는 것은 피하고, 정책이 요구하는 구체 통제를 함께 단다.

## 항목 작성 규칙 (상세 형식: `docs/item-format.md`)

- **1차 출처 추적**: 기사가 원 보고서·보안 권고(GHSA/CVE)·논문·공식 발표·관보에 링크하면 그 원문을 열어 `role: primary, tier: 1`로 넣고, 기사는 `coverage`로 남긴다. 같은 사실을 1·2등급이 다루면 3등급(집계 블로그·주간 정리)은 넣지 않는다.
- `status: confirmed`는 1등급 1차 원문을 열어 주요 주장을 확인했을 때만. 아니면 `partial`/`unverified`와 `followup`.
- **주장(claims)** 2~8개: 한국어로 다시 쓴 문장, 정확한 수치, 실제로 읽은 출처 key, 원문 안 위치(locator), 변하는 수치에는 `as_of`. 인용문은 저장하지 않는다.
- 출처 메타데이터: 원제 그대로, 매체, 저자, 발행일, URL, 열람일(`accessed`, 실제로 연 날짜).
- `book_note`: 이 항목이 책의 어느 논지·장에서 쓰일지 한두 문장 (`content/book/outline.md`의 장 번호·제목을 그대로 쓴다).
- **심층 후보(`deep_dive: true` + `deep_dive_reason`)**: 카드 한 장으로는 부족해 원인·후속·반론까지 파야 하는 사건에만 단다. 기준은 실제 악용 확인 / 영향 범위가 큼 / 새 공격 유형 / 책의 장을 바꿀 만함 (상세: `docs/item-format.md`). 한 번의 수집에서 0~2건이 보통이다. 다음 주간 리포트가 딥 리서치로 파고든다.
- YAML 문자열 안에 큰따옴표를 쓰지 않는다(‘ ’ 사용). 깨진 front matter는 validate가 실패로 잡는다.
- 본문: `## 요약` · `## 동작 원리`(직관적으로) · `## 플랫폼 엔지니어 관점`(Kubernetes·CI/CD·에이전트 플랫폼 팀의 구체 행동).
- 새 ID: `python3 scripts/kb.py next-id` (여러 개면 하나씩 늘려 쓴다). ID는 바꾸지 않는다.
- **중복 판정**: 후보의 URL·제목 키워드·CVE/GHSA/arXiv ID로 `python3 scripts/kb.py find <...>` 를 돌린다. 같은 URL이나 같은 사건(같은 CVE/같은 제품의 같은 취약점)이 있으면 새 항목을 만들지 않는다. 패치·CVE 부여·실제 악용 확인 같은 중요한 후속은 제목을 "후속: …"으로 한 새 항목을 만들고 `related`로 원 항목을 잇는다. 원 항목의 `followup`을 정리한다.
- 기존 항목의 "원문 미확인"·`partial`을 이번에 확인했으면 그 항목 파일을 보완하고 `status`를 올린다.

## 다이제스트 형식

```
---
title: "AI 보안 다이제스트 — YYYY-MM-DD"
date: <그날 첫 실행의 date 명령 출력>
slug: "YYYY-MM-DD"
description: "<가장 큰 2~3건을 언급한 한 문장> 등 N건"
items: N
---

## 수집 (HH:MM CT)

- 이번 묶음을 관통하는 흐름 2~3줄 (직관적으로)

{{< items "AISEC-2026-0021" "AISEC-2026-0022" >}}
```

- 같은 날 이미 파일이 있으면 맨 끝에 `## 수집 (HH:MM CT)` 절을 새로 붙이고, front matter의 `items`(누적)와 `description`을 갱신한다. `date`는 바꾸지 않는다.
- 기초 문헌 작업은 절 제목을 `## 기초 문헌 (HH:MM CT)`로 한다.
- 모든 항목은 적어도 한 다이제스트에 실려야 한다 (validate가 검사).

## state.yaml

수집 작업이 새 항목을 추가하면 `last_run`을 이번 실행 시각(`YYYY-MM-DD HH:MM CT`)으로 바꾸고 `runs` 맨 앞에 `{at, task, added}`를 추가한다. 새 항목이 0건이면 바꾸지 않는다. 기초 문헌 작업은 `runs`에만 기록하고 `last_run`은 건드리지 않는다. `runs`는 최근 60개만 남긴다.

## 주간 리포트 형식

```
---
title: "AI 보안 주간 심층 리포트 — YYYY-Www"
date: <date 명령 출력>
slug: "YYYY-Www"
description: "<이번 주 핵심 흐름을 한 문장으로>"
deep_dives: ["AISEC-2026-0014"]   # 이번 리포트에서 심층 분석한 항목 (없으면 빈 리스트)
---

## 이번 주 한눈에 보기          (5줄 이내)
## 심층 분석: <ID> <제목>        (심층 후보마다 1절: 원인, 1차 원문 간 엇갈림 정리, 후속 상황, 반론, 플랫폼 팀 대응. 최대 2건)
## 핵심 흐름 1: ...             (동작 원리, 이번 주 근거 항목 ID, 추가 근거·반론·후속)
...
## 이번 주 점검 항목             (Kubernetes / CI·CD / 에이전트 플랫폼 팀 기준, 구체 행동)
## 책 관점                       (어느 장의 근거가 늘었나, 매트릭스에서 새로 채워진 칸·여전히 빈 칸, 목차 구조 변경 제안 — 제안만, outline.md는 고치지 않는다. 두 축 격자(2부 = 생명주기 5단계 흐름 순서, 3부 = 통제 6칸과 장 1:1)는 유지하는 범위에서 절·논지·사례를 제안한다)
## 다음 주 지켜볼 것
## Sources
```

본문에서 항목을 언급할 때는 ID를 함께 적는다(예: "에이전트 권한 경계 이탈(AISEC-2026-0017)").

**심층 분석 대상 고르기**: `python3 scripts/kb.py deep-dives` 가 아직 어느 주간 리포트에서도 다루지 않은 심층 후보를 최신순으로 보여 준다. 위에서부터 최대 2건을 고르고, 딥 리서치의 리서처 1명씩을 배정한다. 다룬 항목 ID는 front matter `deep_dives`에 적는다(그래야 다음 주에 다시 고르지 않고, 항목 페이지에 링크가 생긴다). 남은 후보는 다음 주로 넘어간다.

**급한 심층 분석**: 저자가 채팅에서 특정 항목의 심층 분석을 요청하면, 주간 리포트를 기다리지 않고 같은 방식으로 조사해 `content/weekly/YYYY-Www-<ID>.md`(제목 "AI 보안 심층 분석 — <ID> …", `deep_dives: [<ID>]`)로 저장할 수 있다.

## 기초 문헌 트랙

- `track: foundation`, `item_type: 기초 문헌`. 발행일 제한이 없다 (오래된 고전 논문·표준도 대상).
- 대상: 동료 심사 논문·arXiv 원 논문, 표준·프레임워크 문서(OWASP, NIST AI RMF·AI 100-2, MITRE ATLAS, CSA 등), 정부·주요 기관 보고서. 1등급 원문만. 블로그 요약은 대상이 아니다.
- 고르는 기준: 먼저 `content/book/outline.md`의 "기초 문헌 수집 우선순위" 표를 위에서부터 본다(이미 항목이 있으면 `kb.py find`로 확인하고 건너뛴다). 그다음 `python3 scripts/kb.py coverage` 의 빈 칸·1건뿐인 칸, outline.md에서 "근거 부족"이 뜨는 장. 실행당 3~5건.
- 논문은 identifiers.arxiv/doi와 저자 전원, locator는 절·표·그림 번호로.

## 수집 공통 규칙

- 대상 기간(뉴스 트랙): `data/state.yaml`의 `last_run` 이후 발행된 자료.
- 1차 출처 우선: 벤더 보안 권고, GHSA/CVE, arXiv, 연구 기관 블로그, 공식 발표 > 전문 보안 매체 > 집계 블로그.
- 모든 사실·수치·링크는 실제로 읽은 페이지에서 나온 것만 쓴다.
- **웹 접근**: WebFetch가 거절(429 요청 제한, 차단, 법적 사유)하면 그 페이지를 재시도하거나 curl·스크립트·캐시·미러·아카이브·브라우저 위장 등으로 우회하지 않는다. 다른 공개 출처로 교차 확인하고, 안 되면 `status`를 낮추고 `followup`에 적는다. (arXiv는 `arxiv.org/abs/<id>`가 막혀도 `arxiv.org/html/<id>v1` 본문이 열리는 경우가 있다 — 같은 사이트의 정식 페이지라 우회가 아니다. 거기서도 거절되면 멈춘다.)
- 저작권: 원문 문장을 옮기지 않고 요약한다.
- 실행당 최대 12개(뉴스), 3~5개(기초 문헌). 새 자료가 없으면 아무 파일도 바꾸지 않고 커밋하지 않는다.

## 검증과 커밋

1. `./scripts/check.sh` — `kb.py validate`(스키마·두 축 어휘·출처 메타데이터·1차 출처 조건·URL 중복·다이제스트 참조·미래 날짜) + Hugo 빌드. **마지막 줄이 OK여야 커밋한다.** 실패하면 콘텐츠를 고친다. 스크립트·설정을 고쳐서 통과시키지 않는다.
2. 바꾼 파일만 `git add` (`content/items/`, `content/digest/`, `content/weekly/`, `data/state.yaml`).
3. 커밋 메시지: 수집 `digest: YYYY-MM-DD HH:MM CT — N건 추가`, 기초 문헌 `foundation: YYYY-MM-DD — N건 추가`, 주간 `weekly: YYYY-Www`, 보완만 있으면 `items: 원문 확인 보완 (ID, ...)`.
4. `main`에 푸시 (거절되면 `git pull --rebase` 후 check.sh 재실행·재푸시). GitHub Actions가 배포하면서 참고문헌 BibTeX·CSL-JSON도 새로 만든다.

## claude.ai 프로젝트 사본

푸시 후 Projects 도구 `project_write`(`local_path` 사용)로 올린다. 사본 파일은 레포 밖(`$HOME/kb-export/`)에 만든다.

- `python3 scripts/kb.py export-day YYYY-MM-DD > $HOME/kb-export/digest-YYYY-MM-DD.md` → `ai-security/digest/YYYY-MM-DD.md` (그날 다이제스트 + 항목 전문 + 주장·출처)
- `python3 scripts/kb.py export-index > $HOME/kb-export/index.md` → `ai-security/index.md`
- 주간 리포트 `content/weekly/YYYY-Www.md` → `ai-security/weekly/YYYY-Www.md`
- 이 파일이 바뀌었을 때만 `CLAUDE.md` → `ai-security/README.md`

Projects 도구를 쓸 수 없으면 레포 커밋은 그대로 두고 보고에 "프로젝트 사본 갱신 실패"를 적는다. 레포가 원본이다.
