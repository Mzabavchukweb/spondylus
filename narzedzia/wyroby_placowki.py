#!/usr/bin/env python3
"""Generuje źródła podstron grup wyrobów medycznych i placówek (src/pages/*.html).

Dane wyłącznie z istniejących źródeł:
- opisy grup: obecne strony /zaopatrzenie-medyczne/ i /refundacja/ (spondylus.pl),
- marki i przykładowe produkty: kategorie spondylus-sklep.pl (narzedzia/dane/sklep-produkty-2026-11-01.json, pierwsza strona kategorii, pobrane 1.11.2026),
- placówki: adresy, godziny i numery wewnętrzne ze stopki i kontaktu, Jana Pawła II 39 i strefa zaopatrzenia w Koszalinie z tekstu „O nas”,
- specjaliści placówki: „Miejsce przyjęć” z profili (tylko profile podlinkowane w kadrze).
Punkty niepotwierdzone (ul. Ściegiennego 7, Przychodnia Portowa) celowo pominięte do odpowiedzi klienta.

Uruchom po zmianie danych: python3 narzedzia/wyroby_placowki.py && python3 build.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src/pages"
SKLEP = json.loads((ROOT / "narzedzia/dane/sklep-produkty-2026-11-01.json").read_text(encoding="utf-8"))

TEL = '<a class="btn btn--primary" href="tel:+48665035035">{{icon:phone}}665 035 035</a>'


def sklep(klucz):
    k = SKLEP[klucz]
    return k["nazwa"].split(" (")[0], k["url"], k["produkty_strona1"]


# slug, tytuł strony, H1, lead, ikona, opis (zdania z obecnej strony), czy w wykazie refundacji NFZ (strona /refundacja/),
# kategorie sklepu, marki (z nazw produktów w sklepie), przykładowe produkty, tytuł i opis meta
GRUPY = [
    dict(slug="wkladki-ortopedyczne", nazwa="Wkładki ortopedyczne", ikona="wkladka",
         h1="Wkładki ortopedyczne w Szczecinie i Koszalinie",
         lead="Indywidualne, wykonywane na zamówienie, w tym dla diabetyków. Doradzimy i pomożemy dobrać rozwiązanie.",
         nfz="Wkładki ortopedyczne", kat=["wkladki-ortopedyczne"], marki=["KAPS"],
         przyklady=["KAPS Wkładki pełne MASTER", "KAPS Wkładki z pelotą ALLEVIA", "KAPS Półwkładki z pelotą RESTMED", "KAPS Podpiętki ostrogi HEELMED"],
         title="Wkładki ortopedyczne Szczecin i Koszalin | Spondylus",
         desc="Wkładki ortopedyczne indywidualne i na zamówienie, także dla diabetyków i z refundacją NFZ. Spondylus Szczecin i Koszalin, infolinia 665 035 035."),
    dict(slug="obuwie-zdrowotne", nazwa="Obuwie zdrowotne", ikona="obuwie",
         h1="Obuwie zdrowotne i ortopedyczne",
         lead="Obuwie profilaktyczne i zindywidualizowane, także z refundacją NFZ. Doradzimy przy wyborze.",
         nfz="Obuwie ortopedyczne", kat=["obuwie"], marki=["Aurelka"],
         przyklady=[],
         title="Obuwie ortopedyczne i zdrowotne Szczecin | Spondylus",
         desc="Obuwie profilaktyczne i zindywidualizowane, także obuwie ortopedyczne z refundacją NFZ. Spondylus Szczecin i Koszalin, infolinia 665 035 035."),
    dict(slug="ortezy-i-stabilizatory", nazwa="Ortezy i stabilizatory", ikona="sprzet",
         h1="Ortezy i stabilizatory",
         lead="Produkty ortopedyczne dobierane do problemu i rozmiaru. Pomożemy wybrać właściwy model.",
         nfz="Ortezy i aparaty ortopedyczne", kat=["ortezy-i-stabilizatory"], marki=["ANTAR"],
         przyklady=["ANTAR orteza kręgosłupa lędźwiowo-krzyżowa", "ANTAR orteza na ramię i bark typu Dessault", "ANTAR długi bioceramiczny tutor nadgarstka z taśmą"],
         title="Ortezy i stabilizatory Szczecin i Koszalin | Spondylus",
         desc="Ortezy i stabilizatory dobierane do problemu i rozmiaru, także z refundacją NFZ na zlecenie. Spondylus Szczecin i Koszalin, infolinia 665 035 035."),
    dict(slug="wozki-inwalidzkie", nazwa="Wózki inwalidzkie, balkoniki i kule", ikona="wozek",
         h1="Wózki inwalidzkie, balkoniki i kule",
         lead="Wózki i sprzęt do domu, z doradztwem w doborze rozwiązań. Pomagamy też w formalnościach refundacji NFZ.",
         nfz="Wózki inwalidzkie, laski i kule, balkoniki", kat=["wozki-inwalidzkie", "balkoniki", "kule-ortopedyczne", "podnosniki"],
         marki=["AKCESMED", "ARMEDICAL", "VERMEIREN", "ASTON", "MIKIRAD", "LEVICARE"],
         przyklady=["AKCESMED Wózek inwalidzki AURORA", "VERMEIREN Balkonik 201 DELTA", "ASTON Kula łokciowa EVOLUTION", "LEVICARE Podnośnik jezdny 160/190"],
         title="Wózki inwalidzkie, balkoniki i kule z NFZ | Spondylus",
         desc="Wózki inwalidzkie, balkoniki, kule i podnośniki z doradztwem w doborze. Pomagamy w refundacji NFZ. Spondylus Szczecin i Koszalin, tel. 665 035 035."),
    dict(slug="wyroby-uciskowe", nazwa="Wyroby uciskowe", ikona="kompresja",
         h1="Wyroby uciskowe i przeciwżylakowe",
         lead="Produkty kompresyjne: podkolanówki, pończochy i inne wyroby uciskowe.",
         nfz="", kat=["wyroby-przeciwzylakowe"], marki=["ARIES (AVICENUM)"],
         przyklady=["ARIES podkolanówki AVICENUM 70 TRAVEL", "ARIES pończochy samonośne z koronką AVICENUM 140", "ARIES pończochy z lamówką AVICENUM 360 FINE"],
         title="Wyroby uciskowe i przeciwżylakowe Szczecin | Spondylus",
         desc="Produkty kompresyjne: podkolanówki i pończochy uciskowe AVICENUM. Spondylus Szczecin i Koszalin, sklep internetowy i infolinia 665 035 035."),
    dict(slug="zaopatrzenie-stomijne", nazwa="Zaopatrzenie stomijne", ikona="ikona-plaster",
         h1="Zaopatrzenie stomijne",
         lead="Sprzęt stomijny i akcesoria do pielęgnacji stomii. Sprzęt stomijny może refundować NFZ.",
         nfz="Sprzęt stomijny", kat=["coloplast"], marki=["Coloplast"],
         przyklady=["COLOPLAST Brava pasta stomijna", "COLOPLAST Brava krem przeciwodparzeniowy", "COLOPLAST Brava pierścień uszczelniający", "COLOPLAST Brava pasek mocujący"],
         title="Zaopatrzenie stomijne Coloplast Szczecin | Spondylus",
         desc="Zaopatrzenie stomijne i akcesoria Coloplast Brava. Sprzęt stomijny może refundować NFZ. Spondylus Szczecin i Koszalin, infolinia 665 035 035."),
    dict(slug="lozka-rehabilitacyjne", nazwa="Łóżka rehabilitacyjne i sprzęt do domu", ikona="program-dom",
         h1="Łóżka rehabilitacyjne i sprzęt do domu",
         lead="Ciężki sprzęt rehabilitacyjny z doradztwem w doborze rozwiązań: łóżka medyczne i poduszki ortopedyczne.",
         nfz="", kat=["lozka-rehabilitacyjne", "poduszki-ortopedyczne"], marki=["REHABED", "GAMAREHA", "ARMEDICAL", "DR SAPPORO"],
         przyklady=["REHABED Łóżko medyczne ARIES MED", "GAMAREHA Łóżko medyczne TWIST", "ARMEDICAL poduszka do siedzenia EXCLUSIVE SEAT"],
         title="Łóżka rehabilitacyjne i sprzęt do domu | Spondylus",
         desc="Łóżka rehabilitacyjne i medyczne, poduszki ortopedyczne i sprzęt do domu, z doradztwem w doborze. Spondylus Szczecin i Koszalin, tel. 665 035 035."),
    dict(slug="produkty-chlonne", nazwa="Produkty chłonne i pielęgnacyjne", ikona="ikona-pakiet",
         h1="Produkty chłonne i pielęgnacyjne",
         lead="Pieluchomajtki, wkłady i podkłady oraz kosmetyki do pielęgnacji skóry. Pieluchomajtki może refundować NFZ.",
         nfz="Pieluchomajtki", kat=["tena"], marki=["Seni"],
         przyklady=["Pieluchomajtki Super Seni", "Pianka Seni Care", "Olejek pielęgnacyjny Seni Care", "Chusteczki nawilżające Seni Care"],
         title="Pieluchomajtki i produkty chłonne z NFZ | Spondylus",
         desc="Pieluchomajtki, wkłady i podkłady oraz kosmetyki pielęgnacyjne Seni. Pieluchomajtki może refundować NFZ. Spondylus Szczecin i Koszalin."),
]

# placówki: dane ze stopki, kontaktu i „O nas”; specjaliści z „Miejsce przyjęć” w profilach
PLACOWKI = [
    dict(slug="placowka-szczecin-centrum", nazwa="Szczecin, centrum", pelna="Spondylus Szczecin, centrum", ulica="al. Jana Pawła II 36",
         kod="70-453 Szczecin", godz="pon. do pt. 9:00 do 18:00", od=9, do=18, wew="1", book=[("szczecin-jp", "Umów wizytę")],
         mapa="mapa-szczecin-centrum.webp", cel="al.+Jana+Pawła+II+36+Szczecin",
         opis="Centrum Medyczne Spondylus w centrum Szczecina.",
         kadra=[("magdalena-salabon", "Magdalena Sałabon", "fizjoterapeutka dzieci")],
         title="Spondylus Szczecin, al. Jana Pawła II 36 | Placówka",
         desc="Spondylus w centrum Szczecina, al. Jana Pawła II 36: godziny pon. do pt. 9:00 do 18:00, infolinia 665 035 035 wew. 1, dojazd i rejestracja online."),
    dict(slug="placowka-szczecin-pogodno", nazwa="Szczecin, Pogodno", pelna="Spondylus Szczecin Pogodno", ulica="ul. Unii Lubelskiej 2B",
         kod="71-252 Szczecin", godz="pon. do pt. 8:00 do 19:00", od=8, do=19, wew="2", book=[("szczecin-ul", "Umów wizytę")],
         mapa="mapa-szczecin-pogodno.webp", cel="ul.+Unii+Lubelskiej+2B+Szczecin",
         opis="Placówka Spondylus na Pogodnie. Przyjmują tu lekarze specjaliści, fizjoterapeuci i podolog.",
         kadra=[("adam-kaminski", "Adam Kamiński", "ortopeda"), ("piotr-salapa", "Piotr Sałapa", "neurochirurg"),
                ("tomasz-dudzik", "Tomasz Dudzik", "neurolog"), ("tomasz-gnus", "Tomasz Gnus", "fizjoterapeuta"),
                ("tomasz-zdeb-fizjoterapeuta", "Tomasz Zdeb", "fizjoterapeuta"), ("gabriela-majorczyk", "Gabriela Majorczyk", "fizjoterapeutka"),
                ("marika-wachowiak-podolog", "Marika Wachowiak", "podolog")],
         title="Spondylus Szczecin Pogodno, ul. Unii Lubelskiej 2B",
         desc="Spondylus Pogodno, ul. Unii Lubelskiej 2B: ortopeda, neurochirurg, neurolog, fizjoterapia i podolog. Pon. do pt. 8:00 do 19:00, tel. 665 035 035 wew. 2."),
    dict(slug="placowka-koszalin", nazwa="Koszalin", pelna="Spondylus Koszalin", ulica="ul. Jana Pawła II 21",
         kod="75-452 Koszalin", godz="pon. do pt. 9:00 do 18:00", od=9, do=18, wew="4",
         book=[("koszalin", "Umów wizytę")],
         mapa="mapa-koszalin.webp", cel="ul.+Jana+Pawła+II+21+Koszalin",
         opis="Centrum Medyczne w Koszalinie łączy strefę zaopatrzenia medycznego i strefę gabinetową, w której realizowane są usługi medyczne.",
         kadra=[("rafal-perkowski", "Rafał Perkowski", "fizjoterapeuta"), ("olga-veremiienko", "Olga Veremiienko", "stylistka paznokci i brwi")],
         zaopatrzenie=True,
         title="Spondylus Koszalin, ul. Jana Pawła II 21 | Placówka",
         desc="Spondylus Koszalin, ul. Jana Pawła II 21: strefa zaopatrzenia medycznego i gabinety. Pon. do pt. 9:00 do 18:00, infolinia 665 035 035 wew. 4."),
]
# punkt bez własnej strony: z tekstu „O nas” i profilu W. Kujawskiej; godzin nie znamy
JP39 = dict(nazwa="Szczecin, Przychodnia Specjalistyczna", ulica="al. Jana Pawła II 39", kod="Szczecin", cel="al.+Jana+Pawła+II+39+Szczecin")


def okruszki(*kroki):
    return " > ".join(kroki)


def produkt(nazwa, marki):
    """„KAPS Wkładki pełne MASTER” -> („KAPS”, „Wkładki pełne MASTER”); marka z listy marek grupy."""
    for m in marki:
        rdzen = m.split(" (")[0]
        if nazwa.upper().startswith(rdzen.upper() + " "):
            return rdzen, nazwa[len(rdzen) + 1:]
        if rdzen.upper() in nazwa.upper():
            return rdzen, nazwa
    return "", nazwa


def strona_grupy(g):
    kat = [sklep(k) for k in g["kat"]]
    linki_kat = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{n}</a></li>' for n, u, _ in kat)
    marki = ", ".join(m for m in g["marki"])
    karty = []
    if g["nfz"]:
        karty.append(f'''<li>{{{{ilu:skierowanie|}}}}<h3>Refundacja NFZ</h3>
        <p>NFZ może refundować: {g["nfz"].lower()}. NFZ dopłaca do wysokości limitu, potrzebne jest zlecenie. Wykazy wyrobów i limity cen publikuje NFZ na stronie <a href="https://www.nfz.gov.pl" target="_blank" rel="noopener">nfz.gov.pl</a>.</p>
        <a class="zao-info__link" href="refundacja.html">Jak dostać sprzęt z refundacją {{{{icon:arrow}}}}</a></li>''')
    karty.append('''<li>{{ilu:ikona-pinezka|}}<h3>Dobór w placówce</h3>
        <p>W Koszalinie przy ul. Jana Pawła II 21 działa strefa zaopatrzenia medycznego. O dostępność konkretnego produktu i dobór zapytaj na infolinii 665 035 035.</p>
        <a class="zao-info__link" href="placowki.html">Adresy i godziny placówek {{icon:arrow}}</a></li>''')
    karty.append(f'''<li>{{{{ilu:ikona-pakiet|}}}}<h3>Sklep internetowy</h3>
        <p>Produkty z tej grupy kupisz też online w sklepie spondylus-sklep.pl. Marki, m.in.: {marki}.</p>
        <ul class="zao-info__kat" aria-label="Kategorie w sklepie">{linki_kat}</ul></li>''')
    url0 = kat[0][1]
    produkty = ""
    if g["przyklady"]:
        kafle = "".join(
            f'<li><a href="{url0}" target="_blank" rel="noopener"><span>{m}</span><b>{n}</b><em>W sklepie internetowym</em></a></li>'
            for m, n in (produkt(x, g["marki"]) for x in g["przyklady"]))
        produkty = f'''
<section class="section">
  <div class="wrap">
    <div class="head2">
      <h2>Przykładowe produkty</h2>
      <p>Wybrane produkty z kategorii w sklepie spondylus-sklep.pl. Pełna oferta jest w sklepie internetowym.</p>
    </div>
    <ul class="zao-produkty">{kafle}</ul>
  </div>
</section>
'''
    return f'''<!-- title: {g["title"]} -->
<!-- desc: {g["desc"]} -->
<!-- nav: wyroby -->
<!-- okruszki: {okruszki("Wyroby medyczne=/zaopatrzenie-medyczne/", g["nazwa"])} -->

<section class="page-hero">
  <div class="wrap">
    {{{{okruszki}}}}
    <div class="page-hero__grid page-hero__grid--produkt">
      <div>
        <h1>{g["h1"]}</h1>
        <p class="page-hero__lead">{g["lead"]}</p>
        <div class="page-hero__cta">{TEL}<a class="btn btn--ghost" href="{url0}" target="_blank" rel="noopener">Sklep internetowy</a></div>
      </div>
      <div class="page-hero__media page-hero__media--ilu page-hero__media--produkt" aria-hidden="true">{{{{ilu:{g["ikona"]}|}}}}</div>
    </div>
  </div>
</section>

<section class="section section--soft">
  <div class="wrap">
    <div class="head2">
      <h2>{"Refundacja, dobór i zakup" if g["nfz"] else "Dobór i zakup"}</h2>
      <p>Doradzimy przy wyborze. Zadzwoń na infolinię albo kup online.</p>
    </div>
    <ul class="zao-info zao-info--{len(karty)}">{"".join(karty)}</ul>
  </div>
</section>
{produkty}
<section style="padding-bottom:0">
  <div class="wrap">
    <div class="cta-band">
      <div><h2>Zapytaj o {g["nazwa"].split(",")[0].lower()}</h2><p>Infolinia dla wszystkich placówek w Szczecinie i Koszalinie.</p></div>
      <div class="cta-band__actions"><a class="btn btn--light" href="tel:+48665035035">{{{{icon:phone}}}}665 035 035</a><a class="btn btn--outline-light" href="https://spondylus-sklep.pl/" target="_blank" rel="noopener">Sklep internetowy</a></div>
    </div>
  </div>
</section>
'''


def karta(p, szczegoly=True):
    przyciski = "".join(f'<button class="btn btn--primary btn--sm" type="button" data-book="{k}">{t}</button>' for k, t in p["book"][:1])
    przyciski += "".join(f'<button class="btn btn--ghost btn--sm" type="button" data-book="{k}">{t}</button>' for k, t in p["book"][1:])
    link = f'<a class="place__wiecej" href="{p["slug"]}.html">Szczegóły placówki</a>' if szczegoly else ""
    return (f'<div class="place"><a class="map map--statyczna" href="https://www.google.com/maps/dir/?api=1&destination={p["cel"]}" target="_blank" rel="noopener" '
            f'aria-label="Mapa dojazdu: {p["ulica"]}, {p["kod"]}, otwiera Google Maps"><img src="assets/img/{p["mapa"]}" alt="" width="860" height="520" loading="lazy"></a>'
            f'<h3>{p["nazwa"]}</h3><span class="otwarte" data-dni="1-5" data-od="{p["od"]}" data-do="{p["do"]}" hidden></span>'
            f'<address>{p["ulica"]}<br>{p["kod"]}</address><div class="place__godz">{{{{icon:clock}}}}{p["godz"]}</div>'
            f'<div class="place__ext">{{{{icon:phone}}}}<a href="tel:+48665035035">665 035 035</a> wew. {p["wew"]}</div>'
            f'<div class="place__actions">{przyciski}<a class="btn btn--ghost btn--sm" href="https://www.google.com/maps/dir/?api=1&destination={p["cel"]}" target="_blank" rel="noopener">{{{{icon:map}}}}Nawiguj</a></div>{link}</div>')


def karta_jp39():
    return (f'<div class="place-pasek"><div><h3>{JP39["nazwa"]}</h3><address>{JP39["ulica"]}, {JP39["kod"]}</address></div>'
            f'<div class="place-pasek__akcje"><div class="place__ext">{{{{icon:phone}}}}<a href="tel:+48665035035">665 035 035</a></div>'
            f'<a class="btn btn--ghost btn--sm" href="https://www.google.com/maps/dir/?api=1&destination={JP39["cel"]}" target="_blank" rel="noopener">{{{{icon:map}}}}Nawiguj</a></div></div>')


def strona_placowki_hub():
    karty = "".join(karta(p) for p in PLACOWKI)
    return f"""<!-- title: Placówki Spondylus w Szczecinie i Koszalinie -->
