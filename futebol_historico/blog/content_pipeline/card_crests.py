"""Escudos e bandeiras FIFA (FifaRosters) para o editor de carta."""
from __future__ import annotations

import json
import re
from html import unescape
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

FIFAROSTERS_BASE = 'https://www.fifarosters.com/'
USER_AGENT = 'FutebolHistorico/1.0 (card-crest-lookup; +local-dev)'

# Liga «Icons» — badge central em cartas Icon (FIFA 26)
DEFAULT_ICON_LEAGUE_ID = '2118'

LOOKUP_ENDPOINTS = {
    'nation': 'lookupnations.php',
    'club': 'lookupteams.php',
    'league': 'lookupleagues.php',
}

# Nem todo escudo existe em fifa26 (ex.: Milan id 47 → 404 em fifa26, OK em fifa25).
CLUB_ASSET_VERSIONS = ('fifa26', 'fifa25', 'fifa24', 'fifa23', 'fifa22', 'fifa21', 'fifa20')

_CLUB_URL_CACHE: dict[str, str] = {}


def _url_exists(url: str) -> bool:
    if not url:
        return False
    req = Request(url, method='HEAD', headers={'User-Agent': USER_AGENT})
    try:
        with urlopen(req, timeout=8) as resp:
            return resp.status == 200
    except URLError:
        return False


def resolve_club_crest_url(asset_id: str, hint_url: str = '') -> str:
    """Escolhe a primeira URL de escudo de clube que responder 200."""
    aid = str(asset_id or '').strip()
    if not aid:
        return ''
    if aid in _CLUB_URL_CACHE:
        return _CLUB_URL_CACHE[aid]

    candidates: list[str] = []
    if hint_url:
        candidates.append(hint_url.strip())
    for ver in CLUB_ASSET_VERSIONS:
        candidates.append(f'{FIFAROSTERS_BASE}assets/clubs/{ver}/{aid}.png')

    seen: set[str] = set()
    for url in candidates:
        if not url or url in seen:
            continue
        seen.add(url)
        if _url_exists(url):
            _CLUB_URL_CACHE[aid] = url
            return url

    fallback = f'{FIFAROSTERS_BASE}assets/clubs/fifa25/{aid}.png'
    _CLUB_URL_CACHE[aid] = fallback
    return fallback


def crest_asset_url(crest_type: str, asset_id: str, *, img_url: str = '') -> str:
    """Monta URL do PNG no FifaRosters ou usa URL customizada."""
    if img_url:
        url = img_url.strip()
        if crest_type == 'club' and '/assets/clubs/' in url:
            return resolve_club_crest_url(asset_id, url)
        return url
    aid = str(asset_id or '').strip()
    if not aid:
        return ''
    if crest_type == 'nation':
        return f'{FIFAROSTERS_BASE}assets/nations/fifa17/{aid}.png'
    if crest_type == 'club':
        return resolve_club_crest_url(aid)
    if crest_type == 'league':
        return f'{FIFAROSTERS_BASE}assets/leagues/fifa26/{aid}.png'
    return ''


def _extract_img_src(html_fragment: str) -> str:
    if not html_fragment:
        return ''
    m = re.search(r'src=["\']([^"\']+)["\']', html_fragment)
    return unescape(m.group(1)) if m else ''


_NATION_ALIASES = {
    'brasil': 'Brazil',
    'brazil': 'Brazil',
    'argentina': 'Argentina',
    'portugal': 'Portugal',
    'espanha': 'Spain',
    'spain': 'Spain',
    'italia': 'Italy',
    'itália': 'Italy',
    'franca': 'France',
    'frança': 'France',
    'alemanha': 'Germany',
    'inglaterra': 'England',
    'holanda': 'Netherlands',
    'uruguai': 'Uruguay',
    'colombia': 'Colombia',
    'colômbia': 'Colombia',
}

_CLUB_ALIASES = {
    'milão': 'Milan',
    'milao': 'Milan',
    'milan': 'Milan',
    'ac milan': 'Milan',
    'inter': 'Inter',
    'inter milan': 'Inter',
    'internazionale': 'Inter',
    'juventus': 'Juventus',
    'roma': 'Roma',
    'lazio': 'Lazio',
    'napoli': 'Napoli',
    'são paulo': 'Sao Paulo',
    'sao paulo': 'Sao Paulo',
    'corinthians': 'Corinthians',
    'palmeiras': 'Palmeiras',
    'flamengo': 'Flamengo',
    'vasco': 'Vasco da Gama',
    'vasco da gama': 'Vasco da Gama',
    'barcelona': 'FC Barcelona',
    'barça': 'FC Barcelona',
    'real madrid': 'Real Madrid',
    'man city': 'Manchester City',
    'man united': 'Manchester United',
    'psg': 'Paris SG',
    'paris': 'Paris SG',
    'bayern': 'Bayern Munich',
    'borussia': 'Borussia Dortmund',
}


