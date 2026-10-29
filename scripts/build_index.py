#!/usr/bin/env python3
"""Scan the repo's content folders and generate the data the hub site reads.

Outputs (all git-ignored, rebuilt on every run):
  site/data/index.json   the content index (+ search.json for the command palette)
  site/writeups/ series/ one static page per write-up and per series
  site/media/            images referenced by write-ups
  site/feed.xml, sitemap.xml
  site/img/              copy of src/img (logo, favicon)
  site/live/...          copies of any content folder that ships an index.html

Optional:
  --readme   also rewrite the "Latest Blog Posts" table in README.md

Needs `pip install -r scripts/requirements.txt` (markdown-it-py, pygments) for the reading pages,
and full git history for accurate dates (actions/checkout with fetch-depth: 0).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import urllib.request
import shutil
import subprocess
import sys
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"

REPO = "L0WK3Y-IAAN/Hunting-With-L0WK3Y"
BRANCH = "main"
SITE_NAME = "Hunting With L0WK3Y"
SITE_URL = "https://l0wk3y-iaan.github.io/Hunting-With-L0WK3Y/"
GITHUB = f"https://github.com/{REPO}"

# Type id -> label, in the order the sections appear on the site.
TYPES = {
    "writeups": "Write-ups",
    "tools": "Tools",
    "cheatsheets": "Cheat Sheets",
    "curated": "Curated Links",
    "projects": "Projects",
}

CODE_EXT = {".py", ".js", ".sh", ".ps1", ".rb", ".go", ".rs", ".java", ".kt", ".c", ".cpp", ".ts"}
LANG_BY_EXT = {".py": "Python", ".js": "JavaScript", ".sh": "Shell", ".ps1": "PowerShell",
               ".rb": "Ruby", ".go": "Go", ".rs": "Rust", ".java": "Java", ".kt": "Kotlin",
               ".c": "C", ".cpp": "C++", ".ts": "TypeScript"}
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".github", "img", "src", "images", "assets"}
README_RE = re.compile(r"^readme\.md$", re.I)
FRONT_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", re.S)


# ---------------------------------------------------------------- git dates
def git_dates() -> dict[str, tuple[int, int]]:
    """path -> (created, last_modified) as unix timestamps, from one git pass.

    Renames/moves carry the original creation date, so reorganising folders
    does not reshuffle chronology. Deleted-then-re-added paths keep their first date.
    """
    try:
        out = subprocess.run(
            ["git", "-c", "core.quotepath=off", "log", "--reverse", "-M", "--format=@%ct", "--name-status"],
            cwd=ROOT, capture_output=True, text=True, check=True).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return {}
    dates: dict[str, tuple[int, int]] = {}
    ts = 0
    for line in out.splitlines():
        if line.startswith("@") and line[1:].isdigit():
            ts = int(line[1:])
            continue
        parts = line.split("\t")
        if len(parts) < 2 or not parts[0]:
            continue
        status = parts[0][0]
        if status == "R" and len(parts) >= 3:
            created = dates.get(parts[1], (ts, ts))[0]
            dates[parts[2]] = (dates.get(parts[2], (created, ts))[0], ts)
        elif status in "AMC":
            path = parts[-1]
            dates[path] = (dates.get(path, (ts, ts))[0], ts)
    return dates


def is_shallow() -> bool:
    r = subprocess.run(["git", "rev-parse", "--is-shallow-repository"], cwd=ROOT,
                       capture_output=True, text=True)
    return r.stdout.strip() == "true"


def blame_dates(rel: str) -> dict[int, int]:
    """line number (1-based) -> commit time, for per-bullet dates in curated lists."""
    try:
        out = subprocess.run(["git", "-c", "core.quotepath=off", "blame", "--line-porcelain", "--", rel],
                             cwd=ROOT, capture_output=True, text=True, check=True).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return {}
    res: dict[int, int] = {}
    cur = 0
    for line in out.splitlines():
        m = re.match(r"^[0-9a-f]{40} \d+ (\d+)", line)
        if m:
            cur = int(m.group(1))
        elif line.startswith("committer-time "):
            res[cur] = int(line.split()[1])
    return res


# ---------------------------------------------------------------- parsing
def parse_front(text: str) -> tuple[dict, str]:
    """Tiny frontmatter parser: `key: value` and `tags: [a, b]` / comma list / `- item` list."""
    m = FRONT_RE.match(text)
    if not m:
        return {}, text
    meta: dict = {}
    key = None
    for raw in m.group(1).splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        item = re.match(r"^\s+-\s+(.*)$", raw)
        if item and key:
            meta.setdefault(key, [])
            if isinstance(meta[key], list):
                meta[key].append(item.group(1).strip().strip("'\""))
            continue
        kv = re.match(r"^([A-Za-z_][\w-]*)\s*:\s*(.*)$", raw)
        if kv:
            key = kv.group(1).lower()
            val = kv.group(2).strip()
            if val.startswith("[") and val.endswith("]"):
                meta[key] = [v.strip().strip("'\"") for v in val[1:-1].split(",") if v.strip()]
            elif val == "":
                meta[key] = []
            else:
                meta[key] = val.strip("'\"")
    return meta, text[m.end():]


def as_list(v) -> list[str]:
    if v is None:
        return []
    if isinstance(v, list):
        return [str(x).strip() for x in v if str(x).strip()]
    return [t.strip() for t in str(v).split(",") if t.strip()]


EMOJI_RE = re.compile("[\U0001F000-\U0001FAFF\u2190-\u21FF\u2300-\u23FF\u25A0-\u27BF\u2900-\u297F\u2B00-\u2BFF"
                      "\uFE0F\u200D\u20E3]+")


def strip_md(s: str) -> str:
    s = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", s)
    s = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"<[^>]+>", "", s)
    s = re.sub(r"`+|\*+|~~|(?<!\w)_+|_+(?!\w)", "", s)
    s = EMOJI_RE.sub("", s)
    return re.sub(r"\s+", " ", s).strip()


def truncate(text: str, limit: int = 200) -> str:
    """Cut at a sentence end if one lands in a sensible spot, else at a word boundary."""
    text = text.strip()
    if len(text) <= limit:
        return text
    cut = text[:limit + 1]
    ends = [m.end() for m in re.finditer(r"[.!?](?=\s|$)", cut)]
    ends = [e for e in ends if e >= limit * 0.5]
    if ends:
        return cut[:ends[-1]].strip()
    cut = cut[:limit]
    if not text[limit].isspace():        # we are mid-word: back up to the previous space
        cut = cut.rsplit(" ", 1)[0] if " " in cut else cut
    return cut.rstrip(" ,;:-–—(") + "…"


def first_heading(body: str) -> str | None:
    for line in body.splitlines():
        m = re.match(r"^#\s+(.+?)\s*#*\s*$", line)
        if m:
            t = strip_md(m.group(1))
            if t:
                return t
    return None


def first_paragraph(body: str, limit: int = 200) -> str:
    """First real prose paragraph: skips headings, images, tables, code, html, bare labels."""
    in_code = False
    para: list[str] = []
    for line in body.splitlines() + [""]:
        s = line.strip()
        if s.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if not s:
            if para:
                text = strip_md(" ".join(para))
                if len(text) >= 25 and not text.endswith(":") and not re.match(r"^https?://\S+\.?$", text):
                    return truncate(text, limit)
                para = []
            continue
        if s.startswith(("#", "|", "![", "<", "---", "***", "===", "- ", "* ", "+ ")) or re.match(r"^\d+\.\s", s):
            para = []
            continue
        if s.startswith(">"):
            s = s.lstrip("> ").strip()
            if not s:
                continue
        para.append(s)
    return ""


def read_text(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def html_meta(text: str) -> tuple[str | None, str | None]:
    t = re.search(r"<title[^>]*>(.*?)</title>", text, re.S | re.I)
    d = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', text, re.S | re.I)
    return (strip_md(t.group(1)) if t else None, strip_md(d.group(1)) if d else None)


def code_comment(text: str, limit: int = 200) -> str:
    """Description from a leading comment block (// # /* */) in a script."""
    lines = []
    for line in text.splitlines()[:25]:
        s = line.strip()
        if s in ("'use strict';", '"use strict";') or s.startswith("#!") or not s:
            if lines:
                break
            continue
        m = re.match(r"^(?://+|#+|\*+|/\*+)\s?(.*?)(?:\*/)?$", s)
        if not m:
            break
        c = m.group(1).strip(" =-*")
        if c:
            lines.append(c)
    return truncate(" ".join(lines), limit)


def fmt_date(ts: int) -> str:
    return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d")


def parse_date(v: str | None) -> int | None:
    if not v:
        return None
    v = str(v).strip()
    for f in ("%Y-%m-%d", "%m-%d-%Y", "%Y/%m/%d", "%d %b %Y", "%b %d, %Y", "%B %d, %Y", "%Y-%m-%dT%H:%M:%S"):
        try:
            return int(datetime.strptime(v, f).replace(tzinfo=timezone.utc).timestamp())
        except ValueError:
            pass
    return None


def gh_url(rel: str, is_dir: bool) -> str:
    kind = "tree" if is_dir else "blob"
    return f"{GITHUB}/{kind}/{BRANCH}/{urllib.parse.quote(rel, safe='/')}"


def dedupe(tags: list[str]) -> list[str]:
    seen, out = set(), []
    for t in tags:
        k = t.strip().lower()
        if k and k not in seen:
            seen.add(k)
            out.append(t.strip())
    return out


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


# ---------------------------------------------------------------- item building
class Builder:
    def __init__(self) -> None:
        self.gd = git_dates()
        self.items: list[dict] = []
        self.live_dirs: list[Path] = []

    def dates_for(self, rel: str, fm: dict, path: Path) -> tuple[int, int]:
        created, modified = self.gd.get(rel, (0, 0))
        if not created:
            created = modified = int(path.stat().st_mtime)
        fm_date = parse_date(fm.get("date"))
        fm_upd = parse_date(fm.get("updated"))
        return (fm_date or created), (fm_upd or max(modified, fm_date or 0))

    def add(self, **it) -> None:
        it["tags"] = dedupe(it.get("tags", []))
        it.setdefault("description", "")
        it["id"] = slug(f"{it['type']}-{it['path']}")
        it["date"] = fmt_date(it.pop("created"))
        it["updated"] = fmt_date(it.pop("modified"))
        self.items.append(it)

    # --- generic markdown-backed item (a .md file, optionally with sibling folder)
    def md_item(self, md: Path, type_: str, name: str, tags: list[str], extra: dict | None = None,
                folder_item: bool = False) -> None:
        rel = md.relative_to(ROOT).as_posix()
        text = read_text(md)
        fm, body = parse_front(text)
        if str(fm.get("draft", "")).lower() == "true" or str(fm.get("hidden", "")).lower() == "true":
            return
        title = fm.get("title") or first_heading(body) or name
        desc = fm.get("description") or first_paragraph(body)
        created, modified = self.dates_for(rel, fm, md)
        words = len(re.findall(r"\w+", body))
        link_rel = md.parent.relative_to(ROOT).as_posix() if folder_item else rel
        item = dict(
            type=type_, title=title, name=name, description=desc,
            tags=as_list(fm.get("tags")) + tags,
            created=created, modified=modified,
            path=link_rel, url=gh_url(link_rel, folder_item),
            minutes=max(1, round(words / 200)) if type_ == "writeups" else None,
        )
        if extra:
            item.update(extra)
        if type_ == "writeups":
            # frontmatter overrides; `_`-prefixed keys never reach the JSON
            if fm.get("platform"):
                item["platform"] = str(fm["platform"])
            if fm.get("difficulty"):
                item["difficulty"] = str(fm["difficulty"])
            item["_series"] = str(fm["series"]).strip() if fm.get("series") else None
            item["_order"] = float(fm["order"]) if re.match(r"^-?\d+(\.\d+)?$", str(fm.get("order", ""))) else None
            item["_unit"] = str(fm["unit"]).strip() if fm.get("unit") else None
            item["_slug"] = slug(str(fm["slug"])) if fm.get("slug") else None
            item["_src"], item["_body"] = md, body
            item["tags"] = [t for t in item["tags"] if t.lower() != item["platform"].lower()]
        self.add(**item)

    # --- Write-ups/<Platform>/.../<Category>/<Lab>/(README.md | <anything>.md)
    def scan_writeups(self, base: Path) -> None:
        for md in sorted(base.rglob("*.md")):
            parts = md.relative_to(base).parts
            if any(p in SKIP_DIRS for p in parts[:-1]) or len(parts) < 3:
                continue  # skips Write-ups/README.md and Write-ups/<Platform>/x.md
            platform = parts[0]
            if len(parts) == 3:  # Platform/Category/Lab.md
                category, lab = parts[1], md.stem
            else:  # Platform/.../Category/Lab/file.md
                category, lab = parts[-3], parts[-2]
            mid = [p for p in parts[1:-1] if p != lab]
            self.md_item(md, "writeups", lab, [platform] + mid,
                         extra=dict(platform=platform, category=category))

    # --- Tools / Cheat Sheets / Projects: a folder with a README is one item;
    #     loose scripts (no README in their folder) are one item each.
    def scan_folders(self, base: Path, type_: str) -> None:
        def walk(d: Path, trail: list[str]) -> None:
            readme = next((f for f in sorted(d.iterdir()) if f.is_file() and README_RE.match(f.name)), None)
            has_index = (d / "index.html").is_file()
            if d != base and (readme or has_index):
                self.folder_item(d, readme, trail[:-1], type_)
                return
            for child in sorted(d.iterdir()):
                if child.name in SKIP_DIRS or child.name.startswith("."):
                    continue
                if child.is_dir():
                    walk(child, trail + [child.name])
                elif child.suffix.lower() in CODE_EXT:
                    self.script_item(child, trail, type_)
                elif child.suffix.lower() == ".md" and not README_RE.match(child.name) and d != base:
                    self.md_item(child, type_, child.stem, trail)
        if base.is_dir():
            walk(base, [])

    def folder_item(self, d: Path, readme: Path | None, trail: list[str], type_: str) -> None:
        rel_dir = d.relative_to(ROOT).as_posix()
        index = d / "index.html"
        extra: dict = {}
        if index.is_file():
            self.live_dirs.append(d)
            extra["live"] = f"live/{urllib.parse.quote(rel_dir, safe='/')}/index.html"
        # language tag from the files inside
        exts = {LANG_BY_EXT[f.suffix.lower()] for f in d.rglob("*") if f.is_file() and f.suffix.lower() in LANG_BY_EXT}
        if readme:
            self.md_item(readme, type_, d.name, trail + sorted(exts), extra=extra, folder_item=True)
            it = self.items[-1] if self.items and self.items[-1]["path"] == rel_dir else None
            if it and index.is_file():
                t, desc = html_meta(read_text(index))
                if not first_heading(parse_front(read_text(readme))[1]) and "title:" not in read_text(readme)[:300] and t:
                    it["title"] = t
                if not it["description"] and desc:
                    it["description"] = desc
        else:
            t, desc = html_meta(read_text(index))
            rel = index.relative_to(ROOT).as_posix()
            created, modified = self.dates_for(rel, {}, index)
            self.add(type=type_, title=t or d.name, name=d.name, description=desc or "",
                     tags=trail + sorted(exts), created=created, modified=modified,
                     path=rel_dir, url=gh_url(rel_dir, True), **extra)

    def script_item(self, f: Path, trail: list[str], type_: str) -> None:
        rel = f.relative_to(ROOT).as_posix()
        text = read_text(f)
        created, modified = self.dates_for(rel, {}, f)
        lang = LANG_BY_EXT.get(f.suffix.lower())
        self.add(type=type_, title=f.stem.replace("-", " ").replace("_", " ").title(), name=f.stem,
                 description=code_comment(text), tags=([lang] if lang else []) + trail,
                 created=created, modified=modified, path=rel, url=gh_url(rel, False))

    # --- Resources/External/<Kind>/README.md : every `- [name](url) ...` bullet is an item
    def scan_curated(self, base: Path) -> None:
        link_re = re.compile(r"^(\s*)[-*]\s+\[([^\]]+)\]\((https?://[^)]+)\)\s*(.*)$")
        for md in sorted(base.rglob("*.md")):
            rel = md.relative_to(ROOT).as_posix()
            kind = md.parent.name if md.parent != base else "External"
            lines = read_text(md).splitlines()
            blame = blame_dates(rel)
            fallback = self.dates_for(rel, {}, md)
            heads: dict[int, str] = {}
            i = 0
            while i < len(lines):
                h = re.match(r"^(#{2,4})\s+(.*)$", lines[i])
                if h:
                    heads[len(h.group(1))] = strip_md(h.group(2))
                    for deeper in [k for k in heads if k > len(h.group(1))]:
                        del heads[deeper]
                m = link_re.match(lines[i])
                if m and not m.group(1):  # top-level bullets only
                    name, url, rest = m.group(2).strip(), m.group(3), m.group(4)
                    block = [rest]
                    j = i + 1
                    while j < len(lines) and (lines[j].startswith((" ", "\t")) and lines[j].strip()):
                        block.append(lines[j].strip().lstrip("-* ").strip())
                        j += 1
                    text = " | ".join(b for b in block if b)
                    tags: list[str] = []
                    tm = re.search(r"Topics?:\s*([^|]+)", text, re.I)
                    if tm:
                        tags = [t.strip() for t in tm.group(1).split(",")]
                        text = (text[:tm.start()] + text[tm.end():]).strip()
                    text = re.sub(r"(?:^|\|)\s*[—–:\-]*\s*(?=\||$)", "", text)   # drop empty fragments
                    text = re.sub(r"^[\s|—–:\-]+", "", text).replace(" | ", ". ")
                    text = re.sub(r"(?i)\bwhat it is:\s*", "", text)
                    text = re.sub(r"\s*[—–-]\s*$", "", strip_md(text)).strip(" .—–-")
                    ts = blame.get(i + 1)
                    created = ts or fallback[0]
                    section = [heads[k] for k in sorted(heads)]
                    self.add(type="curated", title=name, name=name, description=text[:240],
                             tags=[kind] + section + tags, created=created, modified=created,
                             path=f"{rel}#{slug(name)}", url=url, external=True,
                             source=gh_url(rel, False))
                    i = j
                    continue
                i += 1


# ---------------------------------------------------------------- series
NUM_WORDS = {w: i for i, w in enumerate(
    "ZERO ONE TWO THREE FOUR FIVE SIX SEVEN EIGHT NINE TEN ELEVEN TWELVE THIRTEEN FOURTEEN FIFTEEN "
    "SIXTEEN SEVENTEEN EIGHTEEN NINETEEN TWENTY".split())}
NUM_RE = re.compile(r"\b(" + "|".join(w for w in NUM_WORDS if w != "ZERO") + r")\b")
SERIES_UNITS = {"Injured Android": "flags", "PortSwigger Academy": "labs", "PentesterLab": "exercises"}


def natural_number(title: str) -> int | None:
    m = NUM_RE.search(title)          # FLAG TWO, FLAG ELEVEN ... (upper-case words only)
    if m:
        return NUM_WORDS[m.group(1)]
    m = re.search(r"\d+", title)     # Android 07
    return int(m.group()) if m else None


def unit_for(name: str, entries: list[dict]) -> str:
    for e in entries:
        if e.get("_unit"):
            return e["_unit"]
    if sum(1 for e in entries if re.match(r"(?i)^flag\b", e["title"])) > len(entries) / 2:
        return "flags"
    return SERIES_UNITS.get(name, "write-ups")


def assign_series(items: list[dict]) -> list[dict]:
    """Group write-ups into series and give every write-up its hub URL, order and neighbours."""
    ws = [i for i in items if i["type"] == "writeups"]
    per_platform: dict[str, int] = {}
    for i in ws:
        per_platform[i["platform"]] = per_platform.get(i["platform"], 0) + 1

    # unique, stable page slugs: writeups/<platform>/<name>/
    seen: set[str] = set()
    for i in ws:
        base = f"{slug(i['platform'])}/{i['_slug'] or slug(i['name'])}"
        cand, n = base, 2
        while cand in seen:
            cand, n = f"{base}-{n}", n + 1
        seen.add(cand)
        i["slug"] = cand
        i["href"] = f"writeups/{cand}/"

    groups: dict[str, list[dict]] = {}
    for i in ws:
        name = i["_series"] or (i["platform"] if per_platform[i["platform"]] >= 2 else None)
        i["series"] = name
        if name:
            groups.setdefault(name, []).append(i)

    def key(i: dict):
        if i["_order"] is not None:
            return (0, i["_order"], i["date"], i["title"])
        n = natural_number(i["title"])
        return (1, n, i["date"], i["title"]) if n is not None else (2, 0, i["date"], i["title"].lower())

    series = []
    used: set[str] = set()
    for name, entries in groups.items():
        entries.sort(key=key)
        sslug, n = slug(name) or "series", 2
        while sslug in used:
            sslug, n = f"{slug(name)}-{n}", n + 1
        used.add(sslug)
        counts: dict[str, int] = {}
        for e in entries:
            for t in e["tags"]:
                counts[t] = counts.get(t, 0) + 1
        top = [t for t, _ in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0].lower()))][:5]
        cats = list(dict.fromkeys(e["category"] for e in entries))
        for idx, e in enumerate(entries):
            e["series_slug"], e["series_pos"] = sslug, idx + 1
            e["series_prev"] = entries[idx - 1]["id"] if idx else None
            e["series_next"] = entries[idx + 1]["id"] if idx + 1 < len(entries) else None
            e["group"] = e["category"] if len(cats) > 1 else None
        platforms = list(dict.fromkeys(e["platform"] for e in entries))
        series.append({
            "slug": sslug, "name": name, "href": f"series/{sslug}/",
            "platform": platforms[0] if len(platforms) == 1 else None,
            "count": len(entries), "unit": unit_for(name, entries),
            "latest": max(e["date"] for e in entries), "earliest": min(e["date"] for e in entries),
            "tags": top, "items": [e["id"] for e in entries],
        })
    for i in ws:
        i.setdefault("series_slug", None)
    series.sort(key=lambda s: (s["latest"], s["name"]), reverse=True)
    return series


