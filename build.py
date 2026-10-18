#!/usr/bin/env python3
"""Składa strony prototypu z treści w src/pages/*.html i wspólnych części (nagłówek, stopka, okno rejestracji).

Każda strona w src/pages zaczyna się od komentarzy z metadanymi:
<!-- title: ... -->
<!-- desc: ... -->
<!-- nav: home | oferta | kadra | blog | kontakt -->
"""
import pathlib
import os
import re

ROOT = pathlib.Path(__file__).parent
WERSJA = str(int(max((ROOT / "assets/css/style.css").stat().st_mtime, (ROOT / "assets/js/main.js").stat().st_mtime)))
SRC = ROOT / "src" / "pages"

ICONS = {
    "wozek": '<path d="M4.5 3.5h2.25l1.25 8h6.5"/><path d="M7.5 7.5h5"/><path d="M14.5 11.5l2 5h3"/><circle cx="10" cy="16.5" r="4.5"/><circle cx="10" cy="16.5" r="1"/><circle cx="18.5" cy="20" r="1.3"/>',
    "phone": '<path d="M5 4h3l2 5-2.5 1.5a11 11 0 0 0 6 6L15 14l5 2v3a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
    "pin": '<path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
    "calendar": '<rect x="3.5" y="5" width="17" height="15.5" rx="3"/><path d="M8 3v4M16 3v4M3.5 10h17"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "arrow-left": '<path d="M19 12H5M11 6l-6 6 6 6"/>',
    "chev": '<path d="m6 9 6 6 6-6"/>',
    "chev-right": '<path d="m9 6 6 6-6 6"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h10"/>',
    "close": '<path d="M6 6l12 12M18 6 6 18"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="3"/><path d="m4 7 8 6 8-6"/>',
    "clock": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
    "check": '<path d="m5 12.5 4.5 4.5L19 7.5"/>',
    "shield": '<path d="M12 3 4.5 6v5.5c0 4.6 3.2 8.4 7.5 9.5 4.3-1.1 7.5-4.9 7.5-9.5V6z"/><path d="m8.5 12 2.5 2.5 4.5-5"/>',
    "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><path d="M16 4.6a3.5 3.5 0 0 1 0 6.8M18 14.2a6.5 6.5 0 0 1 3.5 5.8"/>',
    "spine": '<rect x="8" y="2.5" width="8" height="3.5" rx="1.6"/><rect x="7" y="8" width="10" height="3.5" rx="1.6"/><rect x="7.5" y="13.5" width="9" height="3.5" rx="1.6"/><rect x="8.5" y="19" width="7" height="2.8" rx="1.4"/>',
    "foot": '<path d="M8.5 21c-2.4 0-3.5-1.7-3.5-4 0-3 2-4.5 2-8 0-2.5 1.5-4 3.5-4S14 6.6 14 9c0 3.5-1 4.5-1 7.5 0 2.5-1.6 4.5-4.5 4.5z"/><circle cx="16.5" cy="5" r="1.3"/><circle cx="19" cy="7.8" r="1.1"/><circle cx="19.8" cy="11" r="1"/>',
    "run": '<circle cx="14.5" cy="4.5" r="2"/><path d="M8 21l2.5-5.5 3 2.5V22M6 11.5l3-3.5 4.5.5 2.5 3.5 3 1M10.5 15.5 13 9"/>',
    "scan": '<path d="M4 8V5.5A1.5 1.5 0 0 1 5.5 4H8M16 4h2.5A1.5 1.5 0 0 1 20 5.5V8M20 16v2.5a1.5 1.5 0 0 1-1.5 1.5H16M8 20H5.5A1.5 1.5 0 0 1 4 18.5V16"/><path d="M12 7v10M9 9.5h6M9.5 14.5h5"/>',
    "leaf": '<path d="M5 19c0-8 5-13 15-14-1 10-6 15-14 15"/><path d="M5 19c3-4 6-7 10-9"/>',
    "sparkle": '<path d="M12 3.5 13.8 10 20.5 12l-6.7 2L12 20.5 10.2 14 3.5 12l6.7-2z"/><path d="M19 3v3M17.5 4.5h3"/>',
    "crutch": '<path d="M9 3h6M12 3v6M8.5 9h7M12 9v12M10 15h4"/>',
    "cart": '<path d="M3 4h2.5l2.3 11h10l2-8H7"/><circle cx="9.5" cy="19.5" r="1.5"/><circle cx="17" cy="19.5" r="1.5"/>',
    "stethoscope": '<path d="M6 3v6a4 4 0 0 0 8 0V3"/><path d="M10 13v2.5a5 5 0 0 0 10 0V13"/><circle cx="20" cy="11" r="2"/>',
    "child": '<circle cx="12" cy="5" r="2.5"/><path d="M8 11h8M12 9v6M9.5 21l2.5-6 2.5 6"/>',
    "home": '<path d="M4 11 12 4l8 7v9H4z"/><path d="M10 20v-5h4v5"/>',
    "star": '<path d="m12 4 2.4 5 5.4.6-4 3.8 1 5.4L12 16.3 7.2 18.8l1-5.4-4-3.8 5.4-.6z"/>',
    "nail": '<rect x="7" y="3.5" width="10" height="17" rx="5"/><path d="M9.5 9h5"/>',
    "drop": '<path d="M12 3.5s6 6.4 6 10.5a6 6 0 0 1-12 0C6 9.9 12 3.5 12 3.5z"/>',
    "map": '<path d="m3.5 6.5 5.5-2 6 2 5.5-2v13l-5.5 2-6-2-5.5 2z"/><path d="M9 4.5v13M15 6.5v13"/>',
    "a11y": '<circle cx="12" cy="4.5" r="1.8"/><path d="M4.5 8.5 12 10l7.5-1.5M12 10v4.5M12 14.5 9 21M12 14.5l3 6.5"/>',
    "text": '<path d="M4 7V5h11v2M9.5 5v14M7 19h5"/><path d="M14 12v-1.5h6V12M17 10.5V19M15.5 19h3"/>',
    "contrast": '<circle cx="12" cy="12" r="8.5"/><path d="M12 3.5a8.5 8.5 0 0 1 0 17z" fill="currentColor" stroke="none"/>',
    "link": '<path d="M9.5 6.5H7a3.5 3.5 0 0 0 0 7h2.5M14.5 6.5H17a3.5 3.5 0 0 1 0 7h-2.5M8.5 10h7M4 19h16"/>',
    "pause": '<circle cx="12" cy="12" r="8.5"/><path d="M10 9v6M14 9v6"/>',
    "spacing": '<path d="M11 6h9M11 12h9M11 18h9M5.5 4v16M3.5 6.5l2-2.5 2 2.5M3.5 17.5l2 2.5 2-2.5"/>',
    "font": '<path d="M2.5 19 7.5 5l5 14M4.3 14h6.4M20.5 11.5V19"/><circle cx="17.3" cy="15.8" r="3.2"/>',
    "cursor": '<path d="M5.5 3.5 19 11.2l-6.1 1.7 3.2 6.6-2.8 1.3-3.2-6.6-4.6 4z" fill="currentColor" fill-opacity=".18"/>',
    "fb": '<path d="M14 21v-7.5h2.6l.4-3H14V8.7c0-.9.3-1.5 1.6-1.5H17V4.5a19 19 0 0 0-2.3-.1c-2.3 0-3.7 1.4-3.7 3.9v2.2H8.5v3H11V21"/>',
}


