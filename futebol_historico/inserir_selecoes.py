import os
from django.conf import settings
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'futebol_historico.settings')
application = get_wsgi_application()

from blog.models import Selecao

# Lista de seleções históricas
selecoes_historicas = [
    {
        "nome": "Alemanha 2014",
        "imagem": "alemanha2014.jpg",
        "regiao": "Europa",
        "descricao": "A Alemanha de 2014 é lembrada pelo futebol coletivo e técnico, culminando em um histórico 7x1 contra o Brasil nas semifinais da Copa do Mundo.",
        "destaque": "Futebol coletivo e técnico, culminando em um histórico 7x1 contra o Brasil.",
        "jogadores_iconicos": "Miroslav Klose, Thomas Müller, Toni Kroos, Manuel Neuer.",
        "colocacao": "1º lugar",
        "tecnico": "Joachim Löw"
    },
    {
        "nome": "Argentina 1986",
        "imagem": "argentina86.jpg",
        "regiao": "América do Sul",
        "descricao": "A Copa de Diego Maradona, com o famoso 'gol do século' e a 'mão de Deus'.",
        "destaque": "A Copa de Diego Maradona, com o famoso 'gol do século' e a 'mão de Deus'.",
        "jogadores_iconicos": "Diego Maradona, Jorge Valdano, Oscar Ruggeri.",
        "colocacao": "1º lugar",
        "tecnico": "Carlos Bilardo"
    },
    {
        "nome": "Bélgica 2018",
        "imagem": "belgica2018.jpg",
        "regiao": "Europa",
        "descricao": "Futebol ofensivo e técnico, terminando em 3º lugar na Copa do Mundo de 2018.",
        "destaque": "Futebol ofensivo e técnico, terminando em 3º lugar.",
        "jogadores_iconicos": "Eden Hazard, Kevin De Bruyne, Romelu Lukaku, Thibaut Courtois.",
        "colocacao": "3º lugar",
        "tecnico": "Roberto Martínez"
    },
    {
        "nome": "Brasil 1970",
        "imagem": "brasil70.jpg",
        "regiao": "América do Sul",
        "descricao": "Time considerado por muitos como o melhor da história do futebol, com um futebol ofensivo, técnico e com um entrosamento incomparável.",
        "destaque": "Time considerado por muitos como o melhor da história do futebol.",
        "jogadores_iconicos": "Pelé, Jairzinho, Tostão, Rivelino e Carlos Alberto Torres.",
        "colocacao": "1º lugar",
        "tecnico": "Mário Zagallo"
    },
    {
        "nome": "Croácia 1998",
        "imagem": "croacia98.jpg",
        "regiao": "Europa",
        "descricao": "Surpresa ao chegar ao 3º lugar em sua primeira Copa do Mundo.",
        "destaque": "Surpresa ao chegar ao 3º lugar em sua primeira Copa do Mundo.",
        "jogadores_iconicos": "Davor Šuker (artilheiro do torneio), Zvonimir Boban.",
        "colocacao": "3º lugar",
        "tecnico": "Miroslav Blažević"
    },
    {
        "nome": "França 1998",
        "imagem": "franca98.jpg",
        "regiao": "Europa",
        "descricao": "Primeiro título da França, vencendo o Brasil por 3x0 na final.",
        "destaque": "Primeiro título da França, vencendo o Brasil por 3x0 na final.",
        "jogadores_iconicos": "Zinedine Zidane, Thierry Henry, Didier Deschamps, Laurent Blanc.",
        "colocacao": "1º lugar",
        "tecnico": "Aimé Jacquet"
    },
    {
        "nome": "Holanda 1974",
        "imagem": "holanda74.jpg",
        "regiao": "Europa",
        "descricao": "Revolucionou o futebol com o 'Futebol Total'.",
        "destaque": "Revolucionou o futebol com o 'Futebol Total'.",
        "jogadores_iconicos": "Johan Cruyff, Johan Neeskens, Ruud Krol.",
        "colocacao": "2º lugar",
        "tecnico": "Rinus Michels"
    },
    {
        "nome": "Hungria 1954",
        "imagem": "hungria54.jpg",
        "regiao": "Europa",
        "descricao": "'Os Mágicos Magiares', uma das melhores seleções a não vencer uma Copa.",
        "destaque": "'Os Mágicos Magiares', uma das melhores seleções a não vencer uma Copa.",
        "jogadores_iconicos": "Ferenc Puskás, Sándor Kocsis.",
        "colocacao": "2º lugar",
        "tecnico": "Gusztáv Sebes"
    },
    {
        "nome": "Itália 2006",
        "imagem": "italia2006.jpg",
        "regiao": "Europa",
        "descricao": "Defesa sólida liderada por Fabio Cannavaro e Gianluigi Buffon, conquistando o título nos pênaltis contra a França na final.",
        "destaque": "Defesa sólida liderada por Fabio Cannavaro e Gianluigi Buffon.",
        "jogadores_iconicos": "Francesco Totti, Andrea Pirlo, Gennaro Gattuso e Alessandro Del Piero.",
        "colocacao": "1º lugar",
        "tecnico": "Marcello Lippi"
    },
    {
        "nome": "Portugal 1966",
        "imagem": "portugal66.jpg",
        "regiao": "Europa",
        "descricao": "Liderados por Eusébio, terminaram em 3º lugar.",
        "destaque": "Liderados por Eusébio, terminaram em 3º lugar.",
        "jogadores_iconicos": "Eusébio, Coluna, Simões.",
        "colocacao": "3º lugar",
        "tecnico": "Otto Glória"
    },
    {
        "nome": "Rússia 2008 (Eurocopa)",
        "imagem": "russia2008.jpg",
        "regiao": "Europa",
        "descricao": "Embora não seja de Copa do Mundo, o time de Andrey Arshavin encantou na Eurocopa.",
        "destaque": "Embora não seja de Copa do Mundo, o time de Andrey Arshavin encantou na Eurocopa.",
        "jogadores_iconicos": "Andrey Arshavin, Roman Pavlyuchenko, Yuri Zhirkov.",
        "colocacao": "Semifinalista",
        "tecnico": "Guus Hiddink"
    },
    {
        "nome": "Uruguai 1950",
        "imagem": "uruguai50.jpg",
        "regiao": "América do Sul",
        "descricao": "O 'Maracanazo', com a vitória sobre o Brasil na final.",
        "destaque": "O 'Maracanazo', com a vitória sobre o Brasil na final.",
        "jogadores_iconicos": "Alcides Ghiggia, Juan Alberto Schiaffino.",
        "colocacao": "1º lugar",
        "tecnico": "Juan López Fontana"
    },
    {
        "nome": "Senegal 2002",
        "imagem": "senegal2002.jpg",
        "regiao": "África",
        "descricao": "Surpresa ao chegar às quartas de final em sua estreia em Copas.",
        "destaque": "Surpresa ao chegar às quartas de final em sua estreia em Copas.",
        "jogadores_iconicos": "El Hadji Diouf, Papa Bouba Diop.",
        "colocacao": "Quartas de final",
        "tecnico": "Bruno Metsu"
    },
    {
        "nome": "Camarões 1990",
        "imagem": "camaroes1990.jpg",
        "regiao": "África",
        "descricao": "Primeiro time africano a chegar às quartas de final.",
        "destaque": "Primeiro time africano a chegar às quartas de final.",
        "jogadores_iconicos": "Roger Milla, François Omam-Biyik.",
        "colocacao": "Quartas de final",
        "tecnico": "Valeri Nepomniachi"
    },
    {
        "nome": "Coreia do Sul 2002",
        "imagem": "coreiadoSul2002.jpg",
        "regiao": "Ásia",
        "descricao": "Semi-finalistas jogando em casa, surpreendendo o mundo.",
        "destaque": "Semi-finalistas jogando em casa, surpreendendo o mundo.",
        "jogadores_iconicos": "Park Ji-sung, Ahn Jung-hwan.",
        "colocacao": "4º lugar",
        "tecnico": "Guus Hiddink"
    },
    {
        "nome": "Colômbia 2014",
        "imagem": "colombia2014.jpg",
        "regiao": "América do Sul",
        "descricao": "Futebol técnico e emocionante, com James Rodríguez como destaque.",
        "destaque": "Futebol técnico e emocionante, com James Rodríguez como destaque.",
        "jogadores_iconicos": "James Rodríguez, Juan Cuadrado, Radamel Falcao (não jogou a Copa, mas era referência).",
        "colocacao": "Quartas de final",
        "tecnico": "José Pékerman"
    },
    {
        "nome": "Nigéria 1994",
        "imagem": "nigeria1994.jpg",
        "regiao": "África",
        "descricao": "Time vibrante que encantou nas oitavas de final.",
        "destaque": "Time vibrante que encantou nas oitavas de final.",
        "jogadores_iconicos": "Jay-Jay Okocha, Rashidi Yekini.",
        "colocacao": "Oitavas de final",
        "tecnico": "Clemens Westerhof"
    },
    {
        "nome": "Áustria 1934",
        "imagem": "austria1934.jpg",
        "regiao": "Europa",
        "descricao": "Time chamado de 'Wunderteam', foi semifinalista e encantou o mundo.",
        "destaque": "Time chamado de 'Wunderteam', foi semifinalista e encantou o mundo.",
        "jogadores_iconicos": "Matthias Sindelar, Josef Bican.",
        "colocacao": "Semifinalista",
        "tecnico": "Hugo Meisl"
    },
    {
        "nome": "Tchecoslováquia 1962",
        "imagem": "tchecoslovquia1962.jpg",
        "regiao": "Europa",
        "descricao": "Vice-campeões, perderam para o Brasil na final.",
        "destaque": "Vice-campeões, perderam para o Brasil na final.",
        "jogadores_iconicos": "Josef Masopust (Ballon d'Or 1962).",
        "colocacao": "2º lugar",
        "tecnico": "Rudolf Vytlačil"
    },
    {
        "nome": "Suécia 1958",
        "imagem": "suecia1958.jpg",
        "regiao": "Europa",
        "descricao": "Vice-campeões jogando em casa, perdendo para o Brasil de Pelé.",
        "destaque": "Vice-campeões jogando em casa, perdendo para o Brasil de Pelé.",
        "jogadores_iconicos": "Gunnar Gren, Nils Liedholm.",
        "colocacao": "2º lugar",
        "tecnico": "George Raynor"
    },
    {
        "nome": "Polônia 1974",
        "imagem": "polonia1974.jpg",
        "regiao": "Europa",
        "descricao": "Surpresa da Copa, terminando em 3º lugar.",
        "destaque": "Surpresa da Copa, terminando em 3º lugar.",
        "jogadores_iconicos": "Grzegorz Lato (artilheiro), Kazimierz Deyna.",
        "colocacao": "3º lugar",
        "tecnico": "Kazimierz Górski"
    },
    {
        "nome": "Dinamarca 1986",
        "imagem": "dinamarca1986.jpg",
        "regiao": "Europa",
        "descricao": "Time apelidado de 'Dinamáquina', jogou futebol ofensivo, mas caiu nas oitavas.",
        "destaque": "Time apelidado de 'Dinamáquina', jogou futebol ofensivo, mas caiu nas oitavas.",
        "jogadores_iconicos": "Preben Elkjær, Michael Laudrup.",
        "colocacao": "Oitavas de final",
        "tecnico": "Sepp Piontek"
    },
    {
        "nome": "Bulgária 1994",
        "imagem": "bulgaria1994.jpg",
        "regiao": "Europa",
        "descricao": "Surpresa ao chegar às semifinais, eliminando a Alemanha.",
        "destaque": "Surpresa ao chegar às semifinais, eliminando a Alemanha.",
        "jogadores_iconicos": "Hristo Stoichkov, Yordan Letchkov.",
        "colocacao": "4º lugar",
        "tecnico": "Dimitar Penev"
    },
    {
        "nome": "Gana 2010",
        "imagem": "gana2010.jpg",
        "regiao": "África",
        "descricao": "Chegou às quartas de final e quase se tornou a primeira semifinalista africana.",
        "destaque": "Chegou às quartas de final e quase se tornou a primeira semifinalista africana.",
        "jogadores_iconicos": "Asamoah Gyan, Kevin-Prince Boateng.",
        "colocacao": "Quartas de final",
        "tecnico": "Milovan Rajevac"
    },
    {
        "nome": "México 1986",
        "imagem": "mexico1986.jpg",
        "regiao": "América do Norte",
        "descricao": "Chegaram às quartas de final jogando em casa, liderados por Hugo Sánchez.",
        "destaque": "Chegaram às quartas de final jogando em casa, liderados por Hugo Sánchez.",
        "jogadores_iconicos": "Hugo Sánchez, Manuel Negrete.",
        "colocacao": "Quartas de final",
        "tecnico": "Bora Milutinović"
    },
    {
        "nome": "Colômbia 1990",
        "imagem": "colombia1990.jpg",
        "regiao": "América do Sul",
        "descricao": "Estilo ofensivo e futebol alegre.",
        "destaque": "Estilo ofensivo e futebol alegre.",
        "jogadores_iconicos": "Carlos Valderrama, René Higuita.",
        "colocacao": "Oitavas de final",
        "tecnico": "Francisco Maturana"
    },
    {
        "nome": "Nigéria 1998",
        "imagem": "nigeria1998.jpg",
        "regiao": "África",
        "descricao": "Time vibrante e ofensivo, surpreendendo nas fases de grupos.",
        "destaque": "Time vibrante e ofensivo, surpreendendo nas fases de grupos.",
        "jogadores_iconicos": "Jay-Jay Okocha, Nwankwo Kanu.",
        "colocacao": "Oitavas de final",
        "tecnico": "Bora Milutinović"
    },
    {
        "nome": "Turquia 2002",
        "imagem": "turquia2002.jpg",
        "regiao": "Ásia",
        "descricao": "Surpresa ao terminar em 3º lugar, derrotando a Coreia do Sul.",
        "destaque": "Surpresa ao terminar em 3º lugar, derrotando a Coreia do Sul.",
        "jogadores_iconicos": "Hakan Şükür, Hasan Şaş.",
        "colocacao": "3º lugar",
        "tecnico": "Şenol Güneş"
    },
    {
        "nome": "Marrocos 2022",
        "imagem": "marrocos2022.jpg",
        "regiao": "África",
        "descricao": "Primeira seleção africana a chegar às semifinais.",
        "destaque": "Primeira seleção africana a chegar às semifinais.",
        "jogadores_iconicos": "Hakim Ziyech, Sofyan Amrabat.",
        "colocacao": "4º lugar",
        "tecnico": "Walid Regragui"
    },
    {
        "nome": "EUA 1930",
        "imagem": "estadosunidos1930.jpg",
        "regiao": "América do Norte",
        "descricao": "Chegaram às semifinais na primeira Copa.",
        "destaque": "Chegaram às semifinais na primeira Copa.",
        "jogadores_iconicos": "Bert Patenaude (primeiro hat-trick em Copas).",
        "colocacao": "Semifinalista",
        "tecnico": "Robert Millar"
    },
    {
        "nome": "Austrália 2006",
        "imagem": "australia2006.jpg",
        "regiao": "Oceania",
        "descricao": "Chegou às oitavas pela primeira vez, com futebol surpreendente.",
        "destaque": "Chegou às oitavas pela primeira vez, com futebol surpreendente.",
        "jogadores_iconicos": "Tim Cahill, Mark Viduka.",
        "colocacao": "Oitavas de final",
        "tecnico": "Guus Hiddink"
    }
    # Adicione mais seleções conforme necessário
]

# Inserir seleções no banco de dados
for selecao in selecoes_historicas:
    Selecao.objects.update_or_create(
        nome=selecao["nome"],
        defaults={
            "imagem": selecao["imagem"],
            "regiao": selecao["regiao"],
            "descricao": selecao["descricao"],
            "destaque": selecao["destaque"],
            "jogadores_iconicos": selecao["jogadores_iconicos"],
            "colocacao": selecao["colocacao"],
            "tecnico": selecao["tecnico"]
        }
    )
    print(f"Seleção {selecao['nome']} inserida ou atualizada com sucesso.")