def resolve_crest_search_term(crest_type: str, term: str) -> str:
    raw = term.strip()
    if not raw:
        return raw
    key = raw.lower()
    if crest_type == 'club':
        return _CLUB_ALIASES.get(key, raw)
    if crest_type == 'nation':
        return _NATION_ALIASES.get(key, raw)
    return raw


def lookup_crests(crest_type: str, term: str, limit: int = 12) -> list[dict]:
    """Busca na API pública do FifaRosters (nation / club / league)."""
    endpoint = LOOKUP_ENDPOINTS.get(crest_type)
    search_term = resolve_crest_search_term(crest_type, term)
    if not endpoint or not search_term or len(search_term) < 2:
        return []
    q = quote(search_term)
    url = f'{FIFAROSTERS_BASE}{endpoint}?term={q}'
    req = Request(url, headers={'User-Agent': USER_AGENT, 'Accept': 'application/json'})
    try:
        with urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode('utf-8'))
    except (URLError, json.JSONDecodeError, TimeoutError, ValueError):
        return []
    if not isinstance(data, list):
        return []
    out = []
    seen = set()
    for row in data[:limit]:
        if not isinstance(row, dict):
            continue
        cid = str(row.get('value', '')).strip()
        label = str(row.get('label', '')).strip()
        if not cid or cid in seen or label.lower() == 'no results':
            continue
        seen.add(cid)
        hint = _extract_img_src(row.get('img', ''))
        if crest_type == 'club':
            img_url = resolve_club_crest_url(cid, hint)
        else:
            img_url = hint or crest_asset_url(crest_type, cid)
        out.append({
            'id': cid,
            'label': label,
            'url': img_url,
            'type': crest_type,
        })
    return out


def crest_entry(crest_type: str, asset_id: str = '', label: str = '', url: str = '') -> dict:
    return {
        'id': str(asset_id or ''),
        'label': label or '',
        'url': url or crest_asset_url(crest_type, asset_id, img_url=url),
        'type': crest_type,
    }


def default_icon_league_entry() -> dict:
    return crest_entry('league', DEFAULT_ICON_LEAGUE_ID, 'Icons (ICN)')


def resolve_nation_from_label(nacionalidade: str) -> dict | None:
    """Tenta achar bandeira pela nacionalidade do rascunho."""
    if not nacionalidade or len(nacionalidade.strip()) < 2:
        return None
    raw = nacionalidade.strip()
    term = _NATION_ALIASES.get(raw.lower(), raw)
    hits = lookup_crests('nation', term, limit=3)
    if not hits and term != raw:
        hits = lookup_crests('nation', raw, limit=3)
    return hits[0] if hits else None


def default_crests_for_rascunho(rascunho, *, include_icon_league: bool = True) -> dict:
    nat = resolve_nation_from_label(getattr(rascunho, 'nacionalidade', '') or '')
    nation = nat or crest_entry('nation', '', '')
    league = default_icon_league_entry() if include_icon_league else crest_entry('league', '', '')
    return {
        'nation': nation,
        'club': crest_entry('club', '', ''),
        'league': league,
        'show': {
            'nation': bool(nat and nat.get('url')),
            'club': False,
            'league': include_icon_league,
        },
    }


def normalize_crests(design: dict) -> dict:
    """Garante estrutura crests + show no design salvo."""
    raw = design.get('crests') if isinstance(design.get('crests'), dict) else {}
    show_raw = raw.get('show') if isinstance(raw.get('show'), dict) else {}

    def _one(key: str, ctype: str) -> dict:
        block = raw.get(key) if isinstance(raw.get(key), dict) else {}
        eid = str(block.get('id', '') or '').strip()
        stored_url = (block.get('url', '') or '').strip()
        if ctype == 'club' and eid:
            url = resolve_club_crest_url(eid, stored_url)
        else:
            url = stored_url or crest_asset_url(ctype, eid)
        return {
            'id': str(eid or ''),
            'label': block.get('label', '') or '',
            'url': url,
            'type': ctype,
        }

    nation = _one('nation', 'nation')
    club = _one('club', 'club')
    league = _one('league', 'league')

    show = {
        'nation': show_raw.get('nation', design.get('show_nation', False)),
        'club': show_raw.get('club', design.get('show_club', False)),
        'league': show_raw.get('league', design.get('show_league', False)),
    }
    return {'nation': nation, 'club': club, 'league': league, 'show': show}
