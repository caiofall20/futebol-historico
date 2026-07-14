/**
 * Editor completo de carta FUT (fundos FIFA 26 importados).
 */
(function () {
    const LEGACY_BG_MAP = {
        gold_marble: 'fifa26:rare_gold',
        dark_blue: 'fifa26:rare_gold',
        toty_blue: 'fifa26:toty',
        tots_lightning: 'fifa26:tots_gold',
        purple_hero: 'fifa26:hero',
        red_motm: 'fifa26:motm',
    };

    const DEFAULT_PHOTO = { x: 0, y: 0, scale: 100, zoom: 100, fade: 'soft' };
    const DEFAULT_NAME_FADE = { fade: 'soft', intensity: 35, color: '#ffffff' };
    const DEFAULT_COLORS = {
        rating: '#5c4a1a',
        position: '#5c4a1a',
        name: '#5c4a1a',
        stats_label: '#5c4a1a',
        stats_value: '#2a2210',
    };

    const COLOR_INPUT_IDS = [
        ['rating', 'cc-color-rating'],
        ['position', 'cc-color-position'],
        ['name', 'cc-color-name'],
        ['stats_label', 'cc-stat-label-color'],
        ['stats_value', 'cc-stat-value-color'],
    ];

    function isColorsUnifiedMode() {
        return !!$('cc-colors-unified')?.checked;
    }

    function applyUnifiedColorToInputs(hex) {
        COLOR_INPUT_IDS.forEach(([, id]) => {
            const el = $(id);
            if (el) el.value = hex;
        });
    }

    function toggleColorsPanel() {
        const unified = isColorsUnifiedMode();
        $('panel-colors-unified')?.toggleAttribute('hidden', !unified);
        $('panel-colors-individual')?.toggleAttribute('hidden', unified);
    }

    function readColorsFromForm() {
        if (isColorsUnifiedMode()) {
            const hex = $('cc-color-unified')?.value || DEFAULT_COLORS.rating;
            return normalizeColors({
                rating: hex,
                position: hex,
                name: hex,
                stats_label: hex,
                stats_value: hex,
            });
        }
        const raw = {};
        COLOR_INPUT_IDS.forEach(([key, id]) => {
            const el = $(id);
            if (el?.value) raw[key] = el.value;
        });
        return normalizeColors(raw);
    }

    function normalizeColors(colors) {
        const c = { ...DEFAULT_COLORS, ...(colors || {}) };
        const fallback = c.stats_label || c.rating || DEFAULT_COLORS.rating;
        return {
            rating: c.rating || fallback,
            position: c.position || fallback,
            name: c.name || fallback,
            stats_label: c.stats_label || fallback,
            stats_value: c.stats_value || DEFAULT_COLORS.stats_value,
        };
    }
    const PHOTO_CLAMP_FALLBACK = { xMin: -100, xMax: 100, yMin: -220, yMax: 220 };

    let state = {};
    let cardEl, photoEl, photoWrapEl, photoMoverEl, photoClipEl;
    let photoPanLimits = { ...PHOTO_CLAMP_FALLBACK };
    let dragPanLimits = null;
    let dragActive = false;

    const FIFAROSTERS_ASSETS = 'https://www.fifarosters.com/';
    const DEFAULT_ICON_LEAGUE = {
        id: '2118',
        label: 'Icons (ICN)',
        url: `${FIFAROSTERS_ASSETS}assets/leagues/fifa26/2118.png`,
        type: 'league',
    };

    function getConfig() {
        const el = document.getElementById('card-creator-config');
        return {
            saveUrl: el?.dataset.saveUrl || '',
            revisarUrl: el?.dataset.revisarUrl || '',
            crestLookupUrl: el?.dataset.crestLookupUrl || '',
            crestProxyUrl: el?.dataset.crestProxyUrl || '',
            rascunhoNacionalidade: el?.dataset.rascunhoNacionalidade || '',
            rascunhoImagem: el?.dataset.rascunhoImagem || '',
        };
    }

    function fixClubCrestUrl(url, clubId) {
        const id = String(clubId || '').trim();
        const u = (url || '').trim();
        if (!id) return u;
        if (!u) return `${FIFAROSTERS_ASSETS}assets/clubs/fifa25/${id}.png`;
        if (u.includes('/assets/clubs/fifa26/')) {
            return `${FIFAROSTERS_ASSETS}assets/clubs/fifa25/${id}.png`;
        }
        return u;
    }

    function crestAssetUrl(crestType, assetId, customUrl) {
        const id = String(assetId || '').trim();
        if (customUrl) {
            const trimmed = customUrl.trim();
            if (crestType === 'club') return fixClubCrestUrl(trimmed, id);
            return trimmed;
        }
        if (!id) return '';
        if (crestType === 'nation') return `${FIFAROSTERS_ASSETS}assets/nations/fifa17/${id}.png`;
        if (crestType === 'club') return fixClubCrestUrl('', id);
        if (crestType === 'league') return `${FIFAROSTERS_ASSETS}assets/leagues/fifa26/${id}.png`;
        return '';
    }

    function normalizeCrests(source) {
        const raw = source?.crests && typeof source.crests === 'object' ? source.crests : {};
        const showRaw = raw.show && typeof raw.show === 'object' ? raw.show : {};
        const one = (key, type) => {
            const block = raw[key] && typeof raw[key] === 'object' ? raw[key] : {};
            const id = block.id || '';
            let url = (block.url || '').trim() || crestAssetUrl(type, id);
            if (type === 'club') url = fixClubCrestUrl(url, id);
            return { id: String(id), label: block.label || '', url, type };
        };
        return {
            nation: one('nation', 'nation'),
            club: one('club', 'club'),
            league: one('league', 'league'),
            show: {
                nation: !!showRaw.nation,
                club: !!showRaw.club,
                league: showRaw.league !== false && (showRaw.league !== undefined || !!raw.league?.url),
            },
        };
    }

    function readCrestsFromForm() {
        const prev = normalizeCrests(state);
        const readOne = (type) => {
            const id = $(`cc-crest-${type}-id`)?.value || prev[type].id;
            const label = $(`cc-crest-${type}-search`)?.value || prev[type].label;
            const customUrl = $(`cc-crest-${type}-url`)?.value || '';
            const url = crestAssetUrl(type, id, customUrl) || prev[type].url;
            return { id: String(id || ''), label, url, type };
        };
        return {
            nation: readOne('nation'),
            club: readOne('club'),
            league: readOne('league'),
            show: {
                nation: !!$('cc-show-crest-nation')?.checked,
                club: !!$('cc-show-crest-club')?.checked,
                league: !!$('cc-show-crest-league')?.checked,
            },
        };
    }

    const CREST_SEARCH_ALIASES = {
        nation: {
            brasil: 'Brazil',
            brazil: 'Brazil',
            argentina: 'Argentina',
            portugal: 'Portugal',
            espanha: 'Spain',
            italia: 'Italy',
            frança: 'France',
            franca: 'France',
            alemanha: 'Germany',
            inglaterra: 'England',
        },
        league: {
            icon: 'icons',
            icone: 'icons',
            ícone: 'icons',
            icons: 'icons',
        },
        club: {
            milão: 'Milan',
            milao: 'Milan',
            milan: 'Milan',
            'ac milan': 'Milan',
            inter: 'Inter',
            'inter milan': 'Inter',
            juventus: 'Juventus',
            barcelona: 'FC Barcelona',
            barça: 'FC Barcelona',
            'real madrid': 'Real Madrid',
            'man city': 'Manchester City',
            'man united': 'Manchester United',
            psg: 'Paris SG',
            bayern: 'Bayern Munich',
            vasco: 'Vasco da Gama',
            'são paulo': 'Sao Paulo',
            'sao paulo': 'Sao Paulo',
        },
    };

    function crestDisplayUrl(url) {
        const raw = (url || '').trim();
        if (!raw) return '';
        const proxy = getConfig().crestProxyUrl;
        if (proxy && raw.startsWith(FIFAROSTERS_ASSETS)) {
            return `${proxy}?url=${encodeURIComponent(raw)}`;
        }
        return raw;
    }

    function resolveCrestSearchTerm(type, term) {
        const t = term.trim();
        const map = CREST_SEARCH_ALIASES[type] || {};
        return map[t.toLowerCase()] || t;
    }

    function syncCrestsFromForm() {
        state.crests = readCrestsFromForm();
        applyCrests();
    }

    function applyCrests() {
        if (!cardEl) return;
        const crests = normalizeCrests({ crests: state.crests || {} });
        state.crests = crests;
        const wrap = cardEl.querySelector('.fut-creator-card__crests');
        if (!wrap) return;

        let any = false;
        ['nation', 'league', 'club'].forEach((key) => {
            const img = wrap.querySelector(`[data-crest="${key}"]`);
            const holder = img?.closest('.fut-creator-card__crest');
            const entry = crests[key] || {};
            const url = crestDisplayUrl(entry.url || '');
            const visible = !!(crests.show?.[key] && url);
            if (!img || !holder) return;
            if (visible) {
                if (img.getAttribute('src') !== url) img.setAttribute('src', url);
                img.alt = entry.label || key;
                holder.classList.add('is-visible');
                any = true;
            } else {
                img.removeAttribute('src');
                holder.classList.remove('is-visible');
            }
        });
        wrap.style.display = any ? 'flex' : 'none';
        wrap.setAttribute('aria-hidden', any ? 'false' : 'true');
        state.club = crests.club?.label || '';
        state.league = crests.league?.label || '';
    }

    function getCsrf() {
        const inp = document.querySelector('[name=csrfmiddlewaretoken]');
        return inp ? inp.value : '';
    }

    function $(id) {
        return document.getElementById(id);
    }

    function bind(id, event, fn) {
        const el = $(id);
        if (el) el.addEventListener(event, fn);
    }

    function getRadioValue(name, fallback) {
        const el = document.querySelector(`input[name="${name}"]:checked`);
        return el ? el.value : fallback;
    }

    function normalizeBackground(bg) {
        if (!bg) return bg;
        const next = { ...bg };
        if (next.value && !String(next.value).startsWith('fifa26:')) {
            next.value = LEGACY_BG_MAP[next.value] || next.value;
        }
        return next;
    }

    function firstFifaButton() {
        return document.querySelector('.card-creator-fifa-btn');
    }

    function resolveFifaUrl(bg) {
        const value = bg?.value;
        if (!value || !String(value).startsWith('fifa26:')) {
            return '';
        }
        if (bg.asset_url) {
            return bg.asset_url;
        }
        const btn = document.querySelector(`.card-creator-fifa-btn[data-bg="${value}"]`);
        return btn?.dataset.bgUrl || '';
    }

    function getPhotoSource() {
        return getRadioValue('cc-photo-source', 'rascunho');
    }

    function resolvePhotoUrl() {
        const source = getPhotoSource();
        const cfg = getConfig();
        if (source === 'rascunho') {
            return state.player?.url || cfg.rascunhoImagem || '';
        }
        if (source === 'url') {
            return ($('cc-photo-url')?.value || '').trim();
        }
        return state.player?.url || '';
    }

    function readFormIntoState() {
        const g = (id, def) => {
            const el = $(id);
            if (!el) return def;
            if (el.type === 'checkbox') return el.checked;
            if (el.type === 'number' || el.type === 'range') return Number(el.value);
            return el.value;
        };

        const prevPlayer = state.player || {};

        state.template = document.querySelector('.card-creator-tpl-btn.active')?.dataset.tpl || state.template;
        state.name = g('cc-name', state.name);
        state.overall = g('cc-overall', state.overall);
        state.position = g('cc-position', state.position);
        state.nation = g('cc-nation', state.nation);
        state.crests = readCrestsFromForm();
        state.club = state.crests.club?.label || '';
        state.league = state.crests.league?.label || '';
        state.show_nation = false;
        state.show_club = !!state.crests.show?.club;
        state.show_league = !!state.crests.show?.league;

        const activeFifa = document.querySelector('.card-creator-fifa-btn.active');
        state.background = normalizeBackground({
            type: 'preset',
            value: activeFifa?.dataset.bg || state.background?.value,
            color: '#1a2848',
            url: '',
            asset_url: activeFifa?.dataset.bgUrl || state.background?.asset_url || '',
        });

        state.player = {
            url: resolvePhotoUrl(),
            source: getPhotoSource(),
            x: prevPlayer.x ?? DEFAULT_PHOTO.x,
            y: prevPlayer.y ?? DEFAULT_PHOTO.y,
            scale: g('cc-photo-scale', prevPlayer.scale ?? DEFAULT_PHOTO.scale),
            zoom: g('cc-photo-zoom', prevPlayer.zoom ?? DEFAULT_PHOTO.zoom),
            fade: getRadioValue('cc-photo-fade', prevPlayer.fade ?? DEFAULT_PHOTO.fade),
            brightness: g('cc-photo-brightness', 100),
            contrast: g('cc-photo-contrast', 100),
            saturation: g('cc-photo-saturation', 100),
            grayscale: g('cc-photo-grayscale', false),
            cutout: prevPlayer.cutout,
        };

        state.stats = {
            pac: g('cc-pac', 80),
            sho: g('cc-sho', 80),
            pas: g('cc-pas', 80),
            dri: g('cc-dri', 80),
            def: g('cc-def', 70),
            phy: g('cc-phy', 80),
        };

        state.extras = {
            skill: g('cc-skill', 4),
            weak_foot: g('cc-weak', 4),
            foot: g('cc-foot', 'R'),
            work_att: g('cc-work-att', 'M'),
            work_def: g('cc-work-def', 'M'),
            chemistry: g('cc-chemistry', 'basic'),
        };

        state.colors = readColorsFromForm();
        state.colors_unified = g('cc-colors-unified', state.colors_unified ?? false);

        state.name_fade = getRadioValue('cc-name-fade', state.name_fade ?? DEFAULT_NAME_FADE.fade);
        state.name_fade_intensity = g('cc-name-fade-intensity', state.name_fade_intensity ?? DEFAULT_NAME_FADE.intensity);
        state.name_fade_color = g('cc-name-fade-color', state.name_fade_color ?? DEFAULT_NAME_FADE.color);
    }

    function computePhotoPanLimits() {
        if (!photoEl || !photoClipEl) {
            return { ...PHOTO_CLAMP_FALLBACK };
        }
        if (!photoEl.naturalWidth || !photoEl.complete) {
            return { ...PHOTO_CLAMP_FALLBACK };
        }

        const cw = photoClipEl.clientWidth;
        const ch = photoClipEl.clientHeight;
        const sizeScale = (state.player?.scale || 100) / 100;
        const zoom = (state.player?.zoom ?? 100) / 100;
        const nw = photoEl.naturalWidth;
        const nh = photoEl.naturalHeight;
        const displayW = cw * sizeScale * zoom;
        const displayH = (nh / nw) * displayW;
        const overflowX = Math.max(0, (displayW - cw) / 2);
        const overflowY = Math.max(0, displayH - ch);
        const padX = Math.ceil(overflowX + 36);
        const padY = Math.ceil(overflowY + 56);

        return {
            xMin: -padX,
            xMax: padX,
            yMin: -padY,
            yMax: padY,
        };
    }

    function refreshPhotoPanLimits() {
        photoPanLimits = computePhotoPanLimits();
    }

    function clampPhotoPosition(frozenLimits) {
        if (!state.player) return;
        if (!frozenLimits) {
            refreshPhotoPanLimits();
        }
        const lim = frozenLimits || photoPanLimits;
        state.player.x = Math.max(lim.xMin, Math.min(lim.xMax, state.player.x || 0));
        state.player.y = Math.max(lim.yMin, Math.min(lim.yMax, state.player.y || 0));
    }

    function applyColors() {
        if (!cardEl) return;
        const c = normalizeColors(state.colors);
        state.colors = c;

        cardEl.style.setProperty('--rating-color', c.rating);
        cardEl.style.setProperty('--position-color', c.position);
        cardEl.style.setProperty('--name-color', c.name);
        cardEl.style.setProperty('--stat-label-color', c.stats_label);
        cardEl.style.setProperty('--stat-value-color', c.stats_value);
        cardEl.style.setProperty('--text-gold', c.rating);

        const rating = cardEl.querySelector('.fut-creator-card__rating');
        const pos = cardEl.querySelector('.fut-creator-card__position');
        const name = cardEl.querySelector('.fut-creator-card__name');
        if (rating) rating.style.color = c.rating;
        if (pos) pos.style.color = c.position;
        if (name) name.style.color = c.name;
        cardEl.querySelectorAll('.fut-creator-card__stats-labels span').forEach((el) => {
            el.style.color = c.stats_label;
        });
        cardEl.querySelectorAll('.fut-creator-card__stats-values span').forEach((el) => {
            el.style.color = c.stats_value;
        });
    }

    function applyBackground() {
        if (!cardEl) return;
        const bg = normalizeBackground(state.background || {});
        const fifaUrl = resolveFifaUrl(bg);

        cardEl.style.backgroundColor = 'transparent';
        cardEl.style.backgroundSize = 'cover';
        cardEl.style.backgroundPosition = 'center top';
        cardEl.style.backgroundRepeat = 'no-repeat';
        cardEl.style.backgroundImage = fifaUrl ? `url('${fifaUrl}')` : 'none';
        cardEl.classList.toggle('fut-creator-card--official', !!fifaUrl);
    }

    function applyPhotoVars() {
        if (!cardEl) return;
        const p = state.player || {};
        cardEl.style.setProperty('--photo-x', `${p.x || 0}px`);
        cardEl.style.setProperty('--photo-y', `${p.y || 0}px`);
        cardEl.style.setProperty('--photo-scale', String((p.scale || 100) / 100));
        cardEl.style.setProperty('--photo-zoom', String((p.zoom ?? 100) / 100));
    }

    function applyPhotoTransform() {
        if (!cardEl) return;
        const p = state.player || {};
        applyPhotoVars();
        cardEl.style.setProperty('--photo-brightness', String((p.brightness || 100) / 100));
        cardEl.style.setProperty('--photo-contrast', String((p.contrast || 100) / 100));
        cardEl.style.setProperty('--photo-saturation', String((p.saturation || 100) / 100));

        const fade = p.fade || 'none';
        cardEl.classList.remove('fut-creator-card--fade-soft', 'fut-creator-card--fade-strong');
        if (fade === 'soft') cardEl.classList.add('fut-creator-card--fade-soft');
        if (fade === 'strong') cardEl.classList.add('fut-creator-card--fade-strong');

        if (photoWrapEl) {
            photoWrapEl.classList.toggle('has-photo', !!(p.url));
        }
        if (photoEl) {
            const url = p.url || '';
            if (url) {
                const syncAfterLoad = () => {
                    requestAnimationFrame(() => {
                        clampPhotoPosition();
                        applyPhotoVars();
                    });
                };
                if (photoEl.src !== url) {
                    photoEl.onload = syncAfterLoad;
                    photoEl.src = url;
                } else if (photoEl.complete) {
                    syncAfterLoad();
                } else {
                    photoEl.onload = syncAfterLoad;
                }
                photoEl.style.display = 'block';
            } else {
                photoEl.onload = null;
                photoEl.removeAttribute('src');
                photoEl.style.display = 'none';
            }
            photoEl.classList.toggle('grayscale', !!p.grayscale);
        }

        if (p.url && photoEl?.complete && photoEl.naturalWidth) {
            clampPhotoPosition();
            applyPhotoVars();
        }
    }

    function toggleNameFadePanel() {
        const mode = getRadioValue('cc-name-fade', state.name_fade || 'none');
        const panel = $('panel-name-fade-options');
        if (panel) panel.hidden = mode === 'none';
    }

    function updateNameFadeIntensityLabel() {
        const out = $('cc-name-fade-intensity-val');
        const el = $('cc-name-fade-intensity');
        if (out && el) out.textContent = String(el.value);
    }

    function applyNameFade() {
        if (!cardEl) return;
        const mode = state.name_fade || 'none';
        const color = state.name_fade_color || DEFAULT_NAME_FADE.color;
        cardEl.style.setProperty('--name-fade-color', color);
        cardEl.classList.remove('fut-creator-card--name-fade-on');

        if (mode === 'none') {
            cardEl.style.removeProperty('--name-fade-opacity');
            cardEl.style.removeProperty('--name-fade-height');
            cardEl.style.removeProperty('--name-fade-solid-pct');
            return;
        }

        const raw = Number(state.name_fade_intensity);
        const t = Math.max(0, Math.min(100, Number.isFinite(raw) ? raw : DEFAULT_NAME_FADE.intensity)) / 100;
        const reach = mode === 'strong' ? 1 : 0.7;
        const opacity = (0.12 + t * 0.5 * reach).toFixed(3);
        const nameRow = 22;
        const heightPx = Math.round(nameRow + 16 + t * 24 * reach);
        const solidPct = `${(14 + t * 22 * reach).toFixed(1)}%`;

        cardEl.style.setProperty('--name-fade-opacity', opacity);
        cardEl.style.setProperty('--name-fade-height', `${heightPx}px`);
        cardEl.style.setProperty('--name-fade-solid-pct', solidPct);
        cardEl.classList.add('fut-creator-card--name-fade-on');
    }

    function applyCard() {
        if (!cardEl) return;
        cardEl.className = `fut-creator-card fut-creator-card--official style-${state.template || 'icon_gold'}`;

        const rating = cardEl.querySelector('.fut-creator-card__rating');
        const pos = cardEl.querySelector('.fut-creator-card__position');
        const name = cardEl.querySelector('.fut-creator-card__name');
        const statsLabels = cardEl.querySelector('.fut-creator-card__stats-labels');
        const statsValues = cardEl.querySelector('.fut-creator-card__stats-values');

        const overallVal = state.overall ?? 88;
        const posVal = (state.position || 'MEI').toUpperCase();
        if (rating) {
            rating.textContent = String(overallVal);
            const ovrLen = String(overallVal).length;
            const ratingSize = ovrLen >= 3 ? '40px' : ovrLen === 2 ? '48px' : '52px';
            cardEl.style.setProperty('--rating-font-size', ratingSize);
        }
        if (pos) {
            pos.textContent = posVal;
            const posSize = posVal.length > 4 ? '12px' : posVal.length > 3 ? '13px' : '14px';
            cardEl.style.setProperty('--position-font-size', posSize);
        }
        if (name) name.textContent = (state.name || '').toUpperCase();
        if (state.stats) {
            const s = state.stats;
            const labs = ['PAC', 'SHO', 'PAS', 'DRI', 'DEF', 'PHY'];
            const keys = ['pac', 'sho', 'pas', 'dri', 'def', 'phy'];
            if (statsLabels) {
                statsLabels.innerHTML = labs.map((lab) => `<span>${lab}</span>`).join('');
            }
            if (statsValues) {
                statsValues.innerHTML = keys.map((k) => `<span>${s[k]}</span>`).join('');
            }
        }

        applyBackground();
        applyColors();
        applyCrests();
        applyPhotoTransform();
        applyNameFade();
    }

    function render() {
        if (!dragActive) {
            readFormIntoState();
        }
        applyCard();
    }

    function ensureFifaBackgroundSelected() {
        const bg = normalizeBackground(state.background || {});
        let btn = document.querySelector(`.card-creator-fifa-btn[data-bg="${bg.value}"]`);
        if (!btn) {
            btn = firstFifaButton();
            if (btn) {
                state.background = {
                    type: 'preset',
                    value: btn.dataset.bg,
                    asset_url: btn.dataset.bgUrl,
                };
            }
        }
        document.querySelectorAll('.card-creator-fifa-btn').forEach((b) => {
            b.classList.toggle('active', b === btn);
        });
    }

    function togglePhotoPanels() {
        const source = getPhotoSource();
        $('panel-photo-rascunho')?.toggleAttribute('hidden', source !== 'rascunho');
        $('panel-photo-url')?.toggleAttribute('hidden', source !== 'url');
        $('panel-photo-upload')?.toggleAttribute('hidden', source !== 'upload');
    }

    function setPhotoSourceRadio(value) {
        document.querySelectorAll('input[name="cc-photo-source"]').forEach((inp) => {
            inp.checked = inp.value === value;
        });
        togglePhotoPanels();
    }

    function setPhotoFadeRadio(value) {
        document.querySelectorAll('input[name="cc-photo-fade"]').forEach((inp) => {
            inp.checked = inp.value === value;
        });
    }

    function setNameFadeRadio(value) {
        document.querySelectorAll('input[name="cc-name-fade"]').forEach((inp) => {
            inp.checked = inp.value === value;
        });
    }

    function fillFormFromState() {
        state.background = normalizeBackground(state.background || {});
        ensureFifaBackgroundSelected();

        const s = state;
        const set = (id, v) => { const el = $(id); if (el) el.value = v; };
        const setChk = (id, v) => { const el = $(id); if (el) el.checked = !!v; };

        set('cc-name', s.name);
        setNameFadeRadio(s.name_fade ?? DEFAULT_NAME_FADE.fade);
        set('cc-name-fade-intensity', s.name_fade_intensity ?? DEFAULT_NAME_FADE.intensity);
        set('cc-name-fade-color', s.name_fade_color ?? DEFAULT_NAME_FADE.color);
        updateNameFadeIntensityLabel();
        toggleNameFadePanel();
        set('cc-overall', s.overall);
        set('cc-position', s.position);
        set('cc-nation', s.nation);
        const crests = normalizeCrests(s);
        state.crests = crests;
        ['nation', 'league', 'club'].forEach((t) => {
            const e = crests[t] || {};
            set(`cc-crest-${t}-search`, e.label || '');
            set(`cc-crest-${t}-id`, e.id || '');
            set(`cc-crest-${t}-url`, e.url || '');
            setChk(`cc-show-crest-${t}`, !!crests.show?.[t]);
        });

        const p = s.player || {};
        setPhotoSourceRadio(p.source || 'rascunho');
        set('cc-photo-url', p.source === 'url' ? (p.url || '') : '');
        set('cc-photo-scale', p.scale ?? DEFAULT_PHOTO.scale);
        set('cc-photo-zoom', p.zoom ?? DEFAULT_PHOTO.zoom);
        setPhotoFadeRadio(p.fade ?? DEFAULT_PHOTO.fade);
        set('cc-photo-brightness', p.brightness ?? 100);
        set('cc-photo-contrast', p.contrast ?? 100);
        set('cc-photo-saturation', p.saturation ?? 100);
        setChk('cc-photo-grayscale', p.grayscale);

        const st = s.stats || {};
        set('cc-pac', st.pac); set('cc-sho', st.sho); set('cc-pas', st.pas);
        set('cc-dri', st.dri); set('cc-def', st.def); set('cc-phy', st.phy);

        const e = s.extras || {};
        set('cc-skill', e.skill ?? 4);
        set('cc-weak', e.weak_foot ?? 4);
        set('cc-foot', e.foot ?? 'R');
        set('cc-work-att', e.work_att ?? 'M');
        set('cc-work-def', e.work_def ?? 'M');
        set('cc-chemistry', e.chemistry ?? 'basic');

        const c = normalizeColors(s.colors);
        const unified = !!s.colors_unified;
        setChk('cc-colors-unified', unified);
        if (unified) {
            set('cc-color-unified', c.rating);
            applyUnifiedColorToInputs(c.rating);
        } else {
            set('cc-color-rating', c.rating);
            set('cc-color-position', c.position);
            set('cc-color-name', c.name);
            set('cc-stat-label-color', c.stats_label);
            set('cc-stat-value-color', c.stats_value);
        }
        toggleColorsPanel();

        document.querySelectorAll('.card-creator-tpl-btn').forEach((btn) => {
            btn.classList.toggle('active', btn.dataset.tpl === s.template);
        });

        applyCard();
    }

    function resetPhotoTransform() {
        state.player = {
            ...(state.player || {}),
            x: DEFAULT_PHOTO.x,
            y: DEFAULT_PHOTO.y,
            scale: DEFAULT_PHOTO.scale,
            zoom: DEFAULT_PHOTO.zoom,
        };
        const scaleEl = $('cc-photo-scale');
        if (scaleEl) scaleEl.value = DEFAULT_PHOTO.scale;
        const zoomEl = $('cc-photo-zoom');
        if (zoomEl) zoomEl.value = DEFAULT_PHOTO.zoom;
        applyCard();
    }

    function syncFromRascunho() {
        const cfg = getConfig();
        if (cfg.rascunhoImagem) {
            state.player = {
                ...(state.player || {}),
                url: cfg.rascunhoImagem,
                source: 'rascunho',
            };
            setPhotoSourceRadio('rascunho');
            fillFormFromState();
        }
    }

    function loadPhotoFile(file) {
        if (!file) return;
        const reader = new FileReader();
        reader.onload = (e) => {
            state.player = {
                ...(state.player || {}),
                url: e.target.result,
                source: 'upload',
            };
            setPhotoSourceRadio('upload');
            fillFormFromState();
        };
        reader.readAsDataURL(file);
    }

    function setRemoveBgStatus(msg, visible = true) {
        const el = $('cc-remove-bg-status');
        if (!el) return;
        el.textContent = msg;
        el.hidden = !visible;
    }

    async function removePhotoBackground() {
        readFormIntoState();
        const url = state.player?.url;
        if (!url) {
            alert('Adicione uma foto antes de remover o fundo.');
            return;
        }

        const btn = $('cc-btn-remove-bg');
        if (btn) btn.disabled = true;
        setRemoveBgStatus('Removendo fundo… pode levar alguns segundos.');

        try {
            const { removeBackground } = await import(
                'https://esm.sh/@imgly/background-removal@1.4.5'
            );
            const blob = await removeBackground(url, {
                progress: (key, current, total) => {
                    if (total > 0) {
                        const pct = Math.round((current / total) * 100);
                        setRemoveBgStatus(`Removendo fundo… ${pct}%`);
                    }
                },
            });
            const dataUrl = await new Promise((resolve, reject) => {
                const reader = new FileReader();
                reader.onload = () => resolve(reader.result);
                reader.onerror = reject;
                reader.readAsDataURL(blob);
            });
            state.player = {
                ...(state.player || {}),
                url: dataUrl,
                source: getPhotoSource(),
                cutout: true,
            };
            fillFormFromState();
            setRemoveBgStatus('Fundo removido. Arraste na carta para ajustar.', true);
        } catch (err) {
            console.error(err);
            setRemoveBgStatus('');
            alert(
                'Não foi possível remover o fundo automaticamente. '
                + 'Envie um PNG já recortado (sem fundo) ou tente outra imagem.'
            );
        } finally {
            if (btn) btn.disabled = false;
        }
    }

    function initPhotoDrag() {
        if (!photoMoverEl || !photoWrapEl) return;

        let startX = 0;
        let startY = 0;
        let originX = 0;
        let originY = 0;

        const onPointerDown = (e) => {
            if (!state.player?.url) return;
            if (e.button !== undefined && e.button !== 0) return;

            dragActive = true;
            dragPanLimits = computePhotoPanLimits();
            photoWrapEl.classList.add('is-dragging');
            startX = e.clientX;
            startY = e.clientY;
            originX = state.player.x || 0;
            originY = state.player.y || 0;
            photoMoverEl.setPointerCapture?.(e.pointerId);
            e.preventDefault();
        };

        const onPointerMove = (e) => {
            if (!dragActive) return;
            state.player = state.player || {};
            state.player.x = Math.round(originX + (e.clientX - startX));
            state.player.y = Math.round(originY + (e.clientY - startY));
            clampPhotoPosition(dragPanLimits);
            applyPhotoVars();
        };

        const onPointerUp = (e) => {
            if (!dragActive) return;
            dragActive = false;
            dragPanLimits = null;
            photoWrapEl.classList.remove('is-dragging');
            photoMoverEl.releasePointerCapture?.(e.pointerId);
            clampPhotoPosition();
            applyPhotoVars();
        };

        photoMoverEl.addEventListener('pointerdown', onPointerDown);
        photoMoverEl.addEventListener('pointermove', onPointerMove);
        photoMoverEl.addEventListener('pointerup', onPointerUp);
        photoMoverEl.addEventListener('pointercancel', onPointerUp);
    }

    async function exportCanvas() {
        const card = $('fut-creator-card');
        if (!card || typeof html2canvas === 'undefined') {
            return null;
        }
        const canvas = await html2canvas(card, {
            scale: 2,
            useCORS: true,
            allowTaint: true,
            backgroundColor: null,
            logging: false,
        });
        return new Promise((resolve) => {
            canvas.toBlob((blob) => resolve(blob), 'image/png', 0.95);
        });
    }

    async function saveCard() {
        readFormIntoState();
        const cfg = getConfig();
        const loading = $('card-creator-loading');
        if (loading) loading.classList.add('visible');

        try {
            const blob = await exportCanvas();
            const fd = new FormData();
            fd.append('design', JSON.stringify(state));
            fd.append('csrfmiddlewaretoken', getCsrf());
            if (blob) {
                fd.append('carta_png', blob, 'carta.png');
            }

            const res = await fetch(cfg.saveUrl, {
                method: 'POST',
                body: fd,
                credentials: 'same-origin',
            });
            const data = await res.json();
            if (data.ok) {
                const msg = data.portal_atualizado
                    ? 'Carta salva e atualizada na listagem do portal!'
                    : 'Carta salva no rascunho! Publique o jogador para aparecer na listagem.';
                alert(msg);
                window.location.href = cfg.revisarUrl;
            } else {
                alert(data.error || 'Erro ao salvar.');
            }
        } catch (err) {
            alert('Erro ao exportar carta: ' + err.message);
        } finally {
            if (loading) loading.classList.remove('visible');
        }
    }

    function onPhotoSourceChange() {
        const source = getPhotoSource();
        togglePhotoPanels();
        if (source === 'rascunho') {
            syncFromRascunho();
            return;
        }
        readFormIntoState();
        applyCard();
    }

    async function lookupCrest(type, term) {
        const cfg = getConfig();
        const query = resolveCrestSearchTerm(type, term);
        if (!cfg.crestLookupUrl || !query || query.length < 2) {
            return { ok: false, results: [], error: 'Digite pelo menos 2 caracteres.' };
        }
        const url = `${cfg.crestLookupUrl}?type=${encodeURIComponent(type)}&term=${encodeURIComponent(query)}`;
        try {
            const res = await fetch(url, { credentials: 'same-origin' });
            let data = {};
            try {
                data = await res.json();
            } catch (e) {
                return { ok: false, results: [], error: 'Resposta inválida. Faça login como staff.' };
            }
            if (!res.ok) {
                return { ok: false, results: [], error: data.error || 'Erro na busca (verifique se está logado).' };
            }
            return { ok: true, results: data.results || [], error: '' };
        } catch (e) {
            return { ok: false, results: [], error: 'Falha de rede ao buscar escudos.' };
        }
    }

    function showCrestResults(type, html) {
        const resultsEl = $(`cc-crest-${type}-results`);
        if (!resultsEl) return;
        resultsEl.innerHTML = html;
        resultsEl.hidden = false;
    }

    function hideCrestResults(type) {
        const resultsEl = $(`cc-crest-${type}-results`);
        if (!resultsEl) return;
        resultsEl.hidden = true;
        resultsEl.innerHTML = '';
    }

    function renderCrestHits(type, hits) {
        const html = hits.map((h) => {
            const safeLabel = String(h.label || '').replace(/"/g, '&quot;');
            const url = type === 'club' ? fixClubCrestUrl(h.url, h.id) : (h.url || '');
            const disp = crestDisplayUrl(url);
            const fallback = type === 'club' && h.id
                ? crestDisplayUrl(fixClubCrestUrl('', h.id))
                : '';
            const onerr = fallback
                ? ` onerror="if(this.dataset.fallback){this.src=this.dataset.fallback;this.onerror=null;}" data-fallback="${fallback.replace(/"/g, '&quot;')}"`
                : '';
            return `<button type="button" data-id="${h.id}" data-label="${safeLabel}" data-url="${url}">
                <img src="${disp}" alt=""${onerr}>${h.label}
            </button>`;
        }).join('');
        showCrestResults(type, html);
        const resultsEl = $(`cc-crest-${type}-results`);
        resultsEl?.querySelectorAll('button').forEach((btn) => {
            btn.addEventListener('click', () => {
                selectCrest(type, {
                    id: btn.dataset.id,
                    label: btn.dataset.label,
                    url: btn.dataset.url,
                });
            });
        });
    }

    async function runCrestSearch(type, termOverride) {
        const searchEl = $(`cc-crest-${type}-search`);
        const term = (termOverride ?? searchEl?.value ?? '').trim();
        if (term.length < 2) {
            showCrestResults(type, '<p class="card-creator-crest-msg">Digite pelo menos 2 letras e clique em Buscar.</p>');
            return;
        }
        showCrestResults(type, '<p class="card-creator-crest-msg">Buscando…</p>');
        const { ok, results, error } = await lookupCrest(type, term);
        if (!ok) {
            showCrestResults(type, `<p class="card-creator-crest-msg card-creator-crest-msg--error">${error}</p>`);
            return;
        }
        if (!results.length) {
            showCrestResults(
                type,
                '<p class="card-creator-crest-msg card-creator-crest-msg--error">Nenhum resultado. Tente em inglês (ex.: Brazil, Icons, Vasco) ou cole uma URL abaixo.</p>',
            );
            return;
        }
        renderCrestHits(type, results);
    }

    function selectCrest(type, entry) {
        const set = (id, v) => { const el = $(id); if (el) el.value = v; };
        const url = type === 'club' ? fixClubCrestUrl(entry.url, entry.id) : (entry.url || '');
        set(`cc-crest-${type}-search`, entry.label || '');
        set(`cc-crest-${type}-id`, entry.id || '');
        set(`cc-crest-${type}-url`, url);
        hideCrestResults(type);
        syncCrestsFromForm();
    }

    function applyCrestFromUrl(type) {
        const id = ($(`cc-crest-${type}-id`)?.value || '').trim();
        let url = ($(`cc-crest-${type}-url`)?.value || '').trim();
        if (!url) return;
        if (type === 'club') url = fixClubCrestUrl(url, id);
        const label = ($(`cc-crest-${type}-search`)?.value || '').trim() || 'Custom';
        selectCrest(type, { id: '', label, url });
    }

    function initCrestSearch() {
        const cfg = getConfig();

        ['nation', 'league', 'club'].forEach((type) => {
            const searchEl = $(`cc-crest-${type}-search`);
            if (!searchEl) return;

            document.querySelector(`[data-crest-search="${type}"]`)?.addEventListener('click', () => {
                runCrestSearch(type);
            });

            searchEl.addEventListener('keydown', (e) => {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    runCrestSearch(type);
                }
            });

            $(`cc-crest-${type}-url`)?.addEventListener('change', () => applyCrestFromUrl(type));
            $(`cc-show-crest-${type}`)?.addEventListener('change', syncCrestsFromForm);
        });

        if (cfg.rascunhoNacionalidade && !state.crests?.nation?.id) {
            runCrestSearch('nation', cfg.rascunhoNacionalidade);
        }
    }

    function ensureDefaultCrests() {
        const existing = state.crests && typeof state.crests === 'object' ? state.crests : {};
        const show = existing.show && typeof existing.show === 'object' ? existing.show : {};
        state.crests = normalizeCrests({
            crests: {
                nation: existing.nation || {},
                club: existing.club || {},
                league: existing.league?.url ? existing.league : { ...DEFAULT_ICON_LEAGUE },
                show: {
                    nation: show.nation !== false,
                    club: show.club !== false,
                    league: show.league !== false,
                },
            },
        });
    }

    function init() {
        const dataEl = $('card-creator-initial-state');
        if (dataEl) {
            try {
                state = JSON.parse(dataEl.textContent);
            } catch (e) {
                state = {};
            }
        }
        ensureDefaultCrests();

        cardEl = $('fut-creator-card');
        photoClipEl = cardEl?.querySelector('.fut-creator-card__photo-clip');
        photoWrapEl = cardEl?.querySelector('.fut-creator-card__photo-wrap');
        photoMoverEl = cardEl?.querySelector('.fut-creator-card__photo-mover');
        photoEl = cardEl?.querySelector('.fut-creator-card__photo');

        fillFormFromState();
        applyCrests();
        initPhotoDrag();
        initCrestSearch();

        document.querySelectorAll('.card-creator-tpl-btn').forEach((btn) => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.card-creator-tpl-btn').forEach((b) => b.classList.remove('active'));
                btn.classList.add('active');
                render();
            });
        });

        document.querySelectorAll('.card-creator-fifa-btn').forEach((btn) => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.card-creator-fifa-btn').forEach((b) => b.classList.remove('active'));
                btn.classList.add('active');
                render();
            });
        });

        const fifaFilter = $('cc-fifa-filter');
        if (fifaFilter) {
            fifaFilter.addEventListener('input', () => {
                const q = fifaFilter.value.trim().toLowerCase();
                document.querySelectorAll('.card-creator-fifa-btn').forEach((btn) => {
                    const label = (btn.title || btn.textContent || '').toLowerCase();
                    btn.style.display = !q || label.includes(q) ? '' : 'none';
                });
            });
        }

        document.querySelectorAll('input[name="cc-photo-source"]').forEach((inp) => {
            inp.addEventListener('change', onPhotoSourceChange);
        });

        document.querySelectorAll('input[name="cc-photo-fade"]').forEach((inp) => {
            inp.addEventListener('change', () => {
                // Em mobile, alguns reflows/focos causam salto de scroll.
                // Preserva a posição para a experiência ficar estável.
                const x = window.scrollX;
                const y = window.scrollY;
                render();
                requestAnimationFrame(() => window.scrollTo(x, y));
            });
        });

        document.querySelectorAll('input[name="cc-name-fade"]').forEach((inp) => {
            inp.addEventListener('change', () => {
                const x = window.scrollX;
                const y = window.scrollY;
                toggleNameFadePanel();
                render();
                requestAnimationFrame(() => window.scrollTo(x, y));
            });
        });

        $('cc-name-fade-intensity')?.addEventListener('input', () => {
            const x = window.scrollX;
            const y = window.scrollY;
            updateNameFadeIntensityLabel();
            render();
            requestAnimationFrame(() => window.scrollTo(x, y));
        });

        const inputs = document.querySelectorAll(
            '#card-creator-controls input:not([name="cc-photo-source"]):not([name="cc-photo-fade"]):not([name="cc-name-fade"]):not(#cc-color-unified):not(#cc-colors-unified):not([id^="cc-crest-"]), #card-creator-controls select'
        );
        inputs.forEach((inp) => {
            inp.addEventListener('input', render);
            inp.addEventListener('change', render);
        });

        COLOR_INPUT_IDS.forEach(([, id]) => {
            const el = $(id);
            if (!el) return;
            const onColor = () => {
                if (isColorsUnifiedMode()) return;
                state.colors = readColorsFromForm();
                applyColors();
            };
            el.addEventListener('input', onColor);
            el.addEventListener('change', onColor);
        });

        $('cc-colors-unified')?.addEventListener('change', () => {
            if (isColorsUnifiedMode()) {
                const hex = $('cc-color-unified')?.value
                    || $('cc-color-rating')?.value
                    || DEFAULT_COLORS.rating;
                $('cc-color-unified').value = hex;
                applyUnifiedColorToInputs(hex);
            }
            toggleColorsPanel();
            state.colors_unified = isColorsUnifiedMode();
            state.colors = readColorsFromForm();
            applyColors();
        });

        $('cc-color-unified')?.addEventListener('input', () => {
            if (!isColorsUnifiedMode()) return;
            applyUnifiedColorToInputs($('cc-color-unified').value);
            state.colors = readColorsFromForm();
            applyColors();
        });
        $('cc-color-unified')?.addEventListener('change', () => {
            if (!isColorsUnifiedMode()) return;
            applyUnifiedColorToInputs($('cc-color-unified').value);
            state.colors = readColorsFromForm();
            applyColors();
        });

        bind('cc-btn-sync-photo', 'click', syncFromRascunho);
        bind('cc-btn-remove-bg', 'click', removePhotoBackground);
        bind('cc-photo-upload', 'change', (e) => {
            loadPhotoFile(e.target.files[0]);
            e.target.value = '';
        });
        bind('cc-btn-save', 'click', saveCard);
        bind('cc-btn-reset-photo', 'click', resetPhotoTransform);

        $('cc-photo-url')?.addEventListener('change', () => {
            if (getPhotoSource() === 'url') render();
        });
    }

    document.addEventListener('DOMContentLoaded', init);
})();
