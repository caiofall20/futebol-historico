"""Cliente Wikidata para buscar dados de jogadores de futebol."""
import re
from dataclasses import dataclass, field
from datetime import date
from typing import Any, Optional

import requests

WIKIDATA_API = 'https://www.wikidata.org/w/api.php'
USER_AGENT = 'FutebolHistorico/1.0 (https://github.com/; redacao-jogadores)'
SESSION = requests.Session()
SESSION.headers.update({'User-Agent': USER_AGENT})

FOOTBALL_PLAYER_Q = 'Q937857'  # association football player
FOOTBALL_PLAYER_VARIANTS = {FOOTBALL_PLAYER_Q, 'Q1144666'}  # soccer player

POSITION_MAP = {
    'Q193592': 'Meia',
    'Q280658': 'Atacante',
    'Q268258': 'Atacante',
    'Q527969': 'Atacante',
    'Q201330': 'Defensor',
    'Q336286': 'Defensor',
    'Q9028594': 'Goleiro',
    'Q2494180': 'Goleiro',
    'Q6156505': 'Lateral',
    'Q193592': 'Meia',
    'Q1142118': 'Volante',
    'Q193592': 'Meia-atacante',
}

FOOT_LABELS = {
    'Q1090': 'Destro',
    'Q1091': 'Canhoto',
    'Q3039938': 'Ambidestro',
}


@dataclass
class TeamStint:
    nome: str
    inicio: Optional[date] = None
    fim: Optional[date] = None


@dataclass
class WikidataPlayer:
    entity_id: str
    nome: str
    nacionalidade: str = 'Desconhecida'
    altura: str = ''
    perna: str = ''
    posicoes: list[str] = field(default_factory=list)
    times: list[TeamStint] = field(default_factory=list)
    inicio_carreira: Optional[date] = None
    fim_carreira: Optional[date] = None
    imagem_commons: str = ''
    wikipedia_titulo_pt: str = ''
    fontes: list[str] = field(default_factory=list)


def _api(params: dict) -> dict:
    params.setdefault('format', 'json')
    r = SESSION.get(WIKIDATA_API, params=params, timeout=30)
    r.raise_for_status()
    return r.json()


def _get_label(entity_id: str, lang: str = 'pt') -> str:
    data = _api({
        'action': 'wbgetentities',
        'ids': entity_id,
        'props': 'labels',
        'languages': f'{lang}|en',
    })
    ent = data.get('entities', {}).get(entity_id, {})
    labels = ent.get('labels', {})
    if lang in labels:
        return labels[lang]['value']
    if 'en' in labels:
        return labels['en']['value']
    return entity_id


def _parse_wikidata_date(time_str: str) -> Optional[date]:
    if not time_str or time_str.startswith('-'):
        return None
    # Wikidata costuma trazer strings ISO como:
    # +1968-02-05T00:00:00Z
    # mas também pode vir como datas parciais/presisao:
    # +1980-00-00T00:00:00Z, +1974-03-00T00:00:00Z, +1990-00-00T...
    m = re.match(r'\+?(\d{4})(?:-(\d{2}))?(?:-(\d{2}))?', time_str)
    if not m:
        return None
    y = int(m.group(1))
    mo_raw = m.group(2)
    d_raw = m.group(3)
    mo = int(mo_raw) if mo_raw else 1
    d = int(d_raw) if d_raw else 1
    # Quando o Wikidata usa "00" para indicar desconhecido, normalizamos para 1.
    if mo == 0:
        mo = 1
    if d == 0:
        d = 1
    try:
        return date(y, mo, d)
    except ValueError:
        return date(y, 1, 1)


def _claim_snak_value(snak: dict) -> Any:
    if snak.get('snaktype') != 'value':
        return None
    return snak.get('datavalue', {}).get('value')


def _is_football_player(entity: dict) -> bool:
    for claim in entity.get('claims', {}).get('P106', []):
        val = _claim_snak_value(claim.get('mainsnak', {}))
        if isinstance(val, dict) and val.get('id') in FOOTBALL_PLAYER_VARIANTS:
            return True
    return False


def _entity_label(entity: dict) -> str:
    labels = entity.get('labels', {})
    for lang in ('pt', 'en'):
        if lang in labels:
            return labels[lang]['value']
    return ''


def _score_football_entity(entity: dict, nome_busca: str) -> int:
    """Pontua candidatos — evita homônimos (ex.: só 'Nakata')."""
    if not _is_football_player(entity):
        return -1

    score = 10
    claims = entity.get('claims', {})

    if claims.get('P27'):
        score += 35
    if claims.get('P54'):
        score += 15 + min(15, len(claims['P54']))
    if claims.get('P569'):
        score += 10
    if claims.get('P413'):
        score += 8
    if claims.get('P18'):
        score += 5
    if claims.get('P2048'):
        score += 3

    label = _entity_label(entity).lower()
    busca = nome_busca.lower().strip()
    busca_words = set(busca.split())

    if busca in label or label in busca:
        score += 30
    elif busca_words and busca_words <= set(label.split()):
        score += 25
    elif any(w in label for w in busca_words if len(w) > 2):
        score += 8
    else:
        score -= 15

    # Nome muito curto na busca: exige correspondência forte
    if len(busca_words) == 1 and busca not in label:
        score -= 25

    return score


