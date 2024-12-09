from datetime import datetime
from django.utils import timezone
from .models import Time
from django.core.files import File
from pathlib import Path
import os

def create_initial_times():
    times_data = [
        {
            'nome': 'Seleção Brasileira 2002',
            'descricao': '''<p>A Seleção Brasileira de 2002 é considerada uma das maiores equipes da história do futebol. 
            Com jogadores como Ronaldo, Rivaldo, Ronaldinho Gaúcho, Roberto Carlos e Cafu, o Brasil conquistou seu 
            quinto título mundial na Copa do Mundo de 2002, realizada na Coreia do Sul e no Japão. A equipe venceu 
            todos os jogos da competição, com Ronaldo sendo o artilheiro do torneio.</p>''',
            'fundacao': datetime(2002, 1, 1),
            'titulos': 1,
            'regiao': 'América do Sul'
        },
        {
            'nome': 'Milan 2007',
            'descricao': '''<p>O Milan de 2007 foi uma das equipes mais dominantes da Europa. Com um elenco estrelado 
            que incluía Kaká, Andrea Pirlo, Clarence Seedorf, Paolo Maldini e outros grandes nomes, o time conquistou 
            a Liga dos Campeões da UEFA em 2007, derrotando o Liverpool na final. Esta equipe é lembrada por seu 
            futebol técnico e elegante.</p>''',
            'fundacao': datetime(2007, 1, 1),
            'titulos': 7,
            'regiao': 'Europa'
        },
        {
            'nome': 'Barcelona 2006',
            'descricao': '''<p>O Barcelona de 2006, liderado por Ronaldinho Gaúcho no auge de sua carreira, foi uma das 
            equipes mais espetaculares da história do clube. Com jogadores como Samuel Eto'o, Deco, Xavi e Puyol, 
            o time conquistou a Liga dos Campeões da UEFA e demonstrou um futebol ofensivo e envolvente que 
            encantou o mundo.</p>''',
            'fundacao': datetime(2006, 1, 1),
            'titulos': 5,
            'regiao': 'Europa'
        },
        {
            'nome': 'Real Madrid 2017',
            'descricao': '''<p>O Real Madrid de 2017 foi uma das equipes mais dominantes da história recente do futebol. 
            Liderado por Cristiano Ronaldo e com jogadores como Sergio Ramos, Luka Modric, Toni Kroos e Karim Benzema, 
            o time conquistou a Liga dos Campeões e demonstrou um futebol eficiente e decisivo.</p>''',
            'fundacao': datetime(2017, 1, 1),
            'titulos': 13,
            'regiao': 'Europa'
        },
        {
            'nome': 'Santos 1962',
            'descricao': '''<p>O Santos de 1962, com o lendário Pelé, é considerado um dos maiores times de todos os tempos. 
            A equipe conquistou todos os títulos possíveis naquele ano, incluindo o Campeonato Paulista, o Campeonato 
            Brasileiro (Taça Brasil), a Copa Libertadores e o Mundial Interclubes.</p>''',
            'fundacao': datetime(1962, 1, 1),
            'titulos': 6,
            'regiao': 'América do Sul'
        }
    ]

    for time_data in times_data:
        Time.objects.get_or_create(
            nome=time_data['nome'],
            defaults={
                'descricao': time_data['descricao'],
                'fundacao': time_data['fundacao'],
                'titulos': time_data['titulos'],
                'regiao': time_data['regiao']
            }
        )

