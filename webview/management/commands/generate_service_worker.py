import os
from django.conf import settings
from django.core.management.base import BaseCommand
from django.urls import reverse
from django.apps import apps

class Command(BaseCommand):
    help = 'Generate service-worker.js for PWA caching all static assets and pages'

    def handle(self, *args, **kwargs):
        static_path = os.path.join(settings.BASE_DIR, 'webview', 'static')
        service_worker_path = os.path.join(static_path, 'js', 'service-worker.js')

        if not os.path.exists(static_path):
            self.stdout.write(self.style.ERROR('Static directory does not exist'))
            return

        # Collect all static files to cache
        static_files = []
        for root, dirs, files in os.walk(static_path):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, static_path)
                static_files.append(f'/static/{relative_path.replace("\\", "/")}')

        # Collect all URL patterns (pages)
        url_patterns = self.get_url_patterns()

        # Write service-worker.js
        with open(service_worker_path, 'w') as f:
            f.write(f"const CACHE_NAME = 'pwa-cache-v1';\n")
            f.write(f"const urlsToCache = {static_files + url_patterns};\n\n")
            f.write("""
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME)
        .then((cache) => {
            return cache.addAll(urlsToCache);
        })
    );
});

self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request)
        .then((response) => {
            return response || fetch(event.request);
        })
    );
});

self.addEventListener('activate', (event) => {
    const cacheWhitelist = [CACHE_NAME];
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (!cacheWhitelist.includes(cacheName)) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});
            """)

        self.stdout.write(self.style.SUCCESS(f'Service worker generated at {service_worker_path}'))

    def get_url_patterns(self):
        """Collect all URLs from Django app"""
        urls = []
        for model in apps.get_models():
            try:
                urls.append(reverse(f'{model._meta.app_label}:{model._meta.model_name}_list'))
                urls.append(reverse(f'{model._meta.app_label}:{model._meta.model_name}_detail', args=[1]))  # Example dynamic detail view
            except Exception:
                continue
        return urls
