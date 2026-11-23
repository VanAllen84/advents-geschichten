# Adventsgeschichten – ein privater Adventskalender mit 24 Geschichten

Ein statischer Adventskalender aus HTML, CSS und JavaScript, ohne Server-Logik, ohne Datenbank und ohne Anmeldung.
Vom 1. bis 24. Dezember öffnet sich jeden Tag ein Türchen, hinter jedem steht eine weihnachtliche Geschichte mit Bild.
Nach Türchen 24 folgt ein Finale.

Der Kalender ist für mehrere Personen gedacht. Es gibt keinen festen Empfängernamen, die Anrede ist durchgehend „du“.
Absender ist Thilo.

| | Adresse |
|---|---|
| **LIVE** | https://adventsgeschichten.tkagel.de/ |
| **TEST** | https://adventsgeschichten.tkagel.de/test/ |
| GitHub-Repository | `vanallen84/advents-geschichten` |
| Alte GitHub-Adresse (leitet weiter) | https://vanallen84.github.io/advents-geschichten/ |

Stand dieser Beschreibung: November 2026, Service-Worker-Version `advent-v13`.

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

---

## 1. Schnellstart: Was muss ich nächstes Jahr tun?

Wenn der Kalender in einem neuen Jahr wieder laufen soll:

1. **config.js:** `JAHR` auf das neue Jahr setzen.
   Dadurch ändert sich auch der Speicher-Präfix (`weihnacht2027_` …), alle Leser beginnen also mit einem leeren Kalender.
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
├── ton/
│   ├── knarren.mp3       Ton beim Öffnen einer Tür (Portal)
│   └── wirbel.mp3        Ton beim Buchstaben-Wirbel
├── erinnerung/
│   └── 1700.ics … 2100.ics   Kalender-Termine, je eine Datei pro Uhrzeit
├── test/
│   └── index.html        Weiterleitung auf index.html?test=1
└── tools/
    ├── bilder-vorbereiten.py   Rohbilder zuschneiden und verkleinern
    ├── pixel.py                Verpixelte Kachel-Bilder erzeugen
    ├── erinnerung.py           .ics-Dateien erzeugen
    ├── test-symbole.py         Erzeugt die TEST-Symbole mit rotem Band
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
  EMPFAENGER_NAME: "",                 // leer = kein Name (Kalender für mehrere Personen)
  ABSENDER: "Thilo",                   // erscheint in der Finale-Signatur
  JAHR: 2026,                          // Jahr, in dem die Türchen im Dezember aufgehen
  SEITEN_URL: "https://adventsgeschichten.tkagel.de/",  // für die Links in den .ics-Terminen
  KALENDER_TITEL: "Dein Adventskalender",               // Überschrift der Startseite
  VORTEST_NOVEMBER: false              // false = LIVE (immer so lassen!)
};
```

- **EMPFAENGER_NAME:** In den Begrüßungssätzen steht an einigen Stellen `{name}`.
  - Ist ein Name eingetragen, wird `{name}` ersetzt.
  - Ist das Feld leer, verschwindet `{name}` samt Komma (Funktion `mitName`).
  - Aus „Guten Morgen, {name}. …“ wird dann „Guten Morgen. …“.
- **ABSENDER:**
  - Erscheint als Signatur „Frohe Weihnachten, Thilo“ auf der Finale-Seite.
  - Die Zeile unter der Überschrift der Startseite ist **fest** „Von mir, nur für dich!“ und hängt nicht von `ABSENDER` ab.
- **JAHR:** Steuert die Freischaltung, den Speicher-Präfix und die .ics-Termine (über `tools/erinnerung.py`).
- **SEITEN_URL:** Wird nur von `tools/erinnerung.py` gelesen und in die Termine geschrieben. Nach einer Änderung die .ics-Dateien neu erzeugen.
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
  - Gelöscht werden: geöffnete Türchen, Lesepositionen, Begrüßungs-Verlauf, „Finale gesehen“, „schon mal besucht“, gespeicherte Titel.
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
- **Zurück-Geste (Wischen/Zurück-Taste):**
  - Auf Einstimmung, Geschichte und Finale führt sie zurück in die Übersicht und verlässt die Seite nicht.
  - Während einer Animation wird die Geste ignoriert.
- **Antippen überspringt Animationen** (Portal, Wirbel, Finale).

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

- **Überschrift** aus `KALENDER_TITEL`, darunter fest **„Von mir, nur für dich!“**.
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
- **Begrüßungssatz** unter der Überschrift, abhängig von der Tageszeit:
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
- Knopf **„Zum Finale“**: sichtbar ab dem 25. Dezember oder sobald Türchen 24 geöffnet wurde.
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
- **Lesefortschritt:** dünner goldener Balken ganz oben.
- **Leseposition:**
  - Wird beim Scrollen gespeichert und beim erneuten Öffnen **innerhalb von 12 Stunden** wiederhergestellt.
  - Ganz oben (unter 2 %) und ganz unten (über 97 %) wird nichts gespeichert. Wer zu Ende gelesen hat, fängt beim nächsten Mal oben an.
- **Bildschirm bleibt an**, solange eine Geschichte offen ist (Wake Lock, wo das Gerät es unterstützt).
- **Fehler beim Laden:** Meldung „Dieses Türchen lässt sich gerade nicht laden …“ mit Knopf „Nochmal versuchen“.
  Der Knopf lädt die Datei mit einem Zusatz (`?n=1`, `?n=2` …) neu, damit kein veralteter Speicher dazwischenfunkt.

### 7.5 Finale

- Erscheint nach Türchen 24 („Zum Finale …“) oder über den Knopf in der Übersicht.
- Überschrift „Frohe Weihnachten“, zwei Absätze Dank und Wünsche (Eigenformulierung), Signatur „Frohe Weihnachten, Thilo“.
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

### 8.2 Buchstaben-Wirbel – von der Einstimmung zur Geschichte (`wirbelUebergang`)

- Nach „Geschichte beginnen“ lösen sich **alle Buchstaben der Einstimmungsseite** (bis zu 640) und beginnen zu glühen.
- Sie kreisen in Bahnen um die Bildschirmmitte.
- Dann fliegen sie an die Stellen von **Titel und Anfang der Geschichte** und verwandeln sich unterwegs in die richtigen Buchstaben.
- Danach blendet die echte Geschichte ein.
- Dauer etwa 4–5 s, spätestens nach 14 s ist Schluss.
- Nach 1,8 s erscheint unten „Tippen zum Überspringen“.

### 8.3 Finale-Animation (`finaleDurch`, Variante B „Die 24 Lichter“)

- Läuft beim ersten Weg von Türchen 24 zum Finale (etwa 15 s).
- 24 goldene Lichter (für die 24 Türchen) fügen sich zu einem **Tannenbaum**, dann zu einem **Stern**.
- Der Stern wird zur **Sternschnuppe**, am Ende folgt ein **Lichtblitz**, und die Finale-Seite erscheint.
- Sie läuft nur **einmal** von selbst (Speicher-Schlüssel `finaleAn`). Danach kann man sie über „Die Animation noch einmal ansehen“ wieder abspielen.
- **Variante A „Vier Kerzen“** (Adventskranz) ist noch im Code und wird mit `window.FINALE_VAR = "A"` aktiviert.

### 8.4 Töne

Zwei Toneffekte begleiten die Animationen:

| Datei | Wann | Ende |
|---|---|---|
| `ton/knarren.mp3` | sobald die **Portal-Animation** startet, also bei jedem Öffnen einer Tür, egal ob über eine Kachel in der Übersicht oder über „Weiter durch das nächste Türchen“, und egal ob das Türchen schon einmal geöffnet war | spielt bis zum Ende der Datei; wird die Animation übersprungen oder ist sie vorbei, wird der Ton in 0,5 s ausgeblendet |
| `ton/wirbel.mp3` | sobald der **Buchstaben-Wirbel** startet (nach „Geschichte beginnen“) | wird am Ende des Wirbels oder beim Überspringen in 0,7 s ausgeblendet |

- Umgesetzt im Modul `TON` in index.html (`TON.spielen(name)`, `TON.ausblenden(name, ms)`).
  Die Dateinamen stehen dort in `DATEIEN`.
- **Ton nur mit Animation:** Läuft keine Animation (Einstellung „Bewegung reduzieren“, `PORTAL_AUS`, sehr kurze Einstimmung), gibt es auch keinen Ton.
- **Handys spielen Töne nur nach einer Berührung.** Das passt hier immer, weil Portal und Wirbel direkt durch ein Tippen starten. Würde man die Animationen künftig automatisch (ohne Tippen) starten, bliebe der Ton stumm.
- **Fehlt eine Datei** oder blockiert das Gerät den Ton, laufen die Animationen ganz normal weiter, nur ohne Ton.
- **Länge der Dateien:** Am besten passt das Knarren mit ca. 1,5–2 s (so lange öffnet sich die Tür), der Wirbel mit ca. 4–5 s. Längere Dateien werden am Ende der Animation ausgeblendet.
- **Lautstärke:** Die Dateien werden mit voller Lautstärke abgespielt. Ist ein Ton zu laut, die Datei selbst leiser machen.
  Auf dem iPhone lässt sich die Lautstärke per Skript nicht ändern; dort wird beim „Ausblenden“ nach der Zeit einfach angehalten.
- **Stummschalter am iPhone:** Je nach iOS-Version spielt Safari die Töne auch bei eingeschaltetem Stummschalter oder eben nicht. Die normale Lautstärke des Handys gilt immer.
- **Kein Offline-Ton:** Die Töne laufen absichtlich nicht über den Service Worker (siehe [Abschnitt 13](#13-offline-fähigkeit-und-updates-service-worker)). Ohne Netz bleibt es daher still.
- Töne austauschen: Datei mit **gleichem Namen** in `ton/` ersetzen. Sonst muss `DATEIEN` im Modul `TON` angepasst werden.
- Zum Abschalten aller Töne beim Testen: `window.TON_AUS = true` in der Browser-Konsole.

### 8.5 Kleinere Effekte

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
Es gibt **keine Übertragung an einen Server**. Jedes Gerät und jeder Browser hat seinen eigenen Stand.

| Schlüssel | Inhalt |
|---|---|
| `geoeffnet` | Liste der geöffneten Türchen, z. B. `[1,2,3,5]` |
| `titel` | Titel der geöffneten Geschichten, z. B. `{"1":"Frau Holle"}` |
| `lese` | Leseposition je Türchen: Anteil (0–1) und Zeitpunkt |
| `gruss` | Begrüßungs-„Beutel“ und Verlauf je Tageszeit |
| `finaleAn` | `true`, wenn die Finale-Animation schon gelaufen ist |
| `besucht` | `true` nach dem ersten Besuch (für das Einklappen von „Bevor es losgeht“) |

- Funktioniert `localStorage` nicht (z. B. in manchen privaten Modi), arbeitet die Seite mit einem Ersatz im Arbeitsspeicher.
  Dann geht der Stand beim Schließen verloren, aber nichts stürzt ab.
- **Wichtig für iPhone:** Eine auf dem Startbildschirm installierte Web-App hat **einen anderen Speicher** als Safari.
  Wer erst in Safari liest und dann die App nutzt, beginnt dort von vorn.

---

## 13. Offline-Fähigkeit und Updates (Service Worker)

`sw.js` wird nur über `https` registriert, also nicht beim lokalen Testen über `http://localhost`.

