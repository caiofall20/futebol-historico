"""Persistência de rascunhos e publicação no modelo Jogador."""
import re
import unicodedata

from django.core.files.base import ContentFile
from django.utils import timezone

from blog.models import Jogador, JogadorRascunho

from .card_design import default_card_design
from .card_render_server import render_card_from_design
from .generator import PlayerGeneratedData, generate_player_content


def _slug_filename(nome: str, ext: str, *, versioned: bool = False) -> str:
    s = unicodedata.normalize('NFKD', nome).encode('ascii', 'ignore').decode('ascii')
    s = re.sub(r'[^a-zA-Z0-9]+', '_', s).strip('_').lower()
    base = s or 'jogador'
    if versioned:
        ts = timezone.now().strftime('%Y%m%d%H%M%S')
        return f'{base}_{ts}.{ext}'
    return f'{base}.{ext}'


def _copy_jogador_media_to_rascunho(jogador: Jogador, rascunho: JogadorRascunho) -> None:
    """Copia imagem/carta do Jogador publicado para o rascunho de edição."""
    if jogador.imagem and not rascunho.imagem:
        with jogador.imagem.open('rb') as f:
            fname = jogador.imagem.name.split('/')[-1]
            rascunho.imagem.save(fname, ContentFile(f.read()), save=False)
    if jogador.carta and not rascunho.carta:
        with jogador.carta.open('rb') as f:
            fname = jogador.carta.name.split('/')[-1]
            rascunho.carta.save(fname, ContentFile(f.read()), save=False)


def ensure_rascunho_from_jogador(jogador: Jogador, user) -> JogadorRascunho:
    """
    Garante um rascunho editável para um Jogador já no portal
    (ex.: cadastrado via admin ou importação antiga).
    """
    rascunho = (
        JogadorRascunho.objects.filter(jogador_publicado=jogador)
        .order_by('-atualizado_em')
        .first()
    )
    if rascunho:
        return rascunho

    rascunho = JogadorRascunho(
        criado_por=user,
        nome=jogador.nome,
        nacionalidade=jogador.nacionalidade,
        inicio_carreira=jogador.inicio_carreira,
        fim_carreira=jogador.fim_carreira,
        biografia=jogador.biografia,
        carreira=jogador.carreira,
        altura=jogador.altura or '',
        perna=jogador.perna or '',
        outras_posicoes=jogador.outras_posicoes or '',
        titulos_champions=jogador.titulos_champions,
        bola_de_ouro=jogador.bola_de_ouro,
        mundial_clubes=jogador.mundial_clubes,
        status='publicado',
        jogador_publicado=jogador,
    )
    _copy_jogador_media_to_rascunho(jogador, rascunho)
    from .card_stats import compute_carta_stats

    stats = compute_carta_stats(
        outras_posicoes=rascunho.outras_posicoes or '',
        titulos_champions=rascunho.titulos_champions,
        bola_de_ouro=rascunho.bola_de_ouro,
        mundial_clubes=rascunho.mundial_clubes,
        inicio_carreira=rascunho.inicio_carreira,
        fim_carreira=rascunho.fim_carreira,
        perna=rascunho.perna or '',
    )
    rascunho.carta_stats = stats.to_dict()
    rascunho.carta_design = default_card_design(rascunho)
    rascunho.save()
    return rascunho


def _sync_carta_to_jogador_publicado(rascunho: JogadorRascunho, png_bytes: bytes, fname: str) -> Jogador | None:
    """Copia a carta do rascunho para o Jogador já publicado (listagem do portal)."""
    jogador = rascunho.jogador_publicado
    if not jogador:
        return None
    jogador.carta.save(fname, ContentFile(png_bytes), save=True)
    return jogador


def apply_generated_to_rascunho(rascunho: JogadorRascunho, data: PlayerGeneratedData) -> None:
    rascunho.nome = data.nome
    rascunho.nacionalidade = data.nacionalidade
    rascunho.inicio_carreira = data.inicio_carreira
    rascunho.fim_carreira = data.fim_carreira
    rascunho.altura = data.altura or ''
    rascunho.perna = data.perna or ''
    rascunho.outras_posicoes = data.outras_posicoes
    rascunho.titulos_champions = data.titulos_champions
    rascunho.bola_de_ouro = data.bola_de_ouro
    rascunho.mundial_clubes = data.mundial_clubes
    rascunho.biografia = data.biografia
    rascunho.carreira = data.carreira
    rascunho.wikidata_id = data.wikidata_id
    rascunho.wikipedia_titulo = data.wikipedia_titulo
    rascunho.fontes = data.fontes
    if data.carta_stats:
        rascunho.carta_stats = data.carta_stats

    if data.imagem_bytes:
        fname = _slug_filename(data.nome, data.imagem_ext)
        rascunho.imagem.save(fname, ContentFile(data.imagem_bytes), save=False)

    if data.carta_bytes:
        fname = _slug_filename(data.nome, 'png')
        rascunho.carta.save(fname, ContentFile(data.carta_bytes), save=False)

    rascunho.carta_design = default_card_design(rascunho)

    rascunho.status = 'rascunho'
    rascunho.mensagem_erro = ''
    rascunho.save()


