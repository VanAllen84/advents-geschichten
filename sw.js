/* Offline-Speicher: Seite, Geschichten und Bilder werden beim ersten Besuch abgelegt.
   Bei jeder Änderung an der Seite VERSION hochzählen, damit die Handys die neue Fassung holen. */
const VERSION = "advent-v28";
const KERN = ["./", "index.html", "config.js", "manifest.json", "manifest-test.json", "icon-192.png", "icon-512.png", "apple-touch-icon.png", "icon-test-192.png", "icon-test-512.png", "apple-touch-icon-test.png"];
for (let i = 1; i <= 24; i++) KERN.push("story-day" + i + ".js");
const BILDER = ["bilder/landing.jpg", "bilder/finale.jpg"];
for (let i = 1; i <= 24; i++) {
  const n = String(i).padStart(2, "0");
  BILDER.push("bilder/tag-" + n + ".jpg", "bilder/pix-mid-" + n + ".png", "bilder/pix-lock-" + n + ".png");
}
const TOENE = ["ton/knarren.mp3", "ton/zuklappen.mp3", "ton/wirbel.mp3", "ton/finale.mp3", "ton/umschlag.mp3"];
self.addEventListener("install", function (e) {
  e.waitUntil(caches.open(VERSION).then(function (c) {
    return Promise.all(KERN.map(function (u) { return c.add(u).catch(function () {}); }))
      .then(function () { return Promise.all(BILDER.map(function (u) { return c.add(u).catch(function () {}); })); })
      .then(function () { return Promise.all(TOENE.map(function (u) { return c.add(u).catch(function () {}); })); });
  }).then(function () { return self.skipWaiting(); }));
});
self.addEventListener("activate", function (e) {
  e.waitUntil(caches.keys().then(function (ks) {
    // alte Versionen löschen – aber nicht die Angaben für die Push-Erinnerung (Name, Fassung)
    return Promise.all(ks.filter(function (k) { return k !== VERSION && k !== "advent-push-info"; }).map(function (k) { return caches.delete(k); }));
  }).then(function () { return self.clients.claim(); }));
});
self.addEventListener("fetch", function (e) {
  const r = e.request;
  if (r.method !== "GET" || new URL(r.url).origin !== location.origin) return;
  // Kalender-Termine nie aus dem Speicher (immer frisch laden)
  if (/\/erinnerung\//.test(r.url)) return;
  if (/\/ton\//.test(r.url)) {
    // Töne: aus dem Speicher, auch offline. Safari fragt Audio in Teilstücken an
    // (Range-Anfragen, z. B. "bytes=0-1"); die werden aus der gespeicherten Datei mit 206 beantwortet.
    e.respondWith(caches.match(r.url, { ignoreSearch: true }).then(function (m) {
      if (!m) {
        // noch nicht gespeichert: aus dem Netz; eine vollständige, erfolgreiche Antwort wird abgelegt
        return fetch(r).then(function (res) {
          if (res.ok && res.status === 200 && !r.headers.get("range")) { const k = res.clone(); caches.open(VERSION).then(function (c) { c.put(r.url, k); }); }
          return res;
        });
      }
      const rg = r.headers.get("range");
      if (!rg) return m;
      return m.arrayBuffer().then(function (buf) {
        const len = buf.byteLength, mm = /bytes=(\d*)-(\d*)/.exec(rg);
        let s = mm && mm[1] ? +mm[1] : 0, en = mm && mm[2] ? +mm[2] : len - 1;
        if (mm && !mm[1] && mm[2]) { s = Math.max(0, len - +mm[2]); en = len - 1; }   // "bytes=-500" = die letzten 500 Bytes
        en = Math.min(en, len - 1);
        if (s > en || s >= len) return new Response(null, { status: 416, headers: { "Content-Range": "bytes */" + len } });
        return new Response(buf.slice(s, en + 1), { status: 206, headers: { "Content-Type": "audio/mpeg", "Content-Range": "bytes " + s + "-" + en + "/" + len, "Content-Length": String(en - s + 1), "Accept-Ranges": "bytes" } });
      });
    }));
    return;
  }
  if (/\/bilder\//.test(r.url)) {
    // Bilder: zuerst aus dem Speicher
    e.respondWith(caches.match(r).then(function (m) { return m || fetch(r).then(function (res) { if (res.ok) { const k = res.clone(); caches.open(VERSION).then(function (c) { c.put(r, k); }); } return res; }); }));
  } else {
    // Seite und Geschichten: zuerst Netz (damit Änderungen sofort erscheinen).
    // Antwortet das Netz nicht innerhalb von 1,5 s und liegt eine gespeicherte Fassung vor, kommt diese –
    // die App startet dann sofort statt auf ein langsames Mobilnetz zu warten. Die Netzantwort wird trotzdem
    // im Hintergrund gespeichert und ist beim nächsten Öffnen da. Ohne Netz: aus dem Speicher.
    const netz = fetch(r).then(function (res) { if (res.ok) { const k = res.clone(); caches.open(VERSION).then(function (c) { c.put(r, k); }); } return res; });
    const ausSpeicher = function () { return caches.match(r, { ignoreSearch: true }).then(function (m) { return m || caches.match("index.html"); }); };
    e.respondWith(new Promise(function (fertig) {
      let erledigt = false;
      const nimm = function (x) { if (!erledigt && x) { erledigt = true; fertig(x); } };
      const uhr = setTimeout(function () { ausSpeicher().then(nimm); }, 1500);
      netz.then(function (res) { clearTimeout(uhr); nimm(res); })
          .catch(function () { clearTimeout(uhr); ausSpeicher().then(function (m) { nimm(m || Response.error()); }); });
    }));
    e.waitUntil(netz.catch(function () {}));
  }
});

// ---------- Push-Erinnerung ----------
// Der Worker schickt ein leeres Signal. Den Text baut der Service Worker aus Datum, Name und Fassung
// (von der Seite im Cache „advent-push-info“ abgelegt): „Anna, Türchen 5 wartet auf dich“.
function berlinHeute() {
  const f = new Intl.DateTimeFormat("de-DE", { timeZone: "Europe/Berlin", month: "numeric", day: "numeric" });
  const t = {}; f.formatToParts(new Date()).forEach(function (p) { t[p.type] = p.value; });
  return { monat: +t.month, tag: +t.day };
}
function pushInfo() {
  return caches.open("advent-push-info").then(function (c) { return c.match("info"); })
    .then(function (r) { return r ? r.json() : {}; }).catch(function () { return {}; });
}
self.addEventListener("push", function (e) {
  e.waitUntil(pushInfo().then(function (info) {
    const h = berlinHeute(), monat = info.test ? 11 : 12, name = info.name ? String(info.name) : "";
    const tuerchen = h.monat === monat && h.tag >= 1 && h.tag <= 24;
    // vom 1. bis 24.: „Anna, Türchen 5 wartet auf dich“; sonst (Testnachricht): „Anna, so sieht deine Erinnerung aus“
    const titel = tuerchen
      ? (name ? name + ", Türchen " : "Türchen ") + h.tag + " wartet auf dich"
      : (name ? name + ", so" : "So") + " sieht deine Erinnerung aus";
    return self.registration.showNotification(titel, {
      icon: info.test ? "icon-test-192.png" : "icon-192.png",
      tag: "advent-erinnerung",
      data: { url: (info.url || "./index.html") + ((info.url || "").indexOf("?") >= 0 ? "&" : "?") + "von=erinnerung" }
    });
  }));
});
self.addEventListener("notificationclick", function (e) {
  e.notification.close();
  const ziel = new URL((e.notification.data && e.notification.data.url) || "./index.html", self.registration.scope).href;
  // Ist der Kalender schon offen: nach vorn holen und ihm sagen, dass er zum heutigen Türchen springen soll.
  // Sonst neu öffnen – mit „von=erinnerung“ in der Adresse, das erledigt dann die Seite.
  const istTest = /[?&]test=1/.test(ziel);
  e.waitUntil(self.clients.matchAll({ type: "window", includeUncontrolled: true }).then(function (fenster) {
    const passend = fenster.filter(function (f) { return /[?&]test=1/.test(f.url) === istTest; });
    for (const f of passend) {
      if ("focus" in f) return f.focus().then(function (x) { (x || f).postMessage({ typ: "erinnerung" }); return x; });
    }
    return self.clients.openWindow ? self.clients.openWindow(ziel) : null;
  }));
});
