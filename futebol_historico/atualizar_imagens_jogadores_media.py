#!/usr/bin/env python
"""
Script para atualizar as imagens dos jogadores usando arquivos do diretório media/jogadores/
"""
import os
import django

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'futebol_historico.settings')
django.setup()

from blog.models import Jogador
from django.core.files import File
from django.conf import settings

# Mapeamento de nomes de arquivo para nomes de jogadores no banco
# Baseado nos arquivos disponíveis em media/jogadores/
mapeamento_imagens = {
    'baggio.jpg': ['Roberto Baggio', 'Baggio'],
    'canavarro.jpg': ['Fabio Cannavaro', 'Cannavaro', 'Canavarro'],
    'jairzinho.jpg': ['Jairzinho', 'Jair'],
    'maradona.jpeg': ['Diego Maradona', 'Maradona'],
    'mathaus.jpg': ['Lothar Matthäus', 'Matthaus', 'Mathaus'],
    'rivelino.jpg': ['Rivelino', 'Rivellino'],
    'ronaldinho.jpg': ['Ronaldinho Gaúcho', 'Ronaldinho'],
    'ronaldo.jpg': ['Ronaldo Nazário', 'Ronaldo'],
    'zidane.jpg': ['Zinedine Zidane', 'Zidane'],
}

def atualizar_imagens():
    """Atualiza as imagens dos jogadores usando arquivos do diretório media/jogadores/"""
    atualizados = 0
    nao_encontrados = 0
    sem_imagem = 0
    
    print("🖼️  Iniciando atualização de imagens dos jogadores...\n")
    
    # Caminho do diretório de imagens
    diretorio_imagens = os.path.join(settings.MEDIA_ROOT, 'jogadores')
    
    if not os.path.exists(diretorio_imagens):
        print(f"❌ Diretório '{diretorio_imagens}' não encontrado!")
        return
    
    for nome_arquivo, nomes_jogadores in mapeamento_imagens.items():
        caminho_imagem = os.path.join(diretorio_imagens, nome_arquivo)
        
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
            nao_encontrados += 1
            continue
        
        # Carregar e salvar a imagem
        try:
            with open(caminho_imagem, 'rb') as f:
                jogador.imagem.save(nome_arquivo, File(f), save=True)
            print(f"✅ Imagem atualizada para '{jogador.nome}' com '{nome_arquivo}'")
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

if __name__ == "__main__":
    atualizar_imagens()









