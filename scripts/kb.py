#!/usr/bin/env python3
"""AI Security KB 도구.

  python3 scripts/kb.py validate              항목·다이제스트·상태 파일 검증 (OK면 0)
  python3 scripts/kb.py next-id               다음 항목 ID
  python3 scripts/kb.py find <url-or-text>    출처 URL·제목·식별자로 기존 항목 찾기 (중복 판정)
  python3 scripts/kb.py coverage              생명주기 × 통제 매트릭스 건수와 빈칸
  python3 scripts/kb.py deep-dives            아직 주간 리포트에서 다루지 않은 심층 후보 (deep_dive: true)
  python3 scripts/kb.py export-day <date>     그날 다이제스트 + 항목 전문을 하나의 마크다운으로 (프로젝트 사본용)
  python3 scripts/kb.py export-index          전체 목록 마크다운 (프로젝트 ai-security/index.md용)
  python3 scripts/kb.py bib                   참고문헌 BibTeX
  python3 scripts/kb.py csl                   참고문헌 CSL-JSON
"""
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("PyYAML이 필요합니다: pip install pyyaml (샌드박스: --break-system-packages)")

ROOT = Path(__file__).resolve().parent.parent
ITEMS = ROOT / "content" / "items"
DIGEST = ROOT / "content" / "digest"
WEEKLY = ROOT / "content" / "weekly"
AXES = yaml.safe_load((ROOT / "data" / "axes.yaml").read_text(encoding="utf-8"))
STATE = ROOT / "data" / "state.yaml"

ID_RE = re.compile(r"^AISEC-(\d{4})-(\d{4})$")
SHORTCODE_RE = re.compile(r"\{\{<\s*items\s+([^>]*?)\s*>\}\}")
REQUIRED_SECTIONS = ["## 요약", "## 동작 원리", "## 플랫폼 엔지니어 관점"]
CT = dt.timezone(dt.timedelta(hours=-5))  # 비교용 여유: CDT. 미래 판정은 하루 여유를 둔다


def now_ct():
    return dt.datetime.now(dt.timezone.utc).astimezone(CT)


def split_front_matter(text):
    if not text.startswith("---\n"):
        raise ValueError("front matter(---)로 시작하지 않음")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("front matter 끝(---)을 찾지 못함")
    return yaml.safe_load(text[4:end]) or {}, text[end + 5:]


YAML_ERRORS = []


def load_items():
    items = []
    for p in sorted(ITEMS.glob("AISEC-*.md")):
        try:
            fm, body = split_front_matter(p.read_text(encoding="utf-8"))
        except Exception as ex:  # 깨진 YAML은 검증 실패로 보고하고 건너뛴다
            YAML_ERRORS.append(f"{p.name}: front matter를 읽지 못함 — {str(ex).splitlines()[0]} (문자열 안의 큰따옴표·콜론을 확인)")
            continue
        fm["_path"] = p
        fm["_body"] = body
        items.append(fm)
    return items


def load_digests():
    out = []
    for p in sorted(DIGEST.glob("*.md")):
        if p.name == "_index.md":
            continue
        fm, body = split_front_matter(p.read_text(encoding="utf-8"))
        ids = []
        for m in SHORTCODE_RE.finditer(body):
            ids += re.findall(r'"([^"]+)"', m.group(1))
        out.append({"path": p, "fm": fm, "body": body, "ids": ids})
    return out


def norm_url(u):
    s = urlsplit(u.strip())
    path = s.path.rstrip("/") or "/"
    return urlunsplit((s.scheme.lower(), s.netloc.lower().removeprefix("www."), path, s.query, ""))


def as_date(v):
    if isinstance(v, dt.datetime):
        return v.date()
    if isinstance(v, dt.date):
        return v
    if isinstance(v, str):
        return dt.date.fromisoformat(v[:10])
    raise ValueError(f"날짜 아님: {v!r}")


def keys(axis):
    return [x["key"] for x in AXES[axis]]


def label(axis, key):
    for x in AXES[axis]:
        if x["key"] == key:
            return x["label"]
    return key


