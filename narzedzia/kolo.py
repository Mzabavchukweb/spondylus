"""Generuje koło „Zespół wokół pacjenta” w src/pages/index.html.
Jeśli w assets/img/ilu są pliki kolo-*.webp, wstawia je na białych krążkach; w przeciwnym razie ikony liniowe."""
import math
import pathlib
import importlib.util

ROOT = pathlib.Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("b", ROOT / "build.py")
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)

OB = [
    ("rehabilitacja", "spine", "Rehabilitacja i fizjoterapia", "Po operacjach, urazach i przy bólu", "#"),
    ("podologia", "foot", "Podologia", "Paznokcie, stopa cukrzycowa, odciski", "podologia.html"),
    ("diagnostyka", "scan", "Diagnostyka wad postawy", "Postawa, stopy, USG postępów", "#"),
    ("sport", "run", "Medycyna sportowa", "Kontuzje i powrót do treningu", "#"),
    ("lekarze", "stethoscope", "Konsultacje lekarskie", "Ortopeda, neurolog, neurochirurg", "kadra.html"),
    ("dietetyka", "leaf", "Dietetyka", "Kliniczna i sportowa", "#"),
    ("estetyka", "sparkle", "Medycyna estetyczna", "Pod opieką zespołu medycznego", "#"),
    ("zaopatrzenie", "crutch", "Zaopatrzenie z NFZ", "Wózki, wkładki, obuwie", "#refundacja"),
]
C, R, r, GAP = 300, 250, 104, 2.2


def pt(rad, ang):
    a = math.radians(ang - 90)
    return C + rad * math.cos(a), C + rad * math.sin(a)


def demo(h):
    return ' data-demo="1"' if h == "#" else ""


segs = ""
for i, (k, ic, t, o, h) in enumerate(OB):
    a0, a1 = i * 360 / len(OB) + GAP / 2, (i + 1) * 360 / len(OB) - GAP / 2
    x0, y0 = pt(R, a0); x1, y1 = pt(R, a1); x2, y2 = pt(r, a1); x3, y3 = pt(r, a0)
    d = f"M{x0:.1f} {y0:.1f}A{R} {R} 0 0 1 {x1:.1f} {y1:.1f}L{x2:.1f} {y2:.1f}A{r} {r} 0 0 0 {x3:.1f} {y3:.1f}Z"
    mx, my = pt((R + r) / 2, (a0 + a1) / 2)
    plik = ROOT / f"assets/img/ilu/kolo-{k}.webp"
    if plik.exists():
        znak = (f'<circle class="kolo__krazek" cx="{mx:.1f}" cy="{my:.1f}" r="38"/>'
                f'<image href="assets/img/ilu/kolo-{k}.webp" x="{mx - 30:.1f}" y="{my - 30:.1f}" width="60" height="60"/>')
    else:
        s = 44
        znak = (f'<svg x="{mx - s / 2:.1f}" y="{my - s / 2:.1f}" width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" '
                f'stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{b.ICONS[ic]}</svg>')
    segs += f'<a class="kolo__seg" href="{h}"{demo(h)} data-seg="{k}" aria-label="{t}"><path d="{d}"/>{znak}</a>'

svg = (f'<svg class="kolo__svg" viewBox="0 0 600 600" role="group" aria-label="Obszary opieki wokół pacjenta">{segs}'
       f'<circle class="kolo__srodek" cx="{C}" cy="{C}" r="{r - 10}"/>'
       f'<text class="kolo__ty" x="{C}" y="{C - 6}" text-anchor="middle">Pacjent</text>'
       f'<text class="kolo__ty2" x="{C}" y="{C + 22}" text-anchor="middle">w centrum</text></svg>')


def etyk(i):
    k, ic, t, o, h = OB[i]
    return f'<a class="kolo__et" href="{h}"{demo(h)} data-seg="{k}"><b>{t}</b><span>{o}</span></a>'


blok = (f'    <div class="kolo">\n      <div class="kolo__lewa">{"".join(etyk(i) for i in [7, 6, 5, 4])}</div>\n'
        f'      {svg}\n      <div class="kolo__prawa">{"".join(etyk(i) for i in [0, 1, 2, 3])}</div>\n    </div>\n')

p = ROOT / "src/pages/index.html"
s = p.read_text()
a = s.index('    <div class="kolo">')
z = s.index('    </div>\n', s.index('class="kolo__prawa"', a)) + len('    </div>\n')
p.write_text(s[:a] + blok + s[z:])
print("koło:", sum((ROOT / f"assets/img/ilu/kolo-{k}.webp").exists() for k, *_ in OB), "z 8 ikon 3D")
