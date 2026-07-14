import os
import django

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'futebol_historico.settings')
django.setup()

from blog.models import Jogador

# Mapeamento de nomes de jogadores para arquivos de imagem
# Baseado nos arquivos disponíveis na pasta cartas_jogadores
mapeamento_imagens = {
    'Adriano Imperador': 'adriano.png',
    'Alex Del Piero': 'alex.png',
    'Roberto Baggio': 'Baggio.png',
    'Bebeto': 'bebeto.png',
    'Casagrande': 'casagrande.png',
    'Edgar Davids': 'Davids.png',
    'Deco': 'deco.png',
    'Didier Drogba': 'drogba.png',
    'Dunga': 'dunga.png',
    'Edmundo': 'edmundo.png',
    "Samuel Eto'o": 'Etoo.png',
    'Felipe': 'felipe.png',
    'Ruud Gullit': 'gullit.png',
    'Júlio César': 'julio_cesar.png',
    'Kaká': 'kaka.png',
    'Diego Maradona': 'maradona.png',
    'Pavel Nedvěd': 'Nedved.png',
    'Pelé': 'pele.png',
    'Raí': 'rai.png',
    'Frank Rijkaard': 'rijkaard.png',
    'Juan Román Riquelme': 'Riquelme.png',
    'Rivaldo': 'Rivaldo.png',
    'Romário': 'Romario.png',
    'Ronaldinho Gaúcho': 'Ronaldinho.png',
    'Ronaldo Nazário': 'Ronaldo.png',
    'Wesley Sneijder': 'sneider.png',
    'Cláudio Taffarel': 'tafarel.png',
    'Francesco Totti': 'Totti.png',
    'Marco van Basten': 'van_basten.png',
    'Zico': 'zico.png',
    'Zinedine Zidane': 'zidane.png',
}

def atualizar_cartas():
    """Atualiza as cartas dos jogadores com as imagens da pasta"""
    atualizados = 0
    nao_encontrados = 0
    sem_imagem = 0
    
    print("🖼️  Iniciando atualização de cartas dos jogadores...\n")
    
    for nome_jogador, nome_arquivo in mapeamento_imagens.items():
        # Buscar o jogador (case-insensitive)
        jogador = Jogador.objects.filter(nome__iexact=nome_jogador).first()
        
        if not jogador:
            print(f"⚠️  Jogador '{nome_jogador}' não encontrado no banco. Pulando...")
            nao_encontrados += 1
            continue
        
        # Caminho completo da imagem
        caminho_imagem = f'cartas_jogadores/{nome_arquivo}'
        
        # Verificar se o arquivo existe
        caminho_completo = os.path.join('media', caminho_imagem)
        if not os.path.exists(caminho_completo):
            print(f"⚠️  Arquivo '{nome_arquivo}' não encontrado para '{nome_jogador}'. Pulando...")
            sem_imagem += 1
            continue
        
        # Atualizar o campo carta do jogador
        jogador.carta = caminho_imagem
        jogador.save()
        
        print(f"✅ Carta de '{nome_jogador}' atualizada com '{nome_arquivo}'")
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

