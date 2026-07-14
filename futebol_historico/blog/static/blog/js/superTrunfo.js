// ===========================================
// SUPER TRUNFO - INTERAÇÕES DOS CARDS
// ===========================================

class SuperTrunfoManager {
    constructor() {
        this.cards = [];
        this.selectedCard = null;
        this.init();
    }

    init() {
        this.setupCards();
        this.setupEventListeners();
        this.animateCards();
    }

    setupCards() {
        this.cards = document.querySelectorAll('.super-trunfo-card');
        
        // Adicionar delay escalonado para animação
        this.cards.forEach((card, index) => {
            card.style.animationDelay = `${index * 0.2}s`;
        });
    }

    setupEventListeners() {
        this.cards.forEach(card => {
            // Hover effects
            card.addEventListener('mouseenter', () => this.onCardHover(card));
            card.addEventListener('mouseleave', () => this.onCardLeave(card));
            
            // Click para selecionar
            card.addEventListener('click', () => this.onCardClick(card));
            
            // Touch para mobile
            card.addEventListener('touchstart', (e) => {
                e.preventDefault();
                this.onCardTouch(card);
            });
        });

        // Botão "Ver Todas as Cartas"
        const showAllBtn = document.querySelector('button[onclick="showAllCards()"]');
        if (showAllBtn) {
            showAllBtn.addEventListener('click', () => this.showAllCards());
        }
    }

    onCardHover(card) {
        // Adicionar efeito de brilho
        card.classList.add('card-hover');
        
        // Animar estrelas
        const stars = card.querySelectorAll('.star.active');
        stars.forEach((star, index) => {
            setTimeout(() => {
                star.style.animation = 'starGlow 0.5s ease-in-out';
            }, index * 100);
        });
    }

    onCardLeave(card) {
        card.classList.remove('card-hover');
        
        // Reset das estrelas
        const stars = card.querySelectorAll('.star.active');
        stars.forEach(star => {
            star.style.animation = '';
        });
    }

    onCardClick(card) {
        // Remover seleção anterior
        if (this.selectedCard) {
            this.selectedCard.classList.remove('card-selected');
        }
        
        // Selecionar novo card
        this.selectedCard = card;
        card.classList.add('card-selected');
        
        // Efeito de seleção
        this.showCardDetails(card);
        
        // Animar seleção
        card.style.transform = 'scale(1.05)';
        setTimeout(() => {
            card.style.transform = '';
        }, 200);
    }

    onCardTouch(card) {
        // Para mobile, usar touch
        this.onCardClick(card);
    }

    showCardDetails(card) {
        const country = card.dataset.country;
        const countryName = card.querySelector('.country-name').textContent;
        
        // Criar modal ou tooltip com detalhes
        this.createCardModal(card, countryName);
    }

    createCardModal(card, countryName) {
        // Remover modal existente
        const existingModal = document.querySelector('.card-modal');
        if (existingModal) {
            existingModal.remove();
        }

        // Criar modal
        const modal = document.createElement('div');
        modal.className = 'card-modal';
        modal.innerHTML = `
            <div class="modal-backdrop"></div>
            <div class="modal-content">
                <div class="modal-header">
                    <h3>${countryName} - Detalhes Completos</h3>
                    <button class="modal-close">&times;</button>
                </div>
                <div class="modal-body">
                    ${this.getDetailedStats(card)}
                </div>
                <div class="modal-footer">
                    <button class="btn btn-primary">Comparar</button>
                    <button class="btn btn-secondary">Fechar</button>
                </div>
            </div>
        `;

        document.body.appendChild(modal);

        // Event listeners do modal
        modal.querySelector('.modal-close').addEventListener('click', () => {
            modal.remove();
        });

        modal.querySelector('.modal-backdrop').addEventListener('click', () => {
            modal.remove();
        });

        modal.querySelector('.btn-secondary').addEventListener('click', () => {
            modal.remove();
        });

        // Animar entrada
        setTimeout(() => {
            modal.classList.add('modal-show');
        }, 10);
    }

