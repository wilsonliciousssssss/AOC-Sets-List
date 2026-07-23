/* Alpha Omega Collective — Gig Playlists · service worker.
   Network-first for HTML (so new gigs show up immediately once online),
   cache-first for static assets. Bump CACHE to force a refresh. */
const CACHE = 'aoc-gigs-v1';
const CORE = [
  './', './index.html', './tokens.css', './app.webmanifest',
  './assets/gigs.js',
  './assets/icons/icon-192.png', './assets/icons/icon-512.png',
  './assets/icons/apple-touch-icon.png', './assets/icons/favicon-32.png'
];

self.addEventListener('install', e => {
  self.skipWaiting();
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(CORE).catch(() => {})));
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const isHTML = req.mode === 'navigate' ||
    (req.headers.get('accept') || '').includes('text/html') ||
    req.url.endsWith('.html');

  if (isHTML) {
    // network-first: latest set sheets & index win when online
    e.respondWith(
      fetch(req).then(res => {
        const copy = res.clone();
        caches.open(CACHE).then(c => c.put(req, copy)).catch(() => {});
        return res;
      }).catch(() => caches.match(req).then(r => r || caches.match('./index.html')))
    );
  } else {
    // cache-first for assets
    e.respondWith(
      caches.match(req).then(r => r || fetch(req).then(res => {
        const copy = res.clone();
        caches.open(CACHE).then(c => c.put(req, copy)).catch(() => {});
        return res;
      }).catch(() => r))
    );
  }
});
