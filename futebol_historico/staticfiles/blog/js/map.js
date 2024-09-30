// Garante que o script só será executado após todo o DOM ter sido carregado
document.addEventListener("DOMContentLoaded", function () {
    console.log("DOM completamente carregado. Iniciando o script map.js.");

    // Verificação básica: garantir que os ícones de bandeiras estão no DOM
    const icons = document.querySelectorAll('.nations-of-world-icons .icon');
    console.log("Ícones encontrados:", icons.length);  // Deve listar o número de ícones encontrados

    if (icons.length > 0) {
        // Adiciona evento de clique em cada ícone de bandeira
        icons.forEach(function (icon, index) {
            console.log("Ícone encontrado:", index, icon);  // Deve listar cada ícone no console
            icon.addEventListener('click', function () {
                var countryId = this.getAttribute('data-country-id');
                console.log("Bandeira clicada:", countryId);  // Verifique se o clique está sendo registrado
                alert("Bandeira clicada: " + countryId);

                // Aqui você pode chamar a função selectCountry para animar o mapa, se necessário
                selectCountry(countryId);
            });
        });
    } else {
        console.error("Nenhum ícone de bandeira foi encontrado!");
    }

    // Função para selecionar o país (simples para teste)
    function selectCountry(countryId) {
        console.log("Selecionando o país:", countryId);
        // Exemplo de ação ao clicar em uma bandeira (animar o mapa ou exibir card de informações)
        alert("País selecionado: " + countryId);
    }

    // Configuração do mapa amCharts
    am5.ready(function () {
        var root = am5.Root.new("chartdiv");

        root.setThemes([am5themes_Animated.new(root)]);

        var chart = root.container.children.push(am5map.MapChart.new(root, {
            panX: "rotateX",
            panY: "rotateY",
            projection: am5map.geoOrthographic(),
            paddingBottom: 20,
            paddingTop: 20,
            paddingLeft: 20,
            paddingRight: 20
        }));

        var polygonSeries = chart.series.push(am5map.MapPolygonSeries.new(root, {
            geoJSON: am5geodata_worldLow
        }));

        polygonSeries.mapPolygons.template.setAll({
            tooltipText: "{name}",
            toggleKey: "active",
            interactive: true
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
