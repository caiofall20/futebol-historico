#!/usr/bin/env python
"""
Script para corrigir as imagens dos jogadores para usar os arquivos que realmente existem no diretório
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'futebol_historico.settings')
django.setup()

from blog.models import Jogador
from django.core.files import File
from django.conf import settings

# Mapeamento de nomes de jogadores para arquivos que existem no diretório
mapeamento = {
    'Roberto Baggio': 'baggio.jpg',
    'Diego Maradona': 'maradona.jpeg',
    'Ronaldinho Gaúcho': 'ronaldinho.jpg',
    'Ronaldo Nazário': 'ronaldo.jpg',
    'Zinedine Zidane': 'zidane.jpg',
}

diretorio_jogadores = os.path.join(settings.MEDIA_ROOT, 'jogadores')

print("🖼️  Corrigindo imagens dos jogadores...\n")

for nome_jogador, nome_arquivo in mapeamento.items():
    try:
        jogador = Jogador.objects.get(nome=nome_jogador)
        caminho_imagem = os.path.join(diretorio_jogadores, nome_arquivo)
        
        if os.path.exists(caminho_imagem):
            # Abrir o arquivo e salvar no campo imagem
            with open(caminho_imagem, 'rb') as f:
                jogador.imagem.save(nome_arquivo, File(f), save=True)
            print(f"✅ {nome_jogador}: imagem atualizada com {nome_arquivo}")
        else:
            print(f"⚠️  {nome_jogador}: arquivo {nome_arquivo} não encontrado")
    except Jogador.DoesNotExist:
        print(f"❌ {nome_jogador}: jogador não encontrado no banco")
    except Exception as e:
        print(f"❌ {nome_jogador}: erro - {e}")

print("\n✅ Concluído!")