# ---------------------------------------------------------------- validate
def validate():
    errs, warns = [], []
    items = load_items()
    errs += YAML_ERRORS
    ids = {}
    url_owner = {}
    today = now_ct().date() + dt.timedelta(days=1)
    lc_keys, ctl_keys = keys("lifecycle"), keys("controls")

    for it in items:
        p = it["_path"].name
        e = lambda msg: errs.append(f"{p}: {msg}")
        iid = it.get("id", "")
        if not ID_RE.match(str(iid)):
            e(f"id 형식 오류 ({iid!r})")
        elif p != f"{iid}.md":
            e(f"파일명과 id 불일치 ({iid})")
        if iid in ids:
            e(f"id 중복 ({iid}, {ids[iid]})")
        ids[iid] = p
        for f in ["title", "summary", "date", "date_precision", "collected", "item_type", "track",
                  "categories", "lifecycle", "controls", "tags", "identifiers", "status",
                  "sources", "claims", "book_note"]:
            if it.get(f) in (None, "", []) and f not in ("tags",):
                e(f"필수 필드 없음: {f}")
        try:
            if as_date(it.get("date")) > today:
                e(f"date가 미래 ({it.get('date')})")
        except Exception as ex:
            e(f"date 오류: {ex}")
        if it.get("date_precision") not in ("day", "month", "year"):
            e("date_precision은 day/month/year")
        if "type" in it:
            e("type 필드는 쓰지 않는다 (Hugo 예약어). item_type 사용")
        if it.get("item_type") not in AXES["types"]:
            e(f"item_type 값 오류 ({it.get('item_type')})")
        if it.get("track") not in ("news", "foundation"):
            e("track은 news/foundation")
        cats = it.get("categories") or []
        if not (isinstance(cats, list) and len(cats) == 1 and cats[0] in AXES["categories"]):
            e(f"categories는 정해진 값 1개짜리 리스트 ({cats})")
        lc = it.get("lifecycle") or []
        if not (1 <= len(lc) <= 2) or any(k not in lc_keys for k in lc):
            e(f"lifecycle은 {lc_keys} 중 1~2개 ({lc})")
        ctl = it.get("controls") or []
        if not (1 <= len(ctl) <= 3) or any(k not in ctl_keys for k in ctl):
            e(f"controls는 {ctl_keys} 중 1~3개 ({ctl})")
        for t in it.get("tags") or []:
            if not re.match(r"^[a-z0-9][a-z0-9-]*$", str(t)):
                warns.append(f"{p}: 태그 형식(소문자-하이픈) 아님: {t}")
        ident = it.get("identifiers") or {}
        for k in ("cve", "ghsa", "arxiv", "doi"):
            if not isinstance(ident.get(k, []), list):
                e(f"identifiers.{k}는 리스트")
        if it.get("status") not in ("confirmed", "partial", "unverified"):
            e("status는 confirmed/partial/unverified")

        srcs = it.get("sources") or []
        skeys = set()
        has_primary1 = False
        for i, s in enumerate(srcs):
            sk = s.get("key")
            if not sk or sk in skeys:
                e(f"sources[{i}].key 없음 또는 중복")
            skeys.add(sk)
            if s.get("role") not in ("primary", "coverage"):
                e(f"sources[{sk}].role은 primary/coverage")
            if s.get("tier") not in (1, 2, 3):
                e(f"sources[{sk}].tier는 1/2/3")
            for f in ("title", "outlet", "url"):
                if not s.get(f):
                    e(f"sources[{sk}].{f} 없음")
            if not s.get("accessed") and it.get("status") != "unverified":
                e(f"sources[{sk}].accessed 없음 (열어 읽은 출처만 남긴다. 원문을 못 열었으면 status: unverified)")
            if s.get("published"):
                try:
                    if as_date(s["published"]) > today:
                        e(f"sources[{sk}].published가 미래")
                except Exception as ex:
                    e(f"sources[{sk}].published 오류: {ex}")
            if s.get("role") == "primary" and s.get("tier") == 1:
                has_primary1 = True
            if s.get("url"):
                nu = norm_url(s["url"])
                prev = url_owner.get(nu)
                if prev and prev != iid:
                    e(f"출처 URL이 {prev}와 중복: {s['url']}")
                url_owner[nu] = iid
        if it.get("status") == "confirmed" and not has_primary1:
            e("status: confirmed 인데 role: primary, tier: 1 출처가 없음")
        claims = it.get("claims") or []
        if len(claims) < 2:
            e("claims는 2개 이상")
        for i, c in enumerate(claims):
            if not c.get("text"):
                e(f"claims[{i}].text 없음")
            if c.get("source") not in skeys:
                e(f"claims[{i}].source가 sources key가 아님 ({c.get('source')})")
            if not c.get("locator"):
                e(f"claims[{i}].locator 없음")
        dd = it.get("deep_dive", False)
        if dd not in (True, False):
            e("deep_dive는 true/false")
        if dd is True and not str(it.get("deep_dive_reason") or "").strip():
            e("deep_dive: true 인데 deep_dive_reason이 없음")
        body = it["_body"]
        for sec in REQUIRED_SECTIONS:
            if sec not in body:
                e(f"본문 섹션 없음: {sec}")

    for it in items:
        for r in it.get("related") or []:
            if r not in ids:
                errs.append(f"{it['_path'].name}: related에 없는 ID ({r})")

    referenced = {}
    for d in load_digests():
        dp = d["path"].name
        for f in ("title", "date", "slug", "description"):
            if not d["fm"].get(f):
                errs.append(f"digest/{dp}: front matter {f} 없음")
        try:
            if as_date(d["fm"].get("date")) > today:
                errs.append(f"digest/{dp}: date가 미래")
        except Exception as ex:
            errs.append(f"digest/{dp}: date 오류: {ex}")
        for i in d["ids"]:
            if i not in ids:
                errs.append(f"digest/{dp}: 없는 항목 ID ({i})")
            referenced.setdefault(i, []).append(dp)
    for i in ids:
        if i not in referenced:
            errs.append(f"{i}: 어느 다이제스트에도 실리지 않음")

    for p in sorted(WEEKLY.glob("*.md")):
        if p.name == "_index.md":
            continue
        fm, _ = split_front_matter(p.read_text(encoding="utf-8"))
        for f in ("title", "date", "slug", "description"):
            if not fm.get(f):
                errs.append(f"weekly/{p.name}: front matter {f} 없음")
        for i in fm.get("deep_dives") or []:
            if i not in ids:
                errs.append(f"weekly/{p.name}: deep_dives에 없는 항목 ID ({i})")

    if STATE.exists():
        st = yaml.safe_load(STATE.read_text(encoding="utf-8")) or {}
        if not st.get("last_run"):
            errs.append("data/state.yaml: last_run 없음")
    else:
        errs.append("data/state.yaml 없음")

    for w in warns:
        print("WARN", w)
    for x in errs:
        print("FAIL", x)
    if errs:
        return 1
    print(f"OK validate ({len(items)} items)")
    return 0


