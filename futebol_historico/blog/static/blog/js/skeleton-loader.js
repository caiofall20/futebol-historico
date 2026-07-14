// ===========================================
// SKELETON LOADER MANAGER
// ===========================================
// Gerencia estados de loading com skeleton screens

class SkeletonLoader {
    constructor() {
        this.skeletons = new Map();
        this.init();
    }

    init() {
        // Observar quando imagens terminam de carregar
        this.observeImages();
        
        // Observar quando conteúdo dinâmico é carregado
        this.observeContent();
    }

    /**
     * Cria um skeleton loader para cards de jogadores
     */
    createJogadorCardSkeleton(count = 12) {
        const container = document.querySelector('.jogadores-grid');
        if (!container) return;

        const skeletons = [];
        for (let i = 0; i < count; i++) {
            const skeleton = document.createElement('div');
            skeleton.className = 'jogador-card-skeleton';
            skeleton.innerHTML = `
                <div class="skeleton-image"></div>
                <div class="skeleton-text title"></div>
                <div class="skeleton-text"></div>
                <div class="skeleton-text short"></div>
                <div class="skeleton-stats">
                    <div class="skeleton-stat-item"></div>
                    <div class="skeleton-stat-item"></div>
                    <div class="skeleton-stat-item"></div>
                </div>
            `;
            container.appendChild(skeleton);
            skeletons.push(skeleton);
        }
        
        return skeletons;
    }

    /**
     * Remove skeletons quando conteúdo real é carregado
     */
    removeSkeletons(skeletons) {
        if (Array.isArray(skeletons)) {
            skeletons.forEach(skeleton => {
                if (skeleton && skeleton.parentNode) {
                    skeleton.style.transition = 'opacity 0.3s ease';
                    skeleton.style.opacity = '0';
                    setTimeout(() => {
                        skeleton.remove();
                    }, 300);
                }
            });
        }
    }

    /**
     * Observa quando imagens terminam de carregar
     */
    observeImages() {
        const images = document.querySelectorAll('img[data-src], img[src]');
        
        images.forEach(img => {
            if (img.complete) {
                this.handleImageLoad(img);
            } else {
                img.addEventListener('load', () => this.handleImageLoad(img));
                img.addEventListener('error', () => this.handleImageError(img));
            }
        });
    }

    handleImageLoad(img) {
        img.classList.add('fade-in');
        img.style.opacity = '0';
        setTimeout(() => {
            img.style.transition = 'opacity 0.5s ease';
            img.style.opacity = '1';
        }, 10);
    }

    handleImageError(img) {
        img.style.opacity = '0.3';
        img.alt = 'Imagem não disponível';
    }

    /**
     * Observa mudanças no conteúdo
     */
    observeContent() {
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                mutation.addedNodes.forEach((node) => {
                    if (node.nodeType === 1) { // Element node
                        // Se um card real foi adicionado, remover skeletons
                        if (node.classList && node.classList.contains('jogador-card')) {
                            const skeletons = document.querySelectorAll('.jogador-card-skeleton');
                            this.removeSkeletons(Array.from(skeletons));
                        }
                    }
                });
            });
        });

        const container = document.querySelector('.jogadores-grid');
        if (container) {
            observer.observe(container, {
                childList: true,
                subtree: true
            });
        }
    }

    /**
     * Mostra loading overlay global
     */
    showGlobalLoader() {
        const overlay = document.createElement('div');
        overlay.className = 'loading-overlay';
        overlay.id = 'global-loader';
        overlay.innerHTML = '<div class="spinner"></div>';
        document.body.appendChild(overlay);
    }

    /**
     * Remove loading overlay global
     */
    hideGlobalLoader() {
        const overlay = document.getElementById('global-loader');
        if (overlay) {
            overlay.style.opacity = '0';
            overlay.style.transition = 'opacity 0.3s ease';
            setTimeout(() => {
                overlay.remove();
            }, 300);
        }
    }

    /**
     * Mostra skeleton enquanto carrega conteúdo via AJAX
     */
    showSkeletonForAjax(containerSelector, skeletonType = 'jogador') {
        const container = document.querySelector(containerSelector);
        if (!container) return;

        // Limpar conteúdo existente
        container.innerHTML = '';

        // Adicionar skeletons
        if (skeletonType === 'jogador') {
            return this.createJogadorCardSkeleton(12);
        }
    }
}

// Inicializar quando DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    window.skeletonLoader = new SkeletonLoader();
    
    // Mostrar skeletons se não houver conteúdo ainda
    const jogadoresGrid = document.querySelector('.jogadores-grid');
    if (jogadoresGrid && jogadoresGrid.children.length === 0) {
        window.skeletonLoader.createJogadorCardSkeleton(12);
    }
});

// Exportar para uso global
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SkeletonLoader;
}





