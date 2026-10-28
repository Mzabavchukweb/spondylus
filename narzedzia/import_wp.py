#!/usr/bin/env python3
"""Jednorazowy import treści starej strony do źródeł nowej: src/pages/<slug>.html i src/blog/<slug>.html.

Treść zostaje słowo w słowo (to ona trzyma pozycje w Google). Zmienia się oprawa: jeden H1, prawdziwe nagłówki
zamiast pogrubionych akapitów, lekkie obrazy WebP z opisami, tytuły i opisy bez szablonowych emotek.
Strony, które już istnieją w src/pages, są pomijane (nie nadpisuje ręcznej pracy). Wymaga Pillow.
Użycie: python3 narzedzia/import_wp.py [--nadpisz slug,slug]
"""
import html, io, json, pathlib, re, sys, urllib.request
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
TRESCI = ROOT / "src/tresci"
META = json.loads((TRESCI / "_meta.json").read_text())
NADPISZ = set(sys.argv[sys.argv.index("--nadpisz") + 1].split(",")) if "--nadpisz" in sys.argv else set()
UA = {"User-Agent": "Mozilla/5.0 (Macintosh) Chrome/130"}

PLACOWKA_TXT = {
    "szczecin-jp": ("Spondylus Szczecin, centrum", "al. Jana Pawła II 36", "1"),
    "szczecin-ul": ("Spondylus Szczecin Pogodno", "ul. Unii Lubelskiej 2B", "2"),
    "koszalin": ("Spondylus Koszalin", "ul. Jana Pawła II 21", "4"),
}