    getDetailedStats(card) {
        const stats = card.querySelectorAll('.stat-item');
        let detailedHTML = '<div class="detailed-stats">';
        
        stats.forEach(stat => {
            const label = stat.querySelector('.stat-label').textContent;
            const value = stat.querySelector('.stat-value').textContent;
            detailedHTML += `
                <div class="detailed-stat">
                    <span class="stat-label">${label}</span>
                    <div class="stat-bar">
                        <div class="stat-fill" style="width: ${this.getStatPercentage(value, label)}%"></div>
                    </div>
                    <span class="stat-value">${value}</span>
                </div>
            `;
        });
        
        detailedHTML += '</div>';
        return detailedHTML;
    }

    getStatPercentage(value, label) {
        const maxValues = {
            '🏆 Títulos': 5,
            '⚽ Gols': 250,
            '🎯 Partidas': 120,
            '⭐ Rating': 100
        };
        
        const max = maxValues[label] || 100;
        return (parseInt(value) / max) * 100;
    }

    animateCards() {
        // Animar entrada dos cards
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('card-enter');
                }
            });
        }, { threshold: 0.1 });

        this.cards.forEach(card => {
            observer.observe(card);
        });
    }

    showAllCards() {
        // Implementar lógica para mostrar todas as cartas
        console.log('Mostrando todas as cartas...');
        
        // Adicionar mais cartas dinamicamente
        this.addMoreCards();
    }

    addMoreCards() {
        const container = document.querySelector('.row.justify-content-center');
        
        // Cartas adicionais
        const additionalCards = [
            {
                country: 'FR',
                name: 'França',
                flag: 'franca.png',
                titles: 2,
                goals: 120,
                matches: 70,
                rating: 88,
                rarity: 'Raro',
                description: 'A "Les Bleus" é conhecida pela diversidade e talento. Conquistou 2 títulos mundiais e é famosa por jogadores como Zidane e Mbappé.',
                power: 3
            },
            {
                country: 'GB',
                name: 'Inglaterra',
                flag: 'inglaterra.png',
                titles: 1,
                goals: 100,
                matches: 70,
                rating: 85,
                rarity: 'Comum',
                description: 'A "Three Lions" inventou o futebol moderno. Conquistou 1 título mundial em casa e é conhecida pela tradição.',
                power: 2
            },
            {
                country: 'UY',
                name: 'Uruguai',
                flag: 'uruguai.png',
                titles: 2,
                goals: 80,
                matches: 56,
                rating: 82,
                rarity: 'Comum',
                description: 'A "Celeste" foi a primeira campeã mundial. Conquistou 2 títulos nos primórdios e é conhecida pela garra.',
                power: 2
            },
            {
                country: 'ES',
                name: 'Espanha',
                flag: 'espanha.png',
                titles: 1,
                goals: 100,
                matches: 63,
                rating: 87,
                rarity: 'Raro',
                description: 'A "Roja" revolucionou o futebol com o "tiki-taka". Conquistou 1 título mundial e é famosa pelo toque de bola.',
                power: 3
            }
        ];

        additionalCards.forEach((cardData, index) => {
            const cardHTML = this.createCardHTML(cardData, index + 5);
            container.insertAdjacentHTML('beforeend', cardHTML);
        });

        // Reconfigurar event listeners para as novas cartas
        this.setupCards();
        this.setupEventListeners();
    }

    createCardHTML(cardData, cardNumber) {
        const stars = Array(5).fill(0).map((_, i) => 
            i < cardData.power ? '<div class="star active"></div>' : '<div class="star"></div>'
        ).join('');

        return `
            <div class="col-lg-3 col-md-4 col-sm-6 mb-4">
                <div class="super-trunfo-card card-${cardData.rarity.toLowerCase()} card-glow card-enter" data-country="${cardData.country}">
                    <div class="card-header-trunfo">
                        <img src="/static/blog/images/flags/${cardData.flag}" alt="${cardData.name}" class="country-flag">
                        <h3 class="country-name">${cardData.name}</h3>
                        <span class="rarity-badge">${cardData.rarity}</span>
                    </div>
                    
                    <div class="stats-grid">
                        <div class="stat-item">
                            <div class="stat-label">🏆 Títulos</div>
                            <div class="stat-value">${cardData.titles}</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-label">⚽ Gols</div>
                            <div class="stat-value">${cardData.goals}</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-label">🎯 Partidas</div>
                            <div class="stat-value">${cardData.matches}</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-label">⭐ Rating</div>
                            <div class="stat-value">${cardData.rating}</div>
                        </div>
                    </div>
                    
                    <div class="card-description">
                        <p class="description-text">${cardData.description}</p>
                    </div>
                    
                    <div class="card-footer-trunfo">
                        <div class="power-level">
                            <span class="power-text">Poder:</span>
                            <div class="power-stars">
                                ${stars}
                            </div>
                        </div>
                        <div class="card-number">${cardNumber.toString().padStart(2, '0')}</div>
                    </div>
                </div>
            </div>
        `;
    }
}

