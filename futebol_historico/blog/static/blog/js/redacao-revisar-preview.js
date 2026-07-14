/**
 * Prévia ao vivo de foto e carta na página de revisão do rascunho.
 */
(function () {
    function bindImagePreview(card) {
        const input = card.querySelector('input[type="file"]');
        const img = card.querySelector('[data-preview-img]');
        const placeholder = card.querySelector('[data-preview-empty]');
        if (!input || !img) return;

        const showPreview = (src) => {
            img.src = src;
            img.hidden = false;
            if (placeholder) placeholder.hidden = true;
        };

        const showEmpty = () => {
            img.removeAttribute('src');
            img.hidden = true;
            if (placeholder) placeholder.hidden = false;
        };

        input.addEventListener('change', () => {
            const file = input.files && input.files[0];
            if (!file) return;
            if (!file.type.startsWith('image/')) {
                alert('Selecione um arquivo de imagem (PNG, JPEG ou WebP).');
                input.value = '';
                return;
            }
            const reader = new FileReader();
            reader.onload = (e) => showPreview(e.target.result);
            reader.readAsDataURL(file);
        });

        const clearCheck = card.querySelector('input[type="checkbox"][name$="-clear"]');
        if (clearCheck) {
            clearCheck.addEventListener('change', () => {
                if (clearCheck.checked) {
                    input.value = '';
                    showEmpty();
                }
            });
        }
    }

    document.addEventListener('DOMContentLoaded', () => {
        document.querySelectorAll('.redacao-imagem-card').forEach(bindImagePreview);
    });
})();
