from django.core.management.base import BaseCommand
from blog.initial_data import create_historical_teams

class Command(BaseCommand):
    help = 'Cria os times históricos no banco de dados'

    def handle(self, *args, **options):
        create_historical_teams()
        self.stdout.write(self.style.SUCCESS('Times históricos criados com sucesso!'))