# ---------- usługi i programy: H1, tytuł i opis pisane ręcznie, treść ze starej strony ----------
USLUGI = {
    "rehabilitacja-2": dict(
        h1="Rehabilitacja w Szczecinie i Koszalinie",
        lead="Fizjoterapia ortopedyczna, pourazowa, pooperacyjna i neurologiczna. Terapia dobrana po diagnostyce, metody manualne i fizykalne.",
        title="Rehabilitacja Szczecin: poradnia rehabilitacyjna | Spondylus",
        desc="Rehabilitacja w Spondylus: terapia manualna, kinezyterapia, fizykoterapia i masaż. Program dobrany po diagnostyce. Szczecin i Koszalin, od 1989 roku.",
        okruszki="Oferta=/oferta/ > Rehabilitacja", book=""),
    "zakres-uslug-diagnostycznych": dict(
        h1="Diagnostyka wad postawy i aparatu ruchu",
        lead="Komputerowe badanie stóp, diagnostyka posturalna, badania dla sportowców i dzieci. Wynik, który pokazuje, od czego zacząć terapię.",
        title="Diagnostyka wad postawy i badanie stóp Szczecin | Spondylus",
        desc="Komputerowe badanie stóp, diagnostyka postawy ciała, analiza chodu i badania dla sportowców. Diagnostyka dzieci i dorosłych w Spondylus w Szczecinie.",
        okruszki="Oferta=/oferta/ > Diagnostyka", book=""),
    "medycyna-sportowa": dict(
        h1="Medycyna sportowa w Szczecinie i Koszalinie",
        lead="Diagnostyka i badania dla osób aktywnych, leczenie kontuzji i bezpieczny powrót do treningu.",
        title="Medycyna sportowa Szczecin i Koszalin: poradnia | Spondylus",
        desc="Poradnia medycyny sportowej Spondylus: diagnostyka sportowa, badania dla aktywnych, leczenie kontuzji i powrót do treningu. Szczecin i Koszalin.",
        okruszki="Oferta=/oferta/ > Medycyna sportowa", book=""),
    "medycyna-estetyczna": dict(
        h1="Medycyna estetyczna w Spondylus",
        lead="Zabiegi pielęgnacyjne i modelujące sylwetkę prowadzone pod opieką zespołu medycznego.",
        title="Medycyna estetyczna Szczecin: twarz i ciało | Spondylus",
        desc="Medycyna estetyczna w Spondylus: zabiegi pielęgnacyjne, ujędrniające i modelujące sylwetkę, prowadzone przez zespół medyczny. Umów konsultację.",
        okruszki="Oferta=/oferta/ > Medycyna estetyczna", book=""),
    "dietetyka": dict(
        h1="Dietetyka kliniczna w Szczecinie",
        lead="Indywidualne porady żywieniowe i plany dietetyczne dopasowane do stanu zdrowia, terapii i celów.",
        title="Dietetyk kliniczny Szczecin: porady i plany diety | Spondylus",
        desc="Dietetyka kliniczna w Spondylus: indywidualne porady żywieniowe i plany diety dopasowane do zdrowia, terapii i aktywności. Umów wizytę w Szczecinie.",
        okruszki="Oferta=/oferta/ > Dietetyka", book=""),
    "zaopatrzenie-medyczne": dict(
        h1="Zaopatrzenie medyczne w Szczecinie i Koszalinie",
        lead="Wkładki ortopedyczne, obuwie, sprzęt pielęgnacyjny i rehabilitacyjny. Pomagamy dobrać rozwiązanie, także z refundacją NFZ.",
        title="Zaopatrzenie medyczne i sklep ortopedyczny Szczecin",
        desc="Wkładki ortopedyczne, obuwie, ortezy, produkty kompresyjne i ciężki sprzęt rehabilitacyjny. Doradztwo i refundacja NFZ. Spondylus Szczecin i Koszalin.",
        okruszki="Oferta=/oferta/ > Zaopatrzenie medyczne", book=""),
    "zdrowa-nozka-i-kregoslup": dict(
        h1="Program Zdrowa Nóżka i Kręgosłup",
        lead="Badania postawy i stóp dzieci w przedszkolach. Ponad 25 000 przebadanych dzieci.",
        title="Zdrowa Nóżka i Kręgosłup: badania postawy dzieci | Spondylus",
        desc="Program profilaktyki Spondylus: badania postawy i stóp dzieci w przedszkolach w Szczecinie. Jak przebiega badanie i jak zapisać dziecko.",
        okruszki="Programy=/oferta/ > Zdrowa Nóżka i Kręgosłup", book=""),
    "aktywny-senior": dict(
        h1="Program Aktywny Senior",
        lead="Bezpłatne konsultacje i badania profilaktyczne dla osób po 60. roku życia.",
        title="Aktywny Senior: program dla seniorów 60+ Szczecin | Spondylus",
        desc="Aktywny Senior w Spondylus: programy i zajęcia wspierające zdrowie, sprawność i samodzielność seniorów. Bezpłatne konsultacje i badania profilaktyczne.",
        okruszki="Programy=/oferta/ > Aktywny Senior", book=""),
    "podologia": dict(
        h1="Podologia w Szczecinie",
        lead="Zabiegi na stopy w gabinecie podologicznym: pedicure medyczny, odciski, wrastające paznokcie.",
        title="Podologia Szczecin: gabinet podologiczny | Spondylus",
        desc="Gabinet podologiczny Spondylus w Szczecinie: pedicure medyczny, usuwanie odcisków i modzeli, korekta wrastających paznokci, badanie stóp.",
        okruszki="Oferta=/oferta/ > Podologia", book=""),
    "mobilny-podolog": dict(
        h1="Mobilny Podolog z dojazdem do domu",
        lead="Zabiegi podologiczne w domu pacjenta na terenie Szczecina. Umów wizytę: 609 442 071.",
        title="Mobilny podolog Szczecin: wizyty domowe | Spondylus",
        desc="Mobilny podolog Spondylus: pielęgnacja stóp i zabiegi podologiczne z dojazdem do domu pacjenta w Szczecinie. Umów wizytę pod numerem 609 442 071.",
        okruszki="Programy=/oferta/ > Mobilny Podolog", book="", tel="+48609442071", tel_txt="609 442 071"),
    "oferta": dict(
        h1="Oferta Spondylus",
        lead="Rehabilitacja, diagnostyka, konsultacje lekarskie, dietetyka, medycyna sportowa i estetyczna oraz zaopatrzenie medyczne.",
        title="Oferta: rehabilitacja, diagnostyka, zaopatrzenie | Spondylus",
        desc="Pełna oferta centrum medycznego Spondylus: rehabilitacja, diagnostyka wad postawy, medycyna sportowa, dietetyka, medycyna estetyczna i zaopatrzenie NFZ.",
        okruszki="Oferta", book=""),
}