# ---------------------------------------------------------------- curated enrichment
def enrich_curated(items: list[dict]) -> None:
    """Show where a link goes, and add language/topic chips from the GitHub API (best effort)."""
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    for i in items:
        if i["type"] != "curated":
            continue
        u = urllib.parse.urlparse(i["url"])
        host = u.netloc.removeprefix("www.")
        i["display"] = host + u.path.rstrip("/")
        m = re.match(r"^/([\w.-]+)/([\w.-]+)/?$", u.path)
        if host != "github.com" or not m:
            continue
        req = urllib.request.Request(f"https://api.github.com/repos/{m.group(1)}/{m.group(2)}",
                                     headers={"Accept": "application/vnd.github+json", "User-Agent": "hwl-hub-build"})
        if token:
            req.add_header("Authorization", f"Bearer {token}")
        try:
            with urllib.request.urlopen(req, timeout=6) as r:
                meta = json.load(r)
        except Exception as e:                      # offline, rate-limited, renamed: all fine
            print(f"  (no GitHub metadata for {i['display']}: {type(e).__name__})", file=sys.stderr)
            continue
        extra = ([meta["language"]] if meta.get("language") else []) + [t for t in meta.get("topics", [])][:6]
        kind = i["tags"][0] if i["tags"] else ""
        rest = [t for t in i["tags"][1:] if t.lower() not in {x.lower() for x in extra}]
        i["tags"] = dedupe([kind] + extra + rest)
        if meta.get("language"):
            i["language"] = meta["language"]
        if not i["description"] and meta.get("description"):
            i["description"] = truncate(strip_md(meta["description"]), 200)


