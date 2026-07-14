#!/usr/bin/env python
"""
Script para adicionar imagens manualmente na pasta e associar aos times
Uso: Coloque as imagens na pasta static/blog/images/times/ e execute este script
"""

import os
import sys
import django
from pathlib import Path
from django.core.files import File

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'futebol_historico.settings')
django.setup()

from blog.models import Time

# Caminho da pasta de imagens
IMAGES_PATH = Path(__file__).resolve().parent / 'blog' / 'static' / 'blog' / 'images' / 'times'

# Mapeamento manual: nome do arquivo -> nome do time no banco
# Você pode adicionar mais mapeamentos aqui
MANUAL_MAPPING = {
    'bayern_2013.jpg': 'Bayern de Munique 2013',
    'bayern_2020.jpg': 'Bayern de Munique 2020',
    'boca_2000.jpg': 'Boca Juniors 2000',
    'Boca_Juniors_2000.jpg': 'Boca Juniors 2000',
    'river_plate_1986.jpg': 'River Plate 1986',
    'river_1986.jpg': 'River Plate 1986',
    'real_madrid_1956.jpg': 'Real Madrid 1956-1960',
    'real_madrid_1956-1960.jpg': 'Real Madrid 1956-1960',
    'sao_paulo_1992.jpg': 'São Paulo 1992/1993',
    'sao paulo_1992.jpg': 'São Paulo 1992/1993',  # Com espaço
    'sao_paulo_1992-1993.jpg': 'São Paulo 1992/1993',
    # Exemplo:
    # 'nova_imagem_barcelona.jpg': 'Barcelona 2009',
    # 'nova_imagem_arsenal.jpg': 'Arsenal 2004',
}

def processar_imagens_na_pasta():
    """
    Processa todas as imagens na pasta e tenta associá-las aos times
    """
    print("="*70)
    print("ADICIONANDO IMAGENS DA PASTA AOS TIMES")
    print("="*70)
    print(f"\n📁 Pasta: {IMAGES_PATH}\n")
    
    if not IMAGES_PATH.exists():
        print(f"❌ Pasta não existe: {IMAGES_PATH}")
        return
    
    # Listar todas as imagens na pasta (incluindo arquivos com espaços)
    imagens = [f for f in IMAGES_PATH.iterdir() 
               if f.is_file() and f.suffix.lower() in ['.jpg', '.jpeg', '.png', '.webp']]
    
    if not imagens:
        print("⚠️  Nenhuma imagem encontrada na pasta!")
        return
    
    print(f"📸 Encontradas {len(imagens)} imagens na pasta\n")
    print("-"*70)
    
    sucesso = 0
    pulados = 0
    erros = 0
    
    for img_path in imagens:
        filename = img_path.name
        print(f"\n📄 Processando: {filename}")
        
        # Verificar se há mapeamento manual
        time_nome = MANUAL_MAPPING.get(filename)
        
        if not time_nome:
            # Tentar inferir o nome do time do nome do arquivo
            # Ex: "barcelona_2009.jpg" -> "Barcelona 2009"
            time_nome = inferir_nome_time(filename)
        
        if not time_nome:
            print(f"   ⚠️  Não foi possível identificar o time. Adicione ao MANUAL_MAPPING.")
            erros += 1
            continue
        
        try:
            time = Time.objects.get(nome=time_nome)
            
            # Verificar se já tem imagem
            if time.imagem and not '--forcar' in sys.argv:
                print(f"   ⚠️  {time_nome} já tem imagem. Use --forcar para substituir.")
                pulados += 1
                continue
            
            # Ler e salvar imagem
            with open(img_path, 'rb') as f:
                time.imagem.save(filename, File(f), save=True)
            
            print(f"   ✅ Associado a: {time_nome}")
            sucesso += 1
            
        except Time.DoesNotExist:
            print(f"   ❌ Time '{time_nome}' não encontrado no banco de dados")
            erros += 1
        except Exception as e:
            print(f"   ❌ Erro: {e}")
            erros += 1
    
    print("\n" + "="*70)
    print("✅ PROCESSO CONCLUÍDO!")
    print(f"   Sucesso: {sucesso}")
    print(f"   Pulados: {pulados}")
    print(f"   Erros: {erros}")
    print("="*70)

def inferir_nome_time(filename):
    """
    Tenta inferir o nome do time a partir do nome do arquivo
    """
    # Remover extensão
    name = filename.rsplit('.', 1)[0].lower()
    
    # Mapeamentos comuns (ordem importa - mais específicos primeiro)
    mapeamentos = [
        # Manchester United - mais específicos primeiro
        ('united_2008', 'Manchester United 2008'),
        ('united_1999', 'Manchester United 1999'),
        ('manchester_united_2008', 'Manchester United 2008'),
        ('manchester_united_1999', 'Manchester United 1999'),
        # Bayern - mais específicos primeiro
        ('bayern_2020', 'Bayern de Munique 2020'),
        ('bayern_2013', 'Bayern de Munique 2013'),
        # Ajax - mais específicos primeiro
        ('ajax_1971', 'Ajax 1971-1973'),
        ('ajax_1995', 'Ajax 1995'),
        # Outros times
        ('barcelona_2009', 'Barcelona 2009'),
        ('barcelona', 'Barcelona 2009'),
        ('arsenal_2004', 'Arsenal 2004'),
        ('arsenal', 'Arsenal 2004'),
        ('milan_1989', 'Milan 1989'),
        ('milan', 'Milan 1989'),
        ('ajax', 'Ajax 1995'),
        ('bayern', 'Bayern de Munique 2013'),
        ('flamengo_1981', 'Flamengo 1981'),
        ('flamengo', 'Flamengo 1981'),
        ('boca_juniors_2000', 'Boca Juniors 2000'),
        ('boca_2000', 'Boca Juniors 2000'),
        ('boca_juniors', 'Boca Juniors 2000'),
        ('boca', 'Boca Juniors 2000'),
        ('sao_paulo_1992', 'São Paulo 1992/1993'),
        ('sao_paulo', 'São Paulo 1992/1993'),
        ('river_plate_1986', 'River Plate 1986'),
        ('river_plate', 'River Plate 1986'),
        ('river', 'River Plate 1986'),
        ('porto_2004', 'Porto 2004'),
        ('porto', 'Porto 2004'),
        ('celtic_1967', 'Celtic 1967'),
        ('celtic', 'Celtic 1967'),
        ('penarol_1961', 'Peñarol 1961'),
        ('penarol', 'Peñarol 1961'),
        ('marseille_1993', 'Marseille 1993'),
        ('marseille', 'Marseille 1993'),
        ('inter_de_milao_2010', 'Internazionale 2010'),
        ('inter_2010', 'Internazionale 2010'),
        ('inter', 'Internazionale 2010'),
        ('united', 'Manchester United 1999'),  # Fallback genérico
        ('manchester_united', 'Manchester United 1999'),
        ('real_madrid_1956', 'Real Madrid 1956-1960'),
        ('real_madrid', 'Real Madrid 1956-1960'),
    ]
    
    # Procurar correspondência (ordem importa - mais específicos primeiro)
    for key, time_nome in mapeamentos:
        if key in name:
            return time_nome
    
    return None

if __name__ == '__main__':
    processar_imagens_na_pasta()

