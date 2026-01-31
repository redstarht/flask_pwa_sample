const CACHE_NAME = 'flask-pwa-v1'; // キャッシュ名を統一
const urlsToCache = [
  '/',
  '/static/manifest.json',
  '/static/icon-192.png',
  '/static/icon-512.png',
  '/static/style.css', // 新しく追加するCSS
  '/static/app.js', // 既存のJS
  '/login', // ログインページ
  '/register', // 登録ページ
  '/dashboard', // ダッシュボードページ (ログイン後)
  // 必要に応じて他の静的ファイルやHTMLページを追加
];

// インストール時にキャッシュ
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(urlsToCache);
    })
  );
});

// オフライン時は "/" を返す
self.addEventListener('fetch', event => {
  event.respondWith(
    fetch(event.request).catch(() => {
      return caches.match(event.request).then(response => {
        return response || caches.match('/');
      });
    })
  );
});
