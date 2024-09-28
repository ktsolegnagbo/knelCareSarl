import os
import json
from django.conf import settings
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Generate manifest.json for PWA from all static files and folders in the app'

    def handle(self, *args, **kwargs):
        static_path = os.path.join(settings.BASE_DIR, 'static')

        if not os.path.exists(static_path):
            self.stdout.write(self.style.ERROR('Static directory does not exist'))
            return

        icons = []
        start_url = '/'
        
        for root, dirs, files in os.walk(static_path):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, static_path)

                if relative_path.endswith(('.png', '.jpg', '.jpeg', '.ico')):
                    
                    relative_path = relative_path.replace("\\", "/")
                    file_info = {
                        'src': f'/static/{relative_path}',
                        'sizes': 'auto',  # You can set specific sizes for icons if needed
                        'type': f'image/{file.split(".")[-1]}'
                    }
                    icons.append(file_info)

        # Manifest data
        manifest_data = {
            'name': 'Your App Name',
            'short_name': 'App',
            'start_url': start_url,
            'display': 'standalone',
            'background_color': '#ffffff',
            'theme_color': '#000000',
            'icons': icons
        }

        # Write the manifest.json file in the static directory
        manifest_file = os.path.join(static_path, 'manifest.json')
        with open(manifest_file, 'w') as f:
            json.dump(manifest_data, f, indent=4)

        self.stdout.write(self.style.SUCCESS(f'Manifest file generated at {manifest_file}'))
