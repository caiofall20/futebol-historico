#!/usr/bin/env python
"""
Script para baixar imagens dos times históricos do Pinterest e outras fontes
"""

import os
import sys
import django
from pathlib import Path
import requests
from io import BytesIO
from bs4 import BeautifulSoup
import re

# Configurar Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'futebol_historico.settings')
django.setup()

from django.core.files import File
from blog.models import Time

# Caminho para salvar imagens
IMAGES_PATH = Path(__file__).resolve().parent / 'blog' / 'static' / 'blog' / 'images' / 'times'
IMAGES_PATH.mkdir(parents=True, exist_ok=True)

# URLs do Pinterest e outras fontes para os times faltantes
# Formato: 'Nome do Time': ['url1', 'url2', ...]
TEAM_IMAGE_SOURCES = {
    'Milan 1989': [
        'https://i.pinimg.com/originals/...',  # Adicione URLs aqui
    ],
    'Real Madrid 1956-1960': [
        'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Real_Madrid_1957.jpg/800px-Real_Madrid_1957.jpg',
    ],
    'Manchester United 1999': [
        'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/Manchester_United_1998-99.jpg/800px-Manchester_United_1998-99.jpg',
    ],
    'Manchester United 2008': [
        'https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Manchester_United_2007-08.jpg/800px-Manchester_United_2007-08.jpg',
    ],
    'Flamengo 1981': [
        'https://upload.wikimedia.org/wikipedia/pt/thumb/6/6a/Flamengo_1981.jpg/800px-Flamengo_1981.jpg',
    ],
    'São Paulo 1992/1993': [
        'https://upload.wikimedia.org/wikipedia/pt/thumb/a/a4/Sao_Paulo_1992.jpg/800px-Sao_Paulo_1992.jpg',
    ],
    'River Plate 1986': [
        'https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/River_Plate_1986.jpg/800px-River_Plate_1986.jpg',
    ],
    'Boca Juniors 2000': [
        'https://br.pinterest.com/pin/293367363241863276/',
        'https://i.pinimg.com/originals/',
    ],
    'Marseille 1993': [
        'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/Olympique_Marseille_1992-93.jpg/800px-Olympique_Marseille_1992-93.jpg',
    ],
    'Porto 2004': [
        'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/FC_Porto_2003-04.jpg/800px-FC_Porto_2003-04.jpg',
    ],
    'Peñarol 1961': [
        'https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/Penarol_1961.jpg/800px-Penarol_1961.jpg',
    ],
    'Celtic 1967': [
        'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Celtic_1967.jpg/800px-Celtic_1967.jpg',
    ],
    'Internazionale 2010': [
        'https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Inter_Milan_2009-10.jpg/800px-Inter_Milan_2009-10.jpg',
    ],
}

