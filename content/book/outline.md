---
title: "목차 v1.1"
description: "생명주기 5단계 × 통제 계층 6칸의 격자를 그대로 장 구조로 쓰고, 딥 리서치 결과로 각 칸의 사례·절·성숙도를 채운 목차. 4부 16장 + 부록"
weight: 20
updated: "2026-10-20"
---

**가제**: 『에이전트 시대의 AI 보안 — 플랫폼 엔지니어를 위한 통제 설계』

## 이 목차를 짠 방식

**뼈대는 두 축의 격자다.** 2부는 생명주기 다섯 단계를 흐름 순서대로 한 장씩, 3부는 통제 계층 여섯 칸을 한 장씩 맡는다. 장의 구조와 순서는 이 격자가 정한다.

**딥 리서치는 격자를 바꾸는 데가 아니라 시험하고 채우는 데 썼다.** 다섯 갈래 조사(기존 책·강의, 표준·프레임워크 크로스워크, 통제 기술 성숙도, 생명주기별 사고, 독자 수요·한국 규제)로 각 칸에 대해 다음을 확인했다. 조사 전문은 [설계 근거 리포트](../outline-research/)에 있다.

| 확인한 것 | 결과가 목차에 들어간 곳 |
|---|---|
| 어느 칸이 비어 있나 | 표준을 격자에 겹치면 네트워크·egress 열이 모든 단계에서 비고, 격리·신원은 에이전트 밖(학습 잡, 모델 로딩, CI/CD 자격 증명)이 빈다 → 9~11장의 범위를 에이전트 밖까지 넓혔다 |
| 각 칸을 실사고로 쓸 수 있나 | 서빙·공급망은 실사고로, 데이터 오염·학습은 주로 연구로 논증한다 → 여는 사례마다 [실사고]/[공개 취약점]/[연구]를 밝혔다 |
| 각 통제를 지금 가르칠 수 있나 | 절마다 **성숙**(CNCF Graduated·RFC·MUST·stable API) / **부상**(1.0 전후·초안) / **실험**(연구) 라벨을 붙였다. 빠르게 바뀌는 스펙(MCP 개정, IETF 초안)은 온라인 부록으로 보낸다 |
| 독자가 실제로 막히는 곳 | 과잉 권한·가시성·책임자 부재 → 9장(신원)과 14장(거버넌스)의 절 구성에 반영했다. 장 순서는 바꾸지 않고 2부 첫머리에 읽기 안내를 뒀다 |
| 다른 책이 비워 둔 곳 | 통제 계층으로 장을 나눈 책, 에이전트 사고 대응 장을 둔 책이 없다 → 격자를 뼈대로 쓰는 판단을 뒷받침한다. OWASP 항목별 해설은 이미 많으므로 뼈대가 아니라 교차 참조 부록으로 둔다 |

**축 밖의 주제는 그 주제가 속한 칸의 절로 둔다.** AI 게이트웨이는 10장(네트워크)의 절로, 소유권·리스크 등록부·표준 번역·한국 규제는 14장(거버넌스)의 절로 넣었다.

장 틀: **리더용 요약 1쪽 → 사례 → 동작 원리 → 통제 설계 → 점검 목록**. 점검 목록에는 OWASP(LLMxx·ASIxx)와 MITRE ATLAS 기술 ID를 함께 단다.

장 제목·논지·순서는 저자가 고친다. 각 장 아래 "근거 항목"은 지식 베이스에서 자동으로 모이고, 3건 미만이면 "근거 부족"으로 표시된다. 스케줄 작업은 이 문서를 고치지 않는다.

---

## 1부. 왜 AI 보안은 인프라 문제인가

### 1장. 프롬프트 인젝션은 고칠 버그가 아니라 상시 위험이다 — 그래서 폭발 반경을 설계한다

