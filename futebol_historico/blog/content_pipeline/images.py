"""Download de imagens do Wikimedia Commons."""
from urllib.parse import quote

import requests

SESSION = requests.Session()
SESSION.headers.update({'User-Agent': 'FutebolHistorico/1.0 (redacao-jogadores)'})


def download_commons_file(filename: str, width: int = 800) -> tuple[bytes, str]:
    """
    Baixa arquivo do Commons. Retorna (bytes, extensão sugerida).
    """
    safe_name = filename.replace(' ', '_')
    url = f'https://commons.wikimedia.org/wiki/Special:FilePath/{quote(safe_name)}?width={width}'
    r = SESSION.get(url, timeout=45, allow_redirects=True)
    r.raise_for_status()
    content_type = r.headers.get('Content-Type', 'image/jpeg')
    ext = 'jpg'
    if 'png' in content_type:
        ext = 'png'
    elif 'webp' in content_type:
        ext = 'webp'
    return r.content, ext
