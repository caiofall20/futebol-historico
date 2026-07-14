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

        // slick slider
        if ($('#slick').length > 0) {
            $('#slick').slick({
                autoplay: false,
                draggable: true,
                infinite: true,
                dots: false,
                arrows: false,
                speed: 1000,
                mobileFirst: true,
                slidesToShow: 1, // Exibe 1 slide em telas menores que 768px
                slidesToScroll: 1, // Rola 1 slide por vez em telas menores que 768px
                responsive: [
                    {
                        breakpoint: 768, // 768px ou maior
                        settings: {
                            slidesToShow: 3, // Exibe 3 slides por vez
                            slidesToScroll: 3, // Rola 3 slides por vez
                            arrows: true
                        }
                    }
                ]
            });
        }

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
    });
} else {
    // jQuery não está disponível, usar vanilla JS
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initMobileMenu);
    } else {
        initMobileMenu();
    }
}



