#!/usr/bin/env python
"""
Script para preencher os pilares dos times históricos
"""

import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'futebol_historico.settings')
django.setup()

from blog.models import Time

# Dados dos pilares por time
PILARES_DATA = {
    'Arsenal 2004': {
        'pilar1_nome': 'Thierry Henry',
        'pilar1_descricao': 'Artilheiro histórico e líder do ataque. Maior goleador da história do Arsenal, foi fundamental na campanha invicta de 2003-04.',
        'pilar2_nome': 'Dennis Bergkamp',
        'pilar2_descricao': 'Gênio criativo do meio-campo. Sua visão de jogo e passes precisos foram essenciais para o estilo de jogo ofensivo do time.',
        'pilar3_nome': 'Patrick Vieira',
        'pilar3_descricao': 'Líder e capitão do meio-campo. Sua presença física e liderança foram fundamentais na conquista da Premier League invicta.',
    },
    'Barcelona 2009': {
        'pilar1_nome': 'Lionel Messi',
        'pilar1_descricao': 'Gênio absoluto do futebol. Artilheiro e criador, foi o principal nome do time que conquistou 6 títulos em 2009.',
        'pilar2_nome': 'Xavi Hernández',
        'pilar2_descricao': 'Cérebro do meio-campo. Seu controle de jogo e passes precisos definiram o estilo tiki-taka do Barcelona.',
        'pilar3_nome': 'Andrés Iniesta',
        'pilar3_descricao': 'Criador de jogadas e autor do gol do título da Champions League. Sua técnica e visão foram essenciais.',
    },
    'Bayern de Munique 2013': {
        'pilar1_nome': 'Arjen Robben',
        'pilar1_descricao': 'Extremo direito letal. Sua velocidade e chute com a perna esquerda foram decisivos na conquista da tríplice coroa.',
        'pilar2_nome': 'Franck Ribéry',
        'pilar2_descricao': 'Extremo esquerdo criativo. Formou uma dupla devastadora com Robben, sendo eleito o melhor jogador da Europa em 2013.',
        'pilar3_nome': 'Bastian Schweinsteiger',
        'pilar3_descricao': 'Líder do meio-campo. Sua experiência e qualidade técnica foram fundamentais na conquista da Champions League.',
    },
    'Bayern de Munique 2020': {
        'pilar1_nome': 'Robert Lewandowski',
        'pilar1_descricao': 'Artilheiro implacável. Bateu recordes de gols e foi fundamental na conquista da Champions League e tríplice coroa.',
        'pilar2_nome': 'Thomas Müller',
        'pilar2_descricao': 'Raumdeuter (intérprete de espaços). Sua inteligência tática e capacidade de aparecer nos lugares certos foram cruciais.',
        'pilar3_nome': 'Joshua Kimmich',
        'pilar3_descricao': 'Versátil e técnico. Jogou como volante e lateral, sendo um dos principais pilares do time campeão europeu.',
    },
    'Milan 1989': {
        'pilar1_nome': 'Marco van Basten',
        'pilar1_descricao': 'Artilheiro de classe mundial. Sua técnica refinada e gols espetaculares marcaram a era de ouro do Milan.',
        'pilar2_nome': 'Ruud Gullit',
        'pilar2_descricao': 'Meia-atacante completo. Força física, técnica e liderança fizeram dele um dos maiores jogadores da história do clube.',
        'pilar3_nome': 'Frank Rijkaard',
        'pilar3_descricao': 'Volante de classe. Sua qualidade técnica e visão de jogo foram essenciais no meio-campo do Milan campeão europeu.',
    },
    'Manchester United 1999': {
        'pilar1_nome': 'David Beckham',
        'pilar1_descricao': 'Especialista em bolas paradas e cruzamentos precisos. Seus passes e assistências foram fundamentais na tríplice coroa.',
        'pilar2_nome': 'Roy Keane',
        'pilar2_descricao': 'Capitão e líder do meio-campo. Sua garra e liderança foram essenciais na conquista da Champions League.',
        'pilar3_nome': 'Dwight Yorke',
        'pilar3_descricao': 'Artilheiro do ataque. Formou dupla letal com Andy Cole, sendo decisivo na campanha da tríplice coroa.',
    },
    'Manchester United 2008': {
        'pilar1_nome': 'Cristiano Ronaldo',
        'pilar1_descricao': 'Estrela do time. Artilheiro e criador, foi fundamental na conquista da Champions League e Premier League.',
        'pilar2_nome': 'Wayne Rooney',
        'pilar2_descricao': 'Atacante completo. Sua versatilidade e gols foram essenciais na conquista da tríplice coroa.',
        'pilar3_nome': 'Carlos Tevez',
        'pilar3_descricao': 'Atacante incansável. Sua garra e qualidade técnica complementaram o trio ofensivo letal do United.',
    },
    'Real Madrid 1956-1960': {
        'pilar1_nome': 'Alfredo Di Stéfano',
        'pilar1_descricao': 'Lenda do futebol. Líder e artilheiro, foi o principal nome do Real Madrid que conquistou 5 Champions consecutivas.',
        'pilar2_nome': 'Ferenc Puskás',
        'pilar2_descricao': 'Artilheiro húngaro de classe mundial. Sua técnica e gols espetaculares marcaram a era dourada do clube.',
        'pilar3_nome': 'Francisco Gento',
        'pilar3_descricao': 'Extremo esquerdo histórico. Velocidade e qualidade técnica fizeram dele um dos maiores jogadores do Real Madrid.',
    },
    'Flamengo 1981': {
        'pilar1_nome': 'Zico',
        'pilar1_descricao': 'Rei do Maracanã. Maior ídolo da história do Flamengo, foi o principal nome da conquista da Libertadores e Mundial.',
        'pilar2_nome': 'Júnior',
        'pilar2_descricao': 'Lateral esquerdo de classe mundial. Sua qualidade técnica e ofensiva foram fundamentais no time campeão.',
        'pilar3_nome': 'Adílio',
        'pilar3_descricao': 'Meia criativo. Sua qualidade técnica e visão de jogo foram essenciais no meio-campo do Flamengo campeão.',
    },
    'São Paulo 1992/1993': {
        'pilar1_nome': 'Raí',
        'pilar1_descricao': 'Capitão e líder do time. Meia de classe mundial, foi fundamental nas conquistas da Libertadores e Mundial.',
        'pilar2_nome': 'Müller',
        'pilar2_descricao': 'Artilheiro histórico. Sua qualidade técnica e gols decisivos foram essenciais nas conquistas internacionais.',
        'pilar3_nome': 'Cafú',
        'pilar3_descricao': 'Lateral direito de classe mundial. Sua velocidade e qualidade ofensiva marcaram o time campeão mundial.',
    },
    'Boca Juniors 2000': {
        'pilar1_nome': 'Juan Román Riquelme',
        'pilar1_descricao': 'Gênio do meio-campo. Sua qualidade técnica e visão de jogo foram fundamentais na conquista da Libertadores.',
        'pilar2_nome': 'Martín Palermo',
        'pilar2_descricao': 'Artilheiro histórico. Sua capacidade de marcar gols decisivos foi essencial na campanha vitoriosa.',
        'pilar3_nome': 'Carlos Tévez',
        'pilar3_descricao': 'Atacante promissor. Sua garra e qualidade técnica já anunciavam o grande jogador que se tornaria.',
    },
    'River Plate 1986': {
        'pilar1_nome': 'Enzo Francescoli',
        'pilar1_descricao': 'Gênio uruguaio. Meia de classe mundial, foi o principal nome do River Plate campeão da Libertadores.',
        'pilar2_nome': 'Nery Pumpido',
        'pilar2_descricao': 'Goleiro de seleção. Sua experiência e qualidade foram fundamentais na conquista da Libertadores.',
        'pilar3_nome': 'Ramón Díaz',
        'pilar3_descricao': 'Artilheiro histórico. Sua qualidade técnica e gols foram essenciais na campanha vitoriosa.',
    },
    'Porto 2004': {
        'pilar1_nome': 'Deco',
        'pilar1_descricao': 'Meia criativo português. Sua qualidade técnica e visão de jogo foram fundamentais na conquista da Champions League.',
        'pilar2_nome': 'Ricardo Carvalho',
        'pilar2_descricao': 'Zagueiro de classe mundial. Sua qualidade defensiva foi essencial na campanha vitoriosa.',
        'pilar3_nome': 'Benni McCarthy',
        'pilar3_descricao': 'Artilheiro sul-africano. Seus gols foram decisivos na conquista da Champions League sob comando de Mourinho.',
    },
    'Ajax 1995': {
        'pilar1_nome': 'Clarence Seedorf',
        'pilar1_descricao': 'Meia completo de classe mundial. Sua qualidade técnica e física foram fundamentais na conquista da Champions League.',
        'pilar2_nome': 'Edgar Davids',
        'pilar2_descricao': 'Volante incansável. Sua garra e qualidade técnica marcaram o meio-campo do Ajax campeão europeu.',
        'pilar3_nome': 'Patrick Kluivert',
        'pilar3_descricao': 'Artilheiro promissor. Autor do gol do título, já anunciava o grande jogador que se tornaria.',
    },
    'Ajax 1971-1973': {
        'pilar1_nome': 'Johan Cruyff',
        'pilar1_descricao': 'Gênio do futebol total. Líder e criador, foi o principal nome do Ajax que conquistou 3 Champions consecutivas.',
        'pilar2_nome': 'Johan Neeskens',
        'pilar2_descricao': 'Meia de classe mundial. Sua qualidade técnica e visão de jogo foram essenciais no time campeão europeu.',
        'pilar3_nome': 'Arie Haan',
        'pilar3_descricao': 'Meia versátil. Sua qualidade técnica e capacidade de marcar gols importantes marcaram a era dourada do Ajax.',
    },
    'Marseille 1993': {
        'pilar1_nome': 'Didier Deschamps',
        'pilar1_descricao': 'Capitão e líder. Volante de classe mundial, foi fundamental na conquista da Champions League.',
        'pilar2_nome': 'Fabien Barthez',
        'pilar2_descricao': 'Goleiro de seleção. Sua qualidade e experiência foram essenciais na campanha vitoriosa.',
        'pilar3_nome': 'Rudi Völler',
        'pilar3_descricao': 'Atacante alemão experiente. Sua qualidade técnica e gols foram importantes na conquista europeia.',
    },
    'Celtic 1967': {
        'pilar1_nome': 'Billy McNeill',
        'pilar1_descricao': 'Capitão histórico. Zagueiro e líder, foi o primeiro britânico a levantar a Taça dos Campeões Europeus.',
        'pilar2_nome': 'Jimmy Johnstone',
        'pilar2_descricao': 'Extremo direito de classe. Sua velocidade e qualidade técnica foram fundamentais na conquista histórica.',
        'pilar3_nome': 'Bobby Lennox',
        'pilar3_descricao': 'Atacante histórico. Autor de gols importantes, foi essencial na campanha do "Lisbon Lions".',
    },
    'Peñarol 1961': {
        'pilar1_nome': 'Alberto Spencer',
        'pilar1_descricao': 'Artilheiro histórico. Maior goleador da história da Libertadores, foi fundamental na conquista.',
        'pilar2_nome': 'Luis Cubilla',
        'pilar2_descricao': 'Meia criativo uruguaio. Sua qualidade técnica foi essencial no time campeão da Libertadores.',
        'pilar3_nome': 'William Martínez',
        'pilar3_descricao': 'Zagueiro de seleção. Sua qualidade defensiva foi fundamental na campanha vitoriosa.',
    },
    'Internazionale 2010': {
        'pilar1_nome': 'Wesley Sneijder',
        'pilar1_descricao': 'Meia criativo holandês. Sua qualidade técnica e visão de jogo foram fundamentais na conquista da tríplice coroa.',
        'pilar2_nome': 'Diego Milito',
        'pilar2_descricao': 'Artilheiro decisivo. Autor dos gols das finais, foi o principal nome da conquista da Champions League.',
        'pilar3_nome': 'Samuel Eto\'o',
        'pilar3_descricao': 'Atacante de classe mundial. Sua experiência e gols foram essenciais na campanha vitoriosa sob Mourinho.',
    },
}

