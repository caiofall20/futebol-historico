// ===========================================
// OTIMIZAÇÕES DE PERFORMANCE
// ===========================================

// ===========================================
// LAZY LOADING DE IMAGENS
// ===========================================

class LazyImageLoader {
    constructor() {
        this.imageObserver = null;
        this.init();
    }

    init() {
        if ('IntersectionObserver' in window) {
            this.imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        this.loadImage(img);
                        observer.unobserve(img);
                    }
                });
            }, {
                rootMargin: '50px 0px',
                threshold: 0.01
            });

            this.observeImages();
        } else {
            // Fallback para navegadores sem IntersectionObserver
            this.loadAllImages();
        }
    }

    observeImages() {
        const lazyImages = document.querySelectorAll('img[data-src]');
        lazyImages.forEach(img => this.imageObserver.observe(img));
    }

    loadImage(img) {
        const src = img.dataset.src;
        if (src) {
            img.src = src;
            img.classList.remove('lazy');
            img.classList.add('loaded');
            
            // Adicionar transição suave
            img.style.opacity = '0';
            img.onload = () => {
                img.style.transition = 'opacity 0.3s ease';
                img.style.opacity = '1';
            };
        }
    }

    loadAllImages() {
        const lazyImages = document.querySelectorAll('img[data-src]');
        lazyImages.forEach(img => this.loadImage(img));
    }
}

// ===========================================
// DEBOUNCE PARA FILTROS
// ===========================================

class FilterManager {
    constructor() {
        this.debounceTimer = null;
        this.debounceDelay = 300;
        this.init();
    }

    init() {
        const filterInputs = document.querySelectorAll('.filter-input input, .filter-input select');
        filterInputs.forEach(input => {
            input.addEventListener('input', this.debounce(this.applyFilters.bind(this), this.debounceDelay));
        });
    }

    debounce(func, wait) {
        return (...args) => {
            clearTimeout(this.debounceTimer);
            this.debounceTimer = setTimeout(() => func.apply(this, args), wait);
        };
    }

    applyFilters() {
        const filters = this.getFilterValues();
        const items = document.querySelectorAll('.jogador-card, .copa-item');
        
        items.forEach(item => {
            const shouldShow = this.matchesFilters(item, filters);
            item.style.display = shouldShow ? 'block' : 'none';
        });
    }

    getFilterValues() {
        return {
            nome: document.getElementById('filtroNome')?.value.toLowerCase() || '',
            nacionalidade: document.getElementById('filtroNacionalidade')?.value.toLowerCase() || '',
            posicao: document.getElementById('filtroPosicao')?.value || '',
            epoca: document.getElementById('filtroEpoca')?.value || ''
        };
    }

    matchesFilters(item, filters) {
        const nome = item.dataset.nome?.toLowerCase() || '';
        const nacionalidade = item.dataset.nacionalidade?.toLowerCase() || '';
        const posicao = item.dataset.posicao || '';
        const epoca = item.dataset.epoca || '';

        return (
            (filters.nome === '' || nome.includes(filters.nome)) &&
            (filters.nacionalidade === '' || nacionalidade.includes(filters.nacionalidade)) &&
            (filters.posicao === '' || posicao === filters.posicao) &&
            (filters.epoca === '' || epoca.includes(filters.epoca))
        );
    }
}

// ===========================================
// SKELETON LOADING
// ===========================================

class SkeletonLoader {
    constructor() {
        this.init();
    }

    init() {
        this.createSkeletonCards();
        this.loadContent();
    }

    createSkeletonCards() {
        const container = document.getElementById('jogadoresContainer');
        if (!container) return;

        const skeletonHTML = `
            <div class="skeleton-card">
                <div class="skeleton-image"></div>
                <div class="skeleton-text"></div>
                <div class="skeleton-text short"></div>
            </div>
        `;

        // Adicionar 6 skeletons
        for (let i = 0; i < 6; i++) {
            container.insertAdjacentHTML('beforeend', skeletonHTML);
        }
    }

