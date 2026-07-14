"""Renderiza PNG no servidor a partir do JSON do editor (fallback)."""
import io
from typing import Optional

import requests
from PIL import Image, ImageDraw, ImageEnhance, ImageFont

from .card_stats import CartaFutStats
from .fut_card_generator import _load_font

WIDTH, HEIGHT = 450, 630

BG_COLORS = {
    'gold_marble': [(26, 32, 48), (60, 50, 30)],
    'dark_blue': [(12, 18, 40), (20, 35, 70)],
    'toty_blue': [(10, 30, 80), (30, 80, 160)],
    'tots_lightning': [(20, 40, 90), (80, 120, 200)],
    'stadium': [(15, 25, 35), (40, 55, 70)],
    'pitch': [(20, 50, 30), (35, 90, 45)],
    'black_gold': [(8, 8, 12), (80, 65, 25)],
    'purple_hero': [(40, 15, 60), (90, 40, 120)],
    'red_motm': [(60, 15, 15), (120, 40, 40)],
    'gradient_fire': [(40, 20, 10), (120, 60, 20)],
}

FRAME_COLORS = {
    'icon_gold': (212, 175, 55),
    'toty': (100, 180, 255),
    'tots': (70, 130, 255),
    'totw': (30, 30, 30),
    'rare_gold': (212, 175, 55),
    'hero': (180, 100, 220),
    'flashback': (220, 180, 80),
    'common_gold': (180, 150, 60),
}


def _gradient_bg(w: int, h: int, top, bottom) -> Image.Image:
    img = Image.new('RGB', (w, h), top)
    draw = ImageDraw.Draw(img)
    for y in range(h):
        t = y / h
        c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        draw.line([(0, y), (w, y)], fill=c)
    return img


def _load_photo(url: str, timeout: int = 20) -> Optional[Image.Image]:
    if not url:
        return None
    try:
        if url.startswith('/'):
            return None
        r = requests.get(url, timeout=timeout, headers={'User-Agent': 'FutebolHistorico/1.0'})
        r.raise_for_status()
        return Image.open(io.BytesIO(r.content)).convert('RGBA')
    except Exception:
        return None


def render_card_from_design(design: dict, photo_bytes: Optional[bytes] = None) -> bytes:
    """Gera PNG a partir do JSON salvo pelo editor."""
    w, h = WIDTH, HEIGHT
    bg = design.get('background', {})
    if bg.get('type') == 'color' and bg.get('color'):
        hex_c = bg['color'].lstrip('#')
        if len(hex_c) == 6:
            rgb = tuple(int(hex_c[i:i + 2], 16) for i in (0, 2, 4))
            img = Image.new('RGB', (w, h), rgb)
        else:
            img = _gradient_bg(w, h, (26, 32, 48), (60, 50, 30))
    elif bg.get('type') == 'url' and bg.get('url'):
        try:
            r = requests.get(bg['url'], timeout=20)
            img = Image.open(io.BytesIO(r.content)).convert('RGB').resize((w, h))
        except Exception:
            colors = BG_COLORS.get('gold_marble', ((26, 32, 48), (60, 50, 30)))
            img = _gradient_bg(w, h, colors[0], colors[1])
    else:
        preset = bg.get('value', 'gold_marble')
        colors = BG_COLORS.get(preset, ((26, 32, 48), (60, 50, 30)))
        img = _gradient_bg(w, h, colors[0], colors[1])

    draw = ImageDraw.Draw(img)
    template = design.get('template', 'icon_gold')
    frame = FRAME_COLORS.get(template, (212, 175, 55))
    pts = [
        (int(w * 0.08), int(h * 0.02)),
        (int(w * 0.92), int(h * 0.02)),
        (int(w * 0.98), int(h * 0.35)),
        (int(w * 0.98), int(h * 0.88)),
        (int(w * 0.5), int(h * 0.98)),
        (int(w * 0.02), int(h * 0.88)),
        (int(w * 0.02), int(h * 0.35)),
    ]
    draw.polygon(pts, outline=frame, width=4)

    player_cfg = design.get('player', {})
    photo = None
    if photo_bytes:
        try:
            photo = Image.open(io.BytesIO(photo_bytes)).convert('RGBA')
        except Exception:
            pass
    elif player_cfg.get('url'):
        photo = _load_photo(player_cfg['url'])

    if photo:
        scale = float(player_cfg.get('scale', 100)) / 100
        zoom = float(player_cfg.get('zoom', 100)) / 100
        combined = scale * zoom
        pw, ph = int(w * 0.78 * combined), int(h * 0.52 * combined)
        photo = photo.resize((pw, ph), Image.Resampling.LANCZOS)
        if player_cfg.get('grayscale'):
            photo = ImageEnhance.Color(photo).enhance(0)
        br = float(player_cfg.get('brightness', 100)) / 100
        photo = ImageEnhance.Brightness(photo).enhance(br)
        ct = float(player_cfg.get('contrast', 100)) / 100
        photo = ImageEnhance.Contrast(photo).enhance(ct)
        px = int(w * 0.11 + player_cfg.get('x', 0) * 0.5)
        py = int(h * 0.18 + player_cfg.get('y', 0) * 0.5)
        img_rgba = img.convert('RGBA')
        img_rgba.paste(photo, (px, py), photo)
        img = img_rgba.convert('RGB')

    stats = CartaFutStats.from_dict(design.get('stats', {}))
    gold = frame
    white = (255, 255, 255)

    draw.text((42, 36), str(design.get('overall', stats.overall)), fill=gold, font=_load_font(52, True))
    draw.text((42, 92), str(design.get('position', stats.posicao)), fill=white, font=_load_font(22, True))

    nome = str(design.get('name', ''))[:22].upper()
    draw.text((w // 2, 448), nome, fill=gold, font=_load_font(24, True), anchor='mm')

    nat = design.get('nation', '')
    if nat and design.get('show_nation', True):
        draw.text((w // 2, 472), nat, fill=(180, 190, 210), font=_load_font(14), anchor='mm')

    labels = [('PAC', stats.pac), ('SHO', stats.sho), ('PAS', stats.pas),
              ('DRI', stats.dri), ('DEF', stats.def_), ('PHY', stats.phy)]
    y_stats = 510
    col_w = (w - 60) // 6
    for i, (lab, val) in enumerate(labels):
        x = 30 + col_w * i + col_w // 2
        draw.text((x, y_stats), lab, fill=gold, font=_load_font(13), anchor='mm')
        draw.text((x, y_stats + 22), str(val), fill=white, font=_load_font(20, True), anchor='mm')

    buf = io.BytesIO()
    img.save(buf, format='PNG', optimize=True)
    return buf.getvalue()
