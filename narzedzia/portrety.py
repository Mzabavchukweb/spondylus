"""Jednolite portrety zespołu: wycięcie osoby (Vision), zielone tło, kadr według twarzy. Twarz nie jest zmieniana."""
import subprocess, sys, pathlib, tempfile
from PIL import Image, ImageFilter

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC, DST, TMP = ROOT / "assets/src", ROOT / "assets/img/portrety", pathlib.Path(tempfile.gettempdir()) / "spondylus-wyciecia"
W, H = 600, 750
DST.mkdir(parents=True, exist_ok=True)
TMP.mkdir(parents=True, exist_ok=True)

def tlo():
    top, bot = (227, 241, 231), (211, 232, 218)
    im = Image.new("RGB", (W, H))
    px = im.load()
    for y in range(H):
        t = y / (H - 1)
        c = tuple(round(top[i] + (bot[i] - top[i]) * t) for i in range(3))
        for x in range(W):
            px[x, y] = c
    return im

TLO = tlo()
for f in sorted(SRC.glob("kadra-*")):
    slug = f.stem.replace("kadra-", "")
    out_png = TMP / f"{slug}.png"
    r = subprocess.run(["xcrun", "swift", str(ROOT / "narzedzia/wytnij.swift"), str(f), str(out_png)], capture_output=True, text=True)
    if r.returncode or "brak" in r.stdout:
        print("POMINIĘTO", slug, r.stderr.strip() or r.stdout.strip()); continue
    fx, fy, fw, fh = map(int, r.stdout.split())
    osoba = Image.open(out_png).convert("RGBA")
    # skala: twarz zajmuje ok. 30% wysokości kadru
    s = (H * 0.28) / fh
    sw, sh = round(osoba.width * s), round(osoba.height * s)
    cx, cy = (fx + fw / 2) * s, (fy + fh / 2) * s
    ox, oy = W / 2 - cx, H * 0.40 - cy
    # bez „wiszącego” tułowia: dół osoby musi sięgać dołu kadru
    dol = oy + sh
    if dol < H:
        brak = H - dol
        if brak < H * 0.14:
            oy += brak
        else:
            s2 = s * (H - oy) / (sh)  # powiększ, aż dół sięgnie krawędzi
            s, sw, sh = s2, round(osoba.width * s2), round(osoba.height * s2)
            cx, cy = (fx + fw / 2) * s, (fy + fh / 2) * s
            ox, oy = W / 2 - cx, H * 0.40 - cy
            oy += max(0, H - (oy + sh))
    osoba = osoba.resize((sw, sh), Image.LANCZOS)
    # lekkie zmiękczenie krawędzi maski
    a = osoba.getchannel("A").filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.9))
    osoba.putalpha(a)
    kadr = TLO.copy()
    kadr.paste(osoba, (round(ox), round(oy)), osoba)
    kadr.save(DST / f"{slug}.webp", quality=84)
    print("OK", slug, f"twarz {fw}x{fh}", f"skala {s:.2f}")
