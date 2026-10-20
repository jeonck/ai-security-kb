# 항목(item) 파일 형식

지식 베이스의 기본 단위는 **항목 하나 = 파일 하나** (`content/items/AISEC-YYYY-NNNN.md`)다.
책을 쓸 때 인용하는 단위도 항목과 그 안의 **주장(claim)** 이다. 다이제스트·전체 목록·집필 매트릭스·참고문헌은 모두 항목 파일에서 자동으로 만들어진다.

검증: `python3 scripts/kb.py validate` (`scripts/check.sh`가 함께 실행한다)

## 전체 예시

```markdown
---
id: "AISEC-2026-0015"
title: "Claude Code Desktop 프리뷰 창 'SneakPeek' — 저장소 HTML 하나로 자격 증명 유출"
summary: "악성 저장소의 HTML을 프리뷰 창이 렌더링하면서 숨긴 스크립트가 SSH 키·클라우드 자격 증명을 외부로 보낸 취약점. 1.30096.1에서 수정."
date: 2026-10-16
date_precision: day
collected: 2026-10-20T07:24:00-05:00
item_type: 취약점
track: news
categories: ["에이전트·MCP 보안"]
lifecycle: ["agent-runtime"]
controls: ["isolation", "identity"]
tags: ["coding-agent", "claude-code", "exfiltration"]
identifiers:
  cve: []
  ghsa: []
  arxiv: []
  doi: []
status: confirmed
sources:
  - key: noma
    role: primary
    tier: 1
    title: "SneakPeek: How the Preview Pane in Claude Code Desktop Can Exfiltrate Your Data"
    outlet: "Noma Security (Noma Labs)"
    authors: []
    published: 2026-10-16
    url: "https://noma.security/noma-labs/sneakpeek-how-the-preview-pane-in-claude-code-desktop-can-exfiltrate-your-data"
    accessed: 2026-10-20
  - key: cybernews
    role: coverage
    tier: 2
    title: "..."
    outlet: "Cybernews"
    authors: ["Mayank Sharma"]
    published: 2026-10-16
    url: "https://cybernews.com/security/claude-code-preview-pane-secret-leak-flaw/"
    accessed: 2026-10-20
claims:
  - text: "256KB를 넘는 HTML은 CSP가 적용되지 않는 다른 렌더링 경로로 처리됐다."
    source: noma
    locator: "'First bypass' 절"
    as_of: 2026-10-16
  - text: "유출 대상은 SSH 개인키, AWS 액세스 키, npm·GitHub 토큰이었다."
    source: cybernews
    locator: "본문 4번째 문단"
related: ["AISEC-2026-0011"]
followup: ""
book_note: "격리 장의 '렌더링도 실행 경로다' 사례. 에이전트 앱의 부가 기능이 공격 표면이 되는 패턴."
---

## 요약
무슨 일이 있었는지 3~5문장. 원문 문장을 옮기지 않고 새로 쓴다.

## 동작 원리
공격·발견의 메커니즘을 직관적으로. 비유가 있으면 좋다.

## 플랫폼 엔지니어 관점
Kubernetes·CI/CD·에이전트 플랫폼을 운영하는 팀이 무엇을 점검·변경해야 하는지.
```

## 필드 규칙