def preencher_pilares():
    print("="*70)
    print("PREENCHENDO PILARES DOS TIMES")
    print("="*70)
    print()
    
    sucesso = 0
    nao_encontrados = []
    
    for nome_time, pilares in PILARES_DATA.items():
        try:
            time = Time.objects.get(nome=nome_time)
            
            # Preencher pilares
            time.pilar1_nome = pilares.get('pilar1_nome', '')
            time.pilar1_descricao = pilares.get('pilar1_descricao', '')
            time.pilar2_nome = pilares.get('pilar2_nome', '')
            time.pilar2_descricao = pilares.get('pilar2_descricao', '')
            time.pilar3_nome = pilares.get('pilar3_nome', '')
            time.pilar3_descricao = pilares.get('pilar3_descricao', '')
            
            time.save()
            
            print(f"✅ {nome_time}")
            print(f"   Pilar 1: {pilares.get('pilar1_nome', 'N/A')}")
            print(f"   Pilar 2: {pilares.get('pilar2_nome', 'N/A')}")
            print(f"   Pilar 3: {pilares.get('pilar3_nome', 'N/A')}")
            print()
            
            sucesso += 1
            
        except Time.DoesNotExist:
            print(f"⚠️  Time '{nome_time}' não encontrado no banco")
            nao_encontrados.append(nome_time)
            print()
    
    print("="*70)
    print(f"✅ Processo concluído!")
    print(f"   Sucesso: {sucesso}")
    if nao_encontrados:
        print(f"   Não encontrados: {len(nao_encontrados)}")
        for nome in nao_encontrados:
            print(f"      - {nome}")
    print("="*70)
    print()
    print("💡 NOTA: As imagens dos pilares precisam ser adicionadas manualmente")
    print("   no painel administrativo do Django.")

if __name__ == '__main__':
    preencher_pilares()