# ---------------------------------------------------------------- outputs
def copy_assets(b: Builder) -> None:
    img_src = ROOT / "src" / "img"
    if img_src.is_dir():
        shutil.copytree(img_src, SITE / "img", dirs_exist_ok=True)
    live_root = SITE / "live"
    if live_root.exists():
        shutil.rmtree(live_root)
    for d in b.live_dirs:
        dest = live_root / d.relative_to(ROOT)
        shutil.copytree(d, dest, ignore=shutil.ignore_patterns(".git", "__pycache__"))


def readme_table(items: list[dict]) -> str:
    rows = ["| Platform | Lab | Category | Date Posted |", "| --- | --- | --- | --- |"]
    ws = sorted((i for i in items if i["type"] == "writeups"), key=lambda i: (i["date"], i["name"]), reverse=True)
    for i in ws:
        d = datetime.strptime(i["date"], "%Y-%m-%d").strftime("%m-%d-%Y")
        rows.append(f"| {i['platform']} | [{i['name']}]({i['url']}) | {i['category']} | {d} |")
    return "\n".join(rows) + "\n"


def update_readme(items: list[dict]) -> bool:
    path = ROOT / "README.md"
    text = path.read_text(encoding="utf-8")
    header = "## 🔍 Latest Blog Posts"
    idx = text.find(header)
    if idx == -1:
        print("README.md has no 'Latest Blog Posts' section; skipped.")
        return False
    after = idx + len(header)
    nxt = re.search(r"(?m)^#{1,2}\s+", text[after:])
    end = after + nxt.start() if nxt else len(text)
    new = text[:after] + "\n\n" + readme_table(items) + "\n" + text[end:]
    if new != text:
        path.write_text(new, encoding="utf-8")
        return True
    return False