- **Beim ersten Besuch** speichert er im Hintergrund:
  - Seite, `config.js`, Manifeste, Symbole und alle 24 Geschichten,
  - danach alle Bilder (Tagesbilder plus beide Pixelstufen, Start- und Finale-Bild).
- **Seiten und Geschichten:** zuerst aus dem Netz (damit Änderungen sofort ankommen); ohne Netz aus dem Speicher.
- **Bilder:** zuerst aus dem Speicher (schnell), sonst aus dem Netz.
- Gespeichert werden nur erfolgreiche Antworten (`res.ok`). Fehlerseiten landen also nicht im Speicher.
- `.ics`-Dateien werden nie gespeichert.
- **Töne (`ton/`) werden ebenfalls nie über den Service Worker geladen.**
  Safari holt Audio in Teilstücken (Range-Anfragen). Eine zwischengespeicherte Antwort beantwortet das nicht sauber, und der Ton würde auf dem iPhone dann gar nicht spielen.
  Die Töne kommen also immer direkt aus dem Netz (und aus dem normalen Browser-Speicher).

### Updates

> **Bei jeder Änderung `VERSION` in `sw.js` hochzählen** (`advent-v11` → `advent-v12` …).

- Eine neue Version löscht beim Aktivieren den alten Speicher und lädt alles neu.
- Ohne neue Version kommen **geänderte Bilder** auf Handys, die die Seite schon kennen, nicht an. Bilder werden zuerst aus dem Speicher geholt.
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
| `erinnerung.py` | `erinnerung/1700.ics` … `2100.ics`, liest `JAHR` und `SEITEN_URL` aus `config.js` | `python3 tools/erinnerung.py` |
| `bild-prompts.md` | 26 Gemini-Prompts mit gemeinsamem Stil-Block | – |
| `platzhalter.py` | **Veraltet.** Erzeugte Platzhalterbilder vor den echten Bildern. **Nicht mehr ausführen**, es überschreibt die echten Bilder! | – |

