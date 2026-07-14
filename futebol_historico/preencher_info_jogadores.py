import os
import django
from datetime import date

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'futebol_historico.settings')
django.setup()

from blog.models import Jogador

# Dados completos dos jogadores
dados_jogadores = {
    'Adriano Imperador': {
        'nacionalidade': 'Brasil',
        'inicio_carreira': date(1999, 1, 1),
        'fim_carreira': date(2016, 1, 1),
        'altura': '1,89 m',
        'perna': 'Canhoto',
        'outras_posicoes': 'Ponta-esquerda',
        'titulos_champions': 0,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': 'Adriano Leite Ribeiro, conhecido como "Imperador", foi um dos atacantes mais temidos de sua geração. Com físico imponente e chute potente, brilhou na Inter de Milão e na seleção brasileira. Foi campeão da Copa América de 2004 e artilheiro do torneio.',
        'carreira': '<p><strong>Fluminense (1999-2000)</strong> - Início da carreira profissional</p><p><strong>Inter de Milão (2001-2009)</strong> - Maior período, onde se consagrou</p><p><strong>Flamengo (2009-2010)</strong> - Retorno ao Brasil</p><p><strong>Roma (2010-2011)</strong> - Passagem pela Itália</p><p><strong>Corinthians (2011-2012)</strong> - Últimos anos no Brasil</p>'
    },
    'Alex Del Piero': {
        'nacionalidade': 'Itália',
        'inicio_carreira': date(1991, 1, 1),
        'fim_carreira': date(2014, 1, 1),
        'altura': '1,73 m',
        'perna': 'Destro',
        'outras_posicoes': 'Meia-atacante, Ponta-direita',
        'titulos_champions': 1,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': 'Alessandro Del Piero é uma lenda da Juventus e do futebol italiano. Jogou 19 temporadas pelo clube turinês, sendo o maior artilheiro da história do clube. Campeão da Copa do Mundo de 2006 pela Itália e da Liga dos Campeões de 1996.',
        'carreira': '<p><strong>Padova (1991-1993)</strong> - Início profissional</p><p><strong>Juventus (1993-2012)</strong> - 19 temporadas, maior ídolo do clube</p><p><strong>Sydney FC (2012-2014)</strong> - Final da carreira na Austrália</p>'
    },
    'Roberto Baggio': {
        'nacionalidade': 'Itália',
        'inicio_carreira': date(1982, 1, 1),
        'fim_carreira': date(2004, 1, 1),
        'altura': '1,74 m',
        'perna': 'Destro',
        'outras_posicoes': 'Meia-atacante',
        'titulos_champions': 0,
        'bola_de_ouro': 1,
        'mundial_clubes': 0,
        'biografia': 'Roberto Baggio, "Il Divin Codino", é considerado um dos maiores jogadores italianos de todos os tempos. Vencedor da Bola de Ouro em 1993, foi conhecido por sua técnica refinada, dribles e capacidade de decidir jogos. Marcou 27 gols em 56 jogos pela seleção italiana.',
        'carreira': '<p><strong>Vicenza (1982-1985)</strong> - Início</p><p><strong>Fiorentina (1985-1990)</strong> - Consolidação</p><p><strong>Juventus (1990-1995)</strong> - Melhor fase</p><p><strong>Milan (1995-1997)</strong> - Passagem</p><p><strong>Inter de Milão (1998-2000)</strong> - Últimos anos na Itália</p><p><strong>Brescia (2000-2004)</strong> - Final da carreira</p>'
    },
    'Bebeto': {
        'nacionalidade': 'Brasil',
        'inicio_carreira': date(1982, 1, 1),
        'fim_carreira': date(2002, 1, 1),
        'altura': '1,76 m',
        'perna': 'Destro',
        'outras_posicoes': 'Ponta-esquerda',
        'titulos_champions': 0,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': 'José Roberto Gama de Oliveira, o Bebeto, foi um dos maiores atacantes brasileiros. Campeão mundial em 1994, formou dupla histórica com Romário. Ficou famoso pelo gesto de "bebê" na Copa de 1994, celebrando o nascimento de seu filho.',
        'carreira': '<p><strong>Flamengo (1982-1989)</strong> - Início e consolidação</p><p><strong>Vasco (1989-1991)</strong> - Passagem</p><p><strong>Deportivo La Coruña (1992-1996)</strong> - Melhor fase na Europa</p><p><strong>Flamengo (1996-1997)</strong> - Retorno</p><p><strong>Botafogo (1997-1999)</strong> - Últimos anos</p>'
    },
    'Casagrande': {
        'nacionalidade': 'Brasil',
        'inicio_carreira': date(1980, 1, 1),
        'fim_carreira': date(1993, 1, 1),
        'altura': '1,80 m',
        'perna': 'Destro',
        'outras_posicoes': 'Meia-atacante',
        'titulos_champions': 0,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': 'Walter Casagrande foi um dos maiores atacantes brasileiros dos anos 80. Conhecido por sua força física e faro de gol, brilhou no Corinthians e na seleção brasileira. Participou das Copas de 1982 e 1986.',
        'carreira': '<p><strong>Corinthians (1980-1986)</strong> - Maior período</p><p><strong>Ascoli (1986-1987)</strong> - Passagem na Itália</p><p><strong>Corinthians (1987-1991)</strong> - Retorno</p><p><strong>Fluminense (1991-1993)</strong> - Final da carreira</p>'
    },
    'Edgar Davids': {
        'nacionalidade': 'Holanda',
        'inicio_carreira': date(1991, 1, 1),
        'fim_carreira': date(2014, 1, 1),
        'altura': '1,69 m',
        'perna': 'Destro',
        'outras_posicoes': 'Volante, Meia-central',
        'titulos_champions': 1,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': 'Edgar Davids, o "Pitbull", foi um dos meio-campistas mais dominantes de sua geração. Conhecido por seus óculos de proteção e estilo agressivo, era um volante completo com marcação forte e qualidade técnica. Brilhou na Juventus e Ajax.',
        'carreira': '<p><strong>Ajax (1991-1996)</strong> - Início e consolidação</p><p><strong>Milan (1996-1997)</strong> - Passagem</p><p><strong>Juventus (1997-2004)</strong> - Melhor fase</p><p><strong>Inter de Milão (2004-2005)</strong> - Passagem</p><p><strong>Tottenham (2005-2007)</strong> - Final na Europa</p>'
    },
    'Deco': {
        'nacionalidade': 'Brasil',
        'inicio_carreira': date(1996, 1, 1),
        'fim_carreira': date(2013, 1, 1),
        'altura': '1,74 m',
        'perna': 'Destro',
        'outras_posicoes': 'Meia-central, Meia-atacante',
        'titulos_champions': 2,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': 'Anderson Luís de Souza, o Deco, foi um dos maiores meio-campistas brasileiros. Naturalizado português, foi fundamental nas conquistas da Liga dos Campeões pelo Porto e Barcelona. Conhecido por sua visão de jogo e passes precisos.',
        'carreira': '<p><strong>Salgueiros (1996-1997)</strong> - Início em Portugal</p><p><strong>Porto (1999-2004)</strong> - Consolidação e títulos</p><p><strong>Barcelona (2004-2008)</strong> - Melhor fase</p><p><strong>Chelsea (2008-2010)</strong> - Passagem</p><p><strong>Fluminense (2010-2013)</strong> - Final no Brasil</p>'
    },
    'Didier Drogba': {
        'nacionalidade': 'Costa do Marfim',
        'inicio_carreira': date(1998, 1, 1),
        'fim_carreira': date(2018, 1, 1),
        'altura': '1,89 m',
        'perna': 'Destro',
        'outras_posicoes': 'Ponta-direita',
        'titulos_champions': 1,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': 'Didier Drogba é o maior ídolo da história do Chelsea e um dos maiores atacantes africanos. Com físico imponente e chute potente, foi decisivo na conquista da Liga dos Campeões de 2012. Maior artilheiro da história da seleção da Costa do Marfim.',
        'carreira': '<p><strong>Le Mans (1998-2002)</strong> - Início na França</p><p><strong>Marseille (2003-2004)</strong> - Consolidação</p><p><strong>Chelsea (2004-2012, 2014-2015)</strong> - Maior período</p><p><strong>Galatasaray (2013-2014)</strong> - Passagem</p><p><strong>Montreal Impact (2015-2017)</strong> - Final da carreira</p>'
    },
    'Dunga': {
        'nacionalidade': 'Brasil',
        'inicio_carreira': date(1983, 1, 1),
        'fim_carreira': date(2000, 1, 1),
        'altura': '1,77 m',
        'perna': 'Destro',
        'outras_posicoes': 'Volante, Zagueiro',
        'titulos_champions': 0,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': 'Carlos Caetano Bledorn Verri, o Dunga, foi capitão da seleção brasileira campeã mundial em 1994. Volante de marcação e liderança, foi fundamental na conquista. Também foi técnico da seleção brasileira em duas passagens.',
        'carreira': '<p><strong>Internacional (1983-1984)</strong> - Início</p><p><strong>Corinthians (1984-1985)</strong> - Passagem</p><p><strong>Pisa (1987-1988)</strong> - Itália</p><p><strong>Fiorentina (1988-1992)</strong> - Melhor fase na Europa</p><p><strong>Pescara (1992-1993)</strong> - Passagem</p><p><strong>VfB Stuttgart (1993-1995)</strong> - Alemanha</p><p><strong>Júbilo Iwata (1995-1998)</strong> - Japão</p><p><strong>Internacional (1999-2000)</strong> - Final da carreira</p>'
    },
    'Edmundo': {
        'nacionalidade': 'Brasil',
        'inicio_carreira': date(1991, 1, 1),
        'fim_carreira': date(2011, 1, 1),
        'altura': '1,77 m',
        'perna': 'Destro',
        'outras_posicoes': 'Meia-atacante',
        'titulos_champions': 0,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': 'Edmundo Alves de Souza Neto, o "Animal", foi um dos atacantes mais talentosos e polêmicos do futebol brasileiro. Conhecido por sua técnica refinada e personalidade forte, brilhou no Vasco, Palmeiras e Flamengo. Participou da Copa de 1998.',
        'carreira': '<p><strong>Vasco (1991-1993, 1995-1996, 2000-2001)</strong> - Maior período</p><p><strong>Palmeiras (1993-1995)</strong> - Consolidação</p><p><strong>Fiorentina (1996-1997)</strong> - Passagem na Itália</p><p><strong>Flamengo (1997-1999)</strong> - Passagem</p><p><strong>Corinthians (2001-2002)</strong> - Passagem</p>'
    },
    "Samuel Eto'o": {
        'nacionalidade': 'Camarões',
        'inicio_carreira': date(1997, 1, 1),
        'fim_carreira': date(2019, 1, 1),
        'altura': '1,80 m',
        'perna': 'Destro',
        'outras_posicoes': 'Ponta-direita',
        'titulos_champions': 3,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': "Samuel Eto'o é considerado um dos maiores jogadores africanos de todos os tempos. Atacante veloz e com faro de gol, foi fundamental nas conquistas da Liga dos Campeões pelo Barcelona e Inter de Milão. Maior artilheiro da história da seleção de Camarões.",
        'carreira': '<p><strong>Real Madrid (1997-2000)</strong> - Início</p><p><strong>Mallorca (2000-2004)</strong> - Consolidação</p><p><strong>Barcelona (2004-2009)</strong> - Melhor fase</p><p><strong>Inter de Milão (2009-2011)</strong> - Títulos</p><p><strong>Anzhi (2011-2013)</strong> - Passagem</p><p><strong>Chelsea (2013-2014)</strong> - Passagem</p>'
    },
    'Felipe': {
        'nacionalidade': 'Brasil',
        'inicio_carreira': date(1980, 1, 1),
        'fim_carreira': date(1995, 1, 1),
        'altura': '1,75 m',
        'perna': 'Destro',
        'outras_posicoes': 'Meia-atacante',
        'titulos_champions': 0,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': 'Felipe foi um atacante brasileiro que brilhou principalmente no Flamengo nos anos 80. Conhecido por sua técnica e capacidade de finalização, foi importante nas conquistas do clube carioca.',
        'carreira': '<p><strong>Flamengo (1980-1987)</strong> - Maior período</p><p><strong>Vasco (1987-1989)</strong> - Passagem</p><p><strong>Flamengo (1989-1992)</strong> - Retorno</p>'
    },
    'Ruud Gullit': {
        'nacionalidade': 'Holanda',
        'inicio_carreira': date(1979, 1, 1),
        'fim_carreira': date(1998, 1, 1),
        'altura': '1,91 m',
        'perna': 'Destro',
        'outras_posicoes': 'Meia-atacante, Volante',
        'titulos_champions': 2,
        'bola_de_ouro': 1,
        'mundial_clubes': 0,
        'biografia': 'Ruud Gullit foi um dos maiores jogadores holandeses de todos os tempos. Vencedor da Bola de Ouro em 1987, era um jogador completo que podia atuar em várias posições. Campeão da Eurocopa de 1988 e da Liga dos Campeões pelo Milan.',
        'carreira': '<p><strong>Haarlem (1979-1982)</strong> - Início</p><p><strong>Feyenoord (1982-1985)</strong> - Consolidação</p><p><strong>PSV (1985-1987)</strong> - Melhor fase na Holanda</p><p><strong>Milan (1987-1993)</strong> - Maior período</p><p><strong>Sampdoria (1993-1995)</strong> - Passagem</p>'
    },
    'Júlio César': {
        'nacionalidade': 'Brasil',
        'inicio_carreira': date(1997, 1, 1),
        'fim_carreira': date(2018, 1, 1),
        'altura': '1,86 m',
        'perna': 'Destro',
        'outras_posicoes': 'Goleiro',
        'titulos_champions': 1,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': 'Júlio César Soares de Espíndola foi um dos melhores goleiros brasileiros de sua geração. Brilhou na Inter de Milão, onde conquistou a Liga dos Campeões de 2010. Foi titular da seleção brasileira na Copa de 2010 e 2014.',
        'carreira': '<p><strong>Flamengo (1997-2004)</strong> - Início e consolidação</p><p><strong>Chievo (2005)</strong> - Passagem na Itália</p><p><strong>Inter de Milão (2005-2012)</strong> - Melhor fase</p><p><strong>Queens Park Rangers (2012-2014)</strong> - Inglaterra</p><p><strong>Benfica (2014-2017)</strong> - Portugal</p>'
    },
    'Kaká': {
        'nacionalidade': 'Brasil',
        'inicio_carreira': date(2001, 1, 1),
        'fim_carreira': date(2017, 1, 1),
        'altura': '1,86 m',
        'perna': 'Destro',
        'outras_posicoes': 'Meia-atacante, Ponta-direita',
        'titulos_champions': 1,
        'bola_de_ouro': 1,
        'mundial_clubes': 0,
        'biografia': 'Ricardo Izecson dos Santos Leite, o Kaká, foi um dos meio-campistas mais elegantes do futebol. Vencedor da Bola de Ouro em 2007, se destacou no Milan onde conquistou a Liga dos Campeões. Campeão mundial em 2002 pela seleção brasileira.',
        'carreira': '<p><strong>São Paulo (2001-2003)</strong> - Início</p><p><strong>Milan (2003-2009, 2013-2014)</strong> - Melhor fase</p><p><strong>Real Madrid (2009-2013)</strong> - Passagem</p><p><strong>Orlando City (2014-2017)</strong> - Final da carreira</p>'
    },
    'Diego Maradona': {
        'nacionalidade': 'Argentina',
        'inicio_carreira': date(1976, 1, 1),
        'fim_carreira': date(1997, 1, 1),
        'altura': '1,65 m',
        'perna': 'Canhoto',
        'outras_posicoes': 'Meia-atacante, Ponta-esquerda',
        'titulos_champions': 0,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': 'Diego Armando Maradona é considerado por muitos o maior jogador de todos os tempos. Sua técnica extraordinária, dribles desconcertantes e liderança o tornaram uma lenda. Foi protagonista da conquista da Copa do Mundo de 1986 pela Argentina e ídolo máximo do Napoli.',
        'carreira': '<p><strong>Argentinos Juniors (1976-1981)</strong> - Início</p><p><strong>Boca Juniors (1981-1982, 1995-1997)</strong> - Ídolo</p><p><strong>Barcelona (1982-1984)</strong> - Passagem</p><p><strong>Napoli (1984-1991)</strong> - Maior fase</p><p><strong>Sevilla (1992-1993)</strong> - Passagem</p>'
    },
    'Pavel Nedvěd': {
        'nacionalidade': 'República Tcheca',
        'inicio_carreira': date(1991, 1, 1),
        'fim_carreira': date(2009, 1, 1),
        'altura': '1,77 m',
        'perna': 'Destro',
        'outras_posicoes': 'Meia-central, Ponta-esquerda',
        'titulos_champions': 0,
        'bola_de_ouro': 1,
        'mundial_clubes': 0,
        'biografia': 'Pavel Nedvěd foi um meio-campista completo, conhecido por sua incrível resistência física e qualidade técnica. Vencedor da Bola de Ouro em 2003, o tcheco se tornou uma lenda da Juventus, onde sua dedicação e habilidade o transformaram em um dos melhores jogadores da história do clube.',
        'carreira': '<p><strong>Dukla Prague (1991-1992)</strong> - Início</p><p><strong>Sparta Prague (1992-1996)</strong> - Consolidação</p><p><strong>Lazio (1996-2001)</strong> - Melhor fase inicial</p><p><strong>Juventus (2001-2009)</strong> - Maior período</p>'
    },
    'Pelé': {
        'nacionalidade': 'Brasil',
        'inicio_carreira': date(1956, 1, 1),
        'fim_carreira': date(1977, 1, 1),
        'altura': '1,73 m',
        'perna': 'Destro',
        'outras_posicoes': 'Meia-atacante',
        'titulos_champions': 0,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': 'Edson Arantes do Nascimento, o Pelé, é considerado o maior jogador de todos os tempos. Único tricampeão mundial (1958, 1962, 1970), marcou mais de mil gols na carreira. Revolucionou o futebol com sua técnica, velocidade e capacidade de decidir jogos.',
        'carreira': '<p><strong>Santos (1956-1974)</strong> - Maior período, ídolo máximo</p><p><strong>New York Cosmos (1975-1977)</strong> - Final da carreira</p>'
    },
    'Raí': {
        'nacionalidade': 'Brasil',
        'inicio_carreira': date(1984, 1, 1),
        'fim_carreira': date(2000, 1, 1),
        'altura': '1,89 m',
        'perna': 'Destro',
        'outras_posicoes': 'Meia-atacante, Volante',
        'titulos_champions': 0,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': 'Raí Souza Vieira de Oliveira foi um dos maiores meio-campistas brasileiros. Irmão de Sócrates, foi campeão mundial em 1994 e capitão do São Paulo que dominou o futebol mundial nos anos 90. Conhecido por sua técnica refinada e liderança.',
        'carreira': '<p><strong>Botafogo-SP (1984-1986)</strong> - Início</p><p><strong>São Paulo (1986-1993)</strong> - Maior período</p><p><strong>Paris Saint-Germain (1993-1998)</strong> - Melhor fase na Europa</p><p><strong>São Paulo (1998-2000)</strong> - Final da carreira</p>'
    },
    'Frank Rijkaard': {
        'nacionalidade': 'Holanda',
        'inicio_carreira': date(1980, 1, 1),
        'fim_carreira': date(1995, 1, 1),
        'altura': '1,90 m',
        'perna': 'Destro',
        'outras_posicoes': 'Volante, Zagueiro',
        'titulos_champions': 2,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': 'Frank Rijkaard foi um dos maiores volantes da história do futebol. Jogador completo que podia atuar também como zagueiro, foi fundamental nas conquistas da Liga dos Campeões pelo Milan e Ajax. Campeão da Eurocopa de 1988 pela Holanda.',
        'carreira': '<p><strong>Ajax (1980-1987, 1993-1995)</strong> - Maior período</p><p><strong>Real Zaragoza (1987-1988)</strong> - Passagem</p><p><strong>Milan (1988-1993)</strong> - Melhor fase</p>'
    },
    'Juan Román Riquelme': {
        'nacionalidade': 'Argentina',
        'inicio_carreira': date(1996, 1, 1),
        'fim_carreira': date(2015, 1, 1),
        'altura': '1,82 m',
        'perna': 'Canhoto',
        'outras_posicoes': 'Meia-atacante',
        'titulos_champions': 0,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': 'Juan Román Riquelme foi um dos últimos grandes engenheiros do futebol. Meio-campista clássico, com visão de jogo extraordinária e passes precisos, é considerado um dos maiores ídolos da história do Boca Juniors. Sua forma de jogar, pausada e cerebral, o tornou único.',
        'carreira': '<p><strong>Boca Juniors (1996-2002, 2007-2014)</strong> - Maior período, ídolo</p><p><strong>Barcelona (2002-2003)</strong> - Passagem</p><p><strong>Villarreal (2003-2007)</strong> - Melhor fase na Europa</p><p><strong>Argentinos Juniors (2014-2015)</strong> - Final da carreira</p>'
    },
    'Rivaldo': {
        'nacionalidade': 'Brasil',
        'inicio_carreira': date(1991, 1, 1),
        'fim_carreira': date(2015, 1, 1),
        'altura': '1,86 m',
        'perna': 'Canhoto',
        'outras_posicoes': 'Meia-atacante, Ponta-esquerda',
        'titulos_champions': 1,
        'bola_de_ouro': 1,
        'mundial_clubes': 0,
        'biografia': 'Rivaldo foi um dos jogadores mais talentosos de sua geração. Vencedor da Bola de Ouro em 1999, o brasileiro era conhecido por seus gols espetaculares e habilidade técnica impressionante. Foi peça fundamental na conquista da Copa do Mundo de 2002 pela seleção brasileira.',
        'carreira': '<p><strong>Santa Cruz (1991-1992)</strong> - Início</p><p><strong>Mogi Mirim (1992-1993)</strong> - Passagem</p><p><strong>Corinthians (1993-1994)</strong> - Consolidação</p><p><strong>Palmeiras (1994-1996)</strong> - Melhor fase no Brasil</p><p><strong>Deportivo La Coruña (1996-1997)</strong> - Início na Europa</p><p><strong>Barcelona (1997-2002)</strong> - Maior período</p><p><strong>Milan (2002-2004)</strong> - Passagem</p>'
    },
    'Romário': {
        'nacionalidade': 'Brasil',
        'inicio_carreira': date(1985, 1, 1),
        'fim_carreira': date(2009, 1, 1),
        'altura': '1,67 m',
        'perna': 'Destro',
        'outras_posicoes': 'Meia-atacante',
        'titulos_champions': 0,
        'bola_de_ouro': 1,
        'mundial_clubes': 0,
        'biografia': 'Romário é considerado um dos maiores atacantes da história do futebol. Conhecido por sua incrível capacidade de finalização e movimentação dentro da área, foi o principal jogador da seleção brasileira na conquista da Copa do Mundo de 1994. Auto-intitulado "O Baixinho", marcou mais de mil gols na carreira.',
        'carreira': '<p><strong>Vasco (1985-1988, 2000-2002, 2005-2006)</strong> - Maior período</p><p><strong>PSV (1988-1993)</strong> - Melhor fase na Europa</p><p><strong>Barcelona (1993-1995)</strong> - Passagem</p><p><strong>Flamengo (1995-1999, 2002-2004)</strong> - Ídolo</p>'
    },
    'Ronaldinho Gaúcho': {
        'nacionalidade': 'Brasil',
        'inicio_carreira': date(1998, 1, 1),
        'fim_carreira': date(2018, 1, 1),
        'altura': '1,82 m',
        'perna': 'Destro',
        'outras_posicoes': 'Meia-atacante, Ponta-direita',
        'titulos_champions': 1,
        'bola_de_ouro': 1,
        'mundial_clubes': 0,
        'biografia': 'Ronaldinho Gaúcho é considerado um dos jogadores mais habilidosos de todos os tempos. Sua criatividade, dribles e alegria em campo o tornaram um ícone global do futebol. Vencedor da Bola de Ouro em 2005, revolucionou o Barcelona e foi fundamental na conquista da Copa do Mundo de 2002 pelo Brasil.',
        'carreira': '<p><strong>Grêmio (1998-2001)</strong> - Início</p><p><strong>Paris Saint-Germain (2001-2003)</strong> - Consolidação na Europa</p><p><strong>Barcelona (2003-2008)</strong> - Melhor fase</p><p><strong>Milan (2008-2011)</strong> - Passagem</p><p><strong>Flamengo (2011-2012)</strong> - Retorno ao Brasil</p>'
    },
    'Ronaldo Nazário': {
        'nacionalidade': 'Brasil',
        'inicio_carreira': date(1993, 1, 1),
        'fim_carreira': date(2011, 1, 1),
        'altura': '1,83 m',
        'perna': 'Destro',
        'outras_posicoes': 'Ponta-direita',
        'titulos_champions': 0,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': 'Ronaldo Nazário, conhecido como "Fenômeno", é considerado um dos maiores atacantes da história. Sua combinação única de velocidade, força e técnica o tornou praticamente imparável. Vencedor de duas Copas do Mundo (1994 e 2002) e três vezes eleito melhor jogador do mundo pela FIFA.',
        'carreira': '<p><strong>Cruzeiro (1993-1994)</strong> - Início</p><p><strong>PSV (1994-1996)</strong> - Consolidação na Europa</p><p><strong>Barcelona (1996-1997)</strong> - Melhor fase inicial</p><p><strong>Inter de Milão (1997-2002)</strong> - Maior período</p><p><strong>Real Madrid (2002-2007)</strong> - Passagem</p><p><strong>Milan (2007-2008)</strong> - Passagem</p><p><strong>Corinthians (2009-2011)</strong> - Final da carreira</p>'
    },
    'Wesley Sneijder': {
        'nacionalidade': 'Holanda',
        'inicio_carreira': date(2002, 1, 1),
        'fim_carreira': date(2019, 1, 1),
        'altura': '1,70 m',
        'perna': 'Destro',
        'outras_posicoes': 'Meia-atacante, Ponta-direita',
        'titulos_champions': 1,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': 'Wesley Sneijder foi um dos maiores meio-campistas holandeses de sua geração. Fundamental na conquista da Liga dos Campeões pelo Inter de Milão em 2010, foi peça central da seleção holandesa que chegou à final da Copa do Mundo de 2010.',
        'carreira': '<p><strong>Ajax (2002-2007)</strong> - Início e consolidação</p><p><strong>Real Madrid (2007-2009)</strong> - Passagem</p><p><strong>Inter de Milão (2009-2013)</strong> - Melhor fase</p><p><strong>Galatasaray (2013-2017)</strong> - Passagem</p>'
    },
    'Cláudio Taffarel': {
        'nacionalidade': 'Brasil',
        'inicio_carreira': date(1985, 1, 1),
        'fim_carreira': date(2003, 1, 1),
        'altura': '1,85 m',
        'perna': 'Destro',
        'outras_posicoes': 'Goleiro',
        'titulos_champions': 0,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': 'Cláudio André Mergen Taffarel foi um dos maiores goleiros brasileiros. Titular da seleção brasileira campeã mundial em 1994, foi fundamental na conquista. Conhecido por suas defesas decisivas e liderança, é considerado um dos melhores goleiros da história do Brasil.',
        'carreira': '<p><strong>Internacional (1985-1990)</strong> - Início</p><p><strong>Parma (1990-1993)</strong> - Passagem na Itália</p><p><strong>Reggiana (1993-1994)</strong> - Passagem</p><p><strong>Atalanta (1994-1995)</strong> - Passagem</p><p><strong>Galatasaray (1995-1998, 2001-2003)</strong> - Maior período</p><p><strong>Milan (1998-2001)</strong> - Passagem</p>'
    },
    'Francesco Totti': {
        'nacionalidade': 'Itália',
        'inicio_carreira': date(1992, 1, 1),
        'fim_carreira': date(2017, 1, 1),
        'altura': '1,80 m',
        'perna': 'Destro',
        'outras_posicoes': 'Meia-atacante, Ponta-direita',
        'titulos_champions': 0,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': 'Francesco Totti é um dos maiores símbolos de lealdade no futebol. Jogou toda sua carreira pela Roma, tornando-se o maior ídolo da história do clube. Conhecido como "Il Gladiatore" e "Il Re di Roma" (O Rei de Roma), sua técnica refinada e liderança o tornaram uma lenda do futebol italiano.',
        'carreira': '<p><strong>Roma (1992-2017)</strong> - Toda a carreira, ídolo máximo</p>'
    },
    'Marco van Basten': {
        'nacionalidade': 'Holanda',
        'inicio_carreira': date(1981, 1, 1),
        'fim_carreira': date(1995, 1, 1),
        'altura': '1,88 m',
        'perna': 'Destro',
        'outras_posicoes': 'Ponta-direita',
        'titulos_champions': 1,
        'bola_de_ouro': 3,
        'mundial_clubes': 0,
        'biografia': 'Marco van Basten é considerado um dos maiores atacantes da história do futebol. Vencedor de três Bolas de Ouro (1988, 1989, 1992), era conhecido por sua técnica refinada, finalização precisa e gols espetaculares. Campeão da Eurocopa de 1988 pela Holanda.',
        'carreira': '<p><strong>Ajax (1981-1987)</strong> - Início e consolidação</p><p><strong>Milan (1987-1995)</strong> - Melhor fase</p>'
    },
    'Zico': {
        'nacionalidade': 'Brasil',
        'inicio_carreira': date(1971, 1, 1),
        'fim_carreira': date(1994, 1, 1),
        'altura': '1,72 m',
        'perna': 'Canhoto',
        'outras_posicoes': 'Meia-atacante, Ponta-esquerda',
        'titulos_champions': 0,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': 'Arthur Antunes Coimbra, o Zico, é considerado um dos maiores meio-campistas da história do futebol brasileiro. Ídolo máximo do Flamengo, foi conhecido por sua técnica refinada, passes precisos e gols espetaculares. Marcou 48 gols em 71 jogos pela seleção brasileira.',
        'carreira': '<p><strong>Flamengo (1971-1983, 1985-1989)</strong> - Maior período, ídolo máximo</p><p><strong>Udinese (1983-1985)</strong> - Passagem na Itália</p><p><strong>Kashima Antlers (1991-1994)</strong> - Final da carreira no Japão</p>'
    },
    'Zinedine Zidane': {
        'nacionalidade': 'França',
        'inicio_carreira': date(1989, 1, 1),
        'fim_carreira': date(2006, 1, 1),
        'altura': '1,85 m',
        'perna': 'Destro',
        'outras_posicoes': 'Meia-atacante',
        'titulos_champions': 1,
        'bola_de_ouro': 1,
        'mundial_clubes': 0,
        'biografia': 'Zinedine Zidane é considerado um dos maiores meio-campistas da história. Sua elegância em campo, visão de jogo e técnica apurada o tornaram único. Vencedor da Copa do Mundo de 1998 pela França e da Liga dos Campeões pelo Real Madrid, "Zizou" foi eleito melhor jogador do mundo três vezes.',
        'carreira': '<p><strong>Cannes (1989-1992)</strong> - Início</p><p><strong>Bordeaux (1992-1996)</strong> - Consolidação</p><p><strong>Juventus (1996-2001)</strong> - Melhor fase inicial</p><p><strong>Real Madrid (2001-2006)</strong> - Maior período</p>'
    }
}

