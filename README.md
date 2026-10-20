# AI Security KB

AI 보안(프롬프트 인젝션, 에이전트·MCP 보안, 모델 공격 연구, AI 공급망, 개인정보, 규제) 뉴스와 연구를
자동으로 수집·요약해 쌓는 지식 베이스입니다.

- 사이트: https://jeonck.github.io/ai-security-kb/
- 6시간마다: 4개 도메인을 병렬 리서처가 수집 → 검증·중복 제거 → `content/digest/` 에 추가
- 매주 월요일: 지난 7일을 종합한 심층 리포트 → `content/weekly/`
- 전체 목록: [`content/catalog.md`](content/catalog.md)
- 작업 규칙과 형식: [`CLAUDE.md`](CLAUDE.md)

모든 추가·수정은 커밋으로 남으므로, 어떤 항목이 언제 들어왔는지 `git log -- content/` 로 추적할 수 있습니다.
요약은 원문을 대체하지 않습니다. 각 항목의 출처 링크에서 원문을 확인하세요.

## 로컬에서 보기

```bash
hugo server
./scripts/check.sh   # 콘텐츠 검증
```
