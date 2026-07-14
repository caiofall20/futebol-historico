import os
import django
from datetime import date
from django.core.files import File
from django.conf import settings

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'futebol_historico.settings')
django.setup()

from blog.models import Jogador

# Lista de novos jogadores com informações
novos_jogadores = [
    {
        'nome': 'Paul Scholes',
        'nacionalidade': 'Inglaterra',
        'inicio_carreira': date(1993, 1, 1),
        'fim_carreira': date(2013, 1, 1),
        'altura': '1,70 m',
        'perna': 'Destro',
        'outras_posicoes': 'Meia-central, Volante',
        'titulos_champions': 2,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': 'Paul Scholes é considerado um dos maiores meio-campistas da história do Manchester United e da Inglaterra. Conhecido por sua visão de jogo, passes precisos e chutes de longa distância, foi fundamental nas conquistas do United durante a era Ferguson. Jogou toda sua carreira no clube de Manchester.',
        'carreira': '<p><strong>Manchester United (1993-2013)</strong> - Carreira inteira no clube, ídolo máximo</p>',
        'carta': 'cartas_jogadores/scholes.png'
    },
    {
        'nome': 'Ryan Giggs',
        'nacionalidade': 'País de Gales',
        'inicio_carreira': date(1990, 1, 1),
        'fim_carreira': date(2014, 1, 1),
        'altura': '1,80 m',
        'perna': 'Canhoto',
        'outras_posicoes': 'Meia-esquerda, Ponta-esquerda',
        'titulos_champions': 2,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': 'Ryan Giggs é o jogador com mais títulos na história do futebol inglês. Conhecido por sua velocidade, dribles e longevidade, jogou toda sua carreira no Manchester United. É o jogador com mais partidas pelo clube (963 jogos).',
        'carreira': '<p><strong>Manchester United (1990-2014)</strong> - Carreira inteira no clube, recordista de jogos</p>',
        'carta': 'cartas_jogadores/giggs.png'
    },
    {
        'nome': 'Rio Ferdinand',
        'nacionalidade': 'Inglaterra',
        'inicio_carreira': date(1995, 1, 1),
        'fim_carreira': date(2015, 1, 1),
        'altura': '1,88 m',
        'perna': 'Destro',
        'outras_posicoes': 'Zagueiro',
        'titulos_champions': 1,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': 'Rio Ferdinand foi um dos melhores zagueiros de sua geração. Conhecido por sua qualidade técnica, velocidade e capacidade de saída com a bola, foi fundamental nas conquistas do Manchester United. Formou uma das melhores duplas de zaga da história com Nemanja Vidić.',
        'carreira': '<p><strong>West Ham (1995-2000)</strong> - Início</p><p><strong>Leeds United (2000-2002)</strong> - Consolidação</p><p><strong>Manchester United (2002-2014)</strong> - Melhor fase</p><p><strong>Queens Park Rangers (2014-2015)</strong> - Final da carreira</p>',
        'carta': 'cartas_jogadores/ferdinand.png'
    },
    {
        'nome': 'Eric Cantona',
        'nacionalidade': 'França',
        'inicio_carreira': date(1983, 1, 1),
        'fim_carreira': date(1997, 1, 1),
        'altura': '1,88 m',
        'perna': 'Destro',
        'outras_posicoes': 'Atacante, Meia-atacante',
        'titulos_champions': 0,
        'bola_de_ouro': 0,
        'mundial_clubes': 0,
        'biografia': 'Eric Cantona foi um dos jogadores mais carismáticos e talentosos da história do futebol. Conhecido por sua técnica refinada, visão de jogo e personalidade marcante, foi fundamental no renascimento do Manchester United nos anos 90. Ídolo máximo do clube.',
        'carreira': '<p><strong>Auxerre (1983-1988)</strong> - Início</p><p><strong>Marseille (1988-1991)</strong> - Passagem</p><p><strong>Nîmes (1991-1992)</strong> - Passagem</p><p><strong>Leeds United (1992)</strong> - Passagem curta</p><p><strong>Manchester United (1992-1997)</strong> - Melhor fase, ídolo</p>',
        'carta': 'cartas_jogadores/cantona.png'
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
        
        # Criar o jogador com todos os dados (sem a carta primeiro)
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
            carreira=jogador_data['carreira']
        )
        
        # Carregar a imagem da carta
        nome_arquivo = jogador_data['carta'].split('/')[-1]
        caminho_imagem = os.path.join(settings.MEDIA_ROOT, 'cartas_jogadores', nome_arquivo)
        
        if os.path.exists(caminho_imagem):
            with open(caminho_imagem, 'rb') as f:
                jogador.carta.save(nome_arquivo, File(f), save=True)
            print(f"✅ Jogador '{nome}' cadastrado com sucesso! (Nacionalidade: {jogador_data['nacionalidade']}, Imagem: {nome_arquivo})")
        else:
            print(f"⚠️  Jogador '{nome}' cadastrado, mas imagem '{nome_arquivo}' não encontrada em {caminho_imagem}.")
        
        cadastrados += 1
    
    print("\n" + "="*50)
    print(f"📊 Resumo:")
    print(f"   ✅ Cadastrados: {cadastrados}")
    print(f"   ⚠️  Já existentes: {ja_existentes}")
    print(f"   📝 Total na lista: {len(novos_jogadores)}")
    print("="*50)

def atualizar_imagem_van_der_sar():
    """Atualiza a imagem do van der Sar"""
    print("\n🖼️  Atualizando imagem do van der Sar...\n")
    
    # Buscar o jogador (case-insensitive)
    jogador = Jogador.objects.filter(nome__icontains='van der Sar').first()
    
    if not jogador:
        print("⚠️  Jogador 'Edwin van der Sar' não encontrado no banco.")
        return
    
    # Caminho da imagem
    nome_arquivo = 'van_der_sar.png'
    caminho_imagem = os.path.join(settings.MEDIA_ROOT, 'cartas_jogadores', nome_arquivo)
    
    # Verificar se o arquivo existe
    if not os.path.exists(caminho_imagem):
        print(f"⚠️  Arquivo 'van_der_sar.png' não encontrado em {caminho_imagem}.")
        return
    
    # Atualizar o campo carta do jogador usando File()
    with open(caminho_imagem, 'rb') as f:
        jogador.carta.save(nome_arquivo, File(f), save=True)
    
    print(f"✅ Imagem de '{jogador.nome}' atualizada com sucesso!")

if __name__ == "__main__":
    cadastrar_jogadores()
    atualizar_imagem_van_der_sar()
    print("\n✨ Processo concluído!")