def run_generation_for_rascunho(rascunho: JogadorRascunho, nome_busca: str) -> None:
    rascunho.status = 'gerando'
    rascunho.mensagem_erro = ''
    rascunho.save(update_fields=['status', 'mensagem_erro', 'atualizado_em'])

    try:
        data = generate_player_content(nome_busca)
        apply_generated_to_rascunho(rascunho, data)
    except Exception as e:
        rascunho.status = 'erro'
        rascunho.mensagem_erro = str(e)
        rascunho.save(update_fields=['status', 'mensagem_erro', 'atualizado_em'])
        raise


def _copy_rascunho_fields_to_jogador(rascunho: JogadorRascunho, jogador: Jogador) -> None:
    jogador.nome = rascunho.nome
    jogador.nacionalidade = rascunho.nacionalidade
    jogador.inicio_carreira = rascunho.inicio_carreira
    jogador.fim_carreira = rascunho.fim_carreira
    jogador.altura = rascunho.altura
    jogador.perna = rascunho.perna
    jogador.outras_posicoes = rascunho.outras_posicoes
    jogador.titulos_champions = rascunho.titulos_champions
    jogador.bola_de_ouro = rascunho.bola_de_ouro
    jogador.mundial_clubes = rascunho.mundial_clubes
    jogador.biografia = rascunho.biografia
    jogador.carreira = rascunho.carreira


def sync_published_jogador_from_rascunho(rascunho: JogadorRascunho) -> None:
    """Atualiza o Jogador publicado quando o rascunho é editado após publicação."""
    jogador = rascunho.jogador_publicado
    if not jogador:
        return
    _copy_rascunho_fields_to_jogador(rascunho, jogador)
    jogador.save()
    if rascunho.imagem:
        with rascunho.imagem.open('rb') as f:
            fname = rascunho.imagem.name.split('/')[-1]
            jogador.imagem.save(fname, ContentFile(f.read()), save=True)


def publish_rascunho(rascunho: JogadorRascunho) -> Jogador:
    """Cria ou atualiza Jogador publicado a partir do rascunho."""
    existente = Jogador.objects.filter(nome__iexact=rascunho.nome).first()
    if existente:
        jogador = existente
    else:
        jogador = Jogador(nome=rascunho.nome)

    _copy_rascunho_fields_to_jogador(rascunho, jogador)
    jogador.save()

    if rascunho.imagem:
        with rascunho.imagem.open('rb') as f:
            fname = rascunho.imagem.name.split('/')[-1]
            jogador.imagem.save(fname, ContentFile(f.read()), save=True)

    if rascunho.carta:
        with rascunho.carta.open('rb') as f:
            fname = rascunho.carta.name.split('/')[-1]
            jogador.carta.save(fname, ContentFile(f.read()), save=True)

    rascunho.status = 'publicado'
    rascunho.jogador_publicado = jogador
    rascunho.save(update_fields=['status', 'jogador_publicado', 'atualizado_em'])

    return jogador


def save_carta_from_stats(rascunho: JogadorRascunho, stats_dict: dict) -> None:
    """Gera PNG da carta FUT e salva no rascunho (modo legado)."""
    from .card_stats import CartaFutStats

    stats = CartaFutStats.from_dict(stats_dict)
    rascunho.carta_stats = stats.to_dict()
    design = default_card_design(rascunho)
    design['stats'] = stats.to_dict()
    design['overall'] = stats.overall
    design['position'] = stats.posicao
    save_carta_from_design(rascunho, design)


def save_carta_from_design(
    rascunho: JogadorRascunho,
    design: dict,
    png_bytes: bytes | None = None,
) -> None:
    """Salva JSON do editor e PNG (upload do cliente ou render servidor)."""
    rascunho.carta_design = design
    stats = design.get('stats', {})
    if stats:
        rascunho.carta_stats = stats

    if png_bytes is None:
        photo_bytes = None
        if rascunho.imagem:
            with rascunho.imagem.open('rb') as f:
                photo_bytes = f.read()
        png_bytes = render_card_from_design(design, photo_bytes=photo_bytes)

    fname = _slug_filename(design.get('name', rascunho.nome), 'png', versioned=True)
    rascunho.carta.save(fname, ContentFile(png_bytes), save=False)
    rascunho.save(update_fields=['carta', 'carta_stats', 'carta_design', 'atualizado_em'])
    _sync_carta_to_jogador_publicado(rascunho, png_bytes, fname)
