"""Extrai modelos de carta FIFA 26 do FifaRosters (create-card + fut26.css)."""
from __future__ import annotations

import json
import re
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen

BASE_URL = 'https://www.fifarosters.com/'
CREATE_CARD_URL = urljoin(BASE_URL, 'create-card')
FUT26_CSS_URL = urljoin(BASE_URL, 'css/fut26.css?v=2026-04-18--16-15')
USER_AGENT = 'FutebolHistorico/1.0 (card-asset-import; +local-dev)'


def _fetch(url: str, timeout: int = 60) -> bytes:
    req = Request(url, headers={'User-Agent': USER_AGENT})
    with urlopen(req, timeout=timeout) as resp:
        return resp.read()


def _normalize_css_class(css_class: str) -> str:
    parts = [p for p in css_class.split() if p and p != 'dark-card']
    if 'nonrare' in parts:
        parts = [p for p in parts if p != 'nonrare'] + ['nonrare']
    return ' '.join(parts)


def _css_class_variants(css_class: str) -> list[str]:
    base = _normalize_css_class(css_class)
    variants = [base]
    variants.append(base.replace('-', '_'))
    variants.append(base.replace('_', '-'))
    if 'futchamp' in base:
        variants.append(base.replace('futchamp', 'fut_champions'))
    if 'if ' in base:
        variants.append(base.replace('if ', 'totw '))
    seen = set()
    out = []
    for v in variants:
        if v and v not in seen:
            seen.add(v)
            out.append(v)
    return out


def build_css_image_map(css_text: str) -> dict[str, str]:
    """Mapeia classes CSS (ex.: ``rare gold``) para caminho relativo do PNG."""
    css_map: dict[str, str] = {}
    for chunk in css_text.split('}'):
        if 'cards_bg' not in chunk or '{' not in chunk or '.fut26.playercard' not in chunk:
            continue
        sel, body = chunk.rsplit('{', 1)
        m_url = re.search(r'url\(([^)]+)\)', body)
        if not m_url:
            continue
        url = m_url.group(1).strip('"\'').split('?')[0]
        tail = sel.split('.fut26.playercard')[-1].lstrip('.')
        classes = [c for c in tail.split('.') if c and c != 'card-mini']
        css_class = ' '.join(classes)
        if css_class and css_class not in css_map:
            css_map[css_class] = url
    return css_map


def resolve_image(css_class: str, css_map: dict[str, str]) -> str | None:
    for variant in _css_class_variants(css_class):
        if variant in css_map:
            return css_map[variant]
    return None


def parse_card_colors(html: str) -> dict:
    start = html.find('card_colors = {')
    if start < 0:
        return {}
    end = html.find('};', start) + 1
    return json.loads(html[start + len('card_colors = '):end])


def parse_fut26_styles(html: str, css_map: dict[str, str]) -> list[dict]:
    """Lista estilos FIFA 26 do modal (fut26) com rótulo e imagem quando existir."""
    pat = re.compile(
        r'<div class="card_container[^"]*">\s*'
        r'<a href="#" class="playercard card-small fut26 ([^"]+)" '
        r'onclick="changeCardColor\(\'([^\']+)\', \'([^\']+)\'\)[^>]*></a>\s*'
        r'<span>([^<]+)</span>',
        re.DOTALL,
    )
    card_colors = parse_card_colors(html)
    styles: list[dict] = []
    seen_ids: set[str] = set()

    for m in pat.finditer(html):
        _extra, card_id, css_class, label = m.groups()
        if card_id in seen_ids:
            continue
        seen_ids.add(card_id)
        meta = card_colors.get(card_id, {})
        lookup_class = meta.get('css_class') or css_class
        rel = resolve_image(lookup_class, css_map)
        filename = rel.split('/')[-1] if rel else ''
        styles.append({
            'id': card_id,
            'label': label.strip(),
            'css_class': _normalize_css_class(lookup_class),
            'filename': filename,
            'source_path': rel or '',
        })
    return styles


def collect_all_fifa26_png_paths(css_text: str) -> list[str]:
    paths = set(re.findall(r'\.\./(assets/cards/fifa26/[^?)]+)', css_text))
    return sorted(paths)


def import_fifarosters_assets(
    dest_dir: Path,
    *,
    download: bool = True,
    delay: float = 0.05,
) -> dict:
    """
    Baixa PNGs e grava ``manifest.json`` em *dest_dir*.

    Retorna o manifesto gerado.
    """
    dest_dir = Path(dest_dir)
    images_dir = dest_dir / 'fifa26'
    images_dir.mkdir(parents=True, exist_ok=True)

    html = _fetch(CREATE_CARD_URL).decode('utf-8', errors='replace')
    css_text = _fetch(FUT26_CSS_URL).decode('utf-8', errors='replace')
    css_map = build_css_image_map(css_text)
    styles = parse_fut26_styles(html, css_map)
    all_paths = collect_all_fifa26_png_paths(css_text)

    downloaded: dict[str, str] = {}
    errors: list[dict] = []

    if download:
        for rel in all_paths:
            filename = rel.split('/')[-1]
            local = images_dir / filename
            if local.exists() and local.stat().st_size > 0:
                downloaded[rel] = filename
                continue
            url = urljoin(BASE_URL, rel)
            try:
                data = _fetch(url)
                local.write_bytes(data)
                downloaded[rel] = filename
                if delay:
                    time.sleep(delay)
            except (HTTPError, URLError, TimeoutError) as exc:
                errors.append({'path': rel, 'error': str(exc)})

    for style in styles:
        rel = style.get('source_path') or ''
        if rel:
            fn = rel.split('/')[-1]
            style['static_file'] = f'fifa26/{fn}'
            style['has_image'] = (images_dir / fn).exists()
        else:
            style['static_file'] = ''
            style['has_image'] = False

    manifest = {
        'version': 1,
        'source': 'fifarosters.com',
        'fifa_year': 26,
        'imported_at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'styles_count': len(styles),
        'styles_with_image': sum(1 for s in styles if s.get('has_image')),
        'images_downloaded': len(downloaded),
        'images_total_in_css': len(all_paths),
        'errors': errors,
        'styles': styles,
    }
    (dest_dir / 'manifest.json').write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding='utf-8',
    )
    return manifest
