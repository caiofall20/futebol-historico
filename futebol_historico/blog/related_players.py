"""Sugestão de jogadores relacionados para a ficha do portal."""
from __future__ import annotations

from dataclasses import dataclass

from django.db.models import F, Q, QuerySet

from .models import Jogador


@dataclass(frozen=True)
class JogadorRelacionado:
    jogador: Jogador
    motivo: str


def _primary_position(jogador: Jogador) -> str:
    if jogador.outras_posicoes:
        return jogador.outras_posicoes.split(',')[0].strip()
    return (jogador.posicao or '').strip()


def _base_queryset(exclude_pk: int) -> QuerySet[Jogador]:
    return (
        Jogador.objects.exclude(pk=exclude_pk)
        .annotate(total_trofeus=F('titulos_champions') + F('mundial_clubes'))
    )


def _pick(
    related: list[JogadorRelacionado],
    seen: set[int],
    qs: QuerySet[Jogador],
    motivo: str,
    limit: int,
) -> None:
    if len(related) >= limit:
        return
    for jogador in qs:
        if jogador.pk in seen:
            continue
        seen.add(jogador.pk)
        related.append(JogadorRelacionado(jogador=jogador, motivo=motivo))
        if len(related) >= limit:
            break


def get_related_players(jogador: Jogador, limit: int = 6) -> list[JogadorRelacionado]:
    """
    Prioridade: mesma nacionalidade → mesma posição → mesma época → destaques gerais.
    """
    limit = max(1, min(limit, 12))
    related: list[JogadorRelacionado] = []
    seen: set[int] = {jogador.pk}
    base = _base_queryset(jogador.pk)

    nacionalidade = (jogador.nacionalidade or '').strip()
    if nacionalidade and nacionalidade.lower() != 'desconhecida':
        _pick(
            related,
            seen,
            base.filter(nacionalidade__iexact=nacionalidade).order_by('-total_trofeus', 'nome'),
            'Mesma nacionalidade',
            limit,
        )

    posicao = _primary_position(jogador)
    if len(related) < limit and posicao:
        _pick(
            related,
            seen,
            base.filter(outras_posicoes__icontains=posicao).order_by('-total_trofeus', 'nome'),
            f'Mesma posição ({posicao})',
            limit,
        )

    if (
        len(related) < limit
        and jogador.inicio_carreira
        and jogador.fim_carreira
        and jogador.inicio_carreira.year > 1901
    ):
        _pick(
            related,
            seen,
            base.filter(
                inicio_carreira__lte=jogador.fim_carreira,
                fim_carreira__gte=jogador.inicio_carreira,
            ).order_by('-total_trofeus', 'nome'),
            'Mesma época',
            limit,
        )

    if len(related) < limit:
        _pick(
            related,
            seen,
            base.filter(Q(carta__isnull=False) | Q(imagem__isnull=False))
            .exclude(carta='')
            .order_by('-total_trofeus', '-bola_de_ouro', 'nome'),
            'Outros craques',
            limit,
        )

    if len(related) < limit:
        _pick(
            related,
            seen,
            base.order_by('-total_trofeus', 'nome'),
            'Você também pode gostar',
            limit,
        )

    return related
