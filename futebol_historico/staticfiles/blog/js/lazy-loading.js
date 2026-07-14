// ===========================================
// LAZY LOADING OTIMIZADO DE IMAGENS
// ===========================================

class LazyImageLoader {
    constructor() {
        this.imageObserver = null;
        this.init();
    }

    init() {
        // Verificar suporte para Intersection Observer
        if ('IntersectionObserver' in window) {
            this.setupIntersectionObserver();
        } else {
            // Fallback para navegadores antigos
            this.loadAllImages();
        }

        // Carregar imagens visíveis imediatamente
        this.loadVisibleImages();
    }

    setupIntersectionObserver() {
        const options = {
            root: null,
            rootMargin: '50px', // Carregar 50px antes de entrar na viewport
            threshold: 0.01
        };

        this.imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.loadImage(entry.target);
                    observer.unobserve(entry.target);
                }
            });
        }, options);

        // Observar todas as imagens com data-src
        document.querySelectorAll('img[data-src]').forEach(img => {
            this.imageObserver.observe(img);
        });
    }

    loadImage(img) {
        const src = img.getAttribute('data-src');
        if (!src) return;

        // Criar nova imagem para pré-carregar
        const imageLoader = new Image();
        
        imageLoader.onload = () => {
            img.src = src;
            img.removeAttribute('data-src');
            img.classList.add('loaded');
            img.classList.remove('lazy');
            
            // Fade in animation
            img.style.opacity = '0';
            img.style.transition = 'opacity 0.3s ease';
            setTimeout(() => {
                img.style.opacity = '1';
            }, 10);
        };

        imageLoader.onerror = () => {
            img.src = '/static/blog/images/placeholder.jpg'; // Placeholder em caso de erro
            img.alt = 'Imagem não disponível';
            img.classList.add('error');
        };

        imageLoader.src = src;
    }

    loadVisibleImages() {
        // Carregar imagens que já estão visíveis (sem scroll)
        const images = document.querySelectorAll('img[data-src]');
        images.forEach(img => {
            const rect = img.getBoundingClientRect();
            const isVisible = (
                rect.top >= 0 &&
                rect.left >= 0 &&
                rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
                rect.right <= (window.innerWidth || document.documentElement.clientWidth)
            );

            if (isVisible) {
                this.loadImage(img);
            }
        });
    }

    loadAllImages() {
        // Fallback: carregar todas as imagens
        document.querySelectorAll('img[data-src]').forEach(img => {
            this.loadImage(img);
        });
    }

    // Método para adicionar novas imagens dinamicamente
    observeNewImages(container) {
        if (this.imageObserver && container) {
            container.querySelectorAll('img[data-src]').forEach(img => {
                this.imageObserver.observe(img);
            });
        }
    }
}

// Inicializar quando DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    window.lazyImageLoader = new LazyImageLoader();
    
    // Observar mudanças dinâmicas no DOM (para AJAX)
    const mutationObserver = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            mutation.addedNodes.forEach((node) => {
                if (node.nodeType === 1) { // Element node
                    if (node.tagName === 'IMG' && node.hasAttribute('data-src')) {
                        if (window.lazyImageLoader) {
                            window.lazyImageLoader.loadImage(node);
                        }
                    } else if (node.querySelectorAll) {
                        const images = node.querySelectorAll('img[data-src]');
                        images.forEach(img => {
                            if (window.lazyImageLoader) {
                                if (window.lazyImageLoader.imageObserver) {
                                    window.lazyImageLoader.imageObserver.observe(img);
                                } else {
                                    window.lazyImageLoader.loadImage(img);
                                }
                            }
                        });
                    }
                }
            });
        });
    });

    mutationObserver.observe(document.body, {
        childList: true,
        subtree: true
    });
});

// CSS para imagens lazy
const style = document.createElement('style');
style.textContent = `
    img.lazy {
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    img.lazy.loaded {
        opacity: 1;
    }
    
    img[data-src] {
        background: linear-gradient(90deg, 
            rgba(255, 255, 255, 0.05) 0px,
            rgba(255, 255, 255, 0.1) 40px,
            rgba(255, 255, 255, 0.05) 80px
        );
        background-size: 200px 100%;
        animation: skeleton-loading 1.5s ease-in-out infinite;
    }
    
    @keyframes skeleton-loading {
        0% {
            background-position: -200px 0;
        }
        100% {
            background-position: calc(200px + 100%) 0;
        }
    }
`;
document.head.appendChild(style);