# ---------------------------------------------------------------- helpers
def next_id():
    year = now_ct().year
    n = 0
    for p in ITEMS.glob(f"AISEC-{year}-*.md"):
        m = ID_RE.match(p.stem)
        if m:
            n = max(n, int(m.group(2)))
    print(f"AISEC-{year}-{n + 1:04d}")


def find(q):
    qn = norm_url(q) if q.startswith("http") else None
    ql = q.lower()
    hits = []
    for it in load_items():
        why = []
        for s in it.get("sources") or []:
            if qn and norm_url(s.get("url", "")) == qn:
                why.append(f"url {s['url']}")
            elif not qn and (ql in str(s.get("title", "")).lower() or ql in str(s.get("url", "")).lower()):
                why.append(f"source {s.get('key')}")
        if not qn:
            if ql in str(it.get("title", "")).lower():
                why.append("title")
            for k, v in (it.get("identifiers") or {}).items():
                if any(ql == str(x).lower() for x in v):
                    why.append(f"{k}")
        if why:
            hits.append((it["id"], it["title"], ", ".join(why)))
    for h in hits:
        print(" | ".join(h))
    if not hits:
        print("NOT FOUND")
    return 0


def coverage():
    items = load_items()
    lc, ctl = AXES["lifecycle"], AXES["controls"]
    grid = {(a["key"], b["key"]): [] for a in lc for b in ctl}
    for it in items:
        for a in it.get("lifecycle") or []:
            for b in it.get("controls") or []:
                grid.setdefault((a, b), []).append(it["id"])
    w = 10
    print("생명주기\\통제".ljust(14) + "".join(b["label"][:6].ljust(w) for b in ctl))
    for a in lc:
        print(a["label"][:8].ljust(14) + "".join(str(len(grid[(a["key"], b["key"])])).ljust(w) for b in ctl))
    empty = [f"{a['label']}×{b['label']}" for a in lc for b in ctl if not grid[(a["key"], b["key"])]]
    thin = [f"{a['label']}×{b['label']}" for a in lc for b in ctl if len(grid[(a["key"], b["key"])]) == 1]
    print(f"\n빈 칸 {len(empty)}개: " + ", ".join(empty))
    print(f"1건뿐인 칸 {len(thin)}개: " + ", ".join(thin))
    rows = {a["label"]: sum(1 for it in items if a["key"] in (it.get("lifecycle") or [])) for a in lc}
    cols = {b["label"]: sum(1 for it in items if b["key"] in (it.get("controls") or [])) for b in ctl}
    print("\n생명주기별:", rows)
    print("통제별:", cols)
    found = sum(1 for it in items if it.get("track") == "foundation")
    print(f"기초 문헌 {found}건 / 뉴스 {len(items) - found}건")
    return 0


