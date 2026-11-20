#!/usr/bin/env python3
"""Erzeugt die App-Symbole der TEST-Fassung: die normalen Symbole mit einem roten Band „TEST“.

  icon-192.png          -> icon-test-192.png
  icon-512.png          -> icon-test-512.png
  apple-touch-icon.png  -> apple-touch-icon-test.png

Aufruf aus dem Hauptordner:  python3 tools/test-symbole.py
Braucht Pillow. Nach einer Änderung der normalen Symbole erneut ausführen.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HAUPT = Path(__file__).resolve().parent.parent
PAARE = [("icon-192.png", "icon-test-192.png"),
         ("icon-512.png", "icon-test-512.png"),
         ("apple-touch-icon.png", "apple-touch-icon-test.png")]
SCHRIFTEN = ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
             "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
             "C:/Windows/Fonts/arialbd.ttf",
             "/System/Library/Fonts/Supplemental/Arial Bold.ttf"]
ROT = (178, 34, 34)
WEISS = (255, 255, 255)


def schrift(groesse):
    for s in SCHRIFTEN:
        if Path(s).exists():
            return ImageFont.truetype(s, groesse)
    return ImageFont.load_default()


def main():
    for quelle, ziel in PAARE:
        bild = Image.open(HAUPT / quelle).convert("RGB")
        w, h = bild.size
        # Faktor 4 zeichnen und verkleinern = glatte Kanten
        f = 4
        gross = bild.resize((w * f, h * f), Image.LANCZOS)
        d = ImageDraw.Draw(gross)
        oben, unten = int(h * f * 0.64), int(h * f * 0.86)   # Band im unteren Drittel, innerhalb der sicheren Zone
        d.rectangle([0, oben, w * f, unten], fill=ROT)
        d.line([0, oben, w * f, oben], fill=WEISS, width=max(2, h * f // 90))
        d.line([0, unten, w * f, unten], fill=WEISS, width=max(2, h * f // 90))
        fs = int((unten - oben) * 0.78)
        sc = schrift(fs)
        text = "TEST"
        x0, y0, x1, y1 = d.textbbox((0, 0), text, font=sc)
        d.text(((w * f - (x1 - x0)) / 2 - x0, oben + (unten - oben - (y1 - y0)) / 2 - y0), text, font=sc, fill=WEISS)
        gross.resize((w, h), Image.LANCZOS).save(HAUPT / ziel, optimize=True)
        print("geschrieben:", ziel)


if __name__ == "__main__":
    main()
