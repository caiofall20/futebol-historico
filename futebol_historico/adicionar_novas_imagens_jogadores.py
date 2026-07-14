#!/usr/bin/env python
"""
Script para adicionar novas imagens de jogadores do diretório media/jogadores/
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'futebol_historico.settings')
django.setup()

from blog.models import Jogador
from django.core.files import File
from django.conf import settings

# Mapeamento de arquivos para nomes de jogadores no banco
mapeamento_imagens = {
    'roberto_carlos.jpg': ['Roberto Carlos', 'Roberto Carlos'],
    'cr7.jpg': ['Cristiano Ronaldo', 'Cristiano Ronaldo', 'CR7'],
    'messi.jpg': ['Lionel Messi', 'Messi', 'Lionel Andrés Messi'],
    'messi_chuteira.jpg': ['Lionel Messi', 'Messi', 'Lionel Andrés Messi'],
    'beckham.jpg': ['David Beckham', 'Beckham'],
    'scholes.jpg': ['Paul Scholes', 'Scholes'],
    'rooney.jpg': ['Wayne Rooney', 'Rooney'],
    'ozil.jpg': ['Mesut Özil', 'Özil', 'Ozil', 'Mesut Ozil'],
    'kaka.jpg': ['Kaká', 'Kaka'],
    'henry.jpg': ['Thierry Henry', 'Henry'],
}

diretorio_jogadores = os.path.join(settings.MEDIA_ROOT, 'jogadores')

print("🖼️  Adicionando novas imagens de jogadores...\n")

atualizados = 0
criados = 0
nao_encontrados = 0
sem_imagem = 0

for nome_arquivo, nomes_jogadores in mapeamento_imagens.items():
    caminho_imagem = os.path.join(diretorio_jogadores, nome_arquivo)
    
    # Verificar se o arquivo existe
    if not os.path.exists(caminho_imagem):
        print(f"⚠️  Arquivo '{nome_arquivo}' não encontrado. Pulando...")
        sem_imagem += 1
        continue
    
    # Tentar encontrar o jogador pelo nome
    jogador = None
    for nome_jogador in nomes_jogadores:
        jogador = Jogador.objects.filter(nome__iexact=nome_jogador).first()
        if jogador:
            break
    
    if not jogador:
        print(f"⚠️  Jogador não encontrado para '{nome_arquivo}'. Tentou: {', '.join(nomes_jogadores)}")
        print(f"   💡 Você pode criar este jogador manualmente ou adicionar ao mapeamento.")
        nao_encontrados += 1
        continue
    
    # Carregar e salvar a imagem
    try:
        with open(caminho_imagem, 'rb') as f:
            jogador.imagem.save(nome_arquivo, File(f), save=True)
        print(f"✅ {jogador.nome}: imagem atualizada com '{nome_arquivo}'")
        atualizados += 1
    except Exception as e:
        print(f"❌ Erro ao atualizar imagem para '{jogador.nome}': {e}")
        sem_imagem += 1

print("\n" + "="*50)
print(f"📊 Resumo:")
print(f"   ✅ Atualizados: {atualizados}")
print(f"   ⚠️  Jogadores não encontrados: {nao_encontrados}")
print(f"   ⚠️  Imagens não encontradas: {sem_imagem}")
print("="*50)

if nao_encontrados > 0:
    print("\n💡 Jogadores não encontrados que você pode querer adicionar:")
    print("   - Roberto Carlos")
    print("   - Cristiano Ronaldo (CR7)")
    print("   - Lionel Messi")
    print("   - David Beckham")
    print("   - Wayne Rooney")
    print("   - Mesut Özil")









