/* Reading pages: progress bar, table-of-contents scroll-spy and code copy buttons. */
(() => {
  'use strict';
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];

  /* progress bar */
  const bar = $('#bar'), prose = $('.prose');
  if (bar && prose) {
    let raf = 0;
    const update = () => {
      raf = 0;
      const start = prose.getBoundingClientRect().top + scrollY;
      const span = Math.max(1, prose.offsetHeight - innerHeight * 0.6);
      bar.style.transform = `scaleX(${Math.min(1, Math.max(0, (scrollY - start + innerHeight * 0.2) / span))})`;
    };
    addEventListener('scroll', () => { if (!raf) raf = requestAnimationFrame(update); }, { passive: true });
    addEventListener('resize', update);
    update();
  }

  /* table of contents scroll-spy */
  const links = $$('.toc a');
  if (links.length && 'IntersectionObserver' in window) {
    const byId = new Map(links.map((a) => [a.getAttribute('href').slice(1), a]));
    const visible = new Set();
    const mark = () => {
      const heads = $$('.prose h2[id], .prose h3[id]');
      let current = heads.find((h) => visible.has(h.id)) || [...heads].reverse().find((h) => h.getBoundingClientRect().top < 120) || heads[0];
      links.forEach((a) => a.removeAttribute('aria-current'));
      const a = current && byId.get(current.id);
      if (a) { a.setAttribute('aria-current', 'true'); a.scrollIntoView({ block: 'nearest' }); }
    };
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => (e.isIntersecting ? visible.add(e.target.id) : visible.delete(e.target.id)));
      mark();
    }, { rootMargin: '-72px 0px -65% 0px' });
    $$('.prose h2[id], .prose h3[id]').forEach((h) => io.observe(h));
  }
  $$('.toc-m a').forEach((a) => a.addEventListener('click', () => { a.closest('details').open = false; }));

  /* inside the desktop's iframe: external links open in a new tab, the progress/TOC chrome is hidden by CSS */
  if (document.documentElement.classList.contains('embed')) {
    document.querySelectorAll('a[href^="http"]').forEach((l) => { l.target = '_blank'; l.rel = 'noopener'; });
  }

  /* copy buttons (event delegation) */
  document.addEventListener('click', async (e) => {
    const btn = e.target.closest('.copy');
    if (!btn) return;
    const code = btn.closest('.code').querySelector('code').innerText.replace(/\n$/, '');
    try {
      await navigator.clipboard.writeText(code);
    } catch (err) {                       // http:// or blocked clipboard: legacy fallback
      const t = Object.assign(document.createElement('textarea'), { value: code });
      t.style.position = 'fixed'; t.style.opacity = '0';
      document.body.append(t); t.select();
      try { document.execCommand('copy'); } catch (e2) { /* nothing more to try */ }
      t.remove();
    }
    const old = btn.textContent;
    btn.textContent = 'Copied';
    btn.classList.add('done');
    setTimeout(() => { btn.textContent = old; btn.classList.remove('done'); }, 1600);
  });
})();
