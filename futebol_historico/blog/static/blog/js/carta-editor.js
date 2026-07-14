(function () {
    function getCookie(name) {
        const m = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
        return m ? decodeURIComponent(m[2]) : '';
    }

    function getCsrf() {
        const el = document.querySelector('[name=csrfmiddlewaretoken]');
        return el ? el.value : getCookie('csrftoken');
    }

    function updatePreview() {
        const root = document.getElementById('fut-card-preview');
        if (!root) return;

        const get = (id) => document.getElementById(id);
        const set = (sel, val) => {
            const el = root.querySelector(sel);
            if (el) el.textContent = val;
        };

        set('.fut-card-preview__rating', get('id_overall')?.value || '85');
        set('.fut-card-preview__pos', (get('id_posicao')?.value || 'MEI').toUpperCase());
        set('.fut-card-preview__name', (get('id_nome')?.value || root.dataset.nome || '').toUpperCase());

        const nat = get('id_nacionalidade')?.value || root.dataset.nacionalidade || '';
        set('.fut-card-preview__nat', nat);

        const stats = ['pac', 'sho', 'pas', 'dri', 'def_stat', 'phy'];
        const labels = ['PAC', 'SHO', 'PAS', 'DRI', 'DEF', 'PHY'];
        const container = root.querySelector('.fut-card-preview__stats');
        if (!container) return;
        container.innerHTML = '';
        stats.forEach((s, i) => {
            const fid = `id_${s}`;
            const val = document.getElementById(fid)?.value || '80';
            const cell = document.createElement('div');
            cell.innerHTML = `<div class="fut-card-preview__stat-label">${labels[i]}</div><div class="fut-card-preview__stat-val">${val}</div>`;
            container.appendChild(cell);
        });

        const photo = root.querySelector('.fut-card-preview__photo');
        if (photo && root.dataset.photoUrl) {
            photo.style.backgroundImage = `url('${root.dataset.photoUrl}')`;
        }
    }

    function bindInputs() {
        document.querySelectorAll('#fut-card-editor-form input').forEach((inp) => {
            inp.addEventListener('input', updatePreview);
        });
        const nome = document.getElementById('id_nome');
        const nac = document.getElementById('id_nacionalidade');
        if (nome) nome.addEventListener('input', updatePreview);
        if (nac) nac.addEventListener('input', updatePreview);
    }

    function setupSalvarCarta() {
        const btn = document.getElementById('btn-salvar-carta');
        const cfg = document.getElementById('carta-editor-config');
        if (!btn || !cfg) return;

        btn.addEventListener('click', () => {
            const payload = {
                overall: parseInt(document.getElementById('id_overall').value, 10),
                posicao: document.getElementById('id_posicao').value,
                pac: parseInt(document.getElementById('id_pac').value, 10),
                sho: parseInt(document.getElementById('id_sho').value, 10),
                pas: parseInt(document.getElementById('id_pas').value, 10),
                dri: parseInt(document.getElementById('id_dri').value, 10),
                def: parseInt(document.getElementById('id_def_stat').value, 10),
                phy: parseInt(document.getElementById('id_phy').value, 10),
            };

            btn.disabled = true;
            fetch(cfg.dataset.apiUrl, {
                method: 'POST',
                credentials: 'same-origin',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrf(),
                    Accept: 'application/json',
                },
                body: JSON.stringify(payload),
            })
                .then((r) => r.json())
                .then((data) => {
                    btn.disabled = false;
                    if (data.ok && data.carta_url) {
                        const img = document.getElementById('carta-preview-img');
                        if (img) {
                            img.src = data.carta_url + '?t=' + Date.now();
                            img.hidden = false;
                        }
                        alert('Carta salva! Atualize a prévia na listagem após publicar.');
                    } else {
                        alert(data.error || 'Erro ao salvar carta.');
                    }
                })
                .catch(() => {
                    btn.disabled = false;
                    alert('Erro de rede.');
                });
        });
    }

    document.addEventListener('DOMContentLoaded', () => {
        updatePreview();
        bindInputs();
        setupSalvarCarta();
    });
})();
