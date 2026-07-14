"""Melhora biografia e carreira via LLM (opcional), usando apenas fatos fornecidos."""
import json
import logging
import os
import re

import requests

from .wikidata_client import WikidataPlayer

logger = logging.getLogger(__name__)


def is_llm_enabled() -> bool:
    if os.getenv('CONTENT_LLM_ENABLED', 'true').lower() in ('0', 'false', 'no'):
        return False
    return bool(os.getenv('OPENAI_API_KEY', '').strip())


def _facts_payload(player: WikidataPlayer, extra: dict) -> dict:
    times = [
        {
            'clube': t.nome,
            'inicio': t.inicio.isoformat() if t.inicio else None,
            'fim': t.fim.isoformat() if t.fim else None,
        }
        for t in player.times
    ]
    return {
        'nome': player.nome,
        'nacionalidade': player.nacionalidade,
        'altura': player.altura,
        'pe_dominante': player.perna,
        'posicoes': player.posicoes,
        'clubes': times,
        'wikidata_id': player.entity_id,
        **extra,
    }


def enhance_texts_with_llm(
    player: WikidataPlayer,
    biografia_base: str,
    carreira_base: str,
    wikipedia_resumo: str = '',
) -> tuple[str, str, bool]:
    """
    Retorna (biografia_html, carreira_html, usou_llm).
    Se LLM desabilitado ou falhar, devolve textos originais.
    """
    if not is_llm_enabled():
        return biografia_base, carreira_base, False

    api_key = os.getenv('OPENAI_API_KEY', '').strip()
    base_url = os.getenv('OPENAI_API_BASE', 'https://api.openai.com/v1').rstrip('/')
    model = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')

    facts = _facts_payload(player, {
        'periodo_carreira': {
            'inicio': player.inicio_carreira.isoformat() if player.inicio_carreira else None,
            'fim': player.fim_carreira.isoformat() if player.fim_carreira else None,
        },
        'resumo_wikipedia': wikipedia_resumo[:2000] if wikipedia_resumo else '',
    })

    system = (
        'Você é um redator esportivo do portal "Futebol Histórico" em português do Brasil. '
        'Escreva APENAS com base nos fatos JSON fornecidos. Não invente títulos, números, datas ou clubes. '
        'Se um dado não estiver nos fatos, não mencione. '
        'Responda somente com JSON válido: {"biografia": "<html>", "carreira": "<html>"}. '
        'Use HTML: <p>, <h3>, <ul>, <li>, <strong>. Sem markdown.'
    )
    user = (
        f'Fatos verificados:\n{json.dumps(facts, ensure_ascii=False, indent=2)}\n\n'
        f'Rascunho biografia:\n{biografia_base[:1500]}\n\n'
        f'Rascunho carreira:\n{carreira_base[:1500]}\n\n'
        'Reescreva biografia (2-4 parágrafos + seções h3 por fases/clubes principais) '
        'e carreira (lista de clubes com anos e seção de dados). Tom jornalístico, elegante.'
    )

    try:
        r = requests.post(
            f'{base_url}/chat/completions',
            headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json',
            },
            json={
                'model': model,
                'messages': [
                    {'role': 'system', 'content': system},
                    {'role': 'user', 'content': user},
                ],
                'temperature': 0.4,
                'response_format': {'type': 'json_object'},
            },
            timeout=90,
        )
        r.raise_for_status()
        content = r.json()['choices'][0]['message']['content']
        parsed = json.loads(content)
        bio = parsed.get('biografia', biografia_base)
        car = parsed.get('carreira', carreira_base)
        bio = _sanitize_html_fragment(bio)
        car = _sanitize_html_fragment(car)
        return bio, car, True
    except Exception as e:
        logger.warning('LLM enhancer falhou: %s', e)
        return biografia_base, carreira_base, False


def _sanitize_html_fragment(html: str) -> str:
    """Remove tags perigosas; mantém formatação editorial."""
    html = html.strip()
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.I | re.S)
    html = re.sub(r'<iframe[^>]*>.*?</iframe>', '', html, flags=re.I | re.S)
    html = re.sub(r'on\w+="[^"]*"', '', html, flags=re.I)
    return html
