#!/usr/bin/env python3
"""Erzeugt aus den Tagesbildern die verpixelten Fassungen für die Türchen-Kacheln.

Für jedes bilder/tag-NN.jpg (NN = 01 bis 24) entstehen:
  bilder/pix-mid-NN.png   32 x 16 Pixel  (leicht verpixelt: heute, ausgelassen, Türflügel)
  bilder/pix-lock-NN.png  10 x 5 Pixel   (stark verpixelt: gesperrt)

Aufruf (aus dem Hauptordner des Kalenders):
  python3 tools/pixel.py
Optional mit anderem Bilderordner:
  python3 tools/pixel.py pfad/zu/bilder

Braucht Pillow (pip install pillow). Bilder, die nicht im Verhältnis 2:1 sind,
werden mittig auf 2:1 zugeschnitten, bevor sie verkleinert werden.
"""
import sys
from pathlib import Path

from PIL import Image, ImageOps

GROESSEN = {"mid": (32, 16), "lock": (10, 5)}


def main():
    ordner = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "bilder"
    if not ordner.is_dir():
        sys.exit(f"Ordner nicht gefunden: {ordner}")
    fehlt = []
    for tag in range(1, 25):
        nn = f"{tag:02d}"
        quelle = ordner / f"tag-{nn}.jpg"
        if not quelle.exists():
            fehlt.append(quelle.name)
            continue
        with Image.open(quelle) as bild:
            bild = ImageOps.exif_transpose(bild).convert("RGB")
            # zuerst mittig auf 2:1 zuschneiden, dann in zwei Schritten verkleinern (sauberere Farben)
            zweizueins = ImageOps.fit(bild, (bild.width, bild.width // 2), method=Image.Resampling.LANCZOS)
            for art, groesse in GROESSEN.items():
                klein = zweizueins.resize((groesse[0] * 8, groesse[1] * 8), Image.Resampling.LANCZOS)
                klein = klein.resize(groesse, Image.Resampling.BOX)
                klein.save(ordner / f"pix-{art}-{nn}.png", optimize=True)
        print(f"Tag {nn}: pix-mid-{nn}.png und pix-lock-{nn}.png erstellt")
    if fehlt:
        print("Fehlende Tagesbilder:", ", ".join(fehlt))


if __name__ == "__main__":
    main()
