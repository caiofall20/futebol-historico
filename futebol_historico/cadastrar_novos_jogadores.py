import os
import django
from datetime import date

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'futebol_historico.settings')
django.setup()

from blog.models import Jogador

# Lista de novos jogadores com informações
novos_jogadores = [
    {
        'nome': 'Thierry Henry',
        'nacionalidade': 'França',
        'inicio_carreira': date(1994, 1, 1),
        'fim_carreira': date(2014, 1, 1),
        'altura': '1,88 m',
        'perna': 'Destro',
        'outras_posicoes': 'Ponta-esquerda',
        'titulos_champions': 0,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': 'Thierry Henry é considerado um dos maiores atacantes da história do futebol. Maior artilheiro da história do Arsenal, foi fundamental na conquista da Copa do Mundo de 1998 e Eurocopa de 2000 pela França. Conhecido por sua velocidade, técnica e finalização precisa.',
        'carreira': '<p><strong>Monaco (1994-1999)</strong> - Início e consolidação</p><p><strong>Juventus (1999)</strong> - Passagem curta</p><p><strong>Arsenal (1999-2007, 2012)</strong> - Maior período, ídolo máximo</p><p><strong>Barcelona (2007-2010)</strong> - Títulos</p><p><strong>New York Red Bulls (2010-2014)</strong> - Final da carreira</p>',
        'carta': 'cartas_jogadores/henry.png'
    },
    {
        'nome': 'Demetrio Albertini',
        'nacionalidade': 'Itália',
        'inicio_carreira': date(1988, 1, 1),
        'fim_carreira': date(2005, 1, 1),
        'altura': '1,80 m',
        'perna': 'Destro',
        'outras_posicoes': 'Volante, Meia-central',
        'titulos_champions': 2,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': 'Demetrio Albertini foi um dos maiores meio-campistas italianos dos anos 90. Conhecido por sua visão de jogo e passes precisos, foi fundamental nas conquistas do Milan. Participou de três Copas do Mundo pela Itália (1994, 1998, 2002).',
        'carreira': '<p><strong>Milan (1988-2002)</strong> - Maior período, ídolo</p><p><strong>Atletico Madrid (2002-2003)</strong> - Passagem</p><p><strong>Lazio (2003-2004)</strong> - Passagem</p><p><strong>Atalanta (2004-2005)</strong> - Final da carreira</p>',
        'carta': 'cartas_jogadores/albertini.png'
    },
    {
        'nome': 'Albert Ferrer',
        'nacionalidade': 'Espanha',
        'inicio_carreira': date(1989, 1, 1),
        'fim_carreira': date(2003, 1, 1),
        'altura': '1,70 m',
        'perna': 'Destro',
        'outras_posicoes': 'Lateral-esquerdo, Zagueiro',
        'titulos_champions': 1,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': 'Albert Ferrer foi um dos melhores laterais-direitos de sua geração. Conhecido por sua velocidade e capacidade ofensiva, foi fundamental nas conquistas do Barcelona nos anos 90. Campeão da Liga dos Campeões de 1992 pelo Barcelona.',
        'carreira': '<p><strong>Barcelona (1989-1998)</strong> - Maior período</p><p><strong>Chelsea (1998-2003)</strong> - Final da carreira</p>',
        'carta': 'cartas_jogadores/ferrer.png'
    },
    {
        'nome': 'Marcel Desailly',
        'nacionalidade': 'França',
        'inicio_carreira': date(1986, 1, 1),
        'fim_carreira': date(2006, 1, 1),
        'altura': '1,85 m',
        'perna': 'Destro',
        'outras_posicoes': 'Volante, Lateral-direito',
        'titulos_champions': 2,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': 'Marcel Desailly foi um dos maiores zagueiros da história do futebol. Conhecido por sua força física e liderança, foi campeão mundial em 1998 e Eurocopa em 2000 pela França. Conquistou a Liga dos Campeões pelo Milan e Marseille.',
        'carreira': '<p><strong>Nantes (1986-1992)</strong> - Início</p><p><strong>Marseille (1992-1993)</strong> - Consolidação</p><p><strong>Milan (1993-1998)</strong> - Melhor fase</p><p><strong>Chelsea (1998-2004)</strong> - Maior período</p><p><strong>Al-Gharafa (2004-2005)</strong> - Passagem</p>',
        'carta': 'cartas_jogadores/desaily.png'
    },
    {
        'nome': 'Andrea Pirlo',
        'nacionalidade': 'Itália',
        'inicio_carreira': date(1995, 1, 1),
        'fim_carreira': date(2017, 1, 1),
        'altura': '1,77 m',
        'perna': 'Destro',
        'outras_posicoes': 'Meia-central, Volante',
        'titulos_champions': 2,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': 'Andrea Pirlo é considerado um dos maiores meio-campistas da história do futebol. Conhecido por sua visão de jogo, passes precisos e cobranças de falta, foi fundamental nas conquistas da Copa do Mundo de 2006 pela Itália e da Liga dos Campeões pelo Milan.',
        'carreira': '<p><strong>Brescia (1995-1998, 2001)</strong> - Início</p><p><strong>Inter de Milão (1998-2001)</strong> - Passagem</p><p><strong>Milan (2001-2011)</strong> - Maior período</p><p><strong>Juventus (2011-2015)</strong> - Melhor fase</p><p><strong>New York City FC (2015-2017)</strong> - Final da carreira</p>',
        'carta': 'cartas_jogadores/pirlo.png'
    },
    {
        'nome': 'Edwin van der Sar',
        'nacionalidade': 'Holanda',
        'inicio_carreira': date(1990, 1, 1),
        'fim_carreira': date(2011, 1, 1),
        'altura': '1,97 m',
        'perna': 'Destro',
        'outras_posicoes': 'Goleiro',
        'titulos_champions': 2,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': 'Edwin van der Sar foi um dos melhores goleiros de sua geração. Conhecido por sua segurança e qualidade com os pés, foi campeão da Liga dos Campeões pelo Ajax e Manchester United. É o jogador mais velho a conquistar a Liga dos Campeões (40 anos).',
        'carreira': '<p><strong>Ajax (1990-1999)</strong> - Início e consolidação</p><p><strong>Juventus (1999-2001)</strong> - Passagem</p><p><strong>Fulham (2001-2005)</strong> - Passagem</p><p><strong>Manchester United (2005-2011)</strong> - Melhor fase</p>',
        'carta': 'cartas_jogadores/van_der_sar.png'
    }
]

