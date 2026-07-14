import os
import django
from datetime import date
from django.utils.html import format_html

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'futebol_historico.settings')
django.setup()

from blog.models import Jogador

# Dados completos de TODOS os jogadores
DADOS_COMPLETOS = {
    'David Beckham': {
        'nacionalidade': 'Inglaterra',
        'inicio_carreira': date(1992, 1, 1),
        'fim_carreira': date(2013, 1, 1),
        'altura': '1,83 m',
        'perna': 'Destro',
        'outras_posicoes': 'Meia-direita, Volante',
        'titulos_champions': 1,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': format_html("""
            <p>David Robert Joseph Beckham é um dos jogadores mais icônicos da história do futebol. Conhecido por seus passes precisos e cobranças de falta espetaculares, foi fundamental nas conquistas do Manchester United nos anos 90. Capitão da seleção inglesa, jogou também no Real Madrid, LA Galaxy, Milan e Paris Saint-Germain.</p>
            <h3>Manchester United (1992-2003)</h3>
            <p>Formado nas categorias de base do clube, Beckham se tornou uma lenda do United, conquistando seis títulos da Premier League, duas FA Cups e a Liga dos Campeões de 1999. Sua assistência para o gol de Solskjær na final da Champions é uma das mais lembradas da história.</p>
            <h3>Real Madrid (2003-2007)</h3>
            <p>Transferiu-se para o Real Madrid em 2003, onde conquistou a La Liga na última temporada. Formou parte do "Galácticos" ao lado de Zidane, Ronaldo e Figo.</p>
            <h3>Legado</h3>
            <p>Além de suas conquistas em campo, Beckham se tornou um ícone global, transcendendo o futebol e influenciando a cultura pop mundial.</p>
        """),
        'carreira': format_html("""
            <ul>
                <li><strong>Manchester United (1992-2003):</strong> 394 jogos, 85 gols</li>
                <li><strong>Real Madrid (2003-2007):</strong> 155 jogos, 20 gols</li>
                <li><strong>LA Galaxy (2007-2012):</strong> 118 jogos, 20 gols</li>
                <li><strong>Milan (2009, 2010):</strong> Empréstimos</li>
                <li><strong>Paris Saint-Germain (2013):</strong> 14 jogos, 0 gols</li>
            </ul>
            <h4>Principais Títulos Coletivos:</h4>
            <ul>
                <li>1x UEFA Champions League</li>
                <li>6x Premier League</li>
                <li>2x FA Cup</li>
                <li>1x La Liga</li>
                <li>1x Ligue 1</li>
            </ul>
            <h4>Principais Títulos Individuais:</h4>
            <ul>
                <li>Melhor Jogador Jovem da Premier League (1997)</li>
                <li>FIFA 100 (Lista dos 100 maiores jogadores vivos)</li>
            </ul>
        """)
    },
    'Lionel Messi': {
        'nacionalidade': 'Argentina',
        'inicio_carreira': date(2003, 1, 1),
        'fim_carreira': date(2024, 12, 31),
        'altura': '1,70 m',
        'perna': 'Canhoto',
        'outras_posicoes': 'Ponta-direita, Meia-atacante',
        'titulos_champions': 4,
        'bola_de_ouro': 8,
        'mundial_clubes': 3,
        'biografia': format_html("""
            <p>Lionel Andrés Messi Cuccittini é considerado por muitos o maior jogador de todos os tempos. Nascido em Rosário, Argentina, mudou-se para Barcelona aos 13 anos para tratar um problema de crescimento. Sua técnica extraordinária, visão de jogo e capacidade de decidir partidas o tornaram uma lenda viva do futebol.</p>
            <h3>Barcelona (2004-2021)</h3>
            <p>Messi passou 17 temporadas no Barcelona, tornando-se o maior artilheiro e o jogador com mais partidas da história do clube. Conquistou 10 títulos da La Liga, 7 Copas do Rei, 4 Ligas dos Campeões e 3 Mundiais de Clubes. Ganhou 6 Bolas de Ouro durante sua passagem pelo clube catalão.</p>
            <h3>Paris Saint-Germain (2021-2023)</h3>
            <p>Após deixar o Barcelona, Messi se transferiu para o PSG, onde conquistou 2 títulos da Ligue 1 e continuou a demonstrar seu futebol de alto nível.</p>
            <h3>Inter Miami (2023-presente)</h3>
            <p>Em 2023, Messi se transferiu para o Inter Miami, levando o futebol americano a novos patamares e conquistando a Leagues Cup em sua primeira temporada.</p>
            <h3>Seleção Argentina</h3>
            <p>Pela seleção argentina, Messi é o maior artilheiro e o jogador com mais partidas. Liderou a Argentina à conquista da Copa do Mundo de 2022, da Copa América de 2021 e da Finalíssima de 2022, consolidando seu legado como um dos maiores de todos os tempos.</p>
            <h3>Legado</h3>
            <p>Com 8 Bolas de Ouro, Messi detém o recorde de mais prêmios da história. Sua rivalidade com Cristiano Ronaldo marcou uma era no futebol mundial, e sua técnica refinada e humildade o tornaram um ícone global.</p>
        """),
        'carreira': format_html("""
            <ul>
                <li><strong>Barcelona (2004-2021):</strong> 778 jogos, 672 gols</li>
                <li><strong>Paris Saint-Germain (2021-2023):</strong> 75 jogos, 32 gols</li>
                <li><strong>Inter Miami (2023-presente):</strong> Em atividade</li>
            </ul>
            <h4>Principais Títulos Coletivos:</h4>
            <ul>
                <li>4x UEFA Champions League</li>
                <li>3x Mundial de Clubes da FIFA</li>
                <li>10x La Liga</li>
                <li>7x Copa do Rei</li>
                <li>2x Ligue 1</li>
                <li>1x Copa do Mundo</li>
                <li>1x Copa América</li>
                <li>1x Finalíssima</li>
            </ul>
            <h4>Principais Títulos Individuais:</h4>
            <ul>
                <li>8x Bola de Ouro da FIFA</li>
                <li>6x Chuteira de Ouro Europeia</li>
                <li>Melhor Jogador do Mundo pela FIFA (várias vezes)</li>
                <li>Artilheiro da UEFA Champions League (várias vezes)</li>
                <li>Artilheiro da La Liga (várias vezes)</li>
            </ul>
        """)
    },
    'Mesut Özil': {
        'nacionalidade': 'Alemanha',
        'inicio_carreira': date(2006, 1, 1),
        'fim_carreira': date(2023, 1, 1),
        'altura': '1,80 m',
        'perna': 'Ambidestro',
        'outras_posicoes': 'Meia-atacante, Ponta-esquerda',
        'titulos_champions': 0,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': format_html("""
            <p>Mesut Özil é um meio-campista alemão de origem turca, conhecido por sua visão de jogo excepcional e passes precisos. Foi fundamental na conquista da Copa do Mundo de 2014 pela Alemanha e se destacou no Real Madrid e Arsenal.</p>
            <h3>Schalke 04 e Werder Bremen</h3>
            <p>Iniciou sua carreira no Schalke 04 antes de se transferir para o Werder Bremen, onde se destacou e chamou a atenção dos grandes clubes europeus.</p>
            <h3>Real Madrid (2010-2013)</h3>
            <p>No Real Madrid, Özil se tornou um dos principais assistentes do mundo, fornecendo passes decisivos para Cristiano Ronaldo e outros atacantes. Conquistou a La Liga em 2012.</p>
            <h3>Arsenal (2013-2021)</h3>
            <p>No Arsenal, Özil se tornou uma peça fundamental do meio-campo, conquistando 4 FA Cups e se tornando um dos jogadores mais assistidos da Premier League.</p>
            <h3>Seleção Alemã</h3>
            <p>Pela seleção alemã, Özil foi fundamental na conquista da Copa do Mundo de 2014, sendo um dos principais criadores de jogadas do time campeão.</p>
        """),
        'carreira': format_html("""
            <ul>
                <li><strong>Schalke 04 (2006-2008):</strong> 39 jogos, 1 gol</li>
                <li><strong>Werder Bremen (2008-2010):</strong> 108 jogos, 16 gols</li>
                <li><strong>Real Madrid (2010-2013):</strong> 159 jogos, 27 gols</li>
                <li><strong>Arsenal (2013-2021):</strong> 254 jogos, 44 gols</li>
                <li><strong>Fenerbahçe (2021-2022):</strong> 37 jogos, 9 gols</li>
                <li><strong>İstanbul Başakşehir (2022-2023):</strong> 7 jogos, 0 gols</li>
            </ul>
            <h4>Principais Títulos Coletivos:</h4>
            <ul>
                <li>1x Copa do Mundo</li>
                <li>1x La Liga</li>
                <li>4x FA Cup</li>
                <li>1x Copa da Alemanha</li>
            </ul>
            <h4>Principais Títulos Individuais:</h4>
            <ul>
                <li>Melhor Assistente da Premier League (2015-2016)</li>
                <li>Jogador do Ano do Arsenal (2015-2016)</li>
            </ul>
        """)
    },
    'Pavel Nedved': {
        'nacionalidade': 'República Tcheca',
        'inicio_carreira': date(1991, 1, 1),
        'fim_carreira': date(2009, 1, 1),
        'altura': '1,77 m',
        'perna': 'Destro',
        'outras_posicoes': 'Meia-central, Ponta-esquerda',
        'titulos_champions': 0,
        'bola_de_ouro': 1,
        'mundial_clubes': 0,
        'biografia': format_html("""
            <p>Pavel Nedvěd foi um meio-campista completo, conhecido por sua incrível resistência física e qualidade técnica. Vencedor da Bola de Ouro em 2003, o tcheco se tornou uma lenda da Juventus, onde sua dedicação e habilidade o transformaram em um dos melhores jogadores da história do clube.</p>
            <h3>Lazio (1996-2001)</h3>
            <p>Na Lazio, Nedvěd se consolidou como um dos melhores meio-campistas da Europa, conquistando a Serie A e a Copa da Itália.</p>
            <h3>Juventus (2001-2009)</h3>
            <p>Na Juventus, Nedvěd se tornou uma lenda, conquistando múltiplos títulos da Serie A e sendo fundamental no meio-campo do clube. Sua dedicação e qualidade técnica o tornaram um dos maiores ídolos da história do clube turinês.</p>
            <h3>Seleção Tcheca</h3>
            <p>Pela seleção tcheca, Nedvěd foi fundamental na campanha que levou o time à final da Eurocopa de 1996, sendo eleito o melhor jogador do torneio.</p>
        """),
        'carreira': format_html("""
            <ul>
                <li><strong>Dukla Prague (1991-1992):</strong> 19 jogos, 3 gols</li>
                <li><strong>Sparta Prague (1992-1996):</strong> 97 jogos, 23 gols</li>
                <li><strong>Lazio (1996-2001):</strong> 178 jogos, 33 gols</li>
                <li><strong>Juventus (2001-2009):</strong> 327 jogos, 65 gols</li>
            </ul>
            <h4>Principais Títulos Coletivos:</h4>
            <ul>
                <li>3x Serie A</li>
                <li>1x Copa da Itália</li>
                <li>1x Supercopa da Itália</li>
            </ul>
            <h4>Principais Títulos Individuais:</h4>
            <ul>
                <li>1x Bola de Ouro da FIFA</li>
                <li>Melhor Jogador da Eurocopa (1996)</li>
            </ul>
        """)
    },
    'Roberto Carlos': {
        'nacionalidade': 'Brasil',
        'inicio_carreira': date(1991, 1, 1),
        'fim_carreira': date(2012, 1, 1),
        'altura': '1,68 m',
        'perna': 'Canhoto',
        'outras_posicoes': 'Ala-esquerda, Meia-esquerda',
        'titulos_champions': 3,
        'bola_de_ouro': 0,
        'mundial_clubes': 2,
        'biografia': format_html("""
            <p>Roberto Carlos da Silva é considerado um dos maiores laterais-esquerdos da história do futebol. Conhecido por sua velocidade, força física e chutes potentes, foi fundamental nas conquistas do Real Madrid e da seleção brasileira.</p>
            <h3>Real Madrid (1996-2007)</h3>
            <p>No Real Madrid, Roberto Carlos se tornou uma lenda, conquistando 4 Ligas dos Campeões e 4 títulos da La Liga. Seu chute de falta contra a França em 1997 é considerado um dos mais espetaculares da história.</p>
            <h3>Seleção Brasileira</h3>
            <p>Pela seleção brasileira, Roberto Carlos foi titular em três Copas do Mundo, conquistando o título em 2002. Formou uma das melhores laterais da história ao lado de Cafu.</p>
            <h3>Legado</h3>
            <p>Roberto Carlos revolucionou a posição de lateral-esquerdo, combinando defesa sólida com um poder ofensivo impressionante. Seus chutes de longa distância e sua velocidade o tornaram único.</p>
        """),
        'carreira': format_html("""
            <ul>
                <li><strong>União São João (1991-1993):</strong> Início</li>
                <li><strong>Palmeiras (1993-1995):</strong> Consolidação</li>
                <li><strong>Inter de Milão (1995-1996):</strong> Passagem</li>
                <li><strong>Real Madrid (1996-2007):</strong> 527 jogos, 70 gols</li>
                <li><strong>Fenerbahçe (2007-2009):</strong> 65 jogos, 6 gols</li>
                <li><strong>Corinthians (2009-2010):</strong> Retorno ao Brasil</li>
                <li><strong>Anzhi (2011-2012):</strong> Final da carreira</li>
            </ul>
            <h4>Principais Títulos Coletivos:</h4>
            <ul>
                <li>3x UEFA Champions League</li>
                <li>2x Mundial de Clubes da FIFA</li>
                <li>4x La Liga</li>
                <li>1x Copa do Mundo</li>
                <li>2x Copa América</li>
            </ul>
            <h4>Principais Títulos Individuais:</h4>
            <ul>
                <li>FIFA 100 (Lista dos 100 maiores jogadores vivos)</li>
                <li>Melhor Lateral do Mundo (várias vezes)</li>
            </ul>
        """)
    },
    'Samuel Eto\'o': {
        'nacionalidade': 'Camarões',
        'inicio_carreira': date(1997, 1, 1),
        'fim_carreira': date(2019, 1, 1),
        'altura': '1,80 m',
        'perna': 'Destro',
        'outras_posicoes': 'Ponta-direita',
        'titulos_champions': 3,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': format_html("""
            <p>Samuel Eto'o é considerado um dos maiores jogadores africanos de todos os tempos. Atacante veloz e com faro de gol, foi fundamental nas conquistas da Liga dos Campeões pelo Barcelona e Inter de Milão. Maior artilheiro da história da seleção de Camarões.</p>
            <h3>Barcelona (2004-2009)</h3>
            <p>No Barcelona, Eto'o se tornou uma lenda, conquistando 2 Ligas dos Campeões e 3 títulos da La Liga. Foi o artilheiro da Champions em 2006 e fundamental na conquista do triplete em 2009.</p>
            <h3>Inter de Milão (2009-2011)</h3>
            <p>Na Inter, Eto'o conquistou a Liga dos Campeões de 2010 e o triplete histórico sob o comando de José Mourinho, sendo fundamental com seus gols decisivos.</p>
            <h3>Seleção de Camarões</h3>
            <p>Pela seleção de Camarões, Eto'o é o maior artilheiro da história, com 56 gols. Conquistou 2 Copas das Nações Africanas e foi eleito o melhor jogador africano do ano 4 vezes.</p>
        """),
        'carreira': format_html("""
            <ul>
                <li><strong>Real Madrid (1997-2000):</strong> 7 jogos, 0 gols</li>
                <li><strong>Mallorca (2000-2004):</strong> 165 jogos, 70 gols</li>
                <li><strong>Barcelona (2004-2009):</strong> 199 jogos, 130 gols</li>
                <li><strong>Inter de Milão (2009-2011):</strong> 102 jogos, 53 gols</li>
                <li><strong>Anzhi (2011-2013):</strong> 71 jogos, 36 gols</li>
                <li><strong>Chelsea (2013-2014):</strong> 35 jogos, 12 gols</li>
                <li><strong>Everton (2014-2015):</strong> 20 jogos, 4 gols</li>
            </ul>
            <h4>Principais Títulos Coletivos:</h4>
            <ul>
                <li>3x UEFA Champions League</li>
                <li>3x La Liga</li>
                <li>1x Serie A</li>
                <li>2x Copa das Nações Africanas</li>
            </ul>
            <h4>Principais Títulos Individuais:</h4>
            <ul>
                <li>4x Melhor Jogador Africano do Ano</li>
                <li>Artilheiro da UEFA Champions League (2006)</li>
            </ul>
        """)
    },
    'Samuel Etoo': {
        'nacionalidade': 'Camarões',
        'inicio_carreira': date(1997, 1, 1),
        'fim_carreira': date(2019, 1, 1),
        'altura': '1,80 m',
        'perna': 'Destro',
        'outras_posicoes': 'Ponta-direita',
        'titulos_champions': 3,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': format_html("""
            <p>Samuel Eto'o é considerado um dos maiores jogadores africanos de todos os tempos. Atacante veloz e com faro de gol, foi fundamental nas conquistas da Liga dos Campeões pelo Barcelona e Inter de Milão. Maior artilheiro da história da seleção de Camarões.</p>
            <h3>Barcelona (2004-2009)</h3>
            <p>No Barcelona, Eto'o se tornou uma lenda, conquistando 2 Ligas dos Campeões e 3 títulos da La Liga. Foi o artilheiro da Champions em 2006 e fundamental na conquista do triplete em 2009.</p>
            <h3>Inter de Milão (2009-2011)</h3>
            <p>Na Inter, Eto'o conquistou a Liga dos Campeões de 2010 e o triplete histórico sob o comando de José Mourinho, sendo fundamental com seus gols decisivos.</p>
            <h3>Seleção de Camarões</h3>
            <p>Pela seleção de Camarões, Eto'o é o maior artilheiro da história, com 56 gols. Conquistou 2 Copas das Nações Africanas e foi eleito o melhor jogador africano do ano 4 vezes.</p>
        """),
        'carreira': format_html("""
            <ul>
                <li><strong>Real Madrid (1997-2000):</strong> 7 jogos, 0 gols</li>
                <li><strong>Mallorca (2000-2004):</strong> 165 jogos, 70 gols</li>
                <li><strong>Barcelona (2004-2009):</strong> 199 jogos, 130 gols</li>
                <li><strong>Inter de Milão (2009-2011):</strong> 102 jogos, 53 gols</li>
                <li><strong>Anzhi (2011-2013):</strong> 71 jogos, 36 gols</li>
                <li><strong>Chelsea (2013-2014):</strong> 35 jogos, 12 gols</li>
                <li><strong>Everton (2014-2015):</strong> 20 jogos, 4 gols</li>
            </ul>
            <h4>Principais Títulos Coletivos:</h4>
            <ul>
                <li>3x UEFA Champions League</li>
                <li>3x La Liga</li>
                <li>1x Serie A</li>
                <li>2x Copa das Nações Africanas</li>
            </ul>
            <h4>Principais Títulos Individuais:</h4>
            <ul>
                <li>4x Melhor Jogador Africano do Ano</li>
                <li>Artilheiro da UEFA Champions League (2006)</li>
            </ul>
        """)
    },
    'Wayne Rooney': {
        'nacionalidade': 'Inglaterra',
        'inicio_carreira': date(2002, 1, 1),
        'fim_carreira': date(2021, 1, 1),
        'altura': '1,76 m',
        'perna': 'Destro',
        'outras_posicoes': 'Meia-atacante, Ponta-direita',
        'titulos_champions': 1,
        'bola_de_ouro': 0,
        'mundial_clubes': 1,
        'biografia': format_html("""
            <p>Wayne Mark Rooney é o maior artilheiro da história do Manchester United e da seleção inglesa. Conhecido por sua força física, técnica e capacidade de decidir jogos, foi uma das principais estrelas do futebol inglês por mais de uma década.</p>
            <h3>Everton (2002-2004)</h3>
            <p>Rooney iniciou sua carreira no Everton, onde se destacou rapidamente e chamou a atenção dos grandes clubes europeus. Aos 16 anos, já demonstrava seu talento excepcional.</p>
            <h3>Manchester United (2004-2017)</h3>
            <p>No Manchester United, Rooney se tornou uma lenda, conquistando 5 títulos da Premier League, 1 Liga dos Campeões e 1 Mundial de Clubes. É o maior artilheiro da história do clube, com 253 gols.</p>
            <h3>Seleção Inglesa</h3>
            <p>Pela seleção inglesa, Rooney é o maior artilheiro da história, com 53 gols em 120 partidas. Participou de 3 Copas do Mundo e 3 Eurocopas.</p>
            <h3>Legado</h3>
            <p>Rooney é considerado um dos maiores jogadores ingleses de todos os tempos, conhecido por sua versatilidade, liderança e capacidade de marcar gols decisivos.</p>
        """),
        'carreira': format_html("""
            <ul>
                <li><strong>Everton (2002-2004):</strong> 77 jogos, 17 gols</li>
                <li><strong>Manchester United (2004-2017):</strong> 559 jogos, 253 gols</li>
                <li><strong>Everton (2017-2018):</strong> Retorno</li>
                <li><strong>DC United (2018-2020):</strong> 52 jogos, 25 gols</li>
                <li><strong>Derby County (2020-2021):</strong> Final da carreira</li>
            </ul>
            <h4>Principais Títulos Coletivos:</h4>
            <ul>
                <li>1x UEFA Champions League</li>
                <li>1x Mundial de Clubes da FIFA</li>
                <li>5x Premier League</li>
                <li>1x FA Cup</li>
                <li>3x Copa da Liga Inglesa</li>
            </ul>
            <h4>Principais Títulos Individuais:</h4>
            <ul>
                <li>Melhor Jogador Jovem da Premier League (2005)</li>
                <li>Artilheiro da Premier League (2009-2010)</li>
                <li>Maior Artilheiro da História do Manchester United</li>
                <li>Maior Artilheiro da História da Seleção Inglesa</li>
            </ul>
        """)
    },
    'Andrea Pirlo': {
        'nacionalidade': 'Itália',
        'inicio_carreira': date(1995, 1, 1),
        'fim_carreira': date(2017, 1, 1),
        'altura': '1,77 m',
        'perna': 'Destro',
        'outras_posicoes': 'Meia-central, Volante',
        'titulos_champions': 2,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': format_html("""
            <p>Andrea Pirlo é considerado um dos maiores meio-campistas da história do futebol. Conhecido por sua elegância em campo, visão de jogo excepcional e passes precisos, foi fundamental nas conquistas da Juventus, Milan e seleção italiana.</p>
            <h3>Milan (2001-2011)</h3>
            <p>No Milan, Pirlo se tornou uma lenda, conquistando 2 Ligas dos Campeões e 2 títulos da Serie A. Sua capacidade de criar jogadas e controlar o ritmo do jogo o tornou único.</p>
            <h3>Juventus (2011-2015)</h3>
            <p>Na Juventus, Pirlo continuou a demonstrar sua classe, conquistando 4 títulos consecutivos da Serie A e levando o clube à final da Liga dos Campeões de 2015.</p>
            <h3>Seleção Italiana</h3>
            <p>Pela seleção italiana, Pirlo foi fundamental na conquista da Copa do Mundo de 2006, sendo eleito o melhor jogador da final. Participou de 3 Copas do Mundo e 2 Eurocopas.</p>
            <h3>Legado</h3>
            <p>Pirlo é considerado um dos últimos grandes "registas" do futebol, um meio-campista que controlava o jogo com sua técnica e inteligência, não com velocidade ou força física.</p>
        """),
        'carreira': format_html("""
            <ul>
                <li><strong>Brescia (1995-1998, 2001):</strong> Início e retorno</li>
                <li><strong>Inter de Milão (1998-2001):</strong> Passagem</li>
                <li><strong>Milan (2001-2011):</strong> 401 jogos, 41 gols</li>
                <li><strong>Juventus (2011-2015):</strong> 164 jogos, 19 gols</li>
                <li><strong>New York City FC (2015-2017):</strong> Final da carreira</li>
            </ul>
            <h4>Principais Títulos Coletivos:</h4>
            <ul>
                <li>2x UEFA Champions League</li>
                <li>6x Serie A</li>
                <li>1x Copa do Mundo</li>
                <li>1x Copa da Itália</li>
            </ul>
            <h4>Principais Títulos Individuais:</h4>
            <ul>
                <li>Melhor Jogador da Final da Copa do Mundo (2006)</li>
                <li>FIFA 100 (Lista dos 100 maiores jogadores vivos)</li>
            </ul>
        """)
    },
    'Albert Ferrer': {
        'nacionalidade': 'Espanha',
        'inicio_carreira': date(1989, 1, 1),
        'fim_carreira': date(2003, 1, 1),
        'altura': '1,70 m',
        'perna': 'Destro',
        'outras_posicoes': 'Ala-direita',
        'titulos_champions': 1,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': format_html("""
            <p>Albert Ferrer i Llopis foi um lateral-direito espanhol que se destacou no Barcelona durante os anos 90. Conhecido por sua consistência defensiva e capacidade ofensiva, foi fundamental nas conquistas do "Dream Team" de Johan Cruyff.</p>
            <h3>Barcelona (1990-1998)</h3>
            <p>No Barcelona, Ferrer conquistou a Liga dos Campeões de 1992, 4 títulos da La Liga e 2 Copas do Rei. Foi parte do lendário "Dream Team" que revolucionou o futebol espanhol.</p>
            <h3>Seleção Espanhola</h3>
            <p>Pela seleção espanhola, Ferrer participou da Copa do Mundo de 1994 e da Eurocopa de 1996, sendo um dos principais laterais do time.</p>
        """),
        'carreira': format_html("""
            <ul>
                <li><strong>Barcelona B (1989-1990):</strong> Categorias de base</li>
                <li><strong>Barcelona (1990-1998):</strong> 204 jogos, 1 gol</li>
                <li><strong>Chelsea (1998-2003):</strong> 113 jogos, 1 gol</li>
            </ul>
            <h4>Principais Títulos Coletivos:</h4>
            <ul>
                <li>1x UEFA Champions League</li>
                <li>4x La Liga</li>
                <li>2x Copa do Rei</li>
                <li>1x FA Cup</li>
            </ul>
        """)
    },
    'Demetrio Albertini': {
        'nacionalidade': 'Itália',
        'inicio_carreira': date(1988, 1, 1),
        'fim_carreira': date(2005, 1, 1),
        'altura': '1,80 m',
        'perna': 'Destro',
        'outras_posicoes': 'Meia-central, Volante',
        'titulos_champions': 2,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': format_html("""
            <p>Demetrio Albertini foi um meio-campista italiano que se destacou no Milan durante os anos 90. Conhecido por sua visão de jogo e passes precisos, foi fundamental nas conquistas do clube rossonero.</p>
            <h3>Milan (1988-2002)</h3>
            <p>No Milan, Albertini conquistou 2 Ligas dos Campeões e 5 títulos da Serie A. Foi parte do lendário time do Milan que dominou o futebol europeu nos anos 90.</p>
            <h3>Seleção Italiana</h3>
            <p>Pela seleção italiana, Albertini participou de 3 Copas do Mundo e 2 Eurocopas, sendo um dos principais meio-campistas do time.</p>
        """),
        'carreira': format_html("""
            <ul>
                <li><strong>Milan (1988-2002):</strong> 406 jogos, 28 gols</li>
                <li><strong>Atalanta (2002-2003):</strong> Empréstimo</li>
                <li><strong>Lazio (2003-2004):</strong> Passagem</li>
                <li><strong>Atalanta (2004-2005):</strong> Final da carreira</li>
            </ul>
            <h4>Principais Títulos Coletivos:</h4>
            <ul>
                <li>2x UEFA Champions League</li>
                <li>5x Serie A</li>
                <li>1x Copa da Itália</li>
            </ul>
        """)
    },
    'Edwin van der Sar': {
        'nacionalidade': 'Holanda',
        'inicio_carreira': date(1990, 1, 1),
        'fim_carreira': date(2011, 1, 1),
        'altura': '1,97 m',
        'perna': 'Destro',
        'outras_posicoes': 'Goleiro',
        'titulos_champions': 2,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': format_html("""
            <p>Edwin van der Sar é considerado um dos maiores goleiros da história do futebol. Conhecido por sua segurança, reflexos e capacidade de jogar com os pés, foi fundamental nas conquistas do Ajax, Juventus e Manchester United.</p>
            <h3>Ajax (1990-1999)</h3>
            <p>No Ajax, van der Sar conquistou a Liga dos Campeões de 1995 e 4 títulos do Campeonato Holandês. Foi parte do lendário time que dominou o futebol europeu nos anos 90.</p>
            <h3>Manchester United (2005-2011)</h3>
            <p>No Manchester United, van der Sar conquistou a Liga dos Campeões de 2008 e 4 títulos da Premier League. Estabeleceu o recorde de mais tempo sem sofrer gols na Premier League (1.311 minutos).</p>
            <h3>Seleção Holandesa</h3>
            <p>Pela seleção holandesa, van der Sar é o jogador com mais partidas da história, com 130 jogos. Participou de 4 Copas do Mundo e 4 Eurocopas.</p>
        """),
        'carreira': format_html("""
            <ul>
                <li><strong>Ajax (1990-1999):</strong> 312 jogos</li>
                <li><strong>Juventus (1999-2001):</strong> 88 jogos</li>
                <li><strong>Fulham (2001-2005):</strong> 154 jogos</li>
                <li><strong>Manchester United (2005-2011):</strong> 266 jogos</li>
            </ul>
            <h4>Principais Títulos Coletivos:</h4>
            <ul>
                <li>2x UEFA Champions League</li>
                <li>4x Premier League</li>
                <li>4x Eredivisie</li>
            </ul>
            <h4>Principais Títulos Individuais:</h4>
            <ul>
                <li>Melhor Goleiro da UEFA (2009)</li>
                <li>Recorde de mais tempo sem sofrer gols na Premier League</li>
            </ul>
        """)
    },
    'Eric Cantona': {
        'nacionalidade': 'França',
        'inicio_carreira': date(1983, 1, 1),
        'fim_carreira': date(1997, 1, 1),
        'altura': '1,88 m',
        'perna': 'Destro',
        'outras_posicoes': 'Meia-atacante, Ponta-esquerda',
        'titulos_champions': 0,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': format_html("""
            <p>Eric Cantona é considerado um dos maiores ídolos da história do Manchester United. Conhecido por sua técnica refinada, personalidade forte e capacidade de decidir jogos, foi fundamental na transformação do clube inglês nos anos 90.</p>
            <h3>Manchester United (1992-1997)</h3>
            <p>No Manchester United, Cantona conquistou 4 títulos da Premier League e 2 FA Cups. Sua liderança e qualidade técnica foram fundamentais para o sucesso do clube, sendo considerado o "Rei" pelos torcedores.</p>
            <h3>Legado</h3>
            <p>Cantona é lembrado não apenas por suas conquistas, mas também por sua personalidade única e seu impacto cultural no futebol inglês. Sua gola alta e sua confiança o tornaram um ícone.</p>
        """),
        'carreira': format_html("""
            <ul>
                <li><strong>Auxerre (1983-1988):</strong> Início</li>
                <li><strong>Marseille (1988-1991):</strong> Passagem</li>
                <li><strong>Leeds United (1992):</strong> Passagem</li>
                <li><strong>Manchester United (1992-1997):</strong> 185 jogos, 82 gols</li>
            </ul>
            <h4>Principais Títulos Coletivos:</h4>
            <ul>
                <li>4x Premier League</li>
                <li>2x FA Cup</li>
            </ul>
            <h4>Principais Títulos Individuais:</h4>
            <ul>
                <li>Jogador do Ano da PFA (1994)</li>
                <li>FIFA 100 (Lista dos 100 maiores jogadores vivos)</li>
            </ul>
        """)
    },
    'Marcel Desailly': {
        'nacionalidade': 'França',
        'inicio_carreira': date(1986, 1, 1),
        'fim_carreira': date(2006, 1, 1),
        'altura': '1,85 m',
        'perna': 'Destro',
        'outras_posicoes': 'Volante, Zagueiro',
        'titulos_champions': 2,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': format_html("""
            <p>Marcel Desailly é considerado um dos maiores zagueiros da história do futebol. Conhecido por sua força física, marcação sólida e liderança, foi fundamental nas conquistas do Milan, Chelsea e seleção francesa.</p>
            <h3>Milan (1993-1998)</h3>
            <p>No Milan, Desailly conquistou 2 Ligas dos Campeões e 1 título da Serie A. Foi parte do lendário time que dominou o futebol europeu nos anos 90.</p>
            <h3>Chelsea (1998-2004)</h3>
            <p>No Chelsea, Desailly se tornou uma lenda, sendo capitão do clube e fundamental nas conquistas da FA Cup e da Copa da Liga.</p>
            <h3>Seleção Francesa</h3>
            <p>Pela seleção francesa, Desailly foi fundamental na conquista da Copa do Mundo de 1998 e da Eurocopa de 2000, formando uma das melhores defesas da história.</p>
        """),
        'carreira': format_html("""
            <ul>
                <li><strong>Nantes (1986-1992):</strong> Início</li>
                <li><strong>Marseille (1992-1993):</strong> Passagem</li>
                <li><strong>Milan (1993-1998):</strong> 186 jogos, 7 gols</li>
                <li><strong>Chelsea (1998-2004):</strong> 222 jogos, 7 gols</li>
                <li><strong>Al-Gharafa (2004-2005):</strong> Passagem</li>
                <li><strong>Qatar SC (2005-2006):</strong> Final da carreira</li>
            </ul>
            <h4>Principais Títulos Coletivos:</h4>
            <ul>
                <li>2x UEFA Champions League</li>
                <li>1x Serie A</li>
                <li>1x Copa do Mundo</li>
                <li>1x Eurocopa</li>
                <li>1x FA Cup</li>
            </ul>
        """)
    },
    'Paul Scholes': {
        'nacionalidade': 'Inglaterra',
        'inicio_carreira': date(1993, 1, 1),
        'fim_carreira': date(2013, 1, 1),
        'altura': '1,70 m',
        'perna': 'Destro',
        'outras_posicoes': 'Meia-central, Meia-atacante',
        'titulos_champions': 2,
        'bola_de_ouro': 0,
        'mundial_clubes': 1,
        'biografia': format_html("""
            <p>Paul Scholes é considerado um dos maiores meio-campistas da história do Manchester United e do futebol inglês. Conhecido por sua visão de jogo, passes precisos e chutes de longa distância, foi fundamental nas conquistas do clube durante duas décadas.</p>
            <h3>Manchester United (1993-2013)</h3>
            <p>No Manchester United, Scholes conquistou 2 Ligas dos Campeões, 1 Mundial de Clubes, 11 títulos da Premier League e 3 FA Cups. Jogou toda sua carreira no clube, tornando-se uma lenda.</p>
            <h3>Seleção Inglesa</h3>
            <p>Pela seleção inglesa, Scholes participou de 2 Copas do Mundo e 2 Eurocopas, sendo um dos principais meio-campistas do time.</p>
            <h3>Legado</h3>
            <p>Scholes é considerado por muitos técnicos e jogadores como um dos melhores meio-campistas da história. Sua técnica e inteligência em campo o tornaram único.</p>
        """),
        'carreira': format_html("""
            <ul>
                <li><strong>Manchester United (1993-2013):</strong> 718 jogos, 155 gols</li>
            </ul>
            <h4>Principais Títulos Coletivos:</h4>
            <ul>
                <li>2x UEFA Champions League</li>
                <li>1x Mundial de Clubes da FIFA</li>
                <li>11x Premier League</li>
                <li>3x FA Cup</li>
            </ul>
            <h4>Principais Títulos Individuais:</h4>
            <ul>
                <li>FIFA 100 (Lista dos 100 maiores jogadores vivos)</li>
                <li>PFA Team of the Year (várias vezes)</li>
            </ul>
        """)
    },
    'Rio Ferdinand': {
        'nacionalidade': 'Inglaterra',
        'inicio_carreira': date(1995, 1, 1),
        'fim_carreira': date(2015, 1, 1),
        'altura': '1,89 m',
        'perna': 'Destro',
        'outras_posicoes': 'Zagueiro',
        'titulos_champions': 1,
        'bola_de_ouro': 0,
        'mundial_clubes': 1,
        'biografia': format_html("""
            <p>Rio Ferdinand é considerado um dos maiores zagueiros da história do Manchester United e do futebol inglês. Conhecido por sua elegância, qualidade técnica e capacidade de construir jogadas, foi fundamental nas conquistas do clube.</p>
            <h3>Manchester United (2002-2014)</h3>
            <p>No Manchester United, Ferdinand conquistou a Liga dos Campeões de 2008, o Mundial de Clubes, 6 títulos da Premier League e 2 Copas da Liga. Formou uma das melhores duplas de zaga da história ao lado de Nemanja Vidić.</p>
            <h3>Seleção Inglesa</h3>
            <p>Pela seleção inglesa, Ferdinand participou de 3 Copas do Mundo e foi um dos principais zagueiros do time durante mais de uma década.</p>
        """),
        'carreira': format_html("""
            <ul>
                <li><strong>West Ham United (1995-2000):</strong> Início</li>
                <li><strong>Leeds United (2000-2002):</strong> Consolidação</li>
                <li><strong>Manchester United (2002-2014):</strong> 455 jogos, 8 gols</li>
                <li><strong>Queens Park Rangers (2014-2015):</strong> Final da carreira</li>
            </ul>
            <h4>Principais Títulos Coletivos:</h4>
            <ul>
                <li>1x UEFA Champions League</li>
                <li>1x Mundial de Clubes da FIFA</li>
                <li>6x Premier League</li>
                <li>2x Copa da Liga Inglesa</li>
            </ul>
        """)
    },
    'Ryan Giggs': {
        'nacionalidade': 'País de Gales',
        'inicio_carreira': date(1990, 1, 1),
        'fim_carreira': date(2014, 1, 1),
        'altura': '1,80 m',
        'perna': 'Canhoto',
        'outras_posicoes': 'Meia-esquerda, Ponta-esquerda',
        'titulos_champions': 2,
        'bola_de_ouro': 0,
        'mundial_clubes': 1,
        'biografia': format_html("""
            <p>Ryan Giggs é o jogador com mais partidas e títulos da história do Manchester United. Conhecido por sua velocidade, dribles e capacidade de criar jogadas, jogou toda sua carreira no clube inglês, tornando-se uma lenda.</p>
            <h3>Manchester United (1990-2014)</h3>
            <p>No Manchester United, Giggs conquistou 2 Ligas dos Campeões, 1 Mundial de Clubes, 13 títulos da Premier League e 4 FA Cups. É o jogador com mais partidas da história do clube, com 963 jogos.</p>
            <h3>Seleção Galesa</h3>
            <p>Pela seleção galesa, Giggs é o jogador com mais partidas da história, com 64 jogos. Foi fundamental na qualificação do país para a Eurocopa de 2016.</p>
            <h3>Legado</h3>
            <p>Giggs é considerado um dos maiores jogadores da história do futebol inglês. Sua longevidade e consistência o tornaram único, jogando em alto nível por mais de duas décadas.</p>
        """),
        'carreira': format_html("""
            <ul>
                <li><strong>Manchester United (1990-2014):</strong> 963 jogos, 168 gols</li>
            </ul>
            <h4>Principais Títulos Coletivos:</h4>
            <ul>
                <li>2x UEFA Champions League</li>
                <li>1x Mundial de Clubes da FIFA</li>
                <li>13x Premier League</li>
                <li>4x FA Cup</li>
            </ul>
            <h4>Principais Títulos Individuais:</h4>
            <ul>
                <li>Jogador do Ano da PFA (2009)</li>
                <li>FIFA 100 (Lista dos 100 maiores jogadores vivos)</li>
                <li>Jogador com mais partidas da história do Manchester United</li>
            </ul>
        """)
    },
    'Thierry Henry': {
        'nacionalidade': 'França',
        'inicio_carreira': date(1994, 1, 1),
        'fim_carreira': date(2014, 1, 1),
        'altura': '1,88 m',
        'perna': 'Destro',
        'outras_posicoes': 'Ponta-esquerda, Meia-atacante',
        'titulos_champions': 0,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': format_html("""
            <p>Thierry Henry é considerado um dos maiores atacantes da história do futebol. Conhecido por sua velocidade, técnica e capacidade de finalização, foi o maior artilheiro da história do Arsenal e fundamental nas conquistas da seleção francesa.</p>
            <h3>Arsenal (1999-2007, 2012)</h3>
            <p>No Arsenal, Henry se tornou uma lenda, conquistando 2 títulos da Premier League e 2 FA Cups. É o maior artilheiro da história do clube, com 228 gols. Foi eleito o melhor jogador da Premier League duas vezes.</p>
            <h3>Barcelona (2007-2010)</h3>
            <p>No Barcelona, Henry conquistou a Liga dos Campeões de 2009, 2 títulos da La Liga e 1 Copa do Rei, sendo fundamental no triplete histórico do clube.</p>
            <h3>Seleção Francesa</h3>
            <p>Pela seleção francesa, Henry é o maior artilheiro da história, com 51 gols. Foi fundamental na conquista da Copa do Mundo de 1998 e da Eurocopa de 2000.</p>
        """),
        'carreira': format_html("""
            <ul>
                <li><strong>Monaco (1994-1999):</strong> Início</li>
                <li><strong>Juventus (1999):</strong> Passagem</li>
                <li><strong>Arsenal (1999-2007, 2012):</strong> 377 jogos, 228 gols</li>
                <li><strong>Barcelona (2007-2010):</strong> 121 jogos, 49 gols</li>
                <li><strong>New York Red Bulls (2010-2014):</strong> Final da carreira</li>
            </ul>
            <h4>Principais Títulos Coletivos:</h4>
            <ul>
                <li>1x UEFA Champions League</li>
                <li>2x Premier League</li>
                <li>2x La Liga</li>
                <li>1x Copa do Mundo</li>
                <li>1x Eurocopa</li>
            </ul>
            <h4>Principais Títulos Individuais:</h4>
            <ul>
                <li>Artilheiro da Premier League (várias vezes)</li>
                <li>Jogador do Ano da PFA (2003, 2004)</li>
                <li>Maior Artilheiro da História do Arsenal</li>
            </ul>
        """)
    },
}

def preencher_todos_jogadores():
    """Preenche TODOS os jogadores que ainda não têm dados completos"""
    atualizados = 0
    nao_encontrados = 0
    ja_completos = 0
    
    print("📝 Iniciando preenchimento completo de TODOS os jogadores...\n")
    
    # Buscar todos os jogadores
    todos_jogadores = Jogador.objects.all()
    
    for jogador in todos_jogadores:
        nome = jogador.nome
        
        # Verificar se já tem dados completos
        tem_biografia = jogador.biografia and len(str(jogador.biografia).strip()) > 50
        tem_carreira = jogador.carreira and len(str(jogador.carreira).strip()) > 50
        tem_dados_basicos = jogador.altura and jogador.perna and jogador.outras_posicoes
        
        if tem_biografia and tem_carreira and tem_dados_basicos:
            print(f"⏭️  '{nome}' já possui dados completos. Pulando...")
            ja_completos += 1
            continue
        
        # Buscar dados no dicionário (tentar variações do nome)
        dados = None
        for chave, valor in DADOS_COMPLETOS.items():
            if nome.lower() == chave.lower() or nome.lower() in chave.lower() or chave.lower() in nome.lower():
                dados = valor
                break
        
        if not dados:
            print(f"⚠️  Dados não encontrados para '{nome}'. Pulando...")
            nao_encontrados += 1
            continue
        
        # Atualizar apenas os campos que estão vazios ou incompletos
        if not tem_dados_basicos:
            jogador.nacionalidade = dados.get('nacionalidade', jogador.nacionalidade)
            jogador.inicio_carreira = dados.get('inicio_carreira', jogador.inicio_carreira)
            jogador.fim_carreira = dados.get('fim_carreira', jogador.fim_carreira)
            jogador.altura = dados.get('altura', jogador.altura)
            jogador.perna = dados.get('perna', jogador.perna)
            jogador.outras_posicoes = dados.get('outras_posicoes', jogador.outras_posicoes)
            jogador.titulos_champions = dados.get('titulos_champions', jogador.titulos_champions)
            jogador.bola_de_ouro = dados.get('bola_de_ouro', jogador.bola_de_ouro)
            jogador.mundial_clubes = dados.get('mundial_clubes', jogador.mundial_clubes)
        
        if not tem_biografia:
            jogador.biografia = dados.get('biografia', jogador.biografia)
        
        if not tem_carreira:
            jogador.carreira = dados.get('carreira', jogador.carreira)
        
        jogador.save()
        
        print(f"✅ '{nome}' atualizado com sucesso!")
        atualizados += 1
    
    print("\n" + "="*60)
    print(f"📊 Resumo Final:")
    print(f"   ✅ Atualizados: {atualizados}")
    print(f"   ⏭️  Já completos: {ja_completos}")
    print(f"   ⚠️  Não encontrados: {nao_encontrados}")
    print(f"   📝 Total processado: {todos_jogadores.count()}")
    print("="*60)

if __name__ == "__main__":
    preencher_todos_jogadores()
    print("\n✨ Processo concluído!")




