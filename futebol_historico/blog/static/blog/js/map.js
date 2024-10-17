document.addEventListener("DOMContentLoaded", function () {
    console.log("DOM carregado, verificando ícones.");

    const icons = document.querySelectorAll('.nations-of-world-icons .icon');
    console.log("Ícones encontrados:", icons.length);

    // Adicionando evento de clique para cada bandeira
    icons.forEach(function (icon) {
        icon.addEventListener('click', function () {
            const countryId = this.getAttribute('data-country-id');
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

        // Dados do país
        const countryData = {
            "BR": { name: "Brasil", info: "O Brasil ganhou a Copa do Mundo 5 vezes." },
            "DE": { name: "Alemanha", info: "A Alemanha ganhou a Copa do Mundo 4 vezes." },
            "AR": { name: "Argentina", info: "A Argentina ganhou a Copa do Mundo 3 vezes." },
            "IT": { name: "Itália", info: "A Itália ganhou a Copa do Mundo 4 vezes." },
            "FR": { name: "França", info: "A França ganhou a Copa do Mundo 2 vezes." },
            "GB": { name: "Inglaterra", info: "A Inglaterra ganhou a Copa do Mundo 1 vez." },
            "UY": { name: "Uruguai", info: "O Uruguai ganhou a Copa do Mundo 2 vezes." },
            "ES": { name: "Espanha", info: "A Espanha ganhou a Copa do Mundo 1 vez." }
        };

        // Verifica se o país está na lista
        const country = countryData[countryId] || { name: "Desconhecido", info: "Informações não disponíveis." };

        // Atualiza o conteúdo do card de informações
        document.getElementById('country-name').textContent = country.name;
        document.getElementById('country-info').textContent = country.info;

        // Exibe o card de informações
        document.getElementById('info-card').style.display = 'block';

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

    // Função para fechar o card de informações
    function closeInfoCard() {
        document.getElementById('info-card').style.display = 'none';
    }

    // Adiciona o evento de clique para o botão de fechar
    document.getElementById('info-card').querySelector('button').addEventListener('click', closeInfoCard);

    // Configuração do mapa amCharts
    am5.ready(function () {
        var root = am5.Root.new("chartdiv");

        root.setThemes([am5themes_Animated.new(root)]);

        chart = root.container.children.push(am5map.MapChart.new(root, {
            panX: "rotateX",
            panY: "rotateY",
            projection: am5map.geoOrthographic(),
            paddingBottom: 20,
            paddingTop: 20,
            paddingLeft: 20,
            paddingRight: 20
        }));

        polygonSeries = chart.series.push(am5map.MapPolygonSeries.new(root, {
            geoJSON: am5geodata_worldLow
        }));

        polygonSeries.mapPolygons.template.setAll({
            tooltipText: "{name}",
            toggleKey: "active",
            interactive: true
        });

        // Estado para país "selecionado" com uma cor destacada
        polygonSeries.mapPolygons.template.states.create("selected", {
            fill: am5.color(0x6e6ea9)  
        });

        polygonSeries.mapPolygons.template.states.create("hover", {
            fill: root.interfaceColors.get("primaryButtonHover")
        });

        polygonSeries.mapPolygons.template.states.create("active", {
            fill: root.interfaceColors.get("primaryButtonHover")
        });

        var backgroundSeries = chart.series.push(am5map.MapPolygonSeries.new(root, {}));
        backgroundSeries.mapPolygons.template.setAll({
            fill: root.interfaceColors.get("alternativeBackground"),
            fillOpacity: 0.1,
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

        graticuleSeries.mapLines.template.set("strokeOpacity", 0.1);

        var previousPolygon;

        // Evento ao clicar em um país no mapa
        polygonSeries.mapPolygons.template.on("active", function (active, target) {
            if (previousPolygon && previousPolygon != target) {
                previousPolygon.set("active", false);
            }
            if (target.get("active")) {
                console.log("País selecionado no mapa:", target.dataItem.get("id"));
                selectCountry(target.dataItem.get("id"));
            }
            previousPolygon = target;
        });
    });
});
