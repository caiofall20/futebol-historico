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

    $(window).on('scroll', function() {
        if (!isMobile()) {
            if ($(this).scrollTop() > 50) {
                $('.header-principal').addClass('scroll-on');
            } else {
                $('.header-principal').removeClass('scroll-on');
            }
        }

        const $title = $(".highlight-players--content-title");
        const titlePosition = $title[0].getBoundingClientRect().top;
    
        if (titlePosition < window.innerHeight && titlePosition > 0) {
            $title.addClass("scrolled");
        } else {
            $title.removeClass("scrolled");
        }
    });    
});