def search_football_player(nome: str) -> Optional[WikidataPlayer]:
    """Busca jogador de futebol pelo nome; retorna o melhor candidato."""
    candidates = []
    for lang in ('pt', 'en'):
        search = _api({
            'action': 'wbsearchentities',
            'search': nome,
            'language': lang,
            'type': 'item',
            'limit': 10,
        })
        for c in search.get('search', []):
            if c['id'] not in [x['id'] for x in candidates]:
                candidates.append(c)
        if len(candidates) >= 8:
            break

    if not candidates:
        return None

    ids = [c['id'] for c in candidates[:10]]
    entities_data = _api({
        'action': 'wbgetentities',
        'ids': '|'.join(ids),
        'props': 'claims|labels|sitelinks',
        'languages': 'pt|en',
    })
    entities = entities_data.get('entities', {})

    best_id = None
    best_score = -1
    for cid in ids:
        ent = entities.get(cid)
        if not ent:
            continue
        sc = _score_football_entity(ent, nome)
        if sc > best_score:
            best_score = sc
            best_id = cid

    if not best_id or best_score < 25:
        return None

    ent = entities.get(best_id)
    if not ent:
        return None

    return _parse_entity(best_id, ent, nome)


def _parse_entity(entity_id: str, entity: dict, nome_busca: str) -> WikidataPlayer:
    labels = entity.get('labels', {})
    nome = labels.get('pt', labels.get('en', {})).get('value', nome_busca)

    player = WikidataPlayer(
        entity_id=entity_id,
        nome=nome,
        fontes=[f'https://www.wikidata.org/wiki/{entity_id}'],
    )

    # Nacionalidade P27
    for claim in entity.get('claims', {}).get('P27', []):
        val = _claim_snak_value(claim.get('mainsnak', {}))
        if isinstance(val, dict) and val.get('id'):
            player.nacionalidade = _get_label(val['id'], 'pt')
            break

    # Altura P2048 (metros)
    for claim in entity.get('claims', {}).get('P2048', []):
        val = _claim_snak_value(claim.get('mainsnak', {}))
        if isinstance(val, dict) and 'amount' in val:
            try:
                m = float(val['amount'])
                if m > 3:  # Wikidata às vezes usa centímetros
                    m = m / 100
                player.altura = f"{m:.2f}".replace('.', ',') + ' m'
            except (TypeError, ValueError):
                pass
            break

    # Pé dominante P741
    for claim in entity.get('claims', {}).get('P741', []):
        val = _claim_snak_value(claim.get('mainsnak', {}))
        if isinstance(val, dict) and val.get('id'):
            player.perna = FOOT_LABELS.get(val['id'], _get_label(val['id'], 'pt'))
            break

    # Posição P413
    posicoes = []
    for claim in entity.get('claims', {}).get('P413', []):
        val = _claim_snak_value(claim.get('mainsnak', {}))
        if isinstance(val, dict) and val.get('id'):
            pos = POSITION_MAP.get(val['id'], _get_label(val['id'], 'pt'))
            if pos and pos not in posicoes:
                posicoes.append(pos)
    player.posicoes = posicoes

    # Clubes P54
    times = []
    dates_start = []
    dates_end = []
    for claim in entity.get('claims', {}).get('P54', []):
        val = _claim_snak_value(claim.get('mainsnak', {}))
        if not isinstance(val, dict) or not val.get('id'):
            continue
        team_name = _get_label(val['id'], 'pt')
        inicio = fim = None
        for qid, quals in claim.get('qualifiers', {}).items():
            for q in quals:
                qval = _claim_snak_value(q)
                if isinstance(qval, dict) and 'time' in qval:
                    parsed = _parse_wikidata_date(qval['time'])
                    if qid == 'P580' and parsed:
                        inicio = parsed
                        dates_start.append(parsed)
                    elif qid == 'P582' and parsed:
                        fim = parsed
                        dates_end.append(parsed)
        times.append(TeamStint(nome=team_name, inicio=inicio, fim=fim))

    times.sort(key=lambda t: t.inicio or date(1900, 1, 1))
    player.times = times

    if dates_start:
        player.inicio_carreira = min(dates_start)
    if dates_end:
        player.fim_carreira = max(dates_end)
    elif dates_start:
        player.fim_carreira = date.today()

    # Data de nascimento P569 — estima início/fim se clubes sem datas
    for claim in entity.get('claims', {}).get('P569', []):
        val = _claim_snak_value(claim.get('mainsnak', {}))
        if isinstance(val, dict) and 'time' in val:
            nasc = _parse_wikidata_date(val['time'])
            if nasc:
                if not player.inicio_carreira:
                    try:
                        player.inicio_carreira = date(nasc.year + 17, 1, 1)
                    except ValueError:
                        pass
                if not player.fim_carreira:
                    player.fim_carreira = date.today()
            break

    # Aposentadoria P2031
    for claim in entity.get('claims', {}).get('P2031', []):
        val = _claim_snak_value(claim.get('mainsnak', {}))
        if isinstance(val, dict) and 'time' in val:
            apos = _parse_wikidata_date(val['time'])
            if apos:
                player.fim_carreira = apos
            break

    # Imagem P18
    for claim in entity.get('claims', {}).get('P18', []):
        val = _claim_snak_value(claim.get('mainsnak', {}))
        if isinstance(val, str):
            player.imagem_commons = val
            break

    # Wikipedia PT sitelink
    sitelinks = entity.get('sitelinks', {})
    if 'ptwiki' in sitelinks:
        title = sitelinks['ptwiki']['title']
        player.wikipedia_titulo_pt = title
        player.fontes.append(f'https://pt.wikipedia.org/wiki/{title.replace(" ", "_")}')
    elif 'enwiki' in sitelinks:
        title = sitelinks['enwiki']['title']
        player.wikipedia_titulo_pt = title
        player.fontes.append(f'https://en.wikipedia.org/wiki/{title.replace(" ", "_")}')

    return player
