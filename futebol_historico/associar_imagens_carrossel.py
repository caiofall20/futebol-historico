import os
import django
from django.conf import settings

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'futebol_historico.settings')
django.setup()

from blog.models import Jogador

# Mapeamento de nomes de arquivos para nomes de jogadores
MAPEAMENTO_IMAGENS = {
    'beckham.jpg': 'David Beckham',
    'henry.png': 'Thierry Henry',
    'kaka.jpg': 'Kaká',
    'maradona.jpeg': 'Diego Maradona',
    'mathaus.jpg': 'Lothar Matthäus',  # Pode precisar ajustar o nome
    'messi.jpg': 'Lionel Messi',
    'ronaldinho.jpg': 'Ronaldinho Gaúcho',
    'ronaldo.jpg': 'Ronaldo Nazário',
    'rooney.jpg': 'Wayne Rooney',
    'zidane.jpg': 'Zinedine Zidane',
    'zmessi_chuteira.jpg': 'Lionel Messi',  # Duplicata do Messi
}

def associar_imagens_carrossel():
    """Associa as imagens da pasta carrossel_jogadores aos jogadores correspondentes"""
    carrossel_path = os.path.join(settings.MEDIA_ROOT, 'carrossel_jogadores')
    
    if not os.path.exists(carrossel_path):
        print(f"❌ Pasta não encontrada: {carrossel_path}")
        return
    
    arquivos = [f for f in os.listdir(carrossel_path) 
                if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
    
    print(f"📁 Encontrados {len(arquivos)} arquivos na pasta carrossel_jogadores\n")
    
    atualizados = 0
    nao_encontrados = 0
    ja_preenchidos = 0
    
    for arquivo in arquivos:
        nome_jogador = MAPEAMENTO_IMAGENS.get(arquivo)
        
        if not nome_jogador:
            # Tentar encontrar por similaridade no nome do arquivo
            nome_sem_ext = os.path.splitext(arquivo)[0].lower()
            jogador = None
            
            # Buscar jogadores que possam corresponder
            for j in Jogador.objects.all():
                nome_j_lower = j.nome.lower()
                # Verificar se o nome do arquivo contém parte do nome do jogador ou vice-versa
                if nome_sem_ext in nome_j_lower or nome_j_lower.replace(' ', '') in nome_sem_ext.replace('_', ''):
                    jogador = j
                    nome_jogador = j.nome
                    break
            
            if not jogador:
                print(f"⚠️  Não encontrado mapeamento para: {arquivo}")
                nao_encontrados += 1
                continue
        
        # Buscar o jogador
        jogador = Jogador.objects.filter(nome__iexact=nome_jogador).first()
        
        if not jogador:
            print(f"⚠️  Jogador '{nome_jogador}' não encontrado no banco para: {arquivo}")
            nao_encontrados += 1
            continue
        
        # Verificar se já tem imagem_carrossel
        if jogador.imagem_carrossel:
            print(f"⏭️  {jogador.nome} já tem imagem_carrossel: {jogador.imagem_carrossel.name}")
            ja_preenchidos += 1
            continue
        
        # Associar a imagem
        caminho_imagem = f'carrossel_jogadores/{arquivo}'
        jogador.imagem_carrossel = caminho_imagem
        jogador.save()
        
        print(f"✅ {jogador.nome} -> {arquivo}")
        atualizados += 1
    
    print("\n" + "="*60)
    print(f"📊 Resumo:")
    print(f"   ✅ Atualizados: {atualizados}")
    print(f"   ⏭️  Já preenchidos: {ja_preenchidos}")
    print(f"   ⚠️  Não encontrados: {nao_encontrados}")
    print("="*60)

if __name__ == "__main__":
    associar_imagens_carrossel()
    print("\n✨ Processo concluído!")




