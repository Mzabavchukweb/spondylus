#!/usr/bin/env python3
"""Kontrola SEO zbudowanej strony (dist/): tytuły, opisy, H1, canonical, dane strukturalne, obrazy. Uruchom po build.py."""
import collections, html, json, pathlib, re, sys

DIST = pathlib.Path(__file__).resolve().parent.parent / "dist"
uwagi, tytuly, opisy = [], collections.defaultdict(list), collections.defaultdict(list)
for f in sorted(DIST.rglob("*.html")):
    url = "/" + str(f.parent.relative_to(DIST)).replace(".", "") + "/" if f.name == "index.html" else "/" + f.name
    url = url.replace("//", "/")
    s = f.read_text(encoding="utf-8")
    t = html.unescape(re.search(r"<title>(.*?)</title>", s).group(1))
    d = html.unescape(re.search(r'<meta name="description" content="(.*?)"', s).group(1))
    noindex = 'content="noindex' in s
    tytuly[t].append(url); opisy[d].append(url)
    h1 = len(re.findall(r"<h1[\s>]", s))
    kan = re.search(r'<link rel="canonical" href="https://spondylus.pl(.*?)"', s).group(1)
    wpis = '"@type":"BlogPosting"' in s  # tytuły wpisów zostają jak w WordPressie (na nie są pozycje), bez dopisku marki
    if not 30 <= len(t) <= (66 if wpis else 62): uwagi.append(f"{url}: tytuł {len(t)} zn. „{t}”")
    if not noindex and not 110 <= len(d) <= 160: uwagi.append(f"{url}: opis {len(d)} zn.")
    if h1 != 1: uwagi.append(f"{url}: H1 = {h1}")
    if kan != url and f.name != "404.html": uwagi.append(f"{url}: canonical {kan}")
    for blok in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try: json.loads(blok)
        except Exception as e: uwagi.append(f"{url}: zły JSON-LD {e}")
    for img in re.findall(r"<img\b[^>]*>", s):
        if " alt=" not in img: uwagi.append(f"{url}: obraz bez alt {img[:80]}")
        if " width=" not in img: uwagi.append(f"{url}: obraz bez wymiarów {img[:80]}")
    if re.search(r"[➤✔⭐✨]", t + d): uwagi.append(f"{url}: emotki w tytule/opisie")
    if "—" in t + d: uwagi.append(f"{url}: pauza (—) w tytule/opisie")
for t, u in tytuly.items():
    if len(u) > 1: uwagi.append(f"ten sam tytuł na {u}")
for d, u in opisy.items():
    if len(u) > 1: uwagi.append(f"ten sam opis na {u}")
print("\n".join(uwagi) if uwagi else "SEO: bez uwag")
sys.exit(1 if uwagi else 0)