def extrair_imagem_pinterest(url):
    """
    Tenta extrair a URL da imagem de um pin do Pinterest
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'Referer': 'https://www.pinterest.com/',
        }
        
        response = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        response.raise_for_status()
        
        html = response.text
        
        # Procurar por meta tags com imagem (og:image)
        meta_match = re.search(r'<meta\s+property=["\']og:image["\']\s+content=["\']([^"\']+)["\']', html)
        if meta_match:
            img_url = meta_match.group(1)
            print(f"   ✅ Encontrado em og:image: {img_url[:80]}...")
            return img_url
        
        # Procurar por URLs do pinimg.com no HTML
        pinimg_matches = re.findall(r'https?://[^"\s<>]+pinimg\.com[^"\s<>]+', html)
        if pinimg_matches:
            # Filtrar URLs de imagens grandes (não logos, ícones, etc)
            for match in pinimg_matches:
                match_clean = match.split('"')[0].split("'")[0].split(' ')[0].split('>')[0]
                # Ignorar logos, ícones pequenos, avatares
                if any(ignore in match_clean.lower() for ignore in ['logo', 'icon', 'avatar', 'webapp', '144x144', '60x60']):
                    continue
                # Procurar por imagens grandes (originais ou com dimensões grandes)
                if any(ext in match_clean.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp']) or 'originals' in match_clean.lower():
                    # Preferir originals (imagens grandes)
                    if 'originals' in match_clean.lower():
                        # Limpar URL - pegar apenas até o final da extensão
                        img_url = re.sub(r'\.(jpg|jpeg|png|webp).*$', r'.\1', match_clean, flags=re.IGNORECASE)
                        print(f"   ✅ Encontrado pinimg.com (original): {img_url[:80]}...")
                        return img_url
            
            # Se não encontrou originals, pegar a primeira imagem válida
            for match in pinimg_matches:
                match_clean = match.split('"')[0].split("'")[0].split(' ')[0].split('>')[0]
                if any(ignore in match_clean.lower() for ignore in ['logo', 'icon', 'avatar', 'webapp']):
                    continue
                if any(ext in match_clean.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp']):
                    img_url = match_clean
                    print(f"   ✅ Encontrado pinimg.com: {img_url[:80]}...")
                    return img_url
        
        # Tentar encontrar a imagem no HTML com BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        
        # Procurar por meta tags
        meta_image = soup.find('meta', property='og:image')
        if meta_image and meta_image.get('content'):
            return meta_image['content']
        
        # Procurar por img tags com src ou data-src
        img_tags = soup.find_all('img')
        for img in img_tags:
            for attr in ['src', 'data-src', 'data-lazy-src']:
                src = img.get(attr)
                if src and 'pinimg.com' in src:
                    if src.startswith('//'):
                        src = 'https:' + src
                    elif src.startswith('/'):
                        src = 'https://i.pinimg.com' + src
                    return src
        
        # Tentar encontrar em scripts JSON-LD
        scripts = soup.find_all('script', type='application/ld+json')
        for script in scripts:
            try:
                import json
                data = json.loads(script.string)
                if isinstance(data, dict) and 'image' in data:
                    return data['image']
            except:
                pass
        
        print(f"   ⚠️  Não foi possível encontrar URL da imagem no HTML")
        return None
    except Exception as e:
        print(f"   ⚠️  Erro ao extrair imagem do Pinterest: {e}")
        return None

def baixar_imagem(url, timeout=15):
    """
    Baixa uma imagem de uma URL
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
            'Referer': 'https://www.pinterest.com/',
        }
        
        # Se for URL do Pinterest, tentar extrair a imagem
        if 'pinterest.com' in url or 'pinimg.com' in url:
            if '/pin/' in url:
                print(f"   🔍 Extraindo imagem do Pinterest...")
                image_url = extrair_imagem_pinterest(url)
                if image_url:
                    url = image_url
                    print(f"   ✅ URL da imagem encontrada: {url[:80]}...")
                else:
                    print(f"   ⚠️  Não foi possível extrair imagem do Pinterest")
                    return None
        
        response = requests.get(url, headers=headers, timeout=timeout, stream=True, allow_redirects=True)
        response.raise_for_status()
        
        # Verificar se é realmente uma imagem
        content_type = response.headers.get('content-type', '')
        if not content_type.startswith('image/'):
            print(f"   ⚠️  URL não é uma imagem (Content-Type: {content_type})")
            return None
        
        return BytesIO(response.content)
    except Exception as e:
        print(f"   ❌ Erro ao baixar: {e}")
        return None

def processar_time(team_name, urls):
    """
    Processa um time, tentando baixar de múltiplas URLs
    """
    print(f"\n{'='*60}")
    print(f"📥 Processando: {team_name}")
    print(f"{'='*60}")
    
    for i, url in enumerate(urls, 1):
        print(f"\n   Tentativa {i}/{len(urls)}: {url[:80]}...")
        
        image_data = baixar_imagem(url)
        
        if image_data:
            # Salvar localmente
            filename = f"{team_name.replace(' ', '_').replace('/', '_')}.jpg"
            filepath = IMAGES_PATH / filename
            
            with open(filepath, 'wb') as f:
                f.write(image_data.getvalue())
            
            print(f"   ✅ Imagem salva: {filename}")
            print(f"   📁 Local: {filepath}")
            
            # Também atualizar no banco de dados se o time existir
            try:
                time = Time.objects.get(nome=team_name)
                time.imagem.save(filename, File(image_data), save=True)
                print(f"   ✅ Atualizado no banco de dados!")
            except Time.DoesNotExist:
                print(f"   ⚠️  Time '{team_name}' não encontrado no banco")
            except Exception as e:
                print(f"   ⚠️  Erro ao atualizar banco: {e}")
            
            return True
    
    print(f"\n   ❌ Não foi possível baixar imagem para {team_name}")
    return False

def main():
    print("="*60)
    print("BAIXADOR DE IMAGENS DOS TIMES HISTÓRICOS")
    print("="*60)
    print(f"\n📁 Imagens serão salvas em: {IMAGES_PATH}\n")
    
    sucesso = 0
    falhas = 0
    
    for team_name, urls in TEAM_IMAGE_SOURCES.items():
        if processar_time(team_name, urls):
            sucesso += 1
        else:
            falhas += 1
    
    print("\n" + "="*60)
    print("✅ PROCESSO CONCLUÍDO!")
    print(f"   Sucesso: {sucesso}")
    print(f"   Falhas: {falhas}")
    print("="*60)

if __name__ == '__main__':
    main()

