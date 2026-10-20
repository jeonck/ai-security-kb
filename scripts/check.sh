#!/usr/bin/env bash
# 콘텐츠 검증: 항목 스키마·두 축 어휘·출처 메타데이터·URL 중복·다이제스트 참조·날짜(kb.py validate) + Hugo 빌드.
# 통과하면 마지막 줄에 OK를 출력하고 0으로 끝난다.
set -euo pipefail
cd "$(dirname "$0")/.."

if ! python3 -c "import yaml" 2>/dev/null; then
  pip install -q pyyaml 2>/dev/null || pip install -q --break-system-packages pyyaml
fi

fail=0
python3 scripts/kb.py validate || fail=1

if command -v hugo >/dev/null 2>&1; then
  out=$(mktemp -d)
  if ! hugo --quiet --enableGitInfo=false --destination "$out" >/dev/null 2>"$out.err"; then
    echo "FAIL hugo 빌드"; cat "$out.err"; fail=1
  fi
  rm -rf "$out" "$out.err"
else
  echo "SKIP hugo 없음 — 빌드 확인은 GitHub Actions에 맡김"
fi

[ "$fail" -eq 0 ] || exit 1
echo OK
