// blog/static/blog/js/scripts.js

// let slideIndex = 0;
// showSlides();

// function showSlides() {
//     let slides = document.querySelectorAll('.slides img');
//     slides.forEach((slide, index) => {
//         slide.style.display = (index === slideIndex) ? 'block' : 'none';
//     });
//     slideIndex = (slideIndex + 1) % slides.length;
//     setTimeout(showSlides, 3000); // Troca de slide a cada 3 segundos
// }


function isMobile() {
    return window.innerWidth <= 768; 
}

function aplicarFiltrosJogadores($filtroNome, $filtroNacionalidade) {
    const $jogadores = $('.jogador-card');
    const $noResultsMessage = $('.no-results');
    const nomeBusca = $filtroNome.val().trim().toLowerCase();
    const nacionalidadeBusca = $filtroNacionalidade.val().trim().toLowerCase();

    let resultadosVisiveis = false;

    $jogadores.each(function () {
        const $jogador = $(this);

        // Obtém os dados do jogador
        const nomeJogador = $jogador.find('.jogador-nome').text().toLowerCase();
        const nacionalidadeJogador = $jogador
            .find('.card-info-row')
            .filter(function () {
                return $(this).find('.info-label').text().trim() === 'Nacionalidade';
            })
            .find('.info-value')
            .text()
            .toLowerCase();
  
        // Verifica se o nome e a nacionalidade correspondem ao filtro
        const correspondeNome = !nomeBusca || nomeJogador.includes(nomeBusca);
        const correspondeNacionalidade = !nacionalidadeBusca || nacionalidadeJogador.includes(nacionalidadeBusca);

        // Mostra o jogador se os filtros forem atendidos
        const mostrar = correspondeNome && correspondeNacionalidade;
        $jogador.toggle(mostrar);

        if (mostrar) {
            resultadosVisiveis = true;
        }
    });

    // Exibe ou oculta a mensagem de "Nenhum resultado encontrado"
    $noResultsMessage.toggle(!resultadosVisiveis);
}

$(document).ready(function () {
    console.log("Iniciando...");

    // Filtro de jogadores
    if (window.location.pathname.includes('/jogadores')) {
        console.log("Página de jogadores detectada.");
        const $filtroNome = $('#filtro-nome');
        const $filtroNacionalidade = $('#filtro-nacionalidade');
       

        // Aplica filtros ao carregar a página
        aplicarFiltrosJogadores($filtroNome, $filtroNacionalidade);

        // Eventos para aplicar os filtros em tempo real
        $filtroNome.on('input', function () {
            aplicarFiltrosJogadores($filtroNome, $filtroNacionalidade);
        });
        $filtroNacionalidade.on('input', function () {
            aplicarFiltrosJogadores($filtroNome, $filtroNacionalidade);
        });
    }

    $(".mobile-menu-button").on("click", function () {
        // Adiciona ou remove a classe "ativo" do header
        $(".header-principal").toggleClass('ativo');

        // Alterna a exibição do ícone hamburguer e do ícone de fechamento
        $(this).find('.hamburger-icon').toggle();
        $(this).find('.close-icon').toggle();
    });

    if ($('#slick').length) {
        // Slick slider
        $('#slick').slick({
            autoplay: false,
            draggable: true,
            infinite: true,
            dots: false,
            arrows: false,
            speed: 1000,
            mobileFirst: true,
            slidesToShow: 1,
            slidesToScroll: 1,
            responsive: [
                {
                    breakpoint: 768,
                    settings: {
                        slidesToShow: 3,
                        slidesToScroll: 3,
                        arrows: true
                    }
                }
            ]
        });
    }

    const $title = $(".highlight-players--content-title");

    $(window).on('scroll', function () {
        if (!isMobile()) {
            if ($(this).scrollTop() > 50) {
                $('.header-principal').addClass('scroll-on');
            } else {
                $('.header-principal').removeClass('scroll-on');
            }
        }

        if ($title.length) { // Verifica se o elemento existe
            const titlePosition = $title[0].getBoundingClientRect().top;

            if (titlePosition < window.innerHeight && titlePosition > 0) {
                $title.addClass("scrolled");
            } else {
                $title.removeClass("scrolled");
            }
        }
    });
});