INNE = {
    "rejestracja-online": dict(
        h1="Rejestracja online", lead="Wybierz placówkę i wolny termin. Wolisz telefonicznie? Infolinia 665 035 035.",
        title="Rejestracja online: umów wizytę w Spondylus",
        desc="Umów wizytę online w Spondylus: wybierz placówkę w Szczecinie lub Koszalinie i wolny termin w kalendarzu. Infolinia dla wszystkich placówek: 665 035 035.",
        okruszki="Rejestracja online"),
    "polityka-prywatnosci-i-plikow-cookies": dict(
        h1="Polityka prywatności i plików cookies", lead="",
        title="Polityka prywatności i plików cookies | Spondylus",
        desc="Zasady przetwarzania danych osobowych i wykorzystania plików cookies na stronie Spondylus. Administrator danych, cele, prawa pacjentów i kontakt.",
        okruszki="Polityka prywatności"),
    "regulamin-kart-podarunkowych": dict(
        h1="Regulamin kart podarunkowych", lead="",
        title="Regulamin kart podarunkowych | Spondylus",
        desc="Regulamin kart podarunkowych Spondylus: zasady zakupu, ważności i realizacji kart na usługi w placówkach w Szczecinie i Koszalinie.",
        okruszki="Regulamin kart podarunkowych"),
    "regulamin-sportowych-pakietow-medycznych": dict(
        h1="Regulamin Sportowych Pakietów Medycznych", lead="",
        title="Regulamin Sportowych Pakietów Medycznych | Spondylus",
        desc="Regulamin Sportowych Pakietów Medycznych Spondylus do pobrania wraz z załącznikiem. Zasady korzystania z pakietów dla klubów i sportowców.",
        okruszki="Regulamin pakietów sportowych"),
}

KADRA = {  # slug: (imię i nazwisko, rola, placówka, portret w assets/img/portrety albo None)
    "adam-kaminski": ("Adam Kamiński", "Ortopeda, dr hab. n. med.", "szczecin-ul", "adam-kaminski"),
    "dawid-pacek": ("Dawid Pacek", "Ortopeda, dr n. med.", "szczecin-ul", None),
    "rafal-przybylski": ("Rafał Przybylski", "Ortopeda, dr n. med.", "szczecin-ul", None),
    "tomasz-dudzik": ("Tomasz Dudzik", "Neurolog, dr n. med.", "szczecin-ul", "tomasz-dudzik"),
    "piotr-salapa": ("Piotr Sałapa", "Neurochirurg, dr n. med.", "szczecin-ul", "piotr-salapa"),
    "magdalena-salabon": ("Magdalena Sałabon", "Fizjoterapeutka dzieci", "szczecin-jp", "magdalena-salabon"),
    "gabriela-majorczyk": ("Gabriela Majorczyk", "Fizjoterapeutka", "szczecin-ul", "gabriela-majorczyk"),
    "tomasz-zdeb-fizjoterapeuta": ("Tomasz Zdeb", "Fizjoterapeuta", "szczecin-ul", "tomasz-zdeb"),
    "weronika-kujawska": ("Weronika Kujawska", "Fizjoterapeutka dziecięca", "", None),
    "rafal-perkowski": ("Rafał Perkowski", "Fizjoterapeuta", "koszalin", None),
    "marika-wachowiak-podolog": ("Marika Wachowiak", "Podolog, kosmetolog", "szczecin-ul", None),
    "kinga-mackowiak": ("Kinga Maćkowiak", "Podolog, kosmetolog", "szczecin-jp", None),
    "marta-rojewska-podolog": ("Marta Rojewska", "Podolog", "koszalin", None),
    "olga-veremiienko": ("Olga Veremiienko", "Stylistka paznokci i brwi", "koszalin", "olga-veremiienko"),
    "agnieszka-popkowska-dietetyk": ("Agnieszka Popkowska", "Dietetyk", "", None),
}


OPISY = {
    "dieta-ketogeniczna-co-jesc-na-keto-przykladowy-jadlospis": "Co jeść na diecie keto? Jadłospis z przepisami na smaczne dania i gotowe menu na każdy dzień. Zacznij dietę ketogeniczną dzisiaj.",
    "agnieszka-popkowska-dietetyk": "Agnieszka Popkowska, dietetyk w Spondylus. Porady żywieniowe i plany diety dopasowane do zdrowia i aktywności. Umów wizytę: infolinia 665 035 035.",
    "marta-rojewska-podolog": "Marta Rojewska, podolog w Spondylus Koszalin, ul. Jana Pawła II 21. Pielęgnacja i zabiegi podologiczne stóp. Umów wizytę: infolinia 665 035 035, wew. 4.",
}

