/* ==========================================================
   Einstellungen des Adventskalenders
   Hier kannst du alles anpassen, ohne im Code suchen zu müssen.
   ========================================================== */
window.ADVENT_CONFIG = {
  // Name der beschenkten Person. Leer lassen: Dann wird der Name verwendet, den die Person
  // auf der Startseite selbst eingibt (freiwillig).
  EMPFAENGER_NAME: "",

  // Wer den Kalender verschenkt (steht auf der Startseite und unter dem Finale)
  ABSENDER: "Thilo",

  // Jahr, in dem die Türchen im Dezember aufgehen
  JAHR: 2026,

  // Adresse der fertigen Seite, z. B. "https://name.github.io/advent/"
  // (wird für die Links in den Kalender-Terminen gebraucht, kommt später)
  SEITEN_URL: "https://adventsgeschichten.tkagel.de/",

  // Überschrift der Startseite
  KALENDER_TITEL: "Dein Adventskalender",

  // Online-Sicherung des Fortschritts (eigener Cloudflare-Worker „advent-stand“).
  // Adresse des Workers, z. B. "https://advent-stand.DEIN-NAME.workers.dev" – leer = keine Online-Sicherung.
  SYNC_URL: "https://advent-stand.solitary-bird-2ffc.workers.dev/",

  // Fester Zusatz, aus dem zusammen mit dem eingegebenen Vornamen der Speicher-Schlüssel berechnet wird.
  // NICHT mehr ändern, sonst findet der Kalender die gesicherten Stände nicht wieder.
  SYNC_ZUSATZ: "eh9ctfrCSkCAeFapQ2ZRvDlv",

  // false = LIVE: es gilt das echte Datum (so bleibt es auf der Hauptadresse).
  // Zum Vorab-Testen gibt es die TEST-Fassung unter .../advents-geschichten/test/
  // (dort wird der November wie der Dezember behandelt, mit eigenem Speicher).
  VORTEST_NOVEMBER: false
};
