from django.utils import timezone
from blog.models import Jogador
from datetime import date

jogadores = [
    {
        'nome': 'Roberto Baggio',
        'nacionalidade': 'Itália',
        'inicio_carreira': date(1982, 1, 1),
        'fim_carreira': date(2004, 1, 1),
        'biografia': 'Roberto Baggio é considerado um dos maiores jogadores italianos de todos os tempos. Conhecido como "Il Divin Codino" (O Divino Rabinho), devido ao seu característico penteado, Baggio foi um atacante extremamente habilidoso e criativo. Vencedor da Bola de Ouro em 1993, ele é lembrado por sua técnica refinada e capacidade de decidir jogos.',
        'carta': 'cartas_jogadores/Baggio.png'
    },
    {
        'nome': 'Edgar Davids',
        'nacionalidade': 'Holanda',
        'inicio_carreira': date(1991, 1, 1),
        'fim_carreira': date(2014, 1, 1),
        'biografia': 'Edgar Davids foi um dos meio-campistas mais dominantes de sua geração. Conhecido por seus óculos de proteção e estilo agressivo de jogo, o holandês era chamado de "Pitbull" por sua marcação forte e presença intimidadora em campo. Sua passagem mais notável foi pela Juventus.',
        'carta': 'cartas_jogadores/Davids.png'
    },
    {
        'nome': 'Samuel Etoo',
        'nacionalidade': 'Camarões',
        'inicio_carreira': date(1997, 1, 1),
        'fim_carreira': date(2019, 1, 1),
        'biografia': 'Samuel Etoo é considerado um dos maiores jogadores africanos de todos os tempos. Atacante veloz e com faro de gol, brilhou no Barcelona e na Inter de Milão. Foi fundamental nas conquistas da Liga dos Campeões por ambos os clubes e é o maior artilheiro da história da seleção de Camarões.',
        'carta': 'cartas_jogadores/Etoo.png'
    },
    {
        'nome': 'Kaká',
        'nacionalidade': 'Brasil',
        'inicio_carreira': date(2001, 1, 1),
        'fim_carreira': date(2017, 1, 1),
        'biografia': 'Ricardo Izecson dos Santos Leite, conhecido como Kaká, foi um dos meio-campistas mais elegantes do futebol. Vencedor da Bola de Ouro em 2007, ele se destacou principalmente no Milan, onde conquistou a Liga dos Campeões. Sua velocidade, visão de jogo e capacidade de finalização o tornaram um dos melhores jogadores de sua geração.',
        'carta': 'cartas_jogadores/kaka.png'
    },
    {
        'nome': 'Diego Maradona',
        'nacionalidade': 'Argentina',
        'inicio_carreira': date(1976, 1, 1),
        'fim_carreira': date(1997, 1, 1),
        'biografia': 'Diego Armando Maradona é considerado por muitos o maior jogador de todos os tempos. Sua técnica extraordinária, dribles desconcertantes e liderança em campo o tornaram uma lenda. Foi o protagonista da conquista da Copa do Mundo de 1986 pela Argentina e ídolo máximo do Napoli.',
        'carta': 'cartas_jogadores/maradona.png'
    },
    {
        'nome': 'Pavel Nedved',
        'nacionalidade': 'República Tcheca',
        'inicio_carreira': date(1991, 1, 1),
        'fim_carreira': date(2009, 1, 1),
        'biografia': 'Pavel Nedved foi um meio-campista completo, conhecido por sua incrível resistência física e qualidade técnica. Vencedor da Bola de Ouro em 2003, o tcheco se tornou uma lenda da Juventus, onde sua dedicação e habilidade o transformaram em um dos melhores jogadores da história do clube.',
        'carta': 'cartas_jogadores/Nedved.png'
    },
    {
        'nome': 'Juan Román Riquelme',
        'nacionalidade': 'Argentina',
        'inicio_carreira': date(1996, 1, 1),
        'fim_carreira': date(2015, 1, 1),
        'biografia': 'Juan Román Riquelme foi um dos últimos grandes engenheiros do futebol. Meio-campista clássico, com visão de jogo extraordinária e passes precisos, ele é considerado um dos maiores ídolos da história do Boca Juniors. Sua forma de jogar, pausada e cerebral, o tornou único.',
        'carta': 'cartas_jogadores/Riquelme.png'
    },
    {
        'nome': 'Rivaldo',
        'nacionalidade': 'Brasil',
        'inicio_carreira': date(1991, 1, 1),
        'fim_carreira': date(2015, 1, 1),
        'biografia': 'Rivaldo foi um dos jogadores mais talentosos de sua geração. Vencedor da Bola de Ouro em 1999, o brasileiro era conhecido por seus gols espetaculares e habilidade técnica impressionante. Foi peça fundamental na conquista da Copa do Mundo de 2002 pela seleção brasileira.',
        'carta': 'cartas_jogadores/Rivaldo.png'
    },
    {
        'nome': 'Romário',
        'nacionalidade': 'Brasil',
        'inicio_carreira': date(1985, 1, 1),
        'fim_carreira': date(2009, 1, 1),
        'biografia': 'Romário é considerado um dos maiores atacantes da história do futebol. Conhecido por sua incrível capacidade de finalização e movimentação dentro da área, foi o principal jogador da seleção brasileira na conquista da Copa do Mundo de 1994. Auto-intitulado "O Baixinho", marcou mais de mil gols na carreira.',
        'carta': 'cartas_jogadores/Romario.png'
    },
    {
        'nome': 'Ronaldinho Gaúcho',
        'nacionalidade': 'Brasil',
        'inicio_carreira': date(1998, 1, 1),
        'fim_carreira': date(2018, 1, 1),
        'biografia': 'Ronaldinho Gaúcho é considerado um dos jogadores mais habilidosos de todos os tempos. Sua criatividade, dribles e alegria em campo o tornaram um ícone global do futebol. Vencedor da Bola de Ouro em 2005, ele revolucionou o Barcelona e foi fundamental na conquista da Copa do Mundo de 2002 pelo Brasil.',
        'carta': 'cartas_jogadores/Ronaldinho.png'
    },
    {
        'nome': 'Ronaldo Nazário',
        'nacionalidade': 'Brasil',
        'inicio_carreira': date(1993, 1, 1),
        'fim_carreira': date(2011, 1, 1),
        'biografia': 'Ronaldo Nazário, conhecido como "Fenômeno", é considerado um dos maiores atacantes da história. Sua combinação única de velocidade, força e técnica o tornou praticamente imparável. Vencedor de duas Copas do Mundo (1994 e 2002) e três vezes eleito melhor jogador do mundo pela FIFA.',
        'carta': 'cartas_jogadores/Ronaldo.png'
    },
    {
        'nome': 'Francesco Totti',
        'nacionalidade': 'Itália',
        'inicio_carreira': date(1992, 1, 1),
        'fim_carreira': date(2017, 1, 1),
        'biografia': 'Francesco Totti é um dos maiores símbolos de lealdade no futebol. Jogou toda sua carreira pela Roma, tornando-se o maior ídolo da história do clube. Conhecido como "Il Gladiatore" e "Il Re di Roma" (O Rei de Roma), sua técnica refinada e liderança o tornaram uma lenda do futebol italiano.',
        'carta': 'cartas_jogadores/Totti.png'
    },
    {
        'nome': 'Zinedine Zidane',
        'nacionalidade': 'França',
        'inicio_carreira': date(1989, 1, 1),
        'fim_carreira': date(2006, 1, 1),
        'biografia': 'Zinedine Zidane é considerado um dos maiores meio-campistas da história. Sua elegância em campo, visão de jogo e técnica apurada o tornaram único. Vencedor da Copa do Mundo de 1998 pela França e da Liga dos Campeões pelo Real Madrid, "Zizou" foi eleito melhor jogador do mundo três vezes.',
        'carta': 'cartas_jogadores/zidane.png'
    },
]

for jogador_data in jogadores:
    jogador = Jogador.objects.create(
        nome=jogador_data['nome'],
        nacionalidade=jogador_data['nacionalidade'],
        inicio_carreira=jogador_data['inicio_carreira'],
        fim_carreira=jogador_data['fim_carreira'],
        biografia=jogador_data['biografia'],
        carta=jogador_data['carta']
    )
    print(f"Jogador {jogador.nome} cadastrado com sucesso!")
