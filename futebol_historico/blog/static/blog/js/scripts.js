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
    $(".mobile-menu-button").on("click", function() {
        // Adiciona ou remove a classe "ativo" do header
        $(".header-principal").toggleClass('ativo');
        
        // Alterna a exibição do ícone hamburguer e do ícone de fechamento
        $(this).find('.hamburger-icon').toggle();
        $(this).find('.close-icon').toggle();
        
    });

    $(window).on('scroll', function() {
        if (!isMobile()) {
            if ($(this).scrollTop() > 50) {
                $('.header-principal').addClass('scroll-on');
            } else {
                $('.header-principal').removeClass('scroll-on');
            }
        }
    });
});



