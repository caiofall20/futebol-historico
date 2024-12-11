from blog.models import Jogador

# Mapeamento de jogadores e suas imagens
imagens = {
    'Roberto Baggio': 'cartas_jogadores/Baggio.png',
    'Edgar Davids': 'cartas_jogadores/Davids.png',
    'Samuel Etoo': 'cartas_jogadores/Etoo.png',
    'Kaká': 'cartas_jogadores/kaka.png',
    'Diego Maradona': 'cartas_jogadores/maradona.png',
    'Pavel Nedved': 'cartas_jogadores/Nedved.png',
    'Juan Román Riquelme': 'cartas_jogadores/Riquelme.png',
    'Rivaldo': 'cartas_jogadores/Rivaldo.png',
    'Romário': 'cartas_jogadores/Romario.png',
    'Ronaldinho Gaúcho': 'cartas_jogadores/Ronaldinho.png',
    'Ronaldo Nazário': 'cartas_jogadores/Ronaldo.png',
    'Francesco Totti': 'cartas_jogadores/Totti.png',
    'Zinedine Zidane': 'cartas_jogadores/zidane.png'
}

for nome, imagem in imagens.items():
    jogador = Jogador.objects.get(nome=nome)
    jogador.imagem = imagem
    jogador.save()
    print(f"Imagem atualizada para o jogador {nome}!")
