import os

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Import frontend dependencies for serving as static files'

    def handle(self, *args, **options):
        os.system("git clone https://github.com/gurayyarar/AdminBSBMaterialDesign.git bench/static/")
