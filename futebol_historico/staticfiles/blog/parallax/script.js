// Elementos principais
const telaInicial = document.getElementById('tela-inicial');
const btnComecar = document.getElementById('btn-comecar');
const conteudoPrincipal = document.getElementById('conteudo-principal');
const audioMusica = document.getElementById('audio-musica');
const btnMusicaToggle = document.getElementById('btn-musica-toggle');
const volumeSlider = document.getElementById('volume-slider');
const controlesSuperiores = document.querySelector('.controles-superiores');
const btnAutoScroll = document.getElementById('btn-auto-scroll');
const secoesJogador = document.querySelectorAll('.secao-jogador');
const boxesInfo = document.querySelectorAll('.box-info');
const particlesCanvas = document.getElementById('particles-canvas');
const timeline = document.getElementById('timeline');
const timelineMarkers = document.querySelector('.timeline-markers');

// Estado
let musicaPausada = false;
let experienciaIniciada = false;
let autoScrollAtivo = false;
let autoScrollInterval = null;
let particles = [];
let animationFrameId = null;
let audioContext = null;
let torcidaGainNode = null;
// Removido sistema de travamento - navegação livre

// Dados dos jogadores para timeline
const jogadoresData = [
    { nome: 'Pelé', periodo: '1957-1971' },
    { nome: 'Zico', periodo: '1976-1986' },
    { nome: 'Bebeto', periodo: '1985-1998' },
    { nome: 'Romário', periodo: '1987-2005' },
    { nome: 'Rivaldo', periodo: '1993-2003' },
    { nome: 'Roberto Carlos', periodo: '1992-2006' },
    { nome: 'Ronaldo', periodo: '1994-2011' },
    { nome: 'Tafarel', periodo: '1988-1998' },
    { nome: 'Ronaldinho', periodo: '1999-2013' },
    { nome: 'Kaká', periodo: '2002-2016' },
    { nome: 'Neymar', periodo: '2010-Presente' }
];

// Menu de Países
const btnMenuPaises = document.getElementById('btn-menu-paises');
const dropdownPaises = document.getElementById('dropdown-paises');

if (btnMenuPaises && dropdownPaises) {
    btnMenuPaises.addEventListener('click', (e) => {
        e.stopPropagation();
        dropdownPaises.classList.toggle('ativo');
    });

    document.addEventListener('click', (e) => {
        if (!btnMenuPaises.contains(e.target) && !dropdownPaises.contains(e.target)) {
            dropdownPaises.classList.remove('ativo');
        }
    });
}

