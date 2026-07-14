from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from blog.content_pipeline.fifarosters_scraper import import_fifarosters_assets


class Command(BaseCommand):
    help = (
        'Importa fundos de cartas FIFA 26 do FifaRosters (create-card + fut26.css) '
        'para static/blog/card_assets/fifarosters/.'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--no-download',
            action='store_true',
            help='Só gera manifest.json a partir do CSS/HTML, sem baixar PNGs.',
        )
        parser.add_argument(
            '--dest',
            type=str,
            default='',
            help='Pasta de destino (padrão: static/blog/card_assets/fifarosters).',
        )

    def handle(self, *args, **options):
        if options['dest']:
            dest = Path(options['dest'])
        else:
            dest = (
                Path(settings.BASE_DIR)
                / 'blog'
                / 'static'
                / 'blog'
                / 'card_assets'
                / 'fifarosters'
            )

        self.stdout.write(f'Importando para {dest} …')
        manifest = import_fifarosters_assets(
            dest,
            download=not options['no_download'],
        )
        self.stdout.write(self.style.SUCCESS(
            f"Concluído: {manifest['styles_count']} estilos, "
            f"{manifest['styles_with_image']} com imagem, "
            f"{manifest['images_downloaded']} PNGs em disco."
        ))
        if manifest.get('errors'):
            self.stdout.write(self.style.WARNING(
                f"{len(manifest['errors'])} download(s) falharam (ver manifest.json)."
            ))
