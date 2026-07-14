# blog/templatetags/breadcrumbs.py
"""
Template tags para breadcrumbs
"""
from django import template

register = template.Library()


@register.inclusion_tag('blog/breadcrumbs.html', takes_context=True)
def breadcrumbs(context, *args):
    """
    Gera breadcrumbs dinamicamente baseado no contexto
    """
    request = context.get('request')
    breadcrumbs_list = []
    
    # Sempre adicionar "Início"
    breadcrumbs_list.append({
        'name': 'Início',
        'url': '/',
        'is_active': False
    })
    
    # Detectar página atual e adicionar breadcrumbs apropriados
    url_name = request.resolver_match.url_name if request and hasattr(request, 'resolver_match') else None
    
    if url_name == 'jogadores_page':
        breadcrumbs_list.append({
            'name': 'Jogadores',
            'url': '/jogadores/',
            'is_active': True
        })
    elif url_name == 'jogador_detail':
        breadcrumbs_list.append({
            'name': 'Jogadores',
            'url': '/jogadores/',
            'is_active': False
        })
        if 'jogador' in context:
            breadcrumbs_list.append({
                'name': context['jogador'].nome,
                'url': request.path,
                'is_active': True
            })
    elif url_name == 'selecoes':
        breadcrumbs_list.append({
            'name': 'Seleções',
            'url': '/selecoes/',
            'is_active': True
        })
    elif url_name == 'selecao_detail':
        breadcrumbs_list.append({
            'name': 'Seleções',
            'url': '/selecoes/',
            'is_active': False
        })
        if 'selecao' in context:
            breadcrumbs_list.append({
                'name': context['selecao'].nome,
                'url': request.path,
                'is_active': True
            })
    elif url_name == 'times':
        breadcrumbs_list.append({
            'name': 'Times',
            'url': '/times/',
            'is_active': True
        })
    elif url_name == 'time_detail':
        breadcrumbs_list.append({
            'name': 'Times',
            'url': '/times/',
            'is_active': False
        })
        if 'time' in context:
            breadcrumbs_list.append({
                'name': context['time'].nome,
                'url': request.path,
                'is_active': True
            })
    elif url_name == 'copas':
        breadcrumbs_list.append({
            'name': 'Copas',
            'url': '/copas/',
            'is_active': True
        })
    elif url_name == 'copa_detail':
        breadcrumbs_list.append({
            'name': 'Copas',
            'url': '/copas/',
            'is_active': False
        })
        if 'copa' in context:
            breadcrumbs_list.append({
                'name': context['copa'].nome,
                'url': request.path,
                'is_active': True
            })
    elif url_name == 'estadio_list':
        breadcrumbs_list.append({
            'name': 'Estádios',
            'url': '/estadios/',
            'is_active': True
        })
    elif url_name == 'estadio_detail':
        breadcrumbs_list.append({
            'name': 'Estádios',
            'url': '/estadios/',
            'is_active': False
        })
        if 'estadio' in context:
            breadcrumbs_list.append({
                'name': context['estadio'].nome,
                'url': request.path,
                'is_active': True
            })
    
    return {
        'breadcrumbs': breadcrumbs_list
    }