// Botões de Compartilhamento
document.querySelectorAll('.btn-compartilhar').forEach(btn => {
    btn.addEventListener('click', function() {
        const jogador = this.getAttribute('data-jogador');
        const plataforma = this.getAttribute('data-plataforma');
        const url = encodeURIComponent(window.location.href);
        const texto = encodeURIComponent(`Conheça a história de ${jogador} na Seleção Brasileira! 🏆⚽`);
        
        let shareUrl = '';
        
        switch(plataforma) {
            case 'whatsapp':
                shareUrl = `https://wa.me/?text=${texto}%20${url}`;
                break;
            case 'twitter':
                shareUrl = `https://twitter.com/intent/tweet?text=${texto}&url=${url}`;
                break;
            case 'facebook':
                shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${url}`;
                break;
        }
        
        if (shareUrl) {
            window.open(shareUrl, '_blank', 'width=600,height=400');
        }
    });
});

// Botão Voltar ao Topo
const btnVoltarTopo = document.createElement('button');
btnVoltarTopo.className = 'btn-voltar-topo';
btnVoltarTopo.setAttribute('aria-label', 'Voltar ao topo');
btnVoltarTopo.innerHTML = `
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M18 15l-6-6-6 6"/>
    </svg>
`;
document.body.appendChild(btnVoltarTopo);

window.addEventListener('scroll', () => {
    if (window.pageYOffset > 600) {
        btnVoltarTopo.classList.add('visivel');
    } else {
        btnVoltarTopo.classList.remove('visivel');
    }
});

btnVoltarTopo.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

// Barra de Progresso
const barraProgresso = document.createElement('div');
barraProgresso.className = 'barra-progresso';
document.body.appendChild(barraProgresso);

window.addEventListener('scroll', () => {
    const windowHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const scrolled = (window.pageYOffset / windowHeight) * 100;
    barraProgresso.style.transform = `scaleX(${scrolled / 100})`;
});

// Atalhos de Teclado
document.addEventListener('keydown', (e) => {
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
    
    switch(e.key) {
        case ' ':
            e.preventDefault();
            if (btnMusicaToggle) btnMusicaToggle.click();
            break;
        case 'ArrowDown':
            e.preventDefault();
            const btnProximo = document.querySelector('.btn-proximo');
            if (btnProximo) btnProximo.click();
            break;
        case 'ArrowUp':
            e.preventDefault();
            // Scroll para seção anterior
            const secoes = document.querySelectorAll('.secao-jogador');
            const currentIndex = Array.from(secoes).findIndex(sec => {
                const rect = sec.getBoundingClientRect();
                return rect.top >= 0 && rect.top < window.innerHeight / 2;
            });
            if (currentIndex > 0) {
                secoes[currentIndex - 1].scrollIntoView({ behavior: 'smooth' });
            }
            break;
        case 'm':
        case 'M':
            if (btnMusicaToggle) btnMusicaToggle.click();
            break;
    }
});

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    // Configurar volume inicial
    audioMusica.volume = volumeSlider.value / 100;
    
    // Event listeners
    btnComecar.addEventListener('click', iniciarExperiencia);
    btnMusicaToggle.addEventListener('click', toggleMusica);
    volumeSlider.addEventListener('input', ajustarVolume);
    btnAutoScroll.addEventListener('click', toggleAutoScroll);
    
    // Inicializar partículas
    initParticles();
    
    // Inicializar timeline
    initTimeline();
    
    // Scroll parallax
    window.addEventListener('scroll', handleParallax, { passive: true });
    
    // Intersection Observer para animar boxes e estatísticas
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visivel');
                // Animar estatísticas
                const stats = entry.target.querySelectorAll('.stat-number');
                stats.forEach(stat => animarEstatistica(stat));
                // Tocar som de torcida
                tocarSomTorcida();
            }
        });
    }, {
        threshold: 0.3,
        rootMargin: '0px'
    });
    
    boxesInfo.forEach(box => {
        observer.observe(box);
    });
    
    // Observer para timeline
    const timelineObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                atualizarTimeline(entry.target);
            }
        });
    }, {
        threshold: 0.5,
        rootMargin: '-20% 0px -20% 0px'
    });
    
    secoesJogador.forEach(secao => {
        timelineObserver.observe(secao);
    });
    
    // Prevenir scroll durante tela inicial
    document.body.style.overflow = 'hidden';
    
    // Adicionar event listeners aos botões de próximo
    const botoesProximo = document.querySelectorAll('.btn-proximo');
    botoesProximo.forEach((botao, index) => {
        botao.addEventListener('click', () => {
            if (index < secoesJogador.length - 1) {
                secoesJogador[index + 1].scrollIntoView({
                    behavior: 'smooth',
                    block: 'center'
                });
            }
        });
    });
    
    // Inicializar Web Audio API para som de torcida
    initAudioContext();
});

// Inicializar sistema de partículas
function initParticles() {
    const ctx = particlesCanvas.getContext('2d');
    
    function resizeCanvas() {
        particlesCanvas.width = window.innerWidth;
        particlesCanvas.height = window.innerHeight;
    }
    
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);
    
    // Criar partículas
    const particleCount = Math.min(100, Math.floor((window.innerWidth * window.innerHeight) / 15000));
    
    for (let i = 0; i < particleCount; i++) {
        particles.push({
            x: Math.random() * particlesCanvas.width,
            y: Math.random() * particlesCanvas.height,
            radius: Math.random() * 2 + 1,
            speedX: (Math.random() - 0.5) * 0.5,
            speedY: (Math.random() - 0.5) * 0.5,
            opacity: Math.random() * 0.5 + 0.3
        });
    }
    
    function animateParticles() {
        ctx.clearRect(0, 0, particlesCanvas.width, particlesCanvas.height);
        
        particles.forEach(particle => {
            // Atualizar posição
            particle.x += particle.speedX;
            particle.y += particle.speedY;
            
            // Rebater nas bordas
            if (particle.x < 0 || particle.x > particlesCanvas.width) particle.speedX *= -1;
            if (particle.y < 0 || particle.y > particlesCanvas.height) particle.speedY *= -1;
            
            // Desenhar partícula
            ctx.beginPath();
            ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(255, 215, 0, ${particle.opacity})`;
            ctx.fill();
            
            // Conectar partículas próximas
            particles.forEach(otherParticle => {
                const dx = particle.x - otherParticle.x;
                const dy = particle.y - otherParticle.y;
                const distance = Math.sqrt(dx * dx + dy * dy);
                
                if (distance < 100) {
                    ctx.beginPath();
                    ctx.moveTo(particle.x, particle.y);
                    ctx.lineTo(otherParticle.x, otherParticle.y);
                    ctx.strokeStyle = `rgba(255, 215, 0, ${0.1 * (1 - distance / 100)})`;
                    ctx.lineWidth = 0.5;
                    ctx.stroke();
                }
            });
        });
        
        animationFrameId = requestAnimationFrame(animateParticles);
    }
    
    animateParticles();
}

// Inicializar timeline
function initTimeline() {
    secoesJogador.forEach((secao, index) => {
        const marker = document.createElement('div');
        marker.className = 'timeline-marker';
        marker.setAttribute('data-nome', jogadoresData[index].nome);
        marker.setAttribute('data-index', index);
        
        const percentage = (index / (secoesJogador.length - 1)) * 100;
        marker.style.top = `${percentage}%`;
        
        marker.addEventListener('click', () => {
            secao.scrollIntoView({ behavior: 'smooth', block: 'center' });
        });
        
        timelineMarkers.appendChild(marker);
    });
}

// Atualizar timeline baseado no scroll
function atualizarTimeline(secaoAtiva) {
    const index = Array.from(secoesJogador).indexOf(secaoAtiva);
    const markers = document.querySelectorAll('.timeline-marker');
    
    markers.forEach((marker, i) => {
        if (i === index) {
            marker.classList.add('ativo');
        } else {
            marker.classList.remove('ativo');
        }
    });
}

// Iniciar experiência
function iniciarExperiencia() {
    if (experienciaIniciada) return;
    
    experienciaIniciada = true;
    
    // Remover travamento do body
    document.body.classList.remove('tela-inicial-ativa');
    document.body.classList.add('header-visivel');
    document.body.style.overflow = 'auto';
    
    // Mostrar header
    const parallaxHeader = document.getElementById('parallaxHeader');
    if (parallaxHeader) {
        parallaxHeader.classList.remove('hidden');
        parallaxHeader.classList.add('visivel');
    }
    
    // Mostrar menu de países (controlado via CSS com classe header-visivel)
    
    // Esconder tela inicial
    telaInicial.classList.add('escondida');
    
    // Mostrar conteúdo principal
    setTimeout(() => {
        conteudoPrincipal.classList.add('visivel');
        telaInicial.style.display = 'none';
        particlesCanvas.classList.add('ativo');
        timeline.classList.add('visivel');
    }, 800);
    
    // Iniciar música
    setTimeout(() => {
        audioMusica.play().catch(err => {
            console.log('Erro ao reproduzir música:', err);
        });
        controlesSuperiores.classList.add('visivel');
    }, 1000);
    
    // Scroll suave para primeira seção
    setTimeout(() => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    }, 1500);
}

