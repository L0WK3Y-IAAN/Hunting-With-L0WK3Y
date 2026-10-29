# Hub redesign: changelog

## Content
- **Categories:** write-ups group by category (Android, Web, Mobile, ...), one card and one page each, with entries grouped by platform inside. `scripts/categories.json` files a platform under another category (PortSwigger Academy -> Web) without touching the repo layout; `category:` or `series:` frontmatter overrides per write-up. Entries are ordered by `order`, number words (`FLAG TWO`) and trailing numbers, then date.
- **Reading pages:** every write-up renders as its own page at `writeups/<platform>/<name>/` with ~70ch typography, highlighted code with language labels and copy buttons, sticky table of contents (dropdown on mobile), read time, tags, series prev/next, reading progress bar, "view source on GitHub" and per-page Open Graph/JSON-LD tags. Repo images are copied into the site and given width/height so pages don't jump.
- **Metadata:** frontmatter `title`, `date`, `description`, `tags`, `platform`, `series`, `difficulty` (plus `order`, `unit`, `slug`, `updated`, `draft`). Auto descriptions strip markdown and emoji and cut at a sentence or word boundary.
- **Dates:** git "created" dates now follow renames and moves, so reorganising folders no longer changes chronology.
- **Curated links:** show the destination (`github.com/owner/repo`), with language and topic chips from the GitHub API (best effort, falls back silently), and no dates.

## Homepage
- New hero with bio, profile links (`site/profile.json`) and a `whoami` terminal with stats. The duplicate stats line is gone.
- "Recently added" carousel replaced by a compact **Latest** list of 5 with `NEW` badges (under 30 days). Those 5 are not repeated in the grid below.
- Sections: Series, standalone Write-ups, Toolbox (tools + cheat sheets), Curated links. Empty sections (Projects today) and their pills are hidden.
- Cards: platform label, title, 2-line description, topic chips, quiet date/read-time footer; equal heights, whole card clickable, glow/lift on hover, visible focus.

## Navigation
- Sticky search/filter bar (phones keep search + sort pinned). Type pills are real tabs (arrow keys). Top 8 tags plus a searchable "All tags" popover, multi-select, active-filter summary and "Clear filters".
- Search, tabs, tags and sort sync to the URL (`?q=&type=&tags=&sort=`) with working back button. Old `#q=` links still work.
- Section links with scroll-spy, Ctrl/Cmd+K command palette (titles, series, tools, tags), `/` to focus search, back-to-top button, friendly no-results state.

## Visual
- Sans-serif body and headings, monospace only for labels, chips, meta and code (13px minimum). Every text/background pair is at least 4.5:1 in both themes. A designed light theme. 4/8px spacing scale. Motion is subtle and off under `prefers-reduced-motion`.

## Extras
- `feed.xml` (Atom), `sitemap.xml`, `robots.txt`, favicon/apple-touch icons and an Open Graph image (`site/assets/og.png`).
- Lighthouse (local server, mobile and desktop): Performance 97-100, Accessibility 100, Best Practices 100, SEO 100 on the home, a long write-up, a code-heavy write-up and a series page.

## Pipeline
- Same flow as before: build script, generated index, GitHub Action deploy. The workflow now also runs `pip install -r scripts/requirements.txt` and passes `GITHUB_TOKEN` to the build.
- New dependencies: `markdown-it-py`, `pygments` (build time only; the site ships no frameworks).

## Desktop (new front door)
- `/` is now a Windows 95-style desktop; the previous site moved to `/hub/` (old `/#type=writeups` style links still work). Categories are folders (platform sub-folders inside), Toolbox/Favorites/Projects are folders, write-ups and the Mobile Security cheat sheet open in draggable, resizable, minimizable windows with taskbar buttons.
- Start menu (Programs, Documents, Find, Run, Help, Simple View, Shut Down), Find window, Run dialog, About Me notepad, Recycle Bin, clock, keyboard support (arrows, Enter, Backspace, Esc, Ctrl K).
- Write-up windows are iframes of the existing static pages in a light `?embed` mode, so the build pipeline is unchanged. `#open=<page path>` deep links work, including on phones (they go straight to the page).
- Phones, touch screens, narrow windows and no-JS visitors are sent to `/hub/`; `?desktop` overrides.
- Icons are drawn in code (no hotlinked CodePen assets). Credit and MIT license for the inspiration are in `site/assets/LICENSE-windows-95.txt`.
