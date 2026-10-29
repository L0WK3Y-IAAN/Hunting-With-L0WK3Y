(() => {
  'use strict';
  const PAGE = 12;                 // cards shown per section before "show all"
  const TAGS_SHOWN = 14;           // tag chips shown before "more"
  const $ = (s) => document.querySelector(s);
  const el = (tag, props = {}, ...kids) => {
    const n = Object.assign(document.createElement(tag), props);
    kids.forEach((k) => n.append(k));
    return n;
  };

  const state = { q: '', type: 'all', tags: new Set(), sort: 'new', expanded: new Set(), allTags: false };
  let DATA = null;

  /* ---------- URL <-> state (shareable filters) ---------- */
  const readHash = () => {
    const p = new URLSearchParams(location.hash.slice(1));
    state.q = p.get('q') || '';
    state.type = p.get('type') || 'all';
    state.sort = p.get('sort') || 'new';
    state.tags = new Set((p.get('tags') || '').split(',').filter(Boolean));
  };
  const writeHash = () => {
    const p = new URLSearchParams();
    if (state.q) p.set('q', state.q);
    if (state.type !== 'all') p.set('type', state.type);
    if (state.sort !== 'new') p.set('sort', state.sort);
    if (state.tags.size) p.set('tags', [...state.tags].join(','));
    const h = p.toString();
    history.replaceState(null, '', h ? `#${h}` : location.pathname + location.search);
  };

  /* ---------- helpers ---------- */
  const fmtDate = (iso) => new Date(iso + 'T00:00:00Z').toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric', timeZone: 'UTC' });
  const norm = (s) => s.toLowerCase();
  const haystack = (it) => it._h || (it._h = norm([it.title, it.name, it.description, it.platform, it.category, it.tags.join(' ')].filter(Boolean).join(' ')));
  const matches = (it) => {
    const terms = norm(state.q).split(/\s+/).filter(Boolean);
    if (!terms.every((t) => haystack(it).includes(t))) return false;
    for (const t of state.tags) if (!it.tags.some((x) => norm(x) === t)) return false;
    return true;
  };
  const sorters = {
    new: (a, b) => b.date.localeCompare(a.date) || a.title.localeCompare(b.title),
    old: (a, b) => a.date.localeCompare(b.date) || a.title.localeCompare(b.title),
    az: (a, b) => a.title.localeCompare(b.title, undefined, { sensitivity: 'base' }),
  };
  const highlight = (text) => {
    const terms = norm(state.q).split(/\s+/).filter((t) => t.length > 1);
    if (!terms.length) return [text];
    const re = new RegExp(`(${terms.map((t) => t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|')})`, 'ig');
    return text.split(re).map((part, i) => (i % 2 ? el('mark', { textContent: part }) : part));
  };

  /* ---------- rendering ---------- */
  function card(it, compact = false) {
    const typeLabel = DATA.types.find((t) => t.id === it.type).label;
    const primary = it.live || it.url;
    const li = el('li');
    const c = el('article', { className: 'card' + (compact ? ' compact' : '') });

    const meta = el('div', { className: 'meta' },
      el('span', { className: 'badge' + (it.external ? ' ext' : ''), textContent: it.external ? 'external' : typeLabel.replace(/s$/, '') }),
      el('time', { dateTime: it.date, textContent: fmtDate(it.date) }));
    if (it.minutes) meta.append(el('span', { textContent: `${it.minutes} min read` }));
    if (it.platform) meta.append(el('span', { textContent: it.platform }));

    const a = el('a', { href: primary }, ...highlight(it.title));
    if (it.external || it.live) { a.target = '_blank'; a.rel = 'noopener'; }
    c.append(meta, el('h3', {}, a));

    if (it.description) c.append(el('p', {}, ...highlight(it.description)));

    if (!compact) {
      const acts = el('div', { className: 'acts' });
      if (it.live) acts.append(el('a', { href: it.url, target: '_blank', rel: 'noopener', textContent: 'view source ↗' }));
      else if (it.external && it.source) acts.append(el('a', { href: it.source, target: '_blank', rel: 'noopener', textContent: 'listed in repo ↗' }));
      if (acts.children.length) c.append(acts);

      if (it.tags.length) {
        const tags = el('div', { className: 'tags' });
        it.tags.slice(0, 6).forEach((t) => {
          const b = el('button', { type: 'button', className: 'tag', textContent: t });
          b.setAttribute('aria-label', `Filter by tag ${t}`);
          b.addEventListener('click', () => { state.tags.add(norm(t)); update(); });
          tags.append(b);
        });
        c.append(tags);
      }
    }
    li.append(c);
    return li;
  }

  function renderTypes() {
    const box = $('#types');
    box.replaceChildren();
    const visible = DATA.items.filter(matches);   // counts reflect the other filters
    const mk = (id, label, n) => {
      const b = el('button', { type: 'button', className: 'chip' }, label, el('span', { className: 'n', textContent: n }));
      b.setAttribute('aria-pressed', String(state.type === id));
      b.addEventListener('click', () => { state.type = id; update(); });
      return b;
    };
    box.append(mk('all', 'All', visible.length));
    DATA.types.forEach((t) => box.append(mk(t.id, t.label, visible.filter((i) => i.type === t.id).length)));
  }

  function renderTags() {
    const box = $('#tags');
    box.replaceChildren();
    const pool = DATA.items.filter((i) => state.type === 'all' || i.type === state.type);
    const counts = new Map();
    pool.forEach((i) => i.tags.forEach((t) => { const k = norm(t); const o = counts.get(k) || { label: t, n: 0 }; o.n++; counts.set(k, o); }));
    state.tags.forEach((k) => { if (!counts.has(k)) counts.set(k, { label: k, n: 0 }); });
    let list = [...counts.entries()].sort((a, b) => (state.tags.has(b[0]) - state.tags.has(a[0])) || b[1].n - a[1].n || a[1].label.localeCompare(b[1].label));
    const total = list.length;
    if (!state.allTags) list = list.filter(([k], i) => i < TAGS_SHOWN || state.tags.has(k));
    list.forEach(([k, o]) => {
      const b = el('button', { type: 'button', className: 'chip' }, `#${o.label}`, el('span', { className: 'n', textContent: o.n }));
      b.setAttribute('aria-pressed', String(state.tags.has(k)));
      b.addEventListener('click', () => { state.tags.has(k) ? state.tags.delete(k) : state.tags.add(k); update(); });
      box.append(b);
    });
    if (total > TAGS_SHOWN) {
      const b = el('button', { type: 'button', className: 'chip more-tags', textContent: state.allTags ? 'fewer tags' : `+${total - TAGS_SHOWN} more` });
      b.addEventListener('click', () => { state.allTags = !state.allTags; renderTags(); });
      box.append(b);
    }
  }

  function renderResults() {
    const box = $('#results');
    box.replaceChildren();
    const items = DATA.items.filter(matches).sort(sorters[state.sort]);
    const filtering = state.q || state.tags.size;

    DATA.types.forEach((t) => {
      if (state.type !== 'all' && state.type !== t.id) return;
      const list = items.filter((i) => i.type === t.id);
      if (!list.length && (filtering || t.count)) return;       // hide empty sections while filtering
      const open = state.expanded.has(t.id) || state.type !== 'all';
      const shown = open ? list : list.slice(0, PAGE);

      const sec = el('section', { className: 'section', id: t.id });
      sec.setAttribute('aria-labelledby', `${t.id}-h`);
      sec.append(el('h2', { id: `${t.id}-h` }, el('span', { className: 'mono', textContent: '>' }), t.label, el('small', { textContent: `${list.length}` })));
      if (!list.length) {
        sec.append(el('p', { className: 'empty', textContent: '// nothing here yet. Add a folder with a README and it will show up on the next push.' }));
      } else {
        const ul = el('ul', { className: 'grid' });
        shown.forEach((i) => ul.append(card(i)));
        sec.append(ul);
        if (list.length > shown.length) {
          const b = el('button', { type: 'button', className: 'btn showall', textContent: `Show all ${list.length} ${t.label.toLowerCase()}` });
          b.addEventListener('click', () => { state.expanded.add(t.id); renderResults(); });
          sec.append(b);
        }
      }
      box.append(sec);
    });

    if (!items.length && filtering) {
      box.append(el('p', { className: 'empty', textContent: '// no matches. Try fewer words or clear the filters.' }));
    }
    const status = $('#status');
    status.replaceChildren(`${items.length} of ${DATA.items.length} items`);
    if (filtering || state.type !== 'all') {
      const clear = el('button', { type: 'button', textContent: 'clear filters' });
      clear.addEventListener('click', () => { state.q = ''; state.type = 'all'; state.tags.clear(); $('#q').value = ''; update(); });
      status.append(clear);
    }
  }

  function renderRecent() {
    const recent = [...DATA.items].sort(sorters.new).slice(0, 6);
    const wrap = $('#recent-wrap');
    wrap.hidden = !recent.length;
    const ul = $('#recent');
    ul.replaceChildren(...recent.map((i) => card(i, true)));
  }

  function update() {
    writeHash();
    $('#sort').value = state.sort;
    renderTypes();
    renderTags();
    renderResults();
  }

  /* ---------- boot ---------- */
  async function init() {
    try {
      const res = await fetch('data/index.json', { cache: 'no-cache' });
      if (!res.ok) throw new Error(res.status);
      DATA = await res.json();
    } catch (e) {
      $('#stats').textContent = 'could not load data/index.json';
      $('#results').append(el('p', { className: 'empty', textContent: '// index missing. Run `python3 scripts/build_index.py` and serve the site/ folder.' }));
      return;
    }
    const parts = DATA.types.filter((t) => t.count).map((t) => `${t.count} ${t.count === 1 ? t.label.toLowerCase().replace(/s$/, '') : t.label.toLowerCase()}`);
    $('#stats').textContent = `${DATA.items.length} items · ${parts.join(' · ')}`;
    const gen = new Date(DATA.generated);
    $('#gen').textContent = `updated ${gen.toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' })}`;

    readHash();
    $('#q').value = state.q;
    renderRecent();
    update();

    let t;
    $('#q').addEventListener('input', (e) => {
      clearTimeout(t);
      t = setTimeout(() => { state.q = e.target.value.trim(); update(); }, 80);
    });
    $('#sort').addEventListener('change', (e) => { state.sort = e.target.value; update(); });
    window.addEventListener('hashchange', () => { readHash(); $('#q').value = state.q; update(); });
    document.addEventListener('keydown', (e) => {
      if (e.key === '/' && !/^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement.tagName)) { e.preventDefault(); $('#q').focus(); }
      if (e.key === 'Escape' && document.activeElement === $('#q')) { $('#q').value = ''; state.q = ''; update(); }
    });
  }

  $('#theme').addEventListener('click', () => {
    const root = document.documentElement;
    const light = getComputedStyle(root).colorScheme.startsWith('light');
    const next = light ? 'dark' : 'light';
    root.dataset.theme = next;
    try { localStorage.setItem('hwl-theme', next); } catch (e) { /* storage blocked: fine */ }
  });

  init();
})();