// Controle de música
function toggleMusica() {
    if (musicaPausada) {
        audioMusica.play().catch(err => {
            console.log('Erro ao reproduzir música:', err);
        });
        btnMusicaToggle.classList.remove('pausado');
        musicaPausada = false;
    } else {
        audioMusica.pause();
        btnMusicaToggle.classList.add('pausado');
        musicaPausada = true;
    }
}

function ajustarVolume() {
    audioMusica.volume = volumeSlider.value / 100;
}

// Auto-scroll
function toggleAutoScroll() {
    autoScrollAtivo = !autoScrollAtivo;
    btnAutoScroll.classList.toggle('ativo', autoScrollAtivo);
    
    const iconPlay = document.getElementById('icon-play-auto');
    const iconPause = document.getElementById('icon-pause-auto');
    
    if (autoScrollAtivo) {
        iconPlay.style.display = 'none';
        iconPause.style.display = 'block';
        iniciarAutoScroll();
    } else {
        iconPlay.style.display = 'block';
        iconPause.style.display = 'none';
        pararAutoScroll();
    }
}

function iniciarAutoScroll() {
    // Encontrar a seção atual visível
    function getCurrentSectionIndex() {
        const windowHeight = window.innerHeight;
        const scrollY = window.pageYOffset;
        
        for (let i = 0; i < secoesJogador.length; i++) {
            const rect = secoesJogador[i].getBoundingClientRect();
            const sectionTop = rect.top + scrollY;
            
            if (scrollY >= sectionTop - windowHeight * 0.3 && scrollY < sectionTop + rect.height - windowHeight * 0.3) {
                return i;
            }
        }
        return 0;
    }
    
    let currentIndex = getCurrentSectionIndex();
    
    function scrollToNext() {
        if (currentIndex < secoesJogador.length - 1) {
            currentIndex++;
            secoesJogador[currentIndex].scrollIntoView({
                behavior: 'smooth',
                block: 'center'
            });
        } else {
            // Voltar ao início
            currentIndex = 0;
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    }
    
    // Scroll inicial após 2 segundos
    setTimeout(scrollToNext, 2000);
    
    // Continuar scrollando a cada 8 segundos
    autoScrollInterval = setInterval(() => {
        if (autoScrollAtivo) {
            scrollToNext();
        }
    }, 8000);
}

function pararAutoScroll() {
    if (autoScrollInterval) {
        clearInterval(autoScrollInterval);
        autoScrollInterval = null;
    }
}

// Efeito parallax com transição entre jogadores
let ticking = false;
let secaoAtivaAnterior = null;

function handleParallax() {
    if (!experienciaIniciada) return;
    
    if (!ticking) {
        window.requestAnimationFrame(() => {
            const scrollY = window.pageYOffset;
            const windowHeight = window.innerHeight;
            const viewportCenter = scrollY + windowHeight / 2;
            
            secoesJogador.forEach((secao, index) => {
                const rect = secao.getBoundingClientRect();
                const secaoTop = rect.top + scrollY;
                const secaoHeight = rect.height;
                const secaoCenter = secaoTop + secaoHeight / 2;
                
                const isVisible = rect.top < windowHeight && rect.bottom > 0;
                
                if (isVisible) {
                    const scrollProgress = (scrollY - secaoTop + windowHeight) / (windowHeight + secaoHeight);
                    const parallaxOffset = scrollProgress * 100;
                    
                    // Determinar se esta seção está ativa (centro da viewport)
                    const distanciaDoCentro = Math.abs(viewportCenter - secaoCenter);
                    const isAtiva = distanciaDoCentro < windowHeight * 0.4;
                    
                    // Ativar/desativar transição
                    if (isAtiva && !secao.classList.contains('ativa')) {
                        secao.classList.add('ativa');
                        if (secaoAtivaAnterior && secaoAtivaAnterior !== secao) {
                            secaoAtivaAnterior.classList.remove('ativa');
                        }
                        secaoAtivaAnterior = secao;
                    } else if (!isAtiva && secao.classList.contains('ativa')) {
                        secao.classList.remove('ativa');
                    }
                    
                    // Em mobile, não aplicar parallax para manter layout vertical
                    const isMobile = window.innerWidth <= 768;
                    
                    if (!isMobile) {
                        const imagemParallax = secao.querySelector('.imagem-parallax');
                        if (imagemParallax) {
                            const translateY = parallaxOffset * 0.1;
                            imagemParallax.style.transform = `translateY(${translateY}px)`;
                        }
                    }
                    
                    // Ajustar opacidade das imagens baseado no progresso
                    const imgAnterior = secao.querySelector('.img-anterior');
                    const imgAtual = secao.querySelector('.img-atual');
                    
                    if (imgAnterior && imgAtual) {
                        // Calcular progresso de transição baseado na posição do scroll
                        const progressoTransicao = Math.max(0, Math.min(1, 
                            (viewportCenter - secaoTop) / (secaoHeight * 0.5)
                        ));
                        
                        imgAnterior.style.opacity = 1 - progressoTransicao;
                        imgAtual.style.opacity = progressoTransicao;
                    } else {
                        // Para seções sem transição, manter opacidade normal
                        const imgJogador = secao.querySelector('.img-jogador');
                        if (imgJogador) {
                            const opacity = Math.max(0.6, 1 - Math.abs(scrollProgress - 0.5) * 2);
                            imgJogador.style.opacity = opacity;
                        }
                    }
                }
            });
            
            ticking = false;
        });
        
        ticking = true;
    }
}

// Animar estatísticas
function animarEstatistica(element) {
    const target = parseInt(element.getAttribute('data-target'));
    const duration = 2000;
    const start = performance.now();
    const startValue = 0;
    
    function animate(currentTime) {
        const elapsed = currentTime - start;
        const progress = Math.min(elapsed / duration, 1);
        
        // Easing function (ease-out)
        const easeOut = 1 - Math.pow(1 - progress, 3);
        const currentValue = Math.floor(startValue + (target - startValue) * easeOut);
        
        element.textContent = currentValue;
        
        if (progress < 1) {
            requestAnimationFrame(animate);
        } else {
            element.textContent = target;
        }
    }
    
    requestAnimationFrame(animate);
}

// Inicializar Web Audio API para som de torcida
let lastTorcidaTime = 0;
const TORCIDA_COOLDOWN = 2000; // 2 segundos entre sons

function initAudioContext() {
    try {
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
        torcidaGainNode = audioContext.createGain();
        
        // Adicionar filtro passa-baixa para suavizar o som
        const lowpassFilter = audioContext.createBiquadFilter();
        lowpassFilter.type = 'lowpass';
        lowpassFilter.frequency.value = 800; // Frequência mais baixa = som mais suave
        lowpassFilter.Q.value = 1;
        
        torcidaGainNode.connect(lowpassFilter);
        lowpassFilter.connect(audioContext.destination);
        torcidaGainNode.gain.value = 0.08; // Volume muito mais baixo
    } catch (e) {
        console.log('Web Audio API não suportada:', e);
    }
}

// Tocar som de torcida
function tocarSomTorcida() {
    if (!audioContext || !torcidaGainNode) return;
    
    // Prevenir múltiplos sons simultâneos
    const now = Date.now();
    if (now - lastTorcidaTime < TORCIDA_COOLDOWN) {
        return;
    }
    lastTorcidaTime = now;
    
    // Criar som de torcida mais suave usando múltiplos osciladores
    const duration = 0.3; // Duração mais curta
    const sampleRate = audioContext.sampleRate;
    const frameCount = sampleRate * duration;
    const buffer = audioContext.createBuffer(1, frameCount, sampleRate);
    const data = buffer.getChannelData(0);
    
    // Gerar som mais suave com envelope de fade
    for (let i = 0; i < frameCount; i++) {
        const t = i / sampleRate;
        const progress = i / frameCount;
        
        // Envelope de fade in/out para evitar estouro
        const envelope = Math.sin(progress * Math.PI);
        
        // Som mais suave: menos ruído, mais tom
        const tone1 = Math.sin(t * 150 * 2 * Math.PI) * 0.1; // Tom baixo
        const tone2 = Math.sin(t * 200 * 2 * Math.PI) * 0.08; // Tom médio
        const noise = (Math.random() * 2 - 1) * 0.05; // Ruído muito reduzido
        
        // Aplicar envelope e combinar
        data[i] = (tone1 + tone2 + noise) * envelope;
    }
    
    const source = audioContext.createBufferSource();
    source.buffer = buffer;
    source.connect(torcidaGainNode);
    source.start();
}

// Melhorar transição entre seções
function suavizarTransicao() {
    secoesJogador.forEach((secao, index) => {
        const rect = secao.getBoundingClientRect();
        const isActive = rect.top < window.innerHeight / 2 && rect.bottom > window.innerHeight / 2;
        
        if (isActive) {
            secao.style.zIndex = '10';
        } else {
            secao.style.zIndex = '1';
        }
    });
}

window.addEventListener('scroll', suavizarTransicao, { passive: true });

// Adicionar suporte para teclado (acessibilidade)
document.addEventListener('keydown', (e) => {
    if (e.key === ' ' || e.key === 'Enter') {
        if (!experienciaIniciada && document.activeElement === btnComecar) {
            e.preventDefault();
            iniciarExperiencia();
        }
    }
    
    if (e.key === 'm' || e.key === 'M') {
        if (experienciaIniciada) {
            toggleMusica();
        }
    }
    
    if (e.key === 'a' || e.key === 'A') {
        if (experienciaIniciada) {
            toggleAutoScroll();
        }
    }
});

// Prevenir autoplay bloqueado - tentar reproduzir após primeira interação
document.addEventListener('click', () => {
    if (experienciaIniciada && audioMusica.paused && !musicaPausada) {
        audioMusica.play().catch(() => {
            // Ignorar erros de autoplay
        });
    }
}, { once: true });

// Limpar recursos ao sair
window.addEventListener('beforeunload', () => {
    if (animationFrameId) {
        cancelAnimationFrame(animationFrameId);
    }
    if (autoScrollInterval) {
        clearInterval(autoScrollInterval);
    }
    if (audioContext) {
        audioContext.close();
    }
});
