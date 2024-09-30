// const CACHE_NAME = 'my-pwa-cache-v' + new Date().getTime();
// const DATA_CACHE_NAME = 'data-cache-v1';

// const ROUTES_PATH = [
//   '/',
//   '/update_app_site/',
//   '/register/',
//   '/login/',
//   '/logout/',
//   '/products/',
//   '/admin-products/',
//   '/admin-clients/',
//   '/admin-stocks/',
//   '/admin-users/',
//   '/admin-payrolls/',
//   '/admin-sales/',
//   '/shopping/',
//   '/sales/make_payment/',
//   '/sale/print/sale_proformat/'
//   // '/sales/make-rest-payment/',
//   // '/sales/payment/success/',
//   // '/sale/print/',
// ];

// const FILES_TO_CACHE = [
//   ...ROUTES_PATH,
//   '/static/manifest.json',
//   '/static/icons/icon-192x192.png',
//   '/static/icons/icon-512x512.png',
//   '/static/jspdf.min.js'
//   // '/static/core/app.js',
//   // '/static/core/style.css',
// ];

// // Install Event - Caching Static Assets
// self.addEventListener('install', event => {
//   console.log('[ServiceWorker] Install');
//   event.waitUntil(
//     caches.open(CACHE_NAME)
//       .then(cache => {
//         console.log('[ServiceWorker] Pre-caching offline page');
//         console.log(cache);
//         return cache.addAll(FILES_TO_CACHE);
//       })
//   );
//   self.skipWaiting();
// });

// // Activate Event - Cleaning Up Old Caches
// self.addEventListener('activate', event => {
//   console.log('[ServiceWorker] Activate');
//   event.waitUntil(
//     caches.keys().then(keyList => {
//       return Promise.all(keyList.map(key => {
//         if (key !== CACHE_NAME && key !== DATA_CACHE_NAME) {
//           console.log('[ServiceWorker] Removing old cache', key);
//           return caches.delete(key);
//         }
//       }));
//     })
//   );
//   self.clients.claim();
// });

// // Fetch Event - Cache First Strategy
// self.addEventListener('fetch', event => {
//   let found = false;
//   for (const path in ROUTES_PATH) {
//     if (event.request.url.includes(path)) {
//       found = true;
//       break;
//     }
//   }


//   if (found == true) {
//     // Handle API requests with network-first strategy
//     event.respondWith(
//       caches.open(DATA_CACHE_NAME).then(cache => {
//         return fetch(event.request.clone())
//           .then(response => {
//             if (response.status === 200) {
//               cache.put(event.request.url, response.clone());
//             }
//             return response;
//           })
//           .catch(() => {
//             return cache.match(event.request);
//           });
//       })
//     );
//     return;
//   } else {
//     // Handle other requests with cache-first strategy
//     event.respondWith(
//       caches.match(event.request)
//         .then(response => {
//           return response || fetch(event.request.clone());
//         })
//     );
//   }
// });

// // Sync Event - Background Sync
// self.addEventListener('sync', event => {
//   if (event.tag === 'sync-data') {
//       event.waitUntil(syncData());
//   }
// });

// // Dummy syncData function for background sync
// async function syncData() {
//   console.log('Syncing data...');
//   // Your background sync logic goes here
//   // You can interact with IndexedDB or your backend API
// }
