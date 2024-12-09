from django.core.management.base import BaseCommand
from blog.models import Estadio

class Command(BaseCommand):
    help = 'Cria os estádios históricos iniciais'

    def handle(self, *args, **kwargs):
        estadios = [
            # Europa
            {
                'nome': 'Camp Nou',
                'cidade': 'Barcelona',
                'pais': 'Espanha',
                'continente': 'EU',
                'capacidade': 99354,
                'descricao': 'Casa do FC Barcelona, é o maior estádio da Europa. Cenário de grandes partidas da Champions League e da La Liga.'
            },
            {
                'nome': 'Santiago Bernabéu',
                'cidade': 'Madri',
                'pais': 'Espanha',
                'continente': 'EU',
                'capacidade': 81044,
                'descricao': 'Estádio do Real Madrid, sede de várias finais de Champions League e jogos históricos.'
            },
            {
                'nome': 'Old Trafford',
                'cidade': 'Manchester',
                'pais': 'Inglaterra',
                'continente': 'EU',
                'capacidade': 74140,
                'descricao': 'Conhecido como "O Teatro dos Sonhos", é a casa do Manchester United.'
            },
            # América do Sul
            {
                'nome': 'Maracanã',
                'cidade': 'Rio de Janeiro',
                'pais': 'Brasil',
                'continente': 'AS',
                'capacidade': 78838,
                'descricao': 'Cenário de duas finais de Copa do Mundo (1950 e 2014) e dos Jogos Olímpicos de 2016.'
            },
            {
                'nome': 'La Bombonera',
                'cidade': 'Buenos Aires',
                'pais': 'Argentina',
                'continente': 'AS',
                'capacidade': 54000,
                'descricao': 'Estádio do Boca Juniors, famoso pela acústica e atmosfera vibrante.'
            },
            # América do Norte
            {
                'nome': 'Azteca',
                'cidade': 'Cidade do México',
                'pais': 'México',
                'continente': 'AN',
                'capacidade': 87523,
                'descricao': 'Único estádio a sediar duas finais de Copa do Mundo (1970 e 1986).'
            },
            # África
            {
                'nome': 'Soccer City',
                'cidade': 'Johanesburgo',
                'pais': 'África do Sul',
                'continente': 'AF',
                'capacidade': 94736,
                'descricao': 'Sede da final da Copa do Mundo de 2010.'
            },
            # Ásia
            {
                'nome': 'Saitama Stadium 2002',
                'cidade': 'Saitama',
                'pais': 'Japão',
                'continente': 'ASI',
                'capacidade': 63700,
                'descricao': 'Casa da seleção japonesa, cenário de jogos memoráveis na Copa do Mundo de 2002.'
            },
            # Oceania
            {
                'nome': 'Stadium Australia',
                'cidade': 'Sydney',
                'pais': 'Austrália',
                'continente': 'OC',
                'capacidade': 83500,
                'descricao': 'Sede dos Jogos Olímpicos de 2000.'
            },
        ]

        for estadio_data in estadios:
            Estadio.objects.get_or_create(
                nome=estadio_data['nome'],
                defaults=estadio_data
            )
            self.stdout.write(
                self.style.SUCCESS(f'Estádio {estadio_data["nome"]} criado com sucesso!')
            )
