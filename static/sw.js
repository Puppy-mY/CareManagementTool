const CACHE_NAME = 'care-management-v2';

// キャッシュしてよい静的アセットのみ
const STATIC_ASSETS = [
  '/static/manifest.json',
];

// 個人・医療データを含むルート — キャッシュ禁止
const SENSITIVE_PATHS = ['/clients/', '/assessments/', '/facilities/'];

const isSensitive = pathname =>
  SENSITIVE_PATHS.some(p => pathname.startsWith(p));

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(STATIC_ASSETS))
  );
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key))
      )
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);

  if (url.origin !== location.origin) return;
  if (request.method !== 'GET') return;

  // 個人・医療データは常にネットワーク（キャッシュしない）
  if (isSensitive(url.pathname)) return;

  // 静的ファイル → キャッシュ優先
  if (url.pathname.startsWith('/static/')) {
    event.respondWith(
      caches.open(CACHE_NAME).then(cache =>
        cache.match(request).then(cached => {
          if (cached) return cached;
          return fetch(request).then(response => {
            cache.put(request, response.clone());
            return response;
          });
        })
      )
    );
    return;
  }

  // その他のページ → ネットワーク優先、オフライン時のみキャッシュ提供
  event.respondWith(
    caches.open(CACHE_NAME).then(cache =>
      fetch(request)
        .then(response => {
          cache.put(request, response.clone());
          return response;
        })
        .catch(() => cache.match(request))
    )
  );
});