def create_historical_teams():
    """Cria os times históricos do futebol mundial"""
    
    times_data = [
        # Itália
        {
            'nome': 'Milan 1989',
            'descricao': '''<p>O Milan de 1989 foi um time lendário comandado por Arrigo Sacchi, que revolucionou o futebol italiano 
            e europeu. Com o trio holandês formado por Marco van Basten, Ruud Gullit e Frank Rijkaard, além de uma defesa 
            impenetrável com Baresi e Maldini, o time conquistou a Liga dos Campeões e estabeleceu novos padrões táticos 
            no futebol mundial.</p>''',
            'fundacao': datetime(1989, 1, 1),
            'titulos': 7,
            'regiao': 'Europa'
        },
        # Espanha
        {
            'nome': 'Barcelona 2009',
            'descricao': '''<p>O Barcelona de 2009, conhecido como "Pep Team", foi uma das equipes mais dominantes da história. 
            Sob o comando de Pep Guardiola, e com o trio mágico formado por Messi, Xavi e Iniesta, o time conquistou todos 
            os títulos possíveis em 2009, incluindo La Liga, Copa del Rey e Champions League, jogando um futebol revolucionário 
            baseado na posse de bola e pressão alta.</p>''',
            'fundacao': datetime(2009, 1, 1),
            'titulos': 6,
            'regiao': 'Europa'
        },
        {
            'nome': 'Real Madrid 1956-1960',
            'descricao': '''<p>O Real Madrid de 1956-1960 é considerado um dos maiores times de todos os tempos. Esta equipe 
            conquistou as cinco primeiras edições da Copa dos Campeões da Europa (atual Champions League), façanha jamais 
            igualada. Liderado por Alfredo Di Stéfano e Ferenc Puskás, o time revolucionou o futebol europeu com seu estilo 
            ofensivo e técnico.</p>''',
            'fundacao': datetime(1956, 1, 1),
            'titulos': 5,
            'regiao': 'Europa'
        },
        # Inglaterra
        {
            'nome': 'Manchester United 1999',
            'descricao': '''<p>O Manchester United de 1999, sob o comando de Sir Alex Ferguson, conquistou a histórica tríplice 
            coroa (Premier League, FA Cup e Champions League). Com jogadores como Peter Schmeichel, Roy Keane, David Beckham 
            e os atacantes Andy Cole e Dwight Yorke, o time ficou marcado pela dramática virada sobre o Bayern de Munique 
            na final da Champions League.</p>''',
            'fundacao': datetime(1999, 1, 1),
            'titulos': 3,
            'regiao': 'Europa'
        },
        {
            'nome': 'Manchester United 2008',
            'descricao': '''<p>O Manchester United de 2008 reuniu um dos ataques mais letais da história do clube, com 
            Cristiano Ronaldo, Wayne Rooney e Carlos Tevez. Sob o comando de Sir Alex Ferguson, a equipe conquistou a 
            Champions League em uma final histórica contra o Chelsea, além da Premier League, jogando um futebol ofensivo 
            e envolvente.</p>''',
            'fundacao': datetime(2008, 1, 1),
            'titulos': 3,
            'regiao': 'Europa'
        },
        {
            'nome': 'Arsenal 2004',
            'descricao': '''<p>O Arsenal de 2004, conhecido como "The Invincibles", entrou para a história como o único time 
            a conquistar a Premier League de forma invicta na era moderna. Liderado por Arsène Wenger e com estrelas como 
            Thierry Henry, Patrick Vieira e Dennis Bergkamp, o time combinou futebol ofensivo com solidez defensiva.</p>''',
            'fundacao': datetime(2004, 1, 1),
            'titulos': 3,
            'regiao': 'Europa'
        },
        # Alemanha
        {
            'nome': 'Bayern de Munique 2013',
            'descricao': '''<p>O Bayern de Munique de 2013, sob o comando de Jupp Heynckes, conquistou uma histórica tríplice 
            coroa (Bundesliga, Copa da Alemanha e Champions League). Com um elenco estrelado que incluía Ribéry, Robben, 
            Schweinsteiger e Lahm, o time dominou o futebol europeu com um estilo de jogo intenso e ofensivo.</p>''',
            'fundacao': datetime(2013, 1, 1),
            'titulos': 5,
            'regiao': 'Europa'
        },
        {
            'nome': 'Bayern de Munique 2020',
            'descricao': '''<p>O Bayern de 2020 foi uma máquina de vitórias que conquistou a Champions League de forma invicta. 
            Liderado por Robert Lewandowski, que viveu sua melhor temporada, e com jogadores como Thomas Müller e Joshua 
            Kimmich, o time venceu todos os títulos possíveis jogando um futebol avassalador.</p>''',
            'fundacao': datetime(2020, 1, 1),
            'titulos': 6,
            'regiao': 'Europa'
        },
        # Brasil
        {
            'nome': 'Flamengo 1981',
            'descricao': '''<p>O Flamengo de 1981 é considerado um dos maiores times da história do futebol brasileiro. 
            Liderado pelo craque Zico, conquistou a Libertadores e o Mundial Interclubes contra o Liverpool. O time 
            praticava um futebol ofensivo e envolvente, com jogadores como Júnior, Andrade e Nunes.</p>''',
            'fundacao': datetime(1981, 1, 1),
            'titulos': 4,
            'regiao': 'América do Sul'
        },
        {
            'nome': 'São Paulo 1992/1993',
            'descricao': '''<p>O São Paulo de 1992/1993, comandado pelo lendário Telê Santana, conquistou dois títulos 
            consecutivos da Libertadores e Mundial. Com um estilo de jogo baseado na posse de bola e toques rápidos, 
            o time contava com craques como Raí, Müller e Cafú.</p>''',
            'fundacao': datetime(1992, 1, 1),
            'titulos': 5,
            'regiao': 'América do Sul'
        },
        # Argentina
        {
            'nome': 'River Plate 1986',
            'descricao': '''<p>O River Plate de 1986 conquistou a Libertadores e a Copa Intercontinental com um futebol 
            envolvente. Liderado pelo craque Enzo Francescoli, o time praticava um futebol ofensivo e técnico, 
            característico do futebol argentino.</p>''',
            'fundacao': datetime(1986, 1, 1),
            'titulos': 3,
            'regiao': 'América do Sul'
        },
        {
            'nome': 'Boca Juniors 2000',
            'descricao': '''<p>O Boca Juniors de 2000 foi um dos times mais vitoriosos da história do clube. Conquistou 
            a Libertadores e a Copa Intercontinental contra o Real Madrid, com um futebol aguerrido e eficiente. O time 
            contava com jogadores como Martín Palermo e Juan Román Riquelme.</p>''',
            'fundacao': datetime(2000, 1, 1),
            'titulos': 4,
            'regiao': 'América do Sul'
        },
        # Holanda
        {
            'nome': 'Ajax 1995',
            'descricao': '''<p>O Ajax de 1995, comandado por Louis van Gaal, surpreendeu o mundo ao conquistar a Champions 
            League de forma invicta. Com um time jovem que incluía futuros craques como Clarence Seedorf, Edgar Davids 
            e Patrick Kluivert, praticava um futebol total, seguindo a tradição holandesa.</p>''',
            'fundacao': datetime(1995, 1, 1),
            'titulos': 4,
            'regiao': 'Europa'
        },
        {
            'nome': 'Ajax 1971-1973',
            'descricao': '''<p>O Ajax de 1971-1973 revolucionou o futebol mundial com o "Futebol Total". Liderado por 
            Johan Cruyff, o time conquistou três Champions League consecutivas, apresentando ao mundo um novo estilo 
            de jogo onde todos os jogadores atacavam e defendiam.</p>''',
            'fundacao': datetime(1971, 1, 1),
            'titulos': 3,
            'regiao': 'Europa'
        },
        # França
        {
            'nome': 'Marseille 1993',
            'descricao': '''<p>O Marseille de 1993 entrou para a história como o primeiro time francês a conquistar a 
            Champions League. Com jogadores como Didier Deschamps, Fabien Barthez e Rudi Völler, o time combinou 
            técnica e força física característica do futebol francês.</p>''',
            'fundacao': datetime(1993, 1, 1),
            'titulos': 2,
            'regiao': 'Europa'
        },
        # Portugal
        {
            'nome': 'Porto 2004',
            'descricao': '''<p>O Porto de 2004, sob o comando de José Mourinho, surpreendeu a Europa ao conquistar a 
            Champions League. Com um futebol pragmático e eficiente, liderado por Deco no meio-campo, o time eliminou 
            grandes favoritos no caminho do título.</p>''',
            'fundacao': datetime(2004, 1, 1),
            'titulos': 3,
            'regiao': 'Europa'
        },
        # Uruguai
        {
            'nome': 'Peñarol 1961',
            'descricao': '''<p>O Peñarol de 1961 foi um dos times mais marcantes da história do futebol sul-americano. 
            Conquistou a Libertadores e a Copa Intercontinental com um estilo de jogo característico do futebol uruguaio, 
            combinando técnica e garra.</p>''',
            'fundacao': datetime(1961, 1, 1),
            'titulos': 3,
            'regiao': 'América do Sul'
        },
        # Outros Notáveis
        {
            'nome': 'Celtic 1967',
            'descricao': '''<p>O Celtic de 1967, conhecido como "Lisbon Lions", fez história ao se tornar o primeiro time 
            britânico a conquistar a Champions League. Com um time formado inteiramente por jogadores nascidos num raio 
            de 50 km de Glasgow, venceu a poderosa Internazionale de Milão na final.</p>''',
            'fundacao': datetime(1967, 1, 1),
            'titulos': 2,
            'regiao': 'Europa'
        },
        {
            'nome': 'Internazionale 2010',
            'descricao': '''<p>A Internazionale de 2010, sob o comando de José Mourinho, conquistou uma histórica tríplice 
            coroa (Serie A, Copa da Itália e Champions League). Com um futebol pragmático e uma defesa sólida, o time 
            contava com jogadores como Wesley Sneijder, Diego Milito e Samuel Eto'o.</p>''',
            'fundacao': datetime(2010, 1, 1),
            'titulos': 5,
            'regiao': 'Europa'
        }
    ]

    # Imagens disponíveis para usar
    available_images = ['times-historicos.jpg', 'clubes.jpg', 'bocaxriver.jpg']
    image_index = 0

    for time_data in times_data:
        time, created = Time.objects.get_or_create(
            nome=time_data['nome'],
            defaults={
                'descricao': time_data['descricao'],
                'fundacao': time_data['fundacao'],
                'titulos': time_data['titulos'],
                'regiao': time_data['regiao']
            }
        )
        
        # Se o time foi criado e não tem imagem, adiciona uma das imagens disponíveis
        if created or not time.imagem:
            image_name = available_images[image_index % len(available_images)]
            image_path = Path(__file__).resolve().parent / 'static' / 'blog' / 'images' / image_name
            
            if image_path.exists():
                with open(image_path, 'rb') as img_file:
                    time.imagem.save(image_name, File(img_file), save=True)
            
            image_index += 1

    print("Times históricos criados/atualizados com sucesso!")

def update_team_images():
    """Atualiza as imagens dos times que ainda não têm imagem"""
    
    # Mapeamento de imagens para os times
    team_images = {
        'Seleção Brasileira 2002': 'ronaldo-roberto-carlos.jpg',
        'Real Madrid 2017': 'clubes.jpg',
        'Santos 1962': 'times-historicos.jpg'
    }
    
    # Caminho base para as imagens
    base_path = Path(__file__).resolve().parent / 'static' / 'blog' / 'images'
    
    # Atualiza cada time
    for team_name, image_name in team_images.items():
        try:
            time = Time.objects.get(nome=team_name)
            if not time.imagem:  # Só atualiza se não tiver imagem
                image_path = base_path / image_name
                if image_path.exists():
                    with open(image_path, 'rb') as img_file:
                        time.imagem.save(image_name, File(img_file), save=True)
                    print(f'Imagem atualizada para {team_name}')
                else:
                    print(f'Imagem {image_name} não encontrada')
        except Time.DoesNotExist:
            print(f'Time {team_name} não encontrado')
        except Exception as e:
            print(f'Erro ao atualizar imagem para {team_name}: {str(e)}')