IKONA_OBSZARU = {"spine": "rehabilitacja", "scan": "diagnostyka", "run": "sport", "stethoscope": "lekarze", "leaf": "dietetyka", "sparkle": "estetyka", "crutch": "zaopatrzenie"}


def DEMO(h):
    return "" if h != "#" else ' data-demo="1" aria-disabled="true" title="Podstrona w przygotowaniu"'


def icon(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


def why(nr, tytul, problem, rozwiazanie, efekt):
    """Notatka trybu „Uzasadnienie” dla klienta: problem obecnej strony, rozwiązanie, efekt."""
    return (f'<aside class="why-note" aria-label="Uzasadnienie sekcji"><b><i>{nr}</i>{tytul}</b><dl>'
            f'<div><dt>Obecnie</dt><dd>{problem}</dd></div>'
            f'<div><dt>Propozycja</dt><dd>{rozwiazanie}</dd></div>'
            f'<div><dt>Po co</dt><dd>{efekt}</dd></div></dl></aside>')


OBSZARY = [
    ("#", "spine", "Rehabilitacja", "Ortopedyczna, pooperacyjna i neurologiczna"),
    ("#", "scan", "Diagnostyka wad postawy", "Postawa, stopy i diagnostyka sportowa"),
    ("#", "run", "Medycyna sportowa", "Kontuzje i powrót do treningu"),
    ("#", "stethoscope", "Konsultacje lekarskie", "Ortopeda, neurolog, neurochirurg"),
    ("#", "leaf", "Dietetyka", "Kliniczna i sportowa, wsparcie terapii"),
    ("#", "sparkle", "Medycyna estetyczna", "Zabiegi pod opieką zespołu medycznego"),
    ("zaopatrzenie.html", "crutch", "Zaopatrzenie medyczne", "Wkładki, obuwie i sprzęt, także z NFZ"),
]


def header(nav):
    def cur(key):
        return ' aria-current="page"' if nav == key else ""

    mega_items = "".join(
        f'<a class="mega__item" href="{h}"{DEMO(h)}><img class="mega__ilu" src="assets/img/ilu/kolo-{IKONA_OBSZARU[i]}.webp" alt="" width="256" height="256" loading="lazy"><div><b>{t}</b><span>{d}</span></div></a>'
        for h, i, t, d in OBSZARY
    )
    return f'''
<a class="sr-only" href="#tresc">Przejdź do treści</a>
<div class="topbar">
  <div class="wrap">
    <div class="topbar__places">
      <span>{icon("pin")}Szczecin, al. Jana Pawła II 36</span>
      <span>{icon("pin")}Szczecin Pogodno, ul. Unii Lubelskiej 2B</span>
      <span>{icon("pin")}Koszalin, ul. Jana Pawła II 21</span>
    </div>
    <div class="topbar__right">
      <div>Jedna infolinia dla wszystkich placówek: <a href="tel:+48665035035">665 035 035</a></div>
      <div class="topbar__a11y" role="group" aria-label="Wielkość tekstu">
        <span aria-hidden="true">Tekst</span>
        <button type="button" aria-pressed="true" data-a11y-size="0" aria-label="A, tekst standardowy">A</button>
        <button type="button" aria-pressed="false" data-a11y-size="1" aria-label="A+, tekst większy">A+</button>
        <button type="button" aria-pressed="false" data-a11y-size="2" aria-label="A++, tekst największy">A++</button>
      </div>
    </div>
  </div>
</div>
<header class="header" id="header">
  <div class="wrap">
    <a class="header__logo" href="index.html" aria-label="Spondylus, strona główna"><img src="assets/img/logo.png" alt="Spondylus" width="312" height="97"></a>
    <nav class="nav" aria-label="Menu główne">
      <button type="button" aria-expanded="false" aria-controls="mega" data-mega{' class="is-current"' if nav == "oferta" else ""}>Oferta {icon("chev")}</button>
      <a href="index.html#pierwsza-wizyta">Pierwsza wizyta</a>
      <a href="kadra.html"{cur("kadra")}>Nasza kadra</a>
      <a href="zaopatrzenie.html"{cur("nfz")}>Refundacja NFZ</a>
      <a href="o-nas.html"{cur("onas")}>O nas</a>
      <a href="kontakt.html"{cur("kontakt")}>Kontakt</a>
    </nav>
    <div class="header__actions">
      <a class="header__phone" href="tel:+48665035035"><small>Infolinia</small>665 035 035</a>
      <button class="btn btn--primary" type="button" data-book>{icon("calendar")}Umów wizytę</button>
      <button class="burger" type="button" aria-label="Otwórz menu" data-drawer-open>{icon("menu")}</button>
    </div>
  </div>
  <div class="mega" id="mega">
    <div class="wrap">
      {mega_items}
      <div class="mega__aside">
        <b>Nie wiesz, do kogo się zapisać?</b>
        <p>Rejestracja dobierze specjalistę i najbliższy termin.</p>
        <a class="btn btn--primary btn--sm" href="tel:+48665035035">{icon("phone")}665 035 035</a>
      </div>
    </div>
  </div>
</header>
<div class="drawer" id="drawer" aria-hidden="true">
  <div class="drawer__bg" data-drawer-close></div>
  <div class="drawer__panel" role="dialog" aria-modal="true" aria-label="Menu">
    <div class="drawer__top"><a class="drawer__logo" href="index.html"><img src="assets/img/logo.png" alt="Spondylus, strona główna" width="312" height="97"></a><button class="burger burger--zamknij" type="button" aria-label="Zamknij menu" data-drawer-close>{icon("close")}</button></div>
    <div class="drawer__tresc">
      <div class="drawer__group">W czym pomagamy</div>
      <div class="drawer__areas">{"".join(f'<a href="{h}"{"" if h != "#" else " data-demo=\"1\""}><img src="assets/img/ilu/kolo-{IKONA_OBSZARU[i]}.webp" alt="" width="256" height="256" loading="lazy"><span>{t}</span></a>' for h, i, t, d in OBSZARY)}</div>
      <nav class="drawer__nav" aria-label="Menu na telefonie">
        <a class="d-link" href="index.html#pierwsza-wizyta">Pierwsza wizyta {icon("chev-right")}</a>
        <a class="d-link" href="kadra.html">Nasza kadra {icon("chev-right")}</a>
        <a class="d-link" href="zaopatrzenie.html">Refundacja NFZ {icon("chev-right")}</a>
        <a class="d-link" href="index.html#opinie">Opinie pacjentów {icon("chev-right")}</a>
        <a class="d-link" href="o-nas.html">O nas {icon("chev-right")}</a>
        <a class="d-link" href="kontakt.html">Kontakt i placówki {icon("chev-right")}</a>
      </nav>
      <button class="why-toggle why-toggle--menu" type="button" aria-pressed="false" data-why-toggle><span>Uzasadnienie zmian (prototyp)</span><span class="why-toggle__sw" aria-hidden="true"></span></button>
      <p class="drawer__info">Infolinia dla wszystkich placówek, pon.-pt.: Szczecin, centrum i Koszalin 9:00-18:00, Pogodno 8:00-19:00.</p>
    </div>
    <div class="drawer__akcje">
      <button class="btn btn--primary" type="button" data-book>{icon("calendar")}Umów wizytę</button>
      <a class="btn btn--ghost" href="tel:+48665035035">{icon("phone")}665 035 035</a>
    </div>
  </div>
</div>
'''


def footer():
    return f'''
<footer class="footer">
  <div class="wrap">
    <div class="footer__grid">
      <div class="footer__marka">
        <span class="footer__logo"><img src="assets/img/logo.png" alt="Spondylus" width="312" height="97"></span>
        <p>Centrum medyczne w Szczecinie i Koszalinie. Rehabilitacja, diagnostyka i zaopatrzenie medyczne od 1989 roku.</p>
        <div class="footer__kontakt">
          <span class="footer__etykieta">Infolinia dla wszystkich placówek</span>
          <a class="footer__phone" href="tel:+48665035035">665 035 035</a>
          <a class="footer__mail" href="mailto:doktor@spondylus.pl">doktor@spondylus.pl</a>
        </div>
        <button class="btn btn--primary btn--sm" type="button" data-book>{icon("calendar")}Umów wizytę</button>
      </div>
      <div>
        <h2 class="f-title">Oferta</h2>
        <ul>{"".join(f'<li><a href="{h}"{"" if h != "#" else " data-demo=\"1\""}>{t}</a></li>' for h, i, t, d in OBSZARY)}</ul>
      </div>
      <div>
        <h2 class="f-title">Dla pacjenta</h2>
        <ul>
          <li><a href="index.html#pierwsza-wizyta">Pierwsza wizyta</a></li>
          <li><a href="kadra.html">Nasza kadra</a></li>
          <li><a href="zaopatrzenie.html">Refundacja NFZ</a></li>
          <li><a href="index.html#opinie">Opinie pacjentów</a></li>
          <li><a href="o-nas.html">O nas</a></li>
          <li><a href="#" data-demo="1">Poradniki</a></li>
          <li><a href="#" data-demo="1">Regulamin rezerwacji</a></li>
        </ul>
      </div>
      <div>
        <h2 class="f-title">Placówki</h2>
        <ul class="footer__placowki">
          <li><b>Szczecin, centrum</b><span class="otwarte" data-dni="1-5" data-od="9" data-do="18" hidden></span><span>al. Jana Pawła II 36</span><span>pon.-pt. 9:00-18:00, wew. 1</span><a href="https://www.google.com/maps/dir/?api=1&amp;destination=al.+Jana+Pawła+II+36+Szczecin" target="_blank" rel="noopener">Dojazd</a></li>
          <li><b>Szczecin, Pogodno</b><span class="otwarte" data-dni="1-5" data-od="8" data-do="19" hidden></span><span>ul. Unii Lubelskiej 2B</span><span>pon.-pt. 8:00-19:00, wew. 2</span><a href="https://www.google.com/maps/dir/?api=1&amp;destination=ul.+Unii+Lubelskiej+2B+Szczecin" target="_blank" rel="noopener">Dojazd</a></li>
          <li><b>Koszalin</b><span class="otwarte" data-dni="1-5" data-od="9" data-do="18" hidden></span><span>ul. Jana Pawła II 21</span><span>pon.-pt. 9:00-18:00, wew. 4</span><a href="https://www.google.com/maps/dir/?api=1&amp;destination=ul.+Jana+Pawła+II+21+Koszalin" target="_blank" rel="noopener">Dojazd</a></li>
        </ul>
      </div>
    </div>
    <div class="footer__nfz"><img src="assets/img/nfz.png" alt="Narodowy Fundusz Zdrowia" width="142" height="57"><span>Mamy umowę z NFZ na zaopatrzenie w wyroby medyczne: wózki, wkładki, obuwie i sprzęt na zlecenie.</span></div>
    <div class="footer__bottom">
      <span>© 2026 Spondylus Wojciech Wetoszka sp.k., <span class="nowrap">NIP 852-182-32-11</span></span>
      <span class="footer__linki"><a href="#" data-demo="1">Polityka prywatności i cookies</a><a href="#" data-demo="1">Deklaracja dostępności</a><a class="footer__fb" href="https://www.facebook.com/doktor.spondylus/" target="_blank" rel="noopener" aria-label="Spondylus na Facebooku">{icon("fb")}</a></span>
    </div>
  </div>
</footer>
<div class="booking" id="booking" aria-hidden="true">
  <div class="booking__backdrop" data-book-close></div>
  <div class="booking__box" role="dialog" aria-modal="true" aria-labelledby="booking-title">
    <button class="booking__close" type="button" aria-label="Zamknij" data-book-close>{icon("close")}</button>
    <h2 id="booking-title">Umów wizytę</h2>
    <div class="booking__steps" aria-hidden="true"><i class="is-done"></i><i></i><i></i></div>
    <div data-step="1">
      <p style="margin-bottom:16px">Wybierz placówkę. Pokażemy kalendarz wolnych terminów tej placówki.</p>
      <div class="options">
        <button class="option" type="button" data-place="szczecin-jp">{icon("pin")}<div><b>Szczecin, al. Jana Pawła II 36</b><span>Centrum Medyczne, specjaliści</span></div>{icon("chev-right", "chev")}</button>
        <button class="option" type="button" data-place="szczecin-ul">{icon("pin")}<div><b>Szczecin Pogodno, ul. Unii Lubelskiej 2B</b><span>Centrum Medyczne, specjaliści</span></div>{icon("chev-right", "chev")}</button>
        <button class="option" type="button" data-place="koszalin">{icon("pin")}<div><b>Koszalin, ul. Jana Pawła II 21</b><span>Centrum Medyczne, specjaliści i usługi</span></div>{icon("chev-right", "chev")}</button>
      </div>
    </div>
    <div data-step="2" hidden>
      <button class="booking__back" type="button" data-back="1">{icon("arrow-left")}Zmień placówkę</button>
      <p style="margin:10px 0 16px">Koszalin: czego szukasz?</p>
      <div class="options">
        <button class="option" type="button" data-place="koszalin-spec">{icon("stethoscope")}<div><b>Wizyta u specjalisty</b><span>Fizjoterapia, konsultacje lekarskie</span></div>{icon("chev-right", "chev")}</button>
        <button class="option" type="button" data-place="koszalin-uslugi">{icon("sparkle")}<div><b>Usługa lub zabieg</b><span>Zabiegi i usługi dostępne w placówce</span></div>{icon("chev-right", "chev")}</button>
      </div>
    </div>
    <div data-step="3" hidden>
      <button class="booking__back" type="button" data-back="1">{icon("arrow-left")}Zmień placówkę</button>
      <p style="margin:10px 0 14px" data-place-name></p>
      <div class="booking__widget"><iframe title="Kalendarz wolnych terminów" loading="lazy" data-widget></iframe></div>
      <div class="booking__alt">Wolisz telefonicznie? <a class="link-arrow" href="tel:+48665035035" data-place-tel>665 035 035</a></div>
    </div>
  </div>
</div>
<button class="a11y-btn" type="button" aria-label="Ustawienia dostępności" aria-expanded="false" aria-controls="a11y-panel" data-a11y-open>{ikona_dostepnosci()}</button>
<section class="a11y-panel" id="a11y-panel" role="dialog" aria-modal="false" aria-labelledby="a11y-title">
  <h2 id="a11y-title">Dostępność <button type="button" aria-label="Zamknij ustawienia dostępności" data-a11y-close>{icon("close")}</button></h2>
  <p>Dostosuj stronę do swoich potrzeb. Ustawienia zapamiętamy na tym urządzeniu.</p>
  <div class="a11y-size" role="group" aria-label="Wielkość tekstu">
    <button class="a11y-opt" type="button" aria-pressed="true" data-a11y-size="0">A</button>
    <button class="a11y-opt" type="button" aria-pressed="false" data-a11y-size="1" style="font-size:17px">A+</button>
    <button class="a11y-opt" type="button" aria-pressed="false" data-a11y-size="2" style="font-size:19px">A++</button>
  </div>
  <div class="a11y-grid">
    <button class="a11y-opt" type="button" aria-pressed="false" data-a11y="contrast">{icon("contrast")}Wysoki kontrast</button>
    <button class="a11y-opt" type="button" aria-pressed="false" data-a11y="links">{icon("link")}Podkreśl linki</button>
    <button class="a11y-opt" type="button" aria-pressed="false" data-a11y="spacing">{icon("spacing")}Większe odstępy</button>
    <button class="a11y-opt" type="button" aria-pressed="false" data-a11y="font">{icon("font")}Czytelna czcionka</button>
    <button class="a11y-opt" type="button" aria-pressed="false" data-a11y="still">{icon("pause")}Zatrzymaj animacje</button>
    <button class="a11y-opt" type="button" aria-pressed="false" data-a11y="cursor">{icon("cursor")}Duży kursor</button>
  </div>
  <button class="btn btn--ghost btn--sm a11y-reset" type="button" data-a11y-reset>Przywróć ustawienia domyślne</button>
</section>
<div class="proto-dock" id="proto-dock"><span class="proto-dock__label">Prototyp</span><button class="why-toggle" type="button" aria-pressed="false" data-why-toggle><span>Uzasadnienie zmian</span><span class="why-toggle__sw" aria-hidden="true"></span></button></div>
<div class="toast" role="status" aria-live="polite" id="toast"></div>
<script src="assets/js/main.js?v={WERSJA}" defer></script>
'''


def head(title, desc, body_cls=""):
    return f'''<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex">
<link rel="icon" href="assets/img/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Onest:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css?v={WERSJA}">
</head>
<body class="{body_cls}">'''


def przygotuj_zdjecia_objawow():
    """Zdjęcia z assets/src/objawy/ zamienia na WebP 768x512 w assets/img/objawy/."""
    src, dst = ROOT / "assets/src/objawy", ROOT / "assets/img/objawy"
    if not src.exists():
        return
    try:
        from PIL import Image
    except ImportError:
        print("Brak biblioteki Pillow: pip3 install pillow")
        return
    dst.mkdir(parents=True, exist_ok=True)
    for f in src.iterdir():
        if f.suffix.lower() not in (".png", ".jpg", ".jpeg", ".webp"):
            continue
        out = dst / (f.stem.lower() + ".webp")
        if out.exists() and out.stat().st_mtime >= f.stat().st_mtime:
            continue
        im = Image.open(f).convert("RGB")
        w, h = im.size
        cel = 3 / 2
        if w / h > cel:
            nw = int(h * cel); im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
        else:
            nh = int(w / cel); im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
        im.resize((768, 512), Image.LANCZOS).save(out, quality=80)
        print("zdjęcie:", out.name)


def przygotuj_ilustracje():
    """PNG z przezroczystym tłem z assets/src/ilustracje/ przycina do treści, wyrównuje margines i zapisuje jako WebP 256x256."""
    src, dst = ROOT / "assets/src/ilustracje", ROOT / "assets/img/ilu"
    if not src.exists():
        return
    try:
        from PIL import Image
    except ImportError:
        return
    dst.mkdir(parents=True, exist_ok=True)
    for f in src.iterdir():
        if f.suffix.lower() not in (".png", ".webp") or "podglad" in f.stem.lower():
            continue
        out = dst / (f.stem.lower() + ".webp")
        if out.exists() and out.stat().st_mtime >= f.stat().st_mtime:
            continue
        im = Image.open(f).convert("RGBA")
        bbox = im.getchannel("A").point(lambda a: 255 if a > 12 else 0).getbbox()
        if bbox:
            im = im.crop(bbox)
        if f.stem.lower().startswith("scena-"):
            # większe ilustracje sceniczne: zachowują proporcje, dłuższy bok 960 px
            m = int(max(im.size) * 0.06)
            plotno = Image.new("RGBA", (im.width + 2 * m, im.height + 2 * m), (0, 0, 0, 0))
            plotno.paste(im, (m, m), im)
            plotno.thumbnail((960, 960), Image.LANCZOS)
            plotno.save(out, quality=88)
            print("ilustracja:", out.name)
            continue
        bok = int(max(im.size) * 1.12)
        plotno = Image.new("RGBA", (bok, bok), (0, 0, 0, 0))
        plotno.paste(im, ((bok - im.width) // 2, (bok - im.height) // 2), im)
        plotno.resize((256, 256), Image.LANCZOS).save(out, quality=88)
        print("ilustracja:", out.name)


def ilu(m):
    """Ilustracja, jeśli plik już jest; w przeciwnym razie ikona zastępcza (albo nic)."""
    nazwa, ikona = m.group(1), m.group(2)
    plik = ROOT / f"assets/img/ilu/{nazwa}.webp"
    if plik.exists() and nazwa.startswith("scena-"):
        from PIL import Image
        w, h = Image.open(plik).size
        return f'<img class="ilu ilu--scena" src="assets/img/ilu/{nazwa}.webp" alt="" width="{w}" height="{h}" loading="lazy">'
    if plik.exists():
        return f'<img class="ilu" src="assets/img/ilu/{nazwa}.webp" alt="" width="256" height="256" loading="lazy">'
    if ikona.startswith("ilu-") and (ROOT / f"assets/img/ilu/{ikona[4:]}.webp").exists():
        return f'<img class="ilu" src="assets/img/ilu/{ikona[4:]}.webp" alt="" width="256" height="256" loading="lazy">'
    return "{{icon:%s}}" % ikona if ikona else ""


def przygotuj_portrety():
    """Portrety z assets/src/portrety/ zapisuje jako WebP 600x750 (4:5) w assets/img/portrety/."""
    src, dst = ROOT / "assets/src/portrety", ROOT / "assets/img/portrety"
    if not src.exists():
        return
    try:
        from PIL import Image
    except ImportError:
        return
    dst.mkdir(parents=True, exist_ok=True)
    for f in src.iterdir():
        if f.suffix.lower() not in (".png", ".jpg", ".jpeg", ".webp"):
            continue
        out = dst / (f.stem.lower() + ".webp")
        if out.exists() and out.stat().st_mtime >= f.stat().st_mtime:
            continue
        im = Image.open(f).convert("RGB")
        w, h = im.size
        cel = 4 / 5
        if w / h > cel:
            nw = int(h * cel); im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
        else:
            nh = int(w / cel); im = im.crop((0, 0, w, nh))
        im.resize((600, 750), Image.LANCZOS).save(out, quality=82)
        print("portret:", out.name)


def portret(m):
    """Portret w jednolitym szablonie, jeśli już jest; w przeciwnym razie obecne zdjęcie ze strony."""
    slug = m.group(1)
    nowy = ROOT / f"assets/img/portrety/{slug}.webp"
    src = f"assets/img/portrety/{slug}.webp" if nowy.exists() else f"assets/img/kadra-{slug}.webp"
    klasa = "is-szablon" if nowy.exists() else "is-stare"
    return f'<img class="{klasa}" src="{src}" alt="" loading="lazy" width="600" height="750">'


def ikona_dostepnosci():
    if (ROOT / "assets/img/ilu/dostepnosc.webp").exists():
        return '<img class="ilu" src="assets/img/ilu/dostepnosc.webp" alt="" width="256" height="256">'
    return icon("a11y")


def fotka(m):
    """Zdjęcie, jeśli plik już jest w projekcie; w przeciwnym razie ikona zastępcza."""
    sciezka, ikona = m.group(1), m.group(2)
    if os.path.exists(os.path.join(ROOT, sciezka)):
        return f'<span class="objaw__img"><img src="{sciezka}" alt="" loading="lazy" width="768" height="512"></span>'
    return "{{icon:%s}}" % ikona


def twarde_spacje(html):
    """D3: twarda spacja po jednoliterowych słowach (a, i, o, u, w, z), tylko w tekście między tagami."""
    czesci = re.split(r"(<script\b.*?</script>|<style\b.*?</style>|<[^>]+>)", html, flags=re.S | re.I)
    wzor = re.compile(r"(^|[\s(„])([aiouwzAIOUWZ]) (?=\S)")
    for i in range(0, len(czesci), 2):
        czesci[i] = wzor.sub(lambda m: m.group(1) + m.group(2) + "&nbsp;", czesci[i])
    return "".join(czesci)


def build():
    przygotuj_zdjecia_objawow()
    przygotuj_ilustracje()
    # przygotuj_portrety()  # portrety robi narzedzia/portrety.py (wycięcie tła, twarz bez zmian)
    for src in sorted(SRC.glob("*.html")):
        raw = src.read_text(encoding="utf-8")
        meta = dict(re.findall(r"<!--\s*(\w+):\s*(.*?)\s*-->", raw[:600]))
        body = re.sub(r"^(\s*<!--.*?-->\s*)+", "", raw, flags=re.S)
        body = re.sub(r"\{\{portret:([\w-]+)\}\}", portret, body)
        body = re.sub(r"\{\{ilu:([\w-]+)\|([\w-]*)\}\}", ilu, body)
        body = re.sub(r"\{\{fotka:([\w/.-]+)\|([\w-]+)\}\}", fotka, body)
        body = re.sub(r"\{\{icon:([\w-]+)(?::([\w-]+))?\}\}", lambda m: icon(m.group(1), m.group(2) or ""), body)
        body = body.replace('href="#" data-demo="1"', 'href="#" data-demo="1" aria-disabled="true" title="Podstrona w przygotowaniu"')
        body = re.sub(
            r"\{\{why:(\d+)\|(.*?)\|(.*?)\|(.*?)\|(.*?)\}\}",
            lambda m: why(*m.groups()), body, flags=re.S)
        html = head(meta["title"], meta["desc"], meta.get("body", "")) + header(meta.get("nav", "")) + '<main id="tresc">' + body + "</main>" + footer() + "\n</body>\n</html>\n"
        html = twarde_spacje(html)
        html = re.sub(r'href="#" data-demo="1"(?! aria-disabled)', 'href="#" data-demo="1" aria-disabled="true" title="Podstrona w przygotowaniu"', html)
        (ROOT / src.name).write_text(html, encoding="utf-8")
        print("zbudowano", src.name)


if __name__ == "__main__":
    build()