    loadContent() {
        // Simular carregamento
        setTimeout(() => {
            const skeletons = document.querySelectorAll('.skeleton-card');
            skeletons.forEach(skeleton => {
                skeleton.style.opacity = '0';
                setTimeout(() => skeleton.remove(), 300);
            });
        }, 1000);
    }
}

// ===========================================
// PRELOAD DE RECURSOS CRÍTICOS
// ===========================================

class ResourcePreloader {
    constructor() {
        this.init();
    }

    init() {
        this.preloadCriticalImages();
        this.preloadFonts();
    }

    preloadCriticalImages() {
        const criticalImages = [
            '/static/blog/images/bola-adidas.png',
            '/static/blog/images/img-home.svg'
        ];

        criticalImages.forEach(src => {
            const link = document.createElement('link');
            link.rel = 'preload';
            link.as = 'image';
            link.href = src;
            document.head.appendChild(link);
        });
    }

    preloadFonts() {
        const fontLinks = [
            'https://fonts.googleapis.com/css2?family=Georama:ital,wdth,wght@0,87.5,100..900;1,87.5,100..900&display=swap',
            'https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap'
        ];

        fontLinks.forEach(href => {
            const link = document.createElement('link');
            link.rel = 'preload';
            link.as = 'style';
            link.href = href;
            link.onload = () => link.rel = 'stylesheet';
            document.head.appendChild(link);
        });
    }
}

// ===========================================
// OTIMIZAÇÃO DE SCROLL
// ===========================================

class ScrollOptimizer {
    constructor() {
        this.ticking = false;
        this.init();
    }

    init() {
        window.addEventListener('scroll', this.throttle(this.handleScroll.bind(this), 16));
    }

    throttle(func, limit) {
        return (...args) => {
            if (!this.ticking) {
                func.apply(this, args);
                this.ticking = true;
                setTimeout(() => this.ticking = false, limit);
            }
        };
    }

    handleScroll() {
        // Parallax suave para estrelas
        const stars = document.getElementById('stars');
        const stars2 = document.getElementById('stars2');
        const stars3 = document.getElementById('stars3');
        
        if (stars) {
            const scrolled = window.pageYOffset;
            const rate = scrolled * -0.5;
            stars.style.transform = `translateY(${rate}px)`;
        }
        
        if (stars2) {
            const rate = scrolled * -0.3;
            stars2.style.transform = `translateY(${rate}px)`;
        }
        
        if (stars3) {
            const rate = scrolled * -0.1;
            stars3.style.transform = `translateY(${rate}px)`;
        }
    }
}

// ===========================================
// CACHE DE DADOS
// ===========================================

class DataCache {
    constructor() {
        this.cache = new Map();
        this.maxSize = 50;
    }

    set(key, value, ttl = 300000) { // 5 minutos por padrão
        if (this.cache.size >= this.maxSize) {
            const firstKey = this.cache.keys().next().value;
            this.cache.delete(firstKey);
        }

        this.cache.set(key, {
            value,
            timestamp: Date.now(),
            ttl
        });
    }

    get(key) {
        const item = this.cache.get(key);
        if (!item) return null;

        if (Date.now() - item.timestamp > item.ttl) {
            this.cache.delete(key);
            return null;
        }

        return item.value;
    }

    clear() {
        this.cache.clear();
    }
}

// ===========================================
// INICIALIZAÇÃO
// ===========================================

document.addEventListener('DOMContentLoaded', () => {
    // Inicializar otimizações
    new LazyImageLoader();
    new FilterManager();
    new SkeletonLoader();
    new ResourcePreloader();
    new ScrollOptimizer();
    
    // Cache global
    window.dataCache = new DataCache();
    
    console.log('🚀 Performance optimizations loaded!');
});

// ===========================================
// SERVICE WORKER (OPCIONAL)
// ===========================================

if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/static/blog/js/sw.js')
            .then(registration => {
                console.log('SW registered: ', registration);
            })
            .catch(registrationError => {
                console.log('SW registration failed: ', registrationError);
            });
    });
}