<!-- desc: Placówki Spondylus: Szczecin al. Jana Pawła II 36 i 39, Pogodno ul. Unii Lubelskiej 2B, Koszalin ul. Jana Pawła II 21. Godziny, dojazd, infolinia 665 035 035. -->
<!-- nav: placowki -->
<!-- okruszki: Placówki -->

<section class="page-hero">
  <div class="wrap">
    {{{{okruszki}}}}
    <h1>Nasze placówki w Szczecinie i Koszalinie</h1>
    <p class="page-hero__lead">Wszystkie placówki łączy jedna infolinia 665 035 035. Po połączeniu wybierz numer wewnętrzny placówki.</p>
    <div class="page-hero__cta">{TEL}<a class="btn btn--ghost" href="rejestracja-online.html">Rejestracja online</a></div>
  </div>
</section>

<section class="section section--soft">
  <div class="wrap">
    <div class="places">{karty}</div>
    {karta_jp39()}
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="head2">
      <h2>Wyroby medyczne w placówkach</h2>
      <p>Centrum Medyczne w Koszalinie łączy strefę zaopatrzenia medycznego i strefę gabinetową. O dostępność konkretnego produktu w wybranej placówce zapytaj na infolinii.</p>
    </div>
    <ul class="linki-prog linki-prog--siatka">
      <li><a href="zaopatrzenie-medyczne.html">{{{{ilu:wozek|}}}}<b>Wyroby medyczne</b><span>Wkładki, obuwie, ortezy, wózki i sprzęt do domu, także z refundacją NFZ.</span></a></li>
      <li><a href="refundacja.html">{{{{ilu:skierowanie|}}}}<b>Refundacja NFZ</b><span>Jak zrealizować zlecenie na wyroby medyczne.</span></a></li>
    </ul>
  </div>
