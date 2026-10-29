/* Home page: renders series, write-ups, toolbox and curated links from data/index.json. */
(() => {
  'use strict';
  const PAGE = 9;              // cards per section before "Show all"
  const TOP_TAGS = 8;
  const NEW_DAYS = 30;
  const ROOT = document.documentElement.dataset.root || '';
  const abs = (h) => (/^https?:/.test(h) ? h : ROOT + h);
  const $ = (s, r = document) => r.querySelector(s);
  const el = (tag, props = {}, ...kids) => { const n = Object.assign(document.createElement(tag), props); kids.forEach((k) => n.append(k)); return n; };

  const GROUPS = [
    { id: 'writeups', label: 'Write-ups', types: ['writeups'] },
    { id: 'toolbox', label: 'Toolbox', types: ['tools', 'cheatsheets'] },
    { id: 'projects', label: 'Projects', types: ['projects'] },
    { id: 'curated', label: 'Curated links', types: ['curated'] },
  ];
  const groupOf = (it) => GROUPS.find((g) => g.types.includes(it.type)).id;
  const KIND = { tools: 'Tool', cheatsheets: 'Cheat sheet', projects: 'Project' };

  const state = { q: '', type: 'all', tags: [], sort: 'new' };
  const open = new Set();                // sections expanded with "Show all"
  let D, items, series, byId, groups, latestIds = new Set();

  /* ---------- helpers ---------- */
  const norm = (s) => s.toLowerCase();
  const fmt = (iso) => new Date(iso + 'T00:00:00Z').toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric', timeZone: 'UTC' });
  const isNew = (iso) => Date.now() - Date.parse(iso + 'T00:00:00Z') < NEW_DAYS * 864e5;
  const plural = (n, w) => (n === 1 ? w.replace(/s$/, '') : w);
  const hay = (o, build) => o._h || (o._h = norm(build(o)));
  const itemHay = (i) => hay(i, (x) => [x.title, x.description, x.platform, x.category, x.series, x.display, x.tags.join(' ')].filter(Boolean).join(' '));
  const serHay = (s) => hay(s, (x) => [x.name, x.platform, x._tags.join(' ')].filter(Boolean).join(' '));
  const terms = () => norm(state.q).split(/\s+/).filter(Boolean);
  const hasTags = (tags) => state.tags.every((t) => tags.some((x) => norm(x) === t));
  const matchItem = (i) => terms().every((t) => itemHay(i).includes(t)) && hasTags(i.tags);
  const matchSeries = (s) => terms().every((t) => serHay(s).includes(t)) && hasTags(s._tags);
  const sorters = {
    new: (a, b) => b.date.localeCompare(a.date) || a.title.localeCompare(b.title),
    old: (a, b) => a.date.localeCompare(b.date) || a.title.localeCompare(b.title),
    az: (a, b) => a.title.localeCompare(b.title, undefined, { sensitivity: 'base' }),
  };
  const serSort = {
    new: (a, b) => b.latest.localeCompare(a.latest) || a.name.localeCompare(b.name),
    old: (a, b) => a.latest.localeCompare(b.latest) || a.name.localeCompare(b.name),
    az: (a, b) => a.name.localeCompare(b.name, undefined, { sensitivity: 'base' }),
  };
  function highlight(text) {
    const ts = terms().filter((t) => t.length > 1);
    if (!ts.length) return [text];
    const re = new RegExp(`(${ts.map((t) => t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|')})`, 'ig');
    return text.split(re).map((p, i) => (i % 2 ? el('mark', { textContent: p }) : p));
  }

  /* ---------- URL state ---------- */
  function readURL() {
    const p = new URLSearchParams(location.search);
    if (location.hash.includes('=')) new URLSearchParams(location.hash.slice(1)).forEach((v, k) => p.set(k, v));   // old #q= links
    state.q = p.get('q') || '';
    state.type = p.get('type') || 'all';
    state.sort = p.get('sort') || 'new';
    state.tags = (p.get('tags') || '').split(',').map(norm).filter(Boolean);
    if (state.type !== 'all' && !groups.some((g) => g.id === state.type)) state.type = 'all';
    if (!sorters[state.sort]) state.sort = 'new';
  }
  function writeURL(push) {
    const p = new URLSearchParams();
    if (state.q) p.set('q', state.q);
    if (state.type !== 'all') p.set('type', state.type);
    if (state.sort !== 'new') p.set('sort', state.sort);
    if (state.tags.length) p.set('tags', state.tags.join(','));
    const url = location.pathname + (p.toString() ? '?' + p : '');
    if (url === location.pathname + location.search && !location.hash) return;
    history[push ? 'pushState' : 'replaceState'](null, '', url);
  }

  /* ---------- cards ---------- */
  function chipList(tags, max = 3) {
    if (!tags.length) return null;
    const ul = el('ul', { className: 'chips' });
    tags.slice(0, max).forEach((t) => {
      const b = el('button', { type: 'button', className: 'chip' + (state.tags.includes(norm(t)) ? ' on' : ''), textContent: t });
      b.setAttribute('aria-label', `Filter by ${t}`);
      b.addEventListener('click', () => toggleTag(norm(t), true));
      ul.append(el('li', {}, b));
    });
    if (tags.length > max) ul.append(el('li', {}, el('span', { className: 'chip more', textContent: `+${tags.length - max}` })));
    return ul;
  }
  function footRow(...bits) {
    const row = el('div', { className: 'foot-row' });
    bits.filter(Boolean).forEach((b) => row.append(b));
    return row;
  }
  const time = (iso) => el('time', { dateTime: iso, textContent: fmt(iso) });
  function link(card, href, text, external) {
    const a = el('a', { href }, ...highlight(text));
    if (external) { a.target = '_blank'; a.rel = 'noopener'; }
    card.append(el('h3', {}, a));
  }
  const wrap = (card) => el('li', {}, card);

  function writeupCard(it) {
    const c = el('article', { className: 'card' });
    const label = el('div', { className: 'label' }, it.platform || 'Write-up');
    if (isNew(it.date)) label.append(el('span', { className: 'new', textContent: 'New' }));
    c.append(label);
    link(c, abs(it.href), it.title);
    if (it.description) c.append(el('p', { className: 'desc' }, ...highlight(it.description)));
    const chips = chipList(it.tags); if (chips) c.append(chips);
    c.append(footRow(time(it.date), it.minutes && el('span', { className: 'min', textContent: `${it.minutes} min read` }),
      it.series && el('span', { className: 'sp', textContent: it.series })));
    return wrap(c);
  }
  function seriesCard(s) {
    const c = el('article', { className: 'card series-card' });
    const label = el('div', { className: 'label' }, 'Category');
    if (isNew(s.latest)) label.append(el('span', { className: 'new', textContent: 'New' }));
    c.append(label);
    link(c, abs(s.href), s.name);
    c.append(el('div', { className: 'big' }, String(s.count), el('small', { textContent: plural(s.count, s.unit) })));
    if (s.platforms.length) {                              // where the entries come from (plain labels, not filters)
      const ul = el('ul', { className: 'chips', ariaLabel: 'Platforms' });
      s.platforms.slice(0, 3).forEach((p) => ul.append(el('li', {}, el('span', { className: 'chip static', textContent: p }))));
      if (s.platforms.length > 3) ul.append(el('li', {}, el('span', { className: 'chip more', textContent: `+${s.platforms.length - 3}` })));
      c.append(ul);
    }
    c.append(footRow(el('span', {}, 'Latest ', time(s.latest))));
    return wrap(c);
  }
  function toolCard(it) {
    const c = el('article', { className: 'card' });
    c.append(el('div', { className: 'label' }, KIND[it.type] || 'Item'));
    const external = true;
    link(c, abs(it.live || it.url), it.title, external);
    if (it.description) c.append(el('p', { className: 'desc' }, ...highlight(it.description)));
    const chips = chipList(it.tags); if (chips) c.append(chips);
    const src = it.live ? el('a', { className: 'sp', href: it.url, target: '_blank', rel: 'noopener', textContent: 'source ↗' }) : null;
    if (src) src.style.cssText = 'position:relative;z-index:1;color:var(--muted)';
    c.append(footRow(time(it.date), src));
    return wrap(c);
  }
  function curatedCard(it) {
    const c = el('article', { className: 'card' });
    const kind = (it.tags[0] || 'Link').replace(/s$/, '').replace(/^Cheat Sheet$/, 'Cheat sheet');
    c.append(el('div', { className: 'label' }, kind));
    link(c, it.url, it.title, true);
    c.append(el('p', { className: 'url' }, it.display || it.url));
    if (it.description) c.append(el('p', { className: 'desc' }, ...highlight(it.description)));
    const chips = chipList(it.tags.slice(1)); if (chips) c.append(chips);
    return wrap(c);
  }
  const CARD = { writeups: writeupCard, tools: toolCard, cheatsheets: toolCard, projects: toolCard, curated: curatedCard };

  /* ---------- sections ---------- */
  function section(id, label, count, nodes, note) {
    const sec = el('section', { className: 'section fade', id });
    sec.setAttribute('aria-labelledby', id + '-h');
    sec.append(el('h2', { className: 'sec-h', id: id + '-h' }, el('span', { className: 'mono', textContent: '>', ariaHidden: 'true' }), label, el('small', { textContent: note || String(count) })));
    const ul = el('ul', { className: 'grid' });
    const full = open.has(id) || state.type !== 'all';
    (full ? nodes : nodes.slice(0, PAGE)).forEach((n) => ul.append(n));
    sec.append(ul);
    if (!full && nodes.length > PAGE) {
      const b = el('button', { type: 'button', className: 'btn showall', textContent: `Show all ${nodes.length}` });
      b.addEventListener('click', () => { open.add(id); renderResults(); $('#' + id + ' .grid li:nth-child(' + (PAGE + 1) + ') a')?.focus(); });
      sec.append(b);
    }
    return sec;
  }

  function renderLatest() {
    const wrapEl = $('#latest-wrap');
    const showing = !state.q && !state.tags.length && state.type === 'all';
    wrapEl.hidden = !showing;
    if (!showing) return;
    $('#latest').replaceChildren(...items.filter((i) => latestIds.has(i.id)).sort(sorters.new).map((i) => {
      const t = el('span', { className: 't' }, i.title);
      if (isNew(i.date)) t.append(el('span', { className: 'new', textContent: 'New' }));
      const a = el('a', { href: abs(i.type === 'writeups' ? i.href : (i.live || i.url)) }, t,
        el('span', { className: 'p', textContent: i.platform || KIND[i.type] || '' }), time(i.date));
      if (i.type !== 'writeups') { a.target = '_blank'; a.rel = 'noopener'; }
      return el('li', {}, a);
    }));
  }

  function renderResults() {
    const box = $('#results');
    box.replaceChildren();
    const filtering = !!(state.q || state.tags.length);
    const matched = items.filter(matchItem);
    const byGroup = Object.fromEntries(groups.map((g) => [g.id, matched.filter((i) => groupOf(i) === g.id)]));
    const sm = (filtering ? series.filter(matchSeries) : series).slice().sort(serSort[state.sort]);
    const wantType = (id) => state.type === 'all' || state.type === id;
    let shown = 0;

    if (wantType('writeups') && sm.length) {
      box.append(section('series', 'Categories', sm.length, sm.map(seriesCard)));
      shown += sm.length;
    }
    groups.forEach((g) => {
      if (!wantType(g.id)) return;
      let list = byGroup[g.id].slice().sort(sorters[state.sort]);
      let note;
      if (g.id === 'writeups' && !filtering && state.type === 'all') {   // overview: categories above, only uncategorised ones here
        list = list.filter((i) => !i.series && !latestIds.has(i.id));
        if (!list.length) return;
        note = `${list.length} uncategorised`;
      }
      if (!list.length) return;
      box.append(section(g.id, g.label, list.length, list.map((i) => CARD[i.type](i)), note));
      shown += list.length;
    });

    if (!shown) box.append(emptyState());
    renderSummary(matched, sm);
    observeSections();
  }

  function emptyState() {
    const e = el('div', { className: 'empty fade' });
    e.append(el('h2', { textContent: state.q ? `Nothing matched “${state.q}”` : 'Nothing matches those filters' }),
      el('p', { textContent: 'Try fewer words, check the spelling, or start from one of these popular tags.' }));
    const ul = el('ul', { className: 'chips' });
    popularTags(6, true).forEach(([k, o]) => {
      const b = el('button', { type: 'button', className: 'chip', textContent: o.label });
      b.addEventListener('click', () => { state.q = ''; $('#q').value = ''; state.tags = [k]; update(true); });
      ul.append(el('li', {}, b));
    });
    e.append(ul);
    const clear = el('button', { type: 'button', className: 'btn', textContent: 'Clear all filters' });
    clear.addEventListener('click', clearAll);
    e.append(clear, el('p', { className: 'note', textContent: 'Tip: press Ctrl/⌘ K to jump straight to any title.' }));
    return e;
  }

  function renderSummary(matched, sm) {
    const s = $('#status');
    s.replaceChildren();
    const filtering = state.q || state.tags.length;
    const total = matched.length;
    s.append(el('span', {}, el('strong', { textContent: String(total) }), ` of ${items.length} items`));
    if (state.q) s.append(sumChip(`“${state.q}”`, () => { state.q = ''; $('#q').value = ''; update(true); }, 'Clear search'));
    state.tags.forEach((t) => s.append(sumChip(t, () => toggleTag(t, true), `Remove tag ${t}`)));
    if (filtering) {
      const b = el('button', { type: 'button', className: 'linkbtn', textContent: 'Clear filters' });
      b.addEventListener('click', clearAll);
      s.append(b);
    }
  }
  function sumChip(text, fn, label) {
    const b = el('button', { type: 'button', textContent: '×' });
    b.setAttribute('aria-label', label);
    b.addEventListener('click', fn);
    return el('span', { className: 'sum-chip' }, text, b);
  }

  /* ---------- tabs & tags ---------- */
  function renderTabs() {
    const tabs = $('#tabs');
    tabs.replaceChildren();
    const matched = items.filter(matchItem);
    const defs = [{ id: 'all', label: 'All', n: matched.length }, ...groups.map((g) => ({ id: g.id, label: g.label, n: matched.filter((i) => groupOf(i) === g.id).length }))];
    defs.forEach((d) => {
      const b = el('button', { type: 'button', className: 'tab', id: 'tab-' + d.id }, d.label, el('span', { className: 'n', textContent: String(d.n) }));
      b.setAttribute('role', 'tab');
      b.setAttribute('aria-selected', String(state.type === d.id));
      b.tabIndex = state.type === d.id ? 0 : -1;
      b.addEventListener('click', () => { state.type = d.id; update(true); });
      b.addEventListener('keydown', (e) => {
        const all = [...tabs.children], i = all.indexOf(b);
        const to = { ArrowRight: (i + 1) % all.length, ArrowLeft: (i - 1 + all.length) % all.length, Home: 0, End: all.length - 1 }[e.key];
        if (to !== undefined) { e.preventDefault(); all[to].focus(); all[to].click(); $('#tab-' + defs[to].id)?.focus(); }
      });
      tabs.append(b);
    });
    $('#results').setAttribute('aria-labelledby', 'tab-' + state.type);
  }

  function tagPool() {
    const counts = new Map();
    items.filter((i) => state.type === 'all' || groupOf(i) === state.type).forEach((i) => i.tags.forEach((t) => {
      const k = norm(t), o = counts.get(k) || { label: t, n: 0 };
      o.n++; counts.set(k, o);
    }));
    return counts;
  }
  function popularTags(n, ignoreSelected) {
    const counts = tagPool();
    return [...counts.entries()].filter(([k]) => ignoreSelected || !state.tags.includes(k)).sort((a, b) => b[1].n - a[1].n || a[1].label.localeCompare(b[1].label)).slice(0, n);
  }
  function toggleTag(k, push) {
    state.tags = state.tags.includes(k) ? state.tags.filter((t) => t !== k) : [...state.tags, k];
    update(push);
  }
  function fchip(k, o) {
    const b = el('button', { type: 'button', className: 'fchip' }, o.label, el('span', { className: 'n', textContent: String(o.n) }));
    b.setAttribute('aria-pressed', String(state.tags.includes(k)));
    b.addEventListener('click', () => toggleTag(k, true));
    return b;
  }
  function renderTags() {
    const row = $('#tagrow');
    row.querySelectorAll('.top-tags').forEach((n) => n.remove());
    const counts = tagPool();
    const picked = state.tags.map((k) => [k, counts.get(k) || { label: k, n: 0 }]);
    const top = popularTags(TOP_TAGS, false);
    const holder = el('span', { className: 'top-tags' });
    [...picked, ...top].forEach(([k, o]) => holder.append(fchip(k, o)));
    row.insertBefore(holder, $('#more-tags'));
    $('#more-tags').textContent = `All tags (${counts.size})`;
  }

  /* tag popover */
  let pop, popBtn;
  function closePop(focusBtn) {
    if (!pop) return;
    pop.remove(); pop = null;
    popBtn.setAttribute('aria-expanded', 'false');
    document.removeEventListener('mousedown', outside);
    if (focusBtn) popBtn.focus();
  }
  function outside(e) { if (pop && !pop.contains(e.target) && e.target !== popBtn) closePop(false); }
  function openPop() {
    if (pop) { closePop(true); return; }
    popBtn = $('#more-tags');
    const input = el('input', { type: 'search', placeholder: 'Filter tags…', autocomplete: 'off', spellcheck: false });
    input.setAttribute('aria-label', 'Filter tags');
    const ul = el('ul');
    const fill = () => {
      ul.replaceChildren();
      const q = norm(input.value.trim());
      const list = [...tagPool().entries()].filter(([k]) => k.includes(q)).sort((a, b) => b[1].n - a[1].n || a[1].label.localeCompare(b[1].label));
      list.forEach(([k, o]) => ul.append(el('li', {}, fchip(k, o))));
      if (!list.length) ul.append(el('li', { className: 'none', textContent: 'No tags match.' }));
    };
    input.addEventListener('input', fill);
    pop = el('div', { className: 'pop' }, input, ul);
    pop.setAttribute('role', 'dialog');
    pop.setAttribute('aria-label', 'All tags');
    pop.addEventListener('keydown', (e) => { if (e.key === 'Escape') { e.stopPropagation(); closePop(true); } });
    fill();
    $('#tagrow').append(pop);
    popBtn.setAttribute('aria-expanded', 'true');
    document.addEventListener('mousedown', outside);
    input.focus();
    // selecting a tag re-renders the page; keep the popover content in sync
    pop._fill = fill;
  }

  /* ---------- sticky offsets + scroll-spy + header nav ---------- */
  let io;
  function observeSections() {
    const nav = $('#nav');
    const secs = [...document.querySelectorAll('#results > .section')];
    nav.replaceChildren(...secs.map((s) => {
      const a = el('a', { href: '#' + s.id, textContent: $('h2', s).childNodes[1].textContent });
      a.addEventListener('click', (e) => { e.preventDefault(); document.getElementById(s.id).scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' }); });
      return a;
    }));
    if (io) io.disconnect();
    if (!('IntersectionObserver' in window)) return;
    const links = new Map(secs.map((s, i) => [s.id, nav.children[i]]));
    io = new IntersectionObserver((entries) => {
      entries.forEach((e) => { if (e.isIntersecting) { links.forEach((a) => a.removeAttribute('aria-current')); links.get(e.target.id)?.setAttribute('aria-current', 'true'); } });
    }, { rootMargin: `-${(parseInt(getComputedStyle(document.documentElement).getPropertyValue('--sticky')) || 120) + 20}px 0px -60% 0px` });
    secs.forEach((s) => io.observe(s));
  }
  function trackSticky() {
    const root = document.documentElement.style, bar = $('#bar-wrap'), hdr = $('.top');
    const set = () => root.setProperty('--sticky', `${hdr.offsetHeight + bar.offsetHeight}px`);
    new ResizeObserver(set).observe(bar);
    set();
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(([e]) => bar.classList.toggle('stuck', !e.isIntersecting && e.boundingClientRect.top < 0),
        { rootMargin: `-${hdr.offsetHeight}px 0px 0px 0px` }).observe($('#bar-sentinel'));
    }
  }

  /* ---------- orchestration ---------- */
  function update(push) {
    writeURL(push);
    $('#sort').value = state.sort;
    $('.search .clear').hidden = !state.q;
    renderTabs();
    renderTags();
    renderLatest();
    renderResults();
    if (pop && pop._fill) pop._fill();
  }
  function clearAll() {
    state.q = ''; state.tags = []; state.type = 'all'; $('#q').value = '';
    update(true);
    $('#q').focus();
  }

  /* The hero's default content is in index.html so nothing jumps; only touch it if profile.json differs. */
  function hero() {
    const p = D.profile, st = D.stats;
    const setText = (id, v) => { const n = $(id); if (n.textContent !== v) n.textContent = v; };
    setText('#tagline', p.tagline || '');
    setText('#bio', p.bio || '');
    const links = (p.links || []).filter((l) => l.url);
    const ul = $('#profile');
    const now = [...ul.querySelectorAll('a')].map((a) => a.getAttribute('href') + '|' + a.textContent).join();
    if (now !== links.map((l) => l.url + '|' + l.label).join()) {
      ul.replaceChildren(...links.map((l) => { const a = el('a', { href: l.url, textContent: l.label }); a.rel = 'noopener me'; return el('li', {}, a); }));
    }
    const vals = $('#term-body').querySelectorAll('.k + .v');
    [st.writeups, st.platforms, st.series, st.updated ? fmt(st.updated) : '–'].forEach((v, i) => { if (vals[i]) vals[i].textContent = String(v); });
    const who = $('#term-body .v'); const txt = `${p.handle || 'l0wk3y'} · ${p.tagline || ''}`;
    if (who && who.textContent !== txt) who.textContent = txt;
  }

  async function init() {
    try {
      const r = await fetch(ROOT + 'data/index.json', { cache: 'no-cache' });
      if (!r.ok) throw new Error(r.status);
      D = await r.json();
    } catch (e) {
      $('#results').append(el('p', { className: 'note', textContent: '// index missing. Run `python3 scripts/build_index.py`, then serve the site/ folder.' }));
      return;
    }
    items = D.items; series = D.series;
    byId = Object.fromEntries(items.map((i) => [i.id, i]));
        series.forEach((s) => { s._tags = [...new Set(s.items.flatMap((id) => byId[id].tags))]; });
    groups = GROUPS.filter((g) => items.some((i) => g.types.includes(i.type)));     // hide empty sections
    latestIds = new Set(items.filter((i) => i.type !== 'curated').sort(sorters.new).slice(0, 5).map((i) => i.id));
    hero();
    trackSticky();
    readURL();
    $('#q').value = state.q;
    update(false);

    let t;
    $('#q').addEventListener('input', (e) => {
      clearTimeout(t);
      t = setTimeout(() => { state.q = e.target.value.trim(); update(false); }, 90);
    });
    $('#q').addEventListener('keydown', (e) => { if (e.key === 'Escape' && $('#q').value) { e.stopPropagation(); state.q = ''; $('#q').value = ''; update(false); } });
    $('.search .clear').addEventListener('click', () => { state.q = ''; $('#q').value = ''; update(true); $('#q').focus(); });
    $('#sort').addEventListener('change', (e) => { state.sort = e.target.value; update(true); });
    $('#more-tags').addEventListener('click', openPop);
    addEventListener('popstate', () => { readURL(); $('#q').value = state.q; update(false); });
  }
  init();
})();
