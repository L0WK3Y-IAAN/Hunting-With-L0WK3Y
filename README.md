![Banner](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/src/img/HWL.gif?raw=true)
![Visitor Count](https://komarev.com/ghpvc/?username=L0WK3Y-IAAN&color=red&style=for-the-badge)


Welcome to **Hunting with L0WK3Y 👾** — a comprehensive repository documenting my journey in the exciting world of bug bounty hunting and ethical hacking.  

This repository is more than just a collection of tools and techniques; it’s a reflection of my growth, challenges, and successes in the cybersecurity field. Whether you’re just starting or looking to refine your skills, this space is designed to inspire and guide you through your own journey.  

## What This Repository Offers  

- **Resources 📖**: Handpicked tools, learning materials, cheat sheets and methodologies to elevate your bug bounty skills. 
  
- **Projects 🧪**: Explore custom tools, scripts, and proof of concepts developed to streamline hunting and testing.  
  
- **Write-Ups 📝**: Dive into detailed analyses of vulnerabilities, CTF challenges, and real-world bug bounty experiences.  
  
- **And MUCH more 👀** -  Whether you're here to gain knowledge, contribute, or connect, I’m thrilled to have you join me on this adventure.  

### Let’s hunt! 🕵️‍♂️💻  


## 🔗 Quick Links

<div align="left">
  <a href="https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y">
    <img src="https://img.shields.io/badge/Home-930b18?style=for-the-badge&logo=github&logoColor=white" alt="Home">
  </a>
  <a href="https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/tree/main/Resources">
    <img src="https://img.shields.io/badge/Resources-00800c?style=for-the-badge&logo=github&logoColor=white" alt="Resources">
  </a>
  <a href="https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/tree/main/Projects">
    <img src="https://img.shields.io/badge/Projects-930b18?style=for-the-badge&logo=github&logoColor=white" alt="Projects">
  </a>
  <a href="https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/tree/main/Resources/Personal/Write-ups">
    <img src="https://img.shields.io/badge/Blog-00800c?style=for-the-badge&logo=github&logoColor=white" alt="Write-ups">
  </a>
</div>

## 🌐 The Hub (auto-updating site)

Everything in this repo is browsable at **https://l0wk3y-iaan.github.io/Hunting-With-L0WK3Y/**, a retro desktop where categories are folders and write-ups open in windows. A plain, searchable version lives at **/hub/** (phones, touch screens and "Simple View" go there automatically). The site is rebuilt from the repo on every push, so there is nothing to edit by hand.

### Adding content
Add files in the usual place and push. That is all.

| Content | Where | What becomes one card |
| --- | --- | --- |
| Write-up | `Resources/Personal/Write-ups/<Platform>/<Category>/<Lab>/README.md` (or `<Lab>.md`) | each Markdown file, rendered as its own page and filed under its category |
| Tool | `Resources/Personal/Tools/<Lang>/<Tool>/` with a `README.md`, or a loose script | each folder or script |
| Cheat sheet | `Resources/Personal/Cheat Sheets/<Name>/` with a `README.md` and/or `index.html` | each folder (an `index.html` is hosted on the site) |
| Curated link | a bullet `- [name](url) - description - Topics: a, b` in `Resources/External/*/README.md` | each bullet (language and topics are also pulled from the GitHub API) |
| Project | `Projects/<Name>/README.md` | each folder |

### Frontmatter for write-ups (all optional)
Copy this to the top of a new write-up and delete what you don't need:

```yaml
---
title: Union-based SQLi on a login form   # default: first "# Heading", then the folder name
description: One sentence for the card.   # default: first paragraph (markdown/emoji stripped, cut at a sentence or word)
date: 2026-10-30                          # default: date the file was first committed (moves keep it)
tags: [sqli, web, burp]                   # category and sub-folders are added automatically
platform: PortSwigger Academy             # default: the first folder under Write-ups/
category: Web                             # default: the folder above the lab (PortSwigger is filed under Web via scripts/categories.json)
series: Web Basics                        # optional: replaces the category as the grouping, see "Categories" below
order: 3                                  # position inside its group (default: FLAG ONE/TWO.., trailing numbers, then date)
unit: labs                                # counter label on the category card (default: "write-ups")
difficulty: medium                        # easy | medium | hard | insane, shown as a badge
draft: true                               # hide the file from the site
---
```

`date` always wins over git, so editing a write-up never reshuffles the timeline. Other optional fields: `updated`, `slug` (override the URL).

### Categories
The hub groups write-ups by **category**: one card (and one page) per category, e.g. Android, Web, Mobile, Reverse Engineering, LLM Red Teaming. A category page lists its write-ups grouped by platform (Injured Android, PentesterLab, ...), each in order.
- The category is the folder above the lab (`<Platform>/<Category>/<Lab>`), so the repo layout stays as it is.
- To re-file write-ups under another category without moving files, edit `scripts/categories.json`: `by_platform` maps a whole platform (PortSwigger Academy -> **Web**) and `by_category` maps a folder category (Android -> **Mobile**). The original folder category stays as a searchable tag, so the Android write-ups sit in Mobile and the `Android` tag filters them.
- To override a single write-up, set `category:` in its frontmatter. To group write-ups some other way, set `series: Some Name` and that replaces the category as the group.
- Order inside a platform: `order`, then number words and trailing numbers in the title (`FLAG TWO`, `Android 07`), then date.

### Desktop view
`site/index.html` + `site/assets/desktop.{css,js}` render the same `data/index.json` as a Windows 98-style desktop: each category is a folder (platforms are sub-folders), the Toolbox, Favorites (curated links) and Projects are folders, and a write-up opens in its own draggable window (an iframe of its static page in `?embed` mode). Start > Find (or Ctrl K) searches everything, Run opens things by name, and `#open=<page path>` links straight to a window. Add content as usual and the desktop updates itself; there is nothing desktop-specific to maintain. `?desktop` forces the desktop on small screens, and Start > Simple View (or the "Desktop view" link on the hub) switches between the two. The desktop look is inspired by the "Windows 95" CodePen by Gabrielle Wee (MIT, see `site/assets/LICENSE-windows-95.txt`); the icons are Windows 98 icons (`site/assets/icons98/`, © Microsoft, from the Windows98Scaled icon pack), with a few drawn fallbacks in `site/assets/icons95.js`.

### PortSwigger progress
The "My PortSwigger Academy Progress" list and the "Topic Progress" table in this README are the source of truth. The build parses them, so editing the numbers here and pushing updates the progress section on the hub, the PortSwigger window on the desktop, and the search palette. Keep the existing row format (`| Topic | Labs | solved/total | status emoji | MM/DD/YYYY |`, status 🟢 done, 🔵 in progress, 🔴 not started).

### Profile links
Edit `site/profile.json` for the bio and the links in the hero. Links with an empty `"url"` (HackerOne is a placeholder) are hidden until you fill them in.

### How the auto-update works
1. `scripts/build_index.py` scans the content folders and writes `site/data/index.json`. `scripts/hub_pages.py` renders each write-up (Markdown to HTML with syntax highlighting, table of contents, series navigation), each series page, `feed.xml`, `sitemap.xml` and the search index.
2. `.github/workflows/pages.yml` runs it on every push to `main` and deploys `site/` to GitHub Pages. A second job refreshes the "Latest Blog Posts" table below with a normal (non-forced) commit.
3. `site/index.html` and `site/assets/` are plain HTML/CSS/JS that read the JSON: live search, type and tag filters, sorting, a Ctrl/Cmd+K command palette, and shareable URLs.

Preview locally (a virtualenv avoids the "externally managed environment" error on Homebrew Python):

```bash
python3 -m venv .venv                         # once
.venv/bin/pip install -r scripts/requirements.txt   # once
.venv/bin/python scripts/build_index.py       # add --readme to refresh the table below, --offline to skip GitHub API calls
python3 -m http.server -d site 8000           # then open http://localhost:8000
```

## My PortSwigger Academy Progress

- **🟢 Apprentice**: 37/59 (62.7%)
- **🔵 Practitioner**: 29/171 (17.0%)
- **🟣 Expert**: 0/39 (0.0%)

## Topic Progress
| Topic 📖 | Labs 🔬 | Progress ✅ | Status ⭕️ | Last Updated 🗓️ |
|---|---|---|:---:|---|
| **Server-side topics 🟧** | | | | |
| SQL injection | 18 | 5/18 | 🔵 | 05/01/2025 |
| Authentication | 14 | 7/14 | 🔵 | 05/01/2025 |
| Path traversal | 6 | 5/6 | 🔵 | 05/01/2025 |
| Command injection | 5 | 2/5 | 🔵 | 05/01/2025 |
| Business logic vulnerabilities | 11 | 0/11 | 🔴 | 05/01/2025 |
| Information disclosure | 5 | 5/5 | 🟢 | 05/01/2025 |
| Access control | 13 | 10/13 | 🔵 | 05/01/2025 |
| File upload vulnerabilities | 7 | 0/7 | 🔴 | 05/01/2025 |
| Race conditions | 6 | 3/6 | 🔵 | 05/01/2025 |
| Server-side request forgery (SSRF) | 7 | 2/7 | 🔵 | 05/01/2025 |
| XXE injection | 9 | 3/9 | 🔵 | 05/01/2025 |
| NoSQL injection | 4 | 1/4 | 🔵 | 05/01/2025 |
| API testing | 5 | 2/5 | 🔵 | 05/01/2025 |
| Web cache deception | 5 | 0/5 | 🔴 | 05/01/2025 |
| **Client-side topics 🟧** | | | | |
| Cross-site scripting (XSS) | 30 | 13/30 | 🔵 | 05/01/2025 |
| Cross-site request forgery (CSRF) | 12 | 2/12 | 🔵 | 05/01/2025 |
| Cross-origin resource sharing (CORS) | 3 | 0/3 | 🔴 | 05/01/2025 |
| Clickjacking | 5 | 0/5 | 🔴 | 05/01/2025 |
| DOM-based vulnerabilities | 7 | 1/7 | 🔵 | 05/01/2025 |
| WebSockets | 3 | 1/3 | 🔵 | 05/01/2025 |
| **Advanced topics 🟧** | | | | |
| Insecure deserialization | 10 | 0/10 | 🔴 | 05/01/2025 |
| Web LLM attacks | 4 | 0/4 | 🔴 | 05/01/2025 |
| GraphQL API vulnerabilities | 5 | 0/5 | 🔴 | 05/01/2025 |
| Server-side template injection | 7 | 1/7 | 🔵 | 05/01/2025 |
| Web cache poisoning | 13 | 0/13 | 🔴 | 05/01/2025 |
| HTTP Host header attacks | 7 | 0/7 | 🔴 | 05/01/2025 |
| HTTP request smuggling | 21 | 0/21 | 🔴 | 05/01/2025 |
| OAuth authentication | 6 | 0/6 | 🔴 | 05/01/2025 |
| JWT attacks | 8 | 3/8 | 🔵 | 05/01/2025 |
| Prototype pollution | 10 | 0/10 | 🔴 | 05/01/2025 |
| Essential skills | 2 | 0/2 | 🔴 | 05/01/2025 |


## 🔍 Latest Blog Posts

| Platform | Lab | Category | Date Posted |
| --- | --- | --- | --- |
| PortSwigger Academy | [Username enumeration via subtly different responses](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PortSwigger%20Academy/Server-side%20topics/Authentication/Username%20enumeration%20via%20subtly%20different%20responses/README.md) | Web | 10-31-2026 |
| PortSwigger Academy | [Username enumeration via different responses](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PortSwigger%20Academy/Server-side%20topics/Authentication/Username%20enumeration%20via%20different%20responses/README.md) | Web | 10-31-2026 |
| PortSwigger Academy | [User role can be modified in user profile](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PortSwigger%20Academy/Server-side%20topics/Access%20control/User%20role%20can%20be%20modified%20in%20user%20profile/README.md) | Web | 10-31-2026 |
| PortSwigger Academy | [Unprotected admin functionality with unpredictable URL](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PortSwigger%20Academy/Server-side%20topics/Access%20control/Unprotected%20admin%20functionality%20with%20unpredictable%20URL/README.md) | Web | 10-31-2026 |
| PortSwigger Academy | [Unprotected admin functionality](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PortSwigger%20Academy/Server-side%20topics/Access%20control/Unprotected%20admin%20functionality/README.md) | Web | 10-31-2026 |
| PortSwigger Academy | [Stored XSS into onclick event with angle brackets and double quotes HTML-encoded and single quotes and backslash escaped](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PortSwigger%20Academy/Client-side%20topics/Cross-site%20scripting/Stored%20XSS%20into%20onclick%20event%20with%20angle%20brackets%20and%20double%20quotes%20HTML-encoded%20and%20single%20quotes%20and%20backslash%20escaped/README.md) | Web | 10-31-2026 |
| PortSwigger Academy | [Stored XSS into anchor href attribute with double quotes HTML-encoded](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PortSwigger%20Academy/Client-side%20topics/Cross-site%20scripting/Stored%20XSS%20into%20anchor%C2%A0href%C2%A0attribute%20with%20double%20quotes%20HTML-encoded/README.md) | Web | 10-31-2026 |
| HackTheBox | [Spookifier](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/HackTheBox/Web/Spookifier/README.md) | Web | 10-31-2026 |
| PortSwigger Academy | [Single-endpoint race conditions](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PortSwigger%20Academy/Server-side%20topics/Race%20conditions/Single-endpoint%20race%20conditions/README.md) | Web | 10-31-2026 |
| PortSwigger Academy | [SQL injection vulnerability in WHERE clause allowing retrieval of hidden data](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PortSwigger%20Academy/Server-side%20topics/SQL%20injection/SQL%20injection%20vulnerability%20in%20WHERE%20clause%20allowing%20retrieval%20of%20hidden%20data/README.md) | Web | 10-31-2026 |
| PortSwigger Academy | [SQL injection attack, querying the database type and version on Oracle](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PortSwigger%20Academy/Server-side%20topics/SQL%20injection/SQL%20injection%20attack%2C%20querying%20the%20database%20type%20and%20version%20on%20Oracle/README.md) | Web | 10-31-2026 |
| PortSwigger Academy | [SQL injection UNION attack, retrieving multiple values in a single column](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PortSwigger%20Academy/Server-side%20topics/SQL%20injection/SQL%20injection%20UNION%20attack%2C%20retrieving%20multiple%20values%20in%20a%20single%20column/README.md) | Web | 10-31-2026 |
| PortSwigger Academy | [SQL injection UNION attack, retrieving data from other tables](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PortSwigger%20Academy/Server-side%20topics/SQL%20injection/SQL%20injection%20UNION%20attack%2C%20retrieving%20data%20from%20other%20tables/README.md) | Web | 10-31-2026 |
| PortSwigger Academy | [SQL injection UNION attack, finding a column containing text](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PortSwigger%20Academy/Server-side%20topics/SQL%20injection/SQL%20injection%20UNION%20attack%2C%20finding%20a%20column%20containing%20text/README.md) | Web | 10-31-2026 |
| PortSwigger Academy | [SQL injection UNION attack, determining the number of columns returned by the query](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PortSwigger%20Academy/Server-side%20topics/SQL%20injection/SQL%20injection%20UNION%20attack%2C%20determining%20the%20number%20of%20columns%20returned%20by%20the%20query/README.md) | Web | 10-31-2026 |
| PortSwigger Academy | [Reflected XSS into a template literal with angle brackets, single, double quotes, backslash and backticks Unicode-escaped](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PortSwigger%20Academy/Client-side%20topics/Cross-site%20scripting/Reflected%20XSS%20into%20a%20template%20literal%20with%20angle%20brackets%2C%20single%2C%20double%20quotes%2C%20backslash%20and%20backticks%20Unicode-escaped/README.md) | Web | 10-31-2026 |
| PortSwigger Academy | [Reflected XSS into a JavaScript string with single quote and backslash escaped](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PortSwigger%20Academy/Client-side%20topics/Cross-site%20scripting/Reflected%20XSS%20into%20a%20JavaScript%20string%20with%20single%20quote%20and%20backslash%20escaped/README.md) | Web | 10-31-2026 |
| PortSwigger Academy | [Reflected XSS into a JavaScript string with angle brackets and double quotes HTML-encoded and single quotes escaped](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PortSwigger%20Academy/Client-side%20topics/Cross-site%20scripting/Reflected%20XSS%20into%20a%20JavaScript%20string%20with%20angle%20brackets%20and%20double%20quotes%20HTML-encoded%20and%20single%20quotes%20escaped/README.md) | Web | 10-31-2026 |
| PortSwigger Academy | [Reflected XSS into a JavaScript string with angle brackets HTML encoded](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PortSwigger%20Academy/Client-side%20topics/Cross-site%20scripting/Reflected%20XSS%20into%20a%20JavaScript%20string%20with%20angle%20brackets%20HTML%20encoded/README.md) | Web | 10-31-2026 |
| PortSwigger Academy | [Reflected XSS into HTML context with most tags and attributes blocked](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PortSwigger%20Academy/Client-side%20topics/Cross-site%20scripting/Reflected%20XSS%20into%20HTML%20context%20with%20most%20tags%20and%20attributes%20blocked/README.md) | Web | 10-31-2026 |
| PortSwigger Academy | [Referer-based access control](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PortSwigger%20Academy/Server-side%20topics/Access%20control/Referer-based%20access%20control/README.md) | Web | 10-31-2026 |
| PortSwigger Academy | [Password reset broken logic](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PortSwigger%20Academy/Server-side%20topics/Authentication/Password%20reset%20broken%20logic/README.md) | Web | 10-31-2026 |
| HackTheBox | [OnlyHack](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/HackTheBox/Web/OnlyHack/README.md) | Web | 10-31-2026 |
| PortSwigger Academy | [OS command injection, simple case](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PortSwigger%20Academy/Server-side%20topics/OS%20command%20injection/OS%20command%20injection%2C%20simple%20case/README.md) | Web | 10-31-2026 |
| PortSwigger Academy | [Limit overrun race conditions](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PortSwigger%20Academy/Server-side%20topics/Race%20conditions/Limit%20overrun%20race%20conditions/README.md) | Web | 10-31-2026 |
| PortSwigger Academy | [JWT authentication bypass via unverified signature](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PortSwigger%20Academy/Server-side%20topics/JWT%20attacks/JWT%20authentication%20bypass%20via%20unverified%20signature/README.md) | Web | 10-31-2026 |
| PortSwigger Academy | [Insecure direct object references](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PortSwigger%20Academy/Server-side%20topics/Access%20control/Insecure%20direct%20object%20references/README.md) | Web | 10-31-2026 |
| PortSwigger Academy | [File path traversal, validation of start of path](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PortSwigger%20Academy/Server-side%20topics/Path%20traversal/File%20path%20traversal%2C%20validation%20of%20start%20of%20path/README.md) | Web | 10-31-2026 |
| PortSwigger Academy | [File path traversal, traversal sequences blocked with absolute path bypass](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PortSwigger%20Academy/Server-side%20topics/Path%20traversal/File%20path%20traversal%2C%20traversal%20sequences%20blocked%20with%20absolute%20path%20bypass/README.md) | Web | 10-31-2026 |
| PortSwigger Academy | [File path traversal, simple case](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PortSwigger%20Academy/Server-side%20topics/Path%20traversal/File%20path%20traversal%2C%20simple%20case/README.md) | Web | 10-31-2026 |
| PortSwigger Academy | [Exploiting a mass assignment vulnerability](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PortSwigger%20Academy/Server-side%20topics/API%20testing/Exploiting%20a%20mass%20assignment%20vulnerability/README.md) | Web | 10-31-2026 |
| PortSwigger Academy | [Exploiting XXE via image file upload](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PortSwigger%20Academy/Server-side%20topics/XXE%20injection/Exploiting%20XXE%20via%20image%20file%20upload/README.md) | Web | 10-31-2026 |
| PortSwigger Academy | [Exploiting XXE using external entities to retrieve files](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PortSwigger%20Academy/Server-side%20topics/XXE%20injection/Exploiting%20XXE%20using%20external%20entities%20to%20retrieve%20files/README.md) | Web | 10-31-2026 |
| PortSwigger Academy | [Exploiting XSS to perform CSRF](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PortSwigger%20Academy/Client-side%20topics/Cross-site%20scripting/Exploiting%20XSS%20to%20perform%20CSRF/README.md) | Web | 10-31-2026 |
| PortSwigger Academy | [Exploiting XInclude to retrieve files](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PortSwigger%20Academy/Server-side%20topics/XXE%20injection/Exploiting%20XInclude%20to%20retrieve%20files/README.md) | Web | 10-31-2026 |
| PortSwigger Academy | [Exploiting NoSQL operator injection to bypass authentication](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PortSwigger%20Academy/Server-side%20topics/SQL%20injection/Exploiting%20NoSQL%20operator%20injection%20to%20bypass%20authentication/README.md) | Web | 10-31-2026 |
| PortSwigger Academy | [Exploiting LLM APIs with excessive agency](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PortSwigger%20Academy/Server-side%20topics/Web%20LLM%20attacks/Exploiting%20LLM%20APIs%20with%20excessive%20agency/README.md) | Web | 10-31-2026 |
| HackTheBox | [Dont Overreact](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/HackTheBox/Mobile/Dont%20Overreact/README.md) | Mobile | 10-31-2026 |
| PortSwigger Academy | [DOM-based open redirection](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PortSwigger%20Academy/Client-side%20topics/DOM-based%20vulnerabilities/DOM-based%20open%20redirection/README.md) | Web | 10-31-2026 |
| PortSwigger Academy | [DOM XSS in document.write sink using source location.search inside a select element](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PortSwigger%20Academy/Client-side%20topics/Cross-site%20scripting/DOM%20XSS%20in%20document.write%20sink%20using%20source%20location.search%20inside%20a%20select%20element/README.md) | Web | 10-31-2026 |
| PortSwigger Academy | [DOM XSS in document.write sink using source location.search](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PortSwigger%20Academy/Client-side%20topics/Cross-site%20scripting/DOM%20XSS%20in%20document.write%20sink%20using%20source%20location.search/README.md) | Web | 10-31-2026 |
| PortSwigger Academy | [Blind SQL injection with time delays](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PortSwigger%20Academy/Server-side%20topics/SQL%20injection/Blind%20SQL%20injection%20with%20time%20delays/README.md) | Web | 10-31-2026 |
| PortSwigger Academy | [Blind SQL injection with conditional responses](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PortSwigger%20Academy/Server-side%20topics/SQL%20injection/Blind%20SQL%20injection%20with%20conditional%20responses/README.md) | Web | 10-31-2026 |
| PortSwigger Academy | [Blind OS command injection with time delays](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PortSwigger%20Academy/Server-side%20topics/OS%20command%20injection/Blind%20OS%20command%20injection%20with%20time%20delays/README.md) | Web | 10-31-2026 |
| PortSwigger Academy | [Blind OS command injection with output redirection](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PortSwigger%20Academy/Server-side%20topics/OS%20command%20injection/Blind%20OS%20command%20injection%20with%20output%20redirection/README.md) | Web | 10-31-2026 |
| PortSwigger Academy | [Basic server-side template injection](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PortSwigger%20Academy/Server-side%20topics/Server-side%20template%20injection/Basic%20server-side%20template%20injection/README.md) | Web | 10-31-2026 |
| PortSwigger Academy | [Basic SSRF against the local server](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PortSwigger%20Academy/Server-side%20topics/Server-side%20request%20forgery%20%28SSRF%29/Basic%20SSRF%20against%20the%20local%20server/README.md) | Web | 10-31-2026 |
| PortSwigger Academy | [Basic SSRF against another back-end system](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PortSwigger%20Academy/Server-side%20topics/Server-side%20request%20forgery%20%28SSRF%29/Basic%20SSRF%20against%20another%20back-end%20system/README.md) | Web | 10-31-2026 |
| Wiz | [Prompt Airlines CTF](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/Wiz/LLM%20Red%20Teaming/Prompt%20Airlines%20CTF/README.md) | LLM Red Teaming | 10-29-2026 |
| Bugforge.io | [Gift Lab - Daily](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/Bugforge.io/Web/Gift%20Lab%20-%20Daily/README.md) | Web | 03-25-2026 |
| Bugforge.io | [CopyPasta - Daily](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/Bugforge.io/Web/CopyPasta%20-%20Daily/README.md) | Web | 03-25-2026 |
| 8kSec | [Ultimate Essay Grader](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/8kSec/AI/LLM%20Red%20Teaming/Ultimate%20Essay%20Grader/README.md) | LLM Red Teaming | 01-06-2026 |
| tlamb96 | [KGB Messenger](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/tlamb96/Android/KGB%20Messenger.md) | Mobile | 01-06-2026 |
| 8kSec | [FactsDroid](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/8kSec/Android/FactsDroid/README.md) | Mobile | 01-06-2026 |
| Injured Android | [FLAG TWELVE – (PROTECTED COMPONENTS)](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/Injured%20Android/Android/FLAG%20TWELVE%20%E2%80%93%20%28PROTECTED%20COMPONENTS%29/FLAG%20TWELVE%20%E2%80%93%20%28PROTECTED%20COMPONENTS%29.md) | Mobile | 12-23-2025 |
| Injured Android | [FLAG THIRTEEN – (RCE)](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/Injured%20Android/Android/FLAG%20THIRTEEN%20%E2%80%93%20%28RCE%29/FLAG%20THIRTEEN%20%E2%80%93%20%28RCE%29.md) | Mobile | 12-23-2025 |
| Injured Android | [FLAG TEN – (UNICODE)](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/Injured%20Android/Android/FLAG%20TEN%20%E2%80%93%20%28UNICODE%29/FLAG%20TEN%20%E2%80%93%20%28UNICODE%29.md) | Mobile | 12-23-2025 |
| Injured Android | [FLAG ELEVEN – (DEEP LINKS)](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/Injured%20Android/Android/FLAG%20ELEVEN%20%E2%80%93%20%28DEEP%20LINKS%29/FLAG%20ELEVEN%20%E2%80%93%20%28DEEP%20LINKS%29.md) | Mobile | 12-23-2025 |
| Injured Android | [FLAG EIGHT & NINE – (AWS + Firebase)](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/Injured%20Android/Android/FLAG%20EIGHT%20%26%20NINE%20%E2%80%93%20%28AWS%20%2B%20Firebase%29/FLAG%20EIGHT%20%26%20NINE%20%E2%80%93%20%28AWS%20%2B%20Firebase%29.md) | Mobile | 12-23-2025 |
| Injured Android | [Getting Started + FLAG ONE (LOGIN)](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/Injured%20Android/Android/Getting%20Started%20%2B%20FLAG%20ONE%20%28LOGIN%29/Getting%20Started%20%2B%20FLAG%20ONE%20%28LOGIN%29.md) | Mobile | 12-22-2025 |
| Injured Android | [FLAG TWO – (EXPORTED ACTIVITY)](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/Injured%20Android/Android/FLAG%20TWO%20%E2%80%93%20%28EXPORTED%20ACTIVITY%29/FLAG%20TWO%20%E2%80%93%20%28EXPORTED%20ACTIVITY%29.md) | Mobile | 12-22-2025 |
| Injured Android | [FLAG THREE – (RESOURCES)](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/Injured%20Android/Android/FLAG%20THREE%20%E2%80%93%20%28RESOURCES%29/FLAG%20THREE%20%E2%80%93%20%28RESOURCES%29.md) | Mobile | 12-22-2025 |
| Injured Android | [FLAG SIX – (LOGIN 3)](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/Injured%20Android/Android/FLAG%20SIX%20%E2%80%93%20%28LOGIN%203%29/FLAG%20SIX%20%E2%80%93%20%28LOGIN%203%29.md) | Mobile | 12-22-2025 |
| Injured Android | [FLAG SEVEN – (SQLITE)](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/Injured%20Android/Android/FLAG%20SEVEN%20%E2%80%93%20%28SQLITE%29/FLAG%20SEVEN%20%E2%80%93%20%28SQLITE%29.md) | Mobile | 12-22-2025 |
| Injured Android | [FLAG FOUR – (LOGIN 2)](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/Injured%20Android/Android/FLAG%20FOUR%20%E2%80%93%20%28LOGIN%202%29/FLAG%20FOUR%20%E2%80%93%20%28LOGIN%202%29.md) | Mobile | 12-22-2025 |
| Injured Android | [FLAG FIVE – (EXPORTED BROADCAST)](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/Injured%20Android/Android/FLAG%20FIVE%20%E2%80%93%20%28EXPORTED%20BROADCAST%29/FLAG%20FIVE%20%E2%80%93%20%28EXPORTED%20BROADCAST%29.md) | Mobile | 12-22-2025 |
| PortSwigger Academy | [Source code disclosure via backup files](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PortSwigger%20Academy/Server-side%20topics/Information%20disclosure/Source%20code%20disclosure%20via%20backup%20files/README.md) | Web | 11-23-2025 |
| infophreak | [Infophreak Halloween CTF 2025 - Spirit Halloween!](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/infophreak/Reverse%20Engineering/Infophreak%20Halloween%20CTF%202025%20-%20Spirit%20Halloween%21/README.md) | Reverse Engineering | 11-02-2025 |
| PentesterLab | [Android 08](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PentesterLab/Android/Android%2008/Android%2008.md) | Mobile | 10-25-2025 |
| PentesterLab | [Android 07](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PentesterLab/Android/Android%2007/Android%2007.md) | Mobile | 10-25-2025 |
| PentesterLab | [Android 06](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PentesterLab/Android/Android%2006/Android%2006.md) | Mobile | 10-25-2025 |
| PentesterLab | [Android 05](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PentesterLab/Android/Android%2005/Android%2005.md) | Mobile | 10-25-2025 |
| PentesterLab | [Android 04](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PentesterLab/Android/Android%2004/Android%2004.md) | Mobile | 10-25-2025 |
| PentesterLab | [Android 03](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PentesterLab/Android/Android%2003/Android%2003.md) | Mobile | 10-25-2025 |
| PentesterLab | [Android 02](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PentesterLab/Android/Android%2002/Android%2002.md) | Mobile | 10-25-2025 |
| PentesterLab | [Android 01](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PentesterLab/Android/Android%2001/Android%2001.md) | Mobile | 10-25-2025 |
| HackTheBox | [APKey](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/HackTheBox/Mobile/APKey/README.md) | Mobile | 09-22-2025 |
| PortSwigger Academy | [User role controlled by request parameter](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PortSwigger%20Academy/Server-side%20topics/Access%20control/User%20role%20controlled%20by%20request%20parameter/README.md) | Web | 09-21-2025 |
| HackTheBox | [Manager](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/HackTheBox/Mobile/Manager/README.md) | Mobile | 09-21-2025 |
| PortSwigger Academy | [Information disclosure on debug page](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PortSwigger%20Academy/Server-side%20topics/Information%20disclosure/Information%20disclosure%20on%20debug%20page/README.md) | Web | 01-20-2025 |
| PortSwigger Academy | [Information disclosure in version control history](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PortSwigger%20Academy/Server-side%20topics/Information%20disclosure/Information%20disclosure%20in%20version%20control%20history/README.md) | Web | 01-09-2025 |
| PortSwigger Academy | [Authentication bypass via information disclosure](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PortSwigger%20Academy/Server-side%20topics/Information%20disclosure/Authentication%20bypass%20via%20information%20disclosure/README.md) | Web | 01-08-2025 |
| PortSwigger Academy | [Information disclosure in error messages](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PortSwigger%20Academy/Server-side%20topics/Information%20disclosure/Information%20disclosure%20in%20error%20messages/README.md) | Web | 01-07-2025 |

## 🛠️ Tools & Technologies

<div align="left">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JavaScript">
  <img src="https://img.shields.io/badge/Burp_Suite-000000?style=for-the-badge&logo=burpsuite&logoColor=white" alt="Burp Suite">
  <img src="https://img.shields.io/badge/OWASP_ZAP-9C27B0?style=for-the-badge&logo=owasp-zap&logoColor=white" alt="OWASP ZAP">
  <img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white" alt="Git">
  <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub">
</div>



## 📫 Contact Me

<div align="left">
  <a href="https://linkedin.com/in/iaansec">
    <img src="https://custom-icon-badges.demolab.com/badge/LinkedIn-0A66C2?logo=linkedin-white&logoColor=fff">
  </a>
  <a href="https://twitter.com/L0WK3Y_OFFICIAL">
    <img src="https://img.shields.io/badge/X-%23000000.svg?logo=X&logoColor=white" alt="Twitter">
  </a>
</div>



## ❤️ Support

If you enjoy my work, consider giving a ⭐️ or [buying me a coffee](https://www.buymeacoffee.com/l0wk3y)! 😊

