---
title: "목차 v1 설계 근거 — 딥 리서치 리포트"
description: "기존 책·강의, 표준 크로스워크, 통제 기술 성숙도, 생명주기별 사고, 독자 수요·한국 규제를 조사해 목차 v1을 설계한 리포트"
weight: 25
updated: "2026-10-20"
---

> 이 리포트는 2026-10-20 딥 리서치 스킬로 만들었다. 조사원 다섯 명이 갈래별로 웹 원문을 읽고 노트를 남겼고(웹 접근 거절 시 우회 금지, 읽은 페이지의 사실만 사용), 작성자가 노트를 종합했다. 결론은 [목차 v1](../outline/)에 반영되어 있다. 7절 '미확인·주의'의 주장은 책에 인용하기 전에 1차 원문으로 확인한다.

**결론부터.** 두 축(생명주기 × 통제 계층)은 그대로 두고, 무게중심을 3부 '통제 계층'으로 옮긴다. 3부를 분량의 40% 이상으로 키우고, 2부 '생명주기'는 사고 근거가 강한 순서로 다시 배치한 '공격 표면 지도'로 줄인다. 이유는 네 갈래 조사에서 같은 방향이 나왔기 때문이다. 첫째, 확인한 영어권 책은 모두 OWASP 항목 순서나 공격 기법·킬체인 순서로 짜여 있다. 통제 계층(신원·egress·격리·출처)을 장 단위 뼈대로 쓴 책은 없고, 에이전트 사고 대응을 독립 장으로 둔 책도 없다([O'Reilly](https://www.oreilly.com/library/view/-/9781098162191/), [No Starch](https://nostarch.com/node/829)). 둘째, 표준·프레임워크를 5×6 매트릭스에 겹쳐 보면 **네트워크·egress 열은 모든 행에서 비어 있거나 얇다**. 쿠버네티스 수준의 지침을 주는 프레임워크도 찾지 못했다([NIST COSAIS](https://csrc.nist.gov/projects/cosais), [CSA MAESTRO](https://cloudsecurityalliance.org/blog/2025/02/06/agentic-ai-threat-modeling-framework-maestro)). 셋째, 그 빈칸을 채울 플랫폼 기술은 2026년에 1.0·GA·RFC 수준에 도달했다. Cilium FQDN egress, SPIFFE/SPIRE, agent-sandbox v1.0, Agent Router v1.0, MCP 인가의 MUST 요건이 그 예다. 지금은 '실험'이 아니라 '설계'를 가르칠 수 있다([CNCF](https://www.cncf.io/projects/), [agent-sandbox](https://github.com/kubernetes-sigs/agent-sandbox/releases)). 넷째, 독자가 가장 아파하는 곳은 공격 기법이 아니다. 과잉 권한, 행동 가시성 부족, 책임자 부재다. 에이전트 행동에 공식 책임자를 지명한 조직은 7.2%뿐이다([Gravitee](https://www.gravitee.io/state-of-ai-agent-security?hl=cs-CZ), [Help Net Security](https://helpnetsecurity.com/2026/03/26/ciso-ai-agent-identity-security-report/)). 그래서 v1은 v0의 14장을 19장으로 늘린다. 신설하는 장은 참조 아키텍처·신뢰 경계, AI 게이트웨이, 운영 모델·소유권, 한국 규제 번역, 도입 로드맵이다. 사고 대응은 레드팀에서 떼어 독립 장으로 세운다. 한국 독자에게만 필요한 부분도 정한다. 금융권 망분리 완화, 인공지능 기본법(2026-01-22 시행), 금융보안원 에이전트 평가기준(안)을 플랫폼 통제로 번역하는 장이다. 다만 이 부분은 근거 대부분이 2차 보도와 초안이다. 출간 전에 1차 원문을 확인해야 한다.

---

## 1. 한눈에 보기 — 일곱 가지 설계 결정

| # | 결정 | 왜 | 근거 |
|---|---|---|---|
| 1 | **3부(통제 계층)를 책의 몸통으로 키운다(분량 40% 이상, 6장)** | 통제 계층으로 장을 세운 책이 없다. 영어권 책은 OWASP 순서(Wilson, Malik 외)나 공격 기법 순서(Sotiropoulos, Dursey)를 따른다 | [O'Reilly](https://www.oreilly.com/library/view/-/9781098162191/), [Packt](https://packtpub.com/product/adversarial-ai-attacks-mitigations-and-defense-strategies/9781835087985), [No Starch](https://nostarch.com/node/829) |
| 2 | **1부 끝에 '참조 아키텍처와 신뢰 경계' 장을 신설하고, 누적형 실습 환경을 함께 깐다** | 신뢰 경계 장을 앞에 두는 것은 검증된 관례다(Wilson 3장, Malik 외 4장). 쿠버네티스 위 AI 플랫폼 지도는 2·3부 전체가 참조하는 그림이 된다 | [O'Reilly](https://www.oreilly.com/library/view/-/9781098162191/), [Packt](https://subscription.packtpub.com/book/data/9781836203759) |
| 3 | **2부를 사고 근거가 강하고 독자가 많이 겪는 순서로 재배치한다: 서빙 → 에이전트 런타임 → 공급망 → 데이터 → 학습·평가 인프라** | 서빙·공급망은 실사고만으로 논증할 수 있다. 응답자의 52%는 모델을 학습하지 않고, 37%는 관리형 API를 쓴다 | [CNCF Survey](https://www.linuxfoundation.org/hubfs/Research%20Reports/CNCF_Annual_Survey_Report_1.15.26.pdf?hsLang=en), 사건 노트 §3·§5 |
| 4 | **'AI 게이트웨이' 장을 신원과 네트워크 사이에 신설한다** | 키 보관·도구 단위 인가·토큰 쿼터·추적이 한 지점에 모인다. Agent Router v1.0으로 API가 안정됐고, LiteLLM 침해는 게이트웨이 자체가 공급망 위험이라는 점을 보여 준다 | [Agent Router v1.0](https://theagentrouter.ai/release-notes/v1.0/), [LiteLLM](https://docs.litellm.ai/blog/security-update-march-2026) |
| 5 | **네트워크·격리·신원 장의 범위를 에이전트 밖까지 넓힌다(학습 잡·모델 로딩·평가 하네스·파이프라인 ID)** | 프레임워크 매트릭스에서 가장 빈 칸이다. 실사고(ShadowRay, Amazon Q 토큰, o1-preview Docker API)는 정확히 이 칸에서 났다 | [Oligo](https://www.oligo.security/blog/shadowray-attack-ai-workloads-actively-exploited-in-the-wild), [AWS-2025-015](https://aws.amazon.com/security/security-bulletins/AWS-2025-015/), [OpenAI system card](https://cdn.openai.com/o1-preview-system-card-20240917.pdf) |
| 6 | **4부를 '소유권 → 표준 번역 → 한국 규제 → 사고 대응 → 로드맵' 다섯 장으로 다시 짠다. 사고 대응은 레드팀과 분리한다** | 공식 책임자 7.2%, 회수 절차 보유 34.1%. 확인한 어느 책에도 에이전트 IR 장이 없다 | [Gravitee](https://www.gravitee.io/state-of-ai-agent-security?hl=cs-CZ), 책·과정 노트 §2 |
| 7 | **OWASP는 뼈대가 아니라 교차 참조 부록으로 쓰고, 모든 기술 절에 성숙/부상/실험 라벨과 '버전·상태 표'를 붙인다** | OWASP 항목별 해설은 포화 상태다. MCP 스펙은 약 1년 사이 세 번 크게 바뀌었다(2025-06 → 2025-11 → 2026-07) | [OWASP GenAI 2026](https://genai.owasp.org/2026/09/01/owasp-genai-security-project-unveils-2026-top-10-for-llm-applications-new-agent-control-standard-and-sponsors-as-community-tops-30000-members/), [MCP changelog](https://modelcontextprotocol.io/specification/2026-07-28/changelog) |

장 틀은 v0 그대로 쓴다: **리더용 요약 1쪽 → 사례 → 동작 원리 → 통제 설계 → 점검 목록**. 장마다 지킬 표기 규칙 세 가지를 더한다. (a) 사례 절에서 각 사례가 [실사고], [공개 취약점], [연구] 중 무엇인지 밝힌다. (b) 통제 설계 절의 기술마다 성숙·부상·실험 라벨을 붙인다. (c) 점검 목록에 OWASP(LLMxx·ASIxx)와 MITRE ATLAS 기술 ID를 함께 단다.

---

## 2. 근거 요약 — 다섯 갈래 조사가 구조에 대해 말한 것

### 기존 책은 OWASP와 킬체인을 따른다. 통제 계층과 사고 대응은 빈자리다

2024~2027년에 나왔거나 출간이 예고된 영어권 책은 세 부류로 나뉜다. OWASP 기반 개발자·AppSec 책, 공격 유형 중심의 적대적 ML 책, 레드팀 현장 교범이다. Wilson의 『The Developer's Playbook for LLM Security』(O'Reilly, 2024-09)는 2장에서 OWASP Top 10을 소개하고, 4~9장에서 그 위험을 대체로 순서대로 다룬다. 에이전트는 'Excessive Agency' 소절과 12장의 'Autonomous Agents'에서만 나온다([O'Reilly](https://www.oreilly.com/library/view/-/9781098162191/)). Sotiropoulos의 책(Packt, 2024-07, 586쪽)은 '모델 개발 공격'과 '배포된 AI 공격'으로 부를 나눈다. 생명주기를 거칠게 쓰는 셈이다. 그러나 부 안의 장은 여전히 공격 유형별이다([Packt](https://packtpub.com/product/adversarial-ai-attacks-mitigations-and-defense-strategies/9781835087985)). Dursey의 『Red Teaming AI』(No Starch, 2027년 봄 예정)는 'AI Kill Graph'를 따라 정찰부터 추출까지 이어 가고, 에이전트에는 7장 하나를 준다([No Starch](https://nostarch.com/node/829)). 에이전트 전용 책은 Huang·Hughes의 『Securing AI Agents』(Springer, 2025-10)뿐이다. 페이지에 장 제목은 없고, 설명에 신원 보안과 다중 에이전트 통신이 강조되어 있다([Springer](https://link.springer.com/book/10.1007/978-3-032-02130-4)).

확인한 목차 가운데 쿠버네티스·egress·샌드박스 장을 둔 책은 하나도 없다. 에이전트 사고 대응 장도 없다. 플랫폼 관점에 가장 가까운 것은 SANS SEC545다. GIAC 자격 이름부터 'AI Platform Security'이고, MCP·OAuth 실습과 호스팅·파이프라인 모듈이 있다. 그러나 쿠버네티스는 CTF 환경으로만 나오고, 호스팅은 AWS Bedrock·SageMaker 위주다([SANS](https://www.sans.org/cyber-security-courses/genai-llm-application-security-5day)). 쿠버네티스 네이티브 통제 설계서는 SEC545와 겹치지 않고 보완한다. 한국어 쪽에서 확인한 AI 보안서는 『완벽한 바이브 코딩을 위한 보안 플레이북』(2026-06) 하나다. 입문자 대상의 AI 생성 코드·프롬프트 방어서이고, 에이전트·인프라는 마지막 부의 몇 장에 그친다([교보 eBook](https://ebook-product.kyobobook.co.kr/dig/epd/ebook/E000013194494)). 다만 Wilson·Sotiropoulos의 한국어 번역판이 있는지는 확인하지 못했다. 한빛·에이콘 카탈로그를 직접 확인하기 전에는 "번역서 없음"이라고 쓰면 안 된다.

이 갈래에서 빌려 올 관례도 있다. 이야기형 사례로 여는 서장(Wilson 1장), 앞쪽에 둔 신뢰 경계 장(Wilson 3장, Malik 외 4장), 초반에 까는 실습 환경(Sotiropoulos 2장 'Adversarial Playground')이다. v1은 이 셋을 받아들인다. 다만 실습 환경은 공격 놀이터가 아니다. kind/minikube 위에 작은 에이전트 플랫폼을 띄우고, 장마다 통제를 하나씩 더하는 누적형으로 만든다.

### 5×6 크로스워크: 네트워크 열은 모든 행에서 비었고, KB는 에이전트 런타임에 몰려 있다

프레임워크 노트는 OWASP(LLM 2025·Agentic 2026·AI Exchange), NIST(AI 100-2 E2025·AI RMF·600-1·SP 800-218A·IR 8596·COSAIS·NCCoE), MITRE ATLAS, CSA(MAESTRO·AICM), Google SAIF, CoSAI, Databricks DASF, 한국 법·지침을 책의 두 축에 겹쳤다. 아래 표에서 **앞 기호는 프레임워크가 구체적으로 다루는 정도**를 뜻한다(● 여러 프레임워크가 구체적, ◐ 얇음, ○ 찾지 못함. 연구자의 종합 판단이며 공표된 크로스워크가 아니다). **뒤 숫자는 현재 KB 항목 수**다(20건 front matter 기준).

| 생명주기 ＼ 통제 | 신원·권한 | 네트워크·egress | 격리·실행 환경 | 공급망·출처 | 탐지·평가 | 거버넌스·정책 |
|---|---|---|---|---|---|---|
| 데이터 | ◐ / 1 | ○ / 1 | ○ / 0 | ● / 0 | ◐ / 0 | ● / 1 |
| 학습·튜닝 | ◐ / 0 | ○ / 1 | ○ / 1 | ● / 0 | ● / 1 | ● / 0 |
| 서빙·추론 | ◐ / 3 | ◐ / 0 | ◐ / 1 | ◐ / 1 | ● / 5 | ● / 3 |
| 에이전트 런타임 | ● / 9 | ◐ / 6 | ◐→● / 7 | ◐ / 0 | ● / 10 | ◐ / 2 |
| 공급망·배포 | ○ / 4 | ○ / 3 | ◐ / 2 | ● / 2 | ◐ / 2 | ● / 1 |

이 표에서 구조상 결론 세 가지가 나온다. 첫째, **네트워크 열이 가장 약하다**. egress를 AI용 통제 계열로 따로 다루는 프레임워크가 없다. 리스크 항목 안의 완화책, 'AI 게이트웨이', ATLAS의 '도구 호출을 통한 유출' 같은 공격 기술로만 나온다([ATLAS CHANGELOG](https://github.com/mitre-atlas/atlas-data/blob/main/CHANGELOG.md), [Databricks DASF v3.0](https://www.databricks.com/blog/agentic-ai-security-new-risks-and-controls-databricks-ai-security-framework-dasf-v30)). 둘째, **신원은 에이전트 런타임에서만 ●**이다. 학습 잡 ID, 모델 배포 주체, MCP 서버 등록 주체, CI/CD 자격 증명을 다루는 표준은 없다. 그런데 KB와 사건 노트는 공급망×신원 칸에서 실제 사고(Amazon Q의 과도한 범위 토큰, Ultralytics에 남은 PyPI 토큰, Nx의 npm 토큰 유출)를 여럿 보여 준다([AWS-2025-015](https://aws.amazon.com/security/security-bulletins/AWS-2025-015/), [PyPI](https://blog.pypi.org/posts/2024-12-11-ultralytics-attack-analysis/), [GHSA-cxm3-wv7p-598c](https://github.com/nrwl/nx/security/advisories/GHSA-cxm3-wv7p-598c)). 이 칸은 책이 플랫폼 관점으로 채울 자리다. 셋째, KB의 무게는 에이전트 런타임 행에 쏠려 있다. 데이터·학습 행은 거의 비어 있고, 에이전트 런타임×출처는 0건이다. 그래서 기초 문헌 수집은 데이터·학습·출처 칸부터 채워야 한다(6절).

표준 체계가 생명주기를 부르는 방식은 2부 각 장 도입부에 '표준이 이 단계를 어떻게 부르나' 상자로 넣는다. NIST AI 100-2 E2025는 학습 시점과 배포 시점의 이분법을 쓴다([NIST AI 100-2 E2025](https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-2e2025.pdf)). OWASP AI Exchange는 개발 시점, 입력, 런타임 일반 보안의 3분법이다([OWASP AI Exchange](https://owaspai.org/)). MAESTRO는 7계층이고, 그중 'Deployment and Infrastructure'(L4)를 독립 계층으로 둔 유일한 프레임워크다([CSA](https://cloudsecurityalliance.org/blog/2025/02/06/agentic-ai-threat-modeling-framework-maestro)). 책의 5단계는 NIST의 두 단계를 세분한 것으로 소개할 수 있다(학습 시점 → 데이터·학습, 배포 시점 → 서빙·런타임·공급망). 감사 가능한 통제 카탈로그로는 CSA AICM v1.1(247개 통제)이 가장 크다. 통제 열이 감사 통제와 대응한다는 근거로 쓴다([CSA Labs](https://labs.cloudsecurityalliance.org/research/csa-research-note-aicm-v1-1-update-20260730-csa-styled/)). 격리와 출처 메커니즘을 '통제'로 직접 명명하는 곳은 DASF v3.0(샌드박싱 34/62, AI 게이트웨이 54)과 CoSAI(모델 서명 성숙도 3단계)뿐이다. 그래서 이 둘이 12·13장의 가장 강한 외부 근거다([OASIS](https://www.oasis-open.org/2025/11/18/coalition-for-secure-ai-releases-two-actionable-frameworks-for-ai-model-signing-and-incident-response)). 반면 NIST의 에이전트 전용 통제는 모두 확정 전이다. COSAIS 에이전트 오버레이는 계획 단계이고, NCCoE 에이전트 신원은 개념 문서 단계다([NCCoE](https://www.nccoe.nist.gov/projects/software-and-ai-agent-identity-and-authorization)). 책은 이 영역에서 표준보다 앞서 갈 수 있다. 대신 "예상되는 오버레이에 대비한 설계"라고 틀을 밝혀야 한다.

### 통제 기술의 성숙도: 3부는 이제 '설계'를 가르칠 수 있다

플랫폼 통제 노트는 성숙을 엄격하게 정의했다. CNCF Graduated, RFC, MUST 요건이 있는 공개 스펙, 안정 선언된 API 중 하나여야 성숙이다. 이 기준으로 성숙에 드는 것은 SPIFFE/SPIRE·OPA·Cilium·Falco·OpenTelemetry(모두 CNCF Graduated), 쿠버네티스 Pod Certificates(KEP-4317, v1.37 stable), MCP 인가의 MUST 요건, SLSA 1.2, CycloneDX 1.7(ECMA-424), OMS/Sigstore 모델 서명, safetensors, Agent Router 1.x API다([CNCF](https://www.cncf.io/projects/), [KEP-4317](https://www.kubernetes.dev/resources/keps/4317/), [MCP Authorization](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization), [SLSA v1.2](https://slsa.dev/blog/2025/11/announce-slsa-v1.2)). 부상으로 분류된 것은 agent-sandbox, OTel GenAI 규약, ID-JAG·Transaction Tokens, WIMSE-AIMS, NPEP-133, MCP 게이트웨이, Prempti, 기밀 GPU다. agent-sandbox는 v1beta1이고 1.0.x에서도 breaking change가 있다. OTel GenAI 규약은 모든 `gen_ai.*`가 Development 상태다. ID-JAG·Transaction Tokens는 초안, WIMSE-AIMS는 -00, NPEP-133은 v1alpha2다. 기밀 GPU는 좁은 범위의 GA다([agent-sandbox](https://github.com/kubernetes-sigs/agent-sandbox), [WIMSE](https://datatracker.ietf.org/wg/wimse/documents/), [NVIDIA CoCo 1.0.0](https://docs.nvidia.com/datacenter/cloud-native/confidential-containers/1.0.0/release-notes.html)). 연구 단계는 CaMeL과 인젝션 방어 설계 패턴, 그리고 분류기의 견고성 주장이다([arXiv 2503.18813](https://arxiv.org/abs/2503.18813), [arXiv 2506.08837](https://arxiv.org/abs/2506.08837)).

이 지형은 목차를 세 가지로 바꾼다. 첫째, 9~13장의 뼈대(워크로드 ID → audience 바인딩 → 토큰 교환 → 정책 엔진, egress 허용 목록 → L7 게이트웨이, 런타임 사다리 → 샌드박스 CRD, 서명 → SLSA → AI-BOM)는 성숙한 부품으로 세울 수 있다. 부상 기술은 절 단위 라벨로 구분하면 된다. 둘째, MCP는 약 1년 사이 세 번 크게 바뀌었다. 2026-07-28 개정에서는 프로토콜이 무상태로 바뀌고 DCR이 폐기 예정이 됐다([MCP changelog](https://modelcontextprotocol.io/specification/2026-07-28/changelog)). 그래서 본문은 audience 바인딩·범위 최소화·issuer 검증 같은 원리와 현재 개정판의 MUST 요건만 다룬다. 메시지 형식은 KB와 연동한 온라인 부록으로 보낸다. 셋째, 모델·도구 트래픽 게이트웨이는 신원·네트워크·탐지가 한 지점에 모이는 곳이다. 1.0을 넘었고, 그 자체가 침해 대상이 된 사례도 있다(LiteLLM 1.82.7/1.82.8, 2026-03-24). 그래서 독립 장으로 세울 근거가 충분하다([LiteLLM](https://docs.litellm.ai/blog/security-update-march-2026)).

### 사고 근거는 서빙·공급망에 두껍고, 데이터·학습에서는 연구에 기댄다

사건 노트는 각 장이 어떤 근거 유형에 기대는지 정리했다. **서빙과 공급망은 실사고만으로 논증할 수 있다.** 서빙 쪽에는 LLMjacking(최악의 경우 하루 4.6만 달러 이상), Storm-2139의 Azure OpenAI 접근 재판매, Anthropic이 공개한 약 24,000개 계정·1,600만 건 이상의 증류 캠페인이 있다([Sysdig](https://sysdig.com/blog/llmjacking-stolen-cloud-credentials-used-in-new-ai-attack/), [Microsoft](https://blogs.microsoft.com/on-the-issues/2025/02/27/disrupting-cybercrime-abusing-gen-ai/), [Anthropic](https://www.anthropic.com/news/detecting-and-preventing-distillation-attacks)). 공급망 쪽에는 Hugging Face 악성 모델(JFrog 약 100개, nullifAI의 스캐너 우회), CI 결함으로 뚫린 Ultralytics·Nx, 첫 악성 MCP 서버 postmark-mcp, Salesloft Drift OAuth 토큰 탈취가 있다([JFrog](https://jfrog.com/blog/data-scientists-targeted-by-malicious-hugging-face-ml-models-with-silent-backdoor/), [Wiz](https://www.wiz.io/blog/s1ngularity-supply-chain-attack), [Google GTIG](https://cloud.google.com/blog/topics/threat-intelligence/data-theft-salesforce-instances-via-salesloft-drift)). **에이전트 런타임**은 운영 제품에서 공개된 취약점(GitHub MCP, Supabase MCP, EchoLeak)과 일부 실사고(Replit 운영 DB 삭제)로 충분하다. KB에도 이미 이 행이 가장 두껍다. **데이터** 단계의 실사고는 대부분 '노출'이다(Microsoft 38TB SAS 토큰, DeepSeek ClickHouse, KB의 Vibetech). '오염'은 연구로 논증한다. 오염 연구는 '가능하다'에서 '싸고 모델 크기와 무관하다'로 옮겨 왔다. 문서 약 250개로 600M~13B 모델에 백도어를 심었고, 성공은 비율이 아니라 절대 개수에 달려 있었다([Anthropic](https://www.anthropic.com/research/small-samples-poison)). **학습** 단계에는 강한 실사고가 한 계열 있다. ShadowRay(2023-09부터 악용, 2025-11 자기 전파형 2.0)다. 나머지는 연구소 내부 사건과 연구다. o1-preview가 잘못 노출된 Docker API로 평가 환경을 우회한 사례, 실제 Claude RL 환경의 보상 해킹, Sleeper Agents가 여기에 든다([Oligo](https://www.oligo.security/blog/shadowray-attack-ai-workloads-actively-exploited-in-the-wild), [OpenAI](https://cdn.openai.com/o1-preview-system-card-20240917.pdf), [Anthropic](https://www.anthropic.com/research/emergent-misalignment-reward-hacking)).

이 분포에서 2부 구조가 두 가지로 바뀐다. 하나는 근거가 강한 장을 앞에 두는 것이다. 다른 하나는 장 안을 통제 성격이 다른 두 갈래로 나누는 것이다. 서빙은 '오남용'과 '자원·자산 탈취', 학습은 '학습 인프라'와 '평가·RL 환경 격리', 공급망은 '아티팩트'와 '서드파티 연동 토큰', 데이터는 '노출'과 '오염'으로 나눈다. 사건 노트에는 통제 축에 대한 관찰도 있다. **모든 단계에서 가장 자주 실패한 통제는 신원**(장수명 토큰, 과도한 범위, 무인증 엔드포인트)이다. 플랫폼 엔지니어에게 가장 설득력 있는 피해 지표도 모델 피해가 아니라 **탈취된 자격 증명과 컴퓨트**다. 3부를 신원으로 시작하는 결정은 독자 수요뿐 아니라 사고 분포로도 뒷받침된다.

### 독자는 '누가 무엇에 닿고, 누가 보고 있나'를 묻는다. 한국 독자는 데이터 유출과 규제를 묻는다

설문들은 같은 그림을 보여 준다. CSA 설문(n=228)에서 가장 큰 우려는 과잉 권한(24%)과 행동 가시성 부족(19%)이었다. 에이전트 신원으로는 공유·일반 서비스 계정(43%)과 사람 사용자 신원(31%)이 섞여 쓰인다. 에이전트 하나에 인증을 붙이는 데 1~10일이 든다는 응답은 43%였다([Help Net Security](https://helpnetsecurity.com/2026/03/26/ciso-ai-agent-identity-security-report/)). Gravitee 조사(750명)에서 모니터링·보안이 적용된 에이전트는 평균 약 52%였는데, 가시성이 있다는 자신감은 91.8%였다. 접근 일시 중지·회수 절차를 문서로 갖춘 곳은 34.1%다([Gravitee](https://www.gravitee.io/state-of-ai-agent-security?hl=cs-CZ)). CNCF 조사에서는 66%가 쿠버네티스에서 생성형 AI 워크로드를 운영하고, 52%는 모델을 만들거나 학습하지 않는다([CNCF](https://www.linuxfoundation.org/hubfs/Research%20Reports/CNCF_Annual_Survey_Report_1.15.26.pdf?hsLang=en)). KubeCon NA 2026은 운영 중심의 'AI Inference + Agentic' 트랙을 새로 만들었다. 보안 트랙은 여전히 공급망·신원·런타임·멀티테넌시·정책 집행이라는 기존 어휘를 쓴다([CNCF 발표](https://www.cncf.io/announcements/2026/08/10/cncf-reveals-kubecon-cloudnativecon-north-america-2026-schedule-adds-new-ai-inference-agentic-track/)). 이 책의 통제 계층 어휘가 독자의 기존 어휘와 맞는다는 근거다.

한국 독자에게는 세 가지가 더 필요하다. 첫째는 데이터 유출 우려다. 국내 조사 두 건에서 보안·개인정보 유출 우려가 53.3%와 64.5%로 나왔다([파이낸셜뉴스](https://www.fnnews.com/news/202508260933530786), [바이라인네트워크](https://byline.network/2025/02/5-261/)). 둘째는 금융권 망분리 완화다. 2024-08-13 로드맵 이후 규제샌드박스로 외부 생성형 AI를 쓸 수 있게 됐고, 가명처리·해외 사업자 계약 조항·단말 추적성이 조건으로 붙었다([세종](https://shinkim.com/kor/media/newsletter/2533)). 셋째는 인공지능 기본법과 금융 지침이다. 기본법(2026-01-22 시행)에는 고지·표시, 고영향 AI 위험관리, 사람의 관리·감독, 문서 5년 보관이 들어 있고, 과태료는 1년 이상 유예된다([세종](https://shinkim.com/kor/media/newsletter/3114)). 금융위 가이드라인은 비상 정지 기능을 의무화했다([노컷뉴스](https://www.nocutnews.co.kr/news/6534884)). 금융보안원의 에이전트 보안 평가기준(안)은 17개 항목으로 실행 권한·격리, 도구 승인, 자율 실행 제한·중단 가능성을 본다([파이낸셜뉴스](https://www.fnnews.com/news/202610071821048238)). 이 요구들은 플랫폼 쪽으로 오면 감사 로그 보존, 승인 게이트, 비상 정지, 서빙 출력 표시 파이프라인으로 번역된다. 영어권 책에는 없는 장면이다. 국내 실사고도 KB에 이미 있다. 자율 침투 도구 ARTEX가 한국 금융권 공격에 쓰였고, 당국 집계로 16곳·약 10만 건이 유출됐다(AISEC-2026-0001). 독자 수요 노트는 "1차 출처 기준 국내 AI 보안 사고를 찾지 못했다"고 적었지만, 이 항목이 그 공백을 메운다.

---

## 3. 제안 목차 v1

**가제**: 『에이전트 시대의 AI 보안 — 플랫폼 엔지니어를 위한 통제 설계』 (유지)

**구성**: 4부 19장 + 부록. 2부 각 장은 '공격 표면 지도'다. 사례와 동작 원리는 깊게 쓰고, '통제 설계' 절은 짧게 둔다. 해당 3부 장으로 넘기는 교차 참조가 그 절의 역할이다. 3부 각 장은 통제 설계 절이 본문의 절반 이상을 차지한다. 기술 절 라벨: **성숙**(Graduated·RFC·MUST·stable API), **부상**(1.0 전후·초안·Development), **실험**(연구·early-stage).

### 1부. 왜 AI 보안은 인프라 문제인가

#### 1장. 프롬프트 인젝션은 고칠 버그가 아니라 상시 위험이다 — 그래서 폭발 반경을 설계한다

**논지**: 명령과 데이터가 한 채널을 쓰는 한 인젝션은 사라지지 않는다. 그러니 물어야 할 것은 "조작된 에이전트가 무엇에 닿고, 무엇을 들고 나갈 수 있나"다. 장은 한국 독자의 첫 우려인 데이터 유출 경로로 열고, 인젝션은 '왜 막을 수 없나'의 원인으로 설명한다.

**핵심 질문**: 에이전트가 닿는 내부 API·SaaS·클라우드·CI/CD 가운데 무엇이 유출 경로가 되나? 공격 성공률이 낮다는 평가는 무엇을 숨기나? 프롬프트 안의 방어는 왜 통제가 아닌가?

**여는 사례**: ① Slack AI 간접 인젝션(2024-08-14~19). 공개 채널에 심은 지시가 비공개 채널의 API 키를 피싱 링크에 실어 내보냈다. Slack은 "의도된 동작"이라고 답했다 [공개 취약점] ([PromptArmor](https://www.promptarmor.com/resources/data-exfiltration-from-slack-ai-via-indirect-prompt-injection)) ② GitHub MCP 'toxic agent flow'(2025-05-26). 공개 저장소의 이슈 하나가 비공개 저장소 데이터를 공개 PR로 빼냈고, 연구자들은 서버 코드가 아니라 아키텍처의 결함이라고 결론지었다 [공개 취약점] ([Invariant Labs](https://invariantlabs.ai/blog/mcp-github-vulnerability)) ③ EchoLeak CVE-2025-32711(NVD 2025-06-11, M365 Copilot) [공개 취약점] ([NVD](https://nvd.nist.gov/vuln/detail/CVE-2025-32711))

**리더 요약 수치 후보**: 에이전트가 닿는 곳은 내부 앱·API 56%, SaaS 49%, 클라우드 인프라 44%, CI/CD 35%다. 81%가 프롬프트 조작으로 자격 증명이 노출될 수 있다고 본다([Help Net Security](https://helpnetsecurity.com/2026/03/26/ciso-ai-agent-identity-security-report/)).

**절 구성**: ① 에이전트가 닿는 곳: 유출의 세 경로(검색 범위, 도구 권한, 밖으로 나가는 출력) ② 왜 막을 수 없나: 명령·데이터 단일 채널과 직접·간접 인젝션(AI 100-2 §3.3–3.4, LLM01, ASI01) ③ 공격 성공률이 숨기는 것: '거부'와 '무시'의 차이, 적응형 공격(14장 예고) ④ 폭발 반경 = 신원 × egress × 격리: 3부 지도 ⑤ 상시 위험으로 등록하기: 패치가 아니라 범위·가격으로 관리한다(15장 예고)

**축 매핑**: lifecycle `agent-runtime`, `serving`, `data` / controls `identity`, `network`, `isolation`, `governance`

**기존 KB 항목**: AISEC-2026-0005, 0020, 0004, 0002, 0010

**외부 근거**: [NIST AI 100-2 E2025](https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-2e2025.pdf), [OWASP LLM Top 10](https://genai.owasp.org/llm-top-10/), [arXiv 2510.09023](https://arxiv.org/abs/2510.09023)

**근거 수준**: 충분

#### 2장. 공격자도 에이전트를 쓴다 — 위협 환경

**논지**: 성공률이 10%여도 시도 비용이 0에 가까우면 공격은 규모의 게임이 된다. 공격자에게는 모델 API도 인프라다. 그래서 패치 주기와 노출 관리의 전제가 바뀌고, 모델 API로 나가는 egress도 탐지 신호가 된다.

**핵심 질문**: 자율 침투 도구는 공격의 경제학을 어떻게 바꿨나? 위협 행위자의 모델 사용은 방어 쪽 로그 어디에 흔적을 남기나? 벤더 위협 보고서는 단일 출처라는 한계가 있다. 이 한계를 어떻게 다뤄야 하나?

**여는 사례**: ① ARTEX. 한국 금융권 공격(9월 말~10월 초)에 이어 일본 기업 공격에서도 확인됐다 [실사고] (AISEC-2026-0001) ② Anthropic이 2025-11-13에 공개한 AI 주도 첩보 캠페인. 약 30개 표적, 전술 작업의 80~90%를 AI가 수행했다 [실사고] ([Anthropic](https://www.anthropic.com/news/disrupting-AI-espionage)) ③ Google GTIG의 PROMPTSTEAL(2025-11-05). 실제 작전에서 LLM에 질의한 첫 악성코드로, Hugging Face API로 명령을 생성했다 [실사고] ([Google GTIG](https://cloud.google.com/blog/topics/threat-intelligence/threat-actor-usage-of-ai-tools))

**절 구성**: ① 공격 경제학: 성공률보다 시도 비용(AISEC-2026-0013의 과업당 비용·소요 시간) ② 위협 행위자의 모델 사용: 갈취(2025-08), 첩보(2025-11), 모델을 C2처럼 쓰는 악성코드 ③ 노출된 에이전트 제어판: 공격 인프라 자체의 운영 실패 ④ 방어 쪽 함의: 노출 관리 주기, 모델 API로 나가는 egress 신호(11·14장 예고) ⑤ 근거 읽는 법: 벤더 위협 보고서는 자사 모델의 오남용만 보는 단일 출처다

**축 매핑**: lifecycle `agent-runtime`, `serving` / controls `detection`, `network`, `governance`

**기존 KB 항목**: AISEC-2026-0001, 0013 (둘 다 심층 후보)

**외부 근거**: [Anthropic 2025-08](https://www.anthropic.com/news/detecting-countering-misuse-aug-2025), [Anthropic 2025-11](https://www.anthropic.com/news/disrupting-AI-espionage), [Google GTIG](https://cloud.google.com/blog/topics/threat-intelligence/threat-actor-usage-of-ai-tools)

**근거 수준**: 충분 (단, 대부분 벤더 단일 출처)

#### 3장. AI 플랫폼 참조 아키텍처와 신뢰 경계 (신설)

**논지**: 쿠버네티스 위 AI 플랫폼은 모델 서빙, AI 게이트웨이, MCP 서버, 벡터 DB, 학습·평가 클러스터, CI/CD·레지스트리로 이뤄진다. 신뢰 경계는 이 구성 요소들 사이에 있다. 이 장이 그리는 지도가 2부(어디서 뚫리나)와 3부(무엇으로 막나)의 공통 좌표가 된다. 독자는 같은 지도 위에 실습 환경을 띄우고, 장마다 통제를 하나씩 더한다.

**핵심 질문**: 내 플랫폼에서 신뢰할 수 없는 입력은 어디로 들어와 어떤 자격 증명 옆을 지나가나? 표준들(NIST 2분법, AI Exchange 3분법, MAESTRO 7계층)은 이 지도와 어떻게 대응하나?

**여는 사례**: ① Hugging Face 공유 인프라(2024-04-04, Wiz). 악성 pickle 모델로 추론 서비스에서 RCE를 얻었다. 이어서 IMDS를 통해 노드 역할, EKS 시크릿을 차례로 얻었다. Spaces Dockerfile의 `RUN`으로는 공유 내부 레지스트리에 푸시해 다른 테넌트의 이미지를 덮어쓸 수 있었다. 신뢰 경계 다섯 개를 연달아 넘은 사례다 [공개 취약점] ([Wiz](https://www.wiz.io/blog/wiz-and-hugging-face-address-risks-to-ai-infrastructure))

**절 구성**: ① 참조 아키텍처: 구성 요소와 데이터·제어 흐름 ② 신뢰 경계 그리기: 입력·자격 증명·외부 호출의 교차점 ③ 표준 대응표: AI 100-2(학습/배포 시점), AI Exchange(개발/입력/런타임), MAESTRO L1~L7 ↔ 책의 5단계·6통제 ④ 실습 환경: kind/minikube 위 작은 에이전트 플랫폼(모델 프록시, MCP 서버 1개, 벡터 DB, CI) — **성숙** ⑤ 이 책의 표기 규칙: 근거 유형, 성숙도 라벨, OWASP·ATLAS ID

**축 매핑**: lifecycle 전 단계 / controls 전 계층(지도)

**기존 KB 항목**: AISEC-2026-0004(에이전트 미들웨어 비중), 0010(OWASP 2026 매핑)

**외부 근거**: [CSA MAESTRO](https://cloudsecurityalliance.org/blog/2025/02/06/agentic-ai-threat-modeling-framework-maestro), [OWASP AI Exchange](https://owaspai.org/), [NIST AI 100-2 E2025](https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-2e2025.pdf), [SAIF Focus on Agents](https://saif.google/focus-on-agents)

**근거 수준**: 보통 (KB 직접 항목 없음. 표준·사례는 충분)

### 2부. 생명주기로 보는 공격 표면

#### 4장. 서빙·추론 — 모델 엔드포인트는 과금되는 공개 서비스다

**논지**: 유출된 API 키는 곧 비용 책임이고 오남용 통로다. 자체 호스팅 추론 서버는 '기본값 무인증 + 네트워크 노출'이라는 같은 패턴으로 반복해서 뚫린다. 추론 최적화 옵션도 보안 변수다.

**핵심 질문**: 모델 API 키 하나가 새면 하루에 얼마가 나가나? 탈옥·오남용과 키 도용·증류·추출은 통제가 어떻게 다른가? 자체 호스팅 Ollama·vLLM 앞에 무엇을 세워야 하나?

**여는 사례**: ① LLMjacking(2024-05-06, Sysdig). 도용한 클라우드 자격 증명으로 Bedrock의 Claude를 호출했다. 공격자는 호출 로깅 설정이 켜져 있는지부터 확인했다. 최악의 경우 하루 4.6만 달러 이상이 든다 [실사고] ([Sysdig](https://sysdig.com/blog/llmjacking-stolen-cloud-credentials-used-in-new-ai-attack/)) ② Anthropic 증류 캠페인(2026-02-23). 약 24,000개 계정으로 1,600만 건 이상을 교환했다 [실사고] ([Anthropic](https://www.anthropic.com/news/detecting-and-preventing-distillation-attacks)) ③ 무인증 Ollama의 대량 노출(Cisco 2025-09-01: 1,139대 중 214대가 인증 없이 서빙)과 vLLM CVE-2026-22778(CVSS 9.8, 기본 설치에 인증 없음) [공개 취약점] ([Cisco](https://blogs.cisco.com/security/detecting-exposed-llm-servers-shodan-case-study-on-ollama), [GitLab advisory](https://advisories.gitlab.com/pypi/vllm/CVE-2026-22778/))

**절 구성**: ① 표준 상자: LLM10·SAIF Model Exfiltration·ATLAS Cost Harvesting ② 오남용: 탈옥·위협 행위자 사용, 가드레일 우회(Storm-2139) ③ 자원·자산 탈취: 키 도용, 증류(대량 질의)와 파라미터 추출(Carlini 2024)의 구분 ④ 자체 호스팅 서빙 하드닝: 인터넷 비노출, 앞단 인증 프록시, 최소 API 표면, 빠른 패치(Ollama·vLLM CVE) — **성숙** ⑤ 추론 최적화·출력 처리도 보안 변수: 조기 종료와 탈옥 내성, 규제 요건이 서빙 출력 단계로 내려오는 경우(워터마크) — **부상** ⑥ 통제 지도: → 9장(키·계정), 10장(게이트웨이·쿼터), 14장(호출 로깅)

**축 매핑**: lifecycle `serving` (보조 `supply-chain`) / controls `identity`, `detection`, `network`, `governance`

**기존 KB 항목**: AISEC-2026-0016, 0006, 0009, 0005 (0007은 미확인이라 인용하지 않는다)

**외부 근거**: [Microsoft Storm-2139](https://blogs.microsoft.com/on-the-issues/2025/02/27/disrupting-cybercrime-abusing-gen-ai/), [arXiv 2403.06634](https://arxiv.org/abs/2403.06634), [Wiz Probllama](https://www.wiz.io/blog/probllama-ollama-vulnerability-cve-2024-37032), [CNCF KServe](https://www.cncf.io/projects/kserve/)

**근거 수준**: 충분

#### 5장. 에이전트 런타임 — 신뢰할 수 없는 입력, 과도한 권한, 밖으로 나가는 통로

**논지**: 에이전트 사고의 공통 원인은 세 가지가 한자리에 있는 것이다. 신뢰할 수 없는 콘텐츠가 들어오고, 범위가 넓은 자격 증명을 쥐고 있고, 밖으로 나가는 채널이 있다. 미리보기·설정 필드 같은 부가 기능도 실행 경로다. KB 근거가 가장 두꺼운 장이므로 사례를 늘리기보다 이 패턴으로 묶는다.

**핵심 질문**: MCP 서버 등록과 stdio 설정은 왜 임의 명령 실행 권한과 같은가? 벤더가 "취약점 아님"이라고 판정하면 그 위험은 누가 지나? 입구가 아니라 싱크에서 검증한다는 말은 무슨 뜻인가?

**여는 사례**: ① Replit 에이전트의 운영 DB 삭제(2025-07-22 보도). 코드 동결 지시가 있던 중 임원 1,206명과 1,196개 이상 회사의 기록을 지웠다. 이후 개발·운영 DB 분리와 계획 전용 모드가 추가됐다 [실사고] ([eWeek](https://www.eweek.com/news/replit-ai-coding-assistant-failure/)) ② Supabase MCP(2025-07-08). RLS를 우회하는 `service_role`로 돌던 Cursor가 지원 티켓 속 지시를 읽고 토큰을 덤프했다 [연구, 실제 제품 대상 시연] ([General Analysis](https://generalanalysis.com/blog/supabase-mcp-blog)) ③ Langflow MCP stdio 설정 필드 RCE. 실제로 악용 중이다 [실사고] (AISEC-2026-0014)

**절 구성**: ① 표준 상자: ASI01~10, SAIF 에이전트 구성요소(인지·추론·오케스트레이션·응답 렌더링) ② 공통 패턴: 입력 × 권한 × 출구 ③ MCP와 도구 호출: 등록=권한 부여, stdio=명령 실행, 서버가 알려 주는 인증 위치 ④ 코딩·CI 에이전트: 비밀 값과 도구를 쥐고 PR 제목·이슈를 읽는 구조 ⑤ 부가 기능이 실행 경로가 될 때: 미리보기·렌더링 ⑥ 통제 지도: → 9장(최소 권한), 11장(egress), 12장(격리·비상 정지), 14장(행동 순서 탐지)

**축 매핑**: lifecycle `agent-runtime` / controls `identity`, `isolation`, `network`, `detection`

**기존 KB 항목**: AISEC-2026-0002, 0003, 0011, 0013, 0014, 0015, 0017, 0018, 0020

**외부 근거**: [Invariant Labs](https://invariantlabs.ai/blog/mcp-github-vulnerability), [NVD CVE-2025-32711](https://nvd.nist.gov/vuln/detail/CVE-2025-32711), [OWASP Agentic Top 10 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/), [Databricks DASF v3.0](https://www.databricks.com/blog/agentic-ai-security-new-risks-and-controls-databricks-ai-security-framework-dasf-v30)

**근거 수준**: 충분

#### 6장. 공급망·배포 — 모델·패키지·MCP 서버는 코드이고, 연동은 토큰이다

**논지**: 모델은 가중치 파일이 아니라 '로더와 README가 딸린 패키지'다. AI 라이브러리는 평범한 패키지처럼 CI 설정 결함으로 뚫린다. 서드파티 AI·SaaS 연동은 OAuth 토큰 공급망이다. 앞의 두 갈래(아티팩트)에서 실패하는 통제는 출처·격리이고, 뒤의 갈래(연동)에서 실패하는 통제는 신원(토큰 범위·수명)이다.

**핵심 질문**: 다운로드 수와 트렌딩 순위는 신뢰 신호가 될 수 있나? 개발자 PC의 AI CLI는 왜 공격자의 정찰 엔진이 되나? 조달 배제 명령 하나에 어떤 목록이 필요해지나?

**여는 사례**: ① Nx 's1ngularity'(2025-08-26). `pull_request_target` 워크플로 결함으로 npm 토큰을 빼앗긴 뒤 악성 버전이 배포됐다. 악성 버전은 피해자 PC의 Claude·Gemini·Amazon Q CLI를 권한 확인 우회 플래그로 실행해 정찰에 썼다. 결과는 GitHub 토큰 1,000개 이상, 공개로 바뀐 저장소 5,500개 이상이다 [실사고] ([GHSA](https://github.com/nrwl/nx/security/advisories/GHSA-cxm3-wv7p-598c), [Wiz](https://www.wiz.io/blog/s1ngularity-supply-chain-attack)) ② Hugging Face 악성 모델. JFrog가 2024-02-27에 약 100개를 보고했고, nullifAI는 망가진 pickle로 스캐너를 우회했다. KB에는 24만 회 다운로드된 사례도 있다 [실사고] ([JFrog](https://jfrog.com/blog/data-scientists-targeted-by-malicious-hugging-face-ml-models-with-silent-backdoor/), [ReversingLabs](https://www.reversinglabs.com/blog/rl-identifies-malware-ml-model-hosted-on-hugging-face)) ③ Salesloft Drift OAuth 토큰 탈취(2025-08-08~18). 탈취한 토큰으로 Salesforce 데이터를 대량으로 내보낸 뒤 AWS 키를 찾았다 [실사고] ([Google GTIG](https://cloud.google.com/blog/topics/threat-intelligence/data-theft-salesforce-instances-via-salesloft-drift))

**절 구성**: ① 표준 상자: LLM03·ASI04·SAIF·ATLAS의 rug pull·reputation inflation ② 아티팩트 공급망 A: 모델 허브와 직렬화(pickle, 스캐너 우회) ③ 아티팩트 공급망 B: AI 패키지·확장·MCP 서버(Ultralytics, Amazon Q, postmark-mcp, LiteLLM) ④ 서드파티 AI·SaaS 연동 공급망: Drift, Mixpanel→OpenAI, HF Spaces 시크릿, 서드파티 도구에 맡긴 공급자 키 ⑤ 슬롭스쿼팅: 연구로만 측정된 위험 ⑥ 통제 지도: → 13장(서명·AI-BOM·로더), 9장(연동 토큰), 12장(로딩 격리)

**축 매핑**: lifecycle `supply-chain` / controls `provenance`, `identity`, `isolation`, `network`

**기존 KB 항목**: AISEC-2026-0012, 0019, 0016, 0003, 0011, 0004

**외부 근거**: [PyPI Ultralytics](https://blog.pypi.org/posts/2024-12-11-ultralytics-attack-analysis/), [AWS-2025-015](https://aws.amazon.com/security/security-bulletins/AWS-2025-015/), [THN postmark-mcp](https://thehackernews.com/2025/09/first-malicious-mcp-server-found.html), [OpenAI Mixpanel](https://openai.com/index/mixpanel-incident/), [arXiv 2406.10279](https://arxiv.org/abs/2406.10279)

**근거 수준**: 충분

#### 7장. 데이터 — 노출은 사고로, 오염은 연구로

**논지**: 데이터 단계의 실제 사고는 대부분 '노출'이다. 범위가 넓은 공유 토큰, 무인증 저장소, 옛 유출을 한곳에 모은 집적지가 그 예다. '오염'은 싸고 모델 크기와 무관하다는 연구가 쌓였다. 추론 로그와 채팅 기록 저장소도 이 단계의 데이터 레이크다.

**핵심 질문**: 코퍼스가 클수록 오염이 희석되나? 그렇지 않다면 무엇을 출처 단위로 관리해야 하나? 사내 데이터가 외부 모델로 새는 경로(섀도 AI)는 어디서 보이나?

**여는 사례**: ① Microsoft AI 연구팀 38TB 노출(2023-09-18 공개). 저장소 계정 전체에 '전체 제어' 권한을 준 SAS 토큰이었고, 만료일은 2051년으로 늘어나 있었다. 쓰기 권한까지 있어 모델 파일을 덮어쓸 수도 있었다 [실사고] ([Wiz](https://www.wiz.io/blog/38-terabytes-of-private-data-accidentally-exposed-by-microsoft-ai-researchers)) ② DeepSeek ClickHouse 무인증 노출(2025-01-29). 채팅 기록과 API 키가 담긴 로그가 100만 줄 이상이었다 [실사고] ([Wiz](https://www.wiz.io/blog/wiz-research-uncovers-exposed-deepseek-database-leak)) ③ 문서 약 250개로 600M~13B 모델에 백도어를 심은 연구(2025-10-09) [연구] ([Anthropic](https://www.anthropic.com/research/small-samples-poison))

**절 구성**: ① 표준 상자: AI 100-2 §3.2, LLM04·LLM08, SAIF Training Data Management, MAESTRO L2 ② 데이터 노출: 학습 데이터·로그·채팅 기록 저장소, 공유 토큰 ③ 데이터 오염: 웹 규모 코퍼스(Carlini 2023), RAG(PoisonedRAG), 고정 개수 백도어, 실제 세계의 다리(Pravda 'LLM grooming') ④ 수집 단계 위생: 코퍼스 속 시크릿(Common Crawl에서 살아 있는 키 11,908개), URL 데이터셋 해시 검증 — **성숙** ⑤ 섀도 AI: 사내 데이터가 외부 모델로 새는 경로와 탐지(11장 egress와 연결) ⑥ 통제 지도: → 13장(데이터 계보), 9장(검색 권한), 11장

**축 매핑**: lifecycle `data` / controls `provenance`, `identity`, `network`, `detection`, `governance`

**기존 KB 항목**: AISEC-2026-0008 (1건뿐. 기초 문헌 수집 1순위)

**외부 근거**: [arXiv 2302.10149](https://arxiv.org/abs/2302.10149), [arXiv 2402.07867](https://arxiv.org/abs/2402.07867), [Truffle Security](https://trufflesecurity.com/blog/research-finds-12-000-live-api-keys-and-passwords-in-deepseek-s-training-data), [NewsGuard](https://www.newsguardrealitycheck.com/p/a-well-funded-moscow-based-global), [TechRepublic (IBM 섀도 AI)](https://www.techrepublic.com/article/news-ai-breach-risks-rise-as-governance-lags/)

**근거 수준**: 보통 (운영 중인 RAG 코퍼스가 실제로 오염된 1차 보고는 찾지 못했다)

#### 8장. 학습·평가 인프라 — GPU 클러스터와 '훈련 중인 모델'이라는 공격자

**논지**: 학습 클러스터가 고가치 표적인 이유는 모델이 아니라 그 안에 있는 자격 증명과 GPU다. 또 하나의 위협 모델이 있다. 평가·RL 환경에서는 훈련 중인 모델이 실제 권한을 가진 행위자다. 채점기가 잡지 못한 행동은 몇 달 뒤에야 드러난다. 두 갈래는 통제가 다르다. 학습 인프라는 네트워크·신원, 평가 환경은 격리·탐지다.

**핵심 질문**: "취약점이 아니라 설계"라는 입장(disputed CVE)은 위험을 어떻게 몇 년씩 남겨 두나? 평가 샌드박스를 CTF 수준으로 격리해야 하는 이유는 무엇인가? 사후 평가로 백도어가 없음을 증명할 수 있나?

**여는 사례**: ① ShadowRay(CVE-2023-48022). 2023-09-05부터 악용됐고 Oligo가 2024-03-26에 공개했다. 인가 없는 Jobs API로 채굴기를 깔고 OpenAI·HF·클라우드 키와 쿠버네티스 API 접근을 빼앗았다. 2025-11에는 자기 전파형 2.0이 나왔다 [실사고] ([Oligo](https://www.oligo.security/blog/shadowray-attack-ai-workloads-actively-exploited-in-the-wild), [NVD](https://nvd.nist.gov/vuln/detail/CVE-2023-48022)) ② o1-preview(시스템 카드 2024-09-17 §4.2.1). 고장 난 CTF에서 nmap으로 잘못 노출된 Docker API를 찾아 플래그를 읽었다 [실사고, 연구소 내부] ([OpenAI](https://cdn.openai.com/o1-preview-system-card-20240917.pdf)) ③ 실제 Claude RL 환경의 보상 해킹이 오정렬로 일반화된 사례(2025-11-21). Claude Code 평가에서 안전 연구 코드를 12% 비율로 방해했다 [연구] ([Anthropic](https://www.anthropic.com/research/emergent-misalignment-reward-hacking))

**절 구성**: ① 표준 상자: AI 100-2(학습 시점), SSDF-A(SP 800-218A), SAIF Model Source Tampering ② 학습 인프라 보안: Ray 대시보드·Jobs API 노출, 인증 계층(Ray 2.52.0 토큰 인증) — **성숙** ③ GPU 노드 탈출과 공유: NVIDIA Container Toolkit CVE-2024-0132(≤1.16.1) — **성숙**(패치·CDI 모드) ④ 평가·RL 환경 격리: 훈련 중인 모델을 잠재적 공격자로 보기, 채점기 분리 — **부상** ⑤ 내부자·체크포인트 무결성과 백도어 지속성: ByteDance(부분 미확인), Sleeper Agents — **성숙**(서명) / **실험**(탐지) ⑥ 통제 지도: → 11장(학습 잡 egress), 12장(평가 하네스 격리), 9장(학습 잡 ID)

**축 매핑**: lifecycle `training` (보조 `agent-runtime`) / controls `network`, `identity`, `isolation`, `detection`, `provenance`

**기존 KB 항목**: AISEC-2026-0017 (심층 후보, 1건뿐)

**외부 근거**: [THN ShadowRay 2.0](https://thehackernews.com/2025/11/shadowray-20-exploits-unpatched-ray.html), [Dark Reading](https://www.darkreading.com/cyber-risk/shadowray-20-ai-clusters-crypto-botnets), [Wiz CVE-2024-0132](https://www.wiz.io/blog/wiz-research-critical-nvidia-ai-vulnerability), [arXiv 2401.05566](https://arxiv.org/abs/2401.05566), [The Register (ByteDance)](https://www.theregister.com/2024/10/22/bytedance_intern_messed_with_llm/)

**근거 수준**: 보통 (실사고 한 계열 + 연구소 내부 사건. 외부 공격자가 파인튜닝 파이프라인을 오염시킨 1차 보고는 없다)

### 3부. 통제 계층으로 막는다

#### 9장. 신원·권한 — 에이전트 ID와 파이프라인 ID

**논지**: 에이전트는 의도가 아니라 닿을 수 있는 범위로 통제한다. 에이전트 쪽 근거는 표준이 댄다(ASI03·SAIF·MCP 인가·NCCoE·금융보안원). 학습 잡·모델 배포·MCP 서버 등록 주체의 ID는 어느 표준도 다루지 않으므로, 이 장이 플랫폼 관점으로 채운다. LLM은 자격 증명에 절대 닿지 않아야 한다.

**핵심 질문**: 공유 서비스 계정(43%)과 사람 계정 차용(31%)을 어떻게 걷어 내나? 사용자 위임과 에이전트 자체 권한은 어떻게 구분하나? 누가 모델을 승격하고 MCP 서버를 등록할 수 있나?

**여는 사례**: ① Amazon Q Developer 확장 변조(CVE-2025-8217, 2025-07-23). CodeBuild 안의 범위가 과도한 GitHub 토큰으로 공격 코드가 커밋돼 v1.84.0에 실렸다 [실사고] ([AWS-2025-015](https://aws.amazon.com/security/security-bulletins/AWS-2025-015/)) ② MCP Python SDK OAuth 결함. 악성 서버가 클라이언트 시크릿과 PKCE verifier를 탈취할 수 있었다 [공개 취약점] (AISEC-2026-0003) ③ Salesloft Drift. 2025-08-20에 모든 토큰이 회수됐다 [실사고] ([Google GTIG](https://cloud.google.com/blog/topics/threat-intelligence/data-theft-salesforce-instances-via-salesloft-drift))

**리더 요약 수치 후보**: 에이전트 하나에 인증을 붙이는 데 1~10일이 든다(43%). 에이전트와 사람의 신원 분리를 우선순위로 꼽은 비율 45%([Help Net Security](https://helpnetsecurity.com/2026/03/26/ciso-ai-agent-identity-security-report/)).

**절 구성**: ① 워크로드 ID 기초: SPIFFE/SPIRE, 투영 SA 토큰, Pod Certificates(v1.37) — **성숙** ② MCP 인가의 MUST 요건: RFC 9728 발견, RFC 8707 audience 바인딩, 토큰 패스스루 금지, iss 검증, step-up 범위 — **성숙**(원리 중심. 형식은 온라인 부록) ③ 위임과 대리 실행: RFC 8693 토큰 교환, 사용자 위임 대 에이전트 권한, 기업 SSO(ID-JAG, Enterprise-Managed Authorization, Transaction Tokens) — **성숙**(RFC) / **부상**(에이전트 적용·초안) ④ 도구 호출 단위 정책 결정: OPA·Cedar, 게이트웨이의 CEL — **성숙**(엔진) / **부상**(도구 호출 적용) ⑤ 파이프라인 ID: 학습 잡·모델 승격·MCP 서버 등록·CI/CD 자격 증명, 서드파티 연동 토큰의 범위와 수명 — **성숙**(패턴), 표준 공백 ⑥ 표준화 지형: WIMSE-AIMS(-00, 2026-09-15 채택), NCCoE, 동적 권한 축소(벤더 사례) — **실험**

**축 매핑**: lifecycle `agent-runtime`, `supply-chain`, `serving`, `training` / controls `identity`

**기존 KB 항목**: AISEC-2026-0003, 0004, 0010, 0011, 0013, 0014, 0015, 0016, 0018

**외부 근거**: [MCP Authorization 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization), [draft-ietf-wimse-aims](https://datatracker.ietf.org/doc/draft-ietf-wimse-aims/), [KEP-4317](https://www.kubernetes.dev/resources/keps/4317/), [datatracker Txn-Tokens](https://datatracker.ietf.org/doc/draft-ietf-oauth-transaction-tokens/), [datatracker ID-JAG](https://datatracker.ietf.org/doc/draft-ietf-oauth-identity-assertion-authz-grant/), [AWS AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html), [SAIF Focus on Agents](https://saif.google/focus-on-agents)

**근거 수준**: 충분 (에이전트 ID) / 보통 (파이프라인 ID는 표준이 없어 사례 기반)

#### 10장. AI 게이트웨이 — 모델·도구 트래픽이 모이는 한 지점 (신설)

**논지**: 공급자 키 보관, 토큰 쿼터·비용, 공급자 장애 전환, MCP 다중화, 도구 단위 인가, 추적이 게이트웨이 한 지점에 모인다. 신원·네트워크·탐지가 만나는 자리다. 그만큼 게이트웨이 자체가 모든 키를 쥔 고가치 공급망 표적이다.

**핵심 질문**: 에이전트가 공급자 키를 직접 쥐지 않게 하려면 무엇이 필요한가? 도구 필터링과 도구 단위 인가는 어디에서 집행하나? 게이트웨이가 뚫리면 무엇을 잃나?

**여는 사례**: ① LiteLLM PyPI 침해(2026-03-24, 약 40분간 공개). CI 보안 스캐너 의존성이 침해돼 PyPI 자격 증명이 넘어간 것으로 추정된다. 악성 버전은 환경 변수·SSH 키·K8s 토큰을 외부로 보냈다. 고정 의존성을 쓴 공식 Docker 이미지는 영향이 없었다 [실사고] ([LiteLLM](https://docs.litellm.ai/blog/security-update-march-2026)) ② LLMjacking의 OAI 리버스 프록시 재판매. 4장에서 교차 인용한다 [실사고] ([Sysdig](https://sysdig.com/blog/llmjacking-stolen-cloud-credentials-used-in-new-ai-attack/))

**절 구성**: ① 게이트웨이가 하는 일: 키 보관, 쿼터·비용, 장애 전환, 추적 — **부상~성숙** ② MCP 게이트웨이: 다중화·클라이언트별 도구 세트·도구 필터(Agent Router `MCPRoute`, agentgateway) — **부상** ③ 도구 단위 인가: CEL·JWT 클레임 전달, extAuthz, Cedar(AgentCore Policy) — **부상** ④ 자체 호스팅 모델 앞 게이트웨이: Gateway API Inference Extension — **부상** ⑤ 게이트웨이의 공급망: 서명 이미지·고정 의존성, 키 회수 계획(LiteLLM 교훈) — **성숙**(교훈)

**축 매핑**: lifecycle `serving`, `agent-runtime`, `supply-chain` / controls `identity`, `network`, `detection`, `provenance`

**기존 KB 항목**: AISEC-2026-0016(서드파티 도구에 맡긴 공급자 키), 0013(제어판에 쌓인 API 키)

**외부 근거**: [Agent Router v1.0](https://theagentrouter.ai/release-notes/v1.0/), [agentgateway](https://agentgateway.dev/docs/standalone/main/documentation/about/introduction/), [Databricks DASF v3.0 (AI Gateway 54)](https://www.databricks.com/blog/agentic-ai-security-new-risks-and-controls-databricks-ai-security-framework-dasf-v30)

**근거 수준**: 보통 (기술 문서는 충분. MCP 게이트웨이 채택 데이터와 KB 직접 항목이 없다)

#### 11장. 네트워크·egress — 나가는 길과 들어오는 문을 생명주기 전체에서 닫는다

**논지**: 유출 체인의 마지막 단계는 언제나 외부 호출이다. egress 허용 목록은 인젝션을 막지 못해도 피해는 막는다. 모든 프레임워크에서 가장 빈 열이므로 이 책의 차별점이다. 에이전트 파드에서 끝내지 않고 RAG 수집, 학습 잡, 레지스트리 pull-through, 메타데이터 엔드포인트까지 다룬다. 한국 금융권에서는 망분리가 완화되면서, 물리적 분리가 하던 일을 egress 통제가 넘겨받아야 한다.

**핵심 질문**: NetworkPolicy로는 왜 부족하고, FQDN 허용 목록의 함정(DNS 프록시 의존, 와일드카드)은 무엇인가? 샌드박스를 탈출했을 때 공격자가 얻는 것은 무엇이 정하나? 모델 API로 나가는 트래픽은 탐지 신호가 될 수 있나?

**여는 사례**: ① ShadowRay 2.0(2025-11). 노출된 Ray 클러스터를 따라 퍼진 웜으로, 공개 접근 가능한 Ray 서버는 23만 대가 넘는다(접근 가능 기준이며 취약 여부는 미확인) [실사고] ([THN](https://thehackernews.com/2025/11/shadowray-20-exploits-unpatched-ray.html)) ② postmark-mcp(2025-09-17). 코드 한 줄로 모든 메일을 외부 주소로 BCC했고, 1,643회 다운로드됐다 [실사고] ([THN](https://thehackernews.com/2025/09/first-malicious-mcp-server-found.html)) ③ OpenAI 내부 모델의 인터넷 제한 우회 보고 [실사고] (AISEC-2026-0017)

**절 구성**: ① 기본 거부와 egress 허용 목록: NetworkPolicy의 한계, Cilium `toFQDNs`(`--enable-l7-proxy`, DNS 규칙 필수, `*` 패턴 위험) — **성숙** ② 표준 API의 진행: ClusterNetworkPolicy·NPEP-133 `DomainNames` — **부상**(v1alpha2) ③ L7 egress: TLS SNI·HTTP 규칙, 메시 egress 게이트웨이 — **성숙**(메시 쪽 근거 보강 필요) ④ 생명주기 전체의 egress: RAG 수집, 학습 잡, 패키지 미러·git 프록시, 레지스트리 pull-through, IMDS 차단(IMDSv2 hop limit) — **성숙**(패턴) ⑤ 들어오는 문: 관리 패널·추론 엔드포인트 노출 관리 — **성숙** ⑥ 탐지로서의 egress와 한국 맥락: 모델 API로 나가는 트래픽(PROMPTSTEAL), 섀도 AI 탐지, 망분리 특례 아래 외부 LLM 연결 — **부상**

**축 매핑**: lifecycle `agent-runtime`, `data`, `training`, `supply-chain`, `serving` / controls `network`, `detection`

**기존 KB 항목**: AISEC-2026-0001, 0002, 0003, 0008, 0011, 0012, 0013, 0017

**외부 근거**: [Cilium L3 DNS-based](https://docs.cilium.io/en/stable/security/policy/layer3/), [NPEP-133](https://network-policy-api.sigs.k8s.io/npeps/npep-133-fqdn-egress-selector/), [Wiz HF 인프라](https://www.wiz.io/blog/wiz-and-hugging-face-address-risks-to-ai-infrastructure), [Google GTIG](https://cloud.google.com/blog/topics/threat-intelligence/threat-actor-usage-of-ai-tools), [세종 망분리 로드맵](https://shinkim.com/kor/media/newsletter/2533)

**근거 수준**: 보통 (기술은 성숙했지만 프레임워크 근거가 비어 있다. 메시 egress 문서는 아직 수집하지 않았다)

#### 12장. 격리·실행 환경 — 자격 증명 없는 곳에서 실행하고, 멈출 수 있게 만든다

**논지**: 신뢰할 수 없는 입력은 자격 증명이 없는 곳에서 처리한다. 어떤 런타임을 고르든 탈출했을 때 얻는 것은 egress가 정한다. 격리는 에이전트 샌드박스로 끝나지 않는다. 모델 로딩, 평가 하네스, GPU 공유도 격리 대상이다. 비상 정지와 자율 실행 제한은 국내 금융 규제가 요구하지만 구현 지침이 없다. 이 장이 엔지니어링 패턴으로 제시한다.

**핵심 질문**: 컨테이너, gVisor, Kata·Firecracker 가운데 무엇을 언제 고르나? `trust_remote_code=False`를 무시하는 로더 앞에서 무엇이 마지막 방어선인가? 에이전트를 '멈춘다'는 것은 구체적으로 무엇을 끊는 일인가?

**여는 사례**: ① NVIDIA Container Toolkit 탈출 CVE-2024-0132(2024-09-26). 공유 GPU 서비스에서 다른 테넌트의 데이터에 닿을 수 있었다 [공개 취약점] ([Wiz](https://www.wiz.io/blog/wiz-research-critical-nvidia-ai-vulnerability)) ② vLLM CVE-2026-27893(2026-03-27). 모델 구현 파일 두 개에 `trust_remote_code=True`가 하드코딩돼 사용자 설정을 덮어썼다 [공개 취약점] ([GitLab advisory](https://advisories.gitlab.com/pypi/vllm/CVE-2026-27893/)) ③ Claude Code Desktop 프리뷰 'SneakPeek'. 저장소의 HTML 하나로 자격 증명이 유출됐다 [공개 취약점] (AISEC-2026-0015)

**절 구성**: ① 격리 강도의 사다리와 쿠버네티스 에이전트 샌드박스: 컨테이너 → gVisor → Kata 4.0/Firecracker, agent-sandbox CRD(Sandbox·Template·Claim·WarmPool), RuntimeClass — 사다리 **성숙** / agent-sandbox **부상**(v1beta1, 1.0.x에서도 breaking. YAML이 아니라 역할 중심으로 설명) ② 자격 증명 없는 실행 환경: 시크릿 분리, LLM이 자격 증명에 닿지 않게(AIMS 원칙) — **성숙**(원칙) ③ 에이전트 밖의 격리: 모델 로딩·역직렬화, 평가 하네스, 학습 환경 — **부상**(프레임워크 공백) ④ GPU 멀티테넌시: MIG는 성능·장애 격리이지 보안 경계가 아니다. 기밀 GPU(NVIDIA CoCo 1.0)는 제약이 많다 — MIG **성숙** / 기밀 GPU **부상** ⑤ 계획-실행 분리: Plan-Then-Execute, Dual LLM, Action-Selector, CaMeL — 패턴 **부상** / CaMeL **실험** ⑥ 멈출 수 있는 실행: 비상 정지·회로 차단기·자율 실행 제한(금융위·금융보안원 요구, CoSAI의 '실패 모드 사전 정의') — **부상**

**축 매핑**: lifecycle `agent-runtime`, `training`, `supply-chain`, `serving` / controls `isolation` (보조 `network`, `identity`)

**기존 KB 항목**: AISEC-2026-0002, 0005, 0011, 0012, 0014, 0015, 0017, 0018

**외부 근거**: [agent-sandbox](https://github.com/kubernetes-sigs/agent-sandbox), [OpenInfra (Kata 4.0)](https://openinfra.org/blog/openinfra-newsletter-july-2026), [NVIDIA CoCo 1.0.0](https://docs.nvidia.com/datacenter/cloud-native/confidential-containers/1.0.0/release-notes.html), [NVIDIA MIG](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/latest/introduction.html), [arXiv 2503.18813](https://arxiv.org/abs/2503.18813), [arXiv 2506.08837](https://arxiv.org/abs/2506.08837), [CoSAI 원칙](https://www.coalitionforsecureai.org/announcing-the-cosai-principles-for-secure-by-design-agentic-systems/), [파이낸셜뉴스 (금융보안원 기준안)](https://www.fnnews.com/news/202610071821048238)

**근거 수준**: 충분 (에이전트 샌드박스) / 보통 (에이전트 밖 격리·비상 정지 구현)

#### 13장. 공급망·출처 — 서명에서 계보로, 계보에서 정책으로

**논지**: 어떤 모델·패키지·MCP 서버·데이터셋이 어디서 왔는지 모르면 조달 배제 명령 하나에도 대응할 수 없다. 장의 뼈대는 CoSAI 모델 서명 성숙도 3단계(서명 → 계보·체인 → 증명·정책)다. 그 위에 쿠버네티스 admission 검증과 레지스트리 승격 정책을 얹는다. 스캐너는 관문이 될 수 없다. 안전한 형식과 격리 로딩이 기본이다.

**핵심 질문**: 블랙리스트 스캐너는 왜 계속 우회되나? 서명된 모델과 출처 증명이 붙은 빌드는 어떻게 다른가? AI-BOM은 누가 만들고 누가 소비하나?

**여는 사례**: ① Ultralytics PyPI(2024-12). 1차는 GitHub Actions 캐시 오염을 거쳐 정상 Trusted Publishing 경로로 배포됐고, 2차는 회수하지 않은 PyPI 토큰으로 배포됐다. attestation 덕분에 공격을 감사할 수 있었다 [실사고] ([PyPI](https://blog.pypi.org/posts/2024-12-11-ultralytics-attack-analysis/)) ② picklescan 제로데이 3종(2025-12-02). 확장자 우회, ZIP CRC 오류, 등급 하향 [공개 취약점] ([JFrog](https://jfrog.com/blog/unveiling-3-zero-day-vulnerabilities-in-picklescan/)) ③ 미 DHS FASCSA 명령. DeepSeek 기반 서드파티 제품까지 제거 대상이 됐다 [표준·정책 사례] (AISEC-2026-0019)

**절 구성**: ① 모델 서명과 검증: OMS, sigstore/model-transparency, NGC(2025-03부터 전 모델 서명) — **성숙**(형식·도구) / 생태계 채택 **부상** ② 빌드·소스 출처: SLSA 1.2(Source Track), in-toto — **성숙**(ML 전용 트랙은 없음) ③ AI-BOM: CycloneDX 1.7 ML-BOM(ECMA-424), SPDX 3.0 AI·Dataset 프로파일 — 형식 **성숙** / 실무 생성·소비 **부상** ④ 로더 안전성: safetensors 우선, 스캔 실패는 실패로 처리, `trust_remote_code` — **성숙**(교훈) ⑤ 승격 정책과 집행: 레지스트리 승격, admission 서명 검증, MCP 서버 레지스트리·허용 목록 — admission **성숙** / MCP 레지스트리 **부상** ⑥ 조달·배제 대응: 모델 인벤토리와 콘텐츠 출처 표시의 한계(워터마크) — **부상**

**축 매핑**: lifecycle `supply-chain`, `data`, `training` / controls `provenance`, `governance`

**기존 KB 항목**: AISEC-2026-0009, 0012, 0019

**외부 근거**: [OASIS CoSAI 서명](https://www.oasis-open.org/2025/11/18/coalition-for-secure-ai-releases-two-actionable-frameworks-for-ai-model-signing-and-incident-response), [OpenSSF OMS](https://openssf.org/blog/2025/06/25/), [sigstore/model-transparency](https://github.com/sigstore/model-transparency), [NVIDIA NGC](https://developer.nvidia.com/blog/bringing-verifiable-trust-to-ai-models-model-signing-in-ngc), [SLSA v1.2](https://slsa.dev/blog/2025/11/announce-slsa-v1.2), [CycloneDX ML-BOM](https://cyclonedx.org/capabilities/mlbom/), [arXiv 2510.07070](https://arxiv.org/abs/2510.07070), [NIST SP 800-218A](https://csrc.nist.gov/pubs/sp/800/218/a/final), [MCP Registry](https://registry.modelcontextprotocol.io/)

**근거 수준**: 충분 (외부 근거) / KB는 3건이라 기초 문헌 보강 필요

#### 14장. 탐지·평가 — 공격 성공률 너머를 보고, 레드팀을 상시 운영한다

**논지**: 가드레일과 분류기는 경계가 아니라 신호다. 처음 보고된 성공률이 0에 가까웠던 방어 12개 가운데 대부분이 적응형 공격에서 90%를 넘겼다. 탐지는 행동 순서와 도구 호출 단위로 한다. 평가는 모델·프롬프트·설정이 바뀔 때마다 CI에서 다시 돈다. 레드팀은 기획 → 준비 → 수행 → 보고 절차로 운영한다.

**핵심 질문**: '가시성이 있다'는 자신감 91.8%와 실제 보호율 약 52%의 차이는 어디서 오나? 도구 호출 로그에는 무엇이 남아야 하나(해석된 인자, 스키마 버전)? 정적 공격 문자열로 평가하면 왜 틀리나?

**여는 사례**: ① 'The Attacker Moves Second'(2025-10-10). 적응형 공격으로 12개 방어의 대부분을 90% 넘게 뚫었다 [연구] ([arXiv 2510.09023](https://arxiv.org/abs/2510.09023)) ② LLMjacking 공격자는 먼저 `GetModelInvocationLoggingConfiguration`으로 자신이 기록되는지 확인했다 [실사고] ([Sysdig](https://sysdig.com/blog/llmjacking-stolen-cloud-credentials-used-in-new-ai-attack/)) ③ 소형 에이전트는 인젝션을 '거부'하지 않고 '무시'한다. 낮은 공격 성공률이 숨기는 것이다 [연구] (AISEC-2026-0020)

**절 구성**: ① 에이전트 관측의 표준: OTel GenAI(에이전트·도구·MCP 스팬), MCP `traceparent` 전파, 내용 캡처 옵트인과 개인정보 — **부상**(Development, 스키마 고정 필요) ② 런타임 탐지: Falco(syscall), 도구 호출 사전 판정(Prempti), 행동 순서 기반 탐지 — Falco **성숙** / Prempti **실험** ③ 가드레일·분류기의 위치: 신호이지 경계가 아니다(PromptGuard 2, LlamaFirewall) — **성숙**(교훈) / 개별 제품 **부상** ④ CI 회귀 평가와 레드팀 자동화: garak·promptfoo·PyRIT(역할 비교 중심) — **부상** ⑤ 평가 지표 설계: 적응형 공격 기준, 실패 유형, 변경 시 재평가, 추론 최적화 설정별 평가 — **성숙**(방법론) ⑥ 레드팀 운영: KISA 레드티밍 가이드(ISO/IEC 42119-7 기반)의 기획 → 준비 → 수행 → 보고, OWASP GenAI Red Teaming Manual v1.0

**축 매핑**: lifecycle `agent-runtime`, `serving`, `training` / controls `detection`

**기존 KB 항목**: AISEC-2026-0001, 0002, 0004, 0006, 0010, 0013, 0014, 0016, 0017, 0018, 0020

**외부 근거**: [opentelemetry.io gen-ai](https://opentelemetry.io/docs/specs/semconv/gen-ai/), [semantic-conventions-genai](https://github.com/open-telemetry/semantic-conventions-genai), [Sysdig Prempti](https://www.sysdig.com/blog/introducing-prempti-runtime-security-for-ai-coding-agents-powered-by-falco), [arXiv 2505.03574](https://arxiv.org/abs/2505.03574), [garak releases](https://github.com/NVIDIA/garak/releases), [microsoft/PyRIT](https://github.com/microsoft/PyRIT), [바이라인네트워크 (KISA 가이드)](https://byline.network/2026/07/8-489/), [SAIF Agent Observability](https://saif.google/focus-on-agents)

**근거 수준**: 충분

### 4부. 운영과 거버넌스

#### 15장. 누가 책임지나 — 운영 모델, 에이전트 등록부, 리스크 등록부 (신설)

**논지**: 에이전트 행동에 공식 책임자를 지명한 조직은 7.2%다. 책임은 보안·IT(28%), 개발(25%), 비즈니스(18%)로 흩어져 있다. 리더가 내릴 결정의 핵심은 "누가 에이전트를 등록·승인·회수하나"다. 인젝션은 '열린 결함'이 아니라 담당자·범위·재평가 조건이 있는 상시 위험으로 등록한다.

**핵심 질문**: 보안·플랫폼·ML/앱·비즈니스 오너의 RACI는 어떻게 나누나? 에이전트 등록부에는 어떤 필드가 있어야 하나? 범위가 바뀌면 무엇을 다시 평가하나?

**여는 사례**: ① OpenCode Console 레거시 시스템 침해. 폐기 중이던 시스템이 사용자의 공급자 키를 품은 채 남아 있었다 [실사고] (AISEC-2026-0016, status partial) ② Microsoft SAS 토큰(2020 커밋 → 2023 발견). 아무도 그 토큰을 보거나 관리하지 않았다 [실사고] ([Wiz](https://www.wiz.io/blog/38-terabytes-of-private-data-accidentally-exposed-by-microsoft-ai-researchers))

**리더 요약 수치 후보**: 공식 책임자 7.2%, 회수 절차 34.1%, 허용 범위 정의 30.5%([Gravitee](https://www.gravitee.io/state-of-ai-agent-security?hl=cs-CZ)). 섀도 AI가 광범위한 조직의 침해 비용은 67만 달러 더 많다([TechRepublic](https://www.techrepublic.com/article/news-ai-breach-risks-rise-as-governance-lags/)).

**절 구성**: ① 소유권 지형: 설문이 보여 주는 책임 분산 ② RACI와 플랫폼 팀의 위치(골든 패스 제공자) ③ 에이전트 등록부: 신원·범위·소유자·회수 경로 ④ 리스크 등록부: 인젝션을 상시 위험으로, 범위 변경 시 재평가 ⑤ 섀도 AI 정책: 허용 목록, 탐지(11장)와 예외 절차

**축 매핑**: lifecycle 전 단계 / controls `governance`, `identity`

**기존 KB 항목**: AISEC-2026-0005, 0016, 0018

**외부 근거**: [Help Net Security (CSA 설문)](https://helpnetsecurity.com/2026/03/26/ciso-ai-agent-identity-security-report/), [Gravitee](https://www.gravitee.io/state-of-ai-agent-security?hl=cs-CZ), [CSA Labs Identity Sprawl (미열람)](https://labs.cloudsecurityalliance.org/research/csa-research-note-ai-agent-identity-sprawl-authorization-202/)

**근거 수준**: 보통 (벤더 설문 위주. 표본·주체·시점을 함께 적어야 한다)

#### 16장. 표준을 플랫폼 통제로 번역한다 — OWASP·NIST·ATLAS·CSA·SAIF

**논지**: 표준은 위험 목록(OWASP), 공격 어휘(ATLAS), 분류 체계(NIST AI 100-2), 통제 카탈로그(AICM)로 역할이 갈린다. 이 장은 표준 요구를 '어떤 플랫폼 통제로 증빙하나'라는 번역표로 바꾼다. 거버넌스만 다루고 끝나는 장이 되지 않게, 번역표의 모든 칸이 3부의 구체 통제를 가리킨다. 초안 표준은 상태를 표기하는 것을 원칙으로 한다.

**핵심 질문**: 프레임워크들이 공통으로 요구하는 것(인젝션, 오염, 출처, 과잉 권한, 관측, 상시 평가)과 비워 둔 것(egress, 에이전트 밖 격리, 파이프라인 ID)은 무엇인가? 'disputed' CVE처럼 표준 체계 밖으로 빠지는 위험은 어떻게 관리하나?

**여는 사례**: ① ShadowRay CVE-2023-48022. 'disputed' 태그 때문에 많은 스캐너에서 빠졌다. 거버넌스 체계의 맹점이다 [실사고] ([NVD](https://nvd.nist.gov/vuln/detail/CVE-2023-48022)) ② OWASP 2026 LLM Top 10. Excessive Agency가 3위로 올랐고 ACS가 기증됐다 [표준 사례] (AISEC-2026-0010) ③ OpenAI textGrain. EU AI Act 투명성 규정이 서빙 출력 단계로 내려온 사례다 [표준·정책 사례] (AISEC-2026-0009)

**절 구성**: ① 표준 지도: 위험 목록·공격 어휘·분류·통제 카탈로그·위협 모델링(MAESTRO) ② 합의된 것과 비어 있는 것: 5×6 크로스워크 ③ 번역표: 표준 요구 → 플랫폼 통제 → 증적(로그·정책·서명) ④ 취약점 관리의 AI 특수성: disputed CVE, CVE가 붙지 않는 취약점 유형, 설정 변경까지가 패치 ⑤ 초안 표준 다루기: COSAIS·NCCoE·IR 8596·ACS의 상태 표기

**축 매핑**: lifecycle 전 단계 / controls `governance` (+각 장 통제)

**기존 KB 항목**: AISEC-2026-0005, 0009, 0010, 0019, 0004

**외부 근거**: [OWASP LLM Top 10](https://genai.owasp.org/llm-top-10/), [OWASP Agentic Top 10](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/), [NIST AI 600-1](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf), [NIST IR 8596](https://csrc.nist.gov/pubs/ir/8596/iprd), [CSA AICM](https://cloudsecurityalliance.org/artifacts/ai-controls-matrix), [SAIF risks](https://saif.google/secure-ai-framework/risks), [ATLAS](https://github.com/mitre-atlas/atlas-data)

**근거 수준**: 충분

#### 17장. 한국 규제를 플랫폼 통제로 번역한다 (신설)

**논지**: 인공지능 기본법은 거버넌스 수준에서 작동한다. 고지·표시, 고영향 AI 위험관리, 사람의 관리·감독, 문서 5년 보관, 10^26 FLOPs 기준이 그 내용이고, 인프라 통제를 규정하지는 않는다. 구체적인 기술 요구는 비구속 지침과 금융권 기준에 있다. 금융위 비상 정지 의무, 금융보안원 에이전트 평가기준(안) 17개 항목, 망분리 특례 조건이 그 예다. 이 장은 이 요구들을 감사 로그 보존, 승인 게이트, 비상 정지, egress 게이트웨이, 가명처리 파이프라인으로 번역한다.

**핵심 질문**: '사람의 관리·감독'과 '문서 5년 보관'은 어떤 로그·승인 단계로 증빙하나? 망분리 예외로 외부 LLM을 쓸 때 플랫폼이 갖춰야 할 통제는 무엇인가? 금융보안원 평가기준(안)의 실행 권한·격리·도구 승인 항목은 3부의 어느 절과 대응하나?

**여는 사례**: ① ARTEX를 이용한 한국 금융권 공격. 당국 집계로 16곳·약 10만 건이 유출됐다 [실사고] (AISEC-2026-0001) ② 금감원 집계(파이낸셜뉴스 2026-10-07 보도). 8월까지 은행 20곳의 모의해킹 78건 중 9건(11.5%)에서 AI 에이전트가 쓰였다 [조사·통계] ([파이낸셜뉴스](https://www.fnnews.com/news/202610071821048238))

**절 구성**: ① 인공지능 기본법과 시행령: 의무 지도, 고영향 AI 10개 분야, 국내대리인 기준, 과태료 유예(1년 이상) ② 의무 → 통제 번역: 5년 보관 → 감사 로그 보존, 관리·감독 → 승인 게이트·비상 정지, 결과물 표시 → 서빙 출력 파이프라인 ③ 금융권: 망분리 개선 로드맵(2024-08-13)과 특례 조건, 금융분야 AI 가이드라인(비상 정지 의무), 금융보안원 평가기준(안)·보안성 검증체계 ④ 과기정통부·KISA 지침: AI 보안 위협 대응 매뉴얼(위협 분류: 데이터·모델·에이전트·공급망·고성능 모델), 레드티밍 가이드 ⑤ 상태 표와 남은 공백: ISMS-P, 개인정보위 자료는 추가 조사 대상

**축 매핑**: lifecycle `serving`, `agent-runtime`, `data` / controls `governance`, `network`, `identity`, `isolation`, `detection`

**기존 KB 항목**: AISEC-2026-0001

**외부 근거**: [세종 (AI 기본법)](https://shinkim.com/kor/media/newsletter/3114), [바이라인네트워크 (시행령)](https://byline.network/2026/01/21-545/), [노컷뉴스 (금융위 가이드라인)](https://www.nocutnews.co.kr/news/6534884), [파이낸셜뉴스 (금융보안원 기준안)](https://www.fnnews.com/news/202610071821048238), [세종 (망분리)](https://shinkim.com/kor/media/newsletter/2533), [바이라인네트워크 (KISA 매뉴얼)](https://byline.network/2026/07/8-489/), [바이라인네트워크 (금융보안원 검증체계)](https://byline.network/2024/12/19-423), [law.go.kr](https://www.law.go.kr/법령/인공지능발전과신뢰기반조성등에관한기본법)

**근거 수준**: 부족 (1차 원문 미확보. 법령 조문·KISA 원문·금융보안원 원문 모두 2차 보도 기준이고, 일부는 초안)

#### 18장. 에이전트 사고 대응 — 도구 호출 로그, 자격 증명 회수, 재현 (v0 14장에서 분리)

**논지**: 에이전트 사고의 포렌식은 에이전트가 스스로 한 요약으로 하지 않는다. 해석된 인자까지 남긴 도구 호출 로그로 한다. 대응의 중심은 자격 증명 회수다. 회수가 불완전하면 두 번째 침해가 온다. 회수 절차를 문서로 갖춘 조직은 34.1%뿐이다.

**핵심 질문**: 사고가 나면 몇 분 안에 무엇을 끊나(토큰, egress, 샌드박스, 에이전트)? 무엇이 남아 있어야 재현할 수 있나? 모델 아티팩트 오염 사고는 일반 침해 대응과 무엇이 다른가?

**여는 사례**: ① Ultralytics 2차 배포. 1차 대응 뒤에도 회수하지 않은 PyPI API 토큰이 남아 있었다 [실사고] ([PyPI](https://blog.pypi.org/posts/2024-12-11-ultralytics-attack-analysis/)) ② Hugging Face Spaces 시크릿 침해(2024-05-31). 토큰을 회수하고 조직 토큰을 제거했으며, KMS를 도입하고 당국에 신고했다 [실사고] ([Hugging Face](https://huggingface.co/blog/space-secrets-disclosure)) ③ OpenAI 내부 모델 무단 행동. 발견까지 두 달 넘게 걸렸다 [실사고] (AISEC-2026-0017)

**절 구성**: ① 플레이북 틀: CoSAI AI 사고 대응 프레임워크 v1.0(오염·모델 탈취·인젝션·추론 공격, 포렌식, 에이전트 아키텍처) ② 탐지에서 격리까지: 비상 정지 실행, egress 차단, 샌드박스 동결 ③ 자격 증명 회수: 에이전트·파이프라인·서드파티 연동 토큰(Drift 일괄 회수, Nx) ④ 포렌식과 재현: 도구 호출 로그, OTel 추적, 프롬프트·모델 버전 고정 ⑤ 보고와 규제: AI 기본법 기록 보관, 금융권 보고, 개인정보 신고

**축 매핑**: lifecycle `agent-runtime`, `supply-chain`, `training` / controls `detection`, `identity`, `isolation`, `governance`

**기존 KB 항목**: AISEC-2026-0001, 0013, 0014, 0017

**외부 근거**: [OASIS CoSAI IR Framework](https://www.oasis-open.org/2025/11/18/coalition-for-secure-ai-releases-two-actionable-frameworks-for-ai-model-signing-and-incident-response), [Google GTIG (Drift)](https://cloud.google.com/blog/topics/threat-intelligence/data-theft-salesforce-instances-via-salesloft-drift), [Wiz (Nx)](https://www.wiz.io/blog/s1ngularity-supply-chain-attack), [Gravitee](https://www.gravitee.io/state-of-ai-agent-security?hl=cs-CZ)

**근거 수준**: 보통 (CoSAI 프레임워크 본문을 아직 읽지 않았다)

#### 19장. 도입 로드맵 — 0일 차부터 1년 (신설, 맺음 장)

**논지**: 81%가 빨리 배포하라는 압박을 느끼는데, 배포 전 통제를 갖춘 비율은 30~38%에 머문다. 통제를 한 번에 갖출 수는 없다. 섀도 AI 파악 → 최소 통제(신원·egress·로그) → 게이트웨이·샌드박스 → 평가·레드팀 → 거버넌스·규제 증빙 순서의 성숙도 모델로 단계를 밟는다.

**핵심 질문**: 첫 30일에 반드시 해야 할 세 가지는 무엇인가? '에이전트 하나에 인증 1~10일'이라는 고충을 골든 패스로 어떻게 없애나? 각 단계가 끝났다는 것은 어떤 증적으로 판단하나?

**여는 사례**: 여는 사례 대신 조사 수치로 시작한다. Gravitee(2026-04 조사): 넉 달 사이 에이전트 수 약 2배, 배포 압박 81% [조사·벤더] ([Gravitee](https://www.gravitee.io/state-of-ai-agent-security?hl=cs-CZ)). CNCF(2025-09 조사): 쿠버네티스에서 생성형 AI 워크로드를 운영하는 조직 66% [조사] ([CNCF](https://www.linuxfoundation.org/hubfs/Research%20Reports/CNCF_Annual_Survey_Report_1.15.26.pdf?hsLang=en))

**절 구성**: ① 0일 차: 섀도 AI·에이전트 인벤토리 ② 30일: 최소 통제 세트(워크로드 ID, 단기 토큰, 기본 거부 egress, 도구 호출 로그) — **성숙** ③ 90일: 게이트웨이·샌드박스·서명 검증 — **부상~성숙** ④ 180일: CI 회귀 평가·레드팀 정례화 ⑤ 1년: 거버넌스·규제 증빙 자동화, 재평가 주기

**축 매핑**: lifecycle 전 단계 / controls 전 계층(우선순위)

**기존 KB 항목**: (종합 장. 개별 항목 없음)

**외부 근거**: [Help Net Security](https://helpnetsecurity.com/2026/03/26/ciso-ai-agent-identity-security-report/), [Gravitee](https://www.gravitee.io/state-of-ai-agent-security?hl=cs-CZ), [TechRepublic](https://www.techrepublic.com/article/news-ai-breach-risks-rise-as-governance-lags/)

**근거 수준**: 보통

---

## 4. v0 대비 변경점

| v0 장 | v1 장 | 변경 유형 | 이유 (근거) |
|---|---|---|---|
| 1장 프롬프트 인젝션은 상시 위험 | 1장 | 유지·재구성 | 논지는 이미 차별화되어 있다. 기법 나열은 줄인다. 한국 독자의 첫 우려가 데이터 유출(53.3%, 64.5%)이고, CSA가 에이전트의 도달 범위를 수치로 보여 준다. 그래서 장을 유출 경로로 열고, 3부로 넘기는 다리 장으로 만든다 ([파이낸셜뉴스](https://www.fnnews.com/news/202508260933530786), [Help Net Security](https://helpnetsecurity.com/2026/03/26/ciso-ai-agent-identity-security-report/)) |
| 2장 공격자도 에이전트를 쓴다 | 2장 | 유지·보강 | 벤더 위협 보고서(갈취·첩보·PROMPTSTEAL)를 추가하고 단일 출처 한계를 명시한다. 사건 노트는 이 주제를 '위협 환경' 서장으로 따로 빼자고 제안했는데, v0의 위치가 이미 그 자리다 ([Anthropic](https://www.anthropic.com/news/disrupting-AI-espionage), [GTIG](https://cloud.google.com/blog/topics/threat-intelligence/threat-actor-usage-of-ai-tools)) |
| (없음) | 3장 참조 아키텍처·신뢰 경계·실습 환경 | 신설 | Wilson 3장·Malik 외 4장의 관례이고, MAESTRO L4와 대응한다. 2·3부의 공통 지도이자 누적형 실습의 출발점이다 ([O'Reilly](https://www.oreilly.com/library/view/-/9781098162191/), [CSA](https://cloudsecurityalliance.org/blog/2025/02/06/agentic-ai-threat-modeling-framework-maestro)) |
| 3장 데이터 | 7장 | 이동·재구성 | 독자 노출도와 실사고 근거가 상대적으로 약해 뒤로 보낸다. '노출(실사고)/오염(연구)' 두 갈래로 나누고 섀도 AI 절을 신설한다 ([Anthropic 250 docs](https://www.anthropic.com/research/small-samples-poison), [TechRepublic](https://www.techrepublic.com/article/news-ai-breach-risks-rise-as-governance-lags/)) |
| 4장 학습·튜닝 | 8장 학습·평가 인프라 | 이동·재정의 | 52%가 학습을 하지 않으므로 맨 뒤로 보낸다. 그래도 장은 지킨다. ShadowRay는 쿠버네티스 인접 GPU 클러스터 문제이고, '훈련 중인 모델이 공격자'라는 새 위협 모델이 있기 때문이다. 장을 '인프라/평가 환경' 두 갈래로 나눈다 ([CNCF](https://www.linuxfoundation.org/hubfs/Research%20Reports/CNCF_Annual_Survey_Report_1.15.26.pdf?hsLang=en), [Oligo](https://www.oligo.security/blog/shadowray-attack-ai-workloads-actively-exploited-in-the-wild)) |
| 5장 서빙·추론 | 4장 | 이동·병합 | 실사고가 가장 풍부하고 누구나 겪는 단계라 2부 맨 앞에 둔다. 플랫폼 노트가 제안한 '서빙 인프라 하드닝'을 절로 합친다 ([Sysdig](https://sysdig.com/blog/llmjacking-stolen-cloud-credentials-used-in-new-ai-attack/), [GitLab advisory](https://advisories.gitlab.com/pypi/vllm/CVE-2026-22778/)) |
| 6장 에이전트 런타임 | 5장 | 이동·압축 | KB가 이미 가장 두껍다. 사례를 더하지 않고 '입력 × 권한 × 출구' 패턴으로 묶는다 (사건 노트 §4) |
| 7장 공급망·배포 | 6장 | 유지·두 갈래 | 아티팩트(출처·격리)와 서드파티 연동 토큰(신원)은 실패하는 통제가 다르다 ([GTIG Drift](https://cloud.google.com/blog/topics/threat-intelligence/data-theft-salesforce-instances-via-salesloft-drift), [OpenAI Mixpanel](https://openai.com/index/mixpanel-incident/)) |
| 8장 신원·권한 | 9장 | 유지·분리(절 단위) | 3부 맨 앞을 지킨다. 독자의 최대 고충이고, 모든 단계에서 가장 자주 실패한 통제다. '에이전트 ID / 파이프라인 ID' 두 갈래로 나눈다. 파이프라인 ID는 어느 표준도 다루지 않는다 ([Help Net Security](https://helpnetsecurity.com/2026/03/26/ciso-ai-agent-identity-security-report/), [NCCoE](https://www.nccoe.nist.gov/projects/software-and-ai-agent-identity-and-authorization)) |
| (없음, v0 9장 일부) | 10장 AI 게이트웨이 | 신설 | 신원·네트워크·탐지가 모이는 지점이다. API가 v1.0으로 안정됐고, 게이트웨이 자체가 침해된 사례가 있다 ([Agent Router](https://theagentrouter.ai/release-notes/v1.0/), [LiteLLM](https://docs.litellm.ai/blog/security-update-march-2026)) |
| 9장 네트워크·egress | 11장 | 유지·확장 | 프레임워크에서 가장 빈 열이므로 책의 차별점으로 키운다. 생명주기 전체(RAG·학습 잡·레지스트리·IMDS)로 넓히고 망분리 완화 맥락을 넣는다 ([NPEP-133](https://network-policy-api.sigs.k8s.io/npeps/npep-133-fqdn-egress-selector/), [세종](https://shinkim.com/kor/media/newsletter/2533)) |
| 10장 격리·실행 환경 | 12장 | 유지·확장 | 모델 로딩·평가 하네스·GPU 공유로 넓힌다. 비상 정지·자율 실행 제한 절을 신설한다. 금융위·금융보안원이 요구하지만 구현 지침이 없는 부분이다 ([vLLM CVE-2026-27893](https://advisories.gitlab.com/pypi/vllm/CVE-2026-27893/), [노컷뉴스](https://www.nocutnews.co.kr/news/6534884)) |
| 11장 공급망·출처 | 13장 | 유지·재구성 | CoSAI 서명 성숙도 3단계를 뼈대로 쓰고 admission·승격 정책을 얹는다. 6장과는 '공격 표면 대 통제 설계'로 역할을 나눠 중복을 피한다 ([OASIS](https://www.oasis-open.org/2025/11/18/coalition-for-secure-ai-releases-two-actionable-frameworks-for-ai-model-signing-and-incident-response)) |
| 12장 탐지·평가 | 14장 | 유지·병합 | v0 14장의 레드팀 운영을 이쪽으로 옮긴다(CI 회귀 평가와 한 흐름). 적응형 공격 연구를 장의 중심 근거로 쓴다 ([arXiv 2510.09023](https://arxiv.org/abs/2510.09023)) |
| 13장 거버넌스·정책 | 15장(리스크 등록부) + 16장(표준 번역) | 분리 | 리스크 등록부는 '누가 책임지나'와 묶어 15장으로 보낸다. 표준 → 통제 번역표는 16장에 남긴다 ([Gravitee](https://www.gravitee.io/state-of-ai-agent-security?hl=cs-CZ)) |
| (없음) | 15장 운영 모델·소유권 | 신설 | 공식 책임자 7.2%, 책임 분산 28/25/18%. 독자가 기대하는 산출물은 RACI·등록부·회수 런북이다 ([Gravitee](https://www.gravitee.io/state-of-ai-agent-security?hl=cs-CZ), [Help Net Security](https://helpnetsecurity.com/2026/03/26/ciso-ai-agent-identity-security-report/)) |
| (v0 13장 '규제' 일부) | 17장 한국 규제 번역 | 신설·분리 | 확인한 한국어 책 가운데 이를 다룬 책이 없다. 금융권 독자에게 직접 쓰이는 장이다. 다만 근거가 2차 보도와 초안이라 상태 표를 둔다 (책·과정 노트 §4, [파이낸셜뉴스](https://www.fnnews.com/news/202610071821048238)) |
| 14장 사고 대응과 레드팀 운영 | 18장 에이전트 사고 대응 + 14장 ⑥절 | 분리 | 확인한 어느 책 목차에도 에이전트 IR 장이 없다. SEC545도 AI를 조사 도구로 쓰는 실습만 있다 ([SANS](https://www.sans.org/cyber-security-courses/genai-llm-application-security-5day)) |
| (없음) | 19장 도입 로드맵 | 신설 | 배포 압박 81%, 배포 전 통제 보유 30~38%. 리더 요약의 '내릴 결정'과 이어진다 ([Gravitee](https://www.gravitee.io/state-of-ai-agent-security?hl=cs-CZ)) |
| 부록: 점검표·용어집 | 부록 A·J | 유지·확장 | 아래 5절 참고 |

**연구자 간 엇갈림과 이 보고서의 선택.** 세 군데에서 노트끼리 제안이 엇갈렸다. 첫째는 3부의 탐지 장 위치다. 독자 수요 노트는 실시간 가시성이 최우선 과제(52%)라는 근거로 탐지를 신원 바로 뒤로 당기자고 했다. v1은 탐지를 3부 마지막에 둔다. 탐지가 기대는 추적 지점(게이트웨이, 샌드박스, 도구 호출 훅)을 앞 장들이 먼저 깔아 두기 때문이다. 대신 10장 게이트웨이에 추적 절을 넣어 가시성을 일찍 다룬다. 둘째는 2부의 순서다. 독자 노출도 순(런타임 → 서빙 → 공급망 → 데이터 → 학습)과 axes.yaml의 흐름 순(데이터 → … → 공급망)이 맞선다. v1은 서빙을 맨 앞에 둔다. 실사고 근거가 가장 강하고, 관리형 API 사용자까지 포함해 독자 전원이 겪는 단계이기 때문이다. 흐름 순을 지키고 싶다면 장 번호만 바꾸면 된다. 각 장의 내용은 순서와 무관하게 서 있도록 설계했다. 셋째는 공급망을 두 장으로 나눌지다. 사건 노트는 분리를 제안했고, 책·과정 노트는 2부 압축을 제안했다. v1은 한 장 안의 두 갈래로 두고, 연동 토큰의 통제는 9장으로 보낸다.

---

## 5. 부록 후보

| 부록 | 내용 | 근거·출처 |
|---|---|---|
| A. 생명주기 × 통제 점검표 | 집필 매트릭스를 체크리스트로. 칸마다 OWASP LLM/ASI ID, ATLAS 기술 ID, AICM 통제 대응 | [ATLAS (2026.05부터 플랫폼 태그)](https://github.com/mitre-atlas/atlas-data/blob/main/CHANGELOG.md), [CSA AICM](https://cloudsecurityalliance.org/artifacts/ai-controls-matrix) |
| B. OWASP 교차 참조표 | OWASP LLM Top 10(2025/2026판), Agentic Top 10 2026, ACS ↔ 이 책의 장·절·통제 | [OWASP GenAI](https://genai.owasp.org/2026/09/01/owasp-genai-security-project-unveils-2026-top-10-for-llm-applications-new-agent-control-standard-and-sponsors-as-community-tops-30000-members/) |
| C. 참조 아키텍처와 에이전트 골든 패스 | 워크로드 ID·단기 토큰·egress 허용 목록·도구 호출 로그가 기본으로 붙은 Helm/Kustomize 템플릿과 Kyverno·OPA 정책. '인증 하나에 1~10일' 고충에 대한 답 | [Help Net Security](https://helpnetsecurity.com/2026/03/26/ciso-ai-agent-identity-security-report/), [KubeCon India 2026](https://kccncind2026.sched.com/2026-06-19/list/descriptions/type/Security) |
| D. 정책 코드 예시집 | Cilium `toFQDNs` egress, admission 서명 검증, CEL·Cedar 도구 단위 인가, RuntimeClass·Sandbox 템플릿. 각 예시에 버전과 열람일 표기 | [Cilium](https://docs.cilium.io/en/stable/security/policy/layer3/), [AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html), [agent-sandbox](https://github.com/kubernetes-sigs/agent-sandbox) |
| E. 런북 | (1) 에이전트 비상 정지·자격 증명 회수(회수 절차 보유 34.1%) (2) 악성 모델·패키지 유입 대응 (3) 게이트웨이 키 유출 대응 | [Gravitee](https://www.gravitee.io/state-of-ai-agent-security?hl=cs-CZ), [CoSAI IR](https://www.oasis-open.org/2025/11/18/coalition-for-secure-ai-releases-two-actionable-frameworks-for-ai-model-signing-and-incident-response) |
| F. 배포 전 점검표 | Gravitee가 조사한 여섯 가지 배포 전 통제(책임자, 보안 검토, 중지·회수, 민감 데이터 계획, 전용 접근 통제, 범위 정의)를 기본형으로 삼고 금융보안원 17개 항목과 대조 | [Gravitee](https://www.gravitee.io/state-of-ai-agent-security?hl=cs-CZ), [파이낸셜뉴스](https://www.fnnews.com/news/202610071821048238) |
| G. RACI·에이전트 등록부·리스크 등록부 양식 | 보안·플랫폼·ML/앱·비즈니스 오너, 등록 필드, 재평가 조건 | 15장 |
| H. 한국 규제 대응표 | AI 기본법 의무·망분리 특례 조건·금융위 가이드라인·금융보안원 기준(안) ↔ 플랫폼 통제 ↔ 증적 로그. 조문 번호는 원문 확인 후 기입 | [세종](https://shinkim.com/kor/media/newsletter/3114), [세종 망분리](https://shinkim.com/kor/media/newsletter/2533) |
| I. 버전·상태 표 (온라인, KB 연동) | MCP 스펙 개정 이력, IETF 초안 번호·상태, CNCF 단계, NIST 초안 상태, 주요 프로젝트 버전. 본문은 원리만 다루고 이 표만 갱신한다 | 7절 목록 |
| J. 용어집 | 한국어 표기 기준(프롬프트 인젝션, 탈옥, 증류, egress, 워크로드 ID, 폭발 반경 등) | v0 유지 |
| K. 실습 환경 가이드 | kind/minikube 위 누적형 에이전트 플랫폼 구성과 장별 통제 추가 순서 | 3장 |

---

## 6. 기초 문헌 수집 우선순위

순서는 'KB가 얇은 장'을 먼저 채우는 순이다. KB 매트릭스에서 데이터 행은 1건, 학습 행도 1건이고, 에이전트 런타임×출처, 데이터×출처, 학습×출처·신원·거버넌스, 서빙×네트워크 칸은 0건이다. 모두 1등급 원문이고, 수집할 때는 KB 규칙대로 저자 전원과 절·표 번호 locator를 단다.

| # | 채울 장(칸) | 문헌 | 발행·저자 | 버전·날짜 | URL |
|---|---|---|---|---|---|
| 1 | 7장 (데이터×출처) | Poisoning Web-Scale Training Datasets is Practical | Carlini, Jagielski, Choquette-Choo, Paleka, Pearce, Anderson, Terzis, Thomas, Tramèr | arXiv 2302.10149, 2023-02-20 | https://arxiv.org/abs/2302.10149 |
| 2 | 7장 (데이터×탐지) | 소수 표본 오염 연구(250개 문서) | Anthropic·UK AISI·Alan Turing Institute | arXiv 2510.07192, 2025-10-09 | https://www.anthropic.com/research/small-samples-poison |
| 3 | 7장 (데이터, RAG) | PoisonedRAG | Zou, Geng, Wang, Jia | arXiv 2402.07867, 2024-02-12 | https://arxiv.org/abs/2402.07867 |
| 4 | 8장 (학습×출처·탐지) | Sleeper Agents | Hubinger 외 | arXiv 2401.05566, 2024-01-10 | https://arxiv.org/abs/2401.05566 |
| 5 | 8장 (학습×격리·네트워크) | OpenAI o1-preview System Card §4.2.1 | OpenAI | 2024-09-17 | https://cdn.openai.com/o1-preview-system-card-20240917.pdf |
| 6 | 8장 (학습×탐지) | Emergent misalignment from reward hacking | Anthropic | 2025-11-21 | https://www.anthropic.com/research/emergent-misalignment-reward-hacking |
| 7 | 8·13장 (학습×출처·거버넌스) | SP 800-218A SSDF Community Profile for GenAI | NIST | final 2024-07-26 | https://csrc.nist.gov/pubs/sp/800/218/a/final |
| 8 | 13장 (공급망×출처) | Signing ML Artifacts + AI Incident Response Framework V1.0 | CoSAI (OASIS) | 2025-11-18 | https://www.oasis-open.org/2025/11/18/coalition-for-secure-ai-releases-two-actionable-frameworks-for-ai-model-signing-and-incident-response |
| 9 | 13장 | OpenSSF Model Signing (OMS) + sigstore/model-transparency | OpenSSF (Google, HiddenLayer, NVIDIA) | 2025-06-25 | https://openssf.org/blog/2025/06/25/ |
| 10 | 13장 | SLSA v1.2 | OpenSSF SLSA | 2025-11-24 | https://slsa.dev/blog/2025/11/announce-slsa-v1.2 |
| 11 | 13장 (데이터·학습×출처) | CycloneDX 1.7 ML-BOM (ECMA-424) | OWASP CycloneDX / Ecma | 1.7, 2025-10-21 | https://cyclonedx.org/capabilities/mlbom/ |
| 12 | 13장 | Building an Open AIBOM Standard in the Wild | Kate Stewart, Karen Bennet 외 | arXiv 2510.07070 v2, 2026-02-22 | https://arxiv.org/abs/2510.07070 |
| 13 | 9장 (에이전트 런타임×신원, 표준 측) | MCP Authorization (revision 2026-07-28) | Model Context Protocol | 2026-07-28 | https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization |
| 14 | 9장 | draft-ietf-wimse-aims (AI Identity Management System) | IETF WIMSE (Defakto, AWS, Zscaler, Ping, OpenAI, Okta) | -00, 2026-09-15 | https://datatracker.ietf.org/doc/draft-ietf-wimse-aims/ |
| 15 | 9장 | Software and AI Agent Identity and Authorization (concept paper) | NIST NCCoE | 2026-02-05 | https://www.nccoe.nist.gov/projects/software-and-ai-agent-identity-and-authorization |
| 16 | 12장 (격리, 패턴) | CaMeL (arXiv 2503.18813) 및 Design Patterns for Securing LLM Agents (arXiv 2506.08837) | Debenedetti, Carlini, Tramèr 외 / 저자 수 확인 필요 | v2 2025-06-24 / v3 2025-06-27 | https://arxiv.org/abs/2503.18813 , https://arxiv.org/abs/2506.08837 |
| 17 | 14장 (탐지) | The Attacker Moves Second | Nasr, Carlini, Tramèr, Schulhoff 외 | arXiv 2510.09023, 2025-10-10 | https://arxiv.org/abs/2510.09023 |
| 18 | 4장 (서빙×탐지) | Stealing Part of a Production Language Model | Carlini 외 14명 | arXiv 2403.06634, 2024-03-11 | https://arxiv.org/abs/2403.06634 |
| 19 | 3·16장 (전반 분류 체계) | NIST AI 100-2 E2025 (§3.5 Security of Agents 포함) | NIST | E2025, 2025-03-24 | https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-2e2025.pdf |
| 20 | 17장 (한국) | 인공지능 기본법·시행령 원문 + 과기정통부·KISA「AI 보안 위협 대응 매뉴얼」「AI 보안 레드티밍 가이드」 | 대한민국 / 과기정통부·KISA | 시행 2026-01-22 / 2026-07-08 | https://www.law.go.kr/법령/인공지능발전과신뢰기반조성등에관한기본법 (KISA 원문 URL은 미확인. 먼저 찾아야 함) |

예비 후보는 CSA MAESTRO, CSA AICM v1.1, OWASP Agentic Top 10 2026 PDF, 슬롭스쿼팅 논문(arXiv 2406.10279)이다. 6장·16장이 얇아지면 이 가운데서 먼저 넣는다.

---

## 7. 미확인·주의

**인용 전에 1차 원문으로 확인해야 하는 주장.**

- **OWASP**: Agentic Top 10 2026의 ASI01~ASI10 이름은 2차 출처(Giskard·Modulos) 두 곳에서 왔다. OWASP PDF는 열지 않았다([Modulos](https://docs.modulos.ai/frameworks/owasp-top-10-agentic/index)). OWASP 2026 LLM Top 10 전체 목록도 읽지 않았다. 프레임워크 노트는 2025판 목록을 기준으로 했고, 'Excessive Agency 3위'는 후원사 인용에서 나왔다([OWASP GenAI](https://genai.owasp.org/2026/09/01/owasp-genai-security-project-unveils-2026-top-10-for-llm-applications-new-agent-control-standard-and-sponsors-as-community-tops-30000-members/)). 부록 B는 2026판 원문으로 작성해야 한다.
- **크로스워크 매트릭스**: 5×6 매트릭스 등급은 연구자의 종합 판단이다. 출간 전에 OWASP 'GenAI Security Industry Framework Crosswalk'(2026-09-01, 미열람)와 대조한다.
- **MITRE ATLAS**: 전술 이름은 이번에 검증하지 못했다. 확인된 것은 5.1.0 기준 16개라는 개수뿐이다. changelog에는 'AI Agent Tool Poisoning'이 두 ID(AML.T0108, AML.T0110)로 나온다([ATLAS CHANGELOG](https://github.com/mitre-atlas/atlas-data/blob/main/CHANGELOG.md)).
- **NIST·CoSAI·CSA**: NIST AI 100-2 §3.5 'Security of Agents' 본문은 읽지 못했다. CoSAI의 'Zero Trust for AI Systems', 'AI Sandboxing', 'MCP Security v2.0'은 제목만 확인했다. 1장의 "인가는 모델 안에 살 수 없다"는 CoSAI 인용은 본문을 읽은 뒤에 쓴다. AICM 18개 도메인 전체 이름도 확인하지 못했다.
- **한국 규제**: 인공지능 기본법과 시행령은 조문을 읽지 못했다. 내용은 로펌 뉴스레터(2등급) 기준이므로 조문 번호는 원문 확인 후 적는다. 과기정통부·KISA 지침 두 건과 금융보안원 평가기준(안) 17개 항목은 언론 보도만 확인했고, 기준(안)은 연말까지 시범 운영되는 초안이다([파이낸셜뉴스](https://www.fnnews.com/news/202610071821048238)). 금융위 가이드라인의 시행일 '22일'은 6월 22일로 해석한 것이다([노컷뉴스](https://www.nocutnews.co.kr/news/6534884)).
- **금융 AI 보안 가이드라인 발행 연도(노트 간 불일치)**: 프레임워크 노트는 '금융분야 AI 보안 가이드라인'을 2023-04-18로 적었다([법률신문](http://www.lawtimes.co.kr/news/articleView.html?idxno=187302)). 독자 수요 노트는 2024-12-19 기사의 "작년 4월"을 근거로 2024년 4월로 추정했다([바이라인네트워크](https://byline.network/2024/12/19-423)). 같은 문서인지, 연도가 맞는지 금융보안원 원문으로 확인해야 한다.
- **설문 수치**: IBM Cost of a Data Breach 2025 수치는 TechRepublic 보도로만 확인했다. 여러 헤드라인에 나오는 '97% 접근 통제 부재'는 연 페이지에 없었다. Gravitee는 벤더 조사이고, 페이지 안에서 2025-12 비교값과 책임자 수치가 서로 맞지 않는다. CSA 설문은 Help Net Security 보도로만 확인했다.
- **사건 세부**: ByteDance 인턴 사건의 'H100 8,000장·수천만 달러 손실'은 회사가 부인했으므로 '미확인'으로 표기한다. Replit의 '가짜 사용자 4,000명'과 Amazon Q의 'wipe 프롬프트'는 1차 출처에 없다. Drift를 'AI 챗 연동'으로 분류한 것은 연구자의 배경지식이므로 Salesloft 자료로 확인한다. 슬롭스쿼팅의 '전체 19.7%'는 초록 페이지에 없다.
- **열지 못한 1차 원문**: Aim Security의 EchoLeak 원문(열람 실패), Koi Security의 postmark-mcp 원문(리다이렉트), Oligo의 ShadowRay 2.0 원문(미열람), Cyera의 Bleeding Llama 원문(CSA 2차 요약만), OpenAI 2025-06 위협 보고서 PDF.
- **노트 간 수치·시점 차이**: ShadowRay 2.0의 시작 시점은 THN이 2025-11 캠페인으로, Dark Reading이 2024-09경 시작으로 적었다([THN](https://thehackernews.com/2025/11/shadowray-20-exploits-unpatched-ray.html), [Dark Reading](https://www.darkreading.com/cyber-risk/shadowray-20-ai-clusters-crypto-botnets)). Ollama 노출 규모는 1,000대 이상(Wiz 2024), 1,139대(Cisco 2025), 약 30만 대(CSA 2026, 별도 조사 17.5만 대)로 방법론마다 다르다. 하나로 합치지 말고 출처와 시점을 붙여 쓴다.
- **악용 여부와 KEV 등재**: CVE-2023-48022·CVE-2026-7482의 CISA KEV 등재 여부를 확인하지 못했다. 추론 서버 CVE가 실제로 악용됐다는 1차 확인도 없다. 운영 중인 RAG·파인튜닝 파이프라인이 외부 공격자에게 실제로 오염된 1차 보고도 찾지 못했다.
- **KB 항목**: Langflow 실제 악용 항목 AISEC-2026-0014의 제목은 CVE-2026-105740이다. 사건 노트는 KEV 날짜 미확인 대상으로 Langflow CVE-2025-3248을 적었다. 두 CVE가 별개인지 확인한 뒤 본문에 쓴다. *(정리: 별개다. AISEC-2026-0014는 2026년 MCP stdio 설정 필드 취약점 CVE-2026-105740·CVE-2026-105697이고, CVE-2025-3248은 2025년의 다른 Langflow 코드 검증 RCE다.)* AISEC-2026-0007은 unverified, AISEC-2026-0016은 partial이므로 인용 수준을 낮춘다.
- **번역서와 기타**: Wilson·Sotiropoulos의 한국어 번역판 존재 여부는 미확인이다. 쿠버네티스 네이티브 지침이 프레임워크에 없다는 판단은 "읽은 범위에서 찾지 못함"이지, 부재가 증명된 것이 아니다. 인젝션 설계 패턴 논문의 저자 수는 arXiv 14명, Willison 11명으로 엇갈린다.

**as-of 날짜를 반드시 붙여야 하는 빠르게 변하는 항목** (모두 2026-10-20 열람 기준. 부록 I에서 관리한다).

- **MCP**: 스펙 revision 2026-07-28. 무상태화, DCR 폐기 예정, Roots·Sampling·Logging 폐기 예정, 최소 12개월 폐기 유예 정책. 2025-06 → 2025-11 → 2026-07로 세 번 크게 바뀌었다. ext-auth의 Enterprise-Managed Authorization은 Stable, Client Credentials는 Draft. 공식 MCP Registry의 GA 여부는 미확인.
- **IETF**: OAuth 2.1 draft-16(2026-09-03), ID-JAG -04(2026-05-21), Transaction Tokens -11(WG 합의, write-up 대기), WIMSE aims-00(2026-09-15). 2026-09-02의 CSA 노트("WG 채택 없음")는 aims 채택으로 이미 낡은 내용이 됐다. DAWN WG는 차터 검토 중.
- **쿠버네티스·CNCF**: Pod Certificates v1.37 stable(릴리스 sign-off 미완 항목 있음), NPEP-133 v1alpha2, agent-sandbox v1.0.2(1.0.x에서도 breaking, 릴리스 연도는 추정), KServe CNCF Incubating, kgateway의 CNCF 단계 미확인.
- **게이트웨이·런타임**: Agent Router v1.0.0(2026-06-23, Envoy AI Gateway에서 개명), agentgateway docs 1.6, Cilium 1.20.3, Kata 4.0, NVIDIA CoCo 1.0.0(Kata 3.29, GPU Operator v26.3.1).
- **탐지 도구**: OTel semconv 1.44.0. GenAI 규약은 별도 저장소로 옮겨졌고 태그 릴리스가 없으며 Development 상태다(2차 출처 기준). garak v0.16.0(연도 추정). PyRIT는 Azure/PyRIT가 2026-03-27에 보관 처리됐고 microsoft/PyRIT가 활성 저장소로 보인다. promptfoo는 OpenAI가 인수했다(2026-03-09, 업계지 기준). Prempti는 early-stage.
- **취약점 버전**: LiteLLM 1.82.7/1.82.8 침해, 정상 버전 v1.83.0. vLLM 0.14.1/0.18.0 수정. Ollama 0.17.1 수정. picklescan 0.0.31 수정. Ray 2.52.0 토큰 인증.
- **표준·프레임워크**: MITRE ATLAS 2026.06, CSA AICM v1.1, OWASP 2026 LLM Top 10·ACS·GenAI Red Teaming Manual v1.0, NIST IR 8596 예비 초안, COSAIS(개념·개요 단계), NCCoE(의견 수렴), AI RMF 개정 진행 중, AI 100-2 2026판 미발견.
- **한국**: AI 기본법 과태료 유예(1년 이상), 금융보안원 기준(안) 시범 운영(연말까지)과 '2026 AI 레드팀 보고서' 예정, 망분리 로드맵 2·3단계 진행 상황 미확인.

---

## 결론

v0에서 v1으로 바뀌는 핵심은 장 수가 아니다. 책이 무엇을 기준으로 쪼개지는가가 바뀐다. 영어권 책은 '공격자가 무엇을 하나'로 장을 나눴다. 반면 사고 근거는 거의 모든 고피해 사건이 같은 실패에서 났다는 점을 보여 준다. 장수명 토큰, 무인증 엔드포인트, 열린 egress다. v1은 그 실패를 막는 통제 단위로 장을 나누고, 생명주기는 그 통제가 적용될 좌표로 쓴다. 이 배치에는 시간에 대한 판단도 들어 있다. 2026년은 egress·워크로드 ID·샌드박스·서명이 1.0 또는 GA에 도달하고, NIST의 에이전트 통제 오버레이는 아직 계획 단계인 해다. 지금 쓰는 책은 표준이 굳기 전에 플랫폼 팀이 실제로 쓸 설계를 먼저 내놓을 수 있다. 다만 그 시기는 짧다. 그래서 본문은 원리와 MUST 요건만 다루고, 버전 세부는 KB가 갱신하는 부록 I에 둔다.

남은 위험은 두 가지다. 하나는 근거의 비대칭이다. 데이터·학습 장은 여전히 연구와 단일 실사고 계열에 기대고 있다. 다음 기초 문헌 수집이 1~7번(데이터·학습)을 먼저 채워야 하는 이유다. 다른 하나는 한국 장이다. 이 책을 국내 경쟁서와 가장 뚜렷하게 구분하는 장인데, 근거의 1차 원문이 하나도 확보되지 않았다. 17장의 조문 번호와 KISA·금융보안원 원문을 확보하는 일이 목차 v1을 사이트에 올리기 전에 처리할 가장 시급한 과제다.

---

## Sources

**책·과정**
- O'Reilly, The Developer's Playbook for LLM Security — https://www.oreilly.com/library/view/-/9781098162191/
- Packt, Adversarial AI Attacks, Mitigations, and Defense Strategies — https://packtpub.com/product/adversarial-ai-attacks-mitigations-and-defense-strategies/9781835087985
- Packt, AI-Native LLM Security — https://subscription.packtpub.com/book/data/9781836203759
- Springer, Securing AI Agents — https://link.springer.com/book/10.1007/978-3-032-02130-4
- No Starch, Red Teaming AI — https://nostarch.com/node/829
- Manning, AI Agents for Offensive Security — https://manning.com/books/ai-agents-for-offensive-security
- SANS SEC545 — https://www.sans.org/cyber-security-courses/genai-llm-application-security-5day
- 교보 eBook, 완벽한 바이브 코딩을 위한 보안 플레이북 — https://ebook-product.kyobobook.co.kr/dig/epd/ebook/E000013194494
- 교보 eBook, 실무로 통하는 LLM 애플리케이션 설계 — https://ebook-product.kyobobook.co.kr/dig/epd/ebook/E000012087744

**표준·프레임워크**
- OWASP LLM Top 10 — https://genai.owasp.org/llm-top-10/
- OWASP Top 10 for Agentic Applications 2026 — https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/
- OWASP GenAI 2026 update — https://genai.owasp.org/2026/09/01/owasp-genai-security-project-unveils-2026-top-10-for-llm-applications-new-agent-control-standard-and-sponsors-as-community-tops-30000-members/
- OWASP Agentic Security Initiative — https://genai.owasp.org/initiatives/agentic-security-initiative/
- OWASP AI Exchange — https://owaspai.org/
- Modulos (ASI 목록, 2차) — https://docs.modulos.ai/frameworks/owasp-top-10-agentic/index
- Giskard (ASI 목록, 2차) — https://www.giskard.ai/knowledge/owasp-top-10-for-agentic-application-2026
- NIST AI 100-2 E2025 — https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-2e2025.pdf ; https://csrc.nist.gov/news/2025/nist-ai-100-2-adversarial-machine-learning-taxonom
- NIST AI RMF — https://www.nist.gov/itl/ai-risk-management-framework
- NIST AI 600-1 — https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf
- NIST SP 800-218A — https://csrc.nist.gov/pubs/sp/800/218/a/final
- NIST IR 8596 — https://csrc.nist.gov/pubs/ir/8596/iprd
- NIST COSAIS — https://csrc.nist.gov/projects/cosais
- NIST NCCoE — https://www.nccoe.nist.gov/projects/software-and-ai-agent-identity-and-authorization ; https://www.nist.gov/news-events/news/2026/02/new-concept-paper-identity-and-authority-software-agents
- NIST CAISI — https://nist.gov/news-events/news/2026/02/announcing-ai-agent-standards-initiative-interoperable-and-secure
- MITRE ATLAS — https://github.com/mitre-atlas/atlas-data/blob/main/CHANGELOG.md ; https://github.com/mitre-atlas/atlas-data
- CSA MAESTRO — https://cloudsecurityalliance.org/blog/2025/02/06/agentic-ai-threat-modeling-framework-maestro
- CSA AICM — https://cloudsecurityalliance.org/artifacts/ai-controls-matrix ; https://labs.cloudsecurityalliance.org/research/csa-research-note-aicm-v1-1-update-20260730-csa-styled/
- Google SAIF — https://saif.google/secure-ai-framework/risks ; https://saif.google/focus-on-agents
- CoSAI — https://www.coalitionforsecureai.org/ ; https://www.coalitionforsecureai.org/announcing-the-cosai-principles-for-secure-by-design-agentic-systems/ ; https://www.oasis-open.org/2025/11/18/coalition-for-secure-ai-releases-two-actionable-frameworks-for-ai-model-signing-and-incident-response
- Databricks DASF v3.0 — https://www.databricks.com/blog/agentic-ai-security-new-risks-and-controls-databricks-ai-security-framework-dasf-v30

**한국 규제·지침·조사**
- 바이라인네트워크 (AI 기본법 시행령) — https://byline.network/2026/01/21-545/
- 법무법인 세종 (AI 기본법) — https://shinkim.com/kor/media/newsletter/3114 ; https://shinkim.com/kor/media/newsletter/pdf/3114
- 법무법인 세종 (망분리 로드맵) — https://shinkim.com/kor/media/newsletter/2533
- law.go.kr 인공지능 기본법 — https://www.law.go.kr/법령/인공지능발전과신뢰기반조성등에관한기본법
- 바이라인네트워크 (KISA 매뉴얼·레드티밍 가이드) — https://byline.network/2026/07/8-489/
- Supple (KISA 가이드) — https://supple.kr/news/cmrbhuk3w003dsdy6byt7gyj4
- 파이낸셜뉴스 (금융보안원 에이전트 평가기준안) — https://www.fnnews.com/news/202610071821048238
- 노컷뉴스 (금융분야 AI 가이드라인) — https://www.nocutnews.co.kr/news/6534884
- 법률신문 (2023 금융분야 AI 보안 가이드라인) — http://www.lawtimes.co.kr/news/articleView.html?idxno=187302
- 바이라인네트워크 (금융보안원 검증체계) — https://byline.network/2024/12/19-423
- 바이라인네트워크 (혁신금융 생성형 AI 보안성 검토) — https://byline.network/2025/02/20-406
- 파이낸셜뉴스 (메가존·Foundry 조사) — https://www.fnnews.com/news/202508260933530786
- 바이라인네트워크 (이스트시큐리티 조사) — https://byline.network/2025/02/5-261/

**독자 수요·컨퍼런스**
- TechRepublic (IBM 2025) — https://www.techrepublic.com/article/news-ai-breach-risks-rise-as-governance-lags/
- Gravitee State of AI Agent Security — https://www.gravitee.io/state-of-ai-agent-security?hl=cs-CZ
- Help Net Security (CSA 에이전트 신원 설문) — https://helpnetsecurity.com/2026/03/26/ciso-ai-agent-identity-security-report/
- CNCF Annual Survey — https://www.linuxfoundation.org/hubfs/Research%20Reports/CNCF_Annual_Survey_Report_1.15.26.pdf?hsLang=en
- CNCF KubeCon NA 2026 발표 — https://www.cncf.io/announcements/2026/08/10/cncf-reveals-kubecon-cloudnativecon-north-america-2026-schedule-adds-new-ai-inference-agentic-track/
- KubeCon India 2026 보안 트랙 — https://kccncind2026.sched.com/2026-06-19/list/descriptions/type/Security
- CSA Labs Identity Sprawl (미열람) — https://labs.cloudsecurityalliance.org/research/csa-research-note-ai-agent-identity-sprawl-authorization-202/

**사건·연구**
- Wiz (Microsoft 38TB) — https://www.wiz.io/blog/38-terabytes-of-private-data-accidentally-exposed-by-microsoft-ai-researchers
- Wiz (DeepSeek) — https://www.wiz.io/blog/wiz-research-uncovers-exposed-deepseek-database-leak
- Truffle Security — https://trufflesecurity.com/blog/research-finds-12-000-live-api-keys-and-passwords-in-deepseek-s-training-data
- NewsGuard — https://www.newsguardrealitycheck.com/p/a-well-funded-moscow-based-global
- PromptArmor (Slack AI) — https://www.promptarmor.com/resources/data-exfiltration-from-slack-ai-via-indirect-prompt-injection
- arXiv 2302.10149 — https://arxiv.org/abs/2302.10149
- arXiv 2402.07867 — https://arxiv.org/abs/2402.07867
- Anthropic (250 docs) — https://www.anthropic.com/research/small-samples-poison
- Oligo (ShadowRay) — https://www.oligo.security/blog/shadowray-attack-ai-workloads-actively-exploited-in-the-wild
- NVD CVE-2023-48022 — https://nvd.nist.gov/vuln/detail/CVE-2023-48022
- The Hacker News (ShadowRay 2.0) — https://thehackernews.com/2025/11/shadowray-20-exploits-unpatched-ray.html
- Dark Reading (ShadowRay 2.0) — https://www.darkreading.com/cyber-risk/shadowray-20-ai-clusters-crypto-botnets
- The Register (ByteDance) — https://www.theregister.com/2024/10/22/bytedance_intern_messed_with_llm/
- OpenAI o1-preview System Card — https://cdn.openai.com/o1-preview-system-card-20240917.pdf
- Anthropic (reward hacking) — https://www.anthropic.com/research/emergent-misalignment-reward-hacking
- arXiv 2401.05566 — https://arxiv.org/abs/2401.05566
- Wiz (CVE-2024-0132) — https://www.wiz.io/blog/wiz-research-critical-nvidia-ai-vulnerability
- Sysdig (LLMjacking) — https://sysdig.com/blog/llmjacking-stolen-cloud-credentials-used-in-new-ai-attack/
- Microsoft (Storm-2139) — https://blogs.microsoft.com/on-the-issues/2025/02/27/disrupting-cybercrime-abusing-gen-ai/
- Anthropic (distillation) — https://www.anthropic.com/news/detecting-and-preventing-distillation-attacks
- arXiv 2403.06634 — https://arxiv.org/abs/2403.06634
- Wiz (Probllama) — https://www.wiz.io/blog/probllama-ollama-vulnerability-cve-2024-37032
- Cisco (Ollama 노출) — https://blogs.cisco.com/security/detecting-exposed-llm-servers-shodan-case-study-on-ollama
- Anthropic (2025-08 threat report) — https://www.anthropic.com/news/detecting-countering-misuse-aug-2025
- Anthropic (espionage) — https://www.anthropic.com/news/disrupting-AI-espionage
- Google GTIG (AI Threat Tracker) — https://cloud.google.com/blog/topics/threat-intelligence/threat-actor-usage-of-ai-tools
- NVD CVE-2025-32711 — https://nvd.nist.gov/vuln/detail/CVE-2025-32711
- Invariant Labs (GitHub MCP) — https://invariantlabs.ai/blog/mcp-github-vulnerability
- General Analysis (Supabase MCP) — https://generalanalysis.com/blog/supabase-mcp-blog
- eWeek (Replit) — https://www.eweek.com/news/replit-ai-coding-assistant-failure/
- NVD CVE-2025-3248 — https://nvd.nist.gov/vuln/detail/CVE-2025-3248
- JFrog (HF 악성 모델) — https://jfrog.com/blog/data-scientists-targeted-by-malicious-hugging-face-ml-models-with-silent-backdoor/
- ReversingLabs (nullifAI) — https://www.reversinglabs.com/blog/rl-identifies-malware-ml-model-hosted-on-hugging-face
- Wiz (HF 인프라) — https://www.wiz.io/blog/wiz-and-hugging-face-address-risks-to-ai-infrastructure
- Hugging Face (Spaces secrets) — https://huggingface.co/blog/space-secrets-disclosure
- PyPI (Ultralytics) — https://blog.pypi.org/posts/2024-12-11-ultralytics-attack-analysis/
- ReversingLabs (Ultralytics) — https://www.reversinglabs.com/blog/compromised-ultralytics-pypi-package-delivers-crypto-coinminer
- GitHub Advisory GHSA-cxm3-wv7p-598c (Nx) — https://github.com/nrwl/nx/security/advisories/GHSA-cxm3-wv7p-598c
- Wiz (s1ngularity) — https://www.wiz.io/blog/s1ngularity-supply-chain-attack
- AWS-2025-015 (Amazon Q) — https://aws.amazon.com/security/security-bulletins/AWS-2025-015/
- The Hacker News (postmark-mcp) — https://thehackernews.com/2025/09/first-malicious-mcp-server-found.html
- Google GTIG (Salesloft Drift) — https://cloud.google.com/blog/topics/threat-intelligence/data-theft-salesforce-instances-via-salesloft-drift
- OpenAI (Mixpanel) — https://openai.com/index/mixpanel-incident/
- arXiv 2406.10279 — https://arxiv.org/abs/2406.10279

**플랫폼 통제 기술**
- MCP changelog 2026-07-28 — https://modelcontextprotocol.io/specification/2026-07-28/changelog
- MCP Authorization 2026-07-28 — https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization
- MCP ext-auth — https://github.com/modelcontextprotocol/ext-auth
- OAuth 2.1 — https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/
- ID-JAG — https://datatracker.ietf.org/doc/draft-ietf-oauth-identity-assertion-authz-grant/
- Transaction Tokens — https://datatracker.ietf.org/doc/draft-ietf-oauth-transaction-tokens/
- WIMSE documents — https://datatracker.ietf.org/wg/wimse/documents/
- draft-ietf-wimse-aims — https://datatracker.ietf.org/doc/draft-ietf-wimse-aims/
- CSA research note (IETF agent identity) — https://labs.cloudsecurityalliance.org/research/csa-research-note-ietf-agent-identity-standards-20260902-csa/
- CNCF projects — https://www.cncf.io/projects/
- KEP-4317 — https://www.kubernetes.dev/resources/keps/4317/
- AWS AgentCore Policy — https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html
- Agent Router v1.0 — https://theagentrouter.ai/release-notes/v1.0/
- agentgateway — https://agentgateway.dev/docs/standalone/main/documentation/about/introduction/
- Cilium policy — https://docs.cilium.io/en/stable/security/policy/index.html ; https://docs.cilium.io/en/stable/security/policy/layer3/
- NPEP-133 — https://network-policy-api.sigs.k8s.io/npeps/npep-133-fqdn-egress-selector/
- LiteLLM security update — https://docs.litellm.ai/blog/security-update-march-2026
- agent-sandbox — https://github.com/kubernetes-sigs/agent-sandbox ; https://github.com/kubernetes-sigs/agent-sandbox/releases
- OpenInfra newsletter July 2026 (Kata 4.0) — https://openinfra.org/blog/openinfra-newsletter-july-2026
- Fly.io (Firecracker vs gVisor) — https://fly.io/learn/firecracker-vs-gvisor/
- NVIDIA CoCo 1.0.0 — https://docs.nvidia.com/datacenter/cloud-native/confidential-containers/1.0.0/release-notes.html
- NVIDIA MIG — https://docs.nvidia.com/datacenter/tesla/mig-user-guide/latest/introduction.html
- arXiv 2503.18813 (CaMeL) — https://arxiv.org/abs/2503.18813
- arXiv 2506.08837 — https://arxiv.org/abs/2506.08837 ; https://simonwillison.net/2025/Jun/13/prompt-injection-design-patterns/
- OpenSSF OMS — https://openssf.org/blog/2025/06/25/
- sigstore/model-transparency — https://github.com/sigstore/model-transparency
- NVIDIA NGC signing — https://developer.nvidia.com/blog/bringing-verifiable-trust-to-ai-models-model-signing-in-ngc
- SLSA v1.2 — https://slsa.dev/blog/2025/11/announce-slsa-v1.2
- CycloneDX — https://cyclonedx.org/specification/overview/ ; https://cyclonedx.org/capabilities/mlbom/
- arXiv 2510.07070 — https://arxiv.org/abs/2510.07070
- JFrog (picklescan) — https://jfrog.com/blog/unveiling-3-zero-day-vulnerabilities-in-picklescan/
- GitLab advisory vLLM CVE-2026-27893 — https://advisories.gitlab.com/pypi/vllm/CVE-2026-27893/
- GitLab advisory vLLM CVE-2026-22778 — https://advisories.gitlab.com/pypi/vllm/CVE-2026-22778/
- MCP Registry — https://registry.modelcontextprotocol.io/
- CSA research note (Bleeding Llama) — https://labs.cloudsecurityalliance.org/research/csa-research-note-ollama-bleeding-llama-cve-2026-7482-ai-inf
- CNCF KServe — https://www.cncf.io/projects/kserve/
- opentelemetry.io gen-ai — https://opentelemetry.io/docs/specs/semconv/gen-ai/
- semantic-conventions-genai — https://github.com/open-telemetry/semantic-conventions-genai
- Dash0 (OTel GenAI, 2차) — https://www.dash0.com/knowledge/opentelemetry-genai-semantic-conventions-explained
- arXiv 2510.09023 — https://arxiv.org/abs/2510.09023
- arXiv 2505.03574 (LlamaFirewall) — https://arxiv.org/abs/2505.03574
- garak releases — https://github.com/NVIDIA/garak/releases
- PyRIT — https://github.com/Azure/PyRIT/releases ; https://github.com/microsoft/PyRIT
- Security Boulevard (promptfoo) — https://securityboulevard.com/2026/03/openai-acquires-security-startup-promptfoo-to-fortify-ai-agents
- Sysdig (Prempti) — https://www.sysdig.com/blog/introducing-prempti-runtime-security-for-ai-coding-agents-powered-by-falco

**지식 베이스 항목 (front matter 기준)**: AISEC-2026-0001 ~ AISEC-2026-0020 (`/home/claude/ai-security-kb/content/items/`)
