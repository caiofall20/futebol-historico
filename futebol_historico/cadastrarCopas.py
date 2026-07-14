import os
import django

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'futebol_historico.settings')
django.setup()

from blog.models import Copa

copas_data = [
    {
        "nome": "Copa do Mundo FIFA",
        "ano": 1930,
        "pais": "Uruguai",
        "continente": "AS",
        "descricao": "A primeira Copa do Mundo FIFA, realizada no Uruguai, marcou o início de uma das maiores competições esportivas do planeta.",
        "historia": "A Copa do Mundo de 1930 foi a primeira edição do torneio, realizada no Uruguai. Contou com 13 seleções convidadas, divididas em quatro grupos. O Uruguai, país-sede, venceu a Argentina na final por 4x2, em uma partida disputada no Estádio Centenário, diante de 93 mil torcedores. Os Estados Unidos ficaram em terceiro lugar.",
        "campeao": "Uruguai",
        "vice_campeao": "Argentina",
        "terceiro_lugar": "Estados Unidos",
        "imagem": "copa_1930.jpg"
    },
    {
        "nome": "Copa do Mundo FIFA",
        "ano": 1950,
        "pais": "Brasil",
        "continente": "AS",
        "descricao": "A Copa do Mundo de 1950 no Brasil ficou marcada pelo dramático Maracanazo, quando o Uruguai venceu o Brasil na final no Maracanã.",
        "historia": "A Copa de 1950 foi realizada no Brasil e ficou marcada pelo Maracanazo, a derrota brasileira para o Uruguai na decisiva partida final por 2x1. O torneio contou com 13 seleções e não teve uma final oficial, mas sim um quadrangular final, com o jogo decisivo entre Brasil e Uruguai. Suécia ficou com o terceiro lugar.",
        "campeao": "Uruguai",
        "vice_campeao": "Brasil",
        "terceiro_lugar": "Suécia",
        "imagem": "copa_1950.jpg"
    },
    {
        "nome": "Copa do Mundo FIFA",
        "ano": 1958,
        "pais": "Suécia",
        "continente": "EU",
        "descricao": "A Copa de 1958 na Suécia revelou ao mundo o jovem Pelé e o primeiro título mundial do Brasil.",
        "historia": "A Copa do Mundo de 1958 foi disputada na Suécia e revelou o jovem Pelé, que marcou gols decisivos para o Brasil conquistar seu primeiro título mundial. O Brasil venceu a Suécia por 5x2 na final, em Estocolmo. A França, liderada por Just Fontaine, terminou em terceiro lugar.",
        "campeao": "Brasil",
        "vice_campeao": "Suécia",
        "terceiro_lugar": "França",
        "imagem": "copa_1958.jpg"
    },
    {
        "nome": "Copa do Mundo FIFA",
        "ano": 1962,
        "pais": "Chile",
        "continente": "AS",
        "descricao": "O Brasil conquista seu segundo título mundial consecutivo, desta vez no Chile.",
        "historia": "Liderado por Garrincha, o Brasil venceu sua segunda Copa do Mundo consecutiva no Chile, mesmo sem Pelé em boa parte do torneio. Na final, a seleção brasileira derrotou a Tchecoslováquia por 3x1. O Chile, anfitrião, terminou em terceiro lugar.",
        "campeao": "Brasil",
        "vice_campeao": "Tchecoslováquia",
        "terceiro_lugar": "Chile",
        "imagem": "copa_1962.jpg"
    },
    {
        "nome": "Copa do Mundo FIFA",
        "ano": 1966,
        "pais": "Inglaterra",
        "continente": "EU",
        "descricao": "A Inglaterra conquista seu primeiro e único título mundial em casa.",
        "historia": "A Copa do Mundo de 1966 foi disputada na Inglaterra e marcada por controvérsias, como o gol fantasma na final entre Inglaterra e Alemanha Ocidental. Geoff Hurst marcou três gols na final, vencida pelos ingleses por 4x2. Portugal, liderado por Eusébio, terminou em terceiro lugar.",
        "campeao": "Inglaterra",
        "vice_campeao": "Alemanha Ocidental",
        "terceiro_lugar": "Portugal",
        "imagem": "copa_1966.jpg"
    },
    {
        "nome": "Copa do Mundo FIFA",
        "ano": 1970,
        "pais": "México",
        "continente": "AN",
        "descricao": "O Brasil conquista seu terceiro título mundial com a melhor seleção de todos os tempos.",
        "historia": "Considerada a melhor seleção de todos os tempos, o Brasil venceu a Copa de 1970 de forma incontestável. Liderados por Pelé, Gérson, Rivelino e Tostão, derrotaram a Itália por 4x1 na final. A Alemanha Ocidental ficou em terceiro lugar.",
        "campeao": "Brasil",
        "vice_campeao": "Itália",
        "terceiro_lugar": "Alemanha Ocidental",
        "imagem": "copa_1970.jpg"
    },
    {
        "nome": "Copa do Mundo FIFA",
        "ano": 1986,
        "pais": "México",
        "continente": "AN",
        "descricao": "Maradona conduz a Argentina ao título com jogadas históricas.",
        "historia": "A Copa de 1986 foi dominada por Maradona, que marcou o gol da 'Mão de Deus' e o 'Gol do Século' contra a Inglaterra. A Argentina venceu a Alemanha Ocidental por 3x2 na final, enquanto a França terminou em terceiro lugar.",
        "campeao": "Argentina",
        "vice_campeao": "Alemanha Ocidental",
        "terceiro_lugar": "França",
        "imagem": "copa_1986.jpg"
    },
    {
        "nome": "Copa do Mundo FIFA",
        "ano": 1998,
        "pais": "França",
        "continente": "EU",
        "descricao": "A França conquista seu primeiro título mundial em casa.",
        "historia": "Com Zidane brilhando na final, a França venceu o Brasil por 3x0 e conquistou seu primeiro título mundial. O torneio contou com a participação de 32 seleções pela primeira vez. A Croácia terminou em terceiro lugar.",
        "campeao": "França",
        "vice_campeao": "Brasil",
        "terceiro_lugar": "Croácia",
        "imagem": "copa_1998.jpg"
    },
    {
        "nome": "Copa do Mundo FIFA",
        "ano": 2002,
        "pais": "Coreia do Sul/Japão",
        "continente": "ASI",
        "descricao": "O Brasil conquista seu quinto título mundial no primeiro Mundial realizado na Ásia.",
        "historia": "A Copa de 2002 foi a primeira realizada em dois países e no continente asiático. Liderados por Ronaldo, Rivaldo e Ronaldinho, o Brasil venceu a Alemanha por 2x0 na final, conquistando o pentacampeonato. A Turquia ficou em terceiro lugar.",
        "campeao": "Brasil",
        "vice_campeao": "Alemanha",
        "terceiro_lugar": "Turquia"
        "imagem": "copa_2002.jpg"
    },
    {
        "nome": "Copa do Mundo FIFA",
        "ano": 2014,
        "pais": "Brasil",
        "continente": "AS",
        "descricao": "A Alemanha conquista seu quarto título mundial em território brasileiro.",
        "historia": "A Copa de 2014 no Brasil foi marcada pelo famoso 7x1 da Alemanha sobre os anfitriões na semifinal. Na final, a Alemanha venceu a Argentina por 1x0, conquistando seu quarto título. A Holanda terminou em terceiro lugar.",
        "campeao": "Alemanha",
        "vice_campeao": "Argentina",
        "terceiro_lugar": "Holanda",
        "imagem": "copa_2014.jpg"
    },
    {
        "nome": "Copa do Mundo FIFA",
        "ano": 2018,
        "pais": "Rússia",
        "continente": "EU",
        "descricao": "A França conquista seu segundo título mundial com atuações brilhantes.",
        "historia": "A Copa do Mundo de 2018, realizada na Rússia, foi marcada pelo domínio da França, liderada por jogadores como Mbappé e Griezmann. A França venceu a Croácia por 4x2 na final, tornando-se bicampeã mundial. A Bélgica ficou em terceiro lugar após vencer a Inglaterra.",
        "campeao": "França",
        "vice_campeao": "Croácia",
        "terceiro_lugar": "Bélgica",
        "imagem": "copa_2018.jpg"
    },
    {
        "nome": "Copa do Mundo FIFA",
        "ano": 2022,
        "pais": "Catar",
        "continente": "ASI",
        "descricao": "A Argentina vence sua terceira Copa em um torneio histórico no Catar.",
        "historia": "A Copa do Mundo de 2022 foi marcada por momentos históricos, com Lionel Messi liderando a Argentina para conquistar seu terceiro título mundial. Na final, a Argentina derrotou a França nos pênaltis após um empate emocionante por 3x3 no tempo normal e prorrogação. A Croácia terminou em terceiro lugar ao vencer o Marrocos.",
        "campeao": "Argentina",
        "vice_campeao": "França",
        "terceiro_lugar": "Croácia",
        "imagem": "copa_2022.jpg"
    }
]

def inserir_copas():
    for copa_info in copas_data:
        try:
            copa = Copa.objects.create(
                nome=copa_info['nome'],
                ano=copa_info['ano'],
                pais=copa_info['pais'],
                continente=copa_info['continente'],
                descricao=copa_info['descricao'],
                historia=copa_info['historia'],
                campeao=copa_info['campeao'],
                vice_campeao=copa_info['vice_campeao'],
                terceiro_lugar=copa_info['terceiro_lugar']
            )
            print(f"Copa {copa.nome} ({copa.ano}) inserida com sucesso!")
        except Exception as e:
            print(f"Erro ao inserir Copa {copa_info['nome']} ({copa_info['ano']}): {e}")

if __name__ == "__main__":
    inserir_copas()
