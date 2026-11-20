#!/usr/bin/env python3
"""Erzeugt die Kalender-Termine erinnerung/1700.ics bis erinnerung/2100.ics.

Jede Datei enthält 24 Termine "Türchen 1" bis "Türchen 24" (1. bis 24. Dezember),
15 Minuten lang, mit Erinnerung direkt zum Beginn und Link zur Seite.
Adresse und Jahr kommen aus config.js. Aufruf aus dem Hauptordner:
  python3 tools/erinnerung.py
"""
import re
from pathlib import Path

HAUPT = Path(__file__).resolve().parent.parent
cfg = (HAUPT / "config.js").read_text(encoding="utf-8")
URL = re.search(r'SEITEN_URL:\s*"([^"]*)"', cfg).group(1)
JAHR = int(re.search(r"JAHR:\s*(\d{4})", cfg).group(1))
ZEITEN = ["1700", "1730", "1800", "1830", "1900", "1930", "2000", "2030", "2100"]

VTIMEZONE = """BEGIN:VTIMEZONE
TZID:Europe/Berlin
BEGIN:DAYLIGHT
TZOFFSETFROM:+0100
TZOFFSETTO:+0200
TZNAME:CEST
DTSTART:19700329T020000
RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU
END:DAYLIGHT
BEGIN:STANDARD
TZOFFSETFROM:+0200
TZOFFSETTO:+0100
TZNAME:CET
DTSTART:19701025T030000
RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU
END:STANDARD
END:VTIMEZONE"""


def esc(t):
    return t.replace("\\", "\\\\").replace(";", r"\;").replace(",", r"\,").replace("\n", r"\n")


def falten(zeile):
    # Zeilen länger als 75 Byte werden nach dem Kalender-Standard (RFC 5545) umbrochen
    teile, aktuell = [], ""
    for zeichen in zeile:
        grenze = 75 if not teile else 74
        if len((aktuell + zeichen).encode("utf-8")) > grenze:
            teile.append(aktuell)
            aktuell = ""
        aktuell += zeichen
    teile.append(aktuell)
    return "\r\n ".join(teile)


def ende(hhmm):
    h, m = int(hhmm[:2]), int(hhmm[2:]) + 15
    return f"{h + m // 60:02d}{m % 60:02d}"


def main():
    ordner = HAUPT / "erinnerung"
    ordner.mkdir(exist_ok=True)
    for zeit in ZEITEN:
        z = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Adventskalender//DE", "CALSCALE:GREGORIAN",
             "METHOD:PUBLISH", "X-WR-CALNAME:Adventskalender", VTIMEZONE]
        for tag in range(1, 25):
            datum = f"{JAHR}12{tag:02d}"
            z += [
                "BEGIN:VEVENT",
                f"UID:advent-{JAHR}-tuerchen-{tag:02d}-{zeit}@advents-geschichten",
                f"DTSTAMP:{JAHR}1101T000000Z",
                f"DTSTART;TZID=Europe/Berlin:{datum}T{zeit}00",
                f"DTEND;TZID=Europe/Berlin:{datum}T{ende(zeit)}00",
                f"SUMMARY:{esc(f'Türchen {tag}')}",
                f"DESCRIPTION:{esc('Heute wartet Türchen ' + str(tag) + ' auf dich: ' + URL)}",
                f"URL:{URL}",
                "TRANSP:TRANSPARENT",
                "BEGIN:VALARM", "ACTION:DISPLAY", f"DESCRIPTION:{esc(f'Türchen {tag}')}", "TRIGGER:PT0M", "END:VALARM",
                "END:VEVENT",
            ]
        z.append("END:VCALENDAR")
        zeilen = "\n".join(z).split("\n")
        text = "\r\n".join(falten(x) for x in zeilen) + "\r\n"
        (ordner / f"{zeit}.ics").write_bytes(text.encode("utf-8"))
    print(f"{len(ZEITEN)} Dateien in {ordner} (Link: {URL})")


if __name__ == "__main__":
    main()
