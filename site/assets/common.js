/* Shared by every page: theme toggle, back-to-top button and the Ctrl/Cmd+K command palette. */
(() => {
  'use strict';
  const ROOT = document.documentElement.dataset.root || '';
  const $ = (s, r = document) => r.querySelector(s);
  const el = (tag, props = {}, ...kids) => { const n = Object.assign(document.createElement(tag), props); kids.forEach((k) => n.append(k)); return n; };

  /* ---------- theme ---------- */
  const themeBtn = $('#theme');
  if (themeBtn) {
    themeBtn.addEventListener('click', () => {
      const root = document.documentElement;
      const next = getComputedStyle(root).colorScheme.startsWith('light') ? 'dark' : 'light';
      root.dataset.theme = next;
      const meta = $('meta[name="theme-color"]');
      if (meta) meta.content = next === 'light' ? '#f6f8fa' : '#0b0f14';
      try { localStorage.setItem('hwl-theme', next); } catch (e) { /* storage blocked: fine */ }
    });
  }

  if (document.documentElement.classList.contains('embed')) return;     // iframe on the desktop: no palette/back-to-top

  /* ---------- back to top ---------- */
  const top = el('button', { type: 'button', className: 'totop', textContent: '↑' });
  top.setAttribute('aria-label', 'Back to top');
  top.addEventListener('click', () => window.scrollTo({ top: 0, behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' }));
  document.body.append(top);
  let ticking = false;
  addEventListener('scroll', () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => { top.classList.toggle('show', scrollY > 700); ticking = false; });
  }, { passive: true });

  /* ---------- command palette ---------- */
  let data = null, overlay, input, list, active = 0, shown = [], lastFocus;
  const KIND_RANK = { Category: 0, 'Write-up': 1, Tool: 2, 'Cheat sheet': 2, Project: 2, Link: 3, Tag: 4 };

  async function load() {
    if (data) return data;
    try { data = await (await fetch(ROOT + 'data/search.json')).json(); } catch (e) { data = []; }
    return data;
  }
  const hay = (r) => r._h || (r._h = (r.t + ' ' + r.k + ' ' + (r.s || '') + ' ' + (r.g || '')).toLowerCase());
  function search(q) {
    const terms = q.toLowerCase().split(/\s+/).filter(Boolean);
    if (!terms.length) return data.filter((r) => r.k === 'Category' || r.k === 'Write-up').slice(0, 12);
    const out = [];
    for (const r of data) {
      const h = hay(r), t = r.t.toLowerCase();
      if (!terms.every((x) => h.includes(x))) continue;
      let score = 0;
      for (const x of terms) score += (t.startsWith(x) ? 3 : t.includes(x) ? 2 : 1);
      out.push([score - (KIND_RANK[r.k] ?? 5) * 0.1, r]);
    }
    return out.sort((a, b) => b[0] - a[0]).slice(0, 40).map((x) => x[1]);
  }
  const href = (r) => (r.x ? r.u : ROOT + r.u);

  function render() {
    list.replaceChildren();
    if (!shown.length) { list.append(el('li', { className: 'pal-empty', textContent: 'No matches. Try a tag, a platform or a lab name.' })); return; }
    shown.forEach((r, i) => {
      const a = el('a', { href: href(r), id: 'pal-' + i }, el('span', { className: 'kind', textContent: r.k }), el('span', { className: 't', textContent: r.t }), el('span', { className: 's', textContent: r.s || '' }));
      a.setAttribute('role', 'option');
      a.setAttribute('aria-selected', String(i === active));
      if (r.x) { a.target = '_blank'; a.rel = 'noopener'; }
      a.tabIndex = -1;
      a.addEventListener('mousemove', () => { if (active !== i) { active = i; mark(); } });
      list.append(el('li', {}, a));
    });
    input.setAttribute('aria-activedescendant', 'pal-' + active);
  }
  function mark() {
    list.querySelectorAll('a').forEach((a, i) => a.setAttribute('aria-selected', String(i === active)));
    const a = list.querySelectorAll('a')[active];
    if (a) { a.scrollIntoView({ block: 'nearest' }); input.setAttribute('aria-activedescendant', a.id); }
  }
  function close() {
    if (!overlay) return;
    overlay.remove(); overlay = null;
    document.body.style.overflow = '';
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }
  async function open() {
    if (overlay) return;
    lastFocus = document.activeElement;
    input = el('input', { type: 'text', placeholder: 'Jump to a write-up, series, tool or tag…', autocomplete: 'off', spellcheck: false });
    input.setAttribute('role', 'combobox');
    input.setAttribute('aria-expanded', 'true');
    input.setAttribute('aria-controls', 'pal-list');
    input.setAttribute('aria-label', 'Search the site');
    list = el('ul', { id: 'pal-list', className: 'pal-list' });
    list.setAttribute('role', 'listbox');
    const box = el('div', { className: 'pal-box' },
      el('div', { className: 'pal-in' }, el('span', { className: 'mono', textContent: '>', ariaHidden: 'true' }), input),
      list,
      el('div', { className: 'pal-foot' }, el('span', { textContent: '↑↓ navigate' }), el('span', { textContent: '↵ open' }), el('span', { textContent: 'esc close' })));
    box.setAttribute('role', 'dialog');
    box.setAttribute('aria-modal', 'true');
    box.setAttribute('aria-label', 'Command palette');
    overlay = el('div', { className: 'pal-ov' }, box);
    overlay.addEventListener('mousedown', (e) => { if (e.target === overlay) close(); });
    document.body.append(overlay);
    document.body.style.overflow = 'hidden';
    input.focus();
    await load();
    shown = search(''); active = 0; render();
    input.addEventListener('input', () => { shown = search(input.value); active = 0; render(); });
    input.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowDown') { e.preventDefault(); active = Math.min(active + 1, shown.length - 1); mark(); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); active = Math.max(active - 1, 0); mark(); }
      else if (e.key === 'Home') { e.preventDefault(); active = 0; mark(); }
      else if (e.key === 'End') { e.preventDefault(); active = shown.length - 1; mark(); }
      else if (e.key === 'Tab') { e.preventDefault(); }                      // keep focus inside the dialog
      else if (e.key === 'Enter') {
        const r = shown[active];
        if (!r) return;
        e.preventDefault();
        if (r.x) window.open(r.u, '_blank', 'noopener'); else location.href = href(r);
        close();
      }
    });
  }

  document.addEventListener('keydown', (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); overlay ? close() : open(); return; }
    if (e.key === 'Escape' && overlay) { e.preventDefault(); close(); return; }
    if (e.key === '/' && !e.metaKey && !e.ctrlKey && !e.altKey && !/^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement.tagName)) {
      e.preventDefault();
      const q = $('#q');
      q ? q.focus() : open();
    }
  });
  const btn = $('#open-palette');
  if (btn) {
    btn.addEventListener('click', open);
    if (/Mac|iPhone|iPad/.test(navigator.platform)) { const k = $('kbd', btn); if (k) k.textContent = '⌘K'; }
  }
  window.hwlPalette = { open, close };
})();
