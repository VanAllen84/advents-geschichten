/* Offline-Speicher: Seite, Geschichten und Bilder werden beim ersten Besuch abgelegt.
   Bei jeder Änderung an der Seite VERSION hochzählen, damit die Handys die neue Fassung holen. */
const VERSION = "advent-v11";
const KERN = ["./", "index.html", "config.js", "manifest.json", "manifest-test.json", "icon-192.png", "icon-512.png", "apple-touch-icon.png"];
for (let i = 1; i <= 24; i++) KERN.push("story-day" + i + ".js");
const BILDER = ["bilder/landing.jpg", "bilder/finale.jpg"];
for (let i = 1; i <= 24; i++) {
  const n = String(i).padStart(2, "0");
  BILDER.push("bilder/tag-" + n + ".jpg", "bilder/pix-mid-" + n + ".png", "bilder/pix-lock-" + n + ".png");
}
self.addEventListener("install", function (e) {
  e.waitUntil(caches.open(VERSION).then(function (c) {
    return Promise.all(KERN.map(function (u) { return c.add(u).catch(function () {}); }))
      .then(function () { return Promise.all(BILDER.map(function (u) { return c.add(u).catch(function () {}); })); });
  }).then(function () { return self.skipWaiting(); }));
});
self.addEventListener("activate", function (e) {
  e.waitUntil(caches.keys().then(function (ks) {
    return Promise.all(ks.filter(function (k) { return k !== VERSION; }).map(function (k) { return caches.delete(k); }));
  }).then(function () { return self.clients.claim(); }));
});
self.addEventListener("fetch", function (e) {
  const r = e.request;
  if (r.method !== "GET" || new URL(r.url).origin !== location.origin) return;
  // Kalender-Termine nie aus dem Speicher (immer frisch laden)
  if (/\/erinnerung\//.test(r.url)) return;
  if (/\/bilder\//.test(r.url)) {
    // Bilder: zuerst aus dem Speicher
    e.respondWith(caches.match(r).then(function (m) { return m || fetch(r).then(function (res) { if (res.ok) { const k = res.clone(); caches.open(VERSION).then(function (c) { c.put(r, k); }); } return res; }); }));
  } else {
    // Seite und Geschichten: zuerst Netz (damit Änderungen sofort erscheinen), ohne Netz aus dem Speicher
    e.respondWith(fetch(r).then(function (res) { if (res.ok) { const k = res.clone(); caches.open(VERSION).then(function (c) { c.put(r, k); }); } return res; }).catch(function () { return caches.match(r, { ignoreSearch: true }).then(function (m) { return m || caches.match("index.html"); }); }));
  }
});
