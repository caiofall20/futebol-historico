$(document).ready(function () {
    console.log("DOM carregado, verificando ícones.");

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
                stars: 5, 
                rivals: ["Argentina", "Uruguai", "Holanda", "Alemanha", "Itália"], 
                nickname: "Canarinho, Verde e Amarela", 
                mascot: "Canarinho"
            },
            "DE": { 
                name: "Alemanha", 
                stars: 4, 
                rivals: ["Brasil", "Argentina", "Itália", "França"], 
                nickname: "Die Mannschaft", 
                mascot: "Águia"
            },
            "AR": { 
                name: "Argentina", 
                stars: 3, 
                rivals: ["Brasil", "Inglaterra", "Uruguai", "Alemanha"], 
                nickname: "La Albiceleste", 
                mascot: "Sábio"
            },
            "IT": { 
                name: "Itália", 
                stars: 4, 
                rivals: ["Alemanha", "França", "Brasil", "Espanha"], 
                nickname: "Gli Azzurri", 
                mascot: "Ciao"
            },
            "FR": { 
                name: "França", 
                stars: 2, 
                rivals: ["Alemanha", "Itália", "Inglaterra", "Argentina"], 
                nickname: "Les Bleus", 
                mascot: "Footix"
            },
            "GB": { 
                name: "Inglaterra", 
                stars: 1, 
                rivals: ["Argentina", "Alemanha", "França"], 
                nickname: "The Three Lions", 
                mascot: "Willie"
            },
            "UY": { 
                name: "Uruguai", 
                stars: 2, 
                rivals: ["Brasil", "Argentina"], 
                nickname: "La Celeste", 
                mascot: "Pelusa"
            },
            "ES": { 
                name: "Espanha", 
                stars: 1, 
                rivals: ["Itália", "França", "Portugal"], 
                nickname: "La Roja", 
                mascot: "Naranjito"
            }
        };        

        // Verifica se o país está na lista
        const country = countryData[countryId] || { name: "Desconhecido", info: "Informações não disponíveis." };

        // Atualiza o conteúdo do card de informações
        $('#country-name').text(country.name);
        $('#country-info').text(country.info);

        // Exibe o card de informações
        $('#info-card').show();

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

