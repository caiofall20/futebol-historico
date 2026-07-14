"""Orquestra geração de conteúdo a partir de fontes públicas."""
import os
import re
from dataclasses import dataclass
from datetime import date
from typing import Optional

from .card_stats import CartaFutStats, compute_carta_stats
from .fut_card_generator import generate_fut_card
from .html_builder import build_biografia, build_carreira
from .images import download_commons_file
from .llm_enhancer import enhance_texts_with_llm
from .wikidata_client import search_football_player
from .wikipedia_client import resolve_wikipedia_content


@dataclass
class PlayerGeneratedData:
    nome: str
    nacionalidade: str
    inicio_carreira: date
    fim_carreira: date
    altura: str
    perna: str
    outras_posicoes: str
    titulos_champions: int
    bola_de_ouro: int
    mundial_clubes: int
    biografia: str
    carreira: str
    wikidata_id: str
    wikipedia_titulo: str
    fontes: str
    imagem_bytes: Optional[bytes] = None
    imagem_ext: str = 'jpg'
    carta_bytes: Optional[bytes] = None
    carta_stats: Optional[dict] = None


class PlayerNotFoundError(Exception):
    pass


def generate_player_content(nome_busca: str) -> PlayerGeneratedData:
    player = search_football_player(nome_busca)
    if not player:
        raise PlayerNotFoundError(
            f'Não encontramos um jogador de futebol com o nome "{nome_busca}" no Wikidata. '
            'Use o nome completo (ex.: "Hidetoshi Nakata" em vez de só "Nakata").'
        )

    wiki_html, wiki_title, wiki_url = resolve_wikipedia_content(
        nome_busca, player.wikipedia_titulo_pt
    )
    if wiki_title and wiki_url and wiki_url not in player.fontes:
        player.fontes.append(wiki_url)

    biografia = build_biografia(player, wiki_html)
    carreira = build_carreira(player)

    wiki_plain = ''
    if wiki_html:
        wiki_plain = re.sub(r'<[^>]+>', ' ', wiki_html)

    biografia, carreira, llm_used = enhance_texts_with_llm(
        player,
        str(biografia),
        str(carreira),
        wikipedia_resumo=wiki_plain,
    )
    if llm_used:
        player.fontes.append(
            f'Biografia editada por IA ({os.getenv("OPENAI_MODEL", "gpt-4o-mini")}) '
            'com base exclusiva nos fatos acima.'
        )

    inicio = player.inicio_carreira or date(1990, 1, 1)
    fim = player.fim_carreira or date(2010, 1, 1)
    posicoes = ', '.join(player.posicoes) if player.posicoes else 'Meia'

    imagem_bytes = None
    imagem_ext = 'jpg'
    if player.imagem_commons:
        try:
            imagem_bytes, imagem_ext = download_commons_file(player.imagem_commons)
        except Exception:
            imagem_bytes = None

    stats = compute_carta_stats(
        outras_posicoes=posicoes,
        inicio_carreira=inicio,
        fim_carreira=fim,
        perna=player.perna,
    )

    carta_bytes = generate_fut_card(
        nome=player.nome,
        photo_bytes=imagem_bytes,
        nacionalidade=player.nacionalidade,
        stats=stats,
    )

    fontes_texto = '\n'.join(player.fontes)

    return PlayerGeneratedData(
        nome=player.nome,
        nacionalidade=player.nacionalidade,
        inicio_carreira=inicio,
        fim_carreira=fim,
        altura=player.altura,
        perna=player.perna,
        outras_posicoes=posicoes,
        titulos_champions=0,
        bola_de_ouro=0,
        mundial_clubes=0,
        biografia=str(biografia),
        carreira=str(carreira),
        wikidata_id=player.entity_id,
        wikipedia_titulo=wiki_title or player.wikipedia_titulo_pt,
        fontes=fontes_texto,
        imagem_bytes=imagem_bytes,
        imagem_ext=imagem_ext,
        carta_bytes=carta_bytes,
        carta_stats=stats.to_dict(),
    )
