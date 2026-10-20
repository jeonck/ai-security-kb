#!/usr/bin/env bash
# 콘텐츠 검증: 미래 날짜, catalog URL 중복, 필수 front matter, Hugo 빌드.
# 통과하면 마지막 줄에 OK를 출력하고 0으로 끝난다.
set -euo pipefail
cd "$(dirname "$0")/.."

fail=0
now_epoch=$(date +%s)

for f in content/digest/*.md content/weekly/*.md; do
  [ -e "$f" ] || continue
  case "$(basename "$f")" in _index.md) continue;; esac
  fm=$(awk 'NR==1 && $0=="---"{infm=1; next} infm && $0=="---"{exit} infm{print}' "$f")
  for key in title date slug description; do
    if ! printf '%s\n' "$fm" | grep -q "^${key}:"; then
      echo "FAIL $f: front matter에 ${key} 없음"; fail=1
    fi
  done
  d=$(printf '%s\n' "$fm" | sed -n 's/^date:[[:space:]]*//p' | tr -d '"' | head -1)
  if [ -n "$d" ]; then
    if ! e=$(date -d "$d" +%s 2>/dev/null); then
      echo "FAIL $f: 날짜 형식 오류 ($d)"; fail=1
    elif [ "$e" -gt "$now_epoch" ]; then
      echo "FAIL $f: 날짜가 미래 ($d)"; fail=1
    fi
  fi
done

# catalog.md 표에서 원문 URL 중복 검사 (4번째 열의 링크)
dups=$(grep -E '^\| ' content/catalog.md | grep -oE '\[링크\]\([^)]+\)' | sort | uniq -d || true)
if [ -n "$dups" ]; then
  echo "FAIL catalog.md: 중복 URL"; echo "$dups"; fail=1
fi

# catalog에서 가리키는 digest 파일이 실제로 있는지
for slug in $(grep -oE '\(\.\./digest/[0-9]{4}-[0-9]{2}-[0-9]{2}/\)' content/catalog.md | grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}' | sort -u); do
  [ -f "content/digest/${slug}.md" ] || { echo "FAIL catalog.md: digest/${slug}.md 없음"; fail=1; }
done

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
