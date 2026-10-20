# AI Security KB

AI 보안(프롬프트 인젝션, 에이전트·MCP 보안, 모델 공격 연구, AI 공급망, 개인정보, 규제) 뉴스와 연구를
자동으로 수집·요약해 쌓는 지식 베이스입니다.

- 사이트: https://jeonck.github.io/ai-security-kb/
- 6시간마다: 4개 도메인을 병렬 리서처가 수집 → 1차 원문 확인 → 항목 카드(`content/items/`) + 다이제스트(`content/digest/`), 깊게 볼 사건엔 "심층 후보" 표시
- 매주 화·금: 집필 매트릭스의 빈 칸을 채울 기초 문헌 → `content/items/`
- 매주 월요일: 딥 리서치 스킬로 지난 7일을 종합하고 "심층 후보" 사건을 깊게 분석한 리포트 → `content/weekly/`
- 딥 리서치가 어디에 쓰이는지: [시스템 › 딥 리서치는 어디에 쓰이나](https://jeonck.github.io/ai-security-kb/system/deep-research/)
- 전체 목록: [`content/catalog.md`](content/catalog.md)
- 작업 규칙과 형식: [`CLAUDE.md`](CLAUDE.md)

모든 추가·수정은 커밋으로 남으므로, 어떤 항목이 언제 들어왔는지 `git log -- content/` 로 추적할 수 있습니다.
요약은 원문을 대체하지 않습니다. 각 항목의 출처 링크에서 원문을 확인하세요.

## 로컬에서 보기

```bash
hugo server
./scripts/check.sh   # 콘텐츠 검증
```
