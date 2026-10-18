/* Spondylus: prototyp nowej strony. Zachowania interfejsu bez zależności. */
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const ruchOgr = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Nagłówek: linia pod spodem po przewinięciu */
  const header = $('#header');
  const onScroll = () => header && header.classList.toggle('is-scrolled', scrollY > 8);
  addEventListener('scroll', onScroll, { passive: true }); onScroll();

  /* Menu oferty (mega menu) */
  const megaBtn = $('[data-mega]'), mega = $('#mega');
  if (megaBtn && mega) {
    const ustaw = (o) => { mega.classList.toggle('is-open', o); megaBtn.setAttribute('aria-expanded', String(o)); };
    megaBtn.addEventListener('click', () => ustaw(!mega.classList.contains('is-open')));
    document.addEventListener('click', (e) => { if (!e.target.closest('#mega, [data-mega]')) ustaw(false); });
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape') ustaw(false); });
  }

  /* Menu mobilne */
  const drawer = $('#drawer');
  const drawerSet = (o) => { drawer.classList.toggle('is-open', o); drawer.setAttribute('aria-hidden', String(!o)); document.body.style.overflow = o ? 'hidden' : ''; };
  $$('[data-drawer-open]').forEach(b => b.addEventListener('click', () => drawerSet(true)));
  $$('[data-drawer-close]').forEach(b => b.addEventListener('click', () => drawerSet(false)));

  /* Komunikat prototypu dla podstron, które powstaną w kolejnym etapie */
  const toast = $('#toast'); let tt;
  const pokaz = (txt) => { toast.textContent = txt; toast.classList.add('is-on'); clearTimeout(tt); tt = setTimeout(() => toast.classList.remove('is-on'), 2600); };
  document.addEventListener('click', (e) => {
    const a = e.target.closest('[data-demo="1"]');
    if (a) { e.preventDefault(); pokaz('Podstrona w przygotowaniu. Prototyp pokazuje stronę główną, kadrę i kontakt.'); }
  });
  /* K5: linki do podstron z kolejnego etapu oznaczone jako nieaktywne */
  $$('a[data-demo="1"]').forEach(a => { a.setAttribute('aria-disabled', 'true'); a.title = 'Podstrona w przygotowaniu'; });

  /* Rejestracja online: prawdziwe kalendarze ProAssist dla każdej placówki */
  const PLACOWKI = {
    'szczecin-jp': { nazwa: 'Szczecin, al. Jana Pawła II 36', wew: 'wew. 1', url: 'https://system.proassist.pl/widget/venue/view/ps-c618-rtj24/ps-v1212-y3d5s' },
    'szczecin-ul': { nazwa: 'Szczecin Pogodno, ul. Unii Lubelskiej 2B', wew: 'wew. 2', url: 'https://system.proassist.pl/widget/venue/view/ps-c618-rtj24/ps-v2043-5gi56' },
    'koszalin-spec': { nazwa: 'Koszalin, ul. Jana Pawła II 21, specjaliści', wew: 'wew. 4', url: 'https://system.proassist.pl/widget/venue/view/ps-c618-rtj24/ps-v1322-4ojyp' },
    'koszalin-uslugi': { nazwa: 'Koszalin, ul. Jana Pawła II 21, usługi', wew: 'wew. 4', url: 'https://system.proassist.pl/widget/services/venue/view/ps-c618-rtj24/ps-v1322-4ojyp/' },
  };
  const booking = $('#booking');
  if (booking) {
    const krok = (n) => {
      $$('[data-step]', booking).forEach(s => { s.hidden = s.dataset.step !== String(n); });
      $$('.booking__steps i', booking).forEach((i, k) => i.classList.toggle('is-done', k < n));
    };
    let poprzedni;
    const otworz = (miejsce) => {
      poprzedni = document.activeElement;
      drawerSet(false);
      booking.classList.add('is-open'); booking.setAttribute('aria-hidden', 'false'); document.body.style.overflow = 'hidden';
      if (miejsce && PLACOWKI[miejsce]) wybierz(miejsce); else krok(1);
      setTimeout(() => $('.booking__close', booking).focus(), 50);
    };
    const zamknij = () => { booking.classList.remove('is-open'); booking.setAttribute('aria-hidden', 'true'); document.body.style.overflow = ''; poprzedni && poprzedni.focus(); };
    const wybierz = (id) => {
      if (id === 'koszalin') return krok(2);
      const p = PLACOWKI[id];
      $('[data-place-name]', booking).innerHTML = `<b>${p.nazwa}</b>. Wybierz specjalistę lub usługę i wolny termin.`;
      const f = $('[data-widget]', booking); if (f.src !== p.url) f.src = p.url;
      const tel = $('[data-place-tel]', booking); tel.textContent = `665 035 035, ${p.wew}`;
      krok(3);
    };
    document.addEventListener('click', (e) => {
      const b = e.target.closest('[data-book]'); if (b) { e.preventDefault(); otworz(b.dataset.book); }
      if (e.target.closest('[data-book-close]')) zamknij();
      const pl = e.target.closest('[data-place]'); if (pl) wybierz(pl.dataset.place);
      const back = e.target.closest('[data-back]'); if (back) krok(Number(back.dataset.back));
    });
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && booking.classList.contains('is-open')) zamknij(); });
  }

  /* Wyszukiwarka "Z czym przychodzisz?" */
  const FINDER = {
    plecy: { obszar: 'Rehabilitacja i konsultacje', tytul: 'Ból pleców lub kręgosłupa', opis: 'Zaczynamy od oceny przyczyny bólu. Fizjoterapeuta dobiera terapię, a w razie potrzeby konsultuje Cię z neurologiem lub neurochirurgiem.', osoby: ['tomasz-gnus', 'gabriela-majorczyk', 'tomasz-zdeb', 'piotr-salapa'], opisOsob: 'Fizjoterapeuci i neurochirurg', link: '#', demo: true },
    uraz: { obszar: 'Rehabilitacja ortopedyczna', tytul: 'Po urazie lub operacji', opis: 'Rehabilitacja po endoprotezoplastyce, rekonstrukcji więzadeł, złamaniach i skręceniach. Bezpieczny powrót do codziennej aktywności.', osoby: ['tomasz-gnus', 'tomasz-zdeb', 'adam-kaminski'], opisOsob: 'Fizjoterapeuci i ortopeda', link: '#', demo: true },
    stopa: { obszar: 'Podologia', tytul: 'Stopy i paznokcie', opis: 'Wrastające paznokcie, odciski, pękające pięty, stopa cukrzycowa. Najpierw ustalamy przyczynę problemu, potem dobieramy leczenie.', osoby: ['marika-wachowiak'], opisOsob: 'Podolog', link: 'podologia.html' },
    dziecko: { obszar: 'Diagnostyka wad postawy', tytul: 'Wada postawy u dziecka', opis: 'Badanie postawy i stóp oraz terapia dzieci i młodzieży. Od lat prowadzimy też program profilaktyczny „Zdrowa Nóżka i Kręgosłup”.', osoby: ['magdalena-salabon'], opisOsob: 'Fizjoterapeutka dzieci i młodzieży', link: '#', demo: true },
    sport: { obszar: 'Medycyna sportowa', tytul: 'Sport i kontuzje', opis: 'Diagnostyka sportowa, leczenie przeciążeń i kontuzji, bezpieczny powrót do treningu. Dla amatorów i zawodowców.', osoby: ['tomasz-gnus', 'tomasz-zdeb'], opisOsob: 'Fizjoterapeuci', link: '#', demo: true },
    nfz: { obszar: 'Zaopatrzenie medyczne', tytul: 'Wkładki, obuwie, sprzęt z NFZ', opis: 'Indywidualne wkładki, obuwie profilaktyczne i sprzęt rehabilitacyjny. Pomagamy z refundacją NFZ i dofinansowaniem z MOPR i PCPR.', osoby: [], opisOsob: '', link: '#', demo: true },
  };
  const result = $('#finder-result');
  $$('[data-finder]').forEach(chip => chip.addEventListener('click', () => {
    const k = chip.dataset.finder, d = FINDER[k];
    const wl = chip.getAttribute('aria-pressed') === 'true';
    $$('[data-finder]').forEach(c => c.setAttribute('aria-pressed', 'false'));
    if (wl) { result.classList.remove('is-open'); return; }
    chip.setAttribute('aria-pressed', 'true');
    const av = d.osoby.map(o => `<img src="assets/img/kadra-${o}.webp" alt="" width="34" height="34">`).join('');
    result.innerHTML = `<div><div class="result">
      <div><div class="result__area">${d.obszar}</div><h3>${d.tytul}</h3><p>${d.opis}</p></div>
      <div class="result__actions"><button class="btn btn--primary btn--sm" type="button" data-book>Umów wizytę</button>
      <a class="btn btn--ghost btn--sm" href="${d.link}" ${d.demo ? 'data-demo="1"' : ''}>Zobacz szczegóły</a></div>
      ${d.osoby.length ? `<div class="result__people"><span class="avatars">${av}</span>${d.opisOsob}</div>` : `<div class="result__people">Doradztwo w każdej placówce, także w sklepie internetowym</div>`}
    </div></div>`;
    requestAnimationFrame(() => result.classList.add('is-open'));
  }));


  /* Kręgi w hero: po wejściu na stronę przesunięte warstwy układają się w jedną oś */
  const kregi = $('#kregi');
  if (kregi) {
    const wyrownaj = () => setTimeout(() => kregi.classList.remove('is-start'), 250);
    const img = $('img', kregi);
    if (img.complete) wyrownaj(); else img.addEventListener('load', wyrownaj, { once: true });
  }

  /* Opinie Google: karuzela i „Czytaj więcej” */
  const tiTor = $('#ti-tor');
  if (tiTor) {
    $$('[data-ti]').forEach(b => b.addEventListener('click', () => {
      const k = $('.ti-karta', tiTor); const krok = k ? k.getBoundingClientRect().width + 16 : 300;
      const kier = Number(b.dataset.ti), max = tiTor.scrollWidth - tiTor.clientWidth - 2;
      const zachowanie = ruchOgr ? 'auto' : 'smooth';
      if (kier > 0 && tiTor.scrollLeft >= max) tiTor.scrollTo({ left: 0, behavior: zachowanie });
      else if (kier < 0 && tiTor.scrollLeft <= 2) tiTor.scrollTo({ left: max + 2, behavior: zachowanie });
      else tiTor.scrollBy({ left: krok * kier, behavior: zachowanie });
    }));
    /* przeciąganie myszką na komputerze */
    let start = null;
    tiTor.addEventListener('pointerdown', (e) => { if (e.pointerType !== 'mouse' || e.target.closest('button')) return; start = { x: e.clientX, l: tiTor.scrollLeft, ruch: false }; });
    addEventListener('pointermove', (e) => { if (!start) return; const dx = e.clientX - start.x; if (Math.abs(dx) > 4) { start.ruch = true; tiTor.classList.add('is-drag'); } tiTor.scrollLeft = start.l - dx; });
    addEventListener('pointerup', () => { if (!start) return; start = null; tiTor.classList.remove('is-drag'); });
    $$('.ti-karta', tiTor).forEach(k => {
      const t = $('.ti-tekst', k), btn = $('.ti-wiecej', k);
      if (t.scrollHeight <= t.clientHeight + 2) { btn.hidden = true; return; }
      btn.addEventListener('click', () => { const o = k.classList.toggle('is-open'); btn.setAttribute('aria-expanded', String(o)); btn.textContent = o ? 'Zwiń' : 'Czytaj więcej'; });
    });
  }

  /* Kadra: przewijanie rzędu */
  $$('[data-row]').forEach(nav => {
    const row = $(nav.dataset.row);
    $$('button', nav).forEach(b => b.addEventListener('click', () => row.scrollBy({ left: (b.dataset.dir === 'next' ? 1 : -1) * row.clientWidth * .8, behavior: ruchOgr ? 'auto' : 'smooth' })));
  });

  /* Kadra: filtry */
  const filtry = $$('[data-filter]');
  filtry.forEach(f => f.addEventListener('click', () => {
    filtry.forEach(x => x.setAttribute('aria-pressed', String(x === f)));
    const k = f.dataset.filter;
    $$('[data-group]').forEach(p => { p.hidden = !(k === 'wszyscy' || p.dataset.group.split(' ').includes(k)); });
  }));

  /* Spis treści podstrony: aktywna sekcja */
  const toc = $$('.toc a[href^="#"]');
  if (toc.length && 'IntersectionObserver' in window) {
    const io = new IntersectionObserver((ents) => ents.forEach(en => {
      if (en.isIntersecting) toc.forEach(a => a.classList.toggle('is-active', a.getAttribute('href') === '#' + en.target.id));
    }), { rootMargin: '-30% 0px -60% 0px' });
    toc.forEach(a => { const s = $(a.getAttribute('href')); s && io.observe(s); });
  }

  /* Formularz kontaktowy (prototyp: bez wysyłki) */
  $$('form[data-proto]').forEach(f => f.addEventListener('submit', (e) => { e.preventDefault(); if (f.reportValidity()) f.classList.add('is-sent'); }));

  /* Treść widoczna od razu, bez animacji wejścia sekcji */
  $$('.reveal').forEach(r => r.classList.add('is-in'));

  /* Panel dostępności (WCAG): wielkość tekstu, kontrast, linki, odstępy, czcionka, animacje, kursor */
  const html = document.documentElement;
  const a11yBtn = $('[data-a11y-open]'), a11yPanel = $('#a11y-panel');
  const A11Y_KEY = 'spondylus-a11y';
  const czytaj = () => { try { return JSON.parse(localStorage.getItem(A11Y_KEY)) || {}; } catch (e) { return {}; } };
  const zapisz = (st) => { try { localStorage.setItem(A11Y_KEY, JSON.stringify(st)); } catch (e) {} };
  const zastosuj = (st) => {
    html.classList.remove('a11y-txt-1', 'a11y-txt-2');
    if (st.size) html.classList.add('a11y-txt-' + st.size);
    ['contrast', 'links', 'spacing', 'font', 'still', 'cursor'].forEach(k => html.classList.toggle('a11y-' + k, !!st[k]));
    if (st.font && !$('#atkinson')) { const l = document.createElement('link'); l.id = 'atkinson'; l.rel = 'stylesheet'; l.href = 'https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&display=swap'; document.head.appendChild(l); }
    $$('[data-a11y-size]').forEach(b => b.setAttribute('aria-pressed', String(String(st.size || 0) === b.dataset.a11ySize)));
    $$('[data-a11y]').forEach(b => b.setAttribute('aria-pressed', String(!!st[b.dataset.a11y])));
  };
  let a11y = czytaj(); zastosuj(a11y);
  if (a11yBtn && a11yPanel) {
    const otworzA = (o) => { a11yPanel.classList.toggle('is-open', o); a11yBtn.setAttribute('aria-expanded', String(o)); if (o) setTimeout(() => $('[data-a11y-size]', a11yPanel).focus(), 60); };
    a11yBtn.addEventListener('click', () => otworzA(!a11yPanel.classList.contains('is-open')));
    $('[data-a11y-close]').addEventListener('click', () => { otworzA(false); a11yBtn.focus(); });
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && a11yPanel.classList.contains('is-open')) { otworzA(false); a11yBtn.focus(); } });
    document.addEventListener('click', (e) => { if (!e.target.closest('#a11y-panel, [data-a11y-open]')) otworzA(false); });
    $$('[data-a11y-size]').forEach(b => b.addEventListener('click', () => { a11y.size = Number(b.dataset.a11ySize); zastosuj(a11y); zapisz(a11y); }));
    $$('[data-a11y]').forEach(b => b.addEventListener('click', () => { a11y[b.dataset.a11y] = !a11y[b.dataset.a11y]; zastosuj(a11y); zapisz(a11y); }));
    $('[data-a11y-reset]').addEventListener('click', () => { a11y = {}; zastosuj(a11y); zapisz(a11y); });
  }

  /* Akordeony: płynne otwieranie i zamykanie */
  $$('details.acc').forEach(d => {
    const sum = $('summary', d), body = $('.acc__body', d);
    sum.addEventListener('click', (e) => {
      if (ruchOgr || html.classList.contains('a11y-still')) return;
      e.preventDefault();
      if (d.open) {
        const h = body.scrollHeight; body.style.height = h + 'px';
        requestAnimationFrame(() => { body.style.transition = 'height .35s cubic-bezier(.22,.8,.24,1)'; body.style.height = '0px'; });
        body.addEventListener('transitionend', () => { d.open = false; body.style.cssText = ''; }, { once: true });
      } else {
        d.open = true; const h = body.scrollHeight; body.style.height = '0px';
        requestAnimationFrame(() => { body.style.transition = 'height .4s cubic-bezier(.22,.8,.24,1)'; body.style.height = h + 'px'; });
        body.addEventListener('transitionend', () => { body.style.cssText = ''; }, { once: true });
      }
    });
  });

  /* Tryb "Uzasadnienie zmian" dla klienta */
  const wts = $$('[data-why-toggle]');
  const ustawWhy = (o) => { document.body.classList.toggle('why-on', o); wts.forEach(b => b.setAttribute('aria-pressed', String(o))); try { localStorage.setItem('spondylus-why', o ? '1' : '0'); } catch (e) {} };
  if (wts.length) {
    wts.forEach(b => b.addEventListener('click', () => ustawWhy(!document.body.classList.contains('why-on'))));
    try { if (localStorage.getItem('spondylus-why') === '1') ustawWhy(true); } catch (e) {}
  }
  /* K2: element prototypu chowa się przy przewijaniu w dół, wraca przy przewijaniu w górę */
  const dock = $('#proto-dock');
  if (dock) {
    let ostatni = window.scrollY, tik = false;
    window.addEventListener('scroll', () => {
      if (tik) return; tik = true;
      requestAnimationFrame(() => {
        const y = window.scrollY, dol = y > ostatni + 4, gora = y < ostatni - 4;
        const koniec = window.innerHeight + y >= document.documentElement.scrollHeight - 40;
        if (dol && y > 200 && !koniec) dock.classList.add('is-ukryty');
        else if (gora || y <= 200 || koniec) dock.classList.remove('is-ukryty');
        if (dol || gora) ostatni = y; tik = false;
      });
    }, { passive: true });
  }
})();
