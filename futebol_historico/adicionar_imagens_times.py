#!/usr/bin/env python
"""
Script para adicionar imagens reais dos times históricos
IMPORTANTE: Você precisa ter as imagens dos times baixadas localmente
ou fornecer URLs funcionais.

INSTRUÇÕES:
1. Baixe as fotos dos times históricos e coloque na pasta:
   futebol_historico/blog/static/blog/images/times/

2. Ou atualize o dicionário TEAM_IMAGES com URLs funcionais

3. Execute: python3 adicionar_imagens_times.py
"""

import os
import sys
import django
from pathlib import Path

# Configurar Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'futebol_historico.settings')
django.setup()

from django.core.files import File
from django.core.files.base import ContentFile
from blog.models import Time
import requests
from io import BytesIO

# Caminho local para imagens (prioridade)
IMAGES_LOCAL_PATH = Path(__file__).resolve().parent / 'blog' / 'static' / 'blog' / 'images' / 'times'

# Mapeamento de times para nomes de arquivos locais
# Coloque as imagens com estes nomes na pasta static/blog/images/times/
# Aceita variações de nomes (lista de possíveis nomes)
TEAM_LOCAL_IMAGES = {
    'Milan 1989': ['milan_1989.jpg', 'milan_1989.png'],
    'Barcelona 2009': ['barcelona_2009.jpg', 'barcelona_2009.png'],
    'Real Madrid 1956-1960': ['real_madrid_1956.jpg', 'real_madrid_1956.png'],
    'Manchester United 1999': ['manchester_united_1999.jpg', 'manchester_united_1999.png'],
    'Manchester United 2008': ['manchester_united_2008.jpg', 'manchester_united_2008.png'],
    'Arsenal 2004': ['arsenal_2004.jpg', 'arsenal_2004.png'],
    'Bayern de Munique 2013': ['bayern_2013.jpg', 'bayern_2013.png'],
    'Bayern de Munique 2020': ['bayern_2020.jpg', 'bayern_2020.png'],
    'Flamengo 1981': ['flamengo_1981.jpg', 'flamengo_1981.png'],
    'São Paulo 1992/1993': ['sao_paulo_1992.jpg', 'sao_paulo_1992.png'],
    'River Plate 1986': ['river_plate_1986.jpg', 'river_plate_1986.png'],
    'Boca Juniors 2000': ['boca_juniors_2000.jpg', 'boca_2000.jpg', 'boca_juniors_2000.png', 'boca_2000.png'],
    'Ajax 1995': ['ajax_1995.jpg', 'ajax_1995.png'],
    'Ajax 1971-1973': ['ajax_1971.jpg', 'ajax_1971.png'],
    'Marseille 1993': ['marseille_1993.jpg', 'marseille_1993.png'],
    'Porto 2004': ['porto_2004.jpg', 'porto_2004.png'],
    'Peñarol 1961': ['penarol_1961.jpg', 'penarol_1961.png'],
    'Celtic 1967': ['celtic_1967.jpg', 'celtic_1967.png'],
    'Internazionale 2010': ['inter_2010.jpg', 'inter_2010.png'],
}

# URLs alternativas (tentará baixar se não encontrar localmente)
# Você pode adicionar URLs funcionais aqui
TEAM_IMAGE_URLS = {
    # Exemplo - substitua com URLs reais que funcionem
    # 'Barcelona 2009': 'https://example.com/barcelona_2009.jpg',
}