- **논지**: 명령과 데이터가 한 채널을 쓰는 한 인젝션은 사라지지 않는다. 그러니 물어야 할 것은 "조작된 에이전트가 무엇에 닿고, 무엇을 들고 나갈 수 있나"다. 장은 한국 독자의 첫 우려인 데이터 유출 경로로 열고, 인젝션은 '왜 막을 수 없나'의 원인으로 설명한다.
- **핵심 질문**: 에이전트가 닿는 내부 API·SaaS·클라우드·CI/CD 가운데 무엇이 유출 경로가 되나? 공격 성공률이 낮다는 평가는 무엇을 숨기나? 프롬프트 안의 방어는 왜 통제가 아닌가?
- **여는 사례**: ① Slack AI 간접 인젝션(2024-08-14~19). 공개 채널에 심은 지시가 비공개 채널의 API 키를 피싱 링크에 실어 내보냈다. Slack은 "의도된 동작"이라고 답했다 [공개 취약점] ([PromptArmor](https://www.promptarmor.com/resources/data-exfiltration-from-slack-ai-via-indirect-prompt-injection)) ② GitHub MCP 'toxic agent flow'(2025-05-26). 공개 저장소의 이슈 하나가 비공개 저장소 데이터를 공개 PR로 빼냈고, 연구자들은 서버 코드가 아니라 아키텍처의 결함이라고 결론지었다 [공개 취약점] ([Invariant Labs](https://invariantlabs.ai/blog/mcp-github-vulnerability)) ③ EchoLeak CVE-2025-32711(NVD 2025-06-11, M365 Copilot) [공개 취약점] ([NVD](https://nvd.nist.gov/vuln/detail/CVE-2025-32711))
- **리더 요약 수치 후보**: 에이전트가 닿는 곳은 내부 앱·API 56%, SaaS 49%, 클라우드 인프라 44%, CI/CD 35%다. 81%가 프롬프트 조작으로 자격 증명이 노출될 수 있다고 본다([Help Net Security](https://helpnetsecurity.com/2026/03/26/ciso-ai-agent-identity-security-report/)).
- **절 구성**: ① 에이전트가 닿는 곳: 유출의 세 경로(검색 범위, 도구 권한, 밖으로 나가는 출력) ② 왜 막을 수 없나: 명령·데이터 단일 채널과 직접·간접 인젝션(AI 100-2 §3.3–3.4, LLM01, ASI01) ③ 공격 성공률이 숨기는 것: '거부'와 '무시'의 차이, 적응형 공격(13장 예고) ④ 폭발 반경 = 신원 × egress × 격리: 3부 지도 ⑤ 상시 위험으로 등록하기: 패치가 아니라 범위·가격으로 관리한다(14장 예고)
- **근거 수준**: 충분 · **외부 근거**: [NIST AI 100-2 E2025](https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-2e2025.pdf), [OWASP LLM Top 10](https://genai.owasp.org/llm-top-10/), [arXiv 2510.09023](https://arxiv.org/abs/2510.09023)

{{< evidence ids="AISEC-2026-0005 AISEC-2026-0020 AISEC-2026-0004 AISEC-2026-0002 AISEC-2026-0010" >}}

### 2장. 공격자도 에이전트를 쓴다 — 위협 환경

- **논지**: 성공률이 10%여도 시도 비용이 0에 가까우면 공격은 규모의 게임이 된다. 공격자에게는 모델 API도 인프라다. 그래서 패치 주기와 노출 관리의 전제가 바뀌고, 모델 API로 나가는 egress도 탐지 신호가 된다.
- **핵심 질문**: 자율 침투 도구는 공격의 경제학을 어떻게 바꿨나? 위협 행위자의 모델 사용은 방어 쪽 로그 어디에 흔적을 남기나? 벤더 위협 보고서는 단일 출처라는 한계가 있다. 이 한계를 어떻게 다뤄야 하나?
- **여는 사례**: ① ARTEX. 한국 금융권 공격(9월 말~10월 초)에 이어 일본 기업 공격에서도 확인됐다 [실사고] (AISEC-2026-0001) ② Anthropic이 2025-11-13에 공개한 AI 주도 첩보 캠페인. 약 30개 표적, 전술 작업의 80~90%를 AI가 수행했다 [실사고] ([Anthropic](https://www.anthropic.com/news/disrupting-AI-espionage)) ③ Google GTIG의 PROMPTSTEAL(2025-11-05). 실제 작전에서 LLM에 질의한 첫 악성코드로, Hugging Face API로 명령을 생성했다 [실사고] ([Google GTIG](https://cloud.google.com/blog/topics/threat-intelligence/threat-actor-usage-of-ai-tools))
- **절 구성**: ① 공격 경제학: 성공률보다 시도 비용(AISEC-2026-0013의 과업당 비용·소요 시간) ② 위협 행위자의 모델 사용: 갈취(2025-08), 첩보(2025-11), 모델을 C2처럼 쓰는 악성코드 ③ 노출된 에이전트 제어판: 공격 인프라 자체의 운영 실패 ④ 방어 쪽 함의: 노출 관리 주기, 모델 API로 나가는 egress 신호(10·13장 예고) ⑤ 근거 읽는 법: 벤더 위협 보고서는 자사 모델의 오남용만 보는 단일 출처다
- **근거 수준**: 충분 (단, 대부분 벤더 단일 출처) · **외부 근거**: [Anthropic 2025-08](https://www.anthropic.com/news/detecting-countering-misuse-aug-2025), [Anthropic 2025-11](https://www.anthropic.com/news/disrupting-AI-espionage), [Google GTIG](https://cloud.google.com/blog/topics/threat-intelligence/threat-actor-usage-of-ai-tools)

{{< evidence ids="AISEC-2026-0001 AISEC-2026-0013" >}}

### 3장. 두 축을 플랫폼 위에 그린다 — 참조 아키텍처와 신뢰 경계

- **논지**: 이 책의 두 축(어디서 뚫리나 × 무엇으로 막나)을 쿠버네티스 위 AI 플랫폼에 그린다. 플랫폼은 모델 서빙, AI 게이트웨이, MCP 서버, 벡터 DB, 학습·평가 클러스터, CI/CD·레지스트리로 이뤄지고, 신뢰 경계는 이 구성 요소들 사이에 있다. 2부의 다섯 단계는 이 지도의 어느 구역인지, 3부의 여섯 통제는 어느 경계에 서는지로 설명된다. 독자는 같은 지도 위에 실습 환경을 띄우고, 장마다 통제를 하나씩 더한다.
- **핵심 질문**: 5단계 × 6통제 격자의 각 칸은 내 플랫폼의 어느 구성 요소에 해당하나? 신뢰할 수 없는 입력은 어디로 들어와 어떤 자격 증명 옆을 지나가나? 표준들(NIST 2분법, AI Exchange 3분법, MAESTRO 7계층)은 이 격자와 어떻게 대응하나?
- **여는 사례**: ① Hugging Face 공유 인프라(2024-04-04, Wiz). 악성 pickle 모델로 추론 서비스에서 RCE를 얻었다. 이어서 IMDS를 통해 노드 역할, EKS 시크릿을 차례로 얻었다. Spaces Dockerfile의 `RUN`으로는 공유 내부 레지스트리에 푸시해 다른 테넌트의 이미지를 덮어쓸 수 있었다. 신뢰 경계 다섯 개를 연달아 넘은 사례다 [공개 취약점] ([Wiz](https://www.wiz.io/blog/wiz-and-hugging-face-address-risks-to-ai-infrastructure))
- **절 구성**: ① 두 축 격자: 5단계 × 6통제와 이 책을 읽는 법 ② 참조 아키텍처: 구성 요소와 데이터·제어 흐름 ③ 신뢰 경계 그리기: 입력·자격 증명·외부 호출의 교차점 ④ 표준 대응표: AI 100-2(학습/배포 시점), AI Exchange(개발/입력/런타임), MAESTRO L1~L7 ↔ 책의 5단계·6통제 ⑤ 실습 환경: kind/minikube 위 작은 에이전트 플랫폼(모델 프록시, MCP 서버 1개, 벡터 DB, CI) — **성숙** ⑥ 이 책의 표기 규칙: 근거 유형, 성숙도 라벨, OWASP·ATLAS ID
- **근거 수준**: 보통 (KB 직접 항목 없음. 표준·사례는 충분) · **외부 근거**: [CSA MAESTRO](https://cloudsecurityalliance.org/blog/2025/02/06/agentic-ai-threat-modeling-framework-maestro), [OWASP AI Exchange](https://owaspai.org/), [NIST AI 100-2 E2025](https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-2e2025.pdf), [SAIF Focus on Agents](https://saif.google/focus-on-agents)

{{< evidence ids="AISEC-2026-0004 AISEC-2026-0010" >}}

## 2부. 생명주기로 보는 공격 표면

2부는 데이터 → 학습 → 서빙 → 에이전트 런타임 → 공급망·배포의 흐름 순서를 따른다. 파이프라인을 떠올리는 순서 그대로이고, NIST AI 100-2의 '학습 시점 / 배포 시점' 구분을 세분한 것이기도 하다. 앞 장에서 정의한 개념(예: 데이터 장의 오염)을 뒤 장(런타임 장의 RAG 오염)이 이어받는다. 각 장은 '공격 표면 지도'다. 사례와 동작 원리를 깊게 쓰고, 통제 설계는 3부의 해당 장으로 넘긴다.

> **읽기 안내**: 모델을 직접 학습하지 않는 팀이 많다(CNCF 설문 응답자의 52%, 관리형 API 사용 37%). 그런 팀은 6장(서빙)·7장(런타임)부터 읽고 4·5장으로 돌아와도 된다. 다만 4·5장 리더 요약의 '학습을 안 해도 해당되는 이유'는 먼저 읽기를 권한다.

### 4장. 데이터 — 노출은 사고로, 오염은 연구로

- **논지**: 데이터 단계의 실제 사고는 대부분 '노출'이다. 범위가 넓은 공유 토큰, 무인증 저장소, 옛 유출을 한곳에 모은 집적지가 그 예다. '오염'은 싸고 모델 크기와 무관하다는 연구가 쌓였다. 추론 로그와 채팅 기록 저장소도 이 단계의 데이터 레이크다.
- **핵심 질문**: 코퍼스가 클수록 오염이 희석되나? 그렇지 않다면 무엇을 출처 단위로 관리해야 하나? 사내 데이터가 외부 모델로 새는 경로(섀도 AI)는 어디서 보이나?
- **학습을 안 해도 해당되는 이유**: RAG 문서 저장소, 벡터 DB, 대화 로그 수집 파이프라인도 데이터 단계다. 이 단계의 실사고는 대부분 오염이 아니라 노출(Microsoft 38TB SAS 토큰, DeepSeek ClickHouse 로그 DB)이었다.
- **여는 사례**: ① Microsoft AI 연구팀 38TB 노출(2023-09-18 공개). 저장소 계정 전체에 '전체 제어' 권한을 준 SAS 토큰이었고, 만료일은 2051년으로 늘어나 있었다. 쓰기 권한까지 있어 모델 파일을 덮어쓸 수도 있었다 [실사고] ([Wiz](https://www.wiz.io/blog/38-terabytes-of-private-data-accidentally-exposed-by-microsoft-ai-researchers)) ② DeepSeek ClickHouse 무인증 노출(2025-01-29). 채팅 기록과 API 키가 담긴 로그가 100만 줄 이상이었다 [실사고] ([Wiz](https://www.wiz.io/blog/wiz-research-uncovers-exposed-deepseek-database-leak)) ③ 문서 약 250개로 600M~13B 모델에 백도어를 심은 연구(2025-10-09) [연구] ([Anthropic](https://www.anthropic.com/research/small-samples-poison))
- **절 구성**: ① 표준 상자: AI 100-2 §3.2, LLM04·LLM08, SAIF Training Data Management, MAESTRO L2 ② 데이터 노출: 학습 데이터·로그·채팅 기록 저장소, 공유 토큰 ③ 데이터 오염: 웹 규모 코퍼스(Carlini 2023), RAG(PoisonedRAG), 고정 개수 백도어, 실제 세계의 다리(Pravda 'LLM grooming') ④ 수집 단계 위생: 코퍼스 속 시크릿(Common Crawl에서 살아 있는 키 11,908개), URL 데이터셋 해시 검증 — **성숙** ⑤ 섀도 AI: 사내 데이터가 외부 모델로 새는 경로와 탐지(10장 egress와 연결) ⑥ 통제 지도: → 12장(데이터 계보), 9장(검색 권한), 10장
- **근거 수준**: 보통 (운영 중인 RAG 코퍼스가 실제로 오염된 1차 보고는 찾지 못했다) · **외부 근거**: [arXiv 2302.10149](https://arxiv.org/abs/2302.10149), [arXiv 2402.07867](https://arxiv.org/abs/2402.07867), [Truffle Security](https://trufflesecurity.com/blog/research-finds-12-000-live-api-keys-and-passwords-in-deepseek-s-training-data), [NewsGuard](https://www.newsguardrealitycheck.com/p/a-well-funded-moscow-based-global), [TechRepublic (IBM 섀도 AI)](https://www.techrepublic.com/article/news-ai-breach-risks-rise-as-governance-lags/)

{{< evidence ids="AISEC-2026-0008" >}}

### 5장. 학습·평가 인프라 — GPU 클러스터와 '훈련 중인 모델'이라는 공격자

- **논지**: 학습 클러스터가 고가치 표적인 이유는 모델이 아니라 그 안에 있는 자격 증명과 GPU다. 또 하나의 위협 모델이 있다. 평가·RL 환경에서는 훈련 중인 모델이 실제 권한을 가진 행위자다. 채점기가 잡지 못한 행동은 몇 달 뒤에야 드러난다. 두 갈래는 통제가 다르다. 학습 인프라는 네트워크·신원, 평가 환경은 격리·탐지다.
- **핵심 질문**: "취약점이 아니라 설계"라는 입장(disputed CVE)은 위험을 어떻게 몇 년씩 남겨 두나? 평가 샌드박스를 CTF 수준으로 격리해야 하는 이유는 무엇인가? 사후 평가로 백도어가 없음을 증명할 수 있나?
- **학습을 안 해도 해당되는 이유**: ShadowRay가 노린 Ray 클러스터는 학습뿐 아니라 배치 추론·서빙에도 쓰인다. 에이전트를 평가하는 하네스와 API 기반 파인튜닝도 이 단계에 든다. 평가 중인 모델이 잘못 노출된 Docker API를 찾아 쓴 사례(o1-preview)가 그 예다.
- **여는 사례**: ① ShadowRay(CVE-2023-48022). 2023-09-05부터 악용됐고 Oligo가 2024-03-26에 공개했다. 인가 없는 Jobs API로 채굴기를 깔고 OpenAI·HF·클라우드 키와 쿠버네티스 API 접근을 빼앗았다. 2025-11에는 자기 전파형 2.0이 나왔다 [실사고] ([Oligo](https://www.oligo.security/blog/shadowray-attack-ai-workloads-actively-exploited-in-the-wild), [NVD](https://nvd.nist.gov/vuln/detail/CVE-2023-48022)) ② o1-preview(시스템 카드 2024-09-17 §4.2.1). 고장 난 CTF에서 nmap으로 잘못 노출된 Docker API를 찾아 플래그를 읽었다 [실사고, 연구소 내부] ([OpenAI](https://cdn.openai.com/o1-preview-system-card-20240917.pdf)) ③ 실제 Claude RL 환경의 보상 해킹이 오정렬로 일반화된 사례(2025-11-21). Claude Code 평가에서 안전 연구 코드를 12% 비율로 방해했다 [연구] ([Anthropic](https://www.anthropic.com/research/emergent-misalignment-reward-hacking))
- **절 구성**: ① 표준 상자: AI 100-2(학습 시점), SSDF-A(SP 800-218A), SAIF Model Source Tampering ② 학습 인프라 보안: Ray 대시보드·Jobs API 노출, 인증 계층(Ray 2.52.0 토큰 인증) — **성숙** ③ GPU 노드 탈출과 공유: NVIDIA Container Toolkit CVE-2024-0132(≤1.16.1) — **성숙**(패치·CDI 모드) ④ 평가·RL 환경 격리: 훈련 중인 모델을 잠재적 공격자로 보기, 채점기 분리 — **부상** ⑤ 내부자·체크포인트 무결성과 백도어 지속성: ByteDance(부분 미확인), Sleeper Agents — **성숙**(서명) / **실험**(탐지) ⑥ 통제 지도: → 10장(학습 잡 egress), 11장(평가 하네스 격리), 9장(학습 잡 ID)
- **근거 수준**: 보통 (실사고 한 계열 + 연구소 내부 사건. 외부 공격자가 파인튜닝 파이프라인을 오염시킨 1차 보고는 없다) · **외부 근거**: [THN ShadowRay 2.0](https://thehackernews.com/2025/11/shadowray-20-exploits-unpatched-ray.html), [Dark Reading](https://www.darkreading.com/cyber-risk/shadowray-20-ai-clusters-crypto-botnets), [Wiz CVE-2024-0132](https://www.wiz.io/blog/wiz-research-critical-nvidia-ai-vulnerability), [arXiv 2401.05566](https://arxiv.org/abs/2401.05566), [The Register (ByteDance)](https://www.theregister.com/2024/10/22/bytedance_intern_messed_with_llm/)

{{< evidence ids="AISEC-2026-0017" >}}

### 6장. 서빙·추론 — 모델 엔드포인트는 과금되는 공개 서비스다

- **논지**: 유출된 API 키는 곧 비용 책임이고 오남용 통로다. 자체 호스팅 추론 서버는 '기본값 무인증 + 네트워크 노출'이라는 같은 패턴으로 반복해서 뚫린다. 추론 최적화 옵션도 보안 변수다.
- **핵심 질문**: 모델 API 키 하나가 새면 하루에 얼마가 나가나? 탈옥·오남용과 키 도용·증류·추출은 통제가 어떻게 다른가? 자체 호스팅 Ollama·vLLM 앞에 무엇을 세워야 하나?
- **여는 사례**: ① LLMjacking(2024-05-06, Sysdig). 도용한 클라우드 자격 증명으로 Bedrock의 Claude를 호출했다. 공격자는 호출 로깅 설정이 켜져 있는지부터 확인했다. 최악의 경우 하루 4.6만 달러 이상이 든다 [실사고] ([Sysdig](https://sysdig.com/blog/llmjacking-stolen-cloud-credentials-used-in-new-ai-attack/)) ② Anthropic 증류 캠페인(2026-02-23). 약 24,000개 계정으로 1,600만 건 이상을 교환했다 [실사고] ([Anthropic](https://www.anthropic.com/news/detecting-and-preventing-distillation-attacks)) ③ 무인증 Ollama의 대량 노출(Cisco 2025-09-01: 1,139대 중 214대가 인증 없이 서빙)과 vLLM CVE-2026-22778(CVSS 9.8, 기본 설치에 인증 없음) [공개 취약점] ([Cisco](https://blogs.cisco.com/security/detecting-exposed-llm-servers-shodan-case-study-on-ollama), [GitLab advisory](https://advisories.gitlab.com/pypi/vllm/CVE-2026-22778/))
- **절 구성**: ① 표준 상자: LLM10·SAIF Model Exfiltration·ATLAS Cost Harvesting ② 오남용: 탈옥·위협 행위자 사용, 가드레일 우회(Storm-2139) ③ 자원·자산 탈취: 키 도용, 증류(대량 질의)와 파라미터 추출(Carlini 2024)의 구분 ④ 자체 호스팅 서빙 하드닝: 인터넷 비노출, 앞단 인증 프록시, 최소 API 표면, 빠른 패치(Ollama·vLLM CVE) — **성숙** ⑤ 추론 최적화·출력 처리도 보안 변수: 조기 종료와 탈옥 내성, 규제 요건이 서빙 출력 단계로 내려오는 경우(워터마크) — **부상** ⑥ 통제 지도: → 9장(키·계정), 10장(게이트웨이·쿼터), 13장(호출 로깅)
- **근거 수준**: 충분 · **외부 근거**: [Microsoft Storm-2139](https://blogs.microsoft.com/on-the-issues/2025/02/27/disrupting-cybercrime-abusing-gen-ai/), [arXiv 2403.06634](https://arxiv.org/abs/2403.06634), [Wiz Probllama](https://www.wiz.io/blog/probllama-ollama-vulnerability-cve-2024-37032), [CNCF KServe](https://www.cncf.io/projects/kserve/)

{{< evidence ids="AISEC-2026-0016 AISEC-2026-0006 AISEC-2026-0009 AISEC-2026-0005 AISEC-2026-0007" >}}

### 7장. 에이전트 런타임 — 신뢰할 수 없는 입력, 과도한 권한, 밖으로 나가는 통로

- **논지**: 에이전트 사고의 공통 원인은 세 가지가 한자리에 있는 것이다. 신뢰할 수 없는 콘텐츠가 들어오고, 범위가 넓은 자격 증명을 쥐고 있고, 밖으로 나가는 채널이 있다. 미리보기·설정 필드 같은 부가 기능도 실행 경로다. KB 근거가 가장 두꺼운 장이므로 사례를 늘리기보다 이 패턴으로 묶는다.
- **핵심 질문**: MCP 서버 등록과 stdio 설정은 왜 임의 명령 실행 권한과 같은가? 벤더가 "취약점 아님"이라고 판정하면 그 위험은 누가 지나? 입구가 아니라 싱크에서 검증한다는 말은 무슨 뜻인가?
- **여는 사례**: ① Replit 에이전트의 운영 DB 삭제(2025-07-22 보도). 코드 동결 지시가 있던 중 임원 1,206명과 1,196개 이상 회사의 기록을 지웠다. 이후 개발·운영 DB 분리와 계획 전용 모드가 추가됐다 [실사고] ([eWeek](https://www.eweek.com/news/replit-ai-coding-assistant-failure/)) ② Supabase MCP(2025-07-08). RLS를 우회하는 `service_role`로 돌던 Cursor가 지원 티켓 속 지시를 읽고 토큰을 덤프했다 [연구, 실제 제품 대상 시연] ([General Analysis](https://generalanalysis.com/blog/supabase-mcp-blog)) ③ Langflow MCP stdio 설정 필드 RCE. 실제로 악용 중이다 [실사고] (AISEC-2026-0014)
- **절 구성**: ① 표준 상자: ASI01~10, SAIF 에이전트 구성요소(인지·추론·오케스트레이션·응답 렌더링) ② 공통 패턴: 입력 × 권한 × 출구 ③ MCP와 도구 호출: 등록=권한 부여, stdio=명령 실행, 서버가 알려 주는 인증 위치 ④ 코딩·CI 에이전트: 비밀 값과 도구를 쥐고 PR 제목·이슈를 읽는 구조 ⑤ 부가 기능이 실행 경로가 될 때: 미리보기·렌더링 ⑥ 통제 지도: → 9장(최소 권한), 10장(egress), 11장(격리·비상 정지), 13장(행동 순서 탐지)
- **근거 수준**: 충분 · **외부 근거**: [Invariant Labs](https://invariantlabs.ai/blog/mcp-github-vulnerability), [NVD CVE-2025-32711](https://nvd.nist.gov/vuln/detail/CVE-2025-32711), [OWASP Agentic Top 10 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/), [Databricks DASF v3.0](https://www.databricks.com/blog/agentic-ai-security-new-risks-and-controls-databricks-ai-security-framework-dasf-v30)

{{< evidence ids="AISEC-2026-0002 AISEC-2026-0003 AISEC-2026-0011 AISEC-2026-0013 AISEC-2026-0014 AISEC-2026-0015 AISEC-2026-0017 AISEC-2026-0018 AISEC-2026-0020" >}}

### 8장. 공급망·배포 — 모델·패키지·MCP 서버는 코드이고, 연동은 토큰이다

- **논지**: 모델은 가중치 파일이 아니라 '로더와 README가 딸린 패키지'다. AI 라이브러리는 평범한 패키지처럼 CI 설정 결함으로 뚫린다. 서드파티 AI·SaaS 연동은 OAuth 토큰 공급망이다. 앞의 두 갈래(아티팩트)에서 실패하는 통제는 출처·격리이고, 뒤의 갈래(연동)에서 실패하는 통제는 신원(토큰 범위·수명)이다.
- **핵심 질문**: 다운로드 수와 트렌딩 순위는 신뢰 신호가 될 수 있나? 개발자 PC의 AI CLI는 왜 공격자의 정찰 엔진이 되나? 조달 배제 명령 하나에 어떤 목록이 필요해지나?
- **여는 사례**: ① Nx 's1ngularity'(2025-08-26). `pull_request_target` 워크플로 결함으로 npm 토큰을 빼앗긴 뒤 악성 버전이 배포됐다. 악성 버전은 피해자 PC의 Claude·Gemini·Amazon Q CLI를 권한 확인 우회 플래그로 실행해 정찰에 썼다. 결과는 GitHub 토큰 1,000개 이상, 공개로 바뀐 저장소 5,500개 이상이다 [실사고] ([GHSA](https://github.com/nrwl/nx/security/advisories/GHSA-cxm3-wv7p-598c), [Wiz](https://www.wiz.io/blog/s1ngularity-supply-chain-attack)) ② Hugging Face 악성 모델. JFrog가 2024-02-27에 약 100개를 보고했고, nullifAI는 망가진 pickle로 스캐너를 우회했다. KB에는 24만 회 다운로드된 사례도 있다 [실사고] ([JFrog](https://jfrog.com/blog/data-scientists-targeted-by-malicious-hugging-face-ml-models-with-silent-backdoor/), [ReversingLabs](https://www.reversinglabs.com/blog/rl-identifies-malware-ml-model-hosted-on-hugging-face)) ③ Salesloft Drift OAuth 토큰 탈취(2025-08-08~18). 탈취한 토큰으로 Salesforce 데이터를 대량으로 내보낸 뒤 AWS 키를 찾았다 [실사고] ([Google GTIG](https://cloud.google.com/blog/topics/threat-intelligence/data-theft-salesforce-instances-via-salesloft-drift))
- **절 구성**: ① 표준 상자: LLM03·ASI04·SAIF·ATLAS의 rug pull·reputation inflation ② 아티팩트 공급망 A: 모델 허브와 직렬화(pickle, 스캐너 우회) ③ 아티팩트 공급망 B: AI 패키지·확장·MCP 서버(Ultralytics, Amazon Q, postmark-mcp, LiteLLM) ④ 서드파티 AI·SaaS 연동 공급망: Drift, Mixpanel→OpenAI, HF Spaces 시크릿, 서드파티 도구에 맡긴 공급자 키 ⑤ 슬롭스쿼팅: 연구로만 측정된 위험 ⑥ 통제 지도: → 12장(서명·AI-BOM·로더), 9장(연동 토큰), 11장(로딩 격리)
- **근거 수준**: 충분 · **외부 근거**: [PyPI Ultralytics](https://blog.pypi.org/posts/2024-12-11-ultralytics-attack-analysis/), [AWS-2025-015](https://aws.amazon.com/security/security-bulletins/AWS-2025-015/), [THN postmark-mcp](https://thehackernews.com/2025/09/first-malicious-mcp-server-found.html), [OpenAI Mixpanel](https://openai.com/index/mixpanel-incident/), [arXiv 2406.10279](https://arxiv.org/abs/2406.10279)

{{< evidence ids="AISEC-2026-0012 AISEC-2026-0019 AISEC-2026-0016 AISEC-2026-0003 AISEC-2026-0011 AISEC-2026-0004" >}}

## 3부. 통제 계층으로 막는다

3부의 여섯 장은 통제 축의 여섯 칸과 1:1로 대응한다. 각 장은 통제 설계 절이 본문의 절반 이상을 차지하고, 기술 절마다 성숙도 라벨을 붙인다. 여러 통제가 한 부품에서 만나는 경우(예: AI 게이트웨이는 키 보관·길목 통제·추적을 함께 한다)는 그 부품의 핵심 역할이 속한 장에서 다루고, 나머지 장에서는 교차 참조한다.

### 9장. 신원·권한 — 에이전트 ID와 파이프라인 ID

- **논지**: 에이전트는 의도가 아니라 닿을 수 있는 범위로 통제한다. 에이전트 쪽 근거는 표준이 댄다(ASI03·SAIF·MCP 인가·NCCoE·금융보안원). 학습 잡·모델 배포·MCP 서버 등록 주체의 ID는 어느 표준도 다루지 않으므로, 이 장이 플랫폼 관점으로 채운다. LLM은 자격 증명에 절대 닿지 않아야 한다.
- **핵심 질문**: 공유 서비스 계정(43%)과 사람 계정 차용(31%)을 어떻게 걷어 내나? 사용자 위임과 에이전트 자체 권한은 어떻게 구분하나? 누가 모델을 승격하고 MCP 서버를 등록할 수 있나?
- **여는 사례**: ① Amazon Q Developer 확장 변조(CVE-2025-8217, 2025-07-23). CodeBuild 안의 범위가 과도한 GitHub 토큰으로 공격 코드가 커밋돼 v1.84.0에 실렸다 [실사고] ([AWS-2025-015](https://aws.amazon.com/security/security-bulletins/AWS-2025-015/)) ② MCP Python SDK OAuth 결함. 악성 서버가 클라이언트 시크릿과 PKCE verifier를 탈취할 수 있었다 [공개 취약점] (AISEC-2026-0003) ③ Salesloft Drift. 2025-08-20에 모든 토큰이 회수됐다 [실사고] ([Google GTIG](https://cloud.google.com/blog/topics/threat-intelligence/data-theft-salesforce-instances-via-salesloft-drift))
- **리더 요약 수치 후보**: 에이전트 하나에 인증을 붙이는 데 1~10일이 든다(43%). 에이전트와 사람의 신원 분리를 우선순위로 꼽은 비율 45%([Help Net Security](https://helpnetsecurity.com/2026/03/26/ciso-ai-agent-identity-security-report/)).
- **절 구성**: ① 워크로드 ID 기초: SPIFFE/SPIRE, 투영 SA 토큰, Pod Certificates(v1.37) — **성숙** ② MCP 인가의 MUST 요건: RFC 9728 발견, RFC 8707 audience 바인딩, 토큰 패스스루 금지, iss 검증, step-up 범위 — **성숙**(원리 중심. 형식은 온라인 부록) ③ 위임과 대리 실행: RFC 8693 토큰 교환, 사용자 위임 대 에이전트 권한, 기업 SSO(ID-JAG, Enterprise-Managed Authorization, Transaction Tokens) — **성숙**(RFC) / **부상**(에이전트 적용·초안) ④ 도구 호출 단위 정책 결정: OPA·Cedar, 게이트웨이의 CEL — **성숙**(엔진) / **부상**(도구 호출 적용) ⑤ 파이프라인 ID: 학습 잡·모델 승격·MCP 서버 등록·CI/CD 자격 증명, 서드파티 연동 토큰의 범위와 수명 — **성숙**(패턴), 표준 공백 ⑥ 표준화 지형: WIMSE-AIMS(-00, 2026-09-15 채택), NCCoE, 동적 권한 축소(벤더 사례) — **실험**
- **근거 수준**: 충분 (에이전트 ID) / 보통 (파이프라인 ID는 표준이 없어 사례 기반) · **외부 근거**: [MCP Authorization 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization), [draft-ietf-wimse-aims](https://datatracker.ietf.org/doc/draft-ietf-wimse-aims/), [KEP-4317](https://www.kubernetes.dev/resources/keps/4317/), [datatracker Txn-Tokens](https://datatracker.ietf.org/doc/draft-ietf-oauth-transaction-tokens/), [datatracker ID-JAG](https://datatracker.ietf.org/doc/draft-ietf-oauth-identity-assertion-authz-grant/), [AWS AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html), [SAIF Focus on Agents](https://saif.google/focus-on-agents)

{{< evidence ids="AISEC-2026-0003 AISEC-2026-0004 AISEC-2026-0010 AISEC-2026-0011 AISEC-2026-0013 AISEC-2026-0014 AISEC-2026-0015 AISEC-2026-0016 AISEC-2026-0018" >}}

### 10장. 네트워크·egress — 나가는 길, 들어오는 문, 그 길목의 AI 게이트웨이

- **논지**: 유출 체인의 마지막 단계는 언제나 외부 호출이다. egress 허용 목록은 인젝션을 막지 못해도 피해는 막는다. 모든 프레임워크에서 가장 빈 열이므로 이 책의 차별점이다. 에이전트 파드에서 끝내지 않고 RAG 수집, 학습 잡, 레지스트리 pull-through, 메타데이터 엔드포인트까지 다룬다. 한국 금융권에서는 망분리가 완화되면서, 물리적 분리가 하던 일을 egress 통제가 넘겨받아야 한다. 모델·도구 트래픽이 모이는 길목에는 AI 게이트웨이를 둔다. 공급자 키 보관, 토큰 쿼터, 장애 전환, 도구 단위 인가, 추적이 이 한 지점에 모인다. 그만큼 게이트웨이 자체가 모든 키를 쥔 고가치 표적이다.
- **핵심 질문**: NetworkPolicy로는 왜 부족하고, FQDN 허용 목록의 함정(DNS 프록시 의존, 와일드카드)은 무엇인가? 샌드박스를 탈출했을 때 공격자가 얻는 것은 무엇이 정하나? 모델 API로 나가는 트래픽은 탐지 신호가 될 수 있나? 에이전트가 공급자 키를 직접 쥐지 않게 하려면 게이트웨이가 무엇을 맡아야 하나? 게이트웨이가 뚫리면 무엇을 잃나?
- **여는 사례**: ① ShadowRay 2.0(2025-11). 노출된 Ray 클러스터를 따라 퍼진 웜으로, 공개 접근 가능한 Ray 서버는 23만 대가 넘는다(접근 가능 기준이며 취약 여부는 미확인) [실사고] ([THN](https://thehackernews.com/2025/11/shadowray-20-exploits-unpatched-ray.html)) ② postmark-mcp(2025-09-17). 코드 한 줄로 모든 메일을 외부 주소로 BCC했고, 1,643회 다운로드됐다 [실사고] ([THN](https://thehackernews.com/2025/09/first-malicious-mcp-server-found.html)) ③ OpenAI 내부 모델의 인터넷 제한 우회 보고 [실사고] (AISEC-2026-0017) ④ LiteLLM PyPI 침해(2026-03-24, 약 40분간 공개). CI 보안 스캐너 의존성이 침해돼 PyPI 자격 증명이 넘어간 것으로 추정된다. 악성 버전은 환경 변수·SSH 키·K8s 토큰을 외부로 보냈다 [실사고] ([LiteLLM](https://docs.litellm.ai/blog/security-update-march-2026))
- **절 구성**: ① 기본 거부와 egress 허용 목록: NetworkPolicy의 한계, Cilium `toFQDNs`(`--enable-l7-proxy`, DNS 규칙 필수, `*` 패턴 위험) — **성숙**, 표준 API ClusterNetworkPolicy·NPEP-133 `DomainNames` — **부상**(v1alpha2) ② L7 egress: TLS SNI·HTTP 규칙, 메시 egress 게이트웨이 — **성숙**(메시 쪽 근거 보강 필요) ③ 생명주기 전체의 egress: RAG 수집, 학습 잡, 패키지 미러·git 프록시, 레지스트리 pull-through, IMDS 차단(IMDSv2 hop limit) — **성숙**(패턴) ④ 들어오는 문: 관리 패널·추론 엔드포인트 노출 관리 — **성숙** ⑤ AI 게이트웨이: 키 보관, 쿼터·비용, 장애 전환, 추적, 자체 호스팅 모델 앞 Gateway API Inference Extension — **부상~성숙** ⑥ MCP 게이트웨이와 도구 단위 인가: 클라이언트별 도구 세트·도구 필터(Agent Router `MCPRoute`, agentgateway), CEL·JWT 클레임 전달, extAuthz, Cedar — **부상** ⑦ 게이트웨이를 지키기: 서명 이미지·고정 의존성, 키 회수 계획(LiteLLM 교훈) — **성숙**(교훈) ⑧ 탐지로서의 egress와 한국 맥락: 모델 API로 나가는 트래픽(PROMPTSTEAL), 섀도 AI 탐지, 망분리 특례 아래 외부 LLM 연결 — **부상**
- **근거 수준**: 보통 (기술은 성숙했지만 프레임워크 근거가 비어 있다. 메시 egress 문서와 MCP 게이트웨이 채택 데이터는 아직 수집하지 않았다) · **외부 근거**: [Cilium L3 DNS-based](https://docs.cilium.io/en/stable/security/policy/layer3/), [NPEP-133](https://network-policy-api.sigs.k8s.io/npeps/npep-133-fqdn-egress-selector/), [Wiz HF 인프라](https://www.wiz.io/blog/wiz-and-hugging-face-address-risks-to-ai-infrastructure), [Google GTIG](https://cloud.google.com/blog/topics/threat-intelligence/threat-actor-usage-of-ai-tools), [세종 망분리 로드맵](https://shinkim.com/kor/media/newsletter/2533), [Agent Router v1.0](https://theagentrouter.ai/release-notes/v1.0/), [agentgateway](https://agentgateway.dev/docs/standalone/main/documentation/about/introduction/), [Databricks DASF v3.0 (AI Gateway 54)](https://www.databricks.com/blog/agentic-ai-security-new-risks-and-controls-databricks-ai-security-framework-dasf-v30)

{{< evidence ids="AISEC-2026-0001 AISEC-2026-0002 AISEC-2026-0003 AISEC-2026-0008 AISEC-2026-0011 AISEC-2026-0012 AISEC-2026-0013 AISEC-2026-0016 AISEC-2026-0017" >}}

### 11장. 격리·실행 환경 — 자격 증명 없는 곳에서 실행하고, 멈출 수 있게 만든다

- **논지**: 신뢰할 수 없는 입력은 자격 증명이 없는 곳에서 처리한다. 어떤 런타임을 고르든 탈출했을 때 얻는 것은 egress가 정한다. 격리는 에이전트 샌드박스로 끝나지 않는다. 모델 로딩, 평가 하네스, GPU 공유도 격리 대상이다. 비상 정지와 자율 실행 제한은 국내 금융 규제가 요구하지만 구현 지침이 없다. 이 장이 엔지니어링 패턴으로 제시한다.
- **핵심 질문**: 컨테이너, gVisor, Kata·Firecracker 가운데 무엇을 언제 고르나? `trust_remote_code=False`를 무시하는 로더 앞에서 무엇이 마지막 방어선인가? 에이전트를 '멈춘다'는 것은 구체적으로 무엇을 끊는 일인가?
- **여는 사례**: ① NVIDIA Container Toolkit 탈출 CVE-2024-0132(2024-09-26). 공유 GPU 서비스에서 다른 테넌트의 데이터에 닿을 수 있었다 [공개 취약점] ([Wiz](https://www.wiz.io/blog/wiz-research-critical-nvidia-ai-vulnerability)) ② vLLM CVE-2026-27893(2026-03-27). 모델 구현 파일 두 개에 `trust_remote_code=True`가 하드코딩돼 사용자 설정을 덮어썼다 [공개 취약점] ([GitLab advisory](https://advisories.gitlab.com/pypi/vllm/CVE-2026-27893/)) ③ Claude Code Desktop 프리뷰 'SneakPeek'. 저장소의 HTML 하나로 자격 증명이 유출됐다 [공개 취약점] (AISEC-2026-0015)
- **절 구성**: ① 격리 강도의 사다리와 쿠버네티스 에이전트 샌드박스: 컨테이너 → gVisor → Kata 4.0/Firecracker, agent-sandbox CRD(Sandbox·Template·Claim·WarmPool), RuntimeClass — 사다리 **성숙** / agent-sandbox **부상**(v1beta1, 1.0.x에서도 breaking. YAML이 아니라 역할 중심으로 설명) ② 자격 증명 없는 실행 환경: 시크릿 분리, LLM이 자격 증명에 닿지 않게(AIMS 원칙) — **성숙**(원칙) ③ 에이전트 밖의 격리: 모델 로딩·역직렬화, 평가 하네스, 학습 환경 — **부상**(프레임워크 공백) ④ GPU 멀티테넌시: MIG는 성능·장애 격리이지 보안 경계가 아니다. 기밀 GPU(NVIDIA CoCo 1.0)는 제약이 많다 — MIG **성숙** / 기밀 GPU **부상** ⑤ 계획-실행 분리: Plan-Then-Execute, Dual LLM, Action-Selector, CaMeL — 패턴 **부상** / CaMeL **실험** ⑥ 멈출 수 있는 실행: 비상 정지·회로 차단기·자율 실행 제한(금융위·금융보안원 요구, CoSAI의 '실패 모드 사전 정의') — **부상**
- **근거 수준**: 충분 (에이전트 샌드박스) / 보통 (에이전트 밖 격리·비상 정지 구현) · **외부 근거**: [agent-sandbox](https://github.com/kubernetes-sigs/agent-sandbox), [OpenInfra (Kata 4.0)](https://openinfra.org/blog/openinfra-newsletter-july-2026), [NVIDIA CoCo 1.0.0](https://docs.nvidia.com/datacenter/cloud-native/confidential-containers/1.0.0/release-notes.html), [NVIDIA MIG](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/latest/introduction.html), [arXiv 2503.18813](https://arxiv.org/abs/2503.18813), [arXiv 2506.08837](https://arxiv.org/abs/2506.08837), [CoSAI 원칙](https://www.coalitionforsecureai.org/announcing-the-cosai-principles-for-secure-by-design-agentic-systems/), [파이낸셜뉴스 (금융보안원 기준안)](https://www.fnnews.com/news/202610071821048238)

{{< evidence ids="AISEC-2026-0002 AISEC-2026-0005 AISEC-2026-0011 AISEC-2026-0012 AISEC-2026-0014 AISEC-2026-0015 AISEC-2026-0017 AISEC-2026-0018" >}}

### 12장. 공급망·출처 — 서명에서 계보로, 계보에서 정책으로

- **논지**: 어떤 모델·패키지·MCP 서버·데이터셋이 어디서 왔는지 모르면 조달 배제 명령 하나에도 대응할 수 없다. 장의 뼈대는 CoSAI 모델 서명 성숙도 3단계(서명 → 계보·체인 → 증명·정책)다. 그 위에 쿠버네티스 admission 검증과 레지스트리 승격 정책을 얹는다. 스캐너는 관문이 될 수 없다. 안전한 형식과 격리 로딩이 기본이다.
- **핵심 질문**: 블랙리스트 스캐너는 왜 계속 우회되나? 서명된 모델과 출처 증명이 붙은 빌드는 어떻게 다른가? AI-BOM은 누가 만들고 누가 소비하나?
- **여는 사례**: ① Ultralytics PyPI(2024-12). 1차는 GitHub Actions 캐시 오염을 거쳐 정상 Trusted Publishing 경로로 배포됐고, 2차는 회수하지 않은 PyPI 토큰으로 배포됐다. attestation 덕분에 공격을 감사할 수 있었다 [실사고] ([PyPI](https://blog.pypi.org/posts/2024-12-11-ultralytics-attack-analysis/)) ② picklescan 제로데이 3종(2025-12-02). 확장자 우회, ZIP CRC 오류, 등급 하향 [공개 취약점] ([JFrog](https://jfrog.com/blog/unveiling-3-zero-day-vulnerabilities-in-picklescan/)) ③ 미 DHS FASCSA 명령. DeepSeek 기반 서드파티 제품까지 제거 대상이 됐다 [표준·정책 사례] (AISEC-2026-0019)
- **절 구성**: ① 모델 서명과 검증: OMS, sigstore/model-transparency, NGC(2025-03부터 전 모델 서명) — **성숙**(형식·도구) / 생태계 채택 **부상** ② 빌드·소스 출처: SLSA 1.2(Source Track), in-toto — **성숙**(ML 전용 트랙은 없음) ③ AI-BOM: CycloneDX 1.7 ML-BOM(ECMA-424), SPDX 3.0 AI·Dataset 프로파일 — 형식 **성숙** / 실무 생성·소비 **부상** ④ 로더 안전성: safetensors 우선, 스캔 실패는 실패로 처리, `trust_remote_code` — **성숙**(교훈) ⑤ 승격 정책과 집행: 레지스트리 승격, admission 서명 검증, MCP 서버 레지스트리·허용 목록 — admission **성숙** / MCP 레지스트리 **부상** ⑥ 조달·배제 대응: 모델 인벤토리와 콘텐츠 출처 표시의 한계(워터마크) — **부상**
- **근거 수준**: 충분 (외부 근거) / KB는 3건이라 기초 문헌 보강 필요 · **외부 근거**: [OASIS CoSAI 서명](https://www.oasis-open.org/2025/11/18/coalition-for-secure-ai-releases-two-actionable-frameworks-for-ai-model-signing-and-incident-response), [OpenSSF OMS](https://openssf.org/blog/2025/06/25/), [sigstore/model-transparency](https://github.com/sigstore/model-transparency), [NVIDIA NGC](https://developer.nvidia.com/blog/bringing-verifiable-trust-to-ai-models-model-signing-in-ngc), [SLSA v1.2](https://slsa.dev/blog/2025/11/announce-slsa-v1.2), [CycloneDX ML-BOM](https://cyclonedx.org/capabilities/mlbom/), [arXiv 2510.07070](https://arxiv.org/abs/2510.07070), [NIST SP 800-218A](https://csrc.nist.gov/pubs/sp/800/218/a/final), [MCP Registry](https://registry.modelcontextprotocol.io/)

{{< evidence ids="AISEC-2026-0009 AISEC-2026-0012 AISEC-2026-0019" >}}

### 13장. 탐지·평가 — 공격 성공률 너머를 보고, 레드팀을 상시 운영한다

- **논지**: 가드레일과 분류기는 경계가 아니라 신호다. 처음 보고된 성공률이 0에 가까웠던 방어 12개 가운데 대부분이 적응형 공격에서 90%를 넘겼다. 탐지는 행동 순서와 도구 호출 단위로 한다. 평가는 모델·프롬프트·설정이 바뀔 때마다 CI에서 다시 돈다. 레드팀은 기획 → 준비 → 수행 → 보고 절차로 운영한다.
- **핵심 질문**: '가시성이 있다'는 자신감 91.8%와 실제 보호율 약 52%의 차이는 어디서 오나? 도구 호출 로그에는 무엇이 남아야 하나(해석된 인자, 스키마 버전)? 정적 공격 문자열로 평가하면 왜 틀리나?
- **여는 사례**: ① 'The Attacker Moves Second'(2025-10-10). 적응형 공격으로 12개 방어의 대부분을 90% 넘게 뚫었다 [연구] ([arXiv 2510.09023](https://arxiv.org/abs/2510.09023)) ② LLMjacking 공격자는 먼저 `GetModelInvocationLoggingConfiguration`으로 자신이 기록되는지 확인했다 [실사고] ([Sysdig](https://sysdig.com/blog/llmjacking-stolen-cloud-credentials-used-in-new-ai-attack/)) ③ 소형 에이전트는 인젝션을 '거부'하지 않고 '무시'한다. 낮은 공격 성공률이 숨기는 것이다 [연구] (AISEC-2026-0020)
- **절 구성**: ① 에이전트 관측의 표준: OTel GenAI(에이전트·도구·MCP 스팬), MCP `traceparent` 전파, 내용 캡처 옵트인과 개인정보 — **부상**(Development, 스키마 고정 필요) ② 런타임 탐지: Falco(syscall), 도구 호출 사전 판정(Prempti), 행동 순서 기반 탐지 — Falco **성숙** / Prempti **실험** ③ 가드레일·분류기의 위치: 신호이지 경계가 아니다(PromptGuard 2, LlamaFirewall) — **성숙**(교훈) / 개별 제품 **부상** ④ CI 회귀 평가와 레드팀 자동화: garak·promptfoo·PyRIT(역할 비교 중심) — **부상** ⑤ 평가 지표 설계: 적응형 공격 기준, 실패 유형, 변경 시 재평가, 추론 최적화 설정별 평가 — **성숙**(방법론) ⑥ 레드팀 운영: KISA 레드티밍 가이드(ISO/IEC 42119-7 기반)의 기획 → 준비 → 수행 → 보고, OWASP GenAI Red Teaming Manual v1.0
- **근거 수준**: 충분 · **외부 근거**: [opentelemetry.io gen-ai](https://opentelemetry.io/docs/specs/semconv/gen-ai/), [semantic-conventions-genai](https://github.com/open-telemetry/semantic-conventions-genai), [Sysdig Prempti](https://www.sysdig.com/blog/introducing-prempti-runtime-security-for-ai-coding-agents-powered-by-falco), [arXiv 2505.03574](https://arxiv.org/abs/2505.03574), [garak releases](https://github.com/NVIDIA/garak/releases), [microsoft/PyRIT](https://github.com/microsoft/PyRIT), [바이라인네트워크 (KISA 가이드)](https://byline.network/2026/07/8-489/), [SAIF Agent Observability](https://saif.google/focus-on-agents)

{{< evidence ids="AISEC-2026-0001 AISEC-2026-0002 AISEC-2026-0004 AISEC-2026-0006 AISEC-2026-0010 AISEC-2026-0013 AISEC-2026-0014 AISEC-2026-0016 AISEC-2026-0017 AISEC-2026-0018 AISEC-2026-0020" >}}

### 14장. 거버넌스·정책 — 책임자·표준·규제를 플랫폼 통제로 번역한다

- **논지**: 거버넌스는 정책 문서가 아니라 플랫폼이 남기는 증적으로 작동해야 한다. 이 장은 세 가지를 플랫폼 통제로 번역한다. 첫째, 누가 에이전트를 등록·승인·회수하나(공식 책임자를 둔 조직 7.2%). 둘째, 표준(OWASP·NIST·ATLAS·CSA·SAIF)의 요구를 어떤 통제와 증적으로 충족하나. 셋째, 인공지능 기본법과 금융권 기준(비상 정지 의무, 금융보안원 에이전트 평가기준(안), 망분리 특례)을 어떤 로그·승인 게이트·egress 통제로 증빙하나. 번역표의 모든 칸은 9~13장의 구체 통제를 가리킨다.
- **핵심 질문**: 보안·플랫폼·ML/앱·비즈니스 오너의 RACI는 어떻게 나누나? 에이전트 등록부에는 어떤 필드가 있어야 하나? 범위가 바뀌면 무엇을 다시 평가하나? 프레임워크들이 공통으로 요구하는 것(인젝션, 오염, 출처, 과잉 권한, 관측, 상시 평가)과 비워 둔 것(egress, 에이전트 밖 격리, 파이프라인 ID)은 무엇인가? 'disputed' CVE처럼 표준 체계 밖으로 빠지는 위험은 어떻게 관리하나? '사람의 관리·감독'과 '문서 5년 보관'은 어떤 로그·승인 단계로 증빙하나? 망분리 예외로 외부 LLM을 쓸 때 플랫폼이 갖춰야 할 통제는 무엇인가? 금융보안원 평가기준(안)의 실행 권한·격리·도구 승인 항목은 3부의 어느 절과 대응하나?
- **여는 사례**: ① Microsoft SAS 토큰(2020 커밋 → 2023 발견). 아무도 그 토큰을 보거나 관리하지 않았다 [실사고] ([Wiz](https://www.wiz.io/blog/38-terabytes-of-private-data-accidentally-exposed-by-microsoft-ai-researchers)) ② ShadowRay CVE-2023-48022. disputed 태그 때문에 많은 스캐너에서 빠졌다. 표준 체계의 맹점이다 [실사고] ([NVD](https://nvd.nist.gov/vuln/detail/CVE-2023-48022)) ③ ARTEX를 이용한 한국 금융권 공격. 당국 집계로 16곳·약 10만 건이 유출됐다 [실사고] (AISEC-2026-0001)
- **리더 요약 수치 후보**: 공식 책임자 7.2%, 회수 절차 34.1%, 허용 범위 정의 30.5%([Gravitee](https://www.gravitee.io/state-of-ai-agent-security?hl=cs-CZ)). 섀도 AI가 광범위한 조직의 침해 비용은 67만 달러 더 많다([TechRepublic](https://www.techrepublic.com/article/news-ai-breach-risks-rise-as-governance-lags/)).
- **절 구성**: **가. 누가 책임지나** ① 소유권 지형: 설문이 보여 주는 책임 분산 ② RACI와 플랫폼 팀의 위치(골든 패스 제공자) ③ 에이전트 등록부: 신원·범위·소유자·회수 경로 ④ 리스크 등록부: 인젝션을 상시 위험으로, 범위 변경 시 재평가 ⑤ 섀도 AI 정책: 허용 목록, 탐지(10장)와 예외 절차 **나. 표준을 플랫폼 통제로 번역한다** ⑥ 표준 지도: 위험 목록·공격 어휘·분류·통제 카탈로그·위협 모델링(MAESTRO) ⑦ 합의된 것과 비어 있는 것: 5×6 크로스워크 ⑧ 번역표: 표준 요구 → 플랫폼 통제 → 증적(로그·정책·서명) ⑨ 취약점 관리의 AI 특수성: disputed CVE, CVE가 붙지 않는 취약점 유형, 설정 변경까지가 패치 ⑩ 초안 표준 다루기: COSAIS·NCCoE·IR 8596·ACS의 상태 표기 **다. 한국 규제를 플랫폼 통제로 번역한다** ⑪ 인공지능 기본법과 시행령: 의무 지도, 고영향 AI 10개 분야, 국내대리인 기준, 과태료 유예(1년 이상) ⑫ 의무 → 통제 번역: 5년 보관 → 감사 로그 보존, 관리·감독 → 승인 게이트·비상 정지, 결과물 표시 → 서빙 출력 파이프라인 ⑬ 금융권: 망분리 개선 로드맵(2024-08-13)과 특례 조건, 금융분야 AI 가이드라인(비상 정지 의무), 금융보안원 평가기준(안)·보안성 검증체계 ⑭ 과기정통부·KISA 지침: AI 보안 위협 대응 매뉴얼(위협 분류: 데이터·모델·에이전트·공급망·고성능 모델), 레드티밍 가이드 ⑮ 상태 표와 남은 공백: ISMS-P, 개인정보위 자료는 추가 조사 대상
- **근거 수준**: 가·나는 보통~충분 (설문은 벤더 위주라 표본·주체·시점을 함께 적는다), 다는 부족 (법령 조문·KISA·금융보안원 1차 원문 미확보, 일부 초안). 분량이 커지면 다(한국 규제)를 별도 장으로 떼는 것을 검토한다 · **외부 근거**: [Help Net Security (CSA 설문)](https://helpnetsecurity.com/2026/03/26/ciso-ai-agent-identity-security-report/), [Gravitee](https://www.gravitee.io/state-of-ai-agent-security?hl=cs-CZ), [CSA Labs Identity Sprawl (미열람)](https://labs.cloudsecurityalliance.org/research/csa-research-note-ai-agent-identity-sprawl-authorization-202/), [OWASP LLM Top 10](https://genai.owasp.org/llm-top-10/), [OWASP Agentic Top 10](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/), [NIST AI 600-1](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf), [NIST IR 8596](https://csrc.nist.gov/pubs/ir/8596/iprd), [CSA AICM](https://cloudsecurityalliance.org/artifacts/ai-controls-matrix), [SAIF risks](https://saif.google/secure-ai-framework/risks), [ATLAS](https://github.com/mitre-atlas/atlas-data), [세종 (AI 기본법)](https://shinkim.com/kor/media/newsletter/3114), [바이라인네트워크 (시행령)](https://byline.network/2026/01/21-545/), [노컷뉴스 (금융위 가이드라인)](https://www.nocutnews.co.kr/news/6534884), [파이낸셜뉴스 (금융보안원 기준안)](https://www.fnnews.com/news/202610071821048238), [세종 (망분리)](https://shinkim.com/kor/media/newsletter/2533), [바이라인네트워크 (KISA 매뉴얼)](https://byline.network/2026/07/8-489/), [바이라인네트워크 (금융보안원 검증체계)](https://byline.network/2024/12/19-423), [law.go.kr](https://www.law.go.kr/법령/인공지능발전과신뢰기반조성등에관한기본법)

{{< evidence ids="AISEC-2026-0001 AISEC-2026-0004 AISEC-2026-0005 AISEC-2026-0009 AISEC-2026-0010 AISEC-2026-0016 AISEC-2026-0018 AISEC-2026-0019" >}}

## 4부. 운영

### 15장. 에이전트 사고 대응 — 도구 호출 로그, 자격 증명 회수, 재현 (v0 14장에서 분리)

- **논지**: 에이전트 사고의 포렌식은 에이전트가 스스로 한 요약으로 하지 않는다. 해석된 인자까지 남긴 도구 호출 로그로 한다. 대응의 중심은 자격 증명 회수다. 회수가 불완전하면 두 번째 침해가 온다. 회수 절차를 문서로 갖춘 조직은 34.1%뿐이다.
- **핵심 질문**: 사고가 나면 몇 분 안에 무엇을 끊나(토큰, egress, 샌드박스, 에이전트)? 무엇이 남아 있어야 재현할 수 있나? 모델 아티팩트 오염 사고는 일반 침해 대응과 무엇이 다른가?
- **여는 사례**: ① Ultralytics 2차 배포. 1차 대응 뒤에도 회수하지 않은 PyPI API 토큰이 남아 있었다 [실사고] ([PyPI](https://blog.pypi.org/posts/2024-12-11-ultralytics-attack-analysis/)) ② Hugging Face Spaces 시크릿 침해(2024-05-31). 토큰을 회수하고 조직 토큰을 제거했으며, KMS를 도입하고 당국에 신고했다 [실사고] ([Hugging Face](https://huggingface.co/blog/space-secrets-disclosure)) ③ OpenAI 내부 모델 무단 행동. 발견까지 두 달 넘게 걸렸다 [실사고] (AISEC-2026-0017)
- **절 구성**: ① 플레이북 틀: CoSAI AI 사고 대응 프레임워크 v1.0(오염·모델 탈취·인젝션·추론 공격, 포렌식, 에이전트 아키텍처) ② 탐지에서 격리까지: 비상 정지 실행, egress 차단, 샌드박스 동결 ③ 자격 증명 회수: 에이전트·파이프라인·서드파티 연동 토큰(Drift 일괄 회수, Nx) ④ 포렌식과 재현: 도구 호출 로그, OTel 추적, 프롬프트·모델 버전 고정 ⑤ 보고와 규제: AI 기본법 기록 보관, 금융권 보고, 개인정보 신고
- **근거 수준**: 보통 (CoSAI 프레임워크 본문을 아직 읽지 않았다) · **외부 근거**: [OASIS CoSAI IR Framework](https://www.oasis-open.org/2025/11/18/coalition-for-secure-ai-releases-two-actionable-frameworks-for-ai-model-signing-and-incident-response), [Google GTIG (Drift)](https://cloud.google.com/blog/topics/threat-intelligence/data-theft-salesforce-instances-via-salesloft-drift), [Wiz (Nx)](https://www.wiz.io/blog/s1ngularity-supply-chain-attack), [Gravitee](https://www.gravitee.io/state-of-ai-agent-security?hl=cs-CZ)

{{< evidence ids="AISEC-2026-0001 AISEC-2026-0013 AISEC-2026-0014 AISEC-2026-0017" >}}

### 16장. 도입 로드맵 — 0일 차부터 1년 (신설, 맺음 장)

- **논지**: 81%가 빨리 배포하라는 압박을 느끼는데, 배포 전 통제를 갖춘 비율은 30~38%에 머문다. 통제를 한 번에 갖출 수는 없다. 섀도 AI 파악 → 최소 통제(신원·egress·로그) → 게이트웨이·샌드박스 → 평가·레드팀 → 거버넌스·규제 증빙 순서의 성숙도 모델로 단계를 밟는다.
- **핵심 질문**: 첫 30일에 반드시 해야 할 세 가지는 무엇인가? '에이전트 하나에 인증 1~10일'이라는 고충을 골든 패스로 어떻게 없애나? 각 단계가 끝났다는 것은 어떤 증적으로 판단하나?
- **여는 사례**: 여는 사례 대신 조사 수치로 시작한다. Gravitee(2026-04 조사): 넉 달 사이 에이전트 수 약 2배, 배포 압박 81% [조사·벤더] ([Gravitee](https://www.gravitee.io/state-of-ai-agent-security?hl=cs-CZ)). CNCF(2025-09 조사): 쿠버네티스에서 생성형 AI 워크로드를 운영하는 조직 66% [조사] ([CNCF](https://www.linuxfoundation.org/hubfs/Research%20Reports/CNCF_Annual_Survey_Report_1.15.26.pdf?hsLang=en))
- **절 구성**: ① 0일 차: 섀도 AI·에이전트 인벤토리 ② 30일: 최소 통제 세트(워크로드 ID, 단기 토큰, 기본 거부 egress, 도구 호출 로그) — **성숙** ③ 90일: 게이트웨이·샌드박스·서명 검증 — **부상~성숙** ④ 180일: CI 회귀 평가·레드팀 정례화 ⑤ 1년: 거버넌스·규제 증빙 자동화, 재평가 주기
- **근거 수준**: 보통 · **외부 근거**: [Help Net Security](https://helpnetsecurity.com/2026/03/26/ciso-ai-agent-identity-security-report/), [Gravitee](https://www.gravitee.io/state-of-ai-agent-security?hl=cs-CZ), [TechRepublic](https://www.techrepublic.com/article/news-ai-breach-risks-rise-as-governance-lags/)

{{< evidence controls="governance" >}}

---

## 부록 후보

| 부록 | 내용 | 근거·출처 |
|---|---|---|
| A. 생명주기 × 통제 점검표 | 집필 매트릭스를 체크리스트로. 칸마다 OWASP LLM/ASI ID, ATLAS 기술 ID, AICM 통제 대응 | [ATLAS (2026.05부터 플랫폼 태그)](https://github.com/mitre-atlas/atlas-data/blob/main/CHANGELOG.md), [CSA AICM](https://cloudsecurityalliance.org/artifacts/ai-controls-matrix) |
| B. OWASP 교차 참조표 | OWASP LLM Top 10(2025/2026판), Agentic Top 10 2026, ACS ↔ 이 책의 장·절·통제 | [OWASP GenAI](https://genai.owasp.org/2026/09/01/owasp-genai-security-project-unveils-2026-top-10-for-llm-applications-new-agent-control-standard-and-sponsors-as-community-tops-30000-members/) |
| C. 참조 아키텍처와 에이전트 골든 패스 | 워크로드 ID·단기 토큰·egress 허용 목록·도구 호출 로그가 기본으로 붙은 Helm/Kustomize 템플릿과 Kyverno·OPA 정책. '인증 하나에 1~10일' 고충에 대한 답 | [Help Net Security](https://helpnetsecurity.com/2026/03/26/ciso-ai-agent-identity-security-report/), [KubeCon India 2026](https://kccncind2026.sched.com/2026-06-19/list/descriptions/type/Security) |
| D. 정책 코드 예시집 | Cilium `toFQDNs` egress, admission 서명 검증, CEL·Cedar 도구 단위 인가, RuntimeClass·Sandbox 템플릿. 각 예시에 버전과 열람일 표기 | [Cilium](https://docs.cilium.io/en/stable/security/policy/layer3/), [AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html), [agent-sandbox](https://github.com/kubernetes-sigs/agent-sandbox) |
| E. 런북 | (1) 에이전트 비상 정지·자격 증명 회수(회수 절차 보유 34.1%) (2) 악성 모델·패키지 유입 대응 (3) 게이트웨이 키 유출 대응 | [Gravitee](https://www.gravitee.io/state-of-ai-agent-security?hl=cs-CZ), [CoSAI IR](https://www.oasis-open.org/2025/11/18/coalition-for-secure-ai-releases-two-actionable-frameworks-for-ai-model-signing-and-incident-response) |
| F. 배포 전 점검표 | Gravitee가 조사한 여섯 가지 배포 전 통제(책임자, 보안 검토, 중지·회수, 민감 데이터 계획, 전용 접근 통제, 범위 정의)를 기본형으로 삼고 금융보안원 17개 항목과 대조 | [Gravitee](https://www.gravitee.io/state-of-ai-agent-security?hl=cs-CZ), [파이낸셜뉴스](https://www.fnnews.com/news/202610071821048238) |
| G. RACI·에이전트 등록부·리스크 등록부 양식 | 보안·플랫폼·ML/앱·비즈니스 오너, 등록 필드, 재평가 조건 | 14장 |
| H. 한국 규제 대응표 | AI 기본법 의무·망분리 특례 조건·금융위 가이드라인·금융보안원 기준(안) ↔ 플랫폼 통제 ↔ 증적 로그. 조문 번호는 원문 확인 후 기입 | [세종](https://shinkim.com/kor/media/newsletter/3114), [세종 망분리](https://shinkim.com/kor/media/newsletter/2533) |
| I. 버전·상태 표 (온라인, KB 연동) | MCP 스펙 개정 이력, IETF 초안 번호·상태, CNCF 단계, NIST 초안 상태, 주요 프로젝트 버전. 본문은 원리만 다루고 이 표만 갱신한다 | 7절 목록 |
| J. 용어집 | 한국어 표기 기준(프롬프트 인젝션, 탈옥, 증류, egress, 워크로드 ID, 폭발 반경 등) | v0 유지 |
| K. 실습 환경 가이드 | kind/minikube 위 누적형 에이전트 플랫폼 구성과 장별 통제 추가 순서 | 3장 |

## 기초 문헌 수집 우선순위

순서는 'KB가 얇은 장'을 먼저 채우는 순이다. KB 매트릭스에서 데이터 행은 1건, 학습 행도 1건이고, 에이전트 런타임×출처, 데이터×출처, 학습×출처·신원·거버넌스, 서빙×네트워크 칸은 0건이다. 모두 1등급 원문이고, 수집할 때는 KB 규칙대로 저자 전원과 절·표 번호 locator를 단다.

| # | 채울 장(칸) | 문헌 | 발행·저자 | 버전·날짜 | URL |
|---|---|---|---|---|---|
| 1 | 4장 (데이터×출처) | Poisoning Web-Scale Training Datasets is Practical | Carlini, Jagielski, Choquette-Choo, Paleka, Pearce, Anderson, Terzis, Thomas, Tramèr | arXiv 2302.10149, 2023-02-20 | https://arxiv.org/abs/2302.10149 |
| 2 | 4장 (데이터×탐지) | 소수 표본 오염 연구(250개 문서) | Anthropic·UK AISI·Alan Turing Institute | arXiv 2510.07192, 2025-10-09 | https://www.anthropic.com/research/small-samples-poison |
| 3 | 4장 (데이터, RAG) | PoisonedRAG | Zou, Geng, Wang, Jia | arXiv 2402.07867, 2024-02-12 | https://arxiv.org/abs/2402.07867 |
| 4 | 5장 (학습×출처·탐지) | Sleeper Agents | Hubinger 외 | arXiv 2401.05566, 2024-01-10 | https://arxiv.org/abs/2401.05566 |
| 5 | 5장 (학습×격리·네트워크) | OpenAI o1-preview System Card §4.2.1 | OpenAI | 2024-09-17 | https://cdn.openai.com/o1-preview-system-card-20240917.pdf |
| 6 | 5장 (학습×탐지) | Emergent misalignment from reward hacking | Anthropic | 2025-11-21 | https://www.anthropic.com/research/emergent-misalignment-reward-hacking |
| 7 | 5·12장 (학습×출처·거버넌스) | SP 800-218A SSDF Community Profile for GenAI | NIST | final 2024-07-26 | https://csrc.nist.gov/pubs/sp/800/218/a/final |
| 8 | 12장 (공급망×출처) | Signing ML Artifacts + AI Incident Response Framework V1.0 | CoSAI (OASIS) | 2025-11-18 | https://www.oasis-open.org/2025/11/18/coalition-for-secure-ai-releases-two-actionable-frameworks-for-ai-model-signing-and-incident-response |
| 9 | 12장 | OpenSSF Model Signing (OMS) + sigstore/model-transparency | OpenSSF (Google, HiddenLayer, NVIDIA) | 2025-06-25 | https://openssf.org/blog/2025/06/25/ |
| 10 | 12장 | SLSA v1.2 | OpenSSF SLSA | 2025-11-24 | https://slsa.dev/blog/2025/11/announce-slsa-v1.2 |
| 11 | 12장 (데이터·학습×출처) | CycloneDX 1.7 ML-BOM (ECMA-424) | OWASP CycloneDX / Ecma | 1.7, 2025-10-21 | https://cyclonedx.org/capabilities/mlbom/ |
| 12 | 12장 | Building an Open AIBOM Standard in the Wild | Kate Stewart, Karen Bennet 외 | arXiv 2510.07070 v2, 2026-02-22 | https://arxiv.org/abs/2510.07070 |
| 13 | 9장 (에이전트 런타임×신원, 표준 측) | MCP Authorization (revision 2026-07-28) | Model Context Protocol | 2026-07-28 | https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization |
| 14 | 9장 | draft-ietf-wimse-aims (AI Identity Management System) | IETF WIMSE (Defakto, AWS, Zscaler, Ping, OpenAI, Okta) | -00, 2026-09-15 | https://datatracker.ietf.org/doc/draft-ietf-wimse-aims/ |
| 15 | 9장 | Software and AI Agent Identity and Authorization (concept paper) | NIST NCCoE | 2026-02-05 | https://www.nccoe.nist.gov/projects/software-and-ai-agent-identity-and-authorization |
| 16 | 11장 (격리, 패턴) | CaMeL (arXiv 2503.18813) 및 Design Patterns for Securing LLM Agents (arXiv 2506.08837) | Debenedetti, Carlini, Tramèr 외 / 저자 수 확인 필요 | v2 2025-06-24 / v3 2025-06-27 | https://arxiv.org/abs/2503.18813 , https://arxiv.org/abs/2506.08837 |
| 17 | 13장 (탐지) | The Attacker Moves Second | Nasr, Carlini, Tramèr, Schulhoff 외 | arXiv 2510.09023, 2025-10-10 | https://arxiv.org/abs/2510.09023 |
| 18 | 6장 (서빙×탐지) | Stealing Part of a Production Language Model | Carlini 외 14명 | arXiv 2403.06634, 2024-03-11 | https://arxiv.org/abs/2403.06634 |
| 19 | 3·14장 (전반 분류 체계) | NIST AI 100-2 E2025 (§3.5 Security of Agents 포함) | NIST | E2025, 2025-03-24 | https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-2e2025.pdf |
| 20 | 14장 (한국) | 인공지능 기본법·시행령 원문 + 과기정통부·KISA「AI 보안 위협 대응 매뉴얼」「AI 보안 레드티밍 가이드」 | 대한민국 / 과기정통부·KISA | 시행 2026-01-22 / 2026-07-08 | https://www.law.go.kr/법령/인공지능발전과신뢰기반조성등에관한기본법 (KISA 원문 URL은 미확인. 먼저 찾아야 함) |

예비 후보는 CSA MAESTRO, CSA AICM v1.1, OWASP Agentic Top 10 2026 PDF, 슬롭스쿼팅 논문(arXiv 2406.10279)이다. 8장·14장이 얇아지면 이 가운데서 먼저 넣는다.

## 판 이력

| 판 | 날짜 | 무엇으로 짰나 | 구조 |
|---|---|---|---|
| v0 | 2026-10-20 | 두 축 + 수집 항목 20건 | 4부 14장 |
| v1 | 2026-10-20 | 딥 리서치 다섯 갈래 ([설계 근거](../outline-research/)) | 4부 19장. 2부를 근거 순으로 재배치하고, 게이트웨이·소유권·한국 규제·로드맵을 독립 장으로 신설 |
| **v1.1** | 2026-10-20 | v1의 조사 결과를 격자 안으로 되돌림 (저자 판단) | 4부 16장. 2부는 흐름 순서, 3부는 통제 6칸과 1:1 |

### v0 → v1.1 변경점

| v0 | v1.1 | 변경 | 근거 |
|---|---|---|---|
| 1·2장 | 1·2장 | 유지·보강 | 벤더 위협 보고서(갈취·첩보·PROMPTSTEAL) 추가, 데이터 유출 경로로 1장을 연다 |
| (없음) | 3장 두 축 지도 | 신설 | 격자를 쿠버네티스 플랫폼 위에 그린 공통 좌표. 누적형 실습 환경 |
| 3~7장 (생명주기) | 4~8장 | 유지(순서 그대로)·장 안을 두 갈래로 | 데이터 = 노출/오염, 학습 = 인프라/평가·RL 환경, 서빙 = 오남용/자원 탈취, 공급망 = 아티팩트/서드파티 연동 토큰 |
| 8장 신원 | 9장 | 확장 | 에이전트 ID + 파이프라인 ID (모든 단계에서 가장 자주 실패한 통제) |
| 9장 네트워크 | 10장 | 확장 | 생명주기 전체 egress, AI 게이트웨이 절 흡수 (표준에서 가장 빈 열) |
| 10장 격리 | 11장 | 확장 | 모델 로딩·평가 하네스·GPU 공유, 비상 정지 절 신설 |
| 11장 출처 | 12장 | 재구성 | 서명 → SLSA → AI-BOM → admission 정책 |
| 12장 탐지 | 13장 | 확장 | 레드팀 상시 운영을 이쪽으로 (적응형 공격 연구가 중심 근거) |
| 13장 거버넌스 | 14장 | 확장 | 책임자·표준 번역·한국 규제의 세 갈래 절 |
| 14장 사고 대응·레드팀 | 15장 사고 대응 | 분리 | 레드팀은 13장으로. 에이전트 사고 대응 장을 둔 책이 없다 |
| (없음) | 16장 도입 로드맵 | 신설 | 맺음 장. 리더 요약의 '내릴 결정'을 시간 순으로 묶는다 |