def cadastrar_jogadores():
    """Cadastra os novos jogadores"""
    cadastrados = 0
    ja_existentes = 0
    
    print("🚀 Iniciando cadastro de novos jogadores...\n")
    
    for jogador_data in novos_jogadores:
        nome = jogador_data['nome']
        
        # Verificar se o jogador já existe (busca case-insensitive)
        jogador_existente = Jogador.objects.filter(nome__iexact=nome).first()
        
        if jogador_existente:
            print(f"⚠️  Jogador '{nome}' já está cadastrado. Pulando...")
            ja_existentes += 1
            continue
        
        # Criar o jogador com todos os dados
        jogador = Jogador.objects.create(
            nome=nome,
            nacionalidade=jogador_data['nacionalidade'],
            inicio_carreira=jogador_data['inicio_carreira'],
            fim_carreira=jogador_data['fim_carreira'],
            altura=jogador_data['altura'],
            perna=jogador_data['perna'],
            outras_posicoes=jogador_data['outras_posicoes'],
            titulos_champions=jogador_data['titulos_champions'],
            bola_de_ouro=jogador_data['bola_de_ouro'],
            mundial_clubes=jogador_data['mundial_clubes'],
            biografia=jogador_data['biografia'],
            carreira=jogador_data['carreira'],
            carta=jogador_data['carta']
        )
        
        print(f"✅ Jogador '{nome}' cadastrado com sucesso! (Nacionalidade: {jogador_data['nacionalidade']})")
        cadastrados += 1
    
    print("\n" + "="*50)
    print(f"📊 Resumo:")
    print(f"   ✅ Cadastrados: {cadastrados}")
    print(f"   ⚠️  Já existentes: {ja_existentes}")
    print(f"   📝 Total na lista: {len(novos_jogadores)}")
    print("="*50)

if __name__ == "__main__":
    cadastrar_jogadores()
    print("\n✨ Processo concluído!")