Alle Skripte im Hauptordner des Projekts starten. Benötigt wird Python 3, für die Bild-Skripte zusätzlich Pillow.

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

Der Service Worker ist lokal nicht aktiv (nur https), daher gibt es keine Speicher-Probleme beim Entwickeln.

### 17.3 Automatisch mit Playwright (so wurde entwickelt)

- Handy-Ansicht: 390×844, `is_mobile`, `has_touch`, Zeitzone Europe/Berlin, Sprache de-DE.
- Uhrzeit fälschen mit `page.clock.install(time=...)`, z. B. 10. Dezember 10:00 Uhr.
- Gespeicherten Stand vorgeben über `localStorage.setItem('weihnacht2026_geoeffnet', '[1,2,3]')`.
- Geprüft wurden u. a.:
  - Kachelzustände an verschiedenen Tagen (30. Nov., 1., 10., 24., 25., 27. Dez.),
  - Portal-Ablauf per Screenshots zu bestimmten Zeitpunkten,
  - Weiter-Knopf, Finale, Fehler beim Laden, Zurück-Geste,
  - Einklappen der Karten, TEST-Manifest,
  - keine Fehler in der Browser-Konsole.

### 17.4 Was nur auf echten Geräten zuverlässig prüfbar ist

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
- **Ton spielt nicht:** Datei wirklich unter `ton/knarren.mp3` bzw. `ton/wirbel.mp3` (Kleinschreibung beachten, GitHub unterscheidet Groß/Klein)? Handy-Lautstärke an? Am iPhone ggf. Stummschalter prüfen. Format MP3 funktioniert auf allen gängigen Handys.
- **`titel:` in den Geschichten-Dateien** muss als `"…"`-String stehen, sonst kann `titelNachladen` ihn nicht lesen. Die Geschichte selbst funktioniert aber trotzdem.

