from django.core.management.base import BaseCommand
from blog.models import Estadio

class Command(BaseCommand):
    help = 'Cria estádios icônicos no banco de dados'

    def handle(self, *args, **kwargs):
        estadios = [
            # Europa
            {
                'nome': 'Camp Nou',
                'cidade': 'Barcelona',
                'pais': 'Espanha',
                'continente': 'EU',
                'capacidade': 99000,
                'descricao': 'Casa do FC Barcelona, com capacidade para mais de 99.000 pessoas. Cenário de grandes partidas da Champions League e da La Liga.'
            },
            {
                'nome': 'Santiago Bernabéu',
                'cidade': 'Madri',
                'pais': 'Espanha',
                'continente': 'EU',
                'capacidade': 81000,
                'descricao': 'Estádio do Real Madrid, com capacidade para 81.000 pessoas. Sede de várias finais de Champions League e jogos históricos.'
            },
            {
                'nome': 'Old Trafford',
                'cidade': 'Manchester',
                'pais': 'Inglaterra',
                'continente': 'EU',
                'capacidade': 74000,
                'descricao': 'Conhecido como "O Teatro dos Sonhos", é a casa do Manchester United. Capacidade para cerca de 74.000 torcedores.'
            },
            {
                'nome': 'Anfield',
                'cidade': 'Liverpool',
                'pais': 'Inglaterra',
                'continente': 'EU',
                'capacidade': 54000,
                'descricao': 'Estádio do Liverpool FC, famoso pela atmosfera única e pelo canto "You\'ll Never Walk Alone". Capacidade para 54.000 torcedores.'
            },
            {
                'nome': 'San Siro',
                'cidade': 'Milão',
                'pais': 'Itália',
                'continente': 'EU',
                'capacidade': 80000,
                'descricao': 'Casa do AC Milan e Inter de Milão, com capacidade para 80.000 pessoas. Cenário de várias finais da Champions League.'
            },
            {
                'nome': 'Allianz Arena',
                'cidade': 'Munique',
                'pais': 'Alemanha',
                'continente': 'EU',
                'capacidade': 75000,
                'descricao': 'Estádio moderno do Bayern de Munique, famoso por sua fachada iluminada. Capacidade para 75.000 torcedores.'
            },
            {
                'nome': 'Stamford Bridge',
                'cidade': 'Londres',
                'pais': 'Inglaterra',
                'continente': 'EU',
                'capacidade': 42000,
                'descricao': 'Casa do Chelsea FC, com capacidade para 42.000 torcedores. História rica no futebol inglês e europeu.'
            },
            {
                'nome': 'Signal Iduna Park',
                'cidade': 'Dortmund',
                'pais': 'Alemanha',
                'continente': 'EU',
                'capacidade': 81000,
                'descricao': 'Estádio do Borussia Dortmund, famoso pelo "Muro Amarelo" da torcida. Capacidade para mais de 81.000 pessoas.'
            },
            {
                'nome': 'Parc des Princes',
                'cidade': 'Paris',
                'pais': 'França',
                'continente': 'EU',
                'capacidade': 48000,
                'descricao': 'Casa do Paris Saint-Germain, com capacidade para 48.000 torcedores. Cenário de grandes conquistas nacionais e europeias.'
            },
            {
                'nome': 'Estádio da Luz',
                'cidade': 'Lisboa',
                'pais': 'Portugal',
                'continente': 'EU',
                'capacidade': 65000,
                'descricao': 'Casa do SL Benfica, com capacidade para 65.000 torcedores. Sede da final da Champions League em 2014 e 2020.'
            },
            # América do Sul
            {
                'nome': 'Maracanã',
                'cidade': 'Rio de Janeiro',
                'pais': 'Brasil',
                'continente': 'AS',
                'capacidade': 78000,
                'descricao': 'Cenário de duas finais de Copa do Mundo (1950 e 2014) e dos Jogos Olímpicos de 2016. Capacidade para cerca de 78.000 torcedores.'
            },
            {
                'nome': 'La Bombonera',
                'cidade': 'Buenos Aires',
                'pais': 'Argentina',
                'continente': 'AS',
                'capacidade': 54000,
                'descricao': 'Estádio do Boca Juniors, famoso pela acústica e atmosfera vibrante. Capacidade para 54.000 torcedores.'
            },
            {
                'nome': 'Monumental de Núñez',
                'cidade': 'Buenos Aires',
                'pais': 'Argentina',
                'continente': 'AS',
                'capacidade': 83000,
                'descricao': 'Casa do River Plate, o maior estádio da Argentina. Capacidade para cerca de 83.000 pessoas.'
            },
            {
                'nome': 'Morumbi',
                'cidade': 'São Paulo',
                'pais': 'Brasil',
                'continente': 'AS',
                'capacidade': 67000,
                'descricao': 'Estádio do São Paulo FC, com capacidade para 67.000 torcedores. Cenário de grandes finais de Libertadores.'
            },
            {
                'nome': 'Mineirão',
                'cidade': 'Belo Horizonte',
                'pais': 'Brasil',
                'continente': 'AS',
                'capacidade': 62000,
                'descricao': 'Sede da Copa do Mundo de 2014 e das Olimpíadas de 2016. Capacidade para 62.000 torcedores.'
            },
            {
                'nome': 'Arena do Grêmio',
                'cidade': 'Porto Alegre',
                'pais': 'Brasil',
                'continente': 'AS',
                'capacidade': 60000,
                'descricao': 'Estádio moderno com capacidade para 60.000 torcedores. Sede de finais da Libertadores e Sul-Americana.'
            },
            # América do Norte
            {
                'nome': 'Azteca',
                'cidade': 'Cidade do México',
                'pais': 'México',
                'continente': 'AN',
                'capacidade': 87000,
                'descricao': 'Único estádio a sediar duas finais de Copa do Mundo (1970 e 1986). Capacidade para 87.000 torcedores.'
            },
            {
                'nome': 'Rose Bowl',
                'cidade': 'Pasadena',
                'pais': 'Estados Unidos',
                'continente': 'AN',
                'capacidade': 88000,
                'descricao': 'Sede da final da Copa do Mundo de 1994 e do futebol nos Jogos Olímpicos de 1984. Capacidade para 88.000 torcedores.'
            },
            # África
            {
                'nome': 'Soccer City (FNB Stadium)',
                'cidade': 'Johanesburgo',
                'pais': 'África do Sul',
                'continente': 'AF',
                'capacidade': 94000,
                'descricao': 'Sede da final da Copa do Mundo de 2010. Capacidade para 94.000 torcedores.'
            },
            {
                'nome': 'Estádio Olímpico de Radès',
                'cidade': 'Túnis',
                'pais': 'Tunísia',
                'continente': 'AF',
                'capacidade': 60000,
                'descricao': 'Um dos estádios mais modernos da África, com capacidade para 60.000 pessoas.'
            },
            # Ásia
            {
                'nome': 'Saitama Stadium 2002',
                'cidade': 'Saitama',
                'pais': 'Japão',
                'continente': 'ASI',
                'capacidade': 63000,
                'descricao': 'Casa da seleção japonesa, com capacidade para 63.000 torcedores. Cenário de jogos memoráveis na Copa do Mundo de 2002.'
            },
            {
                'nome': 'Azadi Stadium',
                'cidade': 'Teerã',
                'pais': 'Irã',
                'continente': 'ASI',
                'capacidade': 78000,
                'descricao': 'Maior estádio do Irã, com capacidade para 78.000 torcedores.'
            },
            # Oceania
            {
                'nome': 'Stadium Australia',
                'cidade': 'Sydney',
                'pais': 'Austrália',
                'continente': 'OC',
                'capacidade': 83000,
                'descricao': 'Sede dos Jogos Olímpicos de 2000. Capacidade para 83.000 torcedores.'
            }
        ]

        for estadio_data in estadios:
            estadio, created = Estadio.objects.get_or_create(
                nome=estadio_data['nome'],
                defaults=estadio_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Estádio "{estadio.nome}" criado com sucesso!'))
            else:
                self.stdout.write(self.style.WARNING(f'Estádio "{estadio.nome}" já existe.'))
