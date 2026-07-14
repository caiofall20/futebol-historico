import os
import django
from django.core.files import File
from django.conf import settings

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'futebol_historico.settings')
django.setup()

from blog.models import Jogador

# Mapeamento de nomes de jogadores para arquivos de imagem
mapeamento_imagens = {
    'Paul Scholes': 'scholes.png',
    'Ryan Giggs': 'giggs.png',
    'Rio Ferdinand': 'ferdinand.png',
    'Eric Cantona': 'cantona.png',
    'Edwin van der Sar': 'van_der_sar.png',
}

def atualizar_cartas():
    """Atualiza as cartas dos jogadores com as imagens da pasta"""
    atualizados = 0
    nao_encontrados = 0
    sem_imagem = 0
    
    print("🖼️  Iniciando atualização de cartas dos jogadores...\n")
    
    for nome_jogador, nome_arquivo in mapeamento_imagens.items():
        # Buscar o jogador pelo nome exato (case-insensitive)
        jogador = Jogador.objects.filter(nome__iexact=nome_jogador).first()
        
        # Se não encontrou, tentar busca por partes do nome (mas mais específica)
        if not jogador:
            # Para van der Sar, buscar especificamente
            if 'van der Sar' in nome_jogador:
                jogador = Jogador.objects.filter(nome__icontains='van der Sar').first()
            elif 'Rio Ferdinand' in nome_jogador:
                jogador = Jogador.objects.filter(nome__icontains='Rio').filter(nome__icontains='Ferdinand').first()
            elif 'Paul Scholes' in nome_jogador:
                jogador = Jogador.objects.filter(nome__icontains='Paul').filter(nome__icontains='Scholes').first()
            elif 'Ryan Giggs' in nome_jogador:
                jogador = Jogador.objects.filter(nome__icontains='Ryan').filter(nome__icontains='Giggs').first()
            elif 'Eric Cantona' in nome_jogador:
                jogador = Jogador.objects.filter(nome__icontains='Eric').filter(nome__icontains='Cantona').first()
        
        if not jogador:
            print(f"⚠️  Jogador '{nome_jogador}' não encontrado no banco. Pulando...")
            nao_encontrados += 1
            continue
        
        # Caminho completo da imagem
        caminho_imagem = os.path.join(settings.MEDIA_ROOT, 'cartas_jogadores', nome_arquivo)
        
        # Verificar se o arquivo existe
        if not os.path.exists(caminho_imagem):
            print(f"⚠️  Arquivo '{nome_arquivo}' não encontrado para '{nome_jogador}' em {caminho_imagem}. Pulando...")
            sem_imagem += 1
            continue
        
        # Atualizar o campo carta do jogador usando File()
        with open(caminho_imagem, 'rb') as f:
            jogador.carta.save(nome_arquivo, File(f), save=True)
        
        print(f"✅ Carta de '{jogador.nome}' atualizada com '{nome_arquivo}'")
        atualizados += 1
    
    print("\n" + "="*50)
    print(f"📊 Resumo:")
    print(f"   ✅ Atualizados: {atualizados}")
    print(f"   ⚠️  Jogadores não encontrados: {nao_encontrados}")
    print(f"   ⚠️  Imagens não encontradas: {sem_imagem}")
    print("="*50)

if __name__ == "__main__":
    atualizar_cartas()
    print("\n✨ Processo concluído!")

