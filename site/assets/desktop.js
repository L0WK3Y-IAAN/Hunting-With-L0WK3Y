/* Desktop view: categories are folders, write-ups open in draggable windows (iframes of the static article pages).
   Everything is built from data/index.json, so new content appears here with no edits. */
(() => {
  'use strict';
  const icon = window.ICONS95;
  const $ = (s, r = document) => r.querySelector(s);
  const el = (tag, props = {}, ...kids) => { const n = Object.assign(document.createElement(tag), props); kids.forEach((k) => k != null && n.append(k)); return n; };
  const pix = (name, size = 16) => el('img', { src: icon(name, size), alt: '', draggable: false, width: size, height: size });
  const fmt = (iso) => (iso ? new Date(iso + 'T00:00:00Z').toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric', timeZone: 'UTC' }) : '');
  const desktop = $('#desktop'), iconsBox = $('#icons'), tasksBox = $('#tasks');
  const coarse = matchMedia('(pointer: coarse)').matches;
  let D, items, series, byHref = {};

  /* ============================================================ window manager */
  const wins = new Map();
  let zTop = 100, active = null, cascade = 0;
  const area = () => ({ w: desktop.clientWidth, h: desktop.clientHeight });

  function focusWin(w) {
    if (!w || !wins.has(w.id)) return;
    if (w.el.classList.contains('min')) w.el.classList.remove('min');
    w.el.style.zIndex = String(++zTop);
    active = w;
    wins.forEach((o) => { o.el.classList.toggle('active', o === w); if (o.task) o.task.classList.toggle('on', o === w); });
    if (w.onFocus) w.onFocus();
  }
  function topVisible() {
    return [...wins.values()].filter((w) => !w.el.classList.contains('min')).sort((a, b) => +b.el.style.zIndex - +a.el.style.zIndex)[0];
  }
  function closeWin(w) {
    if (!wins.has(w.id)) return;
    wins.delete(w.id);
    w.el.remove();
    if (w.task) w.task.remove();
    if (w.onClose) w.onClose();
    if (active === w) { active = null; const t = topVisible(); if (t) { focusWin(t); t.el.focus({ preventScroll: true }); } }
  }
  function minWin(w) {
    w.el.classList.add('min');
    if (w.task) w.task.classList.remove('on');
    if (active === w) { active = null; const t = topVisible(); if (t) focusWin(t); }
  }
  function toggleMax(w) {
    if (w.fixed) return;
    w.el.classList.toggle('max');
    w.maxBtn.setAttribute('aria-label', w.el.classList.contains('max') ? 'Restore' : 'Maximize');
  }

  const X_ICON = '<svg viewBox="0 0 10 10"><path d="M1 1l8 8M9 1l-8 8"/></svg>';
  const MIN_ICON = '<svg viewBox="0 0 10 10"><path d="M1 8h6"/></svg>';
  const MAX_ICON = '<svg viewBox="0 0 10 10"><rect x="1" y="1" width="8" height="8"/></svg>';

  function openWindow(o) {
    const existing = o.id && wins.get(o.id);
    if (existing) { focusWin(existing); existing.el.focus({ preventScroll: true }); return existing; }
    const a = area();
    const small = a.w < 700;
    const w = { id: o.id || 'w' + Math.random().toString(36).slice(2), fixed: !!o.fixed, onClose: o.onClose, onFocus: o.onFocus };
    const width = Math.min(o.w || 640, a.w - 16), height = Math.min(o.h || 420, a.h - 16);
    const off = (cascade++ % 8) * 28;
    const x = o.x != null ? o.x : Math.max(8, Math.min(a.w - width - 8, (o.center ? (a.w - width) / 2 : (a.w > 900 ? 230 : 40) + off)));
    const y = o.y != null ? o.y : Math.max(8, Math.min(a.h - height - 8, (o.center ? (a.h - height) / 2.4 : 30 + off)));

    const title = el('span', { className: 't', textContent: o.title });
    const btns = el('div', { className: 'btns' });
    const mk = (cls, label, svg, fn) => { const b = el('button', { type: 'button', className: 'tbtn ' + cls, innerHTML: svg }); b.setAttribute('aria-label', label); b.addEventListener('click', (e) => { e.stopPropagation(); fn(); }); return b; };
    if (!o.dialog) {
      btns.append(mk('min', 'Minimize', MIN_ICON, () => minWin(w)));
      w.maxBtn = mk('max', 'Maximize', MAX_ICON, () => toggleMax(w));
      if (!w.fixed) btns.append(w.maxBtn);
    }
    btns.append(mk('close', 'Close', X_ICON, () => closeWin(w)));
    const tbar = el('div', { className: 'tbar' }, pix(o.icon || 'doc'), title, btns);
    const body = el('div', { className: 'wbody', style: 'flex:1;min-height:0;display:flex;flex-direction:column' });
    const wel = el('section', { className: 'win' + (o.dialog ? ' dialog' : ''), tabIndex: -1 }, tbar, body);
    wel.setAttribute('role', 'dialog');
    wel.setAttribute('aria-label', o.title);
    Object.assign(wel.style, { left: x + 'px', top: y + 'px', width: width + 'px', height: o.dialog ? 'auto' : height + 'px' });
    if (!o.dialog && !w.fixed) {
      const grip = el('div', { className: 'grip' });
      grip.addEventListener('pointerdown', (e) => {
        e.preventDefault(); focusWin(w); grip.setPointerCapture(e.pointerId); document.body.classList.add('dragging');
        const sw = wel.offsetWidth, sh = wel.offsetHeight, sx = e.clientX, sy = e.clientY;
        const move = (ev) => { wel.style.width = Math.max(280, sw + ev.clientX - sx) + 'px'; wel.style.height = Math.max(160, sh + ev.clientY - sy) + 'px'; };
        const up = () => { grip.removeEventListener('pointermove', move); grip.removeEventListener('pointerup', up); document.body.classList.remove('dragging'); };
        grip.addEventListener('pointermove', move); grip.addEventListener('pointerup', up);
      });
      wel.append(grip);
    }
    // drag by the title bar
    tbar.addEventListener('pointerdown', (e) => {
      if (e.target.closest('.btns') || e.button !== 0) return;
      focusWin(w);
      if (wel.classList.contains('max')) return;
      const ox = wel.offsetLeft, oy = wel.offsetTop, sx = e.clientX, sy = e.clientY;
      tbar.setPointerCapture(e.pointerId); document.body.classList.add('dragging');
      const move = (ev) => {
        const A = area();
        wel.style.left = Math.max(-wel.offsetWidth + 90, Math.min(A.w - 60, ox + ev.clientX - sx)) + 'px';
        wel.style.top = Math.max(0, Math.min(A.h - 30, oy + ev.clientY - sy)) + 'px';
      };
      const up = () => { tbar.removeEventListener('pointermove', move); tbar.removeEventListener('pointerup', up); document.body.classList.remove('dragging'); };
      tbar.addEventListener('pointermove', move); tbar.addEventListener('pointerup', up);
    });
    tbar.addEventListener('dblclick', (e) => { if (!e.target.closest('.btns') && !o.dialog) toggleMax(w); });
    wel.addEventListener('pointerdown', () => { if (active !== w) focusWin(w); }, true);

    w.el = wel; w.body = body; w.title = title;
    w.setTitle = (t) => { title.textContent = t; wel.setAttribute('aria-label', t); if (w.task) w.task.lastChild.textContent = t; };
    w.close = () => closeWin(w);
    wins.set(w.id, w);
    desktop.append(wel);
    if (!o.dialog) {
      w.task = el('button', { type: 'button', className: 'task' }, pix(o.icon || 'doc'), el('span', { textContent: o.title }));
      w.task.addEventListener('click', () => {
        if (active === w && !wel.classList.contains('min')) minWin(w); else { focusWin(w); wel.focus({ preventScroll: true }); }
      });
      tasksBox.append(w.task);
    }
    if (small && !o.dialog && !w.fixed) wel.classList.add('max');
    focusWin(w);
    return w;
  }

  /* ---------- menu bar with drop-downs ---------- */
  let openPop = null;
  function closePop() { if (openPop) { openPop.btn.setAttribute('aria-expanded', 'false'); openPop.el.remove(); openPop = null; } }
  function menubar(defs) {
    const bar = el('div', { className: 'menubar' });
    defs.forEach((m) => {
      const b = el('button', { type: 'button' });
      b.innerHTML = m.label.replace(/^(.)/, '<u>$1</u>');
      b.setAttribute('aria-haspopup', 'menu'); b.setAttribute('aria-expanded', 'false');
      const show = () => {
        if (openPop && openPop.btn === b) { closePop(); return; }
        closePop();
        const pop = el('div', { className: 'pop' }); pop.setAttribute('role', 'menu');
        m.items().forEach((it) => {
          if (it === '-') { pop.append(el('hr')); return; }
          const i = el('button', { type: 'button', textContent: it.label, disabled: !!it.disabled, className: it.on ? 'on' : '' });
          i.setAttribute('role', 'menuitem');
          i.addEventListener('click', () => { closePop(); it.action && it.action(); });
          pop.append(i);
        });
        pop.style.left = b.offsetLeft + 'px'; pop.style.top = (b.offsetTop + b.offsetHeight) + 'px';
        bar.append(pop); b.setAttribute('aria-expanded', 'true'); openPop = { el: pop, btn: b };
        pop.querySelector('button:not(:disabled)')?.focus();
      };
      b.addEventListener('click', (e) => { e.stopPropagation(); show(); });
      b.addEventListener('mouseenter', () => { if (openPop && openPop.btn !== b) show(); });
      bar.append(b);
    });
    return bar;
  }
  document.addEventListener('pointerdown', (e) => { if (openPop && !e.target.closest('.pop') && !e.target.closest('.menubar')) closePop(); });

  /* ---------- dialogs ---------- */
  function dialog({ id, title, ico = 'info', body, buttons = [{ label: 'OK', def: true }], w = 400 }) {
    const win = openWindow({ id, title, icon: ico, w, h: 0, dialog: true, center: true });
    const msg = el('div', { className: 'msg' });
    (Array.isArray(body) ? body : [body]).forEach((b) => msg.append(typeof b === 'string' ? el('p', { textContent: b }) : b));
    const row = el('div', { className: 'dlg-btns' });
    buttons.forEach((b) => {
      const btn = el('button', { type: 'button', className: 'btn' + (b.def ? ' def' : ''), textContent: b.label });
      btn.addEventListener('click', () => { if (!b.action || b.action(win) !== false) win.close(); });
      row.append(btn);
    });
    win.body.append(el('div', { className: 'dlg' }, pix(ico, 32), msg), row);
    win.body.addEventListener('keydown', (e) => { if (e.key === 'Enter' && e.target.tagName !== 'BUTTON') { e.preventDefault(); row.querySelector('.def')?.click(); } });
    (win.body.querySelector('input') || row.querySelector('.def') || row.querySelector('button'))?.focus();
    return win;
  }
  const alertBox = (title, text, ico = 'warn') => dialog({ title, ico, body: text });

  /* ============================================================ content model */
  function fileNode(i) {
    if (i.type === 'writeups') return { kind: 'doc', name: i.title, icon: 'doc', item: i, c2: i.platform, c3: fmt(i.date), k3: i.date, c4: `${i.minutes} min`, k4: i.minutes };
    if (i.type === 'curated') return { kind: 'link', name: i.title, icon: 'globe', item: i, c2: i.display || '', c3: (i.tags[0] || 'Link').replace(/s$/, ''), k3: i.tags[0] || '', c4: '', k4: 0 };
    const code = i.tags.some((t) => /python|javascript|shell|ruby|go|java/i.test(t));
    return { kind: i.live ? 'cheat' : 'tool', name: i.title, icon: i.live ? 'book' : (code ? 'code' : 'exe'), item: i, c2: i.type === 'cheatsheets' ? 'Cheat sheet' : 'Tool', c3: fmt(i.date), k3: i.date, c4: i.tags[0] || '', k4: 0 };
  }
  function folder(name, id, children, extra = {}) {
    return { kind: 'folder', name, id, icon: 'folder', children, c2: 'File Folder', c3: extra.date ? fmt(extra.date) : '', k3: extra.date || '', c4: `${children.length} item${children.length === 1 ? '' : 's'}`, k4: children.length, ...extra };
  }
  function buildModel() {
    const byId = Object.fromEntries(items.map((i) => [i.id, i]));
    const cats = series.map((s) => {
      const entries = s.items.map((id) => byId[id]);
      const kids = s.platforms.length > 1
        ? s.platforms.map((p) => { const es = entries.filter((e) => e.platform === p); return folder(p, `${s.slug}/${p}`, es.map(fileNode), { date: es.map((e) => e.date).sort().pop() }); })
        : entries.map(fileNode);
      return folder(s.name, s.slug, kids, { date: s.latest, href: s.href });
    }).sort((a, b) => b.children.length - a.children.length || a.name.localeCompare(b.name));
    const pick = (types) => items.filter((i) => types.includes(i.type)).sort((a, b) => b.date.localeCompare(a.date)).map(fileNode);
    const toolbox = folder('Toolbox', 'toolbox', pick(['tools', 'cheatsheets']), { icon: 'tools' });
    const projects = folder('Projects', 'projects', pick(['projects']), { icon: 'folder' });
    const favs = folder('Favorites', 'favorites', pick(['curated']), { icon: 'favorites', cols: ['Name', 'Address', 'Kind', ''] });
    return { cats, toolbox, projects, favs };
  }

  /* ============================================================ explorer + file list */
  function renderList(pane, nodes, st, open, cols) {
    pane.replaceChildren();
    const sorted = nodes.slice().sort((a, b) => {
      if ((a.kind === 'folder') !== (b.kind === 'folder')) return a.kind === 'folder' ? -1 : 1;
      const key = st.sort.key, dir = st.sort.dir;
      const va = key === 'name' ? a.name.toLowerCase() : key === 'c2' ? (a.c2 || '').toLowerCase() : key === 'c3' ? (a.k3 || '') : (a.k4 || 0);
      const vb = key === 'name' ? b.name.toLowerCase() : key === 'c2' ? (b.c2 || '').toLowerCase() : key === 'c3' ? (b.k3 || '') : (b.k4 || 0);
      return (va < vb ? -1 : va > vb ? 1 : 0) * dir;
    });
    st.nodes = sorted;
    if (!sorted.length) { pane.append(el('div', { className: 'empty', textContent: 'This folder is empty.' })); return; }
    const select = (n, node, focus) => {
      pane.querySelectorAll('.sel').forEach((x) => { x.classList.remove('sel'); x.tabIndex = -1; });
      n.classList.add('sel'); n.tabIndex = 0; st.sel = node; st.onSel && st.onSel(node);
      if (focus) n.focus({ preventScroll: false });
    };
    const wire = (n, node, i) => {
      n.dataset.i = i; n.tabIndex = i === 0 ? 0 : -1;
      n.addEventListener('click', () => select(n, node, false));
      n.addEventListener('dblclick', () => open(node));
      n.addEventListener('keydown', (e) => {
        const all = [...pane.querySelectorAll('[data-i]')], at = all.indexOf(n);
        const step = st.view === 'icons' ? { ArrowRight: 1, ArrowLeft: -1, ArrowDown: Math.max(1, Math.floor(pane.clientWidth / 98)), ArrowUp: -Math.max(1, Math.floor(pane.clientWidth / 98)) } : { ArrowDown: 1, ArrowUp: -1, ArrowRight: 1, ArrowLeft: -1 };
        if (e.key === 'Enter') { e.preventDefault(); open(node); }
        else if (step[e.key] != null) { e.preventDefault(); const t = all[Math.max(0, Math.min(all.length - 1, at + step[e.key]))]; if (t) { t.click(); t.focus(); } }
      });
    };
    if (st.view === 'details') {
      const labels = cols || ['Name', 'Platform', 'Date', 'Size'];
      const t = el('table', { className: 'det' }), cg = el('colgroup');
      ['c1', 'c2', 'c3', 'c4'].forEach((c) => cg.append(el('col', { className: c })));
      const head = el('tr');
      ['name', 'c2', 'c3', 'c4'].forEach((k, i) => {
        const th = el('th', { textContent: labels[i] });
        th.setAttribute('role', 'button'); th.tabIndex = 0;
        if (st.sort.key === k) th.className = 'sorted' + (st.sort.dir < 0 ? ' desc' : '');
        const go = () => { st.sort = { key: k, dir: st.sort.key === k ? -st.sort.dir : 1 }; renderList(pane, nodes, st, open, cols); };
        th.addEventListener('click', go); th.addEventListener('keydown', (e) => { if (e.key === 'Enter') go(); });
        head.append(th);
      });
      t.append(cg, el('thead', {}, head));
      const tb = el('tbody');
      sorted.forEach((node, i) => {
        const tr = el('tr', { className: 'row' }, el('td', {}, el('span', { className: 'n' }, pix(node.icon), el('b', { textContent: node.name }))), el('td', { textContent: node.c2 || '' }), el('td', { textContent: node.c3 || '' }), el('td', { textContent: node.c4 || '' }));
        tr.title = node.name; wire(tr, node, i); tb.append(tr);
      });
      t.append(tb); pane.append(t);
    } else {
      const box = el('div', { className: 'items' + (st.view === 'list' ? ' list' : '') });
      sorted.forEach((node, i) => { const b = el('button', { type: 'button', className: 'fi', title: node.name }, pix(node.icon, st.view === 'list' ? 16 : 32), el('span', { textContent: node.name })); wire(b, node, i); box.append(b); });
      pane.append(box);
    }
  }

  function openExplorer(root, o = {}) {
    const st = { stack: [root], view: root.view || 'details', sort: { key: 'name', dir: 1 }, sel: null };
    const path = () => 'C:\\Hunting\\' + st.stack.map((n) => n.name).join('\\');
    const win = openWindow({ id: 'dir:' + root.id, title: root.name, icon: root.icon || 'folder', w: o.w || 660, h: o.h || 430 });
    const pane = el('div', { className: 'pane' });
    const addr = el('div', { className: 'addr' });
    const status = el('div', { className: 'status' }, el('div'), el('div'));
    const back = el('button', { type: 'button', className: 'btn sq', title: 'Back', textContent: '◀' });
    const up = el('button', { type: 'button', className: 'btn sq', title: 'Up one level', textContent: '▲' });
    const cur = () => st.stack[st.stack.length - 1];
    const open = (node) => openNode(node, { explorer: { cd, win } });
    const refresh = () => {
      const n = cur();
      renderList(pane, n.children, st, open, n.cols || (st.stack[0].cols));
      addr.textContent = path(); win.setTitle(n.name); back.disabled = up.disabled = st.stack.length < 2;
      status.firstChild.textContent = `${n.children.length} object(s)`; status.lastChild.textContent = '';
      st.onSel = (node) => { status.lastChild.textContent = node ? (node.kind === 'folder' ? node.c4 : node.c2) : ''; };
      if (win.task) win.task.querySelector('img').src = icon(n.icon || 'folder', 16);
      if (st.moved) pane.querySelector('[data-i]')?.focus({ preventScroll: true });
    };
    const cd = (node) => { st.stack.push(node); st.moved = true; refresh(); };
    const goUp = () => { if (st.stack.length > 1) { st.stack.pop(); st.moved = true; refresh(); } };
    back.addEventListener('click', goUp); up.addEventListener('click', goUp);
    win.body.addEventListener('keydown', (e) => { if (e.key === 'Backspace' && e.target.tagName !== 'INPUT') { e.preventDefault(); goUp(); } });
    const setView = (v) => { st.view = v; refresh(); };
    const menu = menubar([
      { label: 'File', items: () => [{ label: 'Open', action: () => st.sel && open(st.sel), disabled: !st.sel }, '-', { label: 'Close', action: () => win.close() }] },
      { label: 'View', items: () => [{ label: 'Large Icons', on: st.view === 'icons', action: () => setView('icons') }, { label: 'List', on: st.view === 'list', action: () => setView('list') }, { label: 'Details', on: st.view === 'details', action: () => setView('details') }, '-', { label: 'Up One Level', action: goUp, disabled: st.stack.length < 2 }] },
      { label: 'Help', items: () => [{ label: 'About Hunting Desktop', action: aboutDesktop }] },
    ]);
    win.body.append(menu, el('div', { className: 'toolbar' }, back, up, addr), pane, status);
    refresh();
    return win;
  }

  /* ============================================================ opening things */
  function openNode(node, ctx = {}) {
    if (node.kind === 'folder') { ctx.explorer ? ctx.explorer.cd(node) : openExplorer(node); return; }
    if (node.kind === 'doc') { openDoc(node.item); return; }
    if (node.kind === 'cheat') { openReader(node.item, node.item.live, node.name, 'book'); return; }
    openInfo(node.item);
  }
  function setHash(h) { try { history.replaceState(null, '', h ? '#open=' + h : location.pathname + location.search); } catch (e) { /* ignore */ } }

  function openReader(item, src, title, ico) {
    const win = openWindow({ id: 'doc:' + item.id, title: title || item.title, icon: ico || 'doc', w: 840, h: 600, onFocus: () => item.type === 'writeups' && setHash(item.href), onClose: () => { if (location.hash.includes(encodeURIComponent(item.href)) || location.hash.includes(item.href)) setHash(''); } });
    if (win.body.childElementCount) return win;
    const pane = el('div', { className: 'pane iframe' });
    const loading = el('div', { className: 'loading', textContent: 'Loading…' });
    const frame = el('iframe', { src, title: item.title, loading: 'eager' });
    frame.addEventListener('load', () => loading.remove());
    pane.append(frame, loading);
    const pageUrl = item.type === 'writeups' ? item.href : src;
    const menu = menubar([
      { label: 'File', items: () => [{ label: 'Open in New Tab', action: () => window.open(pageUrl, '_blank', 'noopener') }, { label: 'View Source on GitHub', action: () => window.open(item.url, '_blank', 'noopener') }, '-', { label: 'Close', action: () => win.close() }] },
      { label: 'View', items: () => [{ label: 'Refresh', action: () => { frame.contentWindow.location.reload(); } }, { label: win.el.classList.contains('max') ? 'Restore' : 'Maximize', action: () => toggleMax(win) }] },
      { label: 'Help', items: () => [{ label: 'About Hunting Desktop', action: aboutDesktop }] },
    ]);
    const bits = [item.platform, item.category, fmt(item.date), item.minutes ? `${item.minutes} min read` : ''].filter(Boolean).join(' · ');
    win.body.append(menu, pane, el('div', { className: 'status' }, el('div', { textContent: bits || item.description || '' })));
    return win;
  }
  function openDoc(item) { return openReader(item, item.href + '?embed=1', item.title, 'doc'); }

  function openInfo(item) {
    const ext = item.type === 'curated';
    const lines = [el('p', { textContent: item.description || 'No description.' })];
    if (ext) lines.push(el('p', { textContent: item.display || item.url }));
    if (item.tags.length) lines.push(el('p', { textContent: 'Tags: ' + item.tags.slice(ext ? 1 : 0).join(', ') }));
    dialog({ id: 'info:' + item.id, title: item.title, ico: ext ? 'globe' : 'exe', w: 460, body: lines, buttons: [
      { label: ext ? 'Open Link' : 'Open on GitHub', def: true, action: () => { window.open(item.url, '_blank', 'noopener'); return false; } },
      { label: 'Close' }] });
  }

  function openAbout() {
    const p = D.profile, st = D.stats;
    const doc = el('div', { className: 'doc' });
    const line = (t) => doc.append(document.createTextNode(t + '\n'));
    doc.append(el('h1', { textContent: 'ABOUT ME.TXT' }));
    line(`${p.name || 'L0WK3Y'} · ${p.tagline || ''}`); line(''); line(p.bio || ''); line('');
    if (D.portswigger) line(`portswigger ${D.portswigger.overall.done}/${D.portswigger.overall.total} labs`);
    line(`write-ups   ${st.writeups}`); line(`platforms   ${st.platforms}`); line(`categories  ${st.series}`); line(`updated     ${fmt(st.updated)}`); line('');
    line('Find me:');
    (p.links || []).filter((l) => l.url).forEach((l) => { doc.append(document.createTextNode(`  ${l.label.padEnd(10)}`)); doc.append(el('a', { href: l.url, target: '_blank', rel: 'noopener me', textContent: l.url })); doc.append('\n'); });
    line(''); line('Tip: double-click a folder to open it, then double-click a write-up to read it.');
    line('Everything here is generated from the repo on every push.'); line('');
    doc.append('Desktop look inspired by "Windows 95" by Gabrielle Wee (MIT): ');
    doc.append(el('a', { href: 'https://codepen.io/gabriellewee/pen/MWqRZzp', target: '_blank', rel: 'noopener', textContent: 'codepen.io/gabriellewee' }));
    const win = openWindow({ id: 'about', title: 'About Me - Notepad', icon: 'notepad', w: 560, h: 420 });
    if (!win.body.childElementCount) win.body.append(menubar([{ label: 'File', items: () => [{ label: 'Exit', action: () => win.close() }] }, { label: 'Help', items: () => [{ label: 'About Hunting Desktop', action: aboutDesktop }] }]), el('div', { className: 'pane' }, doc));
  }
  function aboutDesktop() {
    dialog({ id: 'about-desktop', title: 'About Hunting Desktop', ico: 'computer', w: 420, body: [
      'Hunting Desktop 98', `${D.stats.writeups} write-ups in ${D.stats.series} categories, rebuilt from the repo on every push.`,
      'Window chrome inspired by the "Windows 95" CodePen by Gabrielle Wee (MIT License). Icons: Windows 98 icon pack.'], buttons: [{ label: 'OK', def: true }] });
  }

  /* ---------- PortSwigger progress (from README.md via data/index.json) ---------- */
  const pbar = (done, total, label) => {
    const b = el('div', { className: 'pbar' }, el('i', { style: `width:${total ? (100 * done / total).toFixed(1) : 0}%` }));
    b.setAttribute('role', 'progressbar'); b.setAttribute('aria-label', label);
    b.setAttribute('aria-valuemin', '0'); b.setAttribute('aria-valuemax', String(total)); b.setAttribute('aria-valuenow', String(done));
    return b;
  };
  function openPortSwigger() {
    const ps = D.portswigger;
    if (!ps) { alertBox('PortSwigger Academy', 'No PortSwigger progress found in README.md.', 'info'); return; }
    const win = openWindow({ id: 'portswigger', title: 'PortSwigger Academy - Progress', icon: 'lock', w: 600, h: 520 });
    if (win.body.childElementCount) return;
    const pane = el('div', { className: 'pane psw' });
    const top = el('div', { className: 'ps-top' }, el('b', { textContent: `${ps.overall.done} of ${ps.overall.total} labs solved` }), el('span', { textContent: ps.updated ? ` · updated ${fmt(ps.updated)}` : '' }));
    pane.append(top);
    ps.levels.forEach((l) => pane.append(el('div', { className: 'ps-lv' }, el('span', { textContent: l.label }), pbar(l.done, l.total, `${l.label} labs solved`), el('span', { className: 'n', textContent: `${l.done}/${l.total}  ${l.pct}%` }))));
    const tbl = el('table', { className: 'det ps-tbl' }), cg = el('colgroup');
    ['46%', '26%', '12%', '16%'].forEach((w) => cg.append(el('col', { style: 'width:' + w })));
    tbl.append(cg, el('thead', {}, el('tr', {}, ...['Topic', 'Progress', 'Solved', 'Status'].map((t) => el('th', { textContent: t })))));
    const tb = el('tbody');
    const ST = { done: 'Complete', progress: 'In progress', todo: 'Not started' };
    [...new Set(ps.topics.map((t) => t.group))].forEach((g) => {
      tb.append(el('tr', { className: 'grp' }, el('td', { colSpan: 4, textContent: g })));
      ps.topics.filter((t) => t.group === g).forEach((t) => tb.append(el('tr', { className: 'row' }, el('td', { textContent: t.name }), el('td', {}, pbar(t.done, t.total, `${t.name} labs solved`)), el('td', { textContent: `${t.done}/${t.total}` }), el('td', { textContent: ST[t.status] }))));
    });
    tbl.append(tb); pane.append(tbl);
    const open = el('button', { type: 'button', className: 'btn', textContent: 'Open Academy' });
    open.addEventListener('click', () => window.open(ps.url, '_blank', 'noopener'));
    const mine = el('button', { type: 'button', className: 'btn', textContent: 'My write-ups' });
    mine.addEventListener('click', () => { const web = model.cats.find((c) => c.name === 'Web'); if (web) openExplorer(web); });
    win.body.append(menubar([{ label: 'File', items: () => [{ label: 'Open Academy in New Tab', action: () => window.open(ps.url, '_blank', 'noopener') }, '-', { label: 'Close', action: () => win.close() }] }, { label: 'Help', items: () => [{ label: 'About Hunting Desktop', action: aboutDesktop }] }]),
      el('div', { className: 'toolbar' }, open, mine), pane, el('div', { className: 'status' }, el('div', { textContent: `${ps.topics.length} topics · numbers come from README.md` })));
  }

  /* ---------- find + run ---------- */
  function openFind(query = '') {
    const st = { view: 'details', sort: { key: 'name', dir: 1 }, sel: null };
    const win = openWindow({ id: 'find', title: 'Find: All Files', icon: 'search', w: 640, h: 430 });
    if (win.body.childElementCount) { win.body.querySelector('input')?.focus(); return; }
    const pane = el('div', { className: 'pane' });
    const input = el('input', { className: 'field', type: 'search', placeholder: 'title, tag, platform…', value: query });
    input.setAttribute('aria-label', 'Named');
    const status = el('div', { className: 'status' }, el('div'));
    const all = items.map(fileNode);
    const run = () => {
      const ts = input.value.toLowerCase().split(/\s+/).filter(Boolean);
      const found = ts.length ? all.filter((n) => { const h = (n.name + ' ' + (n.item.description || '') + ' ' + (n.item.platform || '') + ' ' + (n.item.category || '') + ' ' + n.item.tags.join(' ')).toLowerCase(); return ts.every((t) => h.includes(t)); }) : [];
      renderList(pane, found, st, (node) => openNode(node));
      if (!ts.length) pane.replaceChildren(el('div', { className: 'empty', textContent: 'Type a name above to search every write-up, tool and link.' }));
      status.firstChild.textContent = ts.length ? `${found.length} file(s) found` : 'Ready';
    };
    const go = el('button', { type: 'button', className: 'btn def', textContent: 'Find Now' });
    go.addEventListener('click', run);
    input.addEventListener('input', run);
    win.body.append(menubar([{ label: 'File', items: () => [{ label: 'Close', action: () => win.close() }] }]), el('div', { className: 'toolbar' }, el('span', { className: 'lbl', textContent: 'Named:' }), input, go), pane, status);
    run(); input.focus();
  }
  function runCommand(raw) {
    const q = raw.trim().toLowerCase();
    if (!q) return true;
    const special = { hub: goHub, simple: goHub, exit: goHub, about: openAbout, whoami: openAbout, portswigger: openPortSwigger, ps: openPortSwigger, labs: openPortSwigger, find: () => openFind(), github: () => window.open(D.site.repo, '_blank', 'noopener'), feed: () => window.open('feed.xml', '_blank', 'noopener'), rss: () => window.open('feed.xml', '_blank', 'noopener'), shutdown: shutDown, help: aboutDesktop };
    if (special[q]) { special[q](); return true; }
    const folders = [...model.cats, model.toolbox, model.favs, model.projects].filter((f) => f.children.length);
    const f = folders.find((x) => x.name.toLowerCase() === q) || folders.find((x) => x.name.toLowerCase().startsWith(q));
    if (f) { openExplorer(f); return true; }
    const it = items.find((i) => i.title.toLowerCase() === q) || items.find((i) => i.title.toLowerCase().includes(q));
    if (it) { openNode(fileNode(it)); return true; }
    alertBox(raw, `Cannot find '${raw}'. Make sure you typed the name correctly, then try again.`, 'warn');
    return false;
  }
  function openRun() {
    const input = el('input', { className: 'field', type: 'text', placeholder: 'android, toolbox, a write-up title…', spellcheck: false, autocomplete: 'off' });
    input.setAttribute('aria-label', 'Open');
    const w = dialog({ id: 'run', title: 'Run', ico: 'run', w: 440, body: [el('p', { textContent: 'Type the name of a category, write-up or tool, and Hunting Desktop will open it for you.' }), el('div', { className: 'opt' }, el('label', { textContent: 'Open:' }), input)],
      buttons: [{ label: 'OK', def: true, action: () => (runCommand(input.value) ? true : false) }, { label: 'Cancel' }, { label: 'Browse…', action: () => { openFind(input.value); } }] });
    input.focus();
    return w;
  }

  /* ---------- shut down / simple view ---------- */
  function goHub() { try { localStorage.setItem('hwl-view', 'hub'); } catch (e) { /* ignore */ } location.href = 'hub/'; }
  function shutDown() {
    const opts = [['hub', 'Switch to the simple (modern) view'], ['restart', 'Restart the computer'], ['off', 'Shut down the computer?']];
    const radios = opts.map(([v, t], i) => { const r = el('input', { type: 'radio', name: 'sd', value: v, id: 'sd-' + v, checked: i === 0 }); return el('div', { className: 'opt' }, r, el('label', { htmlFor: 'sd-' + v, textContent: t })); });
    dialog({ id: 'shutdown', title: 'Shut Down Hunting Desktop', ico: 'shutdown', w: 420, body: [el('p', { textContent: 'What do you want the computer to do?' }), ...radios],
      buttons: [{ label: 'OK', def: true, action: () => {
        const v = radios.map((r) => r.firstChild).find((r) => r.checked).value;
        if (v === 'hub') goHub(); else if (v === 'restart') location.reload();
        else { const off = el('div', { id: 'off', tabIndex: 0, innerHTML: 'It\'s now safe to turn off<br>your computer.<br><br><small style="font-size:14px;opacity:.7">(click or press any key to turn it back on)</small>' }); document.body.append(off); off.focus(); const wake = () => location.reload(); off.addEventListener('click', wake); off.addEventListener('keydown', wake); }
      } }, { label: 'Cancel' }] });
  }

  /* ============================================================ desktop icons, start menu, clock */
  let model;
  function deskIcon(name, ico, open) {
    const b = el('button', { type: 'button', className: 'dicon' }, pix(ico, 32), el('span', { textContent: name }));
    b.addEventListener('click', (e) => { e.stopPropagation(); iconsBox.querySelectorAll('.sel').forEach((x) => x.classList.remove('sel')); b.classList.add('sel'); closeStart(); });
    b.addEventListener('dblclick', open);
    b.addEventListener('keydown', (e) => { if (e.key === 'Enter') { e.preventDefault(); open(); } });
    iconsBox.append(b);
    return b;
  }
  function buildDesktop() {
    iconsBox.replaceChildren();
    deskIcon('About Me', 'notepad', openAbout);
    if (D.portswigger) deskIcon('PortSwigger', 'lock', openPortSwigger);
    model.cats.forEach((c) => deskIcon(c.name, 'folder', () => openExplorer(c)));
    [model.toolbox, model.favs, model.projects].forEach((f) => { if (f.children.length) deskIcon(f.name, f.icon, () => openExplorer(f)); });
    deskIcon('Find', 'search', () => openFind());
    deskIcon('Simple View', 'globe', goHub);
    deskIcon('Feed.rss', 'rss', () => window.open('feed.xml', '_blank', 'noopener'));
    deskIcon('Recycle Bin', 'bin', () => alertBox('Recycle Bin', 'The Recycle Bin is empty. 0 bugs deleted (report them instead).', 'info'));
    desktop.append(el('div', { className: 'brand-mark', innerHTML: 'Hunting<br>With L0WK3Y<small>Desktop 98</small>' }));
  }

  const startBtn = $('#start');
  let startEl = null;
  function closeStart() { if (startEl) { startEl.remove(); startEl = null; startBtn.setAttribute('aria-expanded', 'false'); } }
  function toggleStart() {
    if (startEl) { closeStart(); return; }
    const sub = (title, nodes, hdr) => {
      const ul = el('ul', { className: 'sub' });
      if (hdr) ul.append(el('li', { className: 'hd', textContent: hdr }));
      nodes.forEach(([label, ico, fn]) => { const b = el('button', { type: 'button' }, pix(ico), label); b.addEventListener('click', () => { closeStart(); fn(); }); ul.append(el('li', {}, b)); });
      return ul;
    };
    const entry = (label, ico, fn, submenu) => {
      const li = el('li', { className: submenu ? 'has' : '' });
      const b = el('button', { type: 'button' }, pix(ico, 32), label);
      if (submenu) {
        const open = () => { startEl.querySelectorAll('li.open').forEach((x) => x.classList.remove('open')); li.classList.add('open'); };
        b.addEventListener('mouseenter', open); b.addEventListener('click', open); b.addEventListener('focus', open);
        li.append(b, submenu);
        submenu.style.display = 'none';
        new MutationObserver(() => { submenu.style.display = li.classList.contains('open') ? 'block' : 'none'; }).observe(li, { attributes: true, attributeFilter: ['class'] });
      } else { b.addEventListener('mouseenter', () => startEl.querySelectorAll('li.open').forEach((x) => x.classList.remove('open'))); b.addEventListener('click', () => { closeStart(); fn(); }); li.append(b); }
      return li;
    };
    const programs = sub('Programs', [...model.cats.map((c) => [c.name, 'folder', () => openExplorer(c)]), ...(D.portswigger ? [['PortSwigger Progress', 'lock', openPortSwigger]] : []), ...[model.toolbox, model.favs, model.projects].filter((f) => f.children.length).map((f) => [f.name, f.icon, () => openExplorer(f)])]);
    const docs = sub('Documents', items.filter((i) => i.type === 'writeups').slice(0, 8).map((i) => [i.title, 'doc', () => openDoc(i)]), 'Newest write-ups');
    const ul = el('ul', {}, entry('Programs', 'folderOpen', null, programs), entry('Documents', 'doc', null, docs), entry('Find…', 'search', openFind), entry('Run…', 'run', openRun), entry('Help', 'help', aboutDesktop), el('hr'), entry('Simple View', 'globe', goHub), entry('Shut Down…', 'shutdown', shutDown));
    startEl = el('div', { id: 'start-menu' }, el('div', { className: 'side' }, el('b', { innerHTML: 'Hunting <i>98</i>' })), ul);
    document.body.append(startEl);
    startBtn.setAttribute('aria-expanded', 'true');
    startEl.querySelector('button')?.focus();
  }
  startBtn.addEventListener('click', (e) => { e.stopPropagation(); toggleStart(); });
  document.addEventListener('pointerdown', (e) => { if (startEl && !e.target.closest('#start-menu') && !e.target.closest('#start')) closeStart(); });
  desktop.addEventListener('pointerdown', (e) => { if (e.target === desktop || e.target === iconsBox) iconsBox.querySelectorAll('.sel').forEach((x) => x.classList.remove('sel')); });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      if (openPop) { closePop(); return; }
      if (startEl) { closeStart(); startBtn.focus(); return; }
      if (active && !e.defaultPrevented) active.close();
    }
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); openFind(); }
  });

  const clock = $('#clock');
  const tick = () => { clock.textContent = new Date().toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' }); };
  tick(); setInterval(tick, 15000);
  $('#start img').src = icon('flag'); $('#tray-vol').src = icon('speaker');

  /* ============================================================ boot */
  function welcome() {
    let skip = false;
    try { skip = localStorage.getItem('hwl-welcome') === '0'; } catch (e) { /* ignore */ }
    if (skip) return;
    const cb = el('input', { type: 'checkbox', id: 'wlc', checked: true });
    dialog({ id: 'welcome', title: 'Welcome', ico: 'info', w: 460, body: [
      el('p', {}, el('b', { textContent: 'Welcome to Hunting With L0WK3Y.' })),
      el('p', { textContent: 'Each folder is a category of write-ups. Double-click one to open it, then double-click a write-up to read it in its own window. You can open as many as you like.' }),
      el('p', { textContent: 'Start > Find (or Ctrl K) searches everything. "Simple View" switches to the plain website.' }),
      el('div', { className: 'opt' }, cb, el('label', { htmlFor: 'wlc', textContent: 'Show this Welcome Screen next time' }))],
    buttons: [{ label: 'Close', def: true, action: () => { try { localStorage.setItem('hwl-welcome', cb.checked ? '1' : '0'); } catch (e) { /* ignore */ } } }, { label: 'About Me', action: () => { openAbout(); } }] });
  }
  function openFromHash() {
    const m = location.hash.match(/^#open=(.+)$/);
    if (!m) return false;
    const href = decodeURIComponent(m[1]);
    const it = byHref[href];
    if (it) { openDoc(it); return true; }
    const c = model.cats.find((x) => x.href === href);
    if (c) { openExplorer(c); return true; }
    return false;
  }

  async function init() {
    try { D = await (await fetch('data/index.json', { cache: 'no-cache' })).json(); } catch (e) {
      alertBox('Hunting Desktop', 'Could not load data/index.json. Run scripts/build_index.py and serve the site/ folder.');
      return;
    }
    items = D.items; series = D.series;
    items.forEach((i) => { if (i.href) byHref[i.href] = i; });
    model = buildModel();
    buildDesktop();
    if (!openFromHash()) welcome();
    addEventListener('hashchange', openFromHash);
    $('#loading')?.remove();
  }
  init();
})();
