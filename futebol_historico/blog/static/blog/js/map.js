$(document).ready(function () {
    console.log("DOM carregado, verificando ícones.");
    console.log("jQuery carregado:", typeof $ !== 'undefined');

    const icons = $('.nations-of-world-icons .icon');
    console.log("Ícones encontrados:", icons.length);

    // Adicionando evento de clique para cada bandeira
    icons.each(function () {
        $(this).on('click', function () {
            const countryId = $(this).data('country-id');
            console.log("Bandeira clicada: ", countryId);

            // Chama a função para animar o mapa e mostrar o card do país
            selectCountry(countryId);
        });
    });

    // Definindo as variáveis chart e polygonSeries globalmente para uso posterior
    var chart;
    var polygonSeries;
    var previousSelectedPolygon; // Para armazenar o último país selecionado

    // Função para selecionar o país e girar o globo para o país correspondente
    function selectCountry(countryId) {
        console.log("Selecionando o país: ", countryId);

               const countryData = {
                   "BR": { 
                       name: "Brasil", 
                       flag: "/static/blog/images/bandeiras/brasil.png",
                       nickname: "Seleção Canarinho", 
                       description: "A seleção mais vitoriosa da história das Copas do Mundo",
                       titles: 5,
                       participations: 22,
                       goals: 229,
                       matches: 109,
                       victories: 73,
                       draws: 18,
                       defeats: 18,
                       bestResult: "5 títulos mundiais (1958, 1962, 1970, 1994, 2002)",
                       legendaryPlayers: "Pelé, Ronaldo, Ronaldinho, Romário, Zico",
                       style: "Futebol Arte",
                       info: "O Brasil é a única seleção a participar de todas as edições da Copa do Mundo. Conhecida pelo 'futebol arte' e jogadores lendários como Pelé, Ronaldo e Ronaldinho, conquistou 5 títulos mundiais. A seleção brasileira é sinônimo de criatividade, técnica e alegria no futebol mundial.",
                       // Informações adicionais importantes
                       founded: "1914",
                       confederation: "CONMEBOL",
                       homeStadium: "Maracanã",
                       coach: "Tite",
                       captain: "Thiago Silva",
                       worldRanking: "1º",
                       copaAmerica: "9 títulos",
                       olympicGold: "1 (2016)",
                       worldCupFinals: "7 finais",
                       goldenBoot: "Pelé (12 gols em 1958)",
                       mostCaps: "Cafu (142 jogos)",
                       topScorer: "Pelé (77 gols)",
                       topScorerWorldCup: "Ronaldo (15 gols em Copas)",
                       famousVictory: "7x1 Alemanha (2014)",
                       homeKit: "Amarelo e Verde",
                       awayKit: "Azul",
                       motto: "Ordem e Progresso"
                   },
                   "DE": { 
                       name: "Alemanha", 
                       flag: "/static/blog/images/bandeiras/alemanha.png",
                nickname: "Die Mannschaft", 
                description: "A máquina alemã do futebol mundial",
                titles: 4,
                participations: 20,
                goals: 226,
                matches: 109,
                victories: 67,
                draws: 20,
                defeats: 22,
                bestResult: "4 títulos mundiais (1954, 1974, 1990, 2014)",
                legendaryPlayers: "Franz Beckenbauer, Gerd Müller, Miroslav Klose",
                style: "Eficiência Tática",
                info: "A Alemanha é uma das seleções mais consistentes da história. Conhecida pela disciplina tática e eficiência, conquistou 4 títulos mundiais. A 'Mannschaft' sempre apresenta um futebol organizado, físico e tecnicamente sólido.",
                // Informações adicionais importantes
                founded: "1900",
                confederation: "UEFA",
                homeStadium: "Allianz Arena",
                coach: "Hansi Flick",
                captain: "Manuel Neuer",
                worldRanking: "2º",
                euroChampionship: "3 títulos",
                olympicGold: "1 (1976)",
                worldCupFinals: "8 finais",
                goldenBoot: "Gerd Müller (14 gols em 1970)",
                mostCaps: "Lothar Matthäus (150 jogos)",
                topScorer: "Miroslav Klose (71 gols)",
                topScorerWorldCup: "Miroslav Klose (16 gols em Copas)",
                famousVictory: "7x1 Brasil (2014)",
                homeKit: "Branco e Preto",
                awayKit: "Verde",
                motto: "Einigkeit und Recht und Freiheit"
            },
                   "AR": { 
                       name: "Argentina", 
                       flag: "/static/blog/images/bandeiras/argentina.png",
                nickname: "La Albiceleste", 
                description: "A paixão e técnica sul-americana",
                titles: 3,
                participations: 18,
                goals: 137,
                matches: 81,
                victories: 47,
                draws: 15,
                defeats: 19,
                bestResult: "3 títulos mundiais (1978, 1986, 2022)",
                legendaryPlayers: "Diego Maradona, Lionel Messi, Gabriel Batistuta",
                style: "Paixão e Técnica",
                info: "A Argentina é famosa pela paixão e técnica. Conquistou 3 títulos mundiais e é conhecida por produzir grandes craques como Maradona e Messi. A 'Albiceleste' representa a paixão sul-americana no futebol mundial.",
                // Informações adicionais importantes
                founded: "1893",
                confederation: "CONMEBOL",
                homeStadium: "Estadio Monumental",
                coach: "Lionel Scaloni",
                captain: "Lionel Messi",
                worldRanking: "3º",
                copaAmerica: "15 títulos",
                olympicGold: "2 (2004, 2008)",
                worldCupFinals: "6 finais",
                goldenBoot: "Mario Kempes (6 gols em 1978)",
                mostCaps: "Lionel Messi (172 jogos)",
                topScorer: "Lionel Messi (98 gols)",
                topScorerWorldCup: "Gabriel Batistuta (10 gols em Copas)",
                famousVictory: "2x1 Alemanha (1986)",
                homeKit: "Azul e Branco",
                awayKit: "Preto",
                motto: "En unión y libertad"
            },
                   "IT": { 
                       name: "Itália", 
                       flag: "/static/blog/images/bandeiras/italia.png",
                nickname: "Gli Azzurri", 
                description: "A arte da defesa italiana",
                titles: 4,
                participations: 18,
                goals: 128,
                matches: 83,
                victories: 45,
                draws: 21,
                defeats: 17,
                bestResult: "4 títulos mundiais (1934, 1938, 1982, 2006)",
                legendaryPlayers: "Paolo Rossi, Roberto Baggio, Gianluigi Buffon",
                style: "Catenaccio",
                info: "A Itália é conhecida pela defesa sólida e tática italiana. Conquistou 4 títulos mundiais e é famosa pela 'Catenaccio' e grandes goleiros como Buffon. A 'Squadra Azzurra' é mestre na arte defensiva.",
                // Informações adicionais importantes
                founded: "1898",
                confederation: "UEFA",
                homeStadium: "San Siro",
                coach: "Roberto Mancini",
                captain: "Giorgio Chiellini",
                worldRanking: "4º",
                euroChampionship: "2 títulos",
                olympicGold: "1 (1936)",
                worldCupFinals: "6 finais",
                goldenBoot: "Paolo Rossi (6 gols em 1982)",
                mostCaps: "Gianluigi Buffon (176 jogos)",
                topScorer: "Luigi Riva (35 gols)",
                topScorerWorldCup: "Paolo Rossi (9 gols em Copas)",
                famousVictory: "4x3 Alemanha (1970)",
                homeKit: "Azul",
                awayKit: "Branco",
                motto: "Fratelli d'Italia"
            },
                   "FR": { 
                       name: "França", 
                       flag: "/static/blog/images/bandeiras/franca.png",
                nickname: "Les Bleus", 
                description: "O estilo elegante do futebol francês",
                titles: 2,
                participations: 16,
                goals: 120,
                matches: 66,
                victories: 37,
                draws: 13,
                defeats: 16,
                bestResult: "2 títulos mundiais (1998, 2018)",
                legendaryPlayers: "Zinedine Zidane, Thierry Henry, Kylian Mbappé",
                style: "Elegância Técnica",
                info: "A França conquistou 2 títulos mundiais e é conhecida por seu estilo de jogo elegante e jogadores como Zidane e Mbappé. A seleção francesa sempre apresenta um futebol técnico, ofensivo e multicultural.",
                // Informações adicionais importantes
                founded: "1904",
                confederation: "UEFA",
                homeStadium: "Stade de France",
                coach: "Didier Deschamps",
                captain: "Hugo Lloris",
                worldRanking: "5º",
                euroChampionship: "2 títulos",
                olympicGold: "1 (1984)",
                worldCupFinals: "3 finais",
                goldenBoot: "Just Fontaine (13 gols em 1958)",
                mostCaps: "Lilian Thuram (142 jogos)",
                topScorer: "Thierry Henry (51 gols)",
                topScorerWorldCup: "Just Fontaine (13 gols em Copas)",
                famousVictory: "3x0 Brasil (1998)",
                homeKit: "Azul",
                awayKit: "Branco",
                motto: "Liberté, égalité, fraternité"
            },
                   "GB": { 
                       name: "Inglaterra", 
                       flag: "/static/blog/images/bandeiras/inglaterra.png",
                nickname: "The Three Lions", 
                description: "O berço do futebol moderno",
                titles: 1,
                participations: 16,
                goals: 91,
                matches: 69,
                victories: 29,
                draws: 21,
                defeats: 19,
                bestResult: "1 título mundial (1966)",
                legendaryPlayers: "Bobby Charlton, Gary Lineker, Harry Kane",
                style: "Futebol Tradicional",
                info: "A Inglaterra conquistou 1 título mundial em casa (1966) e é conhecida pela paixão de seus torcedores. É considerada o berço do futebol moderno e sempre apresenta jogadores de grande qualidade técnica.",
                // Informações adicionais importantes
                founded: "1863",
                confederation: "UEFA",
                homeStadium: "Wembley Stadium",
                coach: "Gareth Southgate",
                captain: "Harry Kane",
                worldRanking: "6º",
                euroChampionship: "0 títulos",
                olympicGold: "3 (1900, 1908, 1912)",
                worldCupFinals: "1 final",
                goldenBoot: "Gary Lineker (6 gols em 1986)",
                mostCaps: "Peter Shilton (125 jogos)",
                topScorer: "Harry Kane (58 gols)",
                topScorerWorldCup: "Gary Lineker (10 gols em Copas)",
                famousVictory: "4x2 Alemanha (1966)",
                homeKit: "Branco",
                awayKit: "Vermelho",
                motto: "God Save the Queen"
            },
                   "UY": { 
                       name: "Uruguai", 
                       flag: "/static/blog/images/bandeiras/uruguai.png",
                nickname: "La Celeste", 
                description: "A surpresa sul-americana",
                titles: 2,
                participations: 14,
                goals: 88,
                matches: 59,
                victories: 24,
                draws: 12,
                defeats: 23,
                bestResult: "2 títulos mundiais (1930, 1950)",
                legendaryPlayers: "José Nasazzi, Diego Forlán, Luis Suárez",
                style: "Garra Charrúa",
                info: "O Uruguai surpreendeu o mundo com 2 títulos mundiais, incluindo a primeira Copa em 1930. Conhecida pela 'Garra Charrúa' e jogadores como Forlán e Suárez. A 'Celeste' representa a determinação sul-americana.",
                // Informações adicionais importantes
                founded: "1900",
                confederation: "CONMEBOL",
                homeStadium: "Estadio Centenario",
                coach: "Diego Alonso",
                captain: "Diego Godín",
                worldRanking: "7º",
                copaAmerica: "15 títulos",
                olympicGold: "2 (1924, 1928)",
                worldCupFinals: "2 finais",
                goldenBoot: "Óscar Míguez (8 gols em 1950)",
                mostCaps: "Maxi Pereira (125 jogos)",
                topScorer: "Luis Suárez (68 gols)",
                topScorerWorldCup: "Óscar Míguez (8 gols em Copas)",
                famousVictory: "2x1 Brasil (1950)",
                homeKit: "Azul Celeste",
                awayKit: "Branco",
                motto: "Libertad o muerte"
            },
                   "ES": { 
                       name: "Espanha", 
                       flag: "/static/blog/images/bandeiras/espanha.png",
                nickname: "La Roja", 
                description: "O tiki-taka espanhol",
                titles: 1,
                participations: 16,
                goals: 99,
                matches: 63,
                victories: 30,
                draws: 15,
                defeats: 18,
                bestResult: "1 título mundial (2010)",
                legendaryPlayers: "Andrés Iniesta, Xavi, David Villa",
                style: "Tiki-Taka",
                info: "A Espanha conquistou seu primeiro título mundial em 2010, com um estilo de jogo baseado na posse de bola e passes curtos, conhecido como 'Tiki-Taka'. A seleção espanhola revolucionou o futebol moderno com sua técnica apurada.",
                // Informações adicionais importantes
                founded: "1913",
                confederation: "UEFA",
                homeStadium: "Santiago Bernabéu",
                coach: "Luis Enrique",
                captain: "Sergio Busquets",
                worldRanking: "8º",
                euroChampionship: "3 títulos",
                olympicGold: "1 (1992)",
                worldCupFinals: "1 final",
                goldenBoot: "David Villa (5 gols em 2010)",
                mostCaps: "Sergio Ramos (180 jogos)",
                topScorer: "David Villa (59 gols)",
                topScorerWorldCup: "David Villa (9 gols em Copas)",
                famousVictory: "1x0 Holanda (2010)",
                homeKit: "Vermelho",
                awayKit: "Azul",
                motto: "Plus ultra"
            }
        };        

        // Verifica se o país está na lista
        const country = countryData[countryId] || { 
            name: "Desconhecido", 
            flag: "",
            nickname: "N/A",
            description: "N/A",
            titles: 0,
            participations: 0,
            goals: 0,
            matches: 0,
            victories: 0,
            draws: 0,
            defeats: 0,
            bestResult: "N/A",
            legendaryPlayers: "N/A",
            style: "N/A",
            info: "Informações não disponíveis." 
        };

               // Atualiza o conteúdo do card de informações
               console.log("Atualizando card para:", country.name);
               console.log("Dados:", country);
               
               // Verificar se os elementos existem
               console.log("Elemento country-name existe:", $('#country-name').length);
               console.log("Elemento stat-titles existe:", $('#stat-titles').length);
               
               // Atualizar número de títulos no troféu
               $('#trophy-count').text(country.titles);
               
               // Atualizar bandeira como fundo do header
               $('#country-flag').attr('src', country.flag).attr('alt', country.name);
               
               // Atualizar informações do país
               $('#country-nickname').text(country.nickname);
               $('#country-description').text(country.description);
               $('#stat-participations').text(country.participations);
               
               // Atualizar maior artilheiro em Copas
               const topScorerText = country.topScorerWorldCup || 'N/A';
               $('#top-scorer').text(topScorerText);
               console.log("Maior artilheiro:", topScorerText);
               console.log("Elemento top-scorer encontrado:", $('#top-scorer').length);
               
               console.log("Card atualizado com sucesso!");

        // Atualizar link do botão parallax
        const parallaxUrl = `/parallax-craques/${countryId}/`;
        $('#btnParallaxCraques').attr('href', parallaxUrl);

        // Exibe o card de informações com o tema do país (dentro da seção do globo)
        $('#info-card').attr('data-country', countryId).addClass('show');

        const stage = document.querySelector('.nations-of-world__stage');
        if (stage) {
            stage.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }

        // Focar no país no mapa
        var dataItem = polygonSeries.getDataItemById(countryId);
        if (dataItem) {
            var target = dataItem.get("mapPolygon");
            if (target) {
                var centroid = target.geoCentroid();  // Encontra o centro geográfico do país
                console.log("Centróide do país:", centroid);

                // Remove o estado de "selecionado" do país anterior
                if (previousSelectedPolygon) {
                    previousSelectedPolygon.states.applyAnimate("default");
                }

                // Aplica o estado de "selecionado" ao novo país
                target.states.applyAnimate("selected");
                previousSelectedPolygon = target;

                if (centroid) {
                    // Anima a rotação do mapa para centralizar o país clicado
                    chart.animate({
                        key: "rotationX", to: -centroid.longitude, duration: 1500, easing: am5.ease.inOut(am5.ease.cubic)
                    });
                    chart.animate({
                        key: "rotationY", to: -centroid.latitude, duration: 1500, easing: am5.ease.inOut(am5.ease.cubic)
                    });
                }
            }
        }
    }

    $("#btnCloseInfoCard").on("click", function () {
        $('#info-card').removeClass('show');
    });

    function disposeExistingGlobeRoot() {
        if (typeof am5 === 'undefined' || !am5.registry || !am5.registry.rootElements) {
            return;
        }
        am5.array.each(am5.registry.rootElements, function (root) {
            if (root.dom && root.dom.id === 'chartdiv') {
                root.dispose();
            }
        });
    }

    function initWorldGlobe() {
        const chartContainer = document.getElementById('chartdiv');
        if (!chartContainer) {
            return;
        }
        if (typeof am5 === 'undefined' || typeof am5map === 'undefined' || typeof am5geodata_worldLow === 'undefined') {
            console.warn('amCharts não carregado; globo indisponível.');
            return;
        }
        if (chartContainer.dataset.globeReady === '1') {
            return;
        }

        am5.ready(function () {
            try {
                disposeExistingGlobeRoot();

                var root = am5.Root.new('chartdiv');

                if (root._logo) {
                    root._logo.dispose();
                }

                chart = root.container.children.push(am5map.MapChart.new(root, {
                    panX: 'rotateX',
                    panY: 'rotateY',
                    projection: am5map.geoOrthographic(),
                    paddingBottom: 20,
                    paddingTop: 20,
                    paddingLeft: 20,
                    paddingRight: 20
                }));

                if (chart.logo) {
                    chart.logo.disabled = true;
                }

                polygonSeries = chart.series.push(am5map.MapPolygonSeries.new(root, {
                    geoJSON: am5geodata_worldLow
                }));

                polygonSeries.mapPolygons.template.setAll({
                    tooltipText: '{name}',
                    toggleKey: 'active',
                    interactive: true,
                    fill: am5.color(0x6ba4d8),
                    stroke: am5.color(0xb8d9ff),
                    strokeWidth: 0.6
                });

                polygonSeries.mapPolygons.template.states.create('selected', {
                    fill: am5.color(0xFFD700)
                });

                polygonSeries.mapPolygons.template.states.create('hover', {
                    fill: am5.color(0x87CEEB)
                });

                polygonSeries.mapPolygons.template.states.create('active', {
                    fill: am5.color(0x66AAFF)
                });

                var backgroundSeries = chart.series.push(am5map.MapPolygonSeries.new(root, {}));
                backgroundSeries.mapPolygons.template.setAll({
                    fill: am5.color(0x1b2735),
                    fillOpacity: 0.2,
                    strokeOpacity: 0
                });
                backgroundSeries.data.push({
                    geometry: am5map.getGeoRectangle(90, 180, -90, -180)
                });

                var graticuleSeries = chart.series.unshift(
                    am5map.GraticuleSeries.new(root, {
                        step: 10
                    })
                );

                graticuleSeries.mapLines.template.setAll({
                    stroke: am5.color(0xffffff),
                    strokeOpacity: 0.12
                });

                var previousPolygon;
                var rotationInterval = setInterval(function () {
                    if (!chart) {
                        clearInterval(rotationInterval);
                        return;
                    }
                    chart.set('rotationX', chart.get('rotationX') + 0.15);
                }, 50);

                chart.root.container.events.on('pointerdown', function () {
                    clearInterval(rotationInterval);
                });

                polygonSeries.mapPolygons.template.on('active', function (active, target) {
                    if (previousPolygon && previousPolygon !== target) {
                        previousPolygon.set('active', false);
                    }
                    if (target.get('active')) {
                        selectCountry(target.dataItem.get('id'));
                    }
                    previousPolygon = target;
                });

                chartContainer.dataset.globeReady = '1';
            } catch (error) {
                console.error('Erro ao inicializar globo:', error);
                chartContainer.dataset.globeReady = '0';
            }
        });
    }

    initWorldGlobe();
    $(window).on('load', function () {
        var chartContainer = document.getElementById('chartdiv');
        if (chartContainer && chartContainer.dataset.globeReady !== '1') {
            initWorldGlobe();
        }
    });
});

