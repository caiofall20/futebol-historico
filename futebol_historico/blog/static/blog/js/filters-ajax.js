// ===========================================
// FILTROS AJAX E BUSCA EM TEMPO REAL
// ===========================================

class FiltersManager {
    constructor() {
        this.debounceTimer = null;
        this.currentPage = 1;
        this.filters = {
            q: '',
            nacionalidade: '',
            posicao: '',
            periodo: ''
        };
        this.init();
    }

    init() {
        // Carregar filtros da URL ao iniciar
        this.loadFiltersFromURL();
        
        // Aplicar filtros iniciais
        this.applyFilters();
        
        // Event listeners
        this.setupEventListeners();
        
        // Observar mudanças na URL (botão voltar/avançar)
        window.addEventListener('popstate', () => {
            this.loadFiltersFromURL();
            this.applyFilters();
        });
    }

    setupEventListeners() {
        // Busca em tempo real com debounce
        const searchInput = document.getElementById('filtroNome');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                this.debounceFilter(() => {
                    this.filters.q = e.target.value.trim();
                    this.currentPage = 1;
                    this.updateURL();
                    this.applyFilters();
                });
            });
        }

        // Filtros de dropdown
        const nacionalidadeFilter = document.getElementById('filtroNacionalidade');
        if (nacionalidadeFilter) {
            nacionalidadeFilter.addEventListener('change', (e) => {
                this.filters.nacionalidade = e.target.value;
                this.currentPage = 1;
                this.updateURL();
                this.applyFilters();
            });
        }

        const posicaoFilter = document.getElementById('filtroPosicao');
        if (posicaoFilter) {
            posicaoFilter.addEventListener('change', (e) => {
                this.filters.posicao = e.target.value;
                this.currentPage = 1;
                this.updateURL();
                this.applyFilters();
            });
        }

        const periodoFilter = document.getElementById('filtroEpoca');
        if (periodoFilter) {
            periodoFilter.addEventListener('change', (e) => {
                this.filters.periodo = e.target.value;
                this.currentPage = 1;
                this.updateURL();
                this.applyFilters();
            });
        }

        // Botão limpar filtros
        const clearBtn = document.getElementById('limparFiltros');
        if (clearBtn) {
            clearBtn.addEventListener('click', () => {
                this.clearFilters();
            });
        }
    }

    debounceFilter(callback, delay = 300) {
        clearTimeout(this.debounceTimer);
        this.debounceTimer = setTimeout(callback, delay);
    }

    loadFiltersFromURL() {
        const params = new URLSearchParams(window.location.search);
        this.filters.q = params.get('q') || '';
        this.filters.nacionalidade = params.get('nacionalidade') || '';
        this.filters.posicao = params.get('posicao') || '';
        this.filters.periodo = params.get('periodo') || '';
        this.currentPage = parseInt(params.get('page')) || 1;

        // Atualizar campos do formulário
        const searchInput = document.getElementById('filtroNome');
        if (searchInput) searchInput.value = this.filters.q;

        const nacionalidadeFilter = document.getElementById('filtroNacionalidade');
        if (nacionalidadeFilter) nacionalidadeFilter.value = this.filters.nacionalidade;

        const posicaoFilter = document.getElementById('filtroPosicao');
        if (posicaoFilter) posicaoFilter.value = this.filters.posicao;

        const periodoFilter = document.getElementById('filtroEpoca');
        if (periodoFilter) periodoFilter.value = this.filters.periodo;
    }

    updateURL() {
        const params = new URLSearchParams();
        
        if (this.filters.q) params.set('q', this.filters.q);
        if (this.filters.nacionalidade) params.set('nacionalidade', this.filters.nacionalidade);
        if (this.filters.posicao) params.set('posicao', this.filters.posicao);
        if (this.filters.periodo) params.set('periodo', this.filters.periodo);
        if (this.currentPage > 1) params.set('page', this.currentPage);

        const newURL = window.location.pathname + (params.toString() ? '?' + params.toString() : '');
        window.history.pushState({}, '', newURL);
    }

    clearFilters() {
        this.filters = {
            q: '',
            nacionalidade: '',
            posicao: '',
            periodo: ''
        };
        this.currentPage = 1;
        
        // Limpar campos do formulário
        const searchInput = document.getElementById('filtroNome');
        if (searchInput) searchInput.value = '';

        const nacionalidadeFilter = document.getElementById('filtroNacionalidade');
        if (nacionalidadeFilter) nacionalidadeFilter.value = '';

        const posicaoFilter = document.getElementById('filtroPosicao');
        if (posicaoFilter) posicaoFilter.value = '';

        const periodoFilter = document.getElementById('filtroEpoca');
        if (periodoFilter) periodoFilter.value = '';

        this.updateURL();
        this.applyFilters();
    }

    async applyFilters() {
        const container = document.querySelector('.jogadores-grid');
        if (!container) return;

        // Mostrar skeleton loader
        if (window.skeletonLoader) {
            const skeletons = window.skeletonLoader.showSkeletonForAjax('.jogadores-grid', 'jogador');
        } else {
            this.showLoadingState(container);
        }

        try {
            // Construir URL da API
            const params = new URLSearchParams();
            if (this.filters.q) params.set('q', this.filters.q);
            if (this.filters.nacionalidade) params.set('nacionalidade', this.filters.nacionalidade);
            if (this.filters.posicao) params.set('posicao', this.filters.posicao);
            if (this.filters.periodo) params.set('periodo', this.filters.periodo);
            if (this.currentPage > 1) params.set('page', this.currentPage);

            const response = await fetch(`/api/jogadores/?${params.toString()}`);
            const data = await response.json();

            if (data.success) {
                this.renderResults(data.results, container);
                this.updatePagination(data.pagination);
                this.updateResultCounter(data.pagination.total_count);
            } else {
                this.showError(container, data.message || 'Erro ao buscar jogadores');
            }
        } catch (error) {
            console.error('Erro ao buscar jogadores:', error);
            this.showError(container, 'Erro ao carregar jogadores. Tente novamente.');
        }
    }

    showLoadingState(container) {
        container.innerHTML = '<div class="loading-message">Carregando jogadores...</div>';
    }

    renderResults(results, container) {
        if (results.length === 0) {
            this.showEmptyState(container);
            return;
        }

        // Limpar container
        container.innerHTML = '';

        // Renderizar cards (usar template do Django ou criar HTML)
        results.forEach(jogador => {
            const card = this.createJogadorCard(jogador);
            container.appendChild(card);
        });

        // Fade in animation
        container.classList.add('fade-in');
    }

    createJogadorCard(jogador) {
        const card = document.createElement('article');
        card.className = 'jogador-card';
        card.dataset.nome = jogador.nome;
        card.dataset.nacionalidade = jogador.nacionalidade;

        // Para a página de listagem, usar carta primeiro, depois imagem como fallback
        const imageUrl = jogador.carta_url || jogador.imagem_url || '';
        const flagClass = jogador.flag_code ? `flag-icon-${jogador.flag_code}` : '';

        card.innerHTML = `
            <div class="jogador-card-image-wrapper">
                <div class="jogador-image-container">
                    ${jogador.flag_code ? `<div class="jogador-flag-badge"><span class="flag-icon ${flagClass}"></span></div>` : ''}
                    ${imageUrl ? `<img src="${imageUrl}" alt="${jogador.nome}" loading="lazy">` : '<div class="jogador-placeholder-icon">⚽</div>'}
                </div>
                <div class="jogador-info-overlay">
                    <h3 class="jogador-name-overlay">${jogador.nome}</h3>
                    <div class="jogador-stats">
                        <div class="jogador-stat-item">
                            <span class="jogador-stat-label">TÍTULOS</span>
                            <span class="jogador-stat-value">${jogador.total_trofeus}</span>
                        </div>
                        <div class="jogador-stat-item">
                            <span class="jogador-stat-label">PERÍODO DE ATIVIDADE</span>
                            <span class="jogador-stat-value">
                                ${jogador.inicio_carreira ? jogador.inicio_carreira + '-' + (jogador.fim_carreira || 'Atual') : '—'}
                            </span>
                        </div>
                        <div class="jogador-stat-item">
                            <span class="jogador-stat-label">PÉ DOMINANTE</span>
                            <span class="jogador-stat-value">${jogador.perna || '—'}</span>
                        </div>
                        <div class="jogador-stat-item">
                            <span class="jogador-stat-label">NACIONALIDADE</span>
                            <span class="jogador-stat-value">
                                ${jogador.flag_code ? `<span class="flag-icon ${flagClass}"></span>` : jogador.nacionalidade}
                            </span>
                        </div>
                    </div>
                    ${jogador.biografia_preview ? `<div class="jogador-bio-preview"><div class="jogador-bio-preview-title">BIOGRAFIA</div>${jogador.biografia_preview}</div>` : ''}
                    <a href="/jogadores/${jogador.id}/" class="btn-ver-mais">Ver Mais</a>
                </div>
            </div>
        `;

        return card;
    }

    showEmptyState(container) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">🔍</div>
                <h3>Nenhum jogador encontrado</h3>
                <p>Não encontramos jogadores com os filtros selecionados.</p>
                <button onclick="window.filtersManager.clearFilters()" class="btn-clear-filters">
                    Limpar Filtros
                </button>
            </div>
        `;
    }

    showError(container, message) {
        container.innerHTML = `
            <div class="error-state">
                <div class="error-icon">⚠️</div>
                <h3>Erro ao carregar</h3>
                <p>${message}</p>
                <button onclick="window.filtersManager.applyFilters()" class="btn-retry">
                    Tentar Novamente
                </button>
            </div>
        `;
    }

    updatePagination(pagination) {
        // Atualizar controles de paginação se existirem
        const paginationContainer = document.querySelector('.pagination');
        if (!paginationContainer) return;

        // Implementar controles de paginação
        // ...
    }

    updateResultCounter(total) {
        const counter = document.getElementById('result-counter');
        if (counter) {
            counter.textContent = `${total} jogador${total !== 1 ? 'es' : ''} encontrado${total !== 1 ? 's' : ''}`;
        }
    }
}

// Inicializar quando DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    // Só inicializar se estivermos na página de jogadores
    if (document.querySelector('.jogadores-grid')) {
        window.filtersManager = new FiltersManager();
    }
});