---

## 19. Interne Schalter für Entwickler

| Schalter | Ort | Wirkung |
|---|---|---|
| `const testModus = false;` | index.html | `true`: **alle** Türchen offen und eine Entwickler-Leiste oben mit Tagesauswahl. **Niemals so hochladen.** |
| `window.FINALE_VAR = "B";` | index.html | `"A"` = Finale „Vier Kerzen“, `"B"` = „Die 24 Lichter“ |
| `window.PORTAL_AUS = true` | Browser-Konsole | schaltet Portal, Wirbel und Finale-Animation ab |
| `window.TON_AUS = true` | Browser-Konsole | schaltet beide Töne ab |
| `window.PORTAL_FARBE = true` | Browser-Konsole | Portal nur golden, ohne Bild |
| `VORTEST_NOVEMBER` | config.js | November = Dezember auch auf LIVE (nicht mehr nötig, TEST-Fassung nutzen) |
| `?test=1` | Adresse | TEST-Fassung |
| `?reset=1` | Adresse | gespeicherten Stand der Fassung löschen |

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
| Animationen | `portalDurch`, `wirbelUebergang`, `startStory`, `finaleDurch` (mit `bildA`/`bildB`) |
| Töne | `TON.spielen`, `TON.ausblenden` (Dateinamen in `DATEIEN`) |
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
   - Kein fester Empfängername, Absender Thilo.
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

---

## 22. Rechtliches zu Texten und Bildern

- **Texte:** Alle 24 Geschichten sind gemeinfrei. Die Bearbeitung (Modernisierung) ist bei jeder Geschichte in der Quellenzeile vermerkt.
- **Eigenformulierungen:** Einstimmungssätze, Begrüßungssätze, Texte der Startseite und des Finales.
- **Bilder:** Mit Google Gemini erzeugt, für die private Nutzung in diesem Kalender. Keine Fotos realer Personen.
- Die Seite ist privat, nicht in Suchmaschinen gelistet und sammelt keine Daten. Alles bleibt im Browser des Lesers.
