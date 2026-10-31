"""Static pages for the hub: one reading page per write-up, one page per series,
plus feed.xml, sitemap.xml and the command-palette index.

Imported by build_index.py. Needs markdown-it-py and pygments.
"""
from __future__ import annotations

import html
import json
import re
import shutil
import struct
import urllib.parse
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path

try:
    from markdown_it import MarkdownIt
    from pygments import highlight
    from pygments.formatters import HtmlFormatter
    from pygments.lexers import TextLexer, get_lexer_by_name
    from pygments.util import ClassNotFound
except ImportError as e:  # pragma: no cover
    import sys
    raise SystemExit(f"Missing dependency ({e.name}) for {sys.executable}.\n"
                     f"Install it into this exact interpreter (on Homebrew Python use a venv: python3 -m venv .venv && .venv/bin/pip install -r scripts/requirements.txt):\n  {sys.executable} -m pip install -r scripts/requirements.txt")

# set by render_all()
ROOT: Path
SITE: Path
SITE_URL: str
SITE_NAME: str
GITHUB: str
REPO_SLUG: str

ICON_SEARCH = ('<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" '
               'stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>')
ICON_GITHUB = ('<svg viewBox="0 0 16 16" width="18" height="18" fill="currentColor" aria-hidden="true"><path d="M8 0C3.58 0 0 3.58 '
               '0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 '
               '1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 '
               '1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 '
               '1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8z"/></svg>')
ICON_THEME = ('<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">'
              '<circle cx="12" cy="12" r="9"/><path d="M12 3a9 9 0 0 1 0 18z" fill="currentColor"/></svg>')


def esc(s: object) -> str:
    return html.escape(str(s), quote=True)