// ===========================================
// ESTILOS CSS PARA MODAL
// ===========================================

const modalStyles = `
<style>
.card-modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 10000;
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
    transition: opacity 0.3s ease;
}

.card-modal.modal-show {
    opacity: 1;
}

.modal-backdrop {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.8);
    backdrop-filter: blur(5px);
}

.modal-content {
    position: relative;
    background: linear-gradient(145deg, rgba(43, 45, 66, 0.95), rgba(9, 10, 15, 0.98));
    border-radius: 20px;
    padding: 30px;
    max-width: 600px;
    width: 90%;
    max-height: 80vh;
    overflow-y: auto;
    border: 2px solid rgba(102, 170, 255, 0.3);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    padding-bottom: 15px;
    border-bottom: 2px solid rgba(102, 170, 255, 0.3);
}

.modal-header h3 {
    color: #EDF2F4;
    margin: 0;
    font-family: 'Bebas Neue', cursive;
    font-size: 1.8rem;
}

.modal-close {
    background: none;
    border: none;
    color: #EDF2F4;
    font-size: 2rem;
    cursor: pointer;
    padding: 0;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    transition: all 0.3s ease;
}

.modal-close:hover {
    background: rgba(102, 170, 255, 0.2);
    transform: rotate(90deg);
}

.detailed-stats {
    display: grid;
    gap: 15px;
}

.detailed-stat {
    display: flex;
    align-items: center;
    gap: 15px;
    padding: 10px;
    background: rgba(0, 0, 0, 0.3);
    border-radius: 10px;
    border: 1px solid rgba(102, 170, 255, 0.2);
}

.stat-bar {
    flex: 1;
    height: 8px;
    background: rgba(0, 0, 0, 0.5);
    border-radius: 4px;
    overflow: hidden;
}

.stat-fill {
    height: 100%;
    background: linear-gradient(90deg, #66AAFF, #4A90E2);
    border-radius: 4px;
    transition: width 0.5s ease;
}

.modal-footer {
    display: flex;
    gap: 10px;
    justify-content: flex-end;
    margin-top: 20px;
    padding-top: 15px;
    border-top: 1px solid rgba(102, 170, 255, 0.2);
}

.card-hover {
    transform: translateY(-15px) scale(1.05) !important;
    box-shadow: 0 25px 50px rgba(0, 0, 0, 0.4), 0 0 40px rgba(102, 170, 255, 0.6) !important;
}

.card-selected {
    border-color: rgba(102, 170, 255, 0.8) !important;
    box-shadow: 0 0 30px rgba(102, 170, 255, 0.8) !important;
}

@media (max-width: 768px) {
    .modal-content {
        width: 95%;
        padding: 20px;
    }
    
    .detailed-stat {
        flex-direction: column;
        text-align: center;
    }
    
    .stat-bar {
        width: 100%;
    }
}
</style>
`;

// ===========================================
// INICIALIZAÇÃO
// ===========================================

document.addEventListener('DOMContentLoaded', () => {
    // Adicionar estilos do modal
    document.head.insertAdjacentHTML('beforeend', modalStyles);
    
    // Inicializar Super Trunfo
    new SuperTrunfoManager();
    
    console.log('🎮 Super Trunfo Manager carregado!');
});

// Função global para o botão
function showAllCards() {
    const manager = window.superTrunfoManager;
    if (manager) {
        manager.showAllCards();
    }
}