STARE_LINKI = {
    "diagnostyka-komputerowa-stop": "/zakres-uslug-diagnostycznych/", "komputerowe-badanie-stop": "/zakres-uslug-diagnostycznych/",
    "fizykoterapia": "/rehabilitacja-2/", "terapia-manualna": "/rehabilitacja-2/", "drenaz-limfatyczny": "/rehabilitacja-2/",
    "masaze-terapeutyczne": "/rehabilitacja-2/", "korekta-wrastajacych-paznokci": "/podologia/", "pedicure-medyczny": "/podologia/",
    "usuwanie-odciskow": "/podologia/", "podologia/pielegnacja-i-leczenie/pedicure-medyczny": "/podologia/",
    "analiza-skladu-ciala": "/dietetyka/",
}


def sentence_case(t):
    t = t.strip(" :")
    return t[:1].upper() + t[1:].lower() if t.isupper() else t


def pobierz_obraz(url, cel, szer=1200):
    """Obraz ze starej strony → WebP (max szer px). Zwraca (ścieżka względna, w, h)."""
    cel.parent.mkdir(parents=True, exist_ok=True)
    if not cel.exists():
        u = urllib.parse.quote(url, safe=":/")
        dane = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30).read()
        im = Image.open(io.BytesIO(dane)).convert("RGB")
        if im.width > szer:
            im = im.resize((szer, round(im.height * szer / im.width)), Image.LANCZOS)
        im.save(cel, quality=80)
    w, h = Image.open(cel).size
    return "assets/" + str(cel.relative_to(ROOT / "assets")), w, h


def obrazy_w_tresci(body, folder, alt_domyslny):
    def zamien(m):
        tag = m.group(0)
        src = re.search(r'src="([^"]+)"', tag).group(1)
        alt = (re.search(r'alt="([^"]*)"', tag) or [None, ""])[1]
        nazwa = re.sub(r"[^a-z0-9-]+", "-", pathlib.Path(urllib.parse.unquote(src)).stem.lower()).strip("-")
        try:
            sciezka, w, h = pobierz_obraz(src, ROOT / f"assets/img/{folder}/{nazwa}.webp")
        except Exception as e:
            print("  obraz pominięty:", src, e)
            return ""
        return f'<img src="{sciezka}" alt="{html.escape(alt or alt_domyslny, quote=True)}" width="{w}" height="{h}" loading="lazy">'
    return re.sub(r'<img\b[^>]*src="https?://spondylus\.pl[^"]*"[^>]*>', zamien, body)


def porzadkuj(body):
    """Pogrubione akapity-nagłówki na <h2>, zbędne <br>, linki ze starej domeny."""
    body = re.sub(r"<p>\s*<strong>([^<]{3,90}?)</strong>\s*<br/>\s*", lambda m: f"<h2>{sentence_case(m.group(1))}</h2>\n<p>", body)
    body = re.sub(r"<p>\s*<strong>([^<]{3,120}?)</strong>\s*</p>", lambda m: f"<h2>{sentence_case(m.group(1))}</h2>", body)
    body = re.sub(r"<h1>.*?</h1>", "", body, count=1, flags=re.S)

    def listy(m):  # akapit z liniami „– punkt” rozdzielonymi <br/> → lista
        czesci = [c.strip() for c in re.split(r"<br/>", m.group(1))]
        punkty = [c for c in czesci if re.match(r"^[–-]\s*", c)]
        if len(punkty) < 2:
            return m.group(0)
        wstep = [c for c in czesci if c and not re.match(r"^[–-]\s*", c)]
        lis = "".join(f"<li>{re.sub(r'^[–-]\s*', '', c).rstrip(',;.')}</li>" for c in punkty)
        return (f"<p>{' '.join(wstep)}</p>" if wstep else "") + f"<ul>{lis}</ul>"
    body = re.sub(r"<p>((?:(?!</p>).)*?<br/>(?:(?!</p>).)*)</p>", listy, body, flags=re.S)
    body = body.replace("<b>", "<strong>").replace("</b>", "</strong>")
    body = re.sub(r"<p>\s*</p>", "", body)
    body = re.sub(r'href="/(rejestracja|rejestracja-wizyty)/"', 'href="/rejestracja-online/"', body)
    for stary, nowy in STARE_LINKI.items():  # podstrony usunięte w WordPressie → strona usługi
        body = re.sub(rf'href="/{re.escape(stary)}/?"', f'href="{nowy}"', body)
    return body.strip()