| 필드 | 필수 | 규칙 |
|---|---|---|
| `id` | ● | `AISEC-<연도>-<4자리 일련번호>`. 새 번호는 `python3 scripts/kb.py next-id`. 파일명과 같아야 한다. 한 번 정하면 바꾸지 않는다 |
| `title` | ● | 한국어 한 줄 제목. 원제는 sources의 title에 |
| `summary` | ● | 한두 문장. 카드·목록·인용 미리보기에 쓰인다 |
| `date` | ● | **1차 출처의 발행일** (`YYYY-MM-DD`). 1차가 없으면 가장 이른 신뢰 출처의 발행일 |
| `date_precision` | ● | `day` / `month` (월만 알면 `date`를 그 달 1일로) / `year` |
| `collected` | ● | 수집 시각 (`TZ=America/Chicago date +%Y-%m-%dT%H:%M:%S%:z`) |
| `item_type` | ● | `data/axes.yaml`의 types 중 하나 (Hugo 예약어 `type`과 겹치지 않게 이 이름을 쓴다) |
| `track` | ● | `news`(수집 작업) / `foundation`(기초 문헌 작업) |
| `categories` | ● | axes.yaml의 categories 중 정확히 1개를 담은 리스트 |
| `lifecycle` | ● | axes.yaml lifecycle key 1~2개 (가장 중심이 되는 단계 먼저) |
| `controls` | ● | axes.yaml controls key 1~3개 (이 사례가 **어떤 통제의 실패/필요성**을 보여주는지) |
| `tags` | ● | 소문자-하이픈 3~8개 |
| `identifiers` | ● | cve·ghsa·arxiv·doi 리스트 (없으면 빈 리스트) |
| `status` | ● | `confirmed`(주요 주장을 원문에서 확인) / `partial`(일부만 확인) / `unverified`(원문을 못 엶) |
| `sources` | ● | 1개 이상. 아래 참고 |
| `claims` | ● | 2~8개. 책에 인용할 만한 사실·수치·판단. 아래 참고 |
| `related` | | 관련 항목 ID |
| `followup` | | 후속으로 확인할 것 (없으면 빈 문자열). 전체 목록의 "후속 추적"에 모인다 |
| `book_note` | ● | 이 항목이 책의 어느 논지·장에서 쓰일지 한두 문장 |

### sources

| 필드 | 규칙 |
|---|---|
| `key` | 항목 안에서 고유한 짧은 이름 (claims가 참조) |
| `role` | `primary`(사건·연구의 원 출처) / `coverage`(그것을 보도·해설한 글) |
| `tier` | 1 / 2 / 3 — axes.yaml의 tiers 정의 |
| `title` | **원문 제목 그대로** (번역하지 않는다) |
| `outlet` | 매체·기관·회사 이름 |
| `authors` | 저자 이름 리스트 (모르면 빈 리스트) |
| `published` | 원문 발행일 |
| `url` | 원문 URL |
| `accessed` | 실제로 열어 읽은 날짜. **열지 못했으면 이 필드를 비우지 말고 그 출처를 빼거나 status를 낮춘다** |

- **1차 출처 추적**: 2차 기사가 원 보고서·권고·논문·공식 발표에 링크하면 그 원문을 열어 `primary`로 넣는다. 기사는 `coverage`로 남긴다.
- `status: confirmed` 이려면 `role: primary`, `tier: 1` 출처가 최소 1개 있어야 한다 (validate가 검사). 1차 원문을 찾을 수 없는 사건이면 `partial`.
- 같은 URL이 두 항목에 나오면 validate가 실패한다 (중복 판정 기준).

### claims

- `text`: 한국어로 다시 쓴 주장 한 문장. 원문을 옮기지 않는다. 수치는 원문 그대로 정확히.
- `source`: sources의 key. **그 주장을 실제로 읽은 출처**를 단다.
- `locator`: 원문 안의 위치 (절 제목, 표·그림 번호, "n번째 문단", 논문은 "§3.2"/"Table 2"). 저자가 원문에서 바로 찾을 수 있을 정도로.
- `as_of`: 시간에 따라 바뀌는 수치(피해 규모, 시도 횟수, 다운로드 수 등)면 그 수치의 기준일. 바뀌지 않는 사실이면 생략.
- 인용문은 넣지 않는다. 책에 인용할 때는 저자가 locator로 원문을 찾아 직접 인용한다.

## 웹 접근 규칙

- WebFetch가 거절(429 요청 제한, 차단, 법적 사유)하면 그 페이지를 재시도하거나 curl·스크립트·캐시·미러·아카이브·브라우저 위장 등으로 우회하지 않는다. 다른 공개 출처로 교차 확인하고, 그래도 안 되면 `status`를 낮추고 `followup`에 적는다.
- 모든 사실·수치·링크는 실제로 읽은 페이지에서 나온 것만 쓴다.
