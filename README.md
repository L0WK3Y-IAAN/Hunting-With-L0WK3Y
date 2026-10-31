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
| Wiz | [Prompt Airlines CTF](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/Wiz/LLM%20Red%20Teaming/Prompt%20Airlines%20CTF/README.md) | LLM Red Teaming | 10-29-2026 |
| Bugforge.io | [Gift Lab - Daily](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/Bugforge.io/Web/Gift%20Lab%20-%20Daily/README.md) | Web | 03-25-2026 |
| Bugforge.io | [CopyPasta - Daily](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/Bugforge.io/Web/CopyPasta%20-%20Daily/README.md) | Web | 03-25-2026 |
| 8kSec | [Ultimate Essay Grader](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/8kSec/AI/LLM%20Red%20Teaming/Ultimate%20Essay%20Grader/README.md) | LLM Red Teaming | 01-06-2026 |
| tlamb96 | [KGB Messenger](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/tlamb96/Android/KGB%20Messenger.md) | Android | 01-06-2026 |
| 8kSec | [FactsDroid](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/8kSec/Android/FactsDroid/README.md) | Android | 01-06-2026 |
| Injured Android | [FLAG TWELVE – (PROTECTED COMPONENTS)](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/Injured%20Android/Android/FLAG%20TWELVE%20%E2%80%93%20%28PROTECTED%20COMPONENTS%29/FLAG%20TWELVE%20%E2%80%93%20%28PROTECTED%20COMPONENTS%29.md) | Android | 12-23-2025 |
| Injured Android | [FLAG THIRTEEN – (RCE)](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/Injured%20Android/Android/FLAG%20THIRTEEN%20%E2%80%93%20%28RCE%29/FLAG%20THIRTEEN%20%E2%80%93%20%28RCE%29.md) | Android | 12-23-2025 |
| Injured Android | [FLAG TEN – (UNICODE)](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/Injured%20Android/Android/FLAG%20TEN%20%E2%80%93%20%28UNICODE%29/FLAG%20TEN%20%E2%80%93%20%28UNICODE%29.md) | Android | 12-23-2025 |
| Injured Android | [FLAG ELEVEN – (DEEP LINKS)](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/Injured%20Android/Android/FLAG%20ELEVEN%20%E2%80%93%20%28DEEP%20LINKS%29/FLAG%20ELEVEN%20%E2%80%93%20%28DEEP%20LINKS%29.md) | Android | 12-23-2025 |
| Injured Android | [FLAG EIGHT & NINE – (AWS + Firebase)](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/Injured%20Android/Android/FLAG%20EIGHT%20%26%20NINE%20%E2%80%93%20%28AWS%20%2B%20Firebase%29/FLAG%20EIGHT%20%26%20NINE%20%E2%80%93%20%28AWS%20%2B%20Firebase%29.md) | Android | 12-23-2025 |
| Injured Android | [Getting Started + FLAG ONE (LOGIN)](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/Injured%20Android/Android/Getting%20Started%20%2B%20FLAG%20ONE%20%28LOGIN%29/Getting%20Started%20%2B%20FLAG%20ONE%20%28LOGIN%29.md) | Android | 12-22-2025 |
| Injured Android | [FLAG TWO – (EXPORTED ACTIVITY)](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/Injured%20Android/Android/FLAG%20TWO%20%E2%80%93%20%28EXPORTED%20ACTIVITY%29/FLAG%20TWO%20%E2%80%93%20%28EXPORTED%20ACTIVITY%29.md) | Android | 12-22-2025 |
| Injured Android | [FLAG THREE – (RESOURCES)](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/Injured%20Android/Android/FLAG%20THREE%20%E2%80%93%20%28RESOURCES%29/FLAG%20THREE%20%E2%80%93%20%28RESOURCES%29.md) | Android | 12-22-2025 |
| Injured Android | [FLAG SIX – (LOGIN 3)](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/Injured%20Android/Android/FLAG%20SIX%20%E2%80%93%20%28LOGIN%203%29/FLAG%20SIX%20%E2%80%93%20%28LOGIN%203%29.md) | Android | 12-22-2025 |
| Injured Android | [FLAG SEVEN – (SQLITE)](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/Injured%20Android/Android/FLAG%20SEVEN%20%E2%80%93%20%28SQLITE%29/FLAG%20SEVEN%20%E2%80%93%20%28SQLITE%29.md) | Android | 12-22-2025 |
| Injured Android | [FLAG FOUR – (LOGIN 2)](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/Injured%20Android/Android/FLAG%20FOUR%20%E2%80%93%20%28LOGIN%202%29/FLAG%20FOUR%20%E2%80%93%20%28LOGIN%202%29.md) | Android | 12-22-2025 |
| Injured Android | [FLAG FIVE – (EXPORTED BROADCAST)](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/Injured%20Android/Android/FLAG%20FIVE%20%E2%80%93%20%28EXPORTED%20BROADCAST%29/FLAG%20FIVE%20%E2%80%93%20%28EXPORTED%20BROADCAST%29.md) | Android | 12-22-2025 |
| PortSwigger Academy | [Source code disclosure via backup files](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PortSwigger%20Academy/Server-side%20topics/Information%20disclosure/Source%20code%20disclosure%20via%20backup%20files/README.md) | Web | 11-23-2025 |
| infophreak | [Infophreak Halloween CTF 2025 - Spirit Halloween!](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/infophreak/Reverse%20Engineering/Infophreak%20Halloween%20CTF%202025%20-%20Spirit%20Halloween%21/README.md) | Reverse Engineering | 11-02-2025 |
| PentesterLab | [Android 08](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PentesterLab/Android/Android%2008/Android%2008.md) | Android | 10-25-2025 |
| PentesterLab | [Android 07](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PentesterLab/Android/Android%2007/Android%2007.md) | Android | 10-25-2025 |
| PentesterLab | [Android 06](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PentesterLab/Android/Android%2006/Android%2006.md) | Android | 10-25-2025 |
| PentesterLab | [Android 05](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PentesterLab/Android/Android%2005/Android%2005.md) | Android | 10-25-2025 |
| PentesterLab | [Android 04](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PentesterLab/Android/Android%2004/Android%2004.md) | Android | 10-25-2025 |
| PentesterLab | [Android 03](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PentesterLab/Android/Android%2003/Android%2003.md) | Android | 10-25-2025 |
| PentesterLab | [Android 02](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PentesterLab/Android/Android%2002/Android%2002.md) | Android | 10-25-2025 |
| PentesterLab | [Android 01](https://github.com/L0WK3Y-IAAN/Hunting-With-L0WK3Y/blob/main/Resources/Personal/Write-ups/PentesterLab/Android/Android%2001/Android%2001.md) | Android | 10-25-2025 |
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

