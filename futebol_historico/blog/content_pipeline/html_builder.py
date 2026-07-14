"""Monta HTML de biografia e carreira no padrão do portal."""
from django.utils.html import format_html

from .wikidata_client import TeamStint, WikidataPlayer


def build_biografia(player: WikidataPlayer, wiki_html: str) -> str:
    parts = []
    if wiki_html:
        parts.append(wiki_html)
    else:
        parts.append(
            format_html(
                '<p><strong>{}</strong> é um jogador de futebol {}. '
                'Revise e complete esta biografia com base nas fontes indicadas.</p>',
                player.nome,
                player.nacionalidade,
            )
        )

    if player.times:
        parts.append('<h3>Trajetória nos clubes</h3>')
        for stint in player.times[:8]:
            periodo = _format_period(stint)
            parts.append(format_html('<p><strong>{}</strong>{}</p>', stint.nome, periodo))

    parts.append(
        format_html(
            '<p><em>Fontes: Wikidata ({}) e Wikipedia. Revise antes de publicar.</em></p>',
            player.entity_id,
        )
    )
    return '\n'.join(str(p) for p in parts)


def build_carreira(player: WikidataPlayer) -> str:
    items = []
    for stint in player.times:
        periodo = _format_period(stint, list_item=True)
        items.append(format_html('<li><strong>{}</strong>{}</li>', stint.nome, periodo))

    if not items:
        items.append(
            format_html(
                '<li><strong>Carreira</strong> — Complete o histórico de clubes após verificar as fontes.</li>'
            )
        )

    stats = format_html(
        '''
        <h4>Dados (verifique e ajuste)</h4>
        <ul>
            <li><strong>Nacionalidade:</strong> {}</li>
            <li><strong>Altura:</strong> {}</li>
            <li><strong>Pé dominante:</strong> {}</li>
            <li><strong>Posições:</strong> {}</li>
        </ul>
        ''',
        player.nacionalidade or '—',
        player.altura or '—',
        player.perna or '—',
        ', '.join(player.posicoes) if player.posicoes else '—',
    )

    return format_html(
        '<ul>{}</ul>{}',
        format_html(''.join(str(i) for i in items)),
        stats,
    )


def _format_period(stint: TeamStint, list_item: bool = False) -> str:
    if stint.inicio and stint.fim:
        suffix = f' ({stint.inicio.year}-{stint.fim.year})'
    elif stint.inicio:
        suffix = f' (desde {stint.inicio.year})'
    else:
        suffix = ''
    return suffix
