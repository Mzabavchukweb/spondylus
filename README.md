# spondylus.pl: strona statyczna (bez WordPressa)

Źródła w `src/`, gotowa strona w `dist/` (`python3 build.py`). Adresy 1:1 ze starej strony: `/slug/` = `dist/slug/index.html`.

## Budowanie i podgląd

```
python3 build.py                     # składa dist/, sitemap.xml, robots.txt, .htaccess, feed.xml
python3 narzedzia/kontrola_seo.py    # tytuły, opisy, H1, canonical, JSON-LD, obrazy
python3 -m http.server 8790 --directory dist
```

Build wypisuje linki do nieistniejących stron (lista ma być pusta).

Dostępność (WCAG 2.2 AA, axe-core, wszystkie strony na telefonie i komputerze; wymaga `npm install` i podglądu na :8790):

```
npm run wcag
```

## Tekstowa mapa treści

`dist/llms.txt` (llmstxt.org) składa się sam z tytułów i opisów podstron, wpisów i danych placówek.

## Podgląd na żywo

Każdy push na `main` buduje podgląd na GitHub Pages: https://mzabavchukweb.github.io/spondylus/
(`python3 build.py --podglad /spondylus`: adresy z prefiksem, noindex i robots Disallow, canonical na spondylus.pl,
formularz kontaktowy nieaktywny). Produkcję buduje się bez `--podglad`.

## Struktura

- `src/pages/<slug>.html`: podstrony. Nagłówek w komentarzach: `title`, `desc`, `nav`, `okruszki` (`Nasza kadra=/kadra/ > Imię`),
  `osoba` (`Imię | rola | placówka` → schema Physician), `og`, `noindex`.
- `src/blog/<slug>.html`: wpisy (`h1`, `data`, `zmiana`, `og`). Lista na /blog/ i RSS składają się same.
- `src/tresci/`: treści wyeksportowane ze starej strony (źródło dla `narzedzia/import_wp.py`, nie edytować).
- `static/`: pliki kopiowane bez zmian (`api/kontakt.php`, favicon, PDF regulaminu pod starą ścieżką).
- Przekierowania 301 i adresy usunięte (410): listy `PRZEKIEROWANIA` i `USUNIETE` w `build.py` → `dist/.htaccess`.

## Nowy specjalista albo wpis

Skopiuj podobny plik w `src/pages` (profil) lub `src/blog` (wpis), zmień nagłówek i treść, dodaj kartę w `src/pages/kadra.html`,
uruchom build i kontrolę SEO, wgraj `dist/`.

## Pomiar

GA4 `G-YJRR4EB0F8` i GTM `GTM-PB32PJXN` jak na starej stronie, Consent Mode v2 (domyślnie brak zgody, baner w stopce).
