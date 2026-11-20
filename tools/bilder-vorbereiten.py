#!/usr/bin/env python3
"""Bereitet die gelieferten Bilder für den Kalender vor.

Liest aus einem Ordner (Standard: bilder-roh/) tag-01.jpg ... tag-24.jpg, landing.jpg, finale.jpg
(auch .png), schneidet einen gemalten Papierrand ab, schneidet mittig auf 2:1 zu, verkleinert
und speichert nach bilder/. Danach tools/pixel.py ausführen.

Aufruf:  python3 tools/bilder-vorbereiten.py [quellordner]
"""
import sys
from pathlib import Path
from PIL import Image, ImageOps

HAUPT = Path(__file__).resolve().parent.parent
ZIEL = HAUPT / "bilder"
GROESSE = {"tag": (1200, 600), "landing": (1200, 600), "finale": (1200, 600)}

def ist_papier(px, papier):
    r, g, b = px
    hell = (r + g + b) / 3
    return hell > 200 and max(r, g, b) - min(r, g, b) < 40 and abs(hell - sum(papier) / 3) < 30

def rand_finden(bild):
    """Gibt (links, oben, rechts, unten) des bemalten Bereichs zurück."""
    k = bild.convert("RGB").resize((bild.width // 8, bild.height // 8))
    w, h = k.size; p = k.load()
    ecken = [p[2, 2], p[w - 3, 2], p[2, h - 3], p[w - 3, h - 3]]
    hell = [c for c in ecken if sum(c) / 3 > 200 and max(c) - min(c) < 40]
    if not hell:
        return (0, 0, bild.width, bild.height)
    papier = tuple(sum(c[i] for c in hell) // len(hell) for i in range(3))
    def anteil_zeile(y): return sum(ist_papier(p[x, y], papier) for x in range(w)) / w
    def anteil_spalte(x): return sum(ist_papier(p[x, y], papier) for y in range(h)) / h
    GRENZE = 0.35
    oben = next((y for y in range(h // 3) if anteil_zeile(y) < GRENZE), 0)
    unten = next((y for y in range(h - 1, 2 * h // 3, -1) if anteil_zeile(y) < GRENZE), h - 1)
    links = next((x for x in range(w // 3) if anteil_spalte(x) < GRENZE), 0)
    rechts = next((x for x in range(w - 1, 2 * w // 3, -1) if anteil_spalte(x) < GRENZE), w - 1)
    # etwas Abstand nach innen, damit der unregelmäßige Pinselrand sicher wegfällt
    ein_x, ein_y = int(w * 0.025), int(h * 0.035)
    l = links + (ein_x if links else 0); r = rechts - (ein_x if rechts < w - 1 else 0)
    o = oben + (ein_y if oben else 0); u = unten - (ein_y if unten < h - 1 else 0)
    return (l * 8, o * 8, (r + 1) * 8, (u + 1) * 8)

def main():
    quelle = Path(sys.argv[1]) if len(sys.argv) > 1 else HAUPT.parent / "bilder-roh"
    ZIEL.mkdir(exist_ok=True)
    namen = [f"tag-{i:02d}" for i in range(1, 25)] + ["landing", "finale"]
    for n in namen:
        datei = next((quelle / f"{n}.{e}" for e in ("jpg", "jpeg", "png") if (quelle / f"{n}.{e}").exists()), None)
        if not datei:
            print("fehlt:", n); continue
        with Image.open(datei) as b:
            b = ImageOps.exif_transpose(b).convert("RGB")
            box = rand_finden(b)
            innen = b.crop(box)
            groesse = GROESSE["tag" if n.startswith("tag") else n]
            fertig = ImageOps.fit(innen, groesse, method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
            fertig.save(ZIEL / f"{n}.jpg", quality=82, optimize=True, progressive=True)
            print(f"{n}: Rand {box} -> {groesse}, {(ZIEL / f'{n}.jpg').stat().st_size // 1024} KB")

if __name__ == "__main__":
    main()