def preencher_informacoes():
    """Preenche as informações dos jogadores"""
    atualizados = 0
    nao_encontrados = 0
    
    print("📝 Iniciando preenchimento de informações dos jogadores...\n")
    
    for nome_jogador, dados in dados_jogadores.items():
        # Buscar o jogador (case-insensitive)
        jogador = Jogador.objects.filter(nome__iexact=nome_jogador).first()
        
        if not jogador:
            print(f"⚠️  Jogador '{nome_jogador}' não encontrado no banco. Pulando...")
            nao_encontrados += 1
            continue
        
        # Atualizar todos os campos
        jogador.nacionalidade = dados['nacionalidade']
        jogador.inicio_carreira = dados['inicio_carreira']
        jogador.fim_carreira = dados['fim_carreira']
        jogador.altura = dados['altura']
        jogador.perna = dados['perna']
        jogador.outras_posicoes = dados['outras_posicoes']
        jogador.titulos_champions = dados['titulos_champions']
        jogador.bola_de_ouro = dados['bola_de_ouro']
        jogador.mundial_clubes = dados['mundial_clubes']
        jogador.biografia = dados['biografia']
        jogador.carreira = dados['carreira']
        
        jogador.save()
        
        print(f"✅ Informações de '{nome_jogador}' atualizadas com sucesso!")
        atualizados += 1
    
    print("\n" + "="*50)
    print(f"📊 Resumo:")
    print(f"   ✅ Atualizados: {atualizados}")
    print(f"   ⚠️  Não encontrados: {nao_encontrados}")
    print("="*50)

if __name__ == "__main__":
    preencher_informacoes()
    print("\n✨ Processo concluído!")