</section>
"""


KADRA_SRC = (SRC / "kadra.html").read_text(encoding="utf-8")


def karta_kadry(slug):
    """Karta specjalisty 1:1 z listy kadry (zdjęcie, rola, opis, tagi, rejestracja)."""
    i = KADRA_SRC.find(f'href="{slug}.html"')
    s = KADRA_SRC.rfind("<article", 0, i)
    e = KADRA_SRC.find("</article>", i) + len("</article>")
    return KADRA_SRC[s:e] if i != -1 else ""


def strona_placowki(p):
    przyciski = "".join(f'<button class="btn btn--primary" type="button" data-book="{k}">{{{{icon:calendar}}}}{t}</button>' for k, t in p["book"][:1])
    przyciski += "".join(f'<button class="btn btn--ghost" type="button" data-book="{k}">{t}</button>' for k, t in p["book"][1:])
    nawiguj = f'https://www.google.com/maps/dir/?api=1&destination={p["cel"]}'
    tlo = ["section section--soft", "section"]
    sekcje = []
    if p.get("zaopatrzenie"):
        grupy = "".join(f'<li><a href="{g["slug"]}.html">{{{{ilu:{g["ikona"]}|}}}}<b>{g["nazwa"]}</b><span>{g["lead"].split(".")[0]}.</span></a></li>' for g in GRUPY[:4])
        sekcje.append(f"""
  <div class="wrap">
    <div class="head2">
      <h2>Strefa zaopatrzenia medycznego</h2>
      <p>W tej placówce działa strefa zaopatrzenia medycznego. O dostępność konkretnego produktu zapytaj na infolinii, wew. {p["wew"]}.</p>
    </div>
    <ul class="zao-oferta zao-oferta--4 zao-oferta--linki">{grupy}</ul>
    <div class="sekcja-dalej"><a class="btn btn--ghost" href="zaopatrzenie-medyczne.html">Wszystkie wyroby medyczne {{{{icon:arrow}}}}</a></div>
  </div>""")
    kadra = "\n      ".join(karta_kadry(s) for s, _, _ in p["kadra"])
    sekcje.append(f"""
  <div class="wrap">
    <div class="head2">
      <h2>Kto przyjmuje w tej placówce</h2>
      <p>Specjaliści, którzy na swoich profilach podają tę placówkę jako miejsce przyjęć.</p>
    </div>
    <div class="team-grid spec-grid spec-grid--plac">
      {kadra}
    </div>
    <div class="sekcja-dalej"><a class="btn btn--ghost" href="kadra.html">Cały zespół Spondylus {{{{icon:arrow}}}}</a></div>
  </div>""")
    sekcje_html = "".join(f'\n<section class="{tlo[i % 2]}">{x}\n</section>\n' for i, x in enumerate(sekcje))
    return f"""<!-- title: {p["title"]} -->