def covered_deep_dives():
    done = {}
    for p in sorted(WEEKLY.glob("*.md")):
        if p.name == "_index.md":
            continue
        fm, _ = split_front_matter(p.read_text(encoding="utf-8"))
        for i in fm.get("deep_dives") or []:
            done.setdefault(i, []).append(p.stem)
    return done


def deep_dives():
    done = covered_deep_dives()
    pending = [it for it in load_items() if it.get("deep_dive") is True and it["id"] not in done]
    pending.sort(key=lambda x: str(x.get("collected")), reverse=True)
    for it in pending:
        print(f"{it['id']} | {it['title']} | {it.get('deep_dive_reason', '')}")
    if not pending:
        print("NONE")
    covered = [f"{i} → {', '.join(w)}" for i, w in done.items()]
    if covered:
        print("\n이미 다룬 심층 후보: " + "; ".join(covered))
    return 0


def item_markdown(it, heading="###"):
    srcs = {s["key"]: s for s in it.get("sources") or []}
    lines = [f"{heading} {it['id']} — {it['title']}", ""]
    lines.append(f"- 날짜: {it['date']} · 유형: {it['item_type']} · 상태: {it['status']} · 분류: {', '.join(it['categories'])}")
    lines.append(f"- 생명주기: {', '.join(label('lifecycle', k) for k in it['lifecycle'])} · 통제: {', '.join(label('controls', k) for k in it['controls'])}")
    lines.append(f"- 요약: {it['summary']}")
    lines.append(f"- 집필 메모: {it.get('book_note', '')}")
    if it.get("deep_dive") is True:
        lines.append(f"- 심층 후보: {it.get('deep_dive_reason', '')}")
    body = re.sub(r"^## ", "#### ", it["_body"].strip(), flags=re.M)
    lines += ["", body, "", "주장과 출처:"]
    for c in it.get("claims") or []:
        s = srcs.get(c["source"], {})
        asof = f", 기준일 {c['as_of']}" if c.get("as_of") else ""
        lines.append(f"- {c['text']} — [{s.get('outlet', '?')}]({s.get('url', '')}) {c['locator']}{asof}")
    lines += ["", "출처:"]
    for s in it.get("sources") or []:
        au = ", ".join(s.get("authors") or [])
        lines.append(f"- [{s['key']}] ({'1차' if s['role'] == 'primary' else '보도'}, {s['tier']}등급) {au + '. ' if au else ''}\"{s['title']}\". {s['outlet']}, {s.get('published', '')}. {s['url']} ({'열람 ' + str(s['accessed']) if s.get('accessed') else '원문 미열람'})")
    if it.get("followup"):
        lines.append(f"\n후속 추적: {it['followup']}")
    return "\n".join(lines)


def export_day(day):
    items = {it["id"]: it for it in load_items()}
    d = next((x for x in load_digests() if x["path"].stem == day), None)
    if not d:
        sys.exit(f"digest {day} 없음")
    out = [f"# {d['fm']['title']}", "", d["fm"].get("description", ""), ""]
    body = SHORTCODE_RE.sub(lambda m: "\n\n".join(item_markdown(items[i]) for i in re.findall(r'"([^"]+)"', m.group(1)) if i in items), d["body"])
    out.append(body.strip())
    print("\n".join(out))
    return 0


