import os
import django
from datetime import date

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'futebol_historico.settings')
django.setup()

from blog.models import Jogador

# Lista de jogadores para cadastrar
jogadores_lista = [
    'Adriano Imperador',
    'Alex Del Piero',
    'Roberto Baggio',
    'Bebeto',
    'Casagrande',
    'Edgar Davids',
    'Deco',
    'Didier Drogba',
    'Dunga',
    'Edmundo',
    "Samuel Eto'o",
    'Felipe',
    'Ruud Gullit',
    'Júlio César',
    'Kaká',
    'Diego Maradona',
    'Pavel Nedvěd',
    'Pelé',
    'Raí',
    'Frank Rijkaard',
    'Juan Román Riquelme',
    'Rivaldo',
    'Romário',
    'Ronaldinho Gaúcho',
    'Ronaldo Nazário',
    'Wesley Sneijder',
    'Cláudio Taffarel',
    'Francesco Totti',
    'Marco van Basten',
    'Zico',
    'Zinedine Zidane',
]

# Mapeamento de nacionalidades (baseado nos jogadores conhecidos)
nacionalidades_map = {
    'Adriano Imperador': 'Brasil',
    'Alex Del Piero': 'Itália',
    'Roberto Baggio': 'Itália',
    'Bebeto': 'Brasil',
    'Casagrande': 'Brasil',
    'Edgar Davids': 'Holanda',
    'Deco': 'Brasil',
    'Didier Drogba': 'Costa do Marfim',
    'Dunga': 'Brasil',
    'Edmundo': 'Brasil',
    "Samuel Eto'o": 'Camarões',
    'Felipe': 'Brasil',
    'Ruud Gullit': 'Holanda',
    'Júlio César': 'Brasil',
    'Kaká': 'Brasil',
    'Diego Maradona': 'Argentina',
    'Pavel Nedvěd': 'República Tcheca',
    'Pelé': 'Brasil',
    'Raí': 'Brasil',
    'Frank Rijkaard': 'Holanda',
    'Juan Román Riquelme': 'Argentina',
    'Rivaldo': 'Brasil',
    'Romário': 'Brasil',
    'Ronaldinho Gaúcho': 'Brasil',
    'Ronaldo Nazário': 'Brasil',
    'Wesley Sneijder': 'Holanda',
    'Cláudio Taffarel': 'Brasil',
    'Francesco Totti': 'Itália',
    'Marco van Basten': 'Holanda',
    'Zico': 'Brasil',
    'Zinedine Zidane': 'França',
}

def cadastrar_jogadores():
    """Cadastra os jogadores da lista, evitando duplicatas"""
    cadastrados = 0
    ja_existentes = 0
    
    for nome_jogador in jogadores_lista:
        # Verificar se o jogador já existe (busca case-insensitive)
        jogador_existente = Jogador.objects.filter(nome__iexact=nome_jogador).first()
        
        if jogador_existente:
            print(f"⚠️  Jogador '{nome_jogador}' já está cadastrado. Pulando...")
            ja_existentes += 1
            continue
        
        # Obter nacionalidade do mapeamento ou usar padrão
        nacionalidade = nacionalidades_map.get(nome_jogador, 'Desconhecida')
        
        # Criar o jogador com campos mínimos
        # Imagem será deixada vazia para inserção manual posterior
        jogador = Jogador.objects.create(
            nome=nome_jogador,
            nacionalidade=nacionalidade,
            inicio_carreira=date(1900, 1, 1),  # Data padrão
            fim_carreira=date(2000, 1, 1),  # Data padrão
            # imagem será None (vazio)
            # biografia será None (vazio)
            # carta será None (vazio)
        )
        
        print(f"✅ Jogador '{nome_jogador}' cadastrado com sucesso! (Nacionalidade: {nacionalidade})")
        cadastrados += 1
    
    print("\n" + "="*50)
    print(f"📊 Resumo:")
    print(f"   ✅ Cadastrados: {cadastrados}")
    print(f"   ⚠️  Já existentes: {ja_existentes}")
    print(f"   📝 Total na lista: {len(jogadores_lista)}")
    print("="*50)

if __name__ == "__main__":
    print("🚀 Iniciando cadastro de jogadores...\n")
    cadastrar_jogadores()
    print("\n✨ Processo concluído!")

