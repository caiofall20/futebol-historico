"""Resumo da Wikipedia em português para biografia."""
import html
import re
from typing import Optional

import requests

SESSION = requests.Session()
SESSION.headers.update({'User-Agent': 'FutebolHistorico/1.0 (redacao-jogadores)'})


def search_pt_wikipedia(query: str) -> Optional[str]:
    r = SESSION.get(
        'https://pt.wikipedia.org/w/api.php',
        params={
            'action': 'query',
            'list': 'search',
            'srsearch': query,
            'srlimit': 3,
            'format': 'json',
        },
        timeout=25,
    )
    r.raise_for_status()
    results = r.json().get('query', {}).get('search', [])
    if results:
        return results[0]['title']
    return None


def get_article_extract(title: str, lang: str = 'pt') -> tuple[str, str]:
    """
    Retorna (html_paragrafos, url).
    Usa extracts API; limita tamanho para rascunho editável.
    """
    base = f'https://{lang}.wikipedia.org'
    r = SESSION.get(
        f'{base}/w/api.php',
        params={
            'action': 'query',
            'titles': title,
            'prop': 'extracts|info',
            'explaintext': '1',
            'exsectionformat': 'plain',
            'exchars': 2500,
            'format': 'json',
            'inprop': 'url',
        },
        timeout=25,
    )
    r.raise_for_status()
    pages = r.json().get('query', {}).get('pages', {})
    page = next(iter(pages.values()), {})
    if page.get('missing'):
        return '', ''

    extract = page.get('extract', '').strip()
    url = page.get('fullurl', f'{base}/wiki/{title.replace(" ", "_")}')

    if not extract:
        return '', url

    paragraphs = [p.strip() for p in re.split(r'\n+', extract) if p.strip()]
    html_parts = []
    for p in paragraphs[:6]:
        safe = html.escape(p)
        html_parts.append(f'<p>{safe}</p>')

    return '\n'.join(html_parts), url


def resolve_wikipedia_content(nome: str, titulo_hint: str = '') -> tuple[str, str, str]:
    """Retorna (html_biografia_extra, titulo_usado, url)."""
    title = titulo_hint or search_pt_wikipedia(nome)
    if not title:
        return '', '', ''

    content, url = get_article_extract(title, 'pt')
    if not content and titulo_hint:
        content, url = get_article_extract(titulo_hint, 'en')
    return content, title, url