def load_profile() -> dict:
    default = {"name": "L0WK3Y", "handle": "l0wk3y", "tagline": "Bug bounty hunter & mobile security researcher",
               "bio": "", "links": []}
    f = SITE / "profile.json"
    try:
        return {**default, **json.loads(f.read_text(encoding="utf-8"))}
    except (OSError, ValueError):
        return default


def clean_generated() -> None:
    for d in ("writeups", "series", "media"):
        shutil.rmtree(SITE / d, ignore_errors=True)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--readme", action="store_true", help="also refresh the README 'Latest Blog Posts' table")
    ap.add_argument("--offline", action="store_true", help="skip GitHub API lookups for curated links")
    args = ap.parse_args()

    if is_shallow():
        print("warning: shallow git clone, so dates fall back to the oldest fetched commit. "
              "Use `fetch-depth: 0` / `git fetch --unshallow`.", file=sys.stderr)

    b = Builder()
    res = ROOT / "Resources"
    b.scan_writeups(res / "Personal" / "Write-ups")
    b.scan_folders(res / "Personal" / "Tools", "tools")
    b.scan_folders(res / "Personal" / "Cheat Sheets", "cheatsheets")
    b.scan_curated(res / "External")
    b.scan_folders(ROOT / "Projects", "projects")

    b.items.sort(key=lambda i: (i["date"], i["title"].lower()), reverse=True)
    series = assign_series(b.items)
    if args.offline:
        for i in b.items:
            if i["type"] == "curated":
                u = urllib.parse.urlparse(i["url"])
                i["display"] = u.netloc.removeprefix("www.") + u.path.rstrip("/")
    else:
        enrich_curated(b.items)

    counts = {t: sum(1 for i in b.items if i["type"] == t) for t in TYPES}
    ws = [i for i in b.items if i["type"] == "writeups"]
    profile = load_profile()
    stats = {"writeups": len(ws), "platforms": len({i["platform"] for i in ws}), "series": len(series),
             "updated": max((i["updated"] for i in b.items), default="")}

    # render the reading pages, series pages, feed, sitemap and palette index
    import hub_pages
    clean_generated()
    hub_pages.render_all(b.items, series, profile, stats, ROOT, SITE, SITE_URL, SITE_NAME, GITHUB)

    public = [{k: v for k, v in i.items() if not k.startswith("_")} for i in b.items]
    data = {
        "site": {"name": SITE_NAME, "repo": GITHUB, "branch": BRANCH, "url": SITE_URL},
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "profile": profile, "stats": stats,
        "types": [{"id": t, "label": l, "count": counts[t]} for t, l in TYPES.items()],
        "series": series,
        "items": public,
    }
    out = SITE / "data" / "index.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    copy_assets(b)

    print(f"wrote {out.relative_to(ROOT)}: {len(b.items)} items " +
          ", ".join(f"{TYPES[t]}={n}" for t, n in counts.items()) + f", series={len(series)}")
    if args.readme:
        print("README.md updated" if update_readme(b.items) else "README.md already up to date")
    return 0


if __name__ == "__main__":
    sys.exit(main())
