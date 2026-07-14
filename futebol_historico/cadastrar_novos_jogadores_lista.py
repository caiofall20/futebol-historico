import os
import django
from datetime import date

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'futebol_historico.settings')
django.setup()

from blog.models import Jogador

# Lista de jogadores para cadastrar
JOGADORES_NOVOS = [
    'Andriy Shevchenko',
    'Alessandro Del Piero',
    'Gennaro Gattuso',
    'Dennis Bergkamp',
    'Andrey Arshavin',
    'Paolo Maldini',
    'Fernando Hierro',
    'Jaap Stam',
    'Frank de Boer',
    'Javier Zanetti',
    'Aldair',
    'Matthias Sammer',
    'Cafú',
    'Jürgen Klinsmann',
    'Diego Maradona',
    'Claudio López',
    'Freddie Ljungberg',
    'Filippo Inzaghi',
    'Raúl González',
    'Fernando Morientes',
    'Ruud van Nistelrooy',
    'Patrick Kluivert',
    'Rui Costa',
    'Michael Laudrup',
    'Jay-Jay Okocha',
    'Lothar Matthäus',
    'Roy Keane',
    'Demetrio Albertini',
    'Youri Djorkaeff',
    'Juan Román Riquelme',
    'Fernando Redondo',
    'Juan Sebastián Verón',
    'Ole Gunnar Solskjær',
]

# Mapeamento de nacionalidades (alguns jogadores podem precisar de ajuste)
NACIONALIDADES_MAP = {
    'Andriy Shevchenko': 'Ucrânia',
    'Alessandro Del Piero': 'Itália',
    'Gennaro Gattuso': 'Itália',
    'Dennis Bergkamp': 'Holanda',
    'Andrey Arshavin': 'Rússia',
    'Paolo Maldini': 'Itália',
    'Fernando Hierro': 'Espanha',
    'Jaap Stam': 'Holanda',
    'Frank de Boer': 'Holanda',
    'Javier Zanetti': 'Argentina',
    'Aldair': 'Brasil',
    'Matthias Sammer': 'Alemanha',
    'Cafú': 'Brasil',
    'Jürgen Klinsmann': 'Alemanha',
    'Diego Maradona': 'Argentina',
    'Claudio López': 'Argentina',
    'Freddie Ljungberg': 'Suécia',
    'Filippo Inzaghi': 'Itália',
    'Raúl González': 'Espanha',
    'Fernando Morientes': 'Espanha',
    'Ruud van Nistelrooy': 'Holanda',
    'Patrick Kluivert': 'Holanda',
    'Rui Costa': 'Portugal',
    'Michael Laudrup': 'Dinamarca',
    'Jay-Jay Okocha': 'Nigéria',
    'Lothar Matthäus': 'Alemanha',
    'Roy Keane': 'Irlanda',
    'Demetrio Albertini': 'Itália',
    'Youri Djorkaeff': 'França',
    'Juan Román Riquelme': 'Argentina',
    'Fernando Redondo': 'Argentina',
    'Juan Sebastián Verón': 'Argentina',
    'Ole Gunnar Solskjær': 'Noruega',
}

def cadastrar_jogadores():
    """Cadastra os jogadores da lista, evitando duplicatas"""
    cadastrados = 0
    ja_existentes = 0
    erros = 0
    
    print("🚀 Iniciando cadastro de jogadores...\n")
    
    for nome_jogador in JOGADORES_NOVOS:
        # Verificar se o jogador já existe (busca case-insensitive)
        jogador_existente = Jogador.objects.filter(nome__iexact=nome_jogador).first()
        
        if jogador_existente:
            print(f"⏭️  Jogador '{nome_jogador}' já está cadastrado. Pulando...")
            ja_existentes += 1
            continue
        
        try:
            # Obter nacionalidade do mapeamento ou usar padrão
            nacionalidade = NACIONALIDADES_MAP.get(nome_jogador, 'Desconhecida')
            
            # Criar o jogador com campos mínimos
            jogador = Jogador.objects.create(
                nome=nome_jogador,
                nacionalidade=nacionalidade,
                inicio_carreira=date(1900, 1, 1),  # Data padrão
                fim_carreira=date(2000, 1, 1),  # Data padrão
                # imagem, imagem_carrossel, carta, biografia, carreira serão None (vazios)
            )
            
            print(f"✅ Jogador '{nome_jogador}' cadastrado com sucesso! (Nacionalidade: {nacionalidade})")
            cadastrados += 1
            
        except Exception as e:
            print(f"❌ Erro ao cadastrar '{nome_jogador}': {e}")
            erros += 1
    
    print("\n" + "="*60)
    print(f"📊 Resumo:")
    print(f"   ✅ Cadastrados: {cadastrados}")
    print(f"   ⏭️  Já existentes: {ja_existentes}")
    print(f"   ❌ Erros: {erros}")
    print(f"   📝 Total na lista: {len(JOGADORES_NOVOS)}")
    print("="*60)

if __name__ == "__main__":
    cadastrar_jogadores()
    print("\n✨ Processo concluído!")




