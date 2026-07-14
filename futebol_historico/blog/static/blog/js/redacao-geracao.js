/**
 * Geração assíncrona de jogadores na área de redação.
 */
(function () {
    function getCookie(name) {
        const m = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
        return m ? decodeURIComponent(m[2]) : '';
    }

    function getCsrfToken() {
        const input = document.querySelector('[name=csrfmiddlewaretoken]');
        return input ? input.value : getCookie('csrftoken');
    }

    function showOverlay(message) {
        let el = document.getElementById('redacao-overlay');
        if (!el) {
            el = document.createElement('div');
            el.id = 'redacao-overlay';
            el.className = 'redacao-overlay';
            el.innerHTML = `
                <div class="redacao-overlay__box">
                    <div class="redacao-overlay__spinner"></div>
                    <p class="redacao-overlay__msg" id="redacao-overlay-msg"></p>
                    <p class="redacao-overlay__hint">Isso pode levar até um minuto. Não feche a página.</p>
                </div>
            `;
            document.body.appendChild(el);
        }
        document.getElementById('redacao-overlay-msg').textContent = message || 'Gerando conteúdo…';
        el.classList.add('redacao-overlay--visible');
    }

    function hideOverlay() {
        const el = document.getElementById('redacao-overlay');
        if (el) el.classList.remove('redacao-overlay--visible');
    }

    function pollStatus(statusUrl, onDone, onError) {
        const interval = 2000;
        const maxAttempts = 90;
        let attempts = 0;

        function tick() {
            attempts += 1;
            fetch(statusUrl, { credentials: 'same-origin', headers: { Accept: 'application/json' } })
                .then((r) => r.json())
                .then((data) => {
                    if (data.status === 'gerando') {
                        if (attempts >= maxAttempts) {
                            onError('A geração está demorando muito. Tente novamente ou regenere na revisão.');
                            return;
                        }
                        const msg = data.llm_ativo
                            ? 'Buscando fontes e redigindo com IA…'
                            : 'Buscando Wikidata e Wikipedia…';
                        showOverlay(msg);
                        setTimeout(tick, interval);
                        return;
                    }
                    if (data.status === 'rascunho' && data.redirect_url) {
                        onDone(data);
                        return;
                    }
                    if (data.status === 'erro') {
                        onError(data.mensagem_erro || 'Erro na geração.', data.redirect_url);
                        return;
                    }
                    setTimeout(tick, interval);
                })
                .catch(() => onError('Falha de conexão ao verificar o status.'));
        }
        tick();
    }

    function iniciarGeracao(form, gerarUrl) {
        const btn = form.querySelector('button[type=submit]');
        const fd = new FormData(form);
        if (btn) btn.disabled = true;

        showOverlay('Iniciando geração…');

        fetch(gerarUrl, {
            method: 'POST',
            body: fd,
            credentials: 'same-origin',
            headers: {
                'X-CSRFToken': getCsrfToken(),
                Accept: 'application/json',
            },
        })
            .then((r) => r.json().then((data) => ({ ok: r.ok, data })))
            .then(({ ok, data }) => {
                if (!ok && !data.pk) {
                    hideOverlay();
                    if (btn) btn.disabled = false;
                    const err = data.errors?.nome?.[0] || data.error || 'Não foi possível iniciar.';
                    alert(err);
                    return;
                }
                const statusUrl = `/redacao/api/rascunho/${data.pk}/status/`;
                pollStatus(
                    statusUrl,
                    (result) => {
                        hideOverlay();
                        window.location.href = result.redirect_url;
                    },
                    (msg, redirectUrl) => {
                        hideOverlay();
                        if (btn) btn.disabled = false;
                        if (redirectUrl) {
                            if (confirm(msg + '\n\nAbrir tela de revisão?')) {
                                window.location.href = redirectUrl;
                            }
                        } else {
                            alert(msg);
                        }
                    }
                );
            })
            .catch(() => {
                hideOverlay();
                if (btn) btn.disabled = false;
                alert('Erro de rede ao iniciar a geração.');
            });
    }

    function setupCriarForm() {
        const form = document.getElementById('redacao-form-criar');
        if (!form) return;
        const url = form.dataset.gerarUrl;
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            iniciarGeracao(form, url);
        });
    }

    function setupRevisarPolling() {
        const cfg = document.getElementById('redacao-revisar-config');
        if (!cfg) return;
        if (cfg.dataset.status !== 'gerando') return;

        const statusUrl = cfg.dataset.statusUrl;
        showOverlay('Regenerando conteúdo…');
        pollStatus(
            statusUrl,
            () => window.location.reload(),
            (msg) => {
                hideOverlay();
                alert(msg);
                window.location.reload();
            }
        );
    }

    function setupRegenerarAjax() {
        const form = document.getElementById('redacao-form-regenerar');
        if (!form) return;
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const url = form.dataset.regenerarUrl;
            const fd = new FormData(form);
            showOverlay('Regenerando…');
            fetch(url, {
                method: 'POST',
                body: fd,
                credentials: 'same-origin',
                headers: {
                    'X-CSRFToken': getCsrfToken(),
                    Accept: 'application/json',
                },
            })
                .then((r) => r.json())
                .then((data) => {
                    if (!data.ok && data.error) {
                        hideOverlay();
                        alert(data.error);
                        return;
                    }
                    pollStatus(
                        `/redacao/api/rascunho/${data.pk}/status/`,
                        () => window.location.reload(),
                        (msg) => {
                            hideOverlay();
                            alert(msg);
                            window.location.reload();
                        }
                    );
                })
                .catch(() => {
                    hideOverlay();
                    alert('Erro de rede.');
                });
        });
    }

    document.addEventListener('DOMContentLoaded', () => {
        setupCriarForm();
        setupRevisarPolling();
        setupRegenerarAjax();
    });
})();
