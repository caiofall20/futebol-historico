"""Configuração completa do editor de carta FUT."""
from __future__ import annotations

import json
from pathlib import Path

from django.conf import settings

from .card_crests import default_crests_for_rascunho, normalize_crests
from .card_stats import CartaFutStats, compute_carta_stats, posicao_abrev

_FIFAROSTERS_MANIFEST: dict | None = None


CARD_TEMPLATES = [
    {'id': 'icon_gold', 'label': 'Ícone / Ouro'},
    {'id': 'toty', 'label': 'Team of the Year'},
    {'id': 'tots', 'label': 'Team of the Season'},
    {'id': 'totw', 'label': 'Team of the Week'},
    {'id': 'rare_gold', 'label': 'Ouro Raro'},
    {'id': 'hero', 'label': 'Hero'},
    {'id': 'flashback', 'label': 'Flashback'},
    {'id': 'common_gold', 'label': 'Ouro Comum'},
]

def _fifarosters_manifest_path() -> Path:
    return (
        Path(settings.BASE_DIR)
        / 'blog'
        / 'static'
        / 'blog'
        / 'card_assets'
        / 'fifarosters'
        / 'manifest.json'
    )


def load_fifarosters_styles() -> list[dict]:
    """Estilos FIFA 26 importados do FifaRosters (manifest.json)."""
    global _FIFAROSTERS_MANIFEST
    if _FIFAROSTERS_MANIFEST is None:
        path = _fifarosters_manifest_path()
        if not path.exists():
            _FIFAROSTERS_MANIFEST = {'styles': []}
        else:
            _FIFAROSTERS_MANIFEST = json.loads(path.read_text(encoding='utf-8'))
    out = []
    for s in _FIFAROSTERS_MANIFEST.get('styles', []):
        if not s.get('has_image') and not s.get('static_file'):
            continue
        out.append({
            'id': s['id'],
            'label': s.get('label') or s['id'],
            'static_file': s.get('static_file', ''),
            'css_class': s.get('css_class', ''),
        })
    return out


def fifarosters_assets_imported() -> bool:
    return _fifarosters_manifest_path().exists()


def default_fifa_background_id() -> str:
    """ID do modelo FIFA 26 usado ao criar carta nova."""
    styles = load_fifarosters_styles()
    for preferred in ('legend', 'rare_gold', 'icon'):
        for s in styles:
            if s['id'] == preferred:
                return f"fifa26:{s['id']}"
    if styles:
        return f"fifa26:{styles[0]['id']}"
    return 'fifa26:rare_gold'


def default_card_design(rascunho) -> dict:
    """Monta design inicial a partir do rascunho."""
    if getattr(rascunho, 'carta_design', None) and rascunho.carta_design.get('version'):
        return rascunho.carta_design

    if rascunho.carta_stats:
        stats = CartaFutStats.from_dict(rascunho.carta_stats)
    else:
        stats = compute_carta_stats(
            outras_posicoes=rascunho.outras_posicoes or '',
            titulos_champions=rascunho.titulos_champions,
            bola_de_ouro=rascunho.bola_de_ouro,
            mundial_clubes=rascunho.mundial_clubes,
            inicio_carreira=rascunho.inicio_carreira,
            fim_carreira=rascunho.fim_carreira,
            perna=rascunho.perna or '',
        )

    photo_url = ''
    if rascunho.imagem:
        photo_url = rascunho.imagem.url

    foot = 'R'
    if rascunho.perna:
        pl = rascunho.perna.lower()
        if 'canhoto' in pl:
            foot = 'L'
        elif 'ambidestro' in pl:
            foot = 'R'

    return {
        'version': 2,
        'template': 'icon_gold',
        'format': 'full',
        'background': {
            'type': 'preset',
            'value': default_fifa_background_id(),
            'color': '#1a2848',
            'url': '',
        },
        'player': {
            'url': photo_url,
            'source': 'rascunho',
            'x': 0,
            'y': 0,
            'scale': 100,
            'zoom': 100,
            'fade': 'soft',
            'brightness': 100,
            'contrast': 100,
            'saturation': 100,
            'grayscale': False,
        },
        'overall': stats.overall,
        'position': stats.posicao,
        'name': rascunho.nome,
        'nation': rascunho.nacionalidade or '',
        'club': '',
        'league': '',
        'stats': stats.to_dict(),
        'extras': {
            'skill': 4,
            'weak_foot': 4,
            'foot': foot,
            'work_att': 'M',
            'work_def': 'M',
            'chemistry': 'basic',
            'playstyle': '',
        },
        'show_nation': False,
        'show_club': False,
        'show_league': False,
        'name_fade': 'soft',
        'name_fade_intensity': 35,
        'name_fade_color': '#ffffff',
        'crests': default_crests_for_rascunho(rascunho),
        'colors_unified': False,
        'colors': {
            'rating': '#5c4a1a',
            'position': '#5c4a1a',
            'name': '#5c4a1a',
            'stats_label': '#5c4a1a',
            'stats_value': '#2a2210',
        },
    }


def merge_design_update(base: dict, update: dict) -> dict:
    """Mescla atualização parcial do editor."""
    import copy
    result = copy.deepcopy(base)
    for key, val in update.items():
        if isinstance(val, dict) and isinstance(result.get(key), dict):
            result[key] = {**result[key], **val}
        else:
            result[key] = val
    return result
