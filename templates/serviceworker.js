// var CACHE_NAME = 'my-site-cache-v1';
// var urlsToCache = [
//   '/',
//   '/static/images/icons/icon-72x72.png',
//   '/static/images/icons/icon-96x96.png',
//   '/static/css/styles.css', // Add any other assets you want to cache
// ];

// // Install service worker and cache assets
// self.addEventListener('install', function(event) {
//   event.waitUntil(
//     caches.open(CACHE_NAME).then(function(cache) {
//       console.log('Opened cache');
//       return cache.addAll(urlsToCache);
//     })
//   );
// });

// // Fetch cached assets when offline
// self.addEventListener('fetch', function(event) {
//   event.respondWith(
//     caches.match(event.request).then(function(response) {
//       if (response) {
//         return response;  // Serve cached content
//       }
//       return fetch(event.request);  // Fetch from network if not in cache
//     })
//   );
// });
