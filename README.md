# Adventsgeschichten – ein privater Adventskalender mit 24 Geschichten

Ein statischer Adventskalender aus HTML, CSS und JavaScript, ohne Server-Logik, ohne Datenbank und ohne Anmeldung.
Vom 1. bis 24. Dezember öffnet sich jeden Tag ein Türchen, hinter jedem steht eine weihnachtliche Geschichte mit Bild.
Nach Türchen 24 folgt ein Finale.

Der Kalender ist für mehrere Personen gedacht. Es gibt keinen festen Empfängernamen, die Anrede ist durchgehend „du“.
Der Absender steht in `config.js` (`ABSENDER`) und erscheint nur in der Signatur der Finale-Seite.

| | Adresse |
|---|---|
| **LIVE** | https://adventsgeschichten.tkagel.de/ |
| **TEST** | https://adventsgeschichten.tkagel.de/test/ |
| GitHub-Repository | `vanallen84/advents-geschichten` |
| Alte GitHub-Adresse (leitet weiter) | https://vanallen84.github.io/advents-geschichten/ |

Stand dieser Beschreibung: November 2026, Service-Worker-Version `advent-v19`.

---

## Inhalt

1. [Schnellstart: Was muss ich nächstes Jahr tun?](#1-schnellstart-was-muss-ich-nächstes-jahr-tun)
2. [Dateien im Überblick](#2-dateien-im-überblick)
3. [Einstellungen (config.js)](#3-einstellungen-configjs)
4. [LIVE- und TEST-Fassung](#4-live--und-test-fassung)
5. [Datum und Freischaltung der Türchen](#5-datum-und-freischaltung-der-türchen)
6. [Ablauf für die Leser](#6-ablauf-für-die-leser)
7. [Die Seiten im Einzelnen](#7-die-seiten-im-einzelnen)
8. [Animationen](#8-animationen)
9. [Bilder](#9-bilder)
10. [Geschichten](#10-geschichten)
11. [Kalender-Erinnerungen (.ics)](#11-kalender-erinnerungen-ics)
12. [Was im Browser gespeichert wird](#12-was-im-browser-gespeichert-wird)
13. [Offline-Fähigkeit und Updates (Service Worker)](#13-offline-fähigkeit-und-updates-service-worker)
14. [Als App auf dem Startbildschirm](#14-als-app-auf-dem-startbildschirm)
15. [Hosting: GitHub Pages und eigene Domain](#15-hosting-github-pages-und-eigene-domain)
16. [Werkzeuge im Ordner tools/](#16-werkzeuge-im-ordner-tools)
17. [Testen](#17-testen)
18. [Besonderheiten, Stolperfallen und Lösungen](#18-besonderheiten-stolperfallen-und-lösungen)
19. [Interne Schalter für Entwickler](#19-interne-schalter-für-entwickler)
20. [Wichtige Funktionen in index.html](#20-wichtige-funktionen-in-indexhtml)
21. [Verlauf der Änderungen](#21-verlauf-der-änderungen)
22. [Rechtliches zu Texten und Bildern](#22-rechtliches-zu-texten-und-bildern)
23. [Name und Online-Sicherung](#23-name-und-online-sicherung)

---

## 1. Schnellstart: Was muss ich nächstes Jahr tun?

Wenn der Kalender in einem neuen Jahr wieder laufen soll:

1. **config.js:** `JAHR` auf das neue Jahr setzen.
   Dadurch ändert sich auch der Speicher-Präfix (`weihnacht2027_` …), alle Leser beginnen also mit einem leeren Kalender.
   Auch die Online-Sicherung beginnt leer, weil das Jahr im Online-Schlüssel steckt. `SYNC_ZUSATZ` und `SYNC_URL` bleiben, wie sie sind.
2. **Neue Geschichten (optional):** `story-day1.js` bis `story-day24.js` ersetzen (Format siehe [Abschnitt 10](#10-geschichten)).
3. **Neue Bilder (optional):** Rohbilder in `bilder-roh/` legen, dann
   ```bash
   python3 tools/bilder-vorbereiten.py
   python3 tools/pixel.py
   ```
4. **Kalender-Termine neu erzeugen**, weil das Jahr in den Terminen steckt:
   ```bash
   python3 tools/erinnerung.py
   ```
5. **sw.js:** `VERSION` hochzählen (z. B. `advent-v12`). Ohne diesen Schritt sehen Handys, die die Seite schon kennen, womöglich alte Bilder.
6. Alle geänderten Dateien ins Repository hochladen.
7. Im November über die **TEST-Fassung** (`/test/`) prüfen. Dort zählt der November wie der Dezember.
8. Mit `…/test/?reset=1` den eigenen Test-Stand jederzeit zurücksetzen.

Für den Inhalt der Startseite, das Finale und die Begrüßungssätze muss man in `index.html` suchen (siehe [Abschnitt 7](#7-die-seiten-im-einzelnen)).

---

## 2. Dateien im Überblick

```
/
├── index.html            Die ganze Seite: HTML, CSS und JavaScript in einer Datei
├── config.js             Einstellungen (Jahr, Absender, Adresse …)
├── sw.js                 Service Worker: Offline-Speicher und Updates
├── manifest.json         App-Manifest für die LIVE-Fassung
├── manifest-test.json    App-Manifest für die TEST-Fassung
├── icon-192.png          App-Symbol
├── icon-512.png          App-Symbol (groß)
├── apple-touch-icon.png  App-Symbol für iPhone/iPad
├── icon-test-192.png, icon-test-512.png, apple-touch-icon-test.png
│                         dieselben Symbole mit rotem Band „TEST“ (TEST-Fassung)
├── story-day1.js … story-day24.js   Die 24 Geschichten
├── bilder/
│   ├── landing.jpg       Bild der Startseite (1200×600)
│   ├── finale.jpg        Bild der Finale-Seite (1200×600)
│   ├── tag-01.jpg … tag-24.jpg       Tagesbilder (1200×600)
│   ├── pix-mid-01.png … pix-mid-24.png    leicht verpixelt (32×16 Pixel)
│   └── pix-lock-01.png … pix-lock-24.png  stark verpixelt (10×5 Pixel)
├── ton/                  alle Töne, auf ca. −18 LUFS angeglichen
│   ├── knarren.mp3       Tür geht auf (Portal)
│   ├── zuklappen.mp3     Tür schließt sich (Zurück in die Übersicht)
│   ├── wirbel.mp3        Buchstaben-Wirbel
│   ├── finale.mp3        Finale „Die 24 Lichter“
│   └── umschlag.mp3      Umschlag wird geöffnet (nach dem Finale)
├── erinnerung/
│   └── 1700.ics … 2100.ics   Kalender-Termine, je eine Datei pro Uhrzeit
├── test/
│   └── index.html        Weiterleitung auf index.html?test=1
└── tools/
    ├── bilder-vorbereiten.py   Rohbilder zuschneiden und verkleinern
    ├── pixel.py                Verpixelte Kachel-Bilder erzeugen
    ├── erinnerung.py           .ics-Dateien erzeugen
    ├── test-symbole.py         Erzeugt die TEST-Symbole mit rotem Band
    ├── toene-angleichen.py     Gleicht die Töne auf −18 LUFS an (braucht ffmpeg)
    ├── bild-prompts.md         Die 26 Gemini-Prompts für die Bilder
    └── platzhalter.py          VERALTET: erzeugte Platzhalterbilder, nicht mehr ausführen
```

Es gibt keinen Build-Schritt und keine Abhängigkeiten.
Die Seite funktioniert direkt so, wie die Dateien im Repository liegen.

Der Kalender basiert auf einem älteren Kalender (mit index.html, sw.js, manifest.json und story-day1.js).
Code und Animationen wurden so weit wie möglich übernommen und dann erweitert.

---

## 3. Einstellungen (config.js)

```js
window.ADVENT_CONFIG = {
  EMPFAENGER_NAME: "",                 // leer = der Name, den die Person selbst eingibt (freiwillig)
  ABSENDER: "Vorname",                 // erscheint in der Finale-Signatur
  JAHR: 2026,                          // Jahr, in dem die Türchen im Dezember aufgehen
  SEITEN_URL: "https://adventsgeschichten.tkagel.de/",  // für die Links in den .ics-Terminen
  KALENDER_TITEL: "Dein Adventskalender",               // Überschrift der Startseite (ohne Namen)
  SYNC_URL: "https://advent-stand.….workers.dev",       // Online-Sicherung; leer = aus
  SYNC_ZUSATZ: "…",                    // fester Zufallswert für den Online-Schlüssel – NIE ändern
  VORTEST_NOVEMBER: false              // false = LIVE (immer so lassen!)
};
```

- **EMPFAENGER_NAME:** Rückfall für den Namen der lesenden Person. Normalerweise leer: Dann gilt der Vorname, den die Person auf der Startseite selbst eingibt (siehe [Abschnitt 23](#23-name-und-online-sicherung)).
  In den Begrüßungssätzen steht an einigen Stellen `{name}`.
  - Ist ein Name bekannt, wird `{name}` ersetzt.
  - Ist das Feld leer, verschwindet `{name}` samt Komma (Funktion `mitName`).
  - Aus „Guten Morgen, {name}. …“ wird dann „Guten Morgen. …“.
- **ABSENDER:**
  - Erscheint als Unterschrift unter dem Brief auf der Finale-Seite.
  - Die Zeile unter der Überschrift der Startseite ist **fest** „Von mir, nur für dich!“ und hängt nicht von `ABSENDER` ab.
- **JAHR:** Steuert die Freischaltung, den Speicher-Präfix und die .ics-Termine (über `tools/erinnerung.py`).
- **SEITEN_URL:** Wird nur von `tools/erinnerung.py` gelesen und in die Termine geschrieben. Nach einer Änderung die .ics-Dateien neu erzeugen.
- **SYNC_URL:** Adresse des eigenen Cloudflare-Workers „advent-stand“ für die Online-Sicherung. Leer = keine Online-Sicherung (der Name personalisiert trotzdem).
- **SYNC_ZUSATZ:** fester Zufallswert (einmalig erzeugt). Zusammen mit Jahr und Vorname ergibt er den Online-Schlüssel. **Nie ändern**, sonst sind gesicherte Stände nicht mehr auffindbar.
- **VORTEST_NOVEMBER:** Wenn `true`, zählt der November **auch auf der LIVE-Adresse** als Dezember.
  - Das war früher der Weg zum Testen.
  - Heute gibt es dafür die TEST-Fassung, deshalb bleibt der Wert immer `false`.

Fehlt `config.js` oder ein Wert darin, nimmt `index.html` sichere Standardwerte.

---

## 4. LIVE- und TEST-Fassung

Beide Fassungen sind **dieselben Dateien**. Unterschieden wird nur über den Adress-Zusatz `?test=1`.

| | LIVE | TEST |
|---|---|---|
| Aufruf | `/` bzw. `/index.html` | `/test/` → leitet auf `/index.html?test=1` |
| Datum | echtes Datum | **November wird wie Dezember behandelt** (1. Nov. = Türchen 1 usw.) |
| Speicher | `weihnacht2026_…` | `weihnacht2026_test_…` (völlig getrennt) |
| Kennzeichen | – | kleines Schild „TEST“ oben links |
| App-Manifest | `manifest.json` („Advent“) | `manifest-test.json` („Advent (Test)“) |
| App-Symbol | goldener Stern | goldener Stern mit rotem Band „TEST“ |

- **`test/index.html`** ist nur eine Weiterleitung.
  - Ein angehängtes `?reset=1` wird mitgenommen: `/test/?reset=1` → `/index.html?test=1&reset=1`.
- **`?reset=1`** löscht den gespeicherten Stand der jeweiligen Fassung.
  - Gelöscht werden: geöffnete Türchen, Lesepositionen, Begrüßungs-Verlauf, „Finale gesehen“, „schon mal besucht“, gespeicherte Titel, Lieblingsgeschichten, Schriftgröße, Name.
  - War ein Name eingegeben und ist die Online-Sicherung eingerichtet, wird auch dessen **Online-Stand** dieser Fassung gelöscht (sonst käme er beim nächsten Abgleich zurück).
  - Danach wird der Zusatz aus der Adresszeile entfernt, damit ein Neuladen nicht erneut löscht.
- **Wichtig:** Im Dezember verhält sich die TEST-Fassung wie die LIVE-Fassung, nur mit eigenem Speicher.
  Zum Vorab-Testen also immer im November nutzen.

---

## 5. Datum und Freischaltung der Türchen

- Maßgeblich ist **das Datum auf dem Gerät** des Lesers (`new Date()`), nicht eine Serverzeit.
- Türchen N ist ab **dem N. Dezember um 0:00 Uhr** Gerätezeit frei.
- Vor dem 1. Dezember sind alle Türchen gesperrt.
- **Ab dem 25. Dezember** (und in allen späteren Jahren) sind alle 24 Türchen frei.
  - Nie geöffnete Türchen tragen dann „Noch ungeöffnet“.
  - Schon gelesene Türchen zeigen ihr Bild und ihren Titel.
- Die Funktion `jetzt()` liefert das Datum. In der TEST-Fassung macht sie aus November den Dezember.
- **Datumswechsel bei offener Seite:**
  - Kommt die Seite aus dem Hintergrund zurück (App-Wechsel, Tab-Wechsel, Fokus) und ist inzwischen ein anderer Tag, lädt sie sich neu.
  - So erscheint das neue Türchen, ohne dass man die App schließen muss.
- Ein Hinweis auf der Startseite erklärt: Wenn sich ein Türchen nicht öffnet, obwohl sein Tag da ist, stimmt vermutlich das Datum auf dem Handy nicht.

---

## 6. Ablauf für die Leser

```
Startseite ──„Zu den Türchen“──▶ Türchen-Übersicht
                                   │  Tipp auf ein freies Türchen
                                   ▼
                     Portal-Animation (Tür geht auf)
                                   │
          ┌── erstes Öffnen ───────┴────── schon einmal geöffnet ──┐
          ▼                                                        ▼
   Einstimmungsseite                                          Geschichte
   (Titel + ein Satz zur Einstimmung)                              ▲
          │ „Geschichte beginnen“                                  │
          ▼                                                        │
   Buchstaben-Wirbel ──────────────────────────────────────────────┘
                                   │
          „Weiter durch das nächste Türchen …“  → Portal → nächstes Türchen
          bei Türchen 24: „Zum Finale …“        → Finale-Animation → Finale-Seite
```

- **Gesperrtes Türchen antippen:** Die Kachel wackelt kurz, das Schloss pulsiert.
  Dann erscheint das Fenster „Geduld … Dieses Türchen öffnet sich am N. Dezember. Bis dahin darf die Vorfreude noch ein wenig wachsen.“ mit dem Knopf „Bis bald“.
- **„Weiter durch das nächste Türchen“** erscheint unter einer Geschichte nur, wenn das nächste Türchen schon frei ist.
  - Bei Türchen 24 heißt der Knopf „Zum Finale …“.
- **Knopf „Zurück zur Türchen-Auswahl“** auf Einstimmung und Geschichte: Die Tür schließt sich wieder auf ihrer Kachel (siehe [8.2](#82-tür-schließt-sich--zurück-in-die-übersicht-portalzurueck)). Auf der Finale-Seite geht es ohne Animation zurück.
- **Zurück-Geste (Wischen/Zurück-Taste):**
  - Auf Einstimmung, Geschichte und Finale führt sie **sofort** (ohne Tür-Animation) zurück in die Übersicht und verlässt die Seite nicht.
  - Während einer Animation wird die Geste ignoriert.
- **Antippen überspringt Animationen** (Portal, Zuklappen, Wirbel, Finale).

---

## 7. Die Seiten im Einzelnen

Alle Seiten liegen als `<div>`-Bereiche in `index.html` und werden über die Klasse `hidden` ein- und ausgeblendet.

| ID | Seite |
|---|---|
| `landingScreen` | Startseite |
| `calendar-overview` | Türchen-Übersicht |
| `einstimmungScreen` | Einstimmung |
| `storyScreen` | Geschichte |
| `finaleScreen` | Finale |
| `lock-modal` | Fenster für gesperrte Türchen |

### 7.1 Startseite

- **Überschrift:** mit Namen „Annas Adventskalender“ (bei Namen auf s, ß, x, z: „Klaus’ Adventskalender“), sonst `KALENDER_TITEL`. Darunter fest **„Von mir, nur für dich!“**.
- **Namenskarte** (nur solange kein Name eingegeben und nicht „Ohne Namen weiter“ gewählt wurde): „Schön, dass du da bist! Wie heißt du?“ mit Feld, Knopf „Los geht’s“, Hinweis zur Online-Sicherung (nur wenn `SYNC_URL` gesetzt) und „Ohne Namen weiter“. Danach kurz „Schön, dass du da bist, Anna!“ bzw. „Willkommen zurück, Anna! Dein Fortschritt ist wieder da.“
- **Ganz unten:** „Nicht Anna? Namen ändern“ bzw. „Namen eingeben“.
- **Countdown:** nur vor dem 1. Dezember und höchstens 60 Tage vorher.
  - Text: „Noch N Tage, dann öffnet sich das erste Türchen.“ bzw. „Morgen öffnet sich das erste Türchen.“
  - In der TEST-Fassung zählt er bis zum 1. November.
- **Bild** `bilder/landing.jpg`: blendet langsam ein, sobald es im sichtbaren Bereich ist, und bei jeder Rückkehr zur Startseite erneut.
- **Begrüßungstext** („Willkommen in deinem Adventskalender …“).
- **Karte „Bevor es losgeht“** mit zwei Schritten:
  1. **Auf den Startbildschirm legen.**
     - Es wird nur die passende Anleitung gezeigt: iPhone (Safari) oder Android (Chrome).
     - Läuft der Kalender schon als installierte App, entfällt dieser Schritt ganz, und die Erinnerung wird zu Schritt 1.
  2. **Erinnerung:** Uhrzeit wählen (17:00 bis 21:00 im Halbstundentakt, vorausgewählt 20:00), dann „Termine hinzufügen“ → lädt `erinnerung/HHMM.ics` (siehe [Abschnitt 11](#11-kalender-erinnerungen-ics)).
  - Beim **ersten Besuch** ist die Karte offen.
  - **Ab dem zweiten Besuch** ist sie eingeklappt (▾). Ein Tipp auf die Überschrift klappt sie auf (▴).
- **Kasten „So funktioniert’s“** (drei Schritte):
  - Wird eingeklappt, sobald mindestens ein Türchen geöffnet wurde.
  - Lässt sich ebenfalls per Tipp aufklappen.
- Knopf **„Zu den Türchen“**.

### 7.2 Türchen-Übersicht

- Überschrift „Wähle das heutige Türchen“.
- **Begrüßungssatz** unter der Überschrift, abhängig von der Tageszeit (mit Namen, wo der Satz `{name}` enthält):
  - morgens 5–11 Uhr, mittags 11–17 Uhr, abends 17–22 Uhr, nachts 22–5 Uhr.
  - Je Tageszeit gibt es 8 Sätze (Liste `BEGRUESSUNG` in index.html). Die Sätze sind Eigenformulierungen.
  - Pro Tag und Tageszeit gilt ein fester Satz; er bleibt den ganzen Tag gleich.
  - Jeder Satz kommt höchstens 3-mal vor und nie an zwei Tagen hintereinander.
    Umgesetzt mit einem gemischten „Beutel“, in dem jeder Satz dreimal liegt (`begruessungWaehlen`).
- **24 Kacheln**, zwei Spalten auf dem Handy, drei ab 600 px Breite.
  - Beim Öffnen der Übersicht wird zur Kachel des heutigen Tages gescrollt (nur 1.–24. Dezember).
- **Zustände der Kacheln:**

  | Zustand | Aussehen |
  |---|---|
  | **gesperrt** (Tag noch nicht erreicht) | Bild **stark verpixelt** (`pix-lock`, 10×5), dunkel, halb durchsichtig, Schloss 🔒 oben rechts |
  | **heute**, noch nicht geöffnet | Bild **leicht verpixelt** (`pix-mid`, 32×16), goldener Rahmen, pulsierendes Leuchten, Lichtwelle, Schriftzug „HEUTE“ |
  | **frühere Tage, nie geöffnet** | leicht verpixelt, goldener Rahmen, Leuchten, Lichtwelle, „NOCH UNGEÖFFNET“ |
  | **geöffnet** | Bild **scharf**, goldener Rahmen, unten abgedunkelt, **Titel der Geschichte** kursiv (bis zu 3 Zeilen), Nummer etwas nach oben gerückt |
  | ab 25.12., geöffnet (`frei`) | wie geöffnet, aber mit grauem Rahmen |
  | ab 25.12., nie geöffnet | wie „frühere Tage, nie geöffnet“ |

  - Die Lichtwellen laufen zeitversetzt über die Kacheln (CSS-Variable `--sw`).
  - Als „geöffnet“ gilt ein Türchen erst, wenn **die Geschichte selbst** geladen wurde. Wer nur die Einstimmungsseite gesehen hat, hat das Türchen noch nicht geöffnet.
- **Titel auf den Kacheln:**
  - Der Titel wird beim Laden einer Geschichte gespeichert (Speicher-Schlüssel `titel`).
  - Fehlt ein Titel (z. B. bei Türchen, die vor dieser Funktion geöffnet wurden), holt die Seite ihn selbst aus `story-dayN.js` (Funktion `titelNachladen`).
- Knopf **„Zum Finale“**: sichtbar ab dem 25. Dezember oder sobald Türchen 24 geöffnet wurde. Beim **allerersten** Aufruf der Finale-Seite (egal ob über diesen Knopf oder nach Türchen 24) laufen Finale-Animation und Umschlag, danach geht es direkt zum Brief.
- Kacheln von **Lieblingsgeschichten** tragen oben links einen goldenen Stern ★.
- Knopf „Zurück zur Startseite“.

### 7.3 Einstimmungsseite

- Erscheint **nur beim ersten Öffnen** eines Türchens.
- Zeigt „Türchen N“, den Titel und einen kurzen Einstimmungssatz (`einstimmung` aus der Geschichten-Datei).
- Der Knopf **„Geschichte beginnen“** erscheint erst, wenn die Geschichte geladen ist; dann folgt der Buchstaben-Wirbel.
- Im Hintergrund liegt schwach und unscharf das Tagesbild als Wasserzeichen (`wmAnker`).

### 7.4 Geschichte

- „Türchen N“, Titel, Text (Absätze), darunter **„Quelle: …“** in kleiner Schrift.
- Darunter das **Tagesbild**. Es blendet langsam ein (4 s), sobald man beim Lesen dort ankommt.
- Auch hier liegt das Tagesbild schwach als Wasserzeichen im Hintergrund.
- **Lese-Leiste** unter dem Titel:
  - **A− / A+:** Schriftgröße in fünf Stufen (90 %, 100 %, 112 %, 125 %, 140 % von 1,05 rem), pro Gerät gemerkt (Schlüssel `schrift`). Der Absatz, der gerade oben steht, bleibt beim Umschalten an seiner Stelle.
  - **🔈 Vorlesen:** liest Titel und Text mit der Sprachausgabe des Geräts vor (`VORLESEN`).
    - Deutsche Stimme; bevorzugt eine „Premium“/„Verbessert“-Stimme, wenn auf dem Gerät installiert (iPhone: Einstellungen → Bedienungshilfen → Gesprochene Inhalte → Stimmen). Tempo 0,95.
    - Der Text wird in Stücke von höchstens ca. 220 Zeichen an Satzgrenzen zerlegt, weil manche Browser lange Texte sonst abbrechen.
    - Der gerade gelesene Absatz wird leicht golden hinterlegt; die Seite scrollt mit, wenn er aus dem Bild läuft.
    - „■ Vorlesen anhalten“ merkt sich den Absatz; der Knopf heißt dann „🔈 Weiter vorlesen“ und macht dort weiter. Wer die Geschichte verlässt oder sie zu Ende hört, beginnt beim nächsten Mal von vorn.
    - Beim Seitenwechsel und wenn die App in den Hintergrund geht, wird das Vorlesen angehalten.
    - Gibt es auf dem Gerät keine Sprachausgabe, ist der Knopf ausgeblendet. Die Qualität hängt vom Gerät ab und klingt teils mechanisch.
- **Lieblingsgeschichte:** Knopf „☆ Zu den Lieblingen“ / „★ Lieblingsgeschichte“ unter der Geschichte (Schlüssel `lieblinge`).
- **Lesefortschritt:** dünner goldener Balken ganz oben.
- **Leseposition:**
  - Wird beim Scrollen gespeichert und beim erneuten Öffnen **innerhalb von 12 Stunden** wiederhergestellt.
  - Ganz oben (unter 2 %) und ganz unten (über 97 %) wird nichts gespeichert. Wer zu Ende gelesen hat, fängt beim nächsten Mal oben an.
- **Bildschirm bleibt an**, solange eine Geschichte offen ist (Wake Lock, wo das Gerät es unterstützt).
- **Fehler beim Laden:** Meldung „Dieses Türchen lässt sich gerade nicht laden …“ mit Knopf „Nochmal versuchen“.
  Der Knopf lädt die Datei mit einem Zusatz (`?n=1`, `?n=2` …) neu, damit kein veralteter Speicher dazwischenfunkt.

### 7.5 Finale

- Erscheint nach Türchen 24 („Zum Finale …“) oder über den Knopf in der Übersicht.
- Gestaltet als **Brief auf altem Briefpapier** aus **zwei Briefbögen** (`#finaleBrief` mit zwei `.brief`): vergilbter Papierton mit Flecken, dunkle Ränder, feiner Innenrahmen, Faltkante in der Mitte, Seitenzahl „– 1 –“/„– 2 –“.
  - Die Bögen liegen **untereinander**, leicht überlappend und gegeneinander verdreht (Bogen 1 −0,3°, Bogen 2 +0,45°); man liest sie durch normales Scrollen.
  - Aufteilung nach Absätzen, damit kein Satz über zwei Bögen läuft: Bogen 1 = Überschrift und Absätze 1–2, Bogen 2 = Absätze 3–5 und Unterschrift.
  - Ein einzelnes, sehr langes Blatt wirkte unnatürlich; eine Schriftrolle passte nicht zum Umschlag.
  - Brieftext in Serifenschrift (Georgia), passend zum alten Briefpapier.
- **„Deine Lieblingsgeschichten“:** ein kleiner Zettel unter dem Brief mit Nummer und Titel aller gemerkten Geschichten. Antippen öffnet die Geschichte (mit Tür-Animation). Ohne Lieblinge wird der Zettel nicht gezeigt.
- Darin: Überschrift „Frohe Weihnachten!“ bzw. mit Namen „Frohe Weihnachten, Anna!“ (`#finaleGruss`), fünf Absätze Brieftext (vom Absender selbst geschrieben, November 2026), linksbündig mit Silbentrennung, darunter rechts der Name aus `ABSENDER` als Unterschrift. Ist `ABSENDER` leer, entfällt die Unterschrift.
- Bild `bilder/finale.jpg`.
- Knopf **„✨ Die Animation noch einmal ansehen“**.

### 7.6 Browser-Tab und Statusleiste

Titel und Symbol im Browser-Tab passen sich der Seite an:

| Seite | Titel | Symbol |
|---|---|---|
| Startseite | „Advent“ | Kerze |
| Übersicht | „Die Türchen“ | vier Kacheln |
| Einstimmung/Geschichte | „N. Dezember“ | Kalenderblatt mit Tageszahl |
| Finale | „Frohe Weihnachten“ | Stern |

Die Farbe der Browserleiste (`theme-color`) folgt dem Hintergrund.
Bei jedem Seitenwechsel wird nach oben gescrollt.

---

## 8. Animationen

Alle Animationen lassen sich durch Antippen überspringen.
Ist am Gerät „Bewegung reduzieren“ eingestellt (`prefers-reduced-motion`), entfallen sie ganz.

### 8.1 Portal – das Türchen geht auf (`portalDurch`)

- Startet beim Antippen eines freien Türchens und beim Knopf „Weiter durch das nächste Türchen“.
  - Beim Knopf gibt es keine Kachel auf dem Bildschirm. Das Portal startet dann mit einer gleich großen gedachten Kachel in der Bildschirmmitte.
- **Aufbau:**
  - Hinten ein goldenes Leuchten.
  - Davor eine Zeichenfläche (Canvas) mit dem Tagesbild.
  - Davor zwei Türflügel, die zusammen das Bild der Kachel zeigen.
- **Noch nie geöffnetes Türchen** (etwa 4,6 s):

  | Zeit | Was passiert |
  |---|---|
  | 0–0,25 s | Hintergrund wird schwarz, Tür zeigt das **leicht verpixelte** Bild |
  | 0,25–1,45 s | Die beiden Flügel klappen nach außen auf |
  | 1,5–3,5 s | Das Bild hinter der Tür wird in 9 Stufen **scharf** (32 → 42 → 56 → 76 → 104 → 144 → 200 → 280 → 400 Spalten → Original) |
  | ab 3,65 s | **Zoom** ins Bild, dabei Ausblenden |
  | ca. 4,6 s | Wechsel zur Einstimmungsseite |

- **Schon geöffnetes Türchen** (etwa 2,5 s):
  - Die Tür zeigt das scharfe Bild und klappt auf.
  - Ab 1,5 s wird sofort gezoomt, das Entpixeln entfällt.
  - Dann geht es direkt zur Geschichte.
- **Zeitsteuerung:** über die CSS-Variablen `--zd` (Beginn des Zooms) und `--fd` (Beginn des Ausblendens), die das Skript je nach Fall setzt.
- **Bild lädt nicht:** Dann gibt es nur das goldene Portal ohne Bild.

### 8.2 Tür schließt sich – zurück in die Übersicht (`portalZurueck`)

- Startet über die Knöpfe **„Zurück zur Türchen-Auswahl“** auf der Einstimmungsseite und unter der Geschichte.
  **Nicht** bei der Zurück-Wischgeste (die bleibt sofort) und nicht auf der Finale-Seite.
- **Ablauf** (etwa 1,9 s):

  | Zeit | Was passiert |
  |---|---|
  | 0–0,25 s | Bildschirm wird schwarz, Ton `zuklappen.mp3` startet (hörbar ab ca. 0,33 s) |
  | 0,26 s | Übersicht wird darunter eingeblendet, die Kachel des Türchens wird **in die Bildschirmmitte** gescrollt |
  | 0,34–1,3 s | Das Bild schrumpft vom Vollbild auf die Größe der Kachel |
  | 0,73–1,33 s | Die beiden Flügel schließen sich |
  | 1,38–1,9 s | Schwarz blendet aus, die Übersicht ist zu sehen |

- **Bild auf der Tür:** genau das, was die Kachel danach zeigt. Wurde die Geschichte gelesen, ist es scharf. Ging es von der Einstimmung zurück (Geschichte noch nicht gelesen), bleibt es **leicht verpixelt**.
- **Scrollen:** Beim Seitenwechsel scrollt die Seite automatisch nach oben (MutationObserver), und die Übersicht scrollt sonst nach 160 ms zum heutigen Türchen.
  Während des Zuklappens ist das zweite abgeschaltet (`window.__zuKeinScroll`); die Kachel wird erst im nächsten `requestAnimationFrame` mittig gescrollt, also nach dem automatischen Hochscrollen.
- Wird „Zurück“ getippt, während die Öffnen-Animation noch ausblendet (ca. 0,7 s), geht es ohne Zuklappen zurück.

### 8.3 Buchstaben-Wirbel – von der Einstimmung zur Geschichte (`wirbelUebergang`)

- Nach „Geschichte beginnen“ lösen sich **alle Buchstaben der Einstimmungsseite** (bis zu 640) und beginnen zu glühen.
- Sie kreisen in Bahnen um die Bildschirmmitte.
- Dann fliegen sie an die Stellen von **Titel und Anfang der Geschichte** und verwandeln sich unterwegs in die richtigen Buchstaben.
- Danach blendet die echte Geschichte ein.
- Dauer etwa 4–5 s, spätestens nach 14 s ist Schluss.
- Nach 1,8 s erscheint unten „Tippen zum Überspringen“.

### 8.4 Finale-Animation (`finaleDurch`, Variante B „Die 24 Lichter“)

- Läuft beim allerersten Aufruf der Finale-Seite, egal ob von Türchen 24 oder über „Zum Finale“ in der Übersicht (etwa 15 s).
- Zeitleiste (Variante B, ca.): 0–5,4 s Lichter schweben · 5,4–8 s sie formen den Baum · bis 10,2 s Baum · 10,2–12,5 s Baum wird zum Stern · 12,5–13,4 s Sternschnuppe · ca. 13,2 s Lichtblitz · bis 15,3 s Ausblenden.
- 24 goldene Lichter (für die 24 Türchen) fügen sich zu einem **Tannenbaum**, dann zu einem **Stern**.
- Der Stern wird zur **Sternschnuppe**, am Ende folgt ein **Lichtblitz**, und die Finale-Seite erscheint.
- Sie läuft nur **einmal** von selbst (Speicher-Schlüssel `finaleAn`). Danach kann man sie über „Die Animation noch einmal ansehen“ wieder abspielen.
- **Umschlag** (`umschlagZeigen`), direkt im Anschluss an die Animation (auch wenn sie übersprungen wird):
  - Ein Umschlag in warmem Papierton mit goldenem Rand und goldenem Stern-Siegel liegt mittig auf dunkelgrünem Grund, darunter pulsiert „Tippen zum Öffnen“ (Eigenformulierung).
  - Die Finale-Seite liegt schon darunter bereit.
  - Beim Tippen: `ton/umschlag.mp3`, das Siegel verschwindet, die Lasche klappt auf (0–0,65 s), der Brief gleitet heraus (ab 0,65 s), ab 1,7 s wird er größer und blendet aus, während der dunkle Grund verschwindet und den Brief der Finale-Seite freigibt (fertig nach ca. 2,6 s).
  - Tippen während des Öffnens überspringt den Rest.
  - Der Umschlag kommt **nur zusammen mit der Animation**: beim allerersten Aufruf der Finale-Seite (nach Türchen 24 oder über „Zum Finale“) und bei „Die Animation noch einmal ansehen“. Danach, bei „Bewegung reduzieren“ und bei `PORTAL_AUS` liegt der Brief sofort offen da.
  - Die Zurück-Wischgeste entfernt den Umschlag und geht in die Übersicht.
- **Variante A „Vier Kerzen“** (Adventskranz) ist noch im Code und wird mit `window.FINALE_VAR = "A"` aktiviert.

### 8.5 Töne

Fünf Toneffekte begleiten die Animationen:

| Datei | Wann | Ende |
|---|---|---|
| `ton/knarren.mp3` (2,6 s) | sobald die **Portal-Animation** startet, also bei jedem Öffnen einer Tür (Kachel oder „Weiter durch das nächste Türchen“, auch bei schon geöffneten Türchen) | spielt aus; beim Überspringen oder am Ende der Animation in 0,5 s ausgeblendet |
| `ton/zuklappen.mp3` (1,6 s) | sobald die **Tür sich schließt** (Knopf „Zurück zur Türchen-Auswahl“). Die Datei beginnt mit 0,33 s Stille | spielt aus; beim Überspringen in 0,4 s ausgeblendet |
| `ton/wirbel.mp3` (5,2 s) | sobald der **Buchstaben-Wirbel** startet | am Ende des Wirbels oder beim Überspringen in 0,7 s ausgeblendet |
| `ton/umschlag.mp3` (1,2 s) | beim **Öffnen des Umschlags** nach dem Finale (Tippen). Der Finale-Ton läuft dann meist noch und liegt darunter | spielt aus |
| `ton/finale.mp3` (26,5 s) | sobald die **Finale-Animation** startet (auch bei „Die Animation noch einmal ansehen“) | läuft die Animation bis zum Ende, **klingt der Ton auf der Finale-Seite aus** (die Datei blendet selbst ab ca. 23 s aus). Beim Überspringen 1 s Ausblenden, beim Verlassen der Finale-Seite 0,8 s |

- Umgesetzt im Modul `TON` in index.html (`TON.spielen(name)`, `TON.ausblenden(name, ms)`).
  Die Dateinamen stehen dort in `DATEIEN`. Alle Töne werden nach dem Laden der Seite vorgeladen.
- **Ton nur mit Animation:** Läuft keine Animation („Bewegung reduzieren“, `PORTAL_AUS`, sehr kurze Einstimmung), gibt es auch keinen Ton.
- **Handys spielen Töne nur nach einer Berührung.** Deshalb startet jeder Ton **direkt im Tippen**, nie über einen späteren Timer.
  Darum steckt beim Zuklappen die Verzögerung (0,33 s) in der Datei selbst und nicht im Code.
  Würde man Animationen künftig automatisch (ohne Tippen) starten, bliebe der Ton stumm.
- **Fehlt eine Datei** oder blockiert das Gerät den Ton, laufen die Animationen ganz normal weiter, nur ohne Ton.
- **Lautstärke:** Alle Dateien sind auf **ca. −18 LUFS** angeglichen, mit Limiter (Spitzen höchstens ca. −2 dBFS, dekodiert unter 1,0).
  Die Lautstärke steckt in den Dateien, weil das iPhone eine per Skript gesetzte Lautstärke (`audio.volume`) ignoriert.
  Auf dem iPhone wird beim „Ausblenden“ deshalb nach der Zeit einfach angehalten.
  Neue Töne immer mit `tools/toene-angleichen.py` angleichen (siehe [Abschnitt 16](#16-werkzeuge-im-ordner-tools)).

  Stand der Angleichung (November 2026):

  | Datei | vorher | nachher |
  |---|---|---|
  | knarren.mp3 | −19,6 LUFS, −1,5 dBTP | −18,1 LUFS, −1,9 dBTP |
  | zuklappen.mp3 | −18,4 LUFS, −7,5 dBTP | −18,1 LUFS, −7,3 dBTP (+0,33 s Stille vorn) |
  | wirbel.mp3 | −18,5 LUFS, −5,5 dBTP | −18,0 LUFS, −5,1 dBTP |
  | finale.mp3 | −18,5 LUFS, −5,4 dBTP | −18,0 LUFS, −4,9 dBTP |
  | umschlag.mp3 | −17,9 LUFS, −4,0 dBTP | −18,0 LUFS, −4,1 dBTP |

- **Stummschalter am iPhone:** Je nach iOS-Version spielt Safari die Töne auch bei eingeschaltetem Stummschalter oder eben nicht. Die normale Lautstärke des Handys gilt immer.
- **Offline:** Die Töne werden vom Service Worker gespeichert und spielen auch ohne Netz (siehe [Abschnitt 13](#13-offline-fähigkeit-und-updates-service-worker)).
- Töne austauschen: Datei mit **gleichem Namen** in `ton/` ersetzen, vorher angleichen, und `VERSION` in `sw.js` hochzählen (sonst spielt der alte Ton aus dem Speicher).
- Zum Abschalten aller Töne beim Testen: `window.TON_AUS = true` in der Browser-Konsole.

### 8.6 Kleinere Effekte

- Bilder blenden weich ein, sobald sie sichtbar werden.
- Der Begrüßungssatz in der Übersicht blendet ein.
- Gesperrte Kachel: Wackeln und Schloss-Puls.
- Heutige bzw. ungeöffnete Kacheln: Leuchten und Lichtwelle.
- Wasserzeichen-Bild im Hintergrund von Einstimmung und Geschichte.

---

## 9. Bilder

### 9.1 Stil und Entstehung

- Alle 26 Bilder wurden mit **Google Gemini** erzeugt, mit den Prompts aus `tools/bild-prompts.md`.
- Jeder Prompt besteht aus einer Szenenbeschreibung passend zur Geschichte und einem **immer gleichen Stil-Block**:
  - Bilderbuch-Illustration, Gouache und Aquarell auf Papier.
  - Gedämpftes Tannengrün und Nachtblau mit Kerzengold.
  - Kleine Figuren aus der Distanz, keine Nahaufnahmen von Gesichtern, kein Text.
- Gesichter sind in der kleinen Handy-Darstellung nicht wichtig, deshalb wurde darauf nicht besonders geachtet.

### 9.2 Formate

| Datei | Größe | Verwendung |
|---|---|---|
| `tag-NN.jpg` | 1200×600 (2:1), JPEG-Qualität 82 | geöffnete Kachel, Portal, Bild unter der Geschichte, Wasserzeichen |
| `pix-mid-NN.png` | 32×16 | leicht verpixelte Kachel, Türflügel im Portal |
| `pix-lock-NN.png` | 10×5 | stark verpixelte, gesperrte Kachel |
| `landing.jpg`, `finale.jpg` | 1200×600 | Startseite, Finale |

Die verpixelten Bilder sind winzig und werden vom Browser mit `image-rendering: pixelated` hochskaliert.
Daher entstehen die klaren Klötzchen.

### 9.3 Neue Bilder einbauen

1. Rohbilder (JPG oder PNG) mit den Namen `tag-01` … `tag-24`, `landing`, `finale` in den Ordner `bilder-roh/` legen.
2. `python3 tools/bilder-vorbereiten.py` ausführen. Das Skript:
   - entfernt einen hellen, gemalten Papierrand, falls vorhanden,
   - schneidet mittig auf 2:1 zu,
   - verkleinert auf 1200×600 und speichert nach `bilder/`.
3. `python3 tools/pixel.py` ausführen. Es erzeugt `pix-mid-NN.png` und `pix-lock-NN.png` neu.
4. `VERSION` in `sw.js` hochzählen (wichtig, weil Bilder zuerst aus dem Speicher kommen).

Für beide Skripte braucht man Python 3 mit Pillow (`pip install pillow`).
Wichtige Bildinhalte gehören in die Mitte, weil die Kacheln das Bild weiter beschneiden.

---

## 10. Geschichten

### 10.1 Format der Dateien

Jede Datei `story-dayN.js` setzt ein Objekt `window.STORY`:

```js
/* Türchen 1: Frau Holle (Brüder Grimm). Gemeinfreier Text. ... */
window.STORY = {
  titel: "Frau Holle",
  einstimmung: "Ein bis zwei Sätze für die Einstimmungsseite.",
  text: `Erster Absatz ...

Zweiter Absatz ...
Eine Zeile im selben Absatz (z. B. Verse) ...`,
  quelle: "Brüder Grimm, aus den „Kinder- und Hausmärchen“; sprachlich behutsam modernisiert"
};
```

- **`titel`** muss in doppelten Anführungszeichen stehen (`titel: "…"`).
  Die Funktion `titelNachladen` liest den Titel mit einem regulären Ausdruck direkt aus der Datei.
- **`text`** steht in Backticks (Template-Literal).
  - **Leerzeile = neuer Absatz.**
  - Ein einfacher Zeilenumbruch bleibt als Zeilenumbruch im Absatz erhalten (für Verse).
  - Backticks und `${` dürfen im Text nicht vorkommen.
- **`quelle`** erscheint unter der Geschichte als „Quelle: …“.
- Die Seite lädt die Datei per `<script>` nach und merkt sich geladene Geschichten (`storyCache`).
  Spätere, inzwischen überholte Ladevorgänge werden über einen Zähler (`ladeNr`) verworfen.
- Ein Text darf nicht leer sein, sonst erscheint die Fehlermeldung.

### 10.2 Die 24 Geschichten

Alle Texte sind **gemeinfrei** (die Autoren sind seit über 70 Jahren tot).
Sie stammen aus EPUB- und Textausgaben, u. a. von Projekt Gutenberg.
Die Sprache wurde **behutsam modernisiert**: Rechtschreibung (daß → dass, ward → wurde, …) und einzelne veraltete Wörter.
Plattdeutsche Stellen wurden ins Hochdeutsche übertragen.
Die **Einstimmungssätze sind Eigenformulierungen**.

| Tag | Titel | Autor | Quelle |
|---|---|---|---|
| 1 | Frau Holle | Brüder Grimm | Kinder- und Hausmärchen |
| 2 | Der Schneemann | Hans Christian Andersen | Andersens Märchen (Übers. Pauline Klaiber) |
| 3 | Lüttjemann und Püttjerinchen | Hermann Löns | Deutsches Weihnachtsbuch (1918) |
| 4 | Der Schneemann | Manfred Kyber | Märchen |
| 5 | Wie der alte Christian Weihnachten feierte | Paula Dehmel | Deutsches Weihnachtsbuch (1918) |
| 6 | Der kleine Tannenbaum | Manfred Kyber | Märchen |
| 7 | Die Wichtelmänner | Brüder Grimm | Kinder- und Hausmärchen (nur das erste der drei Märchen) |
| 8 | Im Dorf | Max Jungnickel | Deutsches Weihnachtsbuch (1918) |
| 9 | Puck Kraihenfoot | Hermann Löns | Deutsches Weihnachtsbuch (1918), Platt → Hochdeutsch |
| 10 | Der Christabend | Ludwig Thoma | Nachbarsleute |
| 11 | Die sieben Tannenbäume | Gorch Fock | Nach dem Sturm |
| 12 | Hanspeters Weihnachtslied | Charlotte Niese | Deutsches Weihnachtsbuch (1918) |
| 13 | Unter dem Tannenbaum | Theodor Storm | Gesammelte Werke |
| 14 | Marthe und ihre Uhr | Theodor Storm | Gesammelte Werke |
| 15 | Der Tannenbaum | Hans Christian Andersen | Andersens Märchen (Übers. Pauline Klaiber) |
| 16 | Eine Weihnachtsfahrt | Gorch Fock | Nach dem Sturm, Platt → Hochdeutsch |
| 17 | Die Sterntaler | Brüder Grimm | Kinder- und Hausmärchen |
| 18 | Der Weihnachtsabend | Louise Anklam | Kindergeschichten |
| 19 | Der Dickkopf und das Peterlein | Adolf Schmitthenner | Deutsches Weihnachtsbuch (1918); die Aufschrift der Torte steht im Original als Bild |
| 20 | Der Stern zu Bethlehem | Hermine Villinger | Deutsches Weihnachtsbuch (1918) |
| 21 | Unter gutem Stern | W. Fischer | Deutsches Weihnachtsbuch (1918) |
| 22 | Zwölf mit der Post | Hans Christian Andersen | Andersens Märchen (Übers. Pauline Klaiber) |
| 23 | Die Geschichte vom Weihnachtsmarkt | Luise Büchner | Weihnachtsmärchen für Kinder (1868) |
| 24 | Als ich Christtagsfreude holen ging | Peter Rosegger | Waldjugend |

Die Reihenfolge wurde so gewählt, dass sich Märchen, Erzählungen und Autoren abwechseln.
Mit Rosegger steht eine Geschichte am Heiligabend am Ende.

### 10.3 Eine Geschichte austauschen

1. Neue Datei im obigen Format anlegen (Dateiname `story-dayN.js` beibehalten).
2. Optional ein neues Bild `tag-NN.jpg` erzeugen und `tools/pixel.py` laufen lassen.
3. `VERSION` in `sw.js` hochzählen.
4. Wer das Türchen schon geöffnet hat, sieht auf der Kachel noch den **alten gespeicherten Titel**, bis er die Geschichte erneut öffnet.

---

## 11. Kalender-Erinnerungen (.ics)

- Im Ordner `erinnerung/` liegen 9 Dateien: `1700.ics`, `1730.ics`, … `2100.ics`.
- Jede enthält **24 Termine** „Türchen 1“ bis „Türchen 24“, jeweils am 1. bis 24. Dezember zur gewählten Uhrzeit:
  - **15 Minuten** lang,
  - **Erinnerung genau zum Beginn** (`TRIGGER:PT0M`),
  - Link zur Seite (`SEITEN_URL`) in Beschreibung und URL-Feld,
  - Zeitzone Europe/Berlin,
  - Zeilen nach RFC 5545 auf 75 Zeichen gefaltet.
- Auf der Startseite lädt „Termine hinzufügen“ die passende Datei. Das Handy fragt dann, ob die Termine übernommen werden sollen.
- **Neu erzeugen** (nach Änderung von `JAHR` oder `SEITEN_URL`):
  ```bash
  python3 tools/erinnerung.py
  ```
- Der Service Worker speichert diese Dateien **nie** zwischen. Es wird immer die aktuelle Fassung geladen.

---

## 12. Was im Browser gespeichert wird

Alles liegt im `localStorage` des Geräts, mit dem Präfix `weihnacht2026_` (TEST: `weihnacht2026_test_`).
Jedes Gerät und jeder Browser hat seinen eigenen Stand. Nur wenn ein Vorname eingegeben wurde und `SYNC_URL` gesetzt ist, wird ein Teil davon zusätzlich online gesichert (siehe [Abschnitt 23](#23-name-und-online-sicherung)).

| Schlüssel | Inhalt |
|---|---|
| `geoeffnet` | Liste der geöffneten Türchen, z. B. `[1,2,3,5]` |
| `titel` | Titel der geöffneten Geschichten, z. B. `{"1":"Frau Holle"}` |
| `lese` | Leseposition je Türchen: Anteil (0–1) und Zeitpunkt |
| `gruss` | Begrüßungs-„Beutel“ und Verlauf je Tageszeit |
| `finaleAn` | `true`, wenn die Finale-Animation schon gelaufen ist |
| `besucht` | `true` nach dem ersten Besuch (für das Einklappen von „Bevor es losgeht“) |
| `lieblinge` | gemerkte Lieblingsgeschichten, z. B. `[3,7]` (seit v18) |
| `schrift` | gewählte Schriftgröße der Geschichten, Stufe 0–4, Standard 1 (seit v18) |
| `lieblingeTs` | Zeitpunkt der letzten Änderung an den Lieblingen (für den Abgleich, seit v19) |
| `name` | selbst eingegebener Vorname (nur auf dem Gerät, wird **nicht** online gespeichert; seit v19) |
| `nameOhne` | `true`, wenn „Ohne Namen weiter“ gewählt wurde (seit v19) |

- Funktioniert `localStorage` nicht (z. B. in manchen privaten Modi), arbeitet die Seite mit einem Ersatz im Arbeitsspeicher.
  Dann geht der Stand beim Schließen verloren, aber nichts stürzt ab.
- **Wichtig für iPhone:** Eine auf dem Startbildschirm installierte Web-App hat **einen anderen Speicher** als Safari.
  Wer erst in Safari liest und dann die App nutzt, beginnt dort von vorn – außer er gibt dort denselben Vornamen ein (Online-Sicherung, Abschnitt 23).
- Töne, Zuklappen, Finale-Ton (v14) und Umschlag (v15) haben **keine neuen Schlüssel** gebracht, v18 nur die zwei neuen `lieblinge` und `schrift`; der Fortschritt der Leser bleibt unverändert.
  Die Töne selbst liegen nicht im `localStorage`, sondern im Offline-Speicher des Service Workers (Abschnitt 13).

---

## 13. Offline-Fähigkeit und Updates (Service Worker)

`sw.js` wird über `https` registriert und zusätzlich auf `http://localhost` (zum Testen am Rechner).

- **Beim ersten Besuch** speichert er im Hintergrund:
  - Seite, `config.js`, Manifeste, Symbole und alle 24 Geschichten,
  - danach alle Bilder (Tagesbilder plus beide Pixelstufen, Start- und Finale-Bild),
  - danach die fünf Töne aus `ton/` (Liste `TOENE` in `sw.js`).
- **Seiten und Geschichten:** zuerst aus dem Netz (damit Änderungen sofort ankommen); ohne Netz aus dem Speicher.
- **Bilder:** zuerst aus dem Speicher (schnell), sonst aus dem Netz.
- Gespeichert werden nur erfolgreiche Antworten (`res.ok`). Fehlerseiten landen also nicht im Speicher.
- `.ics`-Dateien werden nie gespeichert.
- **Töne (`ton/`):** zuerst aus dem Speicher, damit sie auch **offline** spielen.
  - Safari fragt Audio in Teilstücken an (**Range-Anfragen**, z. B. `Range: bytes=0-1`). Eine gespeicherte, vollständige Datei passt darauf nicht von selbst.
  - Der Service Worker schneidet deshalb den angefragten Bereich aus der gespeicherten Datei und antwortet mit **206 Partial Content** (`Content-Range`, `Content-Length`, `Accept-Ranges`).
    Auch `bytes=500-` und `bytes=-500` (die letzten 500 Bytes) werden verstanden; ein Bereich außerhalb der Datei bekommt **416**.
  - Ist ein Ton noch nicht gespeichert, kommt er aus dem Netz; eine vollständige, erfolgreiche Antwort (200) wird dann abgelegt.
  - Bis v13 liefen die Töne bewusst am Service Worker vorbei (offline still). Seit v14 ist das so gelöst.

### Updates

> **Bei jeder Änderung `VERSION` in `sw.js` hochzählen** (`advent-v18` → `advent-v19` …).

- Eine neue Version löscht beim Aktivieren den alten Speicher und lädt alles neu.
- Ohne neue Version kommen **geänderte Bilder und Töne** auf Handys, die die Seite schon kennen, nicht an. Beide werden zuerst aus dem Speicher geholt.
- Texte und Code kommen meist trotzdem an, weil sie zuerst aus dem Netz geladen werden. Sicher ist es aber nur mit neuer Version.
- **GitHub Pages** hält Dateien selbst etwa 10 Minuten im Zwischenspeicher. Nach dem Hochladen also ein paar Minuten warten.
- Hängt ein Handy trotzdem fest:
  - Seite neu laden,
  - App ganz schließen und neu öffnen,
  - im Notfall die Website-Daten im Browser löschen.

---

## 14. Als App auf dem Startbildschirm

- `manifest.json` (LIVE): Name „Advent“, `start_url` `./index.html`, Vollbild (`standalone`), dunkelgrüne Farben.
- `manifest-test.json` (TEST): Name „Advent (Test)“, Kurzname „Advent Test“, `start_url` `./index.html?test=1`, eigene Symbole `icon-test-192.png` und `icon-test-512.png` mit rotem Band „TEST“.
- **Welches Manifest gilt, entscheidet ein kleines Skript im `<head>` von index.html.**
  - Bei `?test=1` wird `manifest-test.json` eingebunden, der iPhone-App-Titel auf „Advent Test“ gesetzt und das iPhone-Symbol auf `apple-touch-icon-test.png` umgestellt.
  - Sonst gilt `manifest.json`.
- **Warum so kompliziert?** Mit nur einem Manifest startete ein TEST-Symbol auf dem Startbildschirm die **LIVE**-Fassung, weil dort die `start_url` fest eingetragen war.
- Die beiden Manifeste haben verschiedene `id`-Werte. So können beide Fassungen gleichzeitig installiert sein.
- **Tipp:** Wenn ein TEST-Symbol von früher noch LIVE öffnet oder noch kein „TEST“-Band hat, Symbol löschen und neu anlegen, während die TEST-Fassung geöffnet ist. Das Symbol wird nur beim Anlegen übernommen.
- Die TEST-Symbole erzeugt `tools/test-symbole.py` aus den normalen Symbolen. Nach einer Änderung der normalen Symbole erneut ausführen.
- Auf iPhone gelten zusätzlich `apple-touch-icon.png` und die `apple-mobile-web-app-…`-Angaben.

---

## 15. Hosting: GitHub Pages und eigene Domain

### 15.1 GitHub Pages

- Repository `vanallen84/advents-geschichten`, Veröffentlichung aus dem Hauptzweig, Stammordner `/`.
- Unter **Settings → Pages → Custom domain** ist `adventsgeschichten.tkagel.de` eingetragen.
  - GitHub legt dafür die Datei `CNAME` im Repository an. **Diese Datei nicht löschen.**
  - Sie ist nicht in den lokalen Projektdateien enthalten, sondern entsteht direkt auf GitHub.
- „Enforce HTTPS“ ist aktiviert. Das Zertifikat stellt GitHub automatisch aus.
- Die alte Adresse `vanallen84.github.io/advents-geschichten/` leitet automatisch auf die eigene Domain weiter.
- **Hochladen:**
  - Am einfachsten über die GitHub-Weboberfläche mit „Add file → Upload files“.
  - Gleichnamige Dateien werden ersetzt.
  - **Achtung:** Dateien aus einem alten ZIP nicht versehentlich über neuere hochladen.

### 15.2 DNS bei goneo

goneo legt die Subdomain `adventsgeschichten.tkagel.de` als **eigene Zone** an, mit eigenen MX- und TXT-Einträgen.
Neben diesen darf kein CNAME stehen. Deshalb zeigen **A- und AAAA-Einträge** direkt auf GitHub:

| Typ | Name | Wert |
|---|---|---|
| A | `adventsgeschichten` (bzw. @ der Subdomain-Zone) | 185.199.108.153 |
| A | 〃 | 185.199.109.153 |
| A | 〃 | 185.199.110.153 |
| A | 〃 | 185.199.111.153 |
| AAAA | 〃 | 2606:50c0:8000::153 |
| AAAA | 〃 | 2606:50c0:8001::153 |
| AAAA | 〃 | 2606:50c0:8002::153 |
| AAAA | 〃 | 2606:50c0:8003::153 |

- Alte A- und AAAA-Einträge von goneo für diese Subdomain (Webspace) müssen entfernt sein.
- MX- und TXT-Einträge der Subdomain können bleiben. Für den Kalender werden sie nicht gebraucht.
- Die aktuellen GitHub-Adressen stehen in der GitHub-Dokumentation unter „Managing a custom domain for your GitHub Pages site“.

### 15.3 Suchmaschinen

Die Seite trägt `noindex, nofollow`. Sie soll nicht in Suchmaschinen auftauchen und ist nur über den Link erreichbar.

---

## 16. Werkzeuge im Ordner tools/

| Skript | Zweck | Aufruf |
|---|---|---|
| `bilder-vorbereiten.py` | Rohbilder aus `bilder-roh/`: Papierrand weg, auf 2:1 zuschneiden, 1200×600, Qualität 82 → `bilder/` | `python3 tools/bilder-vorbereiten.py [quellordner]` |
| `pixel.py` | `pix-mid-NN.png` (32×16) und `pix-lock-NN.png` (10×5) aus `tag-NN.jpg` | `python3 tools/pixel.py [bilderordner]` |
| `test-symbole.py` | `icon-test-192.png`, `icon-test-512.png`, `apple-touch-icon-test.png`: normale Symbole mit rotem Band „TEST“ | `python3 tools/test-symbole.py` |
| `toene-angleichen.py` | alle `*.mp3` aus `ton-roh/` auf −18 LUFS angleichen (Limiter, 44,1 kHz, 160 kbit/s) → `ton/`; `zuklappen.mp3` bekommt 0,33 s Stille vorn; gibt Vorher/Nachher-Werte aus | `python3 tools/toene-angleichen.py [quellordner]` |
| `erinnerung.py` | `erinnerung/1700.ics` … `2100.ics`, liest `JAHR` und `SEITEN_URL` aus `config.js` | `python3 tools/erinnerung.py` |
| `bild-prompts.md` | 26 Gemini-Prompts mit gemeinsamem Stil-Block | – |
| `platzhalter.py` | **Veraltet.** Erzeugte Platzhalterbilder vor den echten Bildern. **Nicht mehr ausführen**, es überschreibt die echten Bilder! | – |

Alle Skripte im Hauptordner des Projekts starten. Benötigt wird Python 3, für die Bild-Skripte zusätzlich Pillow, für die Töne `ffmpeg`.
Die Rohordner `bilder-roh/` und `ton-roh/` gehören nicht ins Repository.

---

## 17. Testen

### 17.1 Im November auf dem Handy

1. `https://adventsgeschichten.tkagel.de/test/` öffnen. Am 3. November ist dort z. B. Türchen 3 frei.
2. Zum Neuanfang `…/test/?reset=1` aufrufen.
3. Für einen bestimmten Tag das Datum am Handy umstellen (danach wieder zurückstellen!).

### 17.2 Lokal am Rechner

```bash
cd advent
python3 -m http.server 8765
# im Browser: http://localhost:8765/index.html?test=1
```

Der Service Worker ist auch lokal auf `localhost` aktiv. Wer beim Entwickeln Änderungen nicht sieht: in den Entwicklerwerkzeugen des Browsers unter „Application → Service Workers“ „Update on reload“ einschalten oder die Website-Daten löschen.

### 17.3 Automatisch mit Playwright (so wurde entwickelt)

- Handy-Ansicht: 390×844, `is_mobile`, `has_touch`, Zeitzone Europe/Berlin, Sprache de-DE.
- Uhrzeit fälschen mit `page.clock.install(time=...)`, z. B. 10. Dezember 10:00 Uhr.
- Gespeicherten Stand vorgeben über `localStorage.setItem('weihnacht2026_geoeffnet', '[1,2,3]')`.
- Geprüft wurden u. a.:
  - Kachelzustände an verschiedenen Tagen (30. Nov., 1., 10., 24., 25., 27. Dez.),
  - Portal-Ablauf per Screenshots zu bestimmten Zeitpunkten,
  - Weiter-Knopf, Finale, Fehler beim Laden, Zurück-Geste,
  - Zuklappen: Kachel genau in der Bildschirmmitte, sauberes Ende, Antippen überspringt, Wischgeste ohne Animation,
  - Ton-Aufrufe (wann welcher Ton startet und ausgeblendet wird), „Bewegung reduzieren“ ohne Animation und Ton,
  - Offline-Start mit echtem Service Worker: Seite, Geschichten, Bilder und alle Töne; Range-Anfragen (206, 416),
  - Einklappen der Karten, TEST-Manifest,
  - keine Fehler in der Browser-Konsole.

### 17.4 Was nur auf echten Geräten zuverlässig prüfbar ist

- Vorlesen: Klang der Stimme, Mitscrollen, Anhalten/Weiter (im Test nur mit einer nachgebildeten Sprachausgabe geprüft).
- Flüssigkeit der Animationen (Portal-3D-Drehung, Wirbel, Finale), besonders auf älteren iPhones.
- Startbildschirm-App, besonders iPhone und das getrennte TEST-Symbol.
- Übernahme der .ics-Termine in den Handy-Kalender.
- Wake Lock (Bildschirm bleibt an).
- Töne: ob sie spielen, wie laut sie sind und wie sie zum Stummschalter stehen.

---

## 18. Besonderheiten, Stolperfallen und Lösungen

- **Geänderte Bilder kommen nicht an:** `VERSION` in `sw.js` nicht hochgezählt (siehe [Abschnitt 13](#13-offline-fähigkeit-und-updates-service-worker)).
- **Eine Änderung wirkt nicht, obwohl hochgeladen:**
  - GitHub-Cache (ca. 10 Min.) abwarten.
  - Prüfen, ob wirklich die neue Datei auf GitHub liegt. Einmal hatte ein ZIP-Upload eine ältere index.html wieder eingespielt.
- **Nur 20 Dateien im Chat sichtbar:** Beim Übergeben vieler Dateien zeigt die Ansicht höchstens 20 an. Bei mehr Dateien besser als ZIP oder in Teilen.
- **TEST-Symbol öffnet LIVE:** gelöst durch `manifest-test.json` und das Manifest-Skript im `<head>` (siehe [Abschnitt 14](#14-als-app-auf-dem-startbildschirm)).
- **„Bevor es losgeht“ klappt nicht ein:** Das passiert erst ab dem **zweiten** Besuch. Gezählt wird pro Gerät, pro Browser und pro Fassung.
- **„So funktioniert’s“** klappt erst ein, wenn mindestens ein Türchen **gelesen** (nicht nur angetippt) wurde.
- **iPhone-App und Safari** haben getrennte Speicher (siehe [Abschnitt 12](#12-was-im-browser-gespeichert-wird)).
- **Falsches Handy-Datum** schaltet Türchen zu früh oder zu spät frei. Das ist gewollt einfach gehalten, es gibt keine Serverzeit.
- **Speicher-Präfix hängt am Jahr:** Wird `JAHR` geändert, sind alle bisherigen Stände für die Seite „vergessen“. Die alten Daten bleiben unbenutzt im Browser liegen.
- **Plattdeutsch und „ward“:** Eine automatische Ersetzung „ward → wurde“ hätte in plattdeutschen Sätzen Fehler erzeugt. Die betroffenen Geschichten (9, 16) wurden deshalb vollständig ins Hochdeutsche übertragen.
- **Titel auf Kacheln:** Werden aus dem Speicher genommen. Nach dem Austausch einer Geschichte bleibt bei bisherigen Lesern bis zum erneuten Öffnen der alte Titel stehen.
- **Ton spielt nicht:** Datei wirklich unter `ton/knarren.mp3`, `ton/zuklappen.mp3`, `ton/wirbel.mp3`, `ton/finale.mp3` bzw. `ton/umschlag.mp3` (Kleinschreibung beachten, GitHub unterscheidet Groß/Klein)? Handy-Lautstärke an? Am iPhone ggf. Stummschalter prüfen. Nach dem Austausch eines Tons `VERSION` hochgezählt?
- **Ton wird nur verzögert gestartet:** nie einen Ton per `setTimeout` starten, das iPhone blockiert ihn dann womöglich. Verzögerungen gehören als Stille in die Datei.
- **`titel:` in den Geschichten-Dateien** muss als `"…"`-String stehen, sonst kann `titelNachladen` ihn nicht lesen. Die Geschichte selbst funktioniert aber trotzdem.

---

## 19. Interne Schalter für Entwickler

| Schalter | Ort | Wirkung |
|---|---|---|
| `const testModus = false;` | index.html | `true`: **alle** Türchen offen und eine Entwickler-Leiste oben mit Tagesauswahl. **Niemals so hochladen.** |
| `window.FINALE_VAR = "B";` | index.html | `"A"` = Finale „Vier Kerzen“, `"B"` = „Die 24 Lichter“ |
| `window.PORTAL_AUS = true` | Browser-Konsole | schaltet Portal, Zuklappen, Wirbel und Finale-Animation (und damit ihre Töne) ab |
| `window.TON_AUS = true` | Browser-Konsole | schaltet alle Töne ab |
| `window.PORTAL_FARBE = true` | Browser-Konsole | Portal nur golden, ohne Bild |
| `VORTEST_NOVEMBER` | config.js | November = Dezember auch auf LIVE (nicht mehr nötig, TEST-Fassung nutzen) |
| `?test=1` | Adresse | TEST-Fassung |
| `?reset=1` | Adresse | gespeicherten Stand der Fassung löschen (inkl. Name und Online-Stand dieses Namens) |
| `SYNC_URL: ""` | config.js | Online-Sicherung abschalten |

---

## 20. Wichtige Funktionen in index.html

`index.html` ist bewusst eine einzige Datei: zuerst CSS im `<style>`, dann das HTML der Seiten, dann ein großer `<script>`-Block.

| Bereich | Funktionen |
|---|---|
| Einstellungen | `CFG`, `JAHR`, `TEST_FASSUNG`, `VORTEST_NOVEMBER`, `testModus` |
| Speicher | `speicherLesen`, `speicherSchreiben`, `speicherLoeschen` (Präfix `PFX`) |
| Datum | `jetzt`, `tagOffen`, `ab25`, `heuteTag`, `istTagErreicht`, `alleFreigegeben`, `determineActiveDay` |
| Seitenwechsel | `alleScreensAus`, `resetToLanding`, `zeigeTuerenUebersicht`, `zeigeEinstimmung`, `zeigeStory`, `zeigeFinale`, `oeffneTag`, `waehleTag`, `nextDaySetup`, `zeigeGesperrt`, `schliesseModal` |
| Kacheln | `tuerStilAktualisieren`, `pixelSetzen`, `geoeffnetListe`, `merkeGeoeffnet`, `titelMap`, `merkeTitel`, `titelNachladen`, `bildUrl` |
| Geschichten | `ladeGeschichte`, `absaetzeHtml`, `loadStoryContent`, `geschichteFehler`, `geschichteNochmal` |
| Bilder | `bildEinblenden`, `zeigeStoryBild`, `storyBildStart`, `wmAn`, `wmAus` |
| Animationen | `portalDurch`, `portalZurueck`, `wirbelUebergang`, `startStory`, `finaleDurch` (mit `bildA`/`bildB`), `umschlagZeigen` |
| Töne | `TON.spielen`, `TON.ausblenden` (Dateinamen in `DATEIEN`) |
| Name/Sicherung | `leserName`, `personalisieren`, `nameAnzeigen`, `nameSpeichern`, `nameUeberspringen`, `SYNC` (`abgleichen`, `spaeter`, `loeschen`) |
| Lesen | `schriftAendern`, `schriftAnwenden`, `VORLESEN` (`umschalten`, `stop`), `lieblingUmschalten`, `lieblingKnopf`, `lieblingeListe`, `istLiebling`, `lieblingeZeigen` |
| Startseite | `rulesAktualisieren`, `vorabUmschalten`, `rulesUmschalten`, `ladeErinnerung`, Countdown, App-Tipp nach Gerät |
| Übersicht | `begruessungWaehlen`, `begruessungZeigen`, `finaleKnopfAktualisieren` |
| Sonstiges | `seiteAktualisieren` (Tab-Titel/Symbol), Lesebalken und `lesePositionHerstellen`, Wake Lock, Zurück-Geste, Datumswechsel-Prüfung, Service-Worker-Registrierung |

Farben stehen als CSS-Variablen ganz oben im `<style>` (`--bg-color`, `--accent-color` Gold `#d9b45a`, `--heading-color` usw.).
Die Farbwelt: Winterabend, Tannengrün, Kerzengold, warmes Cremeweiß.

---

## 21. Verlauf der Änderungen

Grob in der Reihenfolge der Entstehung (Herbst 2026):

1. **Grundlage:**
   - Alter Kalender übernommen und Einstellungen in `config.js` ausgelagert.
   - Kein fester Empfängername, Absender über `config.js`.
   - Eigener, jahresabhängiger Speicher-Präfix.
2. **Ablauf:**
   - Einstimmungsseite beim ersten Öffnen.
   - Buchstaben-Wirbel als Übergang.
   - Portal-Animation.
   - Gesperrte Türchen wackeln.
   - Zurück-Geste.
   - Lesefortschritt, Leseposition, Wake Lock.
3. **Startseite:**
   - Countdown.
   - Karte „Bevor es losgeht“ mit App-Anleitung je nach Gerät und Kalender-Erinnerung.
   - „So funktioniert’s“.
4. **Übersicht:** Begrüßung nach Tageszeit, Kachelzustände, Finale-Knopf.
5. **Finale:** Variante B „Die 24 Lichter“, wobei der Stern zur Sternschnuppe wird (statt eines Herzens).
6. **TEST-Fassung** unter `/test/` mit November = Dezember und eigenem Speicher. LIVE seitdem fest auf dem echten Datum.
7. **Offline-Fähigkeit** über den Service Worker. Bilder werden zuerst aus dem Speicher geholt, nur erfolgreiche Antworten werden gespeichert.
8. **Kalender-Termine** (.ics) für 9 Uhrzeiten, 15 Minuten lang, Erinnerung zum Beginn.
9. **24 Geschichten:** gemeinfreie Texte, modernisiert, mit Quellenangabe und eigenen Einstimmungssätzen.
10. **26 Bilder** (Gemini) mit Vorbereitungs- und Pixel-Skripten.
11. **Eigene Domain** `adventsgeschichten.tkagel.de` über goneo, mit A- und AAAA-Einträgen.
12. **„Bevor es losgeht“** ab dem zweiten Besuch eingeklappt.
13. **Absenderzeile** fest „Von mir, nur für dich!“.
14. **Eigenes TEST-Manifest**, damit das TEST-Symbol auf dem Startbildschirm auch TEST öffnet.
15. **Portal neu getaktet** (v11):
    - Tür mit leicht verpixeltem Bild geht auf, dann ca. 2 s Entpixeln, dann Zoom.
    - Bei schon geöffneten Türchen sofort Zoom.
    - Ungeöffnete Kacheln heller, geöffnete Kacheln scharf und mit Titel der Geschichte.
16. **Eigenes App-Symbol für TEST** (v12): goldener Stern mit rotem Band „TEST“.
17. **Töne** (v13): `ton/knarren.mp3` beim Öffnen einer Tür, `ton/wirbel.mp3` beim Buchstaben-Wirbel.
18. **Zuklappen, Finale-Ton, Töne offline** (v14):
    - Die Tür schließt sich beim Knopf „Zurück zur Türchen-Auswahl“ wieder auf ihrer Kachel (`portalZurueck`), mit `ton/zuklappen.mp3`.
    - `ton/finale.mp3` zur Finale-Animation.
    - Alle Töne auf −18 LUFS angeglichen (`tools/toene-angleichen.py`).
    - Service Worker speichert die Töne und beantwortet Range-Anfragen (206), damit sie auch offline spielen.
    - Übernommen und angepasst aus einer Schwesterversion des Kalenders; Push-Erinnerungen bewusst nicht.
19. **Umschlag und Brief** (v15): Nach der Finale-Animation liegt ein Umschlag mit Stern-Siegel bereit; Tippen öffnet ihn (`ton/umschlag.mp3`), der Brief wird zur Finale-Seite. Die Finale-Seite sieht aus wie ein Brief auf altem Briefpapier.
20. **Neuer Brieftext** (v16): fünf Absätze, Unterschrift nur noch mit dem Namen.
21. **Zwei Briefbögen** (v17): Der Brief steht auf zwei leicht versetzten Bögen untereinander statt auf einem langen Blatt; im Umschlag gleitet ein kleiner Stapel heraus.
23. **Name und Online-Sicherung** (v19): freiwillige Namenseingabe auf der Startseite, persönliche Überschrift, Begrüßung und Brief-Gruß; Abgleich von Türchen, Titeln, Lieblingen und „Finale gesehen“ über einen eigenen Cloudflare-Worker „advent-stand“.
22. **Lesen und Finale** (v18): Schriftgröße A−/A+, Vorlesen mit „Weiter vorlesen“, Lieblingsgeschichten (Stern auf Kachel, Zettel im Finale), Brief in Serifenschrift, Finale-Animation und Umschlag beim allerersten Aufruf auch über „Zum Finale“.

---

## 22. Rechtliches zu Texten und Bildern

- **Texte:** Alle 24 Geschichten sind gemeinfrei. Die Bearbeitung (Modernisierung) ist bei jeder Geschichte in der Quellenzeile vermerkt.
- **Eigenformulierungen:** Einstimmungssätze, Begrüßungssätze, Texte der Startseite, „Tippen zum Öffnen“, die Beschriftungen „Zu den Lieblingen“, „Lieblingsgeschichte“, „Deine Lieblingsgeschichten“, „Vorlesen“, „Weiter vorlesen“, „Vorlesen anhalten“. Der Brief auf der Finale-Seite stammt vom Absender selbst.
- **Bilder:** Mit Google Gemini erzeugt, für die private Nutzung in diesem Kalender. Keine Fotos realer Personen.
- Die Seite ist privat und nicht in Suchmaschinen gelistet.
- **Daten:** Ohne Namenseingabe bleibt alles im Browser des Lesers. Mit Namen werden geöffnete Türchen, Titel, Lieblinge und „Finale gesehen“ unter einem aus dem Namen berechneten Schlüssel bei Cloudflare gespeichert (KV-Speicher des eigenen Workers). Der Name selbst wird nicht übertragen.

---

## 23. Name und Online-Sicherung

Gedacht für eine Person (oder wenige), die den Kalender auf mehreren Geräten, in Safari **und** in der App nutzt
oder die App einmal neu installiert. Wer denselben Vornamen eingibt, findet seinen Stand wieder.

### 23.1 Name (freiwillig)

- Beim ersten Besuch fragt die **Namenskarte** oben auf der Startseite nach dem Vornamen. „Ohne Namen weiter“ ist jederzeit möglich; später unten auf der Startseite „Namen eingeben“ bzw. „Nicht Anna? Namen ändern“.
- Schreibweise: nur GROSS oder nur klein getippte Namen werden schön geschrieben („anna-lena“ → „Anna-Lena“), sonst bleibt die Eingabe (z. B. „McKenzie“).
- Der Name steht nur im Speicher des Geräts (`name`), **nicht** online und **nicht** im Code.
- **Personalisierung:**
  1. Überschrift der Startseite „Annas Adventskalender“ (Namen auf s/ß/x/z: „Klaus’ Adventskalender“).
  2. Begrüßung in der Übersicht, wo der Satz `{name}` enthält („Guten Morgen, Anna. …“).
  3. Überschrift des Briefs: „Frohe Weihnachten, Anna!“ (bewusst ohne „Liebe/Lieber“, dafür müsste das Geschlecht bekannt sein).

### 23.2 Wie die Sicherung funktioniert

- **Schlüssel:** SHA-256 aus `adventsgeschichten|JAHR|SYNC_ZUSATZ|vorname` (Vorname klein, Leerzeichen bereinigt), davon 40 Hex-Zeichen; die TEST-Fassung hängt `-t` an.
  Groß-/Kleinschreibung und Leerzeichen spielen also keine Rolle, ein Tippfehler ergibt aber einen anderen Speicher.
  Durch das Jahr beginnt jeder neue Jahrgang leer; durch `-t` sind TEST und LIVE getrennt.
- **Gesichert werden:** geöffnete Türchen, Titel, Lieblingsgeschichten (mit Zeitstempel), „Finale gesehen“, „schon besucht“.
  **Nicht:** Name, Schriftgröße, Lesepositionen, Begrüßungen (gerätebezogen).
- **Wann:**
  - beim Start der Seite und nach der Namenseingabe (holen → zusammenführen → ggf. ablegen),
  - etwa 3 s nach jeder Änderung (neues Türchen, Liebling, Finale),
  - wenn die App in den Hintergrund geht und noch etwas offen ist (sofort, `keepalive`),
  - wenn die App nach mehr als 20 s wieder in den Vordergrund kommt (Stand der anderen Geräte holen).
- **Zusammenführen:** Türchen und Titel werden vereinigt; bei den Lieblingen gewinnt die **zuletzt geänderte** Liste (damit ein entfernter Favorit nicht von einem anderen Gerät zurückkommt); „Finale gesehen“/„besucht“: einmal gesehen = überall gesehen.
- **Ohne Netz** läuft alles wie bisher; der Abgleich wird beim nächsten Mal nachgeholt. Ist der Worker nicht erreichbar, merkt die Leserin nichts davon.
- „Willkommen zurück“ erscheint nur, wenn online schon ein Stand mit geöffneten Türchen oder Lieblingen lag.

### 23.3 Der Worker „advent-stand“

- Eigener Cloudflare-Worker, **getrennt** vom Worker des anderen Kalenders, mit eigenem KV-Speicher (Binding `STAND`).
- Wege: `GET /stand/<schlüssel>` (holen; ohne Stand `{"t":0,"daten":null}`), `PUT /stand/<schlüssel>` (ablegen), `DELETE /stand/<schlüssel>` (löschen, für `?reset=1`).
- Schutz: nur Anfragen mit der Herkunft `https://adventsgeschichten.tkagel.de` (oder `ALLOWED_ORIGINS`), Schlüssel genau 40 Hex-Zeichen (+ `-t`), höchstens 16 KB, frühestens alle 1,5 s ein Schreibvorgang pro Schlüssel.
- Keine Passwörter oder Geheimnisse. Wer den Vornamen kennt und `config.js` liest, könnte den Stand theoretisch abrufen; gespeichert sind aber nur Türchen-Nummern, Titel und Lieblinge.
- Code (`worker-advent-stand.js`) und Einrichtungsanleitung (`ANLEITUNG_Cloudflare_advent-stand.md`) liegen **nicht** im Repository.
  Der gültige Code steht im Cloudflare-Dashboard unter dem Worker („Edit code“).
- Kosten: kostenloser Tarif reicht (100.000 Lese- und 1.000 Schreibvorgänge pro Tag).

### 23.4 Testen

- TEST-Fassung: `…/test/?reset=1`, Namen eingeben, Türchen lesen, Liebling setzen, ca. 5 s warten.
  Dann in einem privaten Fenster, auf einem anderen Gerät oder in der TEST-App denselben Namen eingeben → „Willkommen zurück“.
- In Cloudflare unter KV → `advent-stand-kv` sind die Einträge `stand:…` (LIVE) bzw. `stand:…-t` (TEST) zu sehen.
- Entwickelt und geprüft wurde mit dem echten Worker-Code, lokal in Node mit nachgebildetem KV-Speicher, und mehreren getrennten Browser-Kontexten als „Geräten“.
