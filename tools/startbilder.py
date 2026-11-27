#!/usr/bin/env python3
"""Erzeugt die Startbilder für das iPhone (start/start-BREITExHÖHE.png): dunkelgrüner Hintergrund (#07120e)
mit dem App-Symbol in der Mitte. Ohne sie zeigt das iPhone beim Öffnen der App vom Home-Bildschirm kurz einen
weißen Bildschirm. Die passenden <link rel="apple-touch-startup-image" …>-Zeilen stehen im <head> von index.html.

Aufruf aus dem Hauptordner:  python3 tools/startbilder.py      (braucht Pillow)
Neue iPhone-Größen: in GERAETE ergänzen und die ausgegebene <link>-Zeile in index.html übernehmen.
"""
from pathlib import Path
from PIL import Image, ImageDraw

HAUPT = Path(__file__).resolve().parent.parent
BG = (7, 18, 14)
# (CSS-Breite, CSS-Höhe, Pixeldichte, Geräte)
GERAETE = [(440, 956, 3, "iPhone 16/17 Pro Max"), (430, 932, 3, "iPhone 14 Pro Max, 15/16 Plus, 15 Pro Max"), (420, 912, 3, "iPhone Air"),
           (402, 874, 3, "iPhone 16/17 Pro, 17"), (393, 852, 3, "iPhone 14 Pro, 15, 15 Pro, 16"), (428, 926, 3, "iPhone 12/13 Pro Max, 14 Plus"),
           (390, 844, 3, "iPhone 12, 13, 14, 16e"), (375, 812, 3, "iPhone X, XS, 11 Pro, 12/13 mini"), (414, 896, 3, "iPhone XS Max, 11 Pro Max"),
           (414, 896, 2, "iPhone XR, 11"), (375, 667, 2, "iPhone SE (2./3.), 8")]


def main():
    icon = Image.open(HAUPT / "icon-512.png").convert("RGBA")
    (HAUPT / "start").mkdir(exist_ok=True)
    for w, h, d, name in GERAETE:
        W, H = w * d, h * d
        im = Image.new("RGB", (W, H), BG)
        g = int(120 * d)   # Symbol 120 CSS-Pixel groß, mit abgerundeten Ecken
        ic = icon.resize((g, g), Image.LANCZOS)
        m = Image.new("L", (g * 4, g * 4), 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, g * 4 - 1, g * 4 - 1], radius=int(g * 4 * 0.22), fill=255)
        m = m.resize((g, g), Image.LANCZOS)
        im.paste(ic, ((W - g) // 2, (H - g) // 2 - int(30 * d)), m)
        datei = f"start/start-{W}x{H}.png"
        im.save(HAUPT / datei, optimize=True)
        print(f'<link rel="apple-touch-startup-image" href="{datei}" media="(device-width: {w}px) and (device-height: {h}px) '
              f'and (-webkit-device-pixel-ratio: {d}) and (orientation: portrait)">  <!-- {name} -->')


if __name__ == "__main__":
    main()
