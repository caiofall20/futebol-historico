# blog/api_views.py
"""
API Views para endpoints JSON (AJAX)
Sem dependência de Django REST Framework
"""
import logging
from django.http import JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q, Case, When, IntegerField, F
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import Jogador
from .templatetags.flag_tags import get_flag_code

logger = logging.getLogger(__name__)


def _carta_url_with_cache_bust(jogador: Jogador) -> str | None:
    if not jogador.carta:
        return None
    fname = jogador.carta.name.split('/')[-1]
    return f'{jogador.carta.url}?v={jogador.pk}-{fname}'


def serialize_jogador(jogador):
    """Serializa um jogador para JSON
    
    Nota: Para a página de listagem (jogadores.html), deve usar carta_url primeiro.
    Para a página de detalhes (jogador_detail.html), deve usar imagem_url primeiro.
    """
    return {
        'id': jogador.id,
        'nome': jogador.nome,
        'nacionalidade': jogador.nacionalidade,
        'flag_code': get_flag_code(jogador.nacionalidade),
        'imagem_url': jogador.imagem.url if jogador.imagem else None,  # Para página de detalhes
        'carta_url': _carta_url_with_cache_bust(jogador),  # Para página de listagem
        'total_trofeus': getattr(jogador, 'total_trofeus', 0),
        'rating': getattr(jogador, 'rating', 1),
        'inicio_carreira': jogador.inicio_carreira.strftime('%Y') if jogador.inicio_carreira else None,
        'fim_carreira': jogador.fim_carreira.strftime('%Y') if jogador.fim_carreira else None,
        'perna': jogador.perna or '',
        'altura': jogador.altura or '',
        'biografia_preview': jogador.biografia[:100] + '...' if jogador.biografia and len(jogador.biografia) > 100 else (jogador.biografia or ''),
    }


@require_http_methods(["GET"])
def jogadores_api(request):
    """
    API endpoint para buscar jogadores com filtros.
    Retorna JSON para uso com AJAX.
    """
    try:
        # Obter parâmetros de filtro
        query = request.GET.get('q', '').strip()
        nacionalidade = request.GET.get('nacionalidade', '').strip()
        posicao = request.GET.get('posicao', '').strip()
        periodo = request.GET.get('periodo', '').strip()
        
        try:
            page = int(request.GET.get('page', 1))
        except (ValueError, TypeError):
            page = 1

        # Query base otimizada
        jogadores = Jogador.objects.only(
            'id', 'nome', 'nacionalidade', 'imagem', 'carta',
            'inicio_carreira', 'fim_carreira', 'perna',
            'titulos_champions', 'mundial_clubes', 'bola_de_ouro',
            'biografia', 'altura'
        )

        # Aplicar filtros
        if query:
            jogadores = jogadores.filter(
                Q(nome__icontains=query) | 
                Q(nacionalidade__icontains=query)
            )

        if nacionalidade:
            jogadores = jogadores.filter(nacionalidade__icontains=nacionalidade)

        if posicao:
            jogadores = jogadores.filter(posicao=posicao)

        if periodo:
            jogadores = jogadores.filter(periodo__contains=periodo)

        # Calcular campos no banco
        jogadores = jogadores.annotate(
            total_trofeus=F('titulos_champions') + F('mundial_clubes'),
            total_pontos=F('titulos_champions') + F('mundial_clubes') + F('bola_de_ouro'),
        ).annotate(
            rating=Case(
                When(total_pontos__gte=10, then=5),
                When(total_pontos__gte=6, then=4),
                When(total_pontos__gte=3, then=3),
                When(total_pontos__gte=1, then=2),
                default=1,
                output_field=IntegerField()
            )
        ).order_by('-total_trofeus', 'nome')

        # Paginação
        paginator = Paginator(jogadores, 12)
        try:
            jogadores_paginados = paginator.page(page)
        except PageNotAnInteger:
            jogadores_paginados = paginator.page(1)
        except EmptyPage:
            jogadores_paginados = paginator.page(paginator.num_pages)

        # Serializar resultados
        results = [serialize_jogador(j) for j in jogadores_paginados]

        return JsonResponse({
            'success': True,
            'results': results,
            'pagination': {
                'current_page': page,
                'total_pages': paginator.num_pages,
                'total_count': paginator.count,
                'has_next': jogadores_paginados.has_next(),
                'has_previous': jogadores_paginados.has_previous(),
            },
            'filters': {
                'query': query,
                'nacionalidade': nacionalidade,
                'posicao': posicao,
                'periodo': periodo,
            }
        })

    except Exception as e:
        logger.exception(f"Erro na API jogadores: {e}")
        return JsonResponse({
            'success': False,
            'error': 'Erro ao buscar jogadores',
            'message': str(e)
        }, status=500)


