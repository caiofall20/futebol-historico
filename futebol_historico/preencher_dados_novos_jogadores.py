import os
import django
from datetime import date
from django.utils.html import format_html

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'futebol_historico.settings')
django.setup()

from blog.models import Jogador

# Dados completos dos novos jogadores
DADOS_COMPLETOS = {
    'Andriy Shevchenko': {
        'nacionalidade': 'Ucrânia',
        'inicio_carreira': date(1994, 1, 1),
        'fim_carreira': date(2012, 1, 1),
        'altura': '1,83 m',
        'perna': 'Destro',
        'outras_posicoes': 'Centroavante, Ponta-direita',
        'titulos_champions': 1,
        'bola_de_ouro': 1,
        'mundial_clubes': 0,
        'biografia': format_html("""
            <p>Andriy Mykolayovych Shevchenko é considerado o maior jogador ucraniano de todos os tempos. Vencedor da Bola de Ouro em 2004, foi um dos atacantes mais letais da Europa durante sua passagem pelo Milan. Maior artilheiro da história da seleção ucraniana.</p>
            <h3>Dynamo Kyiv (1994-1999)</h3>
            <p>Iniciou sua carreira no Dynamo Kyiv, onde se destacou rapidamente e chamou a atenção dos grandes clubes europeus. Conquistou 5 títulos do Campeonato Ucraniano.</p>
            <h3>Milan (1999-2006, 2008-2009)</h3>
            <p>No Milan, Shevchenko se tornou uma lenda, conquistando a Liga dos Campeões de 2003 e a Bola de Ouro de 2004. É o segundo maior artilheiro da história do clube italiano.</p>
            <h3>Seleção Ucraniana</h3>
            <p>Pela seleção ucraniana, Shevchenko é o maior artilheiro da história, com 48 gols. Liderou a Ucrânia à primeira participação em uma Copa do Mundo em 2006, chegando às quartas de final.</p>
        """),
        'carreira': format_html("""
            <ul>
                <li><strong>Dynamo Kyiv (1994-1999):</strong> 166 jogos, 94 gols</li>
                <li><strong>Milan (1999-2006):</strong> 322 jogos, 175 gols</li>
                <li><strong>Chelsea (2006-2008):</strong> 77 jogos, 22 gols</li>
                <li><strong>Milan (2008-2009):</strong> 26 jogos, 2 gols</li>
                <li><strong>Dynamo Kyiv (2009-2012):</strong> 83 jogos, 36 gols</li>
            </ul>
            <h4>Principais Títulos Coletivos:</h4>
            <ul>
                <li>1x UEFA Champions League</li>
                <li>1x Serie A</li>
                <li>5x Campeonato Ucraniano</li>
                <li>1x Copa da Ucrânia</li>
            </ul>
            <h4>Principais Títulos Individuais:</h4>
            <ul>
                <li>1x Bola de Ouro da FIFA</li>
                <li>Artilheiro da Serie A (2000, 2004)</li>
                <li>Artilheiro da UEFA Champions League (1999, 2006)</li>
            </ul>
        """)
    },
    'Gennaro Gattuso': {
        'nacionalidade': 'Itália',
        'inicio_carreira': date(1995, 1, 1),
        'fim_carreira': date(2013, 1, 1),
        'altura': '1,77 m',
        'perna': 'Destro',
        'outras_posicoes': 'Volante, Meia-central',
        'titulos_champions': 2,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': format_html("""
            <p>Gennaro Ivan Gattuso é um dos maiores volantes da história do futebol italiano. Conhecido por sua agressividade, marcação feroz e liderança, foi fundamental nas conquistas do Milan e da seleção italiana.</p>
            <h3>Milan (1999-2012)</h3>
            <p>No Milan, Gattuso se tornou uma lenda, conquistando 2 Ligas dos Campeões e 2 títulos da Serie A. Formou uma das melhores duplas de meio-campo da história ao lado de Andrea Pirlo.</p>
            <h3>Seleção Italiana</h3>
            <p>Pela seleção italiana, Gattuso foi fundamental na conquista da Copa do Mundo de 2006, sendo um dos principais volantes do time campeão.</p>
        """),
        'carreira': format_html("""
            <ul>
                <li><strong>Perugia (1995-1997):</strong> Início</li>
                <li><strong>Rangers (1997-1998):</strong> Passagem na Escócia</li>
                <li><strong>Salernitana (1998-1999):</strong> Passagem</li>
                <li><strong>Milan (1999-2012):</strong> 468 jogos, 11 gols</li>
                <li><strong>Sion (2012-2013):</strong> Final da carreira</li>
            </ul>
            <h4>Principais Títulos Coletivos:</h4>
            <ul>
                <li>2x UEFA Champions League</li>
                <li>2x Serie A</li>
                <li>1x Copa do Mundo</li>
                <li>1x Copa da Itália</li>
            </ul>
        """)
    },
    'Dennis Bergkamp': {
        'nacionalidade': 'Holanda',
        'inicio_carreira': date(1986, 1, 1),
        'fim_carreira': date(2006, 1, 1),
        'altura': '1,83 m',
        'perna': 'Destro',
        'outras_posicoes': 'Meia-atacante, Ponta-direita',
        'titulos_champions': 0,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': format_html("""
            <p>Dennis Nicolaas Maria Bergkamp é considerado um dos jogadores mais elegantes e técnicos da história do futebol. Conhecido como "O Holandês Não-Voador" por sua fobia de aviões, foi uma lenda do Arsenal e da seleção holandesa.</p>
            <h3>Ajax (1986-1993)</h3>
            <p>No Ajax, Bergkamp se destacou como um dos maiores talentos do futebol holandês, conquistando a Liga dos Campeões de 1992 e a Copa da UEFA de 1992.</p>
            <h3>Arsenal (1995-2006)</h3>
            <p>No Arsenal, Bergkamp se tornou uma lenda, conquistando 3 títulos da Premier League e 4 FA Cups. É considerado um dos maiores jogadores da história do clube londrino.</p>
            <h3>Seleção Holandesa</h3>
            <p>Pela seleção holandesa, Bergkamp marcou 37 gols em 79 jogos. Foi fundamental na conquista da Eurocopa de 1988 e participou de 3 Copas do Mundo.</p>
        """),
        'carreira': format_html("""
            <ul>
                <li><strong>Ajax (1986-1993):</strong> 239 jogos, 103 gols</li>
                <li><strong>Inter de Milão (1993-1995):</strong> 52 jogos, 11 gols</li>
                <li><strong>Arsenal (1995-2006):</strong> 423 jogos, 120 gols</li>
            </ul>
            <h4>Principais Títulos Coletivos:</h4>
            <ul>
                <li>1x UEFA Champions League</li>
                <li>1x Copa da UEFA</li>
                <li>3x Premier League</li>
                <li>4x FA Cup</li>
                <li>1x Eurocopa</li>
            </ul>
            <h4>Principais Títulos Individuais:</h4>
            <ul>
                <li>Jogador do Ano da PFA (1998)</li>
                <li>FIFA 100 (Lista dos 100 maiores jogadores vivos)</li>
            </ul>
        """)
    },
    'Andrey Arshavin': {
        'nacionalidade': 'Rússia',
        'inicio_carreira': date(2000, 1, 1),
        'fim_carreira': date(2018, 1, 1),
        'altura': '1,72 m',
        'perna': 'Ambidestro',
        'outras_posicoes': 'Meia-atacante, Ponta-esquerda',
        'titulos_champions': 0,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': format_html("""
            <p>Andrey Sergeyevich Arshavin é considerado um dos maiores jogadores russos de sua geração. Conhecido por sua técnica refinada e capacidade de criar jogadas, foi fundamental na campanha da Rússia na Eurocopa de 2008.</p>
            <h3>Zenit (2000-2009, 2012-2015)</h3>
            <p>No Zenit, Arshavin se tornou uma lenda, conquistando a Copa da UEFA de 2008 e sendo eleito o melhor jogador do torneio. É considerado um dos maiores ídolos da história do clube.</p>
            <h3>Arsenal (2009-2013)</h3>
            <p>No Arsenal, Arshavin demonstrou sua qualidade técnica, sendo fundamental em várias vitórias importantes do clube londrino.</p>
            <h3>Seleção Russa</h3>
            <p>Pela seleção russa, Arshavin foi fundamental na campanha que levou o time à semifinal da Eurocopa de 2008, sendo eleito o melhor jogador do torneio.</p>
        """),
        'carreira': format_html("""
            <ul>
                <li><strong>Zenit (2000-2009, 2012-2015):</strong> 340 jogos, 85 gols</li>
                <li><strong>Arsenal (2009-2013):</strong> 144 jogos, 31 gols</li>
                <li><strong>Kuban Krasnodar (2015-2016):</strong> Passagem</li>
                <li><strong>Kairat (2016-2018):</strong> Final da carreira</li>
            </ul>
            <h4>Principais Títulos Coletivos:</h4>
            <ul>
                <li>1x Copa da UEFA</li>
                <li>2x Campeonato Russo</li>
                <li>1x Copa da Rússia</li>
            </ul>
            <h4>Principais Títulos Individuais:</h4>
            <ul>
                <li>Melhor Jogador da Eurocopa (2008)</li>
                <li>Jogador do Ano na Rússia (2006, 2007, 2008)</li>
            </ul>
        """)
    },
    'Paolo Maldini': {
        'nacionalidade': 'Itália',
        'inicio_carreira': date(1984, 1, 1),
        'fim_carreira': date(2009, 1, 1),
        'altura': '1,87 m',
        'perna': 'Destro',
        'outras_posicoes': 'Zagueiro, Ala-esquerda',
        'titulos_champions': 5,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': format_html("""
            <p>Paolo Cesare Maldini é considerado um dos maiores zagueiros e laterais da história do futebol. Jogou toda sua carreira pelo Milan, tornando-se o maior símbolo de lealdade e excelência do clube.</p>
            <h3>Milan (1984-2009)</h3>
            <p>No Milan, Maldini jogou por 25 temporadas, conquistando 5 Ligas dos Campeões, 7 títulos da Serie A e inúmeros outros troféus. É o jogador com mais partidas na história do clube (902 jogos).</p>
            <h3>Seleção Italiana</h3>
            <p>Pela seleção italiana, Maldini é o jogador com mais partidas da história (126 jogos). Participou de 4 Copas do Mundo e 3 Eurocopas, sendo capitão em várias delas.</p>
            <h3>Legado</h3>
            <p>Maldini é considerado um dos maiores defensores de todos os tempos, conhecido por sua elegância, inteligência tática e liderança. Sua camisa número 3 foi aposentada pelo Milan.</p>
        """),
        'carreira': format_html("""
            <ul>
                <li><strong>Milan (1984-2009):</strong> 902 jogos, 33 gols</li>
            </ul>
            <h4>Principais Títulos Coletivos:</h4>
            <ul>
                <li>5x UEFA Champions League</li>
                <li>7x Serie A</li>
                <li>1x Copa da Itália</li>
                <li>5x Supercopa da Itália</li>
            </ul>
            <h4>Principais Títulos Individuais:</h4>
            <ul>
                <li>FIFA 100 (Lista dos 100 maiores jogadores vivos)</li>
                <li>Melhor Zagueiro do Mundo (várias vezes)</li>
                <li>Jogador com mais partidas na história do Milan</li>
            </ul>
        """)
    },
    'Fernando Hierro': {
        'nacionalidade': 'Espanha',
        'inicio_carreira': date(1987, 1, 1),
        'fim_carreira': date(2005, 1, 1),
        'altura': '1,88 m',
        'perna': 'Destro',
        'outras_posicoes': 'Zagueiro, Volante',
        'titulos_champions': 3,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': format_html("""
            <p>Fernando Ruiz Hierro é considerado um dos maiores zagueiros da história do Real Madrid e do futebol espanhol. Conhecido por sua liderança, qualidade técnica e capacidade de marcar gols, foi fundamental nas conquistas do clube merengue.</p>
            <h3>Real Madrid (1989-2003)</h3>
            <p>No Real Madrid, Hierro se tornou uma lenda, conquistando 3 Ligas dos Campeões e 5 títulos da La Liga. É o zagueiro com mais gols na história do clube (127 gols).</p>
            <h3>Seleção Espanhola</h3>
            <p>Pela seleção espanhola, Hierro foi capitão e participou de 3 Copas do Mundo e 2 Eurocopas. É o terceiro jogador com mais partidas na história da seleção (89 jogos).</p>
        """),
        'carreira': format_html("""
            <ul>
                <li><strong>Valladolid (1987-1989):</strong> Início</li>
                <li><strong>Real Madrid (1989-2003):</strong> 601 jogos, 127 gols</li>
                <li><strong>Al-Rayyan (2003-2004):</strong> Passagem no Catar</li>
                <li><strong>Bolton Wanderers (2004-2005):</strong> Final da carreira</li>
            </ul>
            <h4>Principais Títulos Coletivos:</h4>
            <ul>
                <li>3x UEFA Champions League</li>
                <li>5x La Liga</li>
                <li>1x Copa do Rei</li>
            </ul>
            <h4>Principais Títulos Individuais:</h4>
            <ul>
                <li>FIFA 100 (Lista dos 100 maiores jogadores vivos)</li>
                <li>Zagueiro com mais gols na história do Real Madrid</li>
            </ul>
        """)
    },
    'Jaap Stam': {
        'nacionalidade': 'Holanda',
        'inicio_carreira': date(1992, 1, 1),
        'fim_carreira': date(2007, 1, 1),
        'altura': '1,91 m',
        'perna': 'Destro',
        'outras_posicoes': 'Zagueiro',
        'titulos_champions': 1,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': format_html("""
            <p>Jakob "Jaap" Stam é considerado um dos maiores zagueiros da história do futebol holandês. Conhecido por sua força física, marcação sólida e liderança, foi fundamental nas conquistas do Manchester United e Milan.</p>
            <h3>Manchester United (1998-2001)</h3>
            <p>No Manchester United, Stam se tornou uma lenda, conquistando a Liga dos Campeões de 1999 e 3 títulos da Premier League. Formou uma das melhores defesas da história do clube.</p>
            <h3>Milan (2004-2006)</h3>
            <p>No Milan, Stam continuou a demonstrar sua qualidade, sendo fundamental na defesa do clube italiano.</p>
            <h3>Seleção Holandesa</h3>
            <p>Pela seleção holandesa, Stam participou de 2 Eurocopas e foi fundamental na defesa do time laranja.</p>
        """),
        'carreira': format_html("""
            <ul>
                <li><strong>Zwolle (1992-1993):</strong> Início</li>
                <li><strong>Cambuur (1993-1995):</strong> Passagem</li>
                <li><strong>Willem II (1995-1996):</strong> Consolidação</li>
                <li><strong>PSV (1996-1998):</strong> Melhor fase na Holanda</li>
                <li><strong>Manchester United (1998-2001):</strong> 127 jogos, 1 gol</li>
                <li><strong>Lazio (2001-2004):</strong> Passagem</li>
                <li><strong>Milan (2004-2006):</strong> 63 jogos, 2 gols</li>
                <li><strong>Ajax (2006-2007):</strong> Final da carreira</li>
            </ul>
            <h4>Principais Títulos Coletivos:</h4>
            <ul>
                <li>1x UEFA Champions League</li>
                <li>3x Premier League</li>
                <li>1x Serie A</li>
                <li>1x Eredivisie</li>
            </ul>
        """)
    },
    'Frank de Boer': {
        'nacionalidade': 'Holanda',
        'inicio_carreira': date(1988, 1, 1),
        'fim_carreira': date(2006, 1, 1),
        'altura': '1,80 m',
        'perna': 'Canhoto',
        'outras_posicoes': 'Zagueiro, Ala-esquerda',
        'titulos_champions': 1,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': format_html("""
            <p>Franciscus "Frank" de Boer é considerado um dos maiores zagueiros da história do Ajax e do futebol holandês. Conhecido por sua qualidade técnica, passes precisos e liderança, foi fundamental nas conquistas do clube holandês.</p>
            <h3>Ajax (1988-1999)</h3>
            <p>No Ajax, de Boer se tornou uma lenda, conquistando a Liga dos Campeões de 1995 e 5 títulos do Campeonato Holandês. Formou uma das melhores defesas da história do clube ao lado de seu irmão gêmeo Ronald.</p>
            <h3>Seleção Holandesa</h3>
            <p>Pela seleção holandesa, de Boer é o jogador com mais partidas da história (112 jogos). Participou de 3 Copas do Mundo e 3 Eurocopas.</p>
        """),
        'carreira': format_html("""
            <ul>
                <li><strong>Ajax (1988-1999):</strong> 328 jogos, 30 gols</li>
                <li><strong>Barcelona (1999-2003):</strong> 144 jogos, 5 gols</li>
                <li><strong>Galatasaray (2003-2004):</strong> Passagem</li>
                <li><strong>Rangers (2004):</strong> Passagem</li>
                <li><strong>Al-Rayyan (2004-2005):</strong> Passagem</li>
                <li><strong>Al-Shamal (2005-2006):</strong> Final da carreira</li>
            </ul>
            <h4>Principais Títulos Coletivos:</h4>
            <ul>
                <li>1x UEFA Champions League</li>
                <li>5x Eredivisie</li>
                <li>1x La Liga</li>
            </ul>
        """)
    },
    'Javier Zanetti': {
        'nacionalidade': 'Argentina',
        'inicio_carreira': date(1992, 1, 1),
        'fim_carreira': date(2014, 1, 1),
        'altura': '1,78 m',
        'perna': 'Destro',
        'outras_posicoes': 'Ala-direita, Volante',
        'titulos_champions': 1,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': format_html("""
            <p>Javier Adelmar Zanetti é considerado um dos maiores laterais e volantes da história do futebol. Jogou 19 temporadas pela Inter de Milão, tornando-se o maior símbolo de lealdade e excelência do clube.</p>
            <h3>Inter de Milão (1995-2014)</h3>
            <p>Na Inter, Zanetti se tornou uma lenda, conquistando a Liga dos Campeões de 2010 e 5 títulos da Serie A. É o jogador com mais partidas na história do clube (858 jogos) e foi capitão por mais de uma década.</p>
            <h3>Seleção Argentina</h3>
            <p>Pela seleção argentina, Zanetti é o segundo jogador com mais partidas da história (143 jogos). Participou de 2 Copas do Mundo e 4 Copas América.</p>
            <h3>Legado</h3>
            <p>Zanetti é considerado um dos maiores laterais de todos os tempos, conhecido por sua resistência física, versatilidade e liderança. Sua camisa número 4 foi aposentada pela Inter de Milão.</p>
        """),
        'carreira': format_html("""
            <ul>
                <li><strong>Talleres (1992-1993):</strong> Início</li>
                <li><strong>Banfield (1993-1995):</strong> Consolidação</li>
                <li><strong>Inter de Milão (1995-2014):</strong> 858 jogos, 21 gols</li>
            </ul>
            <h4>Principais Títulos Coletivos:</h4>
            <ul>
                <li>1x UEFA Champions League</li>
                <li>5x Serie A</li>
                <li>4x Copa da Itália</li>
                <li>1x Mundial de Clubes da FIFA</li>
            </ul>
            <h4>Principais Títulos Individuais:</h4>
            <ul>
                <li>Jogador com mais partidas na história da Inter de Milão</li>
                <li>FIFA 100 (Lista dos 100 maiores jogadores vivos)</li>
            </ul>
        """)
    },
    'Aldair': {
        'nacionalidade': 'Brasil',
        'inicio_carreira': date(1985, 1, 1),
        'fim_carreira': date(2009, 1, 1),
        'altura': '1,83 m',
        'perna': 'Destro',
        'outras_posicoes': 'Zagueiro',
        'titulos_champions': 0,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': format_html("""
            <p>Aldair Nascimento dos Santos é considerado um dos maiores zagueiros brasileiros de todos os tempos. Conhecido por sua elegância, qualidade técnica e liderança, foi fundamental nas conquistas da seleção brasileira e da Roma.</p>
            <h3>Roma (1990-2003)</h3>
            <p>Na Roma, Aldair se tornou uma lenda, conquistando o título da Serie A de 2001 e sendo fundamental na defesa do clube por 13 temporadas. É considerado um dos maiores zagueiros da história do clube.</p>
            <h3>Seleção Brasileira</h3>
            <p>Pela seleção brasileira, Aldair foi fundamental na conquista da Copa do Mundo de 1994, formando uma das melhores defesas da história do Brasil ao lado de Márcio Santos.</p>
        """),
        'carreira': format_html("""
            <ul>
                <li><strong>Fluminense (1985-1989):</strong> Início</li>
                <li><strong>Benfica (1989-1990):</strong> Passagem</li>
                <li><strong>Roma (1990-2003):</strong> 415 jogos, 20 gols</li>
                <li><strong>Genoa (2003-2004):</strong> Passagem</li>
                <li><strong>Roma (2004-2005):</strong> Retorno</li>
                <li><strong>Rio Branco (2007-2009):</strong> Final da carreira</li>
            </ul>
            <h4>Principais Títulos Coletivos:</h4>
            <ul>
                <li>1x Copa do Mundo</li>
                <li>1x Serie A</li>
                <li>1x Copa da Itália</li>
            </ul>
        """)
    },
    'Matthias Sammer': {
        'nacionalidade': 'Alemanha',
        'inicio_carreira': date(1985, 1, 1),
        'fim_carreira': date(1998, 1, 1),
        'altura': '1,81 m',
        'perna': 'Destro',
        'outras_posicoes': 'Zagueiro, Volante',
        'titulos_champions': 1,
        'bola_de_ouro': 1,
        'mundial_clubes': 0,
        'biografia': format_html("""
            <p>Matthias Sammer é considerado um dos maiores zagueiros e volantes da história do futebol alemão. Vencedor da Bola de Ouro em 1996, foi fundamental nas conquistas do Borussia Dortmund e da seleção alemã.</p>
            <h3>Borussia Dortmund (1993-1998)</h3>
            <p>No Borussia Dortmund, Sammer se tornou uma lenda, conquistando a Liga dos Campeões de 1997 e 2 títulos do Campeonato Alemão. Foi eleito o melhor jogador da Europa em 1996.</p>
            <h3>Seleção Alemã</h3>
            <p>Pela seleção alemã, Sammer foi fundamental na conquista da Eurocopa de 1996, sendo eleito o melhor jogador do torneio.</p>
        """),
        'carreira': format_html("""
            <ul>
                <li><strong>Dynamo Dresden (1985-1990):</strong> Início</li>
                <li><strong>VfB Stuttgart (1990-1992):</strong> Passagem</li>
                <li><strong>Inter de Milão (1992-1993):</strong> Passagem</li>
                <li><strong>Borussia Dortmund (1993-1998):</strong> 153 jogos, 21 gols</li>
            </ul>
            <h4>Principais Títulos Coletivos:</h4>
            <ul>
                <li>1x UEFA Champions League</li>
                <li>2x Bundesliga</li>
                <li>1x Eurocopa</li>
            </ul>
            <h4>Principais Títulos Individuais:</h4>
            <ul>
                <li>1x Bola de Ouro da FIFA</li>
                <li>Melhor Jogador da Eurocopa (1996)</li>
            </ul>
        """)
    },
    'Cafú': {
        'nacionalidade': 'Brasil',
        'inicio_carreira': date(1989, 1, 1),
        'fim_carreira': date(2008, 1, 1),
        'altura': '1,76 m',
        'perna': 'Destro',
        'outras_posicoes': 'Ala-direita',
        'titulos_champions': 1,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': format_html("""
            <p>Marcos Evangelista de Moraes, o Cafú, é considerado um dos maiores laterais-direitos da história do futebol. Conhecido por sua velocidade, resistência física e capacidade ofensiva, foi fundamental nas conquistas da seleção brasileira e do Milan.</p>
            <h3>Milan (2003-2008)</h3>
            <p>No Milan, Cafú se tornou uma lenda, conquistando a Liga dos Campeões de 2007 e 1 título da Serie A. Formou uma das melhores laterais da história ao lado de Paolo Maldini.</p>
            <h3>Seleção Brasileira</h3>
            <p>Pela seleção brasileira, Cafú é o jogador com mais partidas da história (142 jogos). Foi capitão na conquista da Copa do Mundo de 2002 e participou de 4 Copas do Mundo consecutivas.</p>
            <h3>Legado</h3>
            <p>Cafú é considerado um dos maiores laterais de todos os tempos, conhecido por sua longevidade e consistência em alto nível por mais de duas décadas.</p>
        """),
        'carreira': format_html("""
            <ul>
                <li><strong>São Paulo (1989-1994):</strong> Início e consolidação</li>
                <li><strong>Real Zaragoza (1994-1995):</strong> Passagem</li>
                <li><strong>Palmeiras (1995):</strong> Retorno ao Brasil</li>
                <li><strong>Roma (1997-2003):</strong> 163 jogos, 5 gols</li>
                <li><strong>Milan (2003-2008):</strong> 119 jogos, 4 gols</li>
            </ul>
            <h4>Principais Títulos Coletivos:</h4>
            <ul>
                <li>1x UEFA Champions League</li>
                <li>2x Copa do Mundo</li>
                <li>2x Copa América</li>
                <li>1x Serie A</li>
            </ul>
            <h4>Principais Títulos Individuais:</h4>
            <ul>
                <li>FIFA 100 (Lista dos 100 maiores jogadores vivos)</li>
                <li>Jogador com mais partidas na história da seleção brasileira</li>
            </ul>
        """)
    },
    'Jürgen Klinsmann': {
        'nacionalidade': 'Alemanha',
        'inicio_carreira': date(1981, 1, 1),
        'fim_carreira': date(1998, 1, 1),
        'altura': '1,81 m',
        'perna': 'Destro',
        'outras_posicoes': 'Ponta-direita',
        'titulos_champions': 0,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': format_html("""
            <p>Jürgen Klinsmann é considerado um dos maiores atacantes da história do futebol alemão. Conhecido por sua capacidade de finalização, movimentação e liderança, foi fundamental nas conquistas da seleção alemã.</p>
            <h3>Stuttgart, Inter de Milão, Monaco, Tottenham</h3>
            <p>Klinsmann jogou em vários clubes europeus, sempre demonstrando sua qualidade e capacidade de marcar gols. Foi artilheiro em várias ligas e conquistou títulos importantes.</p>
            <h3>Seleção Alemã</h3>
            <p>Pela seleção alemã, Klinsmann foi fundamental na conquista da Copa do Mundo de 1990 e da Eurocopa de 1996. É o terceiro maior artilheiro da história da seleção (47 gols).</p>
        """),
        'carreira': format_html("""
            <ul>
                <li><strong>Stuttgart (1984-1989):</strong> 156 jogos, 79 gols</li>
                <li><strong>Inter de Milão (1989-1992):</strong> 95 jogos, 34 gols</li>
                <li><strong>Monaco (1992-1994):</strong> 65 jogos, 29 gols</li>
                <li><strong>Tottenham (1994-1995, 1997-1998):</strong> 69 jogos, 38 gols</li>
                <li><strong>Bayern Munich (1995-1997):</strong> 65 jogos, 31 gols</li>
            </ul>
            <h4>Principais Títulos Coletivos:</h4>
            <ul>
                <li>1x Copa do Mundo</li>
                <li>1x Eurocopa</li>
                <li>1x Copa da UEFA</li>
            </ul>
            <h4>Principais Títulos Individuais:</h4>
            <ul>
                <li>Artilheiro da Copa do Mundo (1990)</li>
                <li>FIFA 100 (Lista dos 100 maiores jogadores vivos)</li>
            </ul>
        """)
    },
    'Claudio López': {
        'nacionalidade': 'Argentina',
        'inicio_carreira': date(1992, 1, 1),
        'fim_carreira': date(2010, 1, 1),
        'altura': '1,78 m',
        'perna': 'Canhoto',
        'outras_posicoes': 'Ponta-esquerda, Meia-atacante',
        'titulos_champions': 0,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': format_html("""
            <p>Claudio Javier López é considerado um dos maiores atacantes argentinos de sua geração. Conhecido por sua velocidade, técnica e capacidade de finalização, foi fundamental em vários clubes europeus.</p>
            <h3>Valencia (1996-2000)</h3>
            <p>No Valencia, López se tornou uma lenda, sendo fundamental nas conquistas do clube espanhol e demonstrando sua qualidade em alto nível.</p>
            <h3>Lazio (2000-2004)</h3>
            <p>Na Lazio, López continuou a demonstrar sua qualidade, sendo fundamental no ataque do clube italiano.</p>
            <h3>Seleção Argentina</h3>
            <p>Pela seleção argentina, López participou da Copa do Mundo de 1998 e foi fundamental em várias campanhas importantes.</p>
        """),
        'carreira': format_html("""
            <ul>
                <li><strong>Racing Club (1992-1996):</strong> Início</li>
                <li><strong>Valencia (1996-2000):</strong> 127 jogos, 47 gols</li>
                <li><strong>Lazio (2000-2004):</strong> 106 jogos, 29 gols</li>
                <li><strong>América (2004-2006):</strong> Passagem no México</li>
                <li><strong>Racing Club (2007-2008):</strong> Retorno</li>
                <li><strong>Colorado Rapids (2008-2010):</strong> Final da carreira</li>
            </ul>
            <h4>Principais Títulos Coletivos:</h4>
            <ul>
                <li>1x Copa da UEFA</li>
                <li>1x Copa do Rei</li>
            </ul>
        """)
    },
    'Freddie Ljungberg': {
        'nacionalidade': 'Suécia',
        'inicio_carreira': date(1994, 1, 1),
        'fim_carreira': date(2014, 1, 1),
        'altura': '1,75 m',
        'perna': 'Destro',
        'outras_posicoes': 'Meia-esquerda, Ponta-esquerda',
        'titulos_champions': 0,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': format_html("""
            <p>Karl Fredrik "Freddie" Ljungberg é considerado um dos maiores jogadores suecos de sua geração. Conhecido por sua velocidade, técnica e capacidade de criar jogadas, foi fundamental nas conquistas do Arsenal.</p>
            <h3>Arsenal (1998-2007)</h3>
            <p>No Arsenal, Ljungberg se tornou uma lenda, conquistando 2 títulos da Premier League e 3 FA Cups. Foi fundamental no "Invincibles" de 2003-2004, time que não perdeu nenhum jogo na temporada.</p>
            <h3>Seleção Sueca</h3>
            <p>Pela seleção sueca, Ljungberg participou de 2 Copas do Mundo e 3 Eurocopas, sendo fundamental em várias campanhas importantes.</p>
        """),
        'carreira': format_html("""
            <ul>
                <li><strong>Halmstad (1994-1998):</strong> Início</li>
                <li><strong>Arsenal (1998-2007):</strong> 328 jogos, 72 gols</li>
                <li><strong>West Ham United (2007-2008):</strong> Passagem</li>
                <li><strong>Seattle Sounders (2008-2010):</strong> Passagem nos EUA</li>
                <li><strong>Chicago Fire (2010):</strong> Passagem</li>
                <li><strong>Celtic (2010-2011):</strong> Passagem</li>
                <li><strong>Shimizu S-Pulse (2011-2012):</strong> Passagem no Japão</li>
            </ul>
            <h4>Principais Títulos Coletivos:</h4>
            <ul>
                <li>2x Premier League</li>
                <li>3x FA Cup</li>
            </ul>
        """)
    },
    'Filippo Inzaghi': {
        'nacionalidade': 'Itália',
        'inicio_carreira': date(1991, 1, 1),
        'fim_carreira': date(2012, 1, 1),
        'altura': '1,81 m',
        'perna': 'Destro',
        'outras_posicoes': 'Centroavante',
        'titulos_champions': 2,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': format_html("""
            <p>Filippo Inzaghi é considerado um dos maiores atacantes da história do futebol italiano. Conhecido por sua capacidade de finalização, movimentação dentro da área e "faro de gol", foi fundamental nas conquistas do Milan.</p>
            <h3>Milan (2001-2012)</h3>
            <p>No Milan, Inzaghi se tornou uma lenda, conquistando 2 Ligas dos Campeões e 2 títulos da Serie A. É o maior artilheiro da história da Liga dos Campeões pelo clube (46 gols).</p>
            <h3>Seleção Italiana</h3>
            <p>Pela seleção italiana, Inzaghi participou de 2 Copas do Mundo e foi fundamental em várias campanhas importantes.</p>
        """),
        'carreira': format_html("""
            <ul>
                <li><strong>Piacenza (1991-1995):</strong> Início</li>
                <li><strong>Parma (1995-1996):</strong> Passagem</li>
                <li><strong>Atalanta (1996-1997):</strong> Consolidação</li>
                <li><strong>Juventus (1997-2001):</strong> 165 jogos, 89 gols</li>
                <li><strong>Milan (2001-2012):</strong> 300 jogos, 126 gols</li>
            </ul>
            <h4>Principais Títulos Coletivos:</h4>
            <ul>
                <li>2x UEFA Champions League</li>
                <li>2x Serie A</li>
                <li>1x Copa do Mundo</li>
            </ul>
            <h4>Principais Títulos Individuais:</h4>
            <ul>
                <li>Artilheiro da Serie A (1997)</li>
                <li>Maior artilheiro da história da Liga dos Campeões pelo Milan</li>
            </ul>
        """)
    },
    'Raúl González': {
        'nacionalidade': 'Espanha',
        'inicio_carreira': date(1994, 1, 1),
        'fim_carreira': date(2015, 1, 1),
        'altura': '1,80 m',
        'perna': 'Destro',
        'outras_posicoes': 'Meia-atacante, Ponta-esquerda',
        'titulos_champions': 3,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': format_html("""
            <p>Raúl González Blanco é considerado um dos maiores atacantes da história do Real Madrid e do futebol espanhol. Conhecido como "El 7", foi uma lenda do clube merengue por 16 temporadas.</p>
            <h3>Real Madrid (1994-2010)</h3>
            <p>No Real Madrid, Raúl se tornou uma lenda, conquistando 3 Ligas dos Campeões e 6 títulos da La Liga. É o segundo maior artilheiro da história do clube (323 gols) e o maior artilheiro da história da Liga dos Campeões (71 gols).</p>
            <h3>Seleção Espanhola</h3>
            <p>Pela seleção espanhola, Raúl é o maior artilheiro da história (44 gols) e participou de 3 Copas do Mundo e 2 Eurocopas.</p>
            <h3>Legado</h3>
            <p>Raúl é considerado um dos maiores atacantes de todos os tempos, conhecido por sua elegância, capacidade de finalização e liderança.</p>
        """),
        'carreira': format_html("""
            <ul>
                <li><strong>Real Madrid (1994-2010):</strong> 741 jogos, 323 gols</li>
                <li><strong>Schalke 04 (2010-2012):</strong> 98 jogos, 40 gols</li>
                <li><strong>Al-Sadd (2012-2014):</strong> Passagem no Catar</li>
                <li><strong>New York Cosmos (2014-2015):</strong> Final da carreira</li>
            </ul>
            <h4>Principais Títulos Coletivos:</h4>
            <ul>
                <li>3x UEFA Champions League</li>
                <li>6x La Liga</li>
                <li>4x Supercopa da Espanha</li>
            </ul>
            <h4>Principais Títulos Individuais:</h4>
            <ul>
                <li>Maior artilheiro da história da Liga dos Campeões (71 gols)</li>
                <li>Maior artilheiro da história da seleção espanhola</li>
                <li>FIFA 100 (Lista dos 100 maiores jogadores vivos)</li>
            </ul>
        """)
    },
    'Fernando Morientes': {
        'nacionalidade': 'Espanha',
        'inicio_carreira': date(1993, 1, 1),
        'fim_carreira': date(2010, 1, 1),
        'altura': '1,84 m',
        'perna': 'Destro',
        'outras_posicoes': 'Centroavante',
        'titulos_champions': 3,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': format_html("""
            <p>Fernando Morientes Sánchez é considerado um dos maiores atacantes da história do Real Madrid e do futebol espanhol. Conhecido por sua capacidade de finalização e jogo aéreo, foi fundamental nas conquistas do clube merengue.</p>
            <h3>Real Madrid (1997-2005)</h3>
            <p>No Real Madrid, Morientes se tornou uma lenda, conquistando 3 Ligas dos Campeões e 2 títulos da La Liga. Formou uma das melhores duplas de ataque da história ao lado de Raúl.</p>
            <h3>Seleção Espanhola</h3>
            <p>Pela seleção espanhola, Morientes participou de 2 Copas do Mundo e 2 Eurocopas, sendo fundamental em várias campanhas importantes.</p>
        """),
        'carreira': format_html("""
            <ul>
                <li><strong>Albacete (1993-1995):</strong> Início</li>
                <li><strong>Real Zaragoza (1995-1997):</strong> Consolidação</li>
                <li><strong>Real Madrid (1997-2005):</strong> 272 jogos, 100 gols</li>
                <li><strong>Monaco (2003-2004):</strong> Empréstimo</li>
                <li><strong>Liverpool (2005-2006):</strong> Passagem</li>
                <li><strong>Valencia (2006-2009):</strong> Passagem</li>
                <li><strong>Marseille (2009-2010):</strong> Final da carreira</li>
            </ul>
            <h4>Principais Títulos Coletivos:</h4>
            <ul>
                <li>3x UEFA Champions League</li>
                <li>2x La Liga</li>
            </ul>
        """)
    },
    'Ruud van Nistelrooy': {
        'nacionalidade': 'Holanda',
        'inicio_carreira': date(1993, 1, 1),
        'fim_carreira': date(2012, 1, 1),
        'altura': '1,88 m',
        'perna': 'Destro',
        'outras_posicoes': 'Centroavante',
        'titulos_champions': 0,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': format_html("""
            <p>Rutgerus Johannes Martinus "Ruud" van Nistelrooy é considerado um dos maiores atacantes da história do futebol holandês. Conhecido por sua capacidade de finalização, movimentação e "faro de gol", foi fundamental nas conquistas do Manchester United e Real Madrid.</p>
            <h3>Manchester United (2001-2006)</h3>
            <p>No Manchester United, van Nistelrooy se tornou uma lenda, conquistando 1 título da Premier League e sendo o maior artilheiro da história da Liga dos Campeões pelo clube (38 gols).</p>
            <h3>Real Madrid (2006-2010)</h3>
            <p>No Real Madrid, van Nistelrooy continuou a demonstrar sua qualidade, conquistando 2 títulos da La Liga e sendo fundamental no ataque do clube.</p>
            <h3>Seleção Holandesa</h3>
            <p>Pela seleção holandesa, van Nistelrooy é o segundo maior artilheiro da história (35 gols) e participou de 2 Copas do Mundo e 2 Eurocopas.</p>
        """),
        'carreira': format_html("""
            <ul>
                <li><strong>Den Bosch (1993-1997):</strong> Início</li>
                <li><strong>Heerenveen (1997-1998):</strong> Consolidação</li>
                <li><strong>PSV (1998-2001):</strong> 90 jogos, 77 gols</li>
                <li><strong>Manchester United (2001-2006):</strong> 219 jogos, 150 gols</li>
                <li><strong>Real Madrid (2006-2010):</strong> 96 jogos, 64 gols</li>
                <li><strong>Hamburg (2010-2011):</strong> Passagem</li>
                <li><strong>Málaga (2011-2012):</strong> Final da carreira</li>
            </ul>
            <h4>Principais Títulos Coletivos:</h4>
            <ul>
                <li>1x Premier League</li>
                <li>2x La Liga</li>
                <li>2x Eredivisie</li>
            </ul>
            <h4>Principais Títulos Individuais:</h4>
            <ul>
                <li>Artilheiro da Premier League (2003)</li>
                <li>Artilheiro da Liga dos Campeões (2002, 2003)</li>
            </ul>
        """)
    },
    'Patrick Kluivert': {
        'nacionalidade': 'Holanda',
        'inicio_carreira': date(1994, 1, 1),
        'fim_carreira': date(2008, 1, 1),
        'altura': '1,88 m',
        'perna': 'Destro',
        'outras_posicoes': 'Centroavante',
        'titulos_champions': 1,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': format_html("""
            <p>Patrick Stephan Kluivert é considerado um dos maiores atacantes da história do futebol holandês. Conhecido por sua capacidade de finalização, força física e técnica, foi fundamental nas conquistas do Ajax e Barcelona.</p>
            <h3>Ajax (1994-1997)</h3>
            <p>No Ajax, Kluivert se tornou uma lenda, conquistando a Liga dos Campeões de 1995 e sendo fundamental no ataque do clube holandês.</p>
            <h3>Barcelona (1998-2004)</h3>
            <p>No Barcelona, Kluivert continuou a demonstrar sua qualidade, conquistando 1 título da La Liga e sendo fundamental no ataque do clube catalão.</p>
            <h3>Seleção Holandesa</h3>
            <p>Pela seleção holandesa, Kluivert é o maior artilheiro da história (40 gols) e participou de 2 Copas do Mundo e 2 Eurocopas.</p>
        """),
        'carreira': format_html("""
            <ul>
                <li><strong>Ajax (1994-1997):</strong> 92 jogos, 52 gols</li>
                <li><strong>Milan (1997-1998):</strong> 27 jogos, 6 gols</li>
                <li><strong>Barcelona (1998-2004):</strong> 257 jogos, 123 gols</li>
                <li><strong>Newcastle United (2004-2005):</strong> Passagem</li>
                <li><strong>Valencia (2005-2006):</strong> Passagem</li>
                <li><strong>PSV (2006-2007):</strong> Passagem</li>
                <li><strong>Lille (2007-2008):</strong> Final da carreira</li>
            </ul>
            <h4>Principais Títulos Coletivos:</h4>
            <ul>
                <li>1x UEFA Champions League</li>
                <li>1x La Liga</li>
                <li>2x Eredivisie</li>
            </ul>
            <h4>Principais Títulos Individuais:</h4>
            <ul>
                <li>Maior artilheiro da história da seleção holandesa</li>
            </ul>
        """)
    },
    'Rui Costa': {
        'nacionalidade': 'Portugal',
        'inicio_carreira': date(1990, 1, 1),
        'fim_carreira': date(2008, 1, 1),
        'altura': '1,80 m',
        'perna': 'Destro',
        'outras_posicoes': 'Meia-atacante, Meia-central',
        'titulos_champions': 1,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': format_html("""
            <p>Rui Manuel César Costa é considerado um dos maiores meio-campistas da história do futebol português. Conhecido por sua elegância, visão de jogo e passes precisos, foi fundamental nas conquistas do Benfica, Fiorentina e Milan.</p>
            <h3>Fiorentina (1994-2001)</h3>
            <p>Na Fiorentina, Rui Costa se tornou uma lenda, sendo fundamental no meio-campo do clube italiano e formando uma das melhores duplas da história ao lado de Gabriel Batistuta.</p>
            <h3>Milan (2001-2006)</h3>
            <p>No Milan, Rui Costa continuou a demonstrar sua qualidade, conquistando a Liga dos Campeões de 2003 e 1 título da Serie A.</p>
            <h3>Seleção Portuguesa</h3>
            <p>Pela seleção portuguesa, Rui Costa participou de 3 Eurocopas e foi fundamental em várias campanhas importantes.</p>
        """),
        'carreira': format_html("""
            <ul>
                <li><strong>Benfica (1990-1994):</strong> Início</li>
                <li><strong>Fiorentina (1994-2001):</strong> 276 jogos, 38 gols</li>
                <li><strong>Milan (2001-2006):</strong> 192 jogos, 11 gols</li>
                <li><strong>Benfica (2006-2008):</strong> Final da carreira</li>
            </ul>
            <h4>Principais Títulos Coletivos:</h4>
            <ul>
                <li>1x UEFA Champions League</li>
                <li>1x Serie A</li>
                <li>1x Campeonato Português</li>
            </ul>
        """)
    },
    'Michael Laudrup': {
        'nacionalidade': 'Dinamarca',
        'inicio_carreira': date(1981, 1, 1),
        'fim_carreira': date(1998, 1, 1),
        'altura': '1,83 m',
        'perna': 'Destro',
        'outras_posicoes': 'Meia-atacante, Ponta-direita',
        'titulos_champions': 1,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': format_html("""
            <p>Michael Laudrup é considerado um dos maiores jogadores da história do futebol dinamarquês. Conhecido por sua elegância, técnica refinada e visão de jogo, foi fundamental nas conquistas do Barcelona, Real Madrid e seleção dinamarquesa.</p>
            <h3>Barcelona (1989-1994)</h3>
            <p>No Barcelona, Laudrup se tornou uma lenda, conquistando a Liga dos Campeões de 1992 e 4 títulos da La Liga. Foi fundamental no "Dream Team" de Johan Cruyff.</p>
            <h3>Real Madrid (1994-1996)</h3>
            <p>No Real Madrid, Laudrup continuou a demonstrar sua qualidade, conquistando 1 título da La Liga e sendo fundamental no meio-campo do clube.</p>
            <h3>Seleção Dinamarquesa</h3>
            <p>Pela seleção dinamarquesa, Laudrup foi fundamental na conquista da Eurocopa de 1992, sendo considerado um dos melhores jogadores do torneio.</p>
        """),
        'carreira': format_html("""
            <ul>
                <li><strong>Brøndby (1981-1982):</strong> Início</li>
                <li><strong>Juventus (1982-1983):</strong> Empréstimo</li>
                <li><strong>Lazio (1983-1985):</strong> Passagem</li>
                <li><strong>Juventus (1985-1989):</strong> 151 jogos, 16 gols</li>
                <li><strong>Barcelona (1989-1994):</strong> 226 jogos, 54 gols</li>
                <li><strong>Real Madrid (1994-1996):</strong> 89 jogos, 12 gols</li>
                <li><strong>Vissel Kobe (1996-1997):</strong> Passagem no Japão</li>
                <li><strong>Ajax (1997-1998):</strong> Final da carreira</li>
            </ul>
            <h4>Principais Títulos Coletivos:</h4>
            <ul>
                <li>1x UEFA Champions League</li>
                <li>5x La Liga</li>
                <li>1x Serie A</li>
                <li>1x Eurocopa</li>
            </ul>
            <h4>Principais Títulos Individuais:</h4>
            <ul>
                <li>FIFA 100 (Lista dos 100 maiores jogadores vivos)</li>
            </ul>
        """)
    },
    'Jay-Jay Okocha': {
        'nacionalidade': 'Nigéria',
        'inicio_carreira': date(1990, 1, 1),
        'fim_carreira': date(2008, 1, 1),
        'altura': '1,73 m',
        'perna': 'Ambidestro',
        'outras_posicoes': 'Meia-atacante, Ponta-direita',
        'titulos_champions': 0,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': format_html("""
            <p>Augustine Azuka "Jay-Jay" Okocha é considerado um dos maiores jogadores africanos de todos os tempos. Conhecido por sua técnica extraordinária, dribles desconcertantes e criatividade, foi uma lenda do futebol nigeriano.</p>
            <h3>Paris Saint-Germain (1998-2002)</h3>
            <p>No PSG, Okocha se tornou uma lenda, demonstrando sua qualidade técnica e sendo fundamental no meio-campo do clube francês.</p>
            <h3>Bolton Wanderers (2002-2006)</h3>
            <p>No Bolton, Okocha continuou a demonstrar sua qualidade, sendo fundamental no meio-campo do clube inglês e conquistando a admiração dos torcedores.</p>
            <h3>Seleção Nigeriana</h3>
            <p>Pela seleção nigeriana, Okocha foi fundamental na conquista da Copa das Nações Africanas de 1994 e participou de 3 Copas do Mundo.</p>
        """),
        'carreira': format_html("""
            <ul>
                <li><strong>Enugu Rangers (1990-1991):</strong> Início</li>
                <li><strong>Borussia Neunkirchen (1991-1992):</strong> Passagem na Alemanha</li>
                <li><strong>Eintracht Frankfurt (1992-1996):</strong> 90 jogos, 18 gols</li>
                <li><strong>Fenerbahçe (1996-1998):</strong> 62 jogos, 30 gols</li>
                <li><strong>Paris Saint-Germain (1998-2002):</strong> 84 jogos, 12 gols</li>
                <li><strong>Bolton Wanderers (2002-2006):</strong> 145 jogos, 18 gols</li>
                <li><strong>Qatar SC (2006-2007):</strong> Passagem</li>
                <li><strong>Hull City (2007-2008):</strong> Final da carreira</li>
            </ul>
            <h4>Principais Títulos Coletivos:</h4>
            <ul>
                <li>1x Copa das Nações Africanas</li>
                <li>1x Copa da Turquia</li>
            </ul>
            <h4>Principais Títulos Individuais:</h4>
            <ul>
                <li>Jogador Africano do Ano (2003, 2004)</li>
            </ul>
        """)
    },
    'Lothar Matthäus': {
        'nacionalidade': 'Alemanha',
        'inicio_carreira': date(1979, 1, 1),
        'fim_carreira': date(2000, 1, 1),
        'altura': '1,74 m',
        'perna': 'Destro',
        'outras_posicoes': 'Volante, Meia-central',
        'titulos_champions': 0,
        'bola_de_ouro': 1,
        'mundial_clubes': 0,
        'biografia': format_html("""
            <p>Lothar Herbert Matthäus é considerado um dos maiores meio-campistas da história do futebol alemão. Vencedor da Bola de Ouro em 1990, foi fundamental nas conquistas da seleção alemã e do Inter de Milão.</p>
            <h3>Inter de Milão (1988-1992)</h3>
            <p>No Inter de Milão, Matthäus se tornou uma lenda, conquistando 1 título da Serie A e sendo eleito o melhor jogador do mundo em 1990.</p>
            <h3>Bayern Munich (1984-1988, 1992-2000)</h3>
            <p>No Bayern Munich, Matthäus conquistou 7 títulos do Campeonato Alemão e foi fundamental no meio-campo do clube bávaro.</p>
            <h3>Seleção Alemã</h3>
            <p>Pela seleção alemã, Matthäus é o jogador com mais partidas da história (150 jogos) e foi fundamental na conquista da Copa do Mundo de 1990.</p>
        """),
        'carreira': format_html("""
            <ul>
                <li><strong>Borussia Mönchengladbach (1979-1984):</strong> Início</li>
                <li><strong>Bayern Munich (1984-1988):</strong> 162 jogos, 85 gols</li>
                <li><strong>Inter de Milão (1988-1992):</strong> 153 jogos, 53 gols</li>
                <li><strong>Bayern Munich (1992-2000):</strong> 189 jogos, 28 gols</li>
                <li><strong>MetroStars (2000):</strong> Final da carreira</li>
            </ul>
            <h4>Principais Títulos Coletivos:</h4>
            <ul>
                <li>1x Copa do Mundo</li>
                <li>1x Eurocopa</li>
                <li>7x Bundesliga</li>
                <li>1x Serie A</li>
            </ul>
            <h4>Principais Títulos Individuais:</h4>
            <ul>
                <li>1x Bola de Ouro da FIFA</li>
                <li>Jogador com mais partidas na história da seleção alemã</li>
                <li>FIFA 100 (Lista dos 100 maiores jogadores vivos)</li>
            </ul>
        """)
    },
    'Roy Keane': {
        'nacionalidade': 'Irlanda',
        'inicio_carreira': date(1989, 1, 1),
        'fim_carreira': date(2006, 1, 1),
        'altura': '1,80 m',
        'perna': 'Destro',
        'outras_posicoes': 'Volante, Meia-central',
        'titulos_champions': 1,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': format_html("""
            <p>Roy Maurice Keane é considerado um dos maiores volantes da história do futebol irlandês e inglês. Conhecido por sua agressividade, liderança feroz e qualidade técnica, foi fundamental nas conquistas do Manchester United.</p>
            <h3>Manchester United (1993-2005)</h3>
            <p>No Manchester United, Keane se tornou uma lenda, conquistando a Liga dos Campeões de 1999 e 7 títulos da Premier League. Foi capitão do clube por mais de uma década e é considerado um dos maiores líderes da história do futebol.</p>
            <h3>Seleção Irlandesa</h3>
            <p>Pela seleção irlandesa, Keane foi fundamental em várias campanhas importantes, sendo considerado um dos maiores jogadores da história do país.</p>
        """),
        'carreira': format_html("""
            <ul>
                <li><strong>Cobh Ramblers (1989-1990):</strong> Início</li>
                <li><strong>Nottingham Forest (1990-1993):</strong> Consolidação</li>
                <li><strong>Manchester United (1993-2005):</strong> 480 jogos, 51 gols</li>
                <li><strong>Celtic (2005-2006):</strong> Final da carreira</li>
            </ul>
            <h4>Principais Títulos Coletivos:</h4>
            <ul>
                <li>1x UEFA Champions League</li>
                <li>7x Premier League</li>
                <li>4x FA Cup</li>
            </ul>
            <h4>Principais Títulos Individuais:</h4>
            <ul>
                <li>Jogador do Ano da PFA (2000)</li>
                <li>FIFA 100 (Lista dos 100 maiores jogadores vivos)</li>
            </ul>
        """)
    },
    'Youri Djorkaeff': {
        'nacionalidade': 'França',
        'inicio_carreira': date(1984, 1, 1),
        'fim_carreira': date(2006, 1, 1),
        'altura': '1,79 m',
        'perna': 'Destro',
        'outras_posicoes': 'Meia-atacante, Ponta-esquerda',
        'titulos_champions': 0,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': format_html("""
            <p>Youri Raffi Djorkaeff é considerado um dos maiores meio-campistas da história do futebol francês. Conhecido por sua técnica refinada, visão de jogo e capacidade de criar jogadas, foi fundamental nas conquistas da seleção francesa.</p>
            <h3>Inter de Milão (1996-1999)</h3>
            <p>No Inter de Milão, Djorkaeff se destacou como um dos principais meio-campistas do clube italiano, demonstrando sua qualidade técnica.</p>
            <h3>Seleção Francesa</h3>
            <p>Pela seleção francesa, Djorkaeff foi fundamental na conquista da Copa do Mundo de 1998 e da Eurocopa de 2000, sendo um dos principais criadores de jogadas do time campeão.</p>
        """),
        'carreira': format_html("""
            <ul>
                <li><strong>Grenoble (1984-1989):</strong> Início</li>
                <li><strong>Strasbourg (1989-1990):</strong> Passagem</li>
                <li><strong>Monaco (1990-1995):</strong> Consolidação</li>
                <li><strong>Paris Saint-Germain (1995-1996):</strong> Passagem</li>
                <li><strong>Inter de Milão (1996-1999):</strong> 127 jogos, 30 gols</li>
                <li><strong>Kaiserslautern (1999-2002):</strong> Passagem</li>
                <li><strong>Bolton Wanderers (2002-2004):</strong> Passagem</li>
                <li><strong>Blackburn Rovers (2004-2005):</strong> Passagem</li>
                <li><strong>New York Red Bulls (2005-2006):</strong> Final da carreira</li>
            </ul>
            <h4>Principais Títulos Coletivos:</h4>
            <ul>
                <li>1x Copa do Mundo</li>
                <li>1x Eurocopa</li>
                <li>1x Ligue 1</li>
            </ul>
        """)
    },
    'Fernando Redondo': {
        'nacionalidade': 'Argentina',
        'inicio_carreira': date(1985, 1, 1),
        'fim_carreira': date(2004, 1, 1),
        'altura': '1,86 m',
        'perna': 'Destro',
        'outras_posicoes': 'Volante, Meia-central',
        'titulos_champions': 2,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': format_html("""
            <p>Fernando Carlos Redondo Neri é considerado um dos maiores volantes da história do futebol argentino. Conhecido por sua elegância, qualidade técnica e visão de jogo, foi fundamental nas conquistas do Real Madrid.</p>
            <h3>Real Madrid (1994-2000)</h3>
            <p>No Real Madrid, Redondo se tornou uma lenda, conquistando 2 Ligas dos Campeões e 2 títulos da La Liga. É considerado um dos maiores volantes da história do clube merengue.</p>
            <h3>Seleção Argentina</h3>
            <p>Pela seleção argentina, Redondo participou de 2 Copas do Mundo e foi fundamental em várias campanhas importantes.</p>
        """),
        'carreira': format_html("""
            <ul>
                <li><strong>Argentinos Juniors (1985-1990):</strong> Início</li>
                <li><strong>Tenerife (1990-1994):</strong> Consolidação</li>
                <li><strong>Real Madrid (1994-2000):</strong> 228 jogos, 4 gols</li>
                <li><strong>Milan (2000-2004):</strong> 16 jogos, 0 gols</li>
            </ul>
            <h4>Principais Títulos Coletivos:</h4>
            <ul>
                <li>2x UEFA Champions League</li>
                <li>2x La Liga</li>
                <li>1x Copa América</li>
            </ul>
        """)
    },
    'Juan Sebastián Verón': {
        'nacionalidade': 'Argentina',
        'inicio_carreira': date(1994, 1, 1),
        'fim_carreira': date(2014, 1, 1),
        'altura': '1,86 m',
        'perna': 'Destro',
        'outras_posicoes': 'Meia-central, Meia-atacante',
        'titulos_champions': 0,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': format_html("""
            <p>Juan Sebastián Verón é considerado um dos maiores meio-campistas da história do futebol argentino. Conhecido por sua visão de jogo, passes precisos e qualidade técnica, foi fundamental em vários clubes europeus.</p>
            <h3>Lazio (1999-2001)</h3>
            <p>Na Lazio, Verón se tornou uma lenda, conquistando 1 título da Serie A e sendo fundamental no meio-campo do clube italiano.</p>
            <h3>Manchester United (2001-2003)</h3>
            <p>No Manchester United, Verón demonstrou sua qualidade técnica, sendo fundamental no meio-campo do clube inglês.</p>
            <h3>Seleção Argentina</h3>
            <p>Pela seleção argentina, Verón participou de 2 Copas do Mundo e foi fundamental em várias campanhas importantes.</p>
        """),
        'carreira': format_html("""
            <ul>
                <li><strong>Estudiantes (1994-1996):</strong> Início</li>
                <li><strong>Boca Juniors (1996):</strong> Passagem</li>
                <li><strong>Sampdoria (1996-1998):</strong> Consolidação</li>
                <li><strong>Parma (1998-1999):</strong> Passagem</li>
                <li><strong>Lazio (1999-2001):</strong> 74 jogos, 11 gols</li>
                <li><strong>Manchester United (2001-2003):</strong> 82 jogos, 11 gols</li>
                <li><strong>Chelsea (2003-2004):</strong> Passagem</li>
                <li><strong>Inter de Milão (2004-2006):</strong> Passagem</li>
                <li><strong>Estudiantes (2006-2012, 2013-2014):</strong> Retorno e final</li>
            </ul>
            <h4>Principais Títulos Coletivos:</h4>
            <ul>
                <li>1x Serie A</li>
                <li>1x Copa da UEFA</li>
                <li>1x Copa Libertadores</li>
            </ul>
        """)
    },
    'Ole Gunnar Solskjær': {
        'nacionalidade': 'Noruega',
        'inicio_carreira': date(1990, 1, 1),
        'fim_carreira': date(2007, 1, 1),
        'altura': '1,78 m',
        'perna': 'Destro',
        'outras_posicoes': 'Centroavante, Ponta-direita',
        'titulos_champions': 1,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': format_html("""
            <p>Ole Gunnar Solskjær é considerado um dos maiores atacantes da história do futebol norueguês. Conhecido como "O Matador de Bebês" por sua capacidade de marcar gols decisivos, foi fundamental nas conquistas do Manchester United.</p>
            <h3>Manchester United (1996-2007)</h3>
            <p>No Manchester United, Solskjær se tornou uma lenda, conquistando a Liga dos Campeões de 1999 e 6 títulos da Premier League. Marcou o gol decisivo na final da Champions de 1999, garantindo o triplete histórico do clube.</p>
            <h3>Seleção Norueguesa</h3>
            <p>Pela seleção norueguesa, Solskjær é o maior artilheiro da história (23 gols) e participou da Copa do Mundo de 1998.</p>
        """),
        'carreira': format_html("""
            <ul>
                <li><strong>Clausenengen (1990-1995):</strong> Início</li>
                <li><strong>Molde (1995-1996):</strong> Consolidação</li>
                <li><strong>Manchester United (1996-2007):</strong> 366 jogos, 126 gols</li>
            </ul>
            <h4>Principais Títulos Coletivos:</h4>
            <ul>
                <li>1x UEFA Champions League</li>
                <li>6x Premier League</li>
                <li>2x FA Cup</li>
            </ul>
            <h4>Principais Títulos Individuais:</h4>
            <ul>
                <li>Maior artilheiro da história da seleção norueguesa</li>
            </ul>
        """)
    },
}

def preencher_dados():
    """Preenche os dados dos novos jogadores"""
    atualizados = 0
    nao_encontrados = 0
    
    print("📝 Iniciando preenchimento de dados dos novos jogadores...\n")
    
    for nome_jogador, dados in DADOS_COMPLETOS.items():
        # Buscar o jogador (case-insensitive)
        jogador = Jogador.objects.filter(nome__iexact=nome_jogador).first()
        
        if not jogador:
            print(f"⚠️  Jogador '{nome_jogador}' não encontrado no banco. Pulando...")
            nao_encontrados += 1
            continue
        
        # Atualizar todos os campos
        jogador.nacionalidade = dados.get('nacionalidade', jogador.nacionalidade)
        jogador.inicio_carreira = dados.get('inicio_carreira', jogador.inicio_carreira)
        jogador.fim_carreira = dados.get('fim_carreira', jogador.fim_carreira)
        jogador.altura = dados.get('altura', jogador.altura)
        jogador.perna = dados.get('perna', jogador.perna)
        jogador.outras_posicoes = dados.get('outras_posicoes', jogador.outras_posicoes)
        jogador.titulos_champions = dados.get('titulos_champions', jogador.titulos_champions)
        jogador.bola_de_ouro = dados.get('bola_de_ouro', jogador.bola_de_ouro)
        jogador.mundial_clubes = dados.get('mundial_clubes', jogador.mundial_clubes)
        jogador.biografia = dados.get('biografia', jogador.biografia)
        jogador.carreira = dados.get('carreira', jogador.carreira)
        
        jogador.save()
        
        print(f"✅ Dados de '{nome_jogador}' atualizados com sucesso!")
        atualizados += 1
    
    print("\n" + "="*60)
    print(f"📊 Resumo:")
    print(f"   ✅ Atualizados: {atualizados}")
    print(f"   ⚠️  Não encontrados: {nao_encontrados}")
    print("="*60)

if __name__ == "__main__":
    preencher_dados()
    print("\n✨ Processo concluído!")




