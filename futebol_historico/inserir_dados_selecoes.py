from blog.models import Selecao
import os
from django.conf import settings
from django.core.wsgi import get_wsgi_application

# Configuração do Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "futebol_historico.settings")  # Substitua SEU_PROJETO pelo nome do seu projeto Django
django.setup()
# Dados detalhados das Seleções Históricas
selecoes = [
    {
        "nome": "EUA 1930",
        "descricao": "A surpreendente campanha dos Estados Unidos na primeira Copa do Mundo.",
        "historia": "A primeira Copa do Mundo da FIFA aconteceu no Uruguai em 1930. A seleção dos Estados Unidos, formada em sua maioria por jogadores amadores, surpreendeu ao vencer a Bélgica (3-0) e o Paraguai (3-0) na fase de grupos. Nas semifinais, enfrentaram a Argentina, mas perderam por 6-1, terminando em 3º lugar, um marco histórico para o futebol norte-americano. Bert Patenaude fez história ao marcar o primeiro hat-trick em Copas do Mundo.",
        "regiao": "América do Norte",
        "titulos": 0,
        "destaque": "Primeira seleção da América do Norte a chegar em uma semifinal de Copa.",
        "jogadores_iconicos": "Bert Patenaude, Tom Florie, Jimmy Douglas",
        "tecnico": "Robert Millar",
        "colocacao": "3º lugar"
    },
    {
        "nome": "Polônia 1974",
        "descricao": "Uma das melhores gerações polonesas que surpreendeu o mundo.",
        "historia": "Na Copa do Mundo de 1974, realizada na Alemanha Ocidental, a seleção da Polônia ficou marcada por seu futebol ofensivo e veloz. Com Grzegorz Lato como artilheiro (7 gols), a Polônia venceu grandes adversários como Argentina (3-2) e Suécia (1-0). Na semifinal, perdeu para a Alemanha Ocidental (1-0) em um campo encharcado, mas derrotou o Brasil por 1-0 na disputa pelo 3º lugar. Foi uma campanha histórica e colocou a Polônia no mapa do futebol mundial.",
        "regiao": "Europa",
        "titulos": 0,
        "destaque": "Grzegorz Lato terminou como artilheiro do torneio com 7 gols.",
        "jogadores_iconicos": "Grzegorz Lato, Kazimierz Deyna, Jan Tomaszewski",
        "tecnico": "Kazimierz Górski",
        "colocacao": "3º lugar"
    },
    {
        "nome": "Suécia 1958",
        "descricao": "O brilhante vice-campeonato da Suécia como anfitriã da Copa.",
        "historia": "A Copa do Mundo de 1958 foi disputada na Suécia, e a seleção anfitriã chegou à final de forma brilhante. Liderados por Gunnar Gren e Nils Liedholm, venceram a Alemanha Ocidental (3-1) nas semifinais. Na final, enfrentaram o Brasil de Pelé e Garrincha e perderam por 5-2, apesar do esforço dos jogadores. O torneio marcou a estreia internacional de Pelé, mas também o ápice do futebol sueco.",
        "regiao": "Europa",
        "titulos": 0,
        "destaque": "Disputa memorável contra o Brasil na final.",
        "jogadores_iconicos": "Gunnar Gren, Nils Liedholm, Agne Simonsson",
        "tecnico": "George Raynor",
        "colocacao": "2º lugar"
    },
    {
        "nome": "Nigéria 1998",
        "descricao": "A Nigéria surpreende com futebol rápido e técnico na França.",
        "historia": "A seleção da Nigéria chegou à Copa de 1998 com grande expectativa após boas atuações em 1994. No grupo da morte, venceu a Espanha por 3-2 em um jogo histórico e também a Bulgária (1-0). Apesar da classificação em primeiro no grupo, foi eliminada nas oitavas pela Dinamarca (4-1). Jay-Jay Okocha brilhou com dribles espetaculares e foi um dos nomes mais lembrados da competição.",
        "regiao": "África",
        "titulos": 0,
        "destaque": "Vitória histórica sobre a Espanha na fase de grupos.",
        "jogadores_iconicos": "Jay-Jay Okocha, Nwankwo Kanu, Sunday Oliseh",
        "tecnico": "Bora Milutinović",
        "colocacao": "Oitavas de final"
    },
    {
        "nome": "Alemanha 2014",
        "descricao": "O tetracampeonato alemão com atuação histórica no Brasil.",
        "historia": "A Alemanha conquistou o seu quarto título mundial na Copa do Mundo de 2014, realizada no Brasil. O time comandado por Joachim Löw marcou a competição com um futebol envolvente e ofensivo. Nas semifinais, protagonizaram um dos jogos mais icônicos da história ao vencerem o Brasil por 7-1. Na final, Mario Götze marcou o gol decisivo na prorrogação contra a Argentina, selando a vitória por 1-0 e garantindo o título.",
        "regiao": "Europa",
        "titulos": 4,
        "destaque": "Goleada histórica de 7-1 sobre o Brasil nas semifinais.",
        "jogadores_iconicos": "Thomas Müller, Miroslav Klose, Manuel Neuer",
        "tecnico": "Joachim Löw",
        "colocacao": "1º lugar"
    },
    {
        "nome": "Hungria 1954",
        "descricao": "Uma seleção lendária conhecida como 'Magiares Mágicos'.",
        "historia": "A Hungria, comandada por Ferenc Puskás, encantou o mundo na Copa do Mundo de 1954. Invicta até a final, a seleção goleou times como a Alemanha Ocidental (8-3 na fase de grupos) e o Brasil (4-2). Na final, enfrentaram novamente a Alemanha Ocidental, mas perderam por 3-2, em um dos jogos mais dramáticos da história do futebol. Apesar da derrota, o time ficou marcado pelo estilo ofensivo e inovador, sendo lembrado até hoje como um dos maiores times de todos os tempos.",
        "regiao": "Europa",
        "titulos": 0,
        "destaque": "Goleada histórica sobre a Alemanha Ocidental na fase de grupos (8-3).",
        "jogadores_iconicos": "Ferenc Puskás, Sándor Kocsis, József Bozsik",
        "tecnico": "Gusztáv Sebes",
        "colocacao": "2º lugar"
    }
]

# Atualizando os dados detalhados no banco
for selecao_data in selecoes:
    selecao = Selecao.objects.filter(nome=selecao_data["nome"]).first()
    if selecao:
        selecao.descricao = selecao_data["descricao"]
        selecao.historia = selecao_data["historia"]
        selecao.regiao = selecao_data["regiao"]
        selecao.titulos = selecao_data["titulos"]
        selecao.destaque = selecao_data["destaque"]
        selecao.jogadores_iconicos = selecao_data["jogadores_iconicos"]
        selecao.tecnico = selecao_data["tecnico"]
        selecao.colocacao = selecao_data["colocacao"]
        selecao.save()
        print(f"Seleção {selecao_data['nome']} atualizada com sucesso!")
    else:
        print(f"Seleção {selecao_data['nome']} não encontrada no banco.")

print("Atualização concluída com histórias detalhadas!")