def czysty_opis(t):
    t = html.unescape(t or "")
    t = re.sub(r"^(spondylus(\.pl)?\s*➤\s*)", "", t, flags=re.I)
    emoji = r"[\u2600-\u27BF\u2B50\uFE0F\U0001F000-\U0001FFFF]+"
    t = re.sub(r"\s*" + emoji + r"\s*(?=[A-ZĄĆĘŁŃÓŚŹŻ])", ". ", t)  # emotka między zdaniami = koniec zdania
    t = re.sub(r"\s*" + emoji + r"\s*", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    t = re.sub(r"([.?!])(\s*\.)+", r"\1", t)
    t = t.replace("\u043a\u0441", "ks")  # cyrylica w starym opisie („haluксами”)
    if t and t[-1] not in ".?!":
        t += "."
    if len(t) > 156:
        t = t[:156].rsplit(" ", 1)[0].rstrip(",;:") + "."
    return t


def cta(tel="+48665035035", tel_txt="665 035 035", book=""):
    b = f' data-book="{book}"' if book else " data-book"
    return f'''<section class="cta-band">
  <div class="wrap">
    <div><h2>Umów wizytę</h2><p>Rejestracja dobierze specjalistę i najbliższy termin w Szczecinie lub Koszalinie.</p></div>
    <div class="cta-band__actions"><button class="btn btn--primary" type="button"{b}>{{{{icon:calendar}}}}Umów wizytę</button><a class="btn btn--ghost" href="tel:{tel}">{{{{icon:phone}}}}{tel_txt}</a></div>
  </div>
</section>'''


def naglowek(meta):
    return "".join(f"<!-- {k}: {v} -->\n" for k, v in meta.items() if v) + "\n"


def zapisz(sciezka, tekst):
    if sciezka.exists() and sciezka.stem not in NADPISZ:
        print("  pomijam (już jest):", sciezka.relative_to(ROOT))
        return
    sciezka.parent.mkdir(parents=True, exist_ok=True)
    sciezka.write_text(tekst, encoding="utf-8")
    print("  zapisano", sciezka.relative_to(ROOT))


def strona_zwykla(slug, d, nav="oferta"):
    body = porzadkuj((TRESCI / f"{slug}.html").read_text())
    body = obrazy_w_tresci(body, f"uslugi/{slug}", d["h1"])
    og = META[slug].get("og_image")
    meta = {"title": d["title"], "desc": d["desc"], "nav": nav, "okruszki": d["okruszki"]}
    lead = f'\n    <p class="page-hero__lead">{d["lead"]}</p>' if d.get("lead") else ""
    tekst = naglowek(meta) + f'''<section class="page-hero">
  <div class="wrap">
    {{{{okruszki}}}}
    <h1>{d["h1"]}</h1>{lead}
  </div>
</section>

<section class="section">
  <div class="wrap wrap--tekst">
    <div class="prose">
{body}
    </div>
  </div>
</section>

''' + cta(d.get("tel", "+48665035035"), d.get("tel_txt", "665 035 035"), d.get("book", "")) + "\n"
    zapisz(ROOT / f"src/pages/{slug}.html", tekst)


def profil(slug, imie, rola, pl, portret):
    m = META[slug]
    body = (TRESCI / f"{slug}.html").read_text()
    body = re.sub(r"<img[^>]*>", "", body, count=1)  # zdjęcie trafia do karty profilu
    body = porzadkuj(body)
    body = obrazy_w_tresci(body, f"kadra/{slug}", imie)
    miasto = {"szczecin-jp": "Szczecin", "szczecin-ul": "Szczecin Pogodno", "koszalin": "Koszalin"}.get(pl, "Szczecin")
    zawod = rola.split(",")[0].lower()
    title = f"{imie}, {zawod} {miasto} | Spondylus"
    if len(title) > 60:
        title = f"{imie}, {zawod} {miasto.split()[0]} | Spondylus"
    if len(title) > 60:
        title = title.replace(" | Spondylus", "")
    desc = czysty_opis(m["desc"])
    if not desc or "Centrum Medyczne" in (m["desc"] or "") or len(desc) < 110:
        tekst_lead = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", re.search(r"<p>(.*?)</p>", body, re.S).group(1) if "<p>" in body else "")).strip()
        desc = czysty_opis(f"{imie}, {zawod} w Spondylus {miasto}. {tekst_lead}")
    if slug in OPISY:
        desc = OPISY[slug]
    foto = ""
    og = None
    if portret:
        foto = f'<div class="profile__foto">{{{{portret:{portret}}}}}</div>'
        og = f"/assets/img/portrety/{portret}.webp"
    elif m["obrazy"]:
        try:
            sciezka, w, h = pobierz_obraz(m["obrazy"][0], ROOT / f"assets/img/kadra/{slug}.webp", 600)
            foto = f'<div class="profile__foto"><img src="{sciezka}" alt="{imie}" width="{w}" height="{h}"></div>'
            og = "/" + sciezka
        except Exception as e:
            print("  zdjęcie pominięte:", e)
    if pl:
        nazwa, ulica, wew = PLACOWKA_TXT[pl]
        miejsce = f'<div>{{{{icon:pin}}}}<span>{nazwa}<br>{ulica}</span></div>'
        przyciski = (f'<button class="btn btn--primary" type="button" data-book="{pl}">{{{{icon:calendar}}}}Umów wizytę</button>'
                     f'<a class="btn btn--ghost" href="tel:+48665035035">{{{{icon:phone}}}}665 035 035, wew. {wew}</a>')
    else:
        miejsce = ""
        przyciski = (f'<button class="btn btn--primary" type="button" data-book>{{{{icon:calendar}}}}Umów wizytę</button>'
                     f'<a class="btn btn--ghost" href="tel:+48665035035">{{{{icon:phone}}}}665 035 035</a>')
    meta = {"title": title, "desc": desc, "nav": "kadra", "okruszki": f"Nasza kadra=/kadra/ > {imie}",
            "osoba": f"{imie} | {rola} | {pl}", "og": og}
    tekst = naglowek(meta) + f'''<section class="page-hero" style="padding-bottom:40px">
  <div class="wrap">
    {{{{okruszki}}}}
  </div>
</section>

<section style="padding-bottom:var(--section)">
  <div class="wrap profile">
    <aside class="profile__card">
      {foto}
      <div class="profile__card-body">
        <div><div class="person__role" style="margin-top:0">{rola}</div><h1 style="font-size:30px;margin-top:4px">{imie}</h1></div>
        <div class="profile__meta">{miejsce}</div>
        {przyciski}
      </div>
    </aside>
    <div class="prose">
{body}
    </div>
  </div>
</section>
'''
    zapisz(ROOT / f"src/pages/{slug}.html", tekst)


def wpis(slug):
    m = META[slug]
    body = porzadkuj((TRESCI / f"{slug}.html").read_text())
    body = obrazy_w_tresci(body, f"blog/{slug}", m["tytul_wp"])
    og, w, h = None, 1200, 630
    if m.get("og_image"):
        sciezka, w, h = pobierz_obraz(m["og_image"], ROOT / f"assets/img/blog/{slug}.webp")
        og = "/" + sciezka
    title = re.sub(r"\s*[|-]\s*(Blog\s*-\s*)?Spondylus\s*$", "", m["title"] or m["tytul_wp"]).strip()
    title = re.sub(r"\s*-\s*Blog$", "", title)
    title = f"{title} | Spondylus" if len(title) <= 48 else title
    meta = {"title": title, "desc": OPISY.get(slug) or czysty_opis(m["desc"]), "h1": html.unescape(m["tytul_wp"]), "data": m["data"],
            "zmiana": m["zmiana"], "og": og, "og_w": w, "og_h": h, "og_alt": html.unescape(m["tytul_wp"]), "nav": "blog"}
    zapisz(ROOT / f"src/blog/{slug}.html", naglowek(meta) + body + "\n")


if __name__ == "__main__":
    import urllib.parse
    for slug, d in USLUGI.items():
        strona_zwykla(slug, d)
    for slug, d in INNE.items():
        strona_zwykla(slug, d, nav="")
    for slug, (imie, rola, pl, portret) in KADRA.items():
        profil(slug, imie, rola, pl, portret)
    for slug, m in META.items():
        if m["typ"] == "wpis":
            wpis(slug)
