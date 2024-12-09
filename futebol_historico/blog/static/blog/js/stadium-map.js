$(document).ready(function () {
    console.log("DOM carregado, iniciando mapa de estádios.");

    // Função para selecionar o continente e mostrar os estádios correspondentes
    function selectContinent(continentId) {
        console.log("Selecionando o continente: ", continentId);

        const continent = continentMap[continentId] || { name: "Desconhecido" };

        // Atualiza o conteúdo do card de informações
        $('#continent-name').text(continent);
        $('#continent-info').text("Clique para ver os estádios deste continente");

        // Exibe o card de informações
        $('#info-card').show();

        // Focar no continente no mapa
        var dataItem = polygonSeries.getDataItemById(continentId);
        if (dataItem) {
            var target = dataItem.get("mapPolygon");
            if (target) {
                var centroid = continentCoordinates[continentId];
                console.log("Coordenadas do continente:", centroid);

                // Remove o estado de "selecionado" do país anterior
                if (previousSelectedPolygon) {
                    previousSelectedPolygon.states.applyAnimate("default");
                }

                // Aplica o estado de "selecionado" ao novo país
                target.states.applyAnimate("selected");
                previousSelectedPolygon = target;

                if (centroid) {
                    // Anima a rotação do mapa para centralizar o continente clicado
                    chart.animate({
                        key: "rotationX",
                        to: -centroid.longitude,
                        duration: 1500,
                        easing: am5.ease.inOut(am5.ease.cubic)
                    });
                    chart.animate({
                        key: "rotationY",
                        to: -centroid.latitude,
                        duration: 1500,
                        easing: am5.ease.inOut(am5.ease.cubic)
                    });

                    // Esconde todas as seções de estádios
                    $('.estadios-section').removeClass('active');

                    // Mostra a seção do continente selecionado
                    $(`#estadios-${continentId.toLowerCase()}`).addClass('active');
                    
                    // Rola suavemente até a seção dos estádios
                    $('html, body').animate({
                        scrollTop: $(`#estadios-${continentId.toLowerCase()}`).offset().top - 100
                    }, 1000);
                }
            }
        }
    }

    $("#btnCloseInfoCard").on("click", function(){
        $('#info-card').hide();
    });

    am5.ready(function () {
        var root = am5.Root.new("chartdiv");

        root.setThemes([am5themes_Animated.new(root)]);
        root._logo.dispose();

        chart = root.container.children.push(am5map.MapChart.new(root, {
            panX: "rotateX",
            panY: "rotateY",
            projection: am5map.geoOrthographic(),
            paddingBottom: 20,
            paddingTop: 20,
            paddingLeft: 20,
            paddingRight: 20
        }));

        if(chart.logo) {
            chart.logo.disabled = true;
        }

        polygonSeries = chart.series.push(am5map.MapPolygonSeries.new(root, {
            geoJSON: am5geodata_worldLow
        }));

        polygonSeries.mapPolygons.template.setAll({
            tooltipText: "{name}",
            toggleKey: "active",
            interactive: true,
            fill: am5.color(0x2B2D42)  // Cor base mais escura
        });

        // Estado para continente "selecionado" com uma cor destacada
        polygonSeries.mapPolygons.template.states.create("selected", {
            fill: am5.color(0x6E6EA9)  // Cor de destaque mais suave
        });

        polygonSeries.mapPolygons.template.states.create("hover", {
            fill: am5.color(0x8D99AE)  // Cor de hover mais suave
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
        graticuleSeries.mapLines.template.set("stroke", am5.color(0xffffff));

        var previousPolygon;

        // Evento ao clicar em um país no mapa
        polygonSeries.mapPolygons.template.on("active", function (active, target) {
            if (previousPolygon && previousPolygon != target) {
                previousPolygon.set("active", false);
            }
            if (target.get("active")) {
                var countryId = target.dataItem.get("id");
                console.log("País selecionado no mapa:", countryId);
                
                // Mapeia o país para o continente correspondente
                let continentId;
                if (["BR", "AR", "UY", "CL", "CO", "PE", "BO", "PY", "EC", "VE"].includes(countryId)) {
                    continentId = "AS";  // América do Sul
                } else if (["US", "CA", "MX"].includes(countryId)) {
                    continentId = "AN";  // América do Norte
                } else if (["GB", "FR", "DE", "IT", "ES", "PT", "NL", "BE", "CH", "AT", "PL", "SE", "NO", "DK", "FI", "RU"].includes(countryId)) {
                    continentId = "EU";  // Europa
                } else if (["CN", "JP", "KR", "IN", "ID", "TH", "VN", "MY", "PH"].includes(countryId)) {
                    continentId = "ASI";  // Ásia
                } else if (["AU", "NZ", "FJ"].includes(countryId)) {
                    continentId = "OC";  // Oceania
                } else if (["ZA", "NG", "EG", "MA", "DZ", "TN", "GH", "CI", "CM", "SN"].includes(countryId)) {
                    continentId = "AF";  // África
                }

                if (continentId) {
                    selectContinent(continentId);
                }
            }
            previousPolygon = target;
        });

        // Animação de rotação contínua
        let rotationInterval = setInterval(function() {
            var currentRotation = chart.get("rotationX");
            chart.set("rotationX", currentRotation + 0.2);
        }, 50);

        // Para a rotação quando o usuário interagir com o mapa
        chart.root.container.events.on("pointerdown", function() {
            clearInterval(rotationInterval);
        });
    });
});
