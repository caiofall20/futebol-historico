// map.js
am5.ready(function() {
    var root = am5.Root.new("chartdiv");

    root.setThemes([
        am5themes_Animated.new(root)
    ]);

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

    graticuleSeries.mapLines.template.set("strokeOpacity", 0.1)

    var previousPolygon;

    polygonSeries.mapPolygons.template.on("active", function(active, target) {
        if (previousPolygon && previousPolygon != target) {
            previousPolygon.set("active", false);
        }
        if (target.get("active")) {
            selectCountry(target.dataItem.get("id"));
        }
        previousPolygon = target;
    });

    function selectCountry(id) {
        var dataItem = polygonSeries.getDataItemById(id);
        var target = dataItem.get("mapPolygon");
        if (target) {
            var centroid = target.geoCentroid();
            if (centroid) {
                chart.animate({ key: "rotationX", to: -centroid.longitude, duration: 1500, easing: am5.ease.inOut(am5.ease.cubic) });
                chart.animate({ key: "rotationY", to: -centroid.latitude, duration: 1500, easing: am5.ease.inOut(am5.ease.cubic) });
                showInfoCard(id); // Exibe o card com as informações do país
            }
        }
    }

    function showInfoCard(countryId) {
        var countryData = {
            "BR": { name: "Brasil", info: "O Brasil ganhou a Copa do Mundo X vezes." },
            "DE": { name: "Alemanha", info: "A Alemanha ganhou a Copa do Mundo X vezes." },
            "AR": { name: "Argentina", info: "A Argentina ganhou a Copa do Mundo X vezes." },
            "IT": { name: "Itália", info: "A Itália ganhou a Copa do Mundo X vezes." },
            "FR": { name: "França", info: "A França ganhou a Copa do Mundo X vezes." },
            "GB": { name: "Inglaterra", info: "A Inglaterra ganhou a Copa do Mundo X vezes." },
            "UY": { name: "Uruguai", info: "O Uruguai ganhou a Copa do Mundo X vezes." },
            "ES": { name: "Espanha", info: "A Espanha ganhou a Copa do Mundo X vezes." }
        };
        
        var country = countryData[countryId] || { name: "Desconhecido", info: "Informações não disponíveis." };
        document.getElementById('country-name').textContent = country.name;
        document.getElementById('country-info').textContent = country.info;
        document.getElementById('info-card').style.display = 'block';
    }

    function closeInfoCard() {
        document.getElementById('info-card').style.display = 'none';
    }

    document.querySelectorAll('.icons-container .icon').forEach(function(icon) {
        icon.addEventListener('click', function() {
            var countryId = this.getAttribute('data-country-id');
            selectCountry(countryId);
        });
    });
});
