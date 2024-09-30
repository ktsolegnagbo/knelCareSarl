const CACHE_NAME = 'my-pwa-cache-v' + new Date().getTime();
const DATA_CACHE_NAME = 'data-cache-v1';

const ROUTES_PATH = [
  '/',
  '/update_app_site/',
  '/register/',
  '/login/',
  '/logout/',
  '/products/',
  '/admin-products/',
  '/admin-clients/',
  '/admin-stocks/',
  '/admin-users/',
  '/admin-payrolls/',
  '/admin-sales/',
  '/shopping/',
  '/sales/make_payment/',
  '/sale/print/sale_proformat/'
];

const FILES_TO_CACHE = [
  ...ROUTES_PATH,
  '/static/manifest.json',
  '/static/icons/icon-192x192.png',
  '/static/icons/icon-512x512.png',
  '/static/jspdf.min.js'
];

// Install Event - Caching Static Assets
self.addEventListener('install', event => {
  console.log('[ServiceWorker] Install');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('[ServiceWorker] Pre-caching offline page');
        return cache.addAll(FILES_TO_CACHE);
      })
  );
  self.skipWaiting(); // Forces the waiting service worker to become the active service worker
});

// Activate Event - Cleaning Up Old Caches
self.addEventListener('activate', event => {
  console.log('[ServiceWorker] Activate');
  event.waitUntil(
    caches.keys().then(keyList => {
      return Promise.all(
        keyList.map(key => {
          if (key !== CACHE_NAME && key !== DATA_CACHE_NAME) {
            console.log('[ServiceWorker] Removing old cache', key);
            return caches.delete(key);
          }
        })
      );
    })
  );
  self.clients.claim(); // Takes control of all clients immediately
});

// Fetch Event - Cache First Strategy with handling for redirected responses
self.addEventListener('fetch', event => {
  const isRoutePath = ROUTES_PATH.some(path => event.request.url.includes(path));

  if (isRoutePath) {
    // Handle API requests with network-first strategy
    event.respondWith(
      caches.open(DATA_CACHE_NAME).then(async cache => {
        try {
          const response = await fetch(event.request);
          
          // Check if the response is redirected
          if (response.redirected) {
            const clonedResponse = response.clone();
            const body = await clonedResponse.text();

            // Recreate the response and ensure it's valid
            const recreatedResponse = new Response(body, {
              status: clonedResponse.status,
              statusText: clonedResponse.statusText,
              headers: clonedResponse.headers,
            });
            return recreatedResponse;
          }

          if (response.status === 200) {
            cache.put(event.request.url, response.clone());
          }
          return response;
        } catch (error) {
          return cache.match(event.request);
        }
      })
    );
  } else {
    // Handle other requests with cache-first strategy
    event.respondWith(
      caches.match(event.request).then(response => {
        return response || fetch(event.request);
      })
    );
  }
});


// Sync Event - Background Sync
self.addEventListener('sync', event => {
  if (event.tag === 'sync-data') {
    event.waitUntil(syncData());
  }
});

// Dummy syncData function for background sync
async function syncData() {
  console.log('Syncing data...');
  // Your background sync logic goes here
  // You can interact with IndexedDB or your backend API
}
