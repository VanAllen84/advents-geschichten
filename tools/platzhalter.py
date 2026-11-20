#!/usr/bin/env python3
"""Erzeugt die Platzhalterbilder (nur bis die echten Bilder da sind).

  bilder/tag-01.jpg ... tag-24.jpg   900 x 450, Tagesnummer in Gold auf Tannengrün
  bilder/landing.jpg, bilder/finale.jpg   1100 x 575

Danach tools/pixel.py laufen lassen. Echte Bilder einfach mit denselben
Dateinamen darüberkopieren; dieses Skript dann nicht mehr ausführen.
"""
import random
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

GRUEN_OBEN = (18, 46, 34)
GRUEN_UNTEN = (6, 20, 14)
GOLD = (217, 180, 90)
GOLD_HELL = (255, 236, 176)
CREME = (230, 224, 207)

SCHRIFTEN = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
    "C:/Windows/Fonts/georgiab.ttf",
    "/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
]


def schrift(groesse):
    for pfad in SCHRIFTEN:
        if Path(pfad).exists():
            return ImageFont.truetype(pfad, groesse)
    return ImageFont.load_default(groesse)


def hintergrund(b, h, seed):
    bild = Image.new("RGB", (b, h))
    zeichner = ImageDraw.Draw(bild)
    for y in range(h):
        f = y / (h - 1)
        farbe = tuple(round(GRUEN_OBEN[i] * (1 - f) + GRUEN_UNTEN[i] * f) for i in range(3))
        zeichner.line([(0, y), (b, y)], fill=farbe)
    # warmer Lichtschein in der Mitte
    schein = Image.new("L", (b, h), 0)
    ImageDraw.Draw(schein).ellipse([b * 0.2, h * 0.05, b * 0.8, h * 0.95], fill=70)
    schein = schein.filter(ImageFilter.GaussianBlur(h // 5))
    bild = Image.composite(Image.new("RGB", (b, h), (120, 96, 40)), bild, schein)
    # kleine goldene Lichtpunkte, damit die verpixelten Fassungen Struktur haben
    zufall = random.Random(seed)
    punkte = Image.new("RGBA", (b, h), (0, 0, 0, 0))
    pz = ImageDraw.Draw(punkte)
    for _ in range(70):
        x, y, r = zufall.uniform(0, b), zufall.uniform(0, h), zufall.uniform(1.5, 5)
        a = zufall.randint(60, 200)
        pz.ellipse([x - r, y - r, x + r, y + r], fill=GOLD_HELL + (a,))
    punkte = punkte.filter(ImageFilter.GaussianBlur(1.2))
    bild.paste(punkte, (0, 0), punkte)
    return bild


def text_mittig(bild, text, groesse, farbe, y_anteil=0.5, schatten=True):
    zeichner = ImageDraw.Draw(bild)
    f = schrift(groesse)
    box = zeichner.textbbox((0, 0), text, font=f)
    x = (bild.width - (box[2] - box[0])) / 2 - box[0]
    y = bild.height * y_anteil - (box[3] - box[1]) / 2 - box[1]
    if schatten:
        zeichner.text((x + 3, y + 4), text, font=f, fill=(0, 0, 0))
    zeichner.text((x, y), text, font=f, fill=farbe)


def main():
    ordner = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "bilder"
    ordner.mkdir(parents=True, exist_ok=True)
    for tag in range(1, 25):
        bild = hintergrund(900, 450, tag)
        text_mittig(bild, str(tag), 230, GOLD, 0.47)
        text_mittig(bild, "Platzhalter", 26, CREME, 0.86, schatten=False)
        bild.save(ordner / f"tag-{tag:02d}.jpg", quality=86)
    for name, titel in (("landing", "Advent"), ("finale", "Frohe Weihnachten")):
        bild = hintergrund(1100, 575, name)
        text_mittig(bild, titel, 110 if name == "landing" else 92, GOLD, 0.46)
        text_mittig(bild, "Platzhalter", 28, CREME, 0.86, schatten=False)
        bild.save(ordner / f"{name}.jpg", quality=86)
    print("Platzhalterbilder erstellt in", ordner)


if __name__ == "__main__":
    main()
