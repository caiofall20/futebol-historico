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

function initHighlightPlayersCarousel() {
    if (typeof jQuery === 'undefined' || !jQuery.fn.slick) {
        return false;
    }

    const $track = jQuery('#slick');
    if (!$track.length || $track.hasClass('slick-initialized')) {
        return !!$track.length;
    }

    const slickItems = $track.find('.highlight-player-item').length;
    if (slickItems < 1) {
        return false;
    }

    const $carousel = $track.closest('.highlight-players--content-carousel');

    $track.slick({
        autoplay: false,
        draggable: true,
        infinite: slickItems > 3,
        dots: false,
        arrows: false,
        speed: 1000,
        mobileFirst: true,
        slidesToShow: 1,
        slidesToScroll: 1,
        appendArrows: $carousel.length ? $carousel : $track.parent(),
        prevArrow: '<button type="button" class="slick-prev highlight-players__arrow" aria-label="Anterior"></button>',
        nextArrow: '<button type="button" class="slick-next highlight-players__arrow" aria-label="Próximo"></button>',
        responsive: [
            {
                breakpoint: 768,
                settings: {
                    slidesToShow: Math.min(3, slickItems),
                    slidesToScroll: 1,
                    arrows: slickItems > 3,
                    infinite: slickItems > 3,
                },
            },
        ],
    });

    return true;
}

function initRelatedPlayersCarousel() {
    if (typeof jQuery === 'undefined' || !jQuery.fn.slick) {
        return false;
    }

    const $track = jQuery('#related-players-slick');
    if (!$track.length || $track.hasClass('slick-initialized')) {
        return !!$track.length;
    }

    const $section = $track.closest('.related-players-section');
    const count = $track.children('.related-player-slide').length;
    if (count < 1) {
        return false;
    }

    const slidesDesktop = Math.min(2, count);
    const slidesTablet = Math.min(2, count);

    $track.slick({
        autoplay: count > 1,
        autoplaySpeed: 4500,
        pauseOnHover: true,
        pauseOnFocus: true,
        draggable: true,
        swipe: true,
        touchMove: true,
        infinite: count > slidesDesktop,
        dots: count > 1,
        arrows: count > 1,
        speed: 500,
        slidesToShow: slidesDesktop,
        slidesToScroll: 1,
        adaptiveHeight: false,
        prevArrow: $section.find('.related-players-carousel__arrow--prev'),
        nextArrow: $section.find('.related-players-carousel__arrow--next'),
        appendDots: $section.find('.related-players-carousel-dots'),
        responsive: [
            {
                breakpoint: 992,
                settings: {
                    slidesToShow: slidesTablet,
                    slidesToScroll: 1,
                    infinite: count > slidesTablet,
                },
            },
            {
                breakpoint: 576,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1,
                    infinite: count > 1,
                },
            },
        ],
    });

    return true;
}

function setupRelatedPlayersCarouselFallback() {
    const track = document.getElementById('related-players-slick');
    if (!track || track.classList.contains('slick-initialized')) {
        return;
    }

    track.classList.add('related-players-track--native');

    const section = track.closest('.related-players-section');
    if (!section) {
        return;
    }

    const prev = section.querySelector('.related-players-carousel__arrow--prev');
    const next = section.querySelector('.related-players-carousel__arrow--next');

    const scrollStep = () => {
        const slide = track.querySelector('.related-player-slide');
        return slide ? slide.offsetWidth + 12 : 280;
    };

    if (prev) {
        prev.addEventListener('click', () => {
            track.scrollBy({ left: -scrollStep(), behavior: 'smooth' });
        });
    }
    if (next) {
        next.addEventListener('click', () => {
            track.scrollBy({ left: scrollStep(), behavior: 'smooth' });
        });
    }
}

function bootRelatedPlayersCarousel() {
    if (initRelatedPlayersCarousel()) {
        return;
    }
    setupRelatedPlayersCarouselFallback();
}

// Função para inicializar menu mobile (compatível com e sem jQuery)
function initMobileMenu() {
    const mobileMenuButtons = document.querySelectorAll(".mobile-menu-button");
    const headerPrincipal = document.querySelector(".header-principal");
    
    if (mobileMenuButtons.length === 0 || !headerPrincipal) {
        return;
    }
    
    mobileMenuButtons.forEach(function(button) {
        button.addEventListener("click", function() {
            // Adiciona ou remove a classe "ativo" do header
            headerPrincipal.classList.toggle('ativo');
            
            // Alterna a exibição do ícone hamburguer e do ícone de fechamento
            const hamburgerIcon = this.querySelector('.hamburger-icon');
            const closeIcon = this.querySelector('.close-icon');
            
            if (hamburgerIcon) {
                hamburgerIcon.style.display = hamburgerIcon.style.display === 'none' ? '' : 'none';
            }
            if (closeIcon) {
                closeIcon.style.display = closeIcon.style.display === 'none' ? '' : 'block';
            }
        });
    });
}

// Inicializar quando o DOM estiver pronto
if (typeof $ !== 'undefined' && $.fn && $.fn.ready) {
    // jQuery está disponível
    $(document).ready(function() {
        console.log("oi");
        $(".mobile-menu-button").on("click", function() {
            // Adiciona ou remove a classe "ativo" do header
            $(".header-principal").toggleClass('ativo');
            
            // Alterna a exibição do ícone hamburguer e do ícone de fechamento
            $(this).find('.hamburger-icon').toggle();
            $(this).find('.close-icon').toggle();
        });

        // Carrossel "Jogadores de Destaque" (index)
        initHighlightPlayersCarousel();

        bootRelatedPlayersCarousel();

        $(window).on('scroll', function() {
            if (!isMobile()) {
                if ($(this).scrollTop() > 50) {
                    $('.header-principal').addClass('scroll-on');
                } else {
                    $('.header-principal').removeClass('scroll-on');
                }
            }

            const $title = $(".highlight-players--content-title");
            if ($title.length > 0) {
                const titlePosition = $title[0].getBoundingClientRect().top;
        
                if (titlePosition < window.innerHeight && titlePosition > 0) {
                    $title.addClass("scrolled");
                } else {
                    $title.removeClass("scrolled");
                }
            }
        });

        jQuery(window).on('load', function () {
            if (!jQuery('#related-players-slick').hasClass('slick-initialized')) {
                bootRelatedPlayersCarousel();
            }
        });
    });
} else {
    // jQuery não está disponível, usar vanilla JS
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function () {
            initMobileMenu();
            bootRelatedPlayersCarousel();
        });
    } else {
        initMobileMenu();
        bootRelatedPlayersCarousel();
    }
}



