#!/usr/bin/env python3
"""Gleicht die Töne des Kalenders auf dieselbe Lautheit an (ca. −18 LUFS) und schreibt sie nach ton/.

Warum in der Datei und nicht per Skript? Das iPhone ignoriert eine Lautstärke, die die Seite
per JavaScript setzt (audio.volume). Gleich laut werden die Töne nur, wenn die Dateien es sind.

Ablauf je Datei:
  1. Lautheit messen (EBU R128, „integrated loudness“)
  2. Verstärkung so wählen, dass −18 LUFS herauskommen
  3. Limiter (Spitzen höchstens ca. −2 dBFS), damit nichts übersteuert
  4. als MP3 speichern (44,1 kHz, Stereo, 160 kbit/s) und nachmessen, ggf. nachregeln
  zuklappen.mp3 bekommt vorn 0,33 s Stille: Der Ton wird gleich beim Tippen gestartet
  (sonst spielt das iPhone ihn evtl. nicht), soll aber erst mit dem Schließen der Tür hörbar sein.

Aufruf aus dem Hauptordner:
  python3 tools/toene-angleichen.py            (liest ton-roh/*.mp3, schreibt ton/*.mp3)
  python3 tools/toene-angleichen.py quellordner
Braucht ffmpeg. Den Ordner ton-roh/ nicht ins Repository hochladen.
"""
import re
import subprocess
import sys
from pathlib import Path

HAUPT = Path(__file__).resolve().parent.parent
ZIEL_LUFS = -18.0
VORLAUF_MS = {"zuklappen": 330}


def messen(datei):
    e = subprocess.run(["ffmpeg", "-nostats", "-i", str(datei), "-af", "ebur128=peak=true:framelog=quiet",
                        "-f", "null", "-"], capture_output=True, text=True).stderr
    i = float(re.search(r"Integrated loudness:\s+I:\s+(-?[\d.]+)", e).group(1))
    tp = float(re.search(r"True peak:\s+Peak:\s+(-?[\d.]+|-inf)", e).group(1))
    return i, tp


def main():
    quelle = Path(sys.argv[1]) if len(sys.argv) > 1 else HAUPT / "ton-roh"
    ziel = HAUPT / "ton"
    ziel.mkdir(exist_ok=True)
    dateien = sorted(quelle.glob("*.mp3"))
    if not dateien:
        sys.exit("Keine MP3-Dateien in " + str(quelle))
    print("%-16s %10s %10s   %10s %10s" % ("Datei", "vorher I", "vorher TP", "nachher I", "nachher TP"))
    for d in dateien:
        i0, tp0 = messen(d)
        gain = ZIEL_LUFS - i0
        aus = ziel / d.name
        for _ in range(3):
            vor = VORLAUF_MS.get(d.stem)
            af = (f"adelay={vor}|{vor}," if vor else "") + \
                 f"aresample=44100,volume={gain:.2f}dB,alimiter=limit=0.79:attack=2:release=60:level=false"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(d), "-af", af, "-ar", "44100", "-ac", "2",
                            "-c:a", "libmp3lame", "-b:a", "160k", "-map_metadata", "-1", str(aus)], check=True)
            i1, tp1 = messen(aus)
            if abs(i1 - ZIEL_LUFS) <= 0.3:
                break
            gain += ZIEL_LUFS - i1
        print("%-16s %6.1f LUFS %6.1f dBTP   %6.1f LUFS %6.1f dBTP" % (d.name, i0, tp0, i1, tp1))


if __name__ == "__main__":
    main()