def slugify(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def long_date(iso: str) -> str:
    d = datetime.strptime(iso, "%Y-%m-%d")
    return f"{d:%b} {d.day}, {d.year}"


def root_prefix(href: str) -> str:
    return "../" * len([p for p in href.strip("/").split("/") if p])


# ================================================================== markdown
EXT_LANG = {"js": "javascript", "jsx": "javascript", "ts": "typescript", "sh": "bash", "shell": "bash", "zsh": "bash",
            "txt": "text", "plaintext": "text", "yml": "yaml", "py": "python", "kt": "kotlin", "html": "html"}


def guess_lang(code: str) -> str:
    s = code.strip()
    if not s:
        return "text"
    if s[0] in "{[":
        try:
            json.loads(s)
            return "json"
        except ValueError:
            pass
    if re.search(r"^\s*\.(method|class|field|locals|registers)\b", s, re.M):
        return "smali"
    if s.startswith("$ ") or re.match(r"^(adb|frida|apktool|jadx|curl|nmap|objection|drozer|keytool|unzip|git|sudo|pip|python3?|"
                                      r"cd|ls|cat|grep|export|chmod|mkdir)\s", s):
        return "bash"
    if re.match(r"^(GET|POST|PUT|DELETE|HEAD|OPTIONS|PATCH) \S+ HTTP/", s) or s.startswith("HTTP/"):
        return "http"
    if s.startswith("<?xml") or (re.match(r"^<[A-Za-z!?][^>]*>", s) and s.endswith(">")):
        return "xml"
    if re.search(r"\bJava\.perform\b|\bInterceptor\.attach\b|\bconsole\.log\b|=>|^\s*(const|let|var) ", s, re.M):
        return "javascript"
    if re.search(r"^\s*(import (java|android|javax)|package |public (final )?(class|static|void)|private (static|final|void)|"
                 r"@Override|protected (void|static))", s, re.M):
        return "java"
    if re.search(r"^\s*(def |import \w|from \w+ import|print\()", s, re.M):
        return "python"
    return "text"


_FORMATTER = HtmlFormatter(nowrap=True)


def render_code(code: str, info: str) -> str:
    raw = (info or "").strip().split()[0].lower() if (info or "").strip() else ""
    if raw in ("jsx", "txt", "text", "plaintext"):      # Notion exports use these as "unknown": look at the code instead
        guess = guess_lang(code)
        raw = guess if guess != "text" else ("javascript" if raw == "jsx" else "text")
    lang = EXT_LANG.get(raw, raw) or guess_lang(code)
    label = EXT_LANG.get(raw, raw) or lang      # py -> python, sh -> bash, txt -> text
    try:
        lexer = get_lexer_by_name(lang)
    except ClassNotFound:
        lexer = TextLexer()
        label = label or "text"
    body = highlight(code.rstrip("\n"), lexer, _FORMATTER).rstrip("\n")
    body = re.sub(r'<span class="w">(\s*)</span>', r"\1", body)      # whitespace spans are pure bloat
    return (f'<figure class="code"><figcaption><span class="lang">{esc(label)}</span>'
            f'<button type="button" class="copy" aria-label="Copy {esc(label)} code to clipboard">Copy</button></figcaption>'
            f'<pre tabindex="0"><code>{body}</code></pre></figure>\n')


def _png_gif_size(p: Path) -> tuple[int, int] | None:
    try:
        with open(p, "rb") as f:
            head = f.read(26)
        if head[:8] == b"\x89PNG\r\n\x1a\n":
            return struct.unpack(">II", head[16:24])
        if head[:6] in (b"GIF87a", b"GIF89a"):
            return struct.unpack("<HH", head[6:10])
    except OSError:
        pass
    return None


# ------------------------------------------------------------------ sanitizer + TOC + asset rewriting
ALLOWED = {"a", "abbr", "aside", "b", "blockquote", "br", "button", "caption", "code", "dd", "del", "details", "div", "dl",
           "dt", "em", "figcaption", "figure", "h1", "h2", "h3", "h4", "h5", "h6", "hr", "i", "img", "kbd", "li", "mark",
           "ol", "p", "pre", "s", "small", "span", "strong", "sub", "summary", "sup", "table", "tbody", "td", "tfoot",
           "th", "thead", "tr", "u", "ul", "center"}
DROP = {"script", "style", "iframe", "object", "embed", "form", "link", "meta", "base", "svg", "noscript", "textarea"}
VOID = {"br", "hr", "img", "link", "meta", "base", "input", "source", "col", "wbr"}
ATTRS = {"*": {"class", "title", "lang"}, "a": {"href"}, "img": {"src", "alt", "width", "height"},
         "td": {"colspan", "rowspan", "align"}, "th": {"colspan", "rowspan", "align"}, "ol": {"start"},
         "pre": {"tabindex"}, "button": {"type", "aria-label"}, "details": {"open"}, "div": {"align"}, "p": {"align"}}


class Cleaner(HTMLParser):
    def __init__(self, md_dir: Path, page_slug: str, root: str):
        super().__init__(convert_charrefs=False)
        self.out: list[str | None] = []
        self.md_dir, self.page_slug, self.root = md_dir, page_slug, root
        self.skip_tag: str | None = None
        self.toc: list[tuple[int, str, str]] = []
        self.ids: set[str] = set()
        self.head: dict | None = None
        self.images = 0

    # -- helpers
    def unique_id(self, text: str) -> str:
        base = slugify(text) or "section"
        cand, n = base, 2
        while cand in self.ids:
            cand, n = f"{base}-{n}", n + 1
        self.ids.add(cand)
        return cand

    def media(self, src: str) -> tuple[str, Path | None]:
        """Copy a relative image into site/media and return its new URL."""
        path = urllib.parse.unquote(urllib.parse.urlparse(src).path)
        target = (self.md_dir / path).resolve()
        if path.startswith("/"):
            target = (ROOT / path.lstrip("/")).resolve()
        try:
            target.relative_to(ROOT)
        except ValueError:
            return src, None
        if not target.is_file():
            return src, None
        rel = Path(path)
        parts = [re.sub(r"[^A-Za-z0-9._-]+", "-", p).strip("-") or "x" for p in rel.parts if p not in (".", "..", "/")]
        dest = SITE / "media" / self.page_slug / "/".join(parts)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(target, dest)
        return f"{self.root}media/{self.page_slug}/{'/'.join(parts)}", target

    def repo_link(self, href: str) -> str | None:
        parsed = urllib.parse.urlparse(href)
        target = (self.md_dir / urllib.parse.unquote(parsed.path)).resolve()
        try:
            rel = target.relative_to(ROOT).as_posix()
        except ValueError:
            return None
        kind = "tree" if target.is_dir() else "blob"
        return f"{GITHUB}/{kind}/main/{urllib.parse.quote(rel, safe='/')}"

    def clean_attrs(self, tag: str, attrs) -> list[tuple[str, str]]:
        allowed = ATTRS["*"] | ATTRS.get(tag, set())
        res = []
        for k, v in attrs:
            k = k.lower()
            if k not in allowed or v is None and k not in ("open",):
                continue
            if k == "tabindex" and v != "0":
                continue
            res.append((k, v or ""))
        return res

    # -- parser callbacks
    def handle_starttag(self, tag, attrs):
        self._start(tag, attrs)

    def handle_startendtag(self, tag, attrs):
        self._start(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def _start(self, tag, attrs):
        if self.skip_tag:
            return
        if tag in DROP:
            if tag not in VOID:
                self.skip_tag = tag
            return
        if tag not in ALLOWED and tag not in VOID:
            self.out.append(esc(self.get_starttag_text()))
            return
        a = self.clean_attrs(tag, attrs)
        d = dict(a)
        if tag == "a":
            href = d.get("href", "")
            if re.match(r"^\s*(javascript|data|vbscript):", href, re.I):
                a = [(k, v) for k, v in a if k != "href"]
            elif href and not re.match(r"^([a-z][a-z0-9+.-]*:|#|//)", href, re.I):
                new = self.repo_link(href)
                a = [(k, new if k == "href" else v) for k, v in a] if new else [(k, v) for k, v in a if k != "href"]
            if any(k == "href" and re.match(r"^https?:", v) for k, v in a):
                a.append(("rel", "noopener"))
        elif tag == "img":
            src = d.get("src", "")
            if not src or re.match(r"^\s*(javascript|data):", src, re.I) and not src.startswith("data:image/"):
                return
            target = None
            own = re.match(r"^https://(?:github\.com/%s/(?:raw|blob)/[\w.-]+/|raw\.githubusercontent\.com/%s/[\w.-]+/)(.+?)(?:\?.*)?$"
                           % (re.escape(REPO_SLUG), re.escape(REPO_SLUG)), src)
            if own:                                   # image hosted in this repo: serve our own copy
                new, target = self.media("/" + own.group(1))
                if target:
                    src = new
            elif not re.match(r"^([a-z][a-z0-9+.-]*:|//)", src, re.I):
                src, target = self.media(src)
            a = [(k, v) for k, v in a if k != "src"] + [("src", src)]
            if "alt" not in d:
                a.append(("alt", ""))
            self.images += 1
            # first image may be the LCP element; everything else loads lazily
            a += [("loading", "lazy"), ("decoding", "async")]
            if target and "width" not in d:
                size = _png_gif_size(target)
                if size:
                    a += [("width", str(size[0])), ("height", str(size[1]))]
        name = tag
        if re.fullmatch(r"h[1-6]", tag):
            name = "h2" if tag == "h1" else tag          # the page title is the only h1
            if name in ("h2", "h3"):
                self.head = {"tag": name, "idx": len(self.out), "attrs": a, "text": []}
                self.out.append(None)                     # filled in once the text is known
                return
        if tag == "table":
            self.out.append('<div class="table-wrap" tabindex="0" role="region" aria-label="Scrollable table">')
        attr_s = "".join(f' {k}="{esc(v)}"' if v != "" or k in ("alt",) else f" {k}" for k, v in a)
        self.out.append(f"<{name}{attr_s}>")

    def handle_endtag(self, tag):
        if self.skip_tag:
            if tag == self.skip_tag:
                self.skip_tag = None
            return
        if tag in VOID:
            return
        if tag not in ALLOWED:
            self.out.append(esc(f"</{tag}>"))
            return
        if re.fullmatch(r"h[1-6]", tag):
            name = "h2" if tag == "h1" else tag
            if self.head and self.head["tag"] == name:
                h = self.head
                self.head = None
                text = re.sub(r"\s+", " ", "".join(h["text"])).strip()
                given = dict(h["attrs"]).get("id")
                hid = self.unique_id(text if not given else given)
                self.toc.append((int(name[1]), text, hid))
                rest = "".join(f' {k}="{esc(v)}"' for k, v in h["attrs"] if k != "id")
                self.out[h["idx"]] = f'<{name} id="{hid}"{rest}>'
                self.out.append(f'<a class="anchor" href="#{hid}" aria-label="Link to this section">#</a></{name}>')
                return
            self.out.append(f"</{name}>")
            return
        self.out.append(f"</{tag}>")
        if tag == "table":
            self.out.append("</div>")

    def handle_data(self, data):
        if self.skip_tag:
            return
        if self.head:
            self.head["text"].append(data)
        self.out.append(html.escape(data, quote=False))

    def handle_entityref(self, name):
        if self.skip_tag:
            return
        if self.head:
            self.head["text"].append(html.unescape(f"&{name};"))
        self.out.append(f"&{name};")

    def handle_charref(self, name):
        if self.skip_tag:
            return
        if self.head:
            self.head["text"].append(html.unescape(f"&#{name};"))
        self.out.append(f"&#{name};")

    def handle_comment(self, data):
        pass

    def handle_decl(self, decl):
        pass

    def handle_pi(self, data):
        if not self.skip_tag:
            self.out.append(esc(f"<?{data}>"))


def _md() -> MarkdownIt:
    md = MarkdownIt("commonmark", {"html": True, "linkify": False}).enable(["table", "strikethrough"])

    def fence(tokens, idx, options, env):
        t = tokens[idx]
        return render_code(t.content, t.info)

    def code_block(tokens, idx, options, env):
        return render_code(tokens[idx].content, "")

    md.renderer.rules["fence"] = fence
    md.renderer.rules["code_block"] = code_block
    return md


_MD = _md()


def render_body(body: str, md_dir: Path, page_slug: str, root: str, title: str):
    tokens = _MD.parse(body)
    # drop the first H1 when it is the document's opening line (an exported title) or repeats the page title;
    # an H1 further down is a real section heading and stays (demoted to h2 by the sanitizer)
    norm = lambda x: re.sub(r"[^a-z0-9]+", " ", x.lower()).strip()
    for i, t in enumerate(tokens):
        if t.type == "heading_open" and t.tag == "h1":
            if i + 2 < len(tokens) and tokens[i + 2].type == "heading_close" and (i == 0 or norm(tokens[i + 1].content) == norm(title)):
                del tokens[i:i + 3]
            break
        if t.type == "heading_open":
            break
    raw = _MD.renderer.render(tokens, _MD.options, {})
    c = Cleaner(md_dir, page_slug, root)
    c.feed(raw)
    c.close()
    return "".join(x for x in c.out if x is not None), c.toc


# ================================================================== page chrome
def head(*, title: str, desc: str, root: str, path: str, og_type: str = "website", extra: str = "") -> str:
    url = SITE_URL + path
    full = title if title == SITE_NAME else f"{title} · {SITE_NAME}"
    desc = desc or "Bug bounty and CTF write-ups, tools, cheat sheets and curated resources from L0WK3Y."
    img = SITE_URL + "assets/og.png"
    return f"""<!DOCTYPE html>
<html lang="en" data-root="{root}">
<head>
<meta charset="utf-8">
<title>{esc(full)}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{esc(desc)}">
<meta name="theme-color" content="#0b0f14">
<link rel="canonical" href="{esc(url)}">
<meta property="og:site_name" content="{esc(SITE_NAME)}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{esc(url)}">
<meta property="og:image" content="{img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{img}">
<link rel="icon" type="image/png" href="{root}assets/icon-64.png">
<link rel="apple-touch-icon" href="{root}assets/icon-180.png">
<link rel="alternate" type="application/atom+xml" title="{esc(SITE_NAME)}" href="{root}feed.xml">
<link rel="stylesheet" href="{root}assets/style.css">
{extra}<script>try{{var t=localStorage.getItem('hwl-theme');if(t)document.documentElement.dataset.theme=t}}catch(e){{}}if(/[?&]embed\\b/.test(location.search)){{document.documentElement.classList.add('embed');document.documentElement.dataset.theme='light'}}</script>
</head>
<body>
"""


def header(root: str) -> str:
    return f"""<a class="skip" href="#content">Skip to content</a>
<header class="top">
  <div class="wrap top-row">
    <a class="brand" href="{root}hub/" aria-label="Hunting With L0WK3Y, home">
      <img src="{root}assets/icon-64.png" alt="" width="28" height="28">
      <span>hunting<b>.with</b>(<i>l0wk3y</i>)</span>
    </a>
    <nav class="nav" id="nav" aria-label="Sections">
      <a href="{root}hub/#series">Categories</a><a href="{root}hub/#writeups">Write-ups</a><a href="{root}hub/#toolbox">Toolbox</a>
    </nav>
    <div class="actions">
      <a class="desk-link" href="{root}?desktop" rel="noopener">Desktop view</a>
      <button type="button" id="open-palette" class="icon-btn pal" aria-label="Search the site" aria-keyshortcuts="Control+K Meta+K">{ICON_SEARCH}<span class="lbl">Search</span><kbd>Ctrl K</kbd></button>
      <a class="icon-btn" href="{GITHUB}" aria-label="GitHub repository" rel="noopener">{ICON_GITHUB}</a>
      <button type="button" id="theme" class="icon-btn" aria-label="Toggle light and dark theme">{ICON_THEME}</button>
    </div>
  </div>
</header>
"""


def footer(root: str) -> str:
    return f"""<footer class="wrap foot">
  <p>Built from the repo on every push · <a href="{root}feed.xml">RSS</a> · <a href="{GITHUB}" rel="noopener">source</a></p>
  <p class="muted">For educational use. Only test systems you are authorised to test.</p>
</footer>
<script src="{root}assets/common.js" defer></script>
"""


def crumbs(root: str, trail: list[tuple[str, str | None]]) -> str:
    lis = [f'<li><a href="{root}hub/">Home</a></li>']
    for label, href in trail:
        lis.append(f'<li><a href="{esc(href)}">{esc(label)}</a></li>' if href else f'<li aria-current="page">{esc(label)}</li>')
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{"".join(lis)}</ol></nav>'


def tag_chips(root: str, tags: list[str], limit: int = 12) -> str:
    if not tags:
        return ""
    lis = "".join(f'<li><a class="chip" href="{root}hub/?tags={urllib.parse.quote(t.lower())}">{esc(t)}</a></li>' for t in tags[:limit])
    return f'<ul class="chips" aria-label="Tags">{lis}</ul>'


def diff_chip(d: str | None) -> str:
    if not d:
        return ""
    return f'<span class="diff diff-{slugify(d)}">{esc(d)}</span>'


# ================================================================== pages
def write_article(it: dict, by_id: dict, series_by_slug: dict) -> None:
    href = it["href"]
    root = root_prefix(href)
    html_body, toc = render_body(it["_body"], it["_src"].parent, it["slug"].replace("/", "-"), root, it["title"])
    toc = [t for t in toc if t[0] <= 3]
    sr = series_by_slug.get(it["series_slug"]) if it.get("series_slug") else None

    trail: list[tuple[str, str | None]] = []
    if sr:
        trail.append((sr["name"], root + sr["href"]))
    trail.append((it["title"], None))

    toc_html = ""
    if len(toc) >= 2:
        li = "".join(f'<li class="l{lvl}"><a href="#{hid}">{esc(text)}</a></li>' for lvl, text, hid in toc)
        toc_html = (f'<aside class="toc" aria-label="On this page"><p class="toc-h">On this page</p><ol>{li}</ol></aside>'
                    f'<details class="toc-m"><summary>On this page</summary><ol>{li}</ol></details>')

    pn = ""
    if sr:
        def link(rel: str, other: str | None, label: str) -> str:
            if not other:
                return '<span class="pn-gap"></span>'
            o = by_id[other]
            return (f'<a class="pn-{rel}" rel="{rel}" href="{root}{o["href"]}"><span class="pn-l">{label}</span>'
                    f'<strong>{esc(o["title"])}</strong></a>')
        pn = (f'<nav class="pn" aria-label="More in {esc(sr["name"])}">'
              f'{link("prev", it["series_prev"], "← Previous")}{link("next", it["series_next"], "Next →")}</nav>')

    meta = [f'<time datetime="{it["date"]}">{long_date(it["date"])}</time>', f'{it["minutes"]} min read']
    if it.get("difficulty"):
        meta.append(diff_chip(it["difficulty"]))
    if sr:
        meta.append(f'<span>{esc(it["group"] or sr["name"])} · {it["series_pos"]} of {it["series_total"]}</span>')
    meta_html = "".join(f"<li>{m}</li>" for m in meta)

    plat = f'<span class="plat">{esc(it["platform"])}</span>'
    if sr:
        plat += f' <span class="sep" aria-hidden="true">/</span> <a class="plat" href="{root}{sr["href"]}">{esc(sr["name"])}</a>'
    desc = it["description"]
    desc_html = '<p class="a-desc">' + esc(desc) + "</p>" if desc else ""
    ld = json.dumps({"@context": "https://schema.org", "@type": "TechArticle", "headline": it["title"],
                     "description": desc, "datePublished": it["date"], "dateModified": it["updated"],
                     "author": {"@type": "Person", "name": "L0WK3Y"}, "keywords": ", ".join(it["tags"]),
                     "mainEntityOfPage": SITE_URL + href}, ensure_ascii=False).replace("</", "<\\/")
    extra = (f'<meta property="article:published_time" content="{it["date"]}">\n'
             f'<meta property="article:modified_time" content="{it["updated"]}">\n'
             + "".join(f'<meta property="article:tag" content="{esc(t)}">\n' for t in it["tags"][:8])
             + f'<script type="application/ld+json">{ld}</script>\n')

    page = head(title=it["title"], desc=desc, root=root, path=href, og_type="article", extra=extra)
    page += '<div class="progress" aria-hidden="true"><i id="bar"></i></div>\n' + header(root)
    page += f"""<main id="content" class="wrap article-wrap">
  {crumbs(root, trail)}
  <header class="a-head">
    <p class="eyebrow">{plat}</p>
    <h1>{esc(it["title"])}</h1>
    {desc_html}
    <ul class="a-meta">{meta_html}</ul>
    {tag_chips(root, it["tags"])}
  </header>
  <div class="a-grid">
    {toc_html}
    <article class="prose">
{html_body}
    </article>
  </div>
  {pn}
  <p class="src"><a href="{esc(it["url"])}" rel="noopener">View source on GitHub ↗</a></p>
</main>
"""
    page += footer(root) + '<script src="' + root + 'assets/article.js" defer></script>\n</body>\n</html>\n'
    out = SITE / href / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")


def write_series(sr: dict, by_id: dict) -> None:
    href = sr["href"]
    root = root_prefix(href)
    entries = [by_id[i] for i in sr["items"]]
    rows, last_group, n = [], object(), 0
    multi = any(e["group"] for e in entries)
    for e in entries:
        n += 1
        if multi and e["group"] != last_group:
            if rows:
                rows.append("</ol>")
            rows.append(f'<h2 class="grp">{esc(e["group"] or "Other")}</h2><ol class="entries">')
            last_group = e["group"]
        elif not rows:
            rows.append('<ol class="entries">')
        bits = [f'<time datetime="{e["date"]}">{long_date(e["date"])}</time>', f'{e["minutes"]} min read']
        if e.get("difficulty"):
            bits.append(diff_chip(e["difficulty"]))
        desc_html = '<span class="desc">' + esc(e["description"]) + "</span>" if e["description"] else ""
        meta_html = " · ".join(bits)
        rows.append(f'<li><a class="entry" href="{root}{e["href"]}"><span class="num" aria-hidden="true">{e["series_pos"]:02d}</span>'
                    f'<span class="body"><strong>{esc(e["title"])}</strong>{desc_html}'
                    f'<span class="meta">{meta_html}</span></span></a></li>')
    rows.append("</ol>")
    first = entries[0]
    unit = sr["unit"] if sr["count"] != 1 else sr["unit"].rstrip("s")
    plats = sr["platforms"]
    desc = f'{sr["count"]} {unit} filed under {sr["name"]} from {len(plats)} platform{"s" if len(plats) != 1 else ""}, latest {long_date(sr["latest"])}.'
    page = head(title=f'{sr["name"]} write-ups', desc=desc, root=root, path=href)
    page += header(root)
    page += f"""<main id="content" class="wrap series-wrap">
  {crumbs(root, [("Categories", root + "hub/#series"), (sr["name"], None)])}
  <header class="a-head">
    <p class="eyebrow"><span class="plat">Category</span></p>
    <h1>{esc(sr["name"])}</h1>
    <ul class="a-meta"><li><strong>{sr["count"]}</strong> {esc(unit)}</li><li>Latest <time datetime="{sr["latest"]}">{long_date(sr["latest"])}</time></li>
    <li>{len(plats)} platform{"s" if len(plats) != 1 else ""}</li></ul>
    {tag_chips(root, sr["tags"])}
    <p><a class="btn primary" href="{root}{first["href"]}">Start with {esc(first["title"])} →</a></p>
  </header>
  {"".join(rows)}
</main>
"""
    page += footer(root) + "</body>\n</html>\n"
    out = SITE / href / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")


def write_feed(items: list[dict]) -> None:
    ws = [i for i in items if i["type"] == "writeups"]
    ws.sort(key=lambda i: (i["date"], i["title"]), reverse=True)
    updated = max((i["updated"] for i in ws), default="1970-01-01")
    ents = []
    for i in ws:
        cats = "".join(f'<category term="{esc(t)}"/>' for t in i["tags"])
        ents.append(f"""  <entry>
    <id>{esc(SITE_URL + i["href"])}</id>
    <title>{esc(i["title"])}</title>
    <link href="{esc(SITE_URL + i["href"])}"/>
    <published>{i["date"]}T00:00:00Z</published>
    <updated>{i["updated"]}T00:00:00Z</updated>
    <author><name>L0WK3Y</name></author>
    <summary>{esc(i["description"])}</summary>
    {cats}
  </entry>""")
    xml = f"""<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <id>{SITE_URL}</id>
  <title>{esc(SITE_NAME)}: write-ups</title>
  <subtitle>Bug bounty and CTF write-ups</subtitle>
  <link href="{SITE_URL}feed.xml" rel="self"/>
  <link href="{SITE_URL}"/>
  <updated>{updated}T00:00:00Z</updated>
{chr(10).join(ents)}
</feed>
"""
    (SITE / "feed.xml").write_text(xml, encoding="utf-8")


def write_sitemap(items: list[dict], series: list[dict]) -> None:
    newest = max((i["updated"] for i in items), default="")
    urls = [(SITE_URL, newest), (SITE_URL + "hub/", newest)]
    urls += [(SITE_URL + s["href"], s["latest"]) for s in series]
    urls += [(SITE_URL + i["href"], i["updated"]) for i in items if i["type"] == "writeups"]
    body = "\n".join("  <url><loc>%s</loc>%s</url>" % (esc(u), "<lastmod>%s</lastmod>" % d if d else "") for u, d in urls)
    (SITE / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}\n</urlset>\n',
        encoding="utf-8")


def write_search(items: list[dict], series: list[dict], portswigger: dict | None = None) -> None:
    rows = []
    kinds = {"writeups": "Write-up", "tools": "Tool", "cheatsheets": "Cheat sheet", "projects": "Project", "curated": "Link"}
    if portswigger:
        o = portswigger["overall"]
        rows.append({"t": "PortSwigger Academy progress", "k": "Progress", "u": "hub/#progress", "s": f'{o["done"]}/{o["total"]} labs', "g": "portswigger academy labs apprentice practitioner expert"})
    for s in series:
        rows.append({"t": s["name"], "k": "Category", "u": s["href"], "s": f'{s["count"]} {s["unit"]}'})
    tag_counts: dict[str, int] = {}
    for i in items:
        for t in i["tags"]:
            tag_counts[t.lower()] = tag_counts.get(t.lower(), 0) + 1
        if i["type"] == "writeups":
            rows.append({"t": i["title"], "k": "Write-up", "u": i["href"], "s": i["platform"], "g": " ".join(i["tags"])})
        else:
            rows.append({"t": i["title"], "k": kinds[i["type"]], "u": i.get("live") or i["url"], "x": 1,
                         "s": i.get("display") or " ".join(i["tags"][:3]), "g": " ".join(i["tags"])})
    for t, n in sorted(tag_counts.items(), key=lambda kv: -kv[1]):
        rows.append({"t": t, "k": "Tag", "u": "hub/?tags=" + urllib.parse.quote(t), "s": f"{n} items"})
    out = SITE / "data" / "search.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rows, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


def render_all(items, series, profile, stats, root, site, site_url, site_name, github, portswigger=None) -> None:
    global ROOT, SITE, SITE_URL, SITE_NAME, GITHUB, REPO_SLUG
    ROOT, SITE, SITE_URL, SITE_NAME, GITHUB = root, site, site_url, site_name, github
    REPO_SLUG = github.removeprefix("https://github.com/")
    by_id = {i["id"]: i for i in items}
    series_by_slug = {s["slug"]: s for s in series}
    n = 0
    for it in items:
        if it["type"] == "writeups":
            write_article(it, by_id, series_by_slug)
            n += 1
    for s in series:
        write_series(s, by_id)
    write_feed(items)
    write_sitemap(items, series)
    write_search(items, series, portswigger)
    print(f"rendered {n} write-up pages, {len(series)} category pages")
