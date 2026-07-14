#!/usr/bin/env python
"""
Script para criar novos jogadores e associar suas imagens
"""
import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'futebol_historico.settings')
django.setup()

from blog.models import Jogador
from django.core.files import File
from django.conf import settings

# Dados dos novos jogadores
novos_jogadores = [
    {
        'nome': 'Roberto Carlos',
        'nacionalidade': 'Brasil',
        'inicio_carreira': date(1991, 1, 1),
        'fim_carreira': date(2012, 12, 31),
        'imagem': 'roberto_carlos.jpg',
    },
    {
        'nome': 'Cristiano Ronaldo',
        'nacionalidade': 'Portugal',
        'inicio_carreira': date(2002, 1, 1),
        'fim_carreira': date(2024, 12, 31),
        'imagem': 'cr7.jpg',
    },
    {
        'nome': 'Lionel Messi',
        'nacionalidade': 'Argentina',
        'inicio_carreira': date(2004, 1, 1),
        'fim_carreira': date(2024, 12, 31),
        'imagem': 'messi.jpg',
    },
    {
        'nome': 'David Beckham',
        'nacionalidade': 'Inglaterra',
        'inicio_carreira': date(1992, 1, 1),
        'fim_carreira': date(2013, 5, 18),
        'imagem': 'beckham.jpg',
    },
    {
        'nome': 'Wayne Rooney',
        'nacionalidade': 'Inglaterra',
        'inicio_carreira': date(2002, 8, 17),
        'fim_carreira': date(2021, 1, 15),
        'imagem': 'rooney.jpg',
    },
    {
        'nome': 'Mesut Özil',
        'nacionalidade': 'Alemanha',
        'inicio_carreira': date(2006, 1, 1),
        'fim_carreira': date(2023, 3, 22),
        'imagem': 'ozil.jpg',
    },
]

diretorio_jogadores = os.path.join(settings.MEDIA_ROOT, 'jogadores')

print("🚀 Criando novos jogadores e associando imagens...\n")

criados = 0
atualizados = 0
erros = 0

for jogador_data in novos_jogadores:
    nome = jogador_data['nome']
    nome_arquivo = jogador_data['imagem']
    caminho_imagem = os.path.join(diretorio_jogadores, nome_arquivo)
    
    # Verificar se o jogador já existe
    jogador_existente = Jogador.objects.filter(nome__iexact=nome).first()
    
    if jogador_existente:
        print(f"⚠️  Jogador '{nome}' já existe. Atualizando imagem...")
        jogador = jogador_existente
        atualizados += 1
    else:
        # Criar novo jogador
        jogador = Jogador.objects.create(
            nome=nome,
            nacionalidade=jogador_data['nacionalidade'],
            inicio_carreira=jogador_data['inicio_carreira'],
            fim_carreira=jogador_data['fim_carreira'],
        )
        print(f"✅ Jogador '{nome}' criado.")
        criados += 1
    
    # Associar a imagem
    if os.path.exists(caminho_imagem):
        try:
            with open(caminho_imagem, 'rb') as f:
                jogador.imagem.save(nome_arquivo, File(f), save=True)
            print(f"   📸 Imagem '{nome_arquivo}' associada com sucesso!")
        except Exception as e:
            print(f"   ❌ Erro ao associar imagem: {e}")
            erros += 1
    else:
        print(f"   ⚠️  Arquivo '{nome_arquivo}' não encontrado em {caminho_imagem}")

print("\n" + "="*50)
print(f"📊 Resumo:")
print(f"   ✅ Criados: {criados}")
print(f"   🔄 Atualizados: {atualizados}")
print(f"   ❌ Erros: {erros}")
print("="*50)









