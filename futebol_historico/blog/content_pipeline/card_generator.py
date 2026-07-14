"""Gera carta do jogador (PNG) para a listagem."""
import io
from datetime import date

from PIL import Image, ImageDraw, ImageFont


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


def generate_player_card(
    nome: str,
    photo_bytes: bytes | None,
    nacionalidade: str,
    inicio: date | None,
    fim: date | None,
    perna: str,
    titulos_champions: int,
    bola_de_ouro: int,
    mundial_clubes: int,
    width: int = 400,
    height: int = 560,
) -> bytes:
    img = Image.new('RGB', (width, height), color=(12, 18, 32))
    draw = ImageDraw.Draw(img)

    # Moldura dourada
    draw.rectangle([8, 8, width - 9, height - 9], outline=(212, 175, 55), width=3)
    draw.rectangle([16, 16, width - 17, height - 120], fill=(22, 30, 48))

    # Foto
    photo_top = 24
    photo_box = (40, photo_top, width - 40, photo_top + 280)
    if photo_bytes:
        try:
            photo = Image.open(io.BytesIO(photo_bytes)).convert('RGB')
            pw, ph = photo_box[2] - photo_box[0], photo_box[3] - photo_box[1]
            photo = photo.resize((pw, ph), Image.Resampling.LANCZOS)
            img.paste(photo, (photo_box[0], photo_box[1]))
        except Exception:
            draw.ellipse([width // 2 - 60, 80, width // 2 + 60, 200], fill=(40, 50, 70))
    else:
        draw.ellipse([width // 2 - 60, 80, width // 2 + 60, 200], fill=(40, 50, 70))

    font_name = _load_font(22, bold=True)
    font_sm = _load_font(14)
    font_stat = _load_font(16, bold=True)

    # Nome
    nome_curto = nome if len(nome) <= 28 else nome[:25] + '...'
    draw.text((width // 2, height - 108), nome_curto, fill=(255, 255, 255), font=font_name, anchor='mm')

    periodo = '—'
    if inicio and fim:
        periodo = f'{inicio.year}-{fim.year}'
    elif inicio:
        periodo = f'{inicio.year}-'

    draw.text((width // 2, height - 82), nacionalidade or '—', fill=(200, 200, 210), font=font_sm, anchor='mm')
    draw.text((width // 2, height - 62), periodo, fill=(180, 180, 190), font=font_sm, anchor='mm')

    stats_y = height - 42
    stats = [
        ('UCL', titulos_champions),
        ('BO', bola_de_ouro),
        ('Mund.', mundial_clubes),
        ('Pé', perna[:6] if perna else '—'),
    ]
    step = width // (len(stats) + 1)
    for i, (label, val) in enumerate(stats):
        x = step * (i + 1)
        draw.text((x, stats_y - 14), label, fill=(212, 175, 55), font=font_sm, anchor='mm')
        draw.text((x, stats_y + 4), str(val), fill=(255, 255, 255), font=font_stat, anchor='mm')

    buf = io.BytesIO()
    img.save(buf, format='PNG', optimize=True)
    return buf.getvalue()