def export_index():
    items = sorted(load_items(), key=lambda x: (str(x["date"]), x["id"]), reverse=True)
    st = yaml.safe_load(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}
    out = ["# AI 보안 지식 베이스 — 전체 목록", "",
           "레포 jeonck/ai-security-kb 의 사본. 원본과 규칙은 레포 CLAUDE.md, 항목 형식은 docs/item-format.md.", "",
           f"- 마지막 실행: {st.get('last_run', '')}", f"- 누적 항목: {len(items)}", "",
           "| ID | 날짜 | 생명주기 | 통제 | 제목 | 1차 출처 | 상태 |", "|---|---|---|---|---|---|---|"]
    for it in items:
        prim = next((s for s in it["sources"] if s["role"] == "primary"), it["sources"][0])
        out.append(f"| {it['id']} | {it['date']} | {', '.join(label('lifecycle', k) for k in it['lifecycle'])} | {', '.join(label('controls', k) for k in it['controls'])} | {it['title']} | [{prim['outlet']}]({prim['url']}) | {it['status']} |")
    fu = [f"- {it['id']}: {it['followup']}" for it in items if it.get("followup")]
    out += ["", "## 후속 추적", ""] + (fu or ["- 없음"])
    print("\n".join(out))
    return 0


def _bib_key(it, s):
    return f"{it['id'].lower().replace('-', '')}{s['key']}"


def bib():
    out = []
    for it in load_items():
        for s in it.get("sources") or []:
            kind = "article" if s.get("outlet") == "arXiv" else "online"
            pub = as_date(s["published"]) if s.get("published") else None
            esc = lambda v: str(v).replace("{", "\\{").replace("}", "\\}")
            fields = [
                f"  title = {{{{{esc(s['title'])}}}}}",
                f"  author = {{{esc(' and '.join(s.get('authors') or []) or s['outlet'])}}}",
                f"  {'journal' if kind == 'article' else 'organization'} = {{{esc(s['outlet'])}}}",
                f"  url = {{{s['url']}}}",
            ]
            if pub:
                fields += [f"  year = {{{pub.year}}}", f"  date = {{{pub.isoformat()}}}"]
            if s.get("accessed"):
                fields.append(f"  urldate = {{{as_date(s['accessed']).isoformat()}}}")
            fields.append(f"  note = {{{it['id']}, {'primary' if s['role'] == 'primary' else 'coverage'}, tier {s['tier']}}}")
            out.append(f"@{kind}{{{_bib_key(it, s)},\n" + ",\n".join(fields) + "\n}")
    print("\n\n".join(out))
    return 0


def csl():
    out = []
    for it in load_items():
        for s in it.get("sources") or []:
            e = {
                "id": _bib_key(it, s),
                "type": "article" if s.get("outlet") == "arXiv" else "webpage",
                "title": s["title"],
                "container-title": s["outlet"],
                "URL": s["url"],
                "note": f"{it['id']}; {s['role']}; tier {s['tier']}",
            }
            if s.get("authors"):
                e["author"] = [{"literal": a} for a in s["authors"]]
            else:
                e["author"] = [{"literal": s["outlet"]}]
            if s.get("published"):
                d = as_date(s["published"])
                e["issued"] = {"date-parts": [[d.year, d.month, d.day]]}
            if s.get("accessed"):
                d = as_date(s["accessed"])
                e["accessed"] = {"date-parts": [[d.year, d.month, d.day]]}
            out.append(e)
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 0


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    cmd, args = argv[1], argv[2:]
    if cmd == "validate":
        return validate()
    if cmd == "next-id":
        return next_id() or 0
    if cmd == "find" and args:
        return find(" ".join(args))
    if cmd == "coverage":
        return coverage()
    if cmd == "deep-dives":
        return deep_dives()
    if cmd == "export-day" and args:
        return export_day(args[0])
    if cmd == "export-index":
        return export_index()
    if cmd == "bib":
        return bib()
    if cmd == "csl":
        return csl()
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
