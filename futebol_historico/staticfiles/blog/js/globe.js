document.addEventListener('DOMContentLoaded', function() {
    // Configuração do Three.js
    const container = document.getElementById('globe-container');
    const width = container.clientWidth;
    const height = container.clientHeight;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(width, height);
    container.appendChild(renderer.domElement);

    // Criar o globo
    const geometry = new THREE.SphereGeometry(5, 32, 32);
    const textureLoader = new THREE.TextureLoader();
    
    // Carregar a textura do mapa-múndi
    const texture = textureLoader.load('/static/blog/images/textures/earth.jpg');
    const material = new THREE.MeshPhongMaterial({
        map: texture,
        shininess: 5
    });
    
    const globe = new THREE.Mesh(geometry, material);
    scene.add(globe);

    // Adicionar iluminação
    const ambientLight = new THREE.AmbientLight(0x404040);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
    directionalLight.position.set(5, 3, 5);
    scene.add(directionalLight);

    camera.position.z = 15;

    // Definir as coordenadas dos continentes
    const continents = {
        'Europa': { lat: 48.8566, lon: 2.3522 },
        'América do Sul': { lat: -15.7975, lon: -47.8919 },
        'América do Norte': { lat: 40.7128, lon: -74.0060 },
        'África': { lat: -1.2921, lon: 36.8219 },
        'Ásia': { lat: 35.6762, lon: 139.6503 },
        'Oceania': { lat: -33.8688, lon: 151.2093 }
    };

    // Função para converter coordenadas em posição 3D
    function latLonToVector3(lat, lon, radius) {
        const phi = (90 - lat) * (Math.PI / 180);
        const theta = (lon + 180) * (Math.PI / 180);
        const x = -(radius * Math.sin(phi) * Math.cos(theta));
        const z = (radius * Math.sin(phi) * Math.sin(theta));
        const y = (radius * Math.cos(phi));
        return new THREE.Vector3(x, y, z);
    }

    // Adicionar marcadores para os continentes
    Object.entries(continents).forEach(([name, coords]) => {
        const markerGeometry = new THREE.SphereGeometry(0.2, 16, 16);
        const markerMaterial = new THREE.MeshBasicMaterial({ color: 0x66aaff });
        const marker = new THREE.Mesh(markerGeometry, markerMaterial);
        const position = latLonToVector3(coords.lat, coords.lon, 5.2);
        marker.position.copy(position);
        marker.userData.continent = name;
        globe.add(marker);
    });

    // Animação do globo
    let isRotating = true;
    function animate() {
        requestAnimationFrame(animate);
        if (isRotating) {
            globe.rotation.y += 0.001;
        }
        renderer.render(scene, camera);
    }
    animate();

    // Interatividade
    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();
    const continentInfo = document.querySelector('.continent-info');

    function normalizeContinent(name) {
        return name.toLowerCase()
                  .normalize('NFD')
                  .replace(/[\u0300-\u036f]/g, '')
                  .replace(/\s+/g, '-')
                  .replace(/[^a-z0-9-]/g, '');
    }

    container.addEventListener('mousemove', (event) => {
        const rect = container.getBoundingClientRect();
        mouse.x = ((event.clientX - rect.left) / width) * 2 - 1;
        mouse.y = -((event.clientY - rect.top) / height) * 2 + 1;

        raycaster.setFromCamera(mouse, camera);
        const intersects = raycaster.intersectObjects(globe.children);

        if (intersects.length > 0) {
            const marker = intersects[0].object;
            if (marker.userData.continent) {
                container.style.cursor = 'pointer';
                continentInfo.style.display = 'block';
                continentInfo.querySelector('h3').textContent = marker.userData.continent;
                continentInfo.querySelector('p').textContent = 'Clique para ver os estádios';
                continentInfo.style.left = event.clientX - rect.left + 20 + 'px';
                continentInfo.style.top = event.clientY - rect.top + 20 + 'px';
            }
        } else {
            container.style.cursor = 'default';
            continentInfo.style.display = 'none';
        }
    });

    container.addEventListener('click', (event) => {
        const rect = container.getBoundingClientRect();
        mouse.x = ((event.clientX - rect.left) / width) * 2 - 1;
        mouse.y = -((event.clientY - rect.top) / height) * 2 + 1;

        raycaster.setFromCamera(mouse, camera);
        const intersects = raycaster.intersectObjects(globe.children);

        if (intersects.length > 0) {
            const marker = intersects[0].object;
            if (marker.userData.continent) {
                const continent = marker.userData.continent;
                const normalizedContinent = normalizeContinent(continent);
                
                // Esconder todas as seções
                document.querySelectorAll('.estadios-section').forEach(section => {
                    section.classList.remove('active');
                });
                
                // Mostrar a seção do continente clicado
                const targetSection = document.getElementById(`estadios-${normalizedContinent}`);
                if (targetSection) {
                    targetSection.classList.add('active');
                    targetSection.scrollIntoView({ behavior: 'smooth' });
                }
                
                // Parar a rotação do globo
                isRotating = false;
            }
        }
    });

    // Reiniciar rotação ao passar o mouse para fora do globo
    container.addEventListener('mouseleave', () => {
        isRotating = true;
        continentInfo.style.display = 'none';
    });

    // Responsividade
    window.addEventListener('resize', () => {
        const newWidth = container.clientWidth;
        const newHeight = container.clientHeight;
        camera.aspect = newWidth / newHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(newWidth, newHeight);
    });
});
