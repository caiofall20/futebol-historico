"""Carta estilo FUT / ícone (PNG) para listagem do portal."""
import io
import math
from datetime import date

from PIL import Image, ImageDraw, ImageFont

from .card_stats import CartaFutStats


def _load_font(size: int, bold: bool = False):
    paths = [
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        '/usr/share/fonts/TTF/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/TTF/DejaVuSans.ttf',
    ]
    for p in paths:
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _draw_shield_background(draw: ImageDraw.ImageDraw, w: int, h: int):
    """Fundo escudo dourado / azul escuro."""
    draw.rectangle([0, 0, w, h], fill=(8, 12, 28))
    # Gradiente superior dourado
    for i in range(120):
        t = i / 120
        c = (
            int(12 + 80 * t),
            int(18 + 60 * t),
            int(40 + 20 * t),
        )
        draw.line([(30, 20 + i), (w - 30, 20 + i)], fill=c, width=1)
    # Moldura dourada
    pts = [
        (w * 0.08, h * 0.02),
        (w * 0.92, h * 0.02),
        (w * 0.98, h * 0.35),
        (w * 0.98, h * 0.88),
        (w * 0.5, h * 0.98),
        (w * 0.02, h * 0.88),
        (w * 0.02, h * 0.35),
    ]
    draw.polygon(pts, outline=(212, 175, 55), width=4)
    draw.polygon(pts, fill=(18, 28, 52))


def generate_fut_card(
    nome: str,
    photo_bytes: bytes | None,
    nacionalidade: str,
    stats: CartaFutStats,
    width: int = 450,
    height: int = 630,
) -> bytes:
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    _draw_shield_background(draw, width, height)

    font_ovr = _load_font(52, bold=True)
    font_pos = _load_font(22, bold=True)
    font_name = _load_font(26, bold=True)
    font_stat_l = _load_font(13)
    font_stat_v = _load_font(20, bold=True)

    gold = (212, 175, 55)
    white = (255, 255, 255)
    dim = (180, 190, 210)

    # Overall + posição (canto superior esquerdo)
    draw.text((42, 36), str(stats.overall), fill=gold, font=font_ovr)
    draw.text((42, 92), stats.posicao, fill=white, font=font_pos)

    # Área da foto
    photo_top, photo_bottom = 130, 420
    photo_box = (55, photo_top, width - 55, photo_bottom)
    if photo_bytes:
        try:
            photo = Image.open(io.BytesIO(photo_bytes)).convert('RGBA')
            pw = photo_box[2] - photo_box[0]
            ph = photo_box[3] - photo_box[1]
            ratio = min(pw / photo.width, ph / photo.height)
            nw, nh = int(photo.width * ratio), int(photo.height * ratio)
            photo = photo.resize((nw, nh), Image.Resampling.LANCZOS)
            px = photo_box[0] + (pw - nw) // 2
            py = photo_box[1] + (ph - nh) // 2
            img.paste(photo, (px, py), photo)
        except Exception:
            pass

    # Nome
    nome_show = nome.upper() if len(nome) <= 22 else nome[:19].upper() + '...'
    draw.text((width // 2, 448), nome_show, fill=gold, font=font_name, anchor='mm')

    # Nacionalidade
    if nacionalidade and nacionalidade != 'Desconhecida':
        draw.text((width // 2, 472), nacionalidade, fill=dim, font=font_stat_l, anchor='mm')

    # Stats FUT
    labels = [
        ('PAC', stats.pac),
        ('SHO', stats.sho),
        ('PAS', stats.pas),
        ('DRI', stats.dri),
        ('DEF', stats.def_),
        ('PHY', stats.phy),
    ]
    y_stats = 510
    col_w = (width - 60) // 6
    for i, (lab, val) in enumerate(labels):
        x = 30 + col_w * i + col_w // 2
        draw.text((x, y_stats), lab, fill=gold, font=font_stat_l, anchor='mm')
        draw.text((x, y_stats + 22), str(val), fill=white, font=font_stat_v, anchor='mm')

    # Rodapé marca
    draw.text((width // 2, height - 28), 'FUTEBOL HISTÓRICO', fill=(100, 110, 130), font=font_stat_l, anchor='mm')

    rgb = Image.new('RGB', img.size, (8, 12, 28))
    rgb.paste(img, mask=img.split()[3])
    buf = io.BytesIO()
    rgb.save(buf, format='PNG', optimize=True)
    return buf.getvalue()