<!-- desc: {p["desc"]} -->
<!-- nav: placowki -->
<!-- okruszki: {okruszki("Placówki=/placowki/", p["nazwa"])} -->
<!-- placowka: {p["book"][0][0].replace("-spec", "")} -->

<section class="page-hero">
  <div class="wrap">
    {{{{okruszki}}}}
    <div class="page-hero__grid">
      <div>
        <h1>{p["pelna"]}</h1>
        <p class="page-hero__lead">{p["opis"]}</p>
        <div class="plac-info">
          <span class="otwarte" data-dni="1-5" data-od="{p["od"]}" data-do="{p["do"]}" hidden></span>
          <address>{p["ulica"]}, {p["kod"]}</address>
          <div class="place__godz">{{{{icon:clock}}}}{p["godz"]}</div>
          <div class="place__ext">{{{{icon:phone}}}}<a href="tel:+48665035035">665 035 035</a> wew. {p["wew"]}</div>
        </div>
        <div class="page-hero__cta">{przyciski}<a class="btn btn--ghost" href="{nawiguj}" target="_blank" rel="noopener">{{{{icon:map}}}}Nawiguj</a></div>
      </div>
      <a class="page-hero__media plac-mapa" href="{nawiguj}" target="_blank" rel="noopener" aria-label="Mapa dojazdu: {p["ulica"]}, {p["kod"]}, otwiera Google Maps"><img src="assets/img/{p["mapa"]}" alt="" width="860" height="520"></a>
    </div>
  </div>
</section>
{sekcje_html}
<section style="padding-bottom:0">
  <div class="wrap">
    <div class="cta-band">
      <div><h2>Umów wizytę</h2><p>Infolinia 665 035 035, numer wewnętrzny tej placówki: {p["wew"]}.</p></div>
      <div class="cta-band__actions"><a class="btn btn--light" href="tel:+48665035035">{{{{icon:phone}}}}665 035 035</a><button class="btn btn--outline-light" type="button" data-book="{p["book"][0][0]}">{{{{icon:calendar}}}}Umów wizytę</button></div>
    </div>
  </div>
</section>
"""


def main():
    for g in GRUPY:
        (SRC / f'{g["slug"]}.html').write_text(strona_grupy(g), encoding="utf-8")
    (SRC / "placowki.html").write_text(strona_placowki_hub(), encoding="utf-8")
    for p in PLACOWKI:
        (SRC / f'{p["slug"]}.html').write_text(strona_placowki(p), encoding="utf-8")
    print(f"zapisano {len(GRUPY)} grup wyrobów i {len(PLACOWKI) + 1} stron placówek")


if __name__ == "__main__":
    main()