def baixar_imagem_url(url, timeout=10):
    """Baixa uma imagem de uma URL"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return BytesIO(response.content)
    except Exception as e:
        print(f"   Erro ao baixar: {e}")
        return None

def atualizar_imagens_times(forcar=False):
    """Atualiza as imagens dos times com fotos dos elencos/equipes da época
    
    Args:
        forcar: Se True, substitui imagens existentes
    """
    print("=" * 60)
    print("ADICIONANDO IMAGENS DOS TIMES HISTÓRICOS")
    print("=" * 60)
    print(f"\n📁 Procurando imagens em: {IMAGES_LOCAL_PATH}")
    
    if not IMAGES_LOCAL_PATH.exists():
        print(f"⚠️  Pasta não existe! Criando: {IMAGES_LOCAL_PATH}")
        IMAGES_LOCAL_PATH.mkdir(parents=True, exist_ok=True)
    
    print("\n" + "=" * 60)
    
    sucesso = 0
    falhas = 0
    
    for team_name, local_filename in TEAM_LOCAL_IMAGES.items():
        try:
            time = Time.objects.get(nome=team_name)
            
            # Pular se já tiver imagem e não forçar
            if time.imagem and not forcar:
                print(f"⚠️  {team_name} já tem imagem, pulando...")
                continue
            
            if time.imagem and forcar:
                print(f"🔄 Substituindo imagem para {team_name}...")
            else:
                print(f"📥 Adicionando imagem para {team_name}...")
            
            image_data = None
            source = None
            found_filename = None
            
            # 1. Tentar arquivo local primeiro (aceita variações de nomes)
            # Se local_filename é uma lista, tentar cada variação
            possible_names = local_filename if isinstance(local_filename, list) else [local_filename]
            
            for filename_variant in possible_names:
                local_path = IMAGES_LOCAL_PATH / filename_variant
                if local_path.exists():
                    print(f"   ✅ Encontrado arquivo local: {filename_variant}")
                    with open(local_path, 'rb') as f:
                        image_data = BytesIO(f.read())
                    source = "local"
                    found_filename = filename_variant
                    break
            
            # 2. Se não encontrou local, tentar URL
            if not image_data and team_name in TEAM_IMAGE_URLS:
                print(f"   📡 Tentando baixar de URL...")
                url = TEAM_IMAGE_URLS[team_name]
                image_data = baixar_imagem_url(url)
                if image_data:
                    source = "url"
                    found_filename = url.split('/')[-1] or f"{team_name.replace(' ', '_')}.jpg"
            
            # 3. Se encontrou imagem, salvar
            if image_data:
                # Usar o nome do arquivo encontrado ou o primeiro da lista
                if found_filename:
                    base_filename = found_filename
                else:
                    # Fallback: usar primeiro nome da lista ou o nome original
                    if isinstance(local_filename, list):
                        base_filename = local_filename[0]
                    else:
                        base_filename = local_filename
                
                # Garantir extensão válida
                if not base_filename.endswith(('.png', '.jpg', '.jpeg', '.svg')):
                    base_filename = f"{base_filename}.jpg"
                
                # Limpar nome do arquivo para salvar no Django
                filename = f"{team_name.replace(' ', '_').replace('/', '_')}_{base_filename}"
                
                time.imagem.save(filename, File(image_data), save=True)
                print(f"   ✅ Imagem salva! ({source})")
                sucesso += 1
            else:
                print(f"   ❌ Nenhuma imagem encontrada")
                print(f"   💡 DICA: Coloque '{local_filename}' em {IMAGES_LOCAL_PATH}")
                falhas += 1
                
        except Time.DoesNotExist:
            print(f"⚠️  Time '{team_name}' não encontrado no banco de dados")
            falhas += 1
        except Exception as e:
            print(f"❌ Erro ao processar {team_name}: {e}")
            falhas += 1
    
    print("\n" + "=" * 60)
    print(f"✅ Processo concluído!")
    print(f"   Sucesso: {sucesso}")
    print(f"   Falhas: {falhas}")
    print("=" * 60)
    
    if falhas > 0:
        print("\n📋 INSTRUÇÕES PARA ADICIONAR IMAGENS FALTANTES:")
        print(f"   1. Baixe fotos dos times históricos")
        print(f"   2. Coloque na pasta: {IMAGES_LOCAL_PATH}")
        print(f"   3. Use os nomes sugeridos acima")
        print(f"   4. Execute novamente: python3 adicionar_imagens_times.py --forcar")

if __name__ == '__main__':
    import sys
    # Se passar --forcar como argumento, substitui imagens existentes
    forcar = '--forcar' in sys.argv or '-f' in sys.argv
    atualizar_imagens_times(forcar=forcar)
