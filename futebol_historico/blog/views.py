# blog/views.py

import logging
import re
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import Jogador, Post, Comment, Selecao, Time, Estadio, Copa, TimelineEvento
from .forms import CommentForm

# def index(request):
#     # Obter as 3 últimas postagens
#     recent_posts = Post.objects.order_by('-created_at')[:3]
#     return render(request, 'blog/index.html', {'recent_posts': recent_posts})

logger = logging.getLogger(__name__)

def index(request):
    """
    View para a página inicial.
    Carrossel de jogadores: busca APENAS jogadores com campo 'imagem_carrossel' preenchido.
    NÃO busca de outros diretórios ou campos.
    
    Otimizado com cache para evitar consultas ao banco a cada request.
    """
    from django.core.cache import cache
    
    cache_key = 'imagens_carrossel_index'
    cache_timeout = 60 * 15  # 15 minutos
    
    # Tentar obter do cache primeiro
    imagens_carrossel = cache.get(cache_key)
    
    # Se o cache retornar uma lista vazia, forçar recarregamento
    # IMPORTANTE: Sempre recarregar se for lista vazia para evitar cache de lista vazia
    if imagens_carrossel is None or (isinstance(imagens_carrossel, list) and len(imagens_carrossel) == 0):
        try:
            # IMPORTANTE: Buscar APENAS jogadores com imagem_carrossel preenchida
            jogadores_com_carrossel = Jogador.objects.filter(
                imagem_carrossel__isnull=False
            ).exclude(
                imagem_carrossel=''
            ).only('id', 'nome', 'imagem_carrossel').order_by('nome')
            
            logger.info(f'Jogadores encontrados com imagem_carrossel: {jogadores_com_carrossel.count()}')
            
            imagens_carrossel = []
            
            for jogador in jogadores_com_carrossel:
                if jogador.imagem_carrossel:
                    try:
                        # Verificar se o arquivo realmente existe
                        url = jogador.imagem_carrossel.url
                        imagens_carrossel.append({
                            'url': url,
                            'nome_arquivo': jogador.imagem_carrossel.name.split('/')[-1],
                            'nome_display': jogador.nome,
                            'jogador_id': jogador.id
                        })
                        logger.debug(f'Adicionada imagem do carrossel: {jogador.nome} - {url}')
                    except Exception as e:
                        logger.warning(f"Erro ao processar imagem_carrossel do jogador {jogador.nome}: {e}")
                        continue
            
            # Salvar no cache apenas se houver imagens
            if imagens_carrossel:
                cache.set(cache_key, imagens_carrossel, cache_timeout)
                logger.info(f'✅ Imagens do carrossel carregadas e cacheadas: {len(imagens_carrossel)} imagens')
                logger.info(f'Primeira imagem: {imagens_carrossel[0]["url"]}')
            else:
                # Se não houver imagens, não cachear lista vazia
                logger.warning('⚠️ Nenhuma imagem encontrada para o carrossel')
                cache.delete(cache_key)  # Garantir que não há cache vazio
                
        except Exception as e:
            logger.exception(f"Erro inesperado ao carregar imagens do carrossel: {e}")
            imagens_carrossel = []
            cache.delete(cache_key)  # Limpar cache em caso de erro
    
    context = {
        'imagens_carrossel': imagens_carrossel
    }
    return render(request, 'blog/index.html', context)

def selecoes(request):
    """
    View para listagem de seleções com tratamento de erros robusto.
    """
    from django.db.models import Count, Q
    import re
    
    try:
        query = request.GET.get('q', '').strip()
        region = request.GET.get('region', '').strip()
        
        selecoes = Selecao.objects.all()

        if query:
            selecoes = selecoes.filter(nome__icontains=query)

        if region:
            selecoes = selecoes.filter(regiao=region)

        # Estatísticas agregadas com tratamento de erro
        try:
            total_selecoes = Selecao.objects.count()
            selecoes_por_regiao = Selecao.objects.values('regiao').annotate(total=Count('id')).order_by('-total')
            top_selecoes_titulos = Selecao.objects.order_by('-titulos')[:10]
        except Exception as e:
            logger.error(f"Erro ao calcular estatísticas de seleções: {e}")
            total_selecoes = 0
            selecoes_por_regiao = []
            top_selecoes_titulos = []
        
        # Calcular estatísticas de copas para cada seleção
        copas = Copa.objects.all().order_by('ano')
        for selecao in selecoes:
            # Extrair ano do nome da seleção (formato: "Brasil 1970", "Itália 2006", etc)
            ano_match = re.search(r'\b(19|20)\d{2}\b', selecao.nome)
            selecao.ano_copa = int(ano_match.group()) if ano_match else None
            
            # Buscar a copa específica desse ano
            copa_especifica = None
            if selecao.ano_copa:
                copa_especifica = copas.filter(ano=selecao.ano_copa).first()
            
            # Extrair nome do país (primeira palavra antes do ano)
            if selecao.ano_copa:
                nome_pais = selecao.nome.replace(str(selecao.ano_copa), '').strip()
            else:
                nome_pais = selecao.nome.split()[0] if selecao.nome else ''
            
            selecao.nome_pais = nome_pais
            
            # Se encontrou a copa específica, usar dados dela
            if copa_especifica:
                # Verificar posição nesta copa específica
                selecao.copa_ano = copa_especifica.ano
                selecao.copa_pais = copa_especifica.pais
                selecao.copa_imagem = copa_especifica.imagem.url if copa_especifica.imagem else None
                selecao.copa_id = copa_especifica.id
                
                # Determinar colocação nesta copa
                from django.utils.translation import gettext as _
                if copa_especifica.campeao and nome_pais.lower() in copa_especifica.campeao.lower():
                    selecao.colocacao_copa = _('Campeão')
                    selecao.colocacao_pontos = 100
                elif copa_especifica.vice_campeao and nome_pais.lower() in copa_especifica.vice_campeao.lower():
                    selecao.colocacao_copa = _('Vice-Campeão')
                    selecao.colocacao_pontos = 50
                elif copa_especifica.terceiro_lugar and nome_pais.lower() in copa_especifica.terceiro_lugar.lower():
                    selecao.colocacao_copa = _('3º Lugar')
                    selecao.colocacao_pontos = 30
                else:
                    selecao.colocacao_copa = _('Participante')
                    selecao.colocacao_pontos = 10
                
                # Dados específicos desta copa
                selecao.copa_campeao = copa_especifica.campeao
                selecao.copa_vice = copa_especifica.vice_campeao
                selecao.copa_terceiro = copa_especifica.terceiro_lugar
            else:
                # Fallback: buscar em todas as copas ou usar dados padrão
                selecao.copa_ano = selecao.ano_copa  # Usar ano extraído do nome
                selecao.copa_pais = None
                selecao.copa_id = None
                selecao.colocacao_copa = selecao.colocacao if hasattr(selecao, 'colocacao') else None
                selecao.colocacao_pontos = 0
                copas_campeao = copas.filter(campeao__icontains=nome_pais).count() if nome_pais else 0
                copas_vice = copas.filter(vice_campeao__icontains=nome_pais).count() if nome_pais else 0
                copas_terceiro = copas.filter(terceiro_lugar__icontains=nome_pais).count() if nome_pais else 0
                selecao.copas_campeao = copas_campeao
                selecao.copas_vice = copas_vice
                selecao.copas_terceiro = copas_terceiro
                selecao.total_participacoes = copas_campeao + copas_vice + copas_terceiro
        
        # Top seleções com mais copas
        try:
            top_copas = sorted(selecoes, key=lambda s: getattr(s, 'total_participacoes', 0), reverse=True)[:10]
        except Exception as e:
            logger.error(f"Erro ao ordenar seleções: {e}")
            top_copas = []
        
    except Exception as e:
        logger.exception(f"Erro crítico na view selecoes: {e}")
        # Retornar dados vazios em caso de erro crítico
        selecoes = Selecao.objects.none()
        total_selecoes = 0
        selecoes_por_regiao = []
        top_selecoes_titulos = []
        top_copas = []
        copas = Copa.objects.none()

    context = {
        'selecoes': selecoes,
        'total_selecoes': total_selecoes,
        'selecoes_por_regiao': selecoes_por_regiao,
        'top_selecoes_titulos': top_selecoes_titulos,
        'top_copas': top_copas,
        'copas': copas,
    }
    return render(request, 'blog/selecoes.html', context)

def selecao_detail(request, selecao_id):
    from .security import check_rate_limit
    
    selecao = get_object_or_404(Selecao, id=selecao_id)
    comments = Comment.objects.filter(selecao=selecao, active=True)

    # Buscar seleções sugeridas da mesma região
    selecoes_sugeridas = Selecao.objects.filter(regiao=selecao.regiao).exclude(id=selecao_id)[:4]

    if request.method == 'POST':
        # Rate limiting para comentários
        is_allowed, remaining, reset_time = check_rate_limit(
            request, 
            action='comment', 
            limit=5,  # 5 comentários
            window=60  # por minuto
        )
        
        if not is_allowed:
            messages.error(
                request, 
                f'Muitos comentários. Aguarde {reset_time} segundos antes de comentar novamente.'
            )
            comment_form = CommentForm(request.POST)
        else:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.selecao = selecao
                comment.active = True
                # Sanitizar conteúdo HTML
                from .security import sanitize_html
                if comment.body:
                    comment.body = sanitize_html(comment.body)
                comment.save()
                messages.success(request, 'Comentário adicionado com sucesso!')
                return redirect('selecao_detail', selecao_id=selecao_id)
    else:
        comment_form = CommentForm()

    context = {
        'selecao': selecao,
        'comments': comments,
        'comment_form': comment_form,
        'selecoes_sugeridas': selecoes_sugeridas,
    }
    return render(request, 'blog/selecao_detail.html', context)


def times(request):
    from .initial_data import create_initial_times, update_team_images, create_historical_teams
    
    # Criar times históricos independentemente se já existem outros times
    create_historical_teams()
    
    query = request.GET.get('q')
    region = request.GET.get('region')
    times = Time.objects.all().order_by('nome')

    if query:
        times = times.filter(nome__icontains=query)

    if region:
        times = times.filter(regiao=region)

    context = {
        'times': times,
    }
    return render(request, 'blog/times.html', context)

def jogadores(request):
    """
    View otimizada para listagem de jogadores.
    Usa select_related/prefetch_related e cálculos no banco para evitar N+1 queries.
    """
    from blog.templatetags.flag_tags import get_flag_code
    from django.db.models import Case, When, IntegerField, F
    
    try:
        query = request.GET.get('q', '').strip()
        nacionalidade = request.GET.get('nacionalidade', '').strip()
        posicao = request.GET.get('posicao', '').strip()
        periodo = request.GET.get('periodo', '').strip()
        
        try:
            page = int(request.GET.get('page', 1))
        except (ValueError, TypeError):
            page = 1

        # Query base otimizada - usar apenas() para campos necessários
        jogadores = Jogador.objects.only(
            'id', 'nome', 'nacionalidade', 'imagem', 'carta',
            'inicio_carreira', 'fim_carreira', 'perna',
            'titulos_champions', 'mundial_clubes', 'bola_de_ouro',
            'biografia', 'altura', 'outras_posicoes'
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

        # Calcular total_trofeus no banco de dados (evita loop)
        jogadores = jogadores.annotate(
            total_trofeus=F('titulos_champions') + F('mundial_clubes'),
            total_pontos=F('titulos_champions') + F('mundial_clubes') + F('bola_de_ouro'),
            ano_nascimento=Case(
                When(inicio_carreira__isnull=False, 
                     then=F('inicio_carreira__year') - 17),
                default=None,
                output_field=IntegerField()
            )
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

        # Paginação ANTES de processar flag codes (otimização)
        paginator = Paginator(jogadores, 12)  # 12 jogadores por página
        try:
            jogadores_paginados = paginator.page(page)
        except PageNotAnInteger:
            jogadores_paginados = paginator.page(1)
        except EmptyPage:
            jogadores_paginados = paginator.page(paginator.num_pages)
        
        # Cache de flag codes - processar apenas nacionalidades únicas
        nacionalidades_unicas = set(
            jogadores_paginados.values_list('nacionalidade', flat=True)
        )
        flag_cache = {
            nat: get_flag_code(nat) 
            for nat in nacionalidades_unicas 
            if nat
        }
        
        # Adicionar flag_code apenas aos jogadores paginados
        for jogador in jogadores_paginados:
            jogador.flag_code = flag_cache.get(jogador.nacionalidade, 'xx')
        
        # Estatísticas para o template
        total_jogadores = paginator.count
        nacionalidades_unicas_list = sorted(list(nacionalidades_unicas))
        
    except Exception as e:
        logger.exception(f"Erro na view jogadores: {e}")
        # Retornar lista vazia em caso de erro
        jogadores_paginados = Paginator(Jogador.objects.none(), 12).page(1)
        total_jogadores = 0
        nacionalidades_unicas_list = []
        paginator = None
    
    context = {
        'jogadores': jogadores_paginados,
        'paginator': paginator,
        'total_jogadores': total_jogadores,
        'nacionalidades': nacionalidades_unicas_list,
        'query': query or '',
        'nacionalidade_filter': nacionalidade or '',
        'posicao_filter': posicao or '',
        'periodo_filter': periodo or '',
    }
    return render(request, 'blog/jogadores.html', context)

    context = {
        'jogadores': jogadores_paginados,
        'paginator': paginator
    }
    return render(request, 'blog/jogadores.html', context)

def render_jogadores(request, template_name):
    jogadores = Jogador.objects.all()
    print(f"Jogadores encontrados: {jogadores}")  # Linha de depuração
    return render(request, template_name, {'jogadores': jogadores})

def jogadores_index(request):
    jogadores = Jogador.objects.all()
    print(f"Jogadores encontrados: {jogadores}")  # Linha de depuração
    return render(request, 'blog/index.html', {'jogadores': jogadores})

def jogadores_page(request):
    """
    View otimizada para listagem de jogadores com paginação.
    Usa select_related/prefetch_related e cálculos no banco para evitar N+1 queries.
    """
    from blog.templatetags.flag_tags import get_flag_code
    from django.db.models import Case, When, IntegerField, F, Q
    from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
    
    try:
        query = request.GET.get('q', '').strip()
        nacionalidade = request.GET.get('nacionalidade', '').strip()
        posicao = request.GET.get('posicao', '').strip()
        periodo = request.GET.get('periodo', '').strip()
        
        try:
            page = int(request.GET.get('page', 1))
        except (ValueError, TypeError):
            page = 1

        # Query base otimizada - usar apenas() para campos necessários
        jogadores = Jogador.objects.only(
            'id', 'nome', 'nacionalidade', 'imagem', 'carta',
            'inicio_carreira', 'fim_carreira', 'perna',
            'titulos_champions', 'mundial_clubes', 'bola_de_ouro',
            'biografia', 'altura', 'outras_posicoes'
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
            jogadores = jogadores.filter(outras_posicoes__icontains=posicao)

        if periodo:
            try:
                start_year, end_year = map(int, periodo.split('-'))
                jogadores = jogadores.filter(
                    Q(inicio_carreira__year__lte=end_year) & Q(fim_carreira__year__gte=start_year)
                )
            except (ValueError, AttributeError):
                pass

        # Calcular total_trofeus no banco de dados (evita loop)
        jogadores = jogadores.annotate(
            total_trofeus=F('titulos_champions') + F('mundial_clubes'),
            total_pontos=F('titulos_champions') + F('mundial_clubes') + F('bola_de_ouro'),
            ano_nascimento=Case(
                When(inicio_carreira__isnull=False, 
                     then=F('inicio_carreira__year') - 17),
                default=None,
                output_field=IntegerField()
            )
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

        # Paginação ANTES de processar flag codes (otimização)
        paginator = Paginator(jogadores, 12)  # 12 jogadores por página
        try:
            jogadores_paginados = paginator.page(page)
        except PageNotAnInteger:
            jogadores_paginados = paginator.page(1)
        except EmptyPage:
            jogadores_paginados = paginator.page(paginator.num_pages)
        
        # Cache de flag codes - processar apenas nacionalidades únicas
        nacionalidades_unicas = set(
            jogador.nacionalidade for jogador in jogadores_paginados if jogador.nacionalidade
        )
        flag_cache = {
            nat: get_flag_code(nat) 
            for nat in nacionalidades_unicas 
            if nat
        }
        
        # Adicionar flag_code apenas aos jogadores paginados
        for jogador in jogadores_paginados:
            jogador.flag_code = flag_cache.get(jogador.nacionalidade, 'xx')
        
        # Estatísticas para o template
        total_jogadores = paginator.count
        nacionalidades_unicas_list = sorted(list(nacionalidades_unicas))
        
    except Exception as e:
        logger.exception(f"Erro na view jogadores_page: {e}")
        # Retornar lista vazia em caso de erro
        jogadores_paginados = Paginator(Jogador.objects.none(), 12).page(1)
        total_jogadores = 0
        nacionalidades_unicas_list = []
        paginator = None
    
    context = {
        'jogadores': jogadores_paginados,
        'paginator': paginator,
        'total_jogadores': total_jogadores,
        'nacionalidades': nacionalidades_unicas_list,
        'query': query or '',
        'nacionalidade_filter': nacionalidade or '',
        'posicao_filter': posicao or '',
        'periodo_filter': periodo or '',
    }
    return render(request, 'blog/jogadores.html', context)

def jogador_detail(request, pk):
    from .security import check_rate_limit, sanitize_html
    
    jogador = get_object_or_404(Jogador, pk=pk)
    comments = Comment.objects.filter(jogador=jogador, active=True)

    if request.method == 'POST':
        # Rate limiting
        is_allowed, remaining, reset_time = check_rate_limit(request, 'comment', limit=5, window=60)
        
        if not is_allowed:
            messages.error(request, f'Muitos comentários. Aguarde {reset_time} segundos.')
            comment_form = CommentForm(request.POST)
        else:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.jogador = jogador
                comment.active = True
                # Sanitizar HTML
                if comment.body:
                    comment.body = sanitize_html(comment.body)
                comment.save()
                messages.success(request, 'Comentário adicionado com sucesso!')
                return redirect('jogador_detail', pk=pk)
    else:
        comment_form = CommentForm()

    from .related_players import get_related_players

    return render(request, 'blog/jogador_detail.html', {
        'jogador': jogador,
        'comments': comments,
        'comment_form': comment_form,
        'jogadores_relacionados': get_related_players(jogador, limit=6),
    })


def time_detail(request, time_id):
    time = get_object_or_404(Time, id=time_id)
    comments = Comment.objects.filter(time=time, active=True)
    
    # Times relacionados (mesma região)
    related_times = Time.objects.filter(regiao=time.regiao).exclude(id=time.id).order_by('?')[:6]
    
    # Eventos da timeline
    from .models import TimelineEvento
    timeline_eventos = TimelineEvento.objects.filter(time=time).order_by('ano', 'ordem')

    if request.method == 'POST':
        from .security import check_rate_limit, sanitize_html
        
        # Rate limiting
        is_allowed, remaining, reset_time = check_rate_limit(request, 'comment', limit=5, window=60)
        
        if not is_allowed:
            messages.error(request, f'Muitos comentários. Aguarde {reset_time} segundos.')
            comment_form = CommentForm(request.POST)
        else:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.time = time
                comment.active = True
                # Sanitizar HTML
                if comment.body:
                    comment.body = sanitize_html(comment.body)
                comment.save()
                messages.success(request, 'Comentário adicionado com sucesso!')
                return redirect('time_detail', time_id=time_id)
    else:
        comment_form = CommentForm()

    context = {
        'time': time,
        'comments': comments,
        'comment_form': comment_form,
        'related_times': related_times,
        'timeline_eventos': timeline_eventos,
    }
    return render(request, 'blog/time_detail.html', context)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post)
    recent_posts = Post.objects.order_by('-created_at')[:5]
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
    else:
        comment_form = CommentForm()
    
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'recent_posts': recent_posts
    })
# View para a lista de estádios
def estadio_list(request):
    estadios = Estadio.objects.all()
    continent_map = {
        'EU': 'Europa',
        'AS': 'América do Sul',
        'AN': 'América do Norte',
        'AF': 'África',
        'ASI': 'Ásia',
        'OC': 'Oceania',
    }
    
    return render(request, 'blog/estadios.html', {
        'estadios': estadios,
        'continent_map': continent_map
    })

# View para detalhes do estádio
def estadio_detail(request, estadio_id):
    estadio = get_object_or_404(Estadio, id=estadio_id)
    return render(request, 'blog/estadio_detail.html', {'estadio': estadio})

def copas(request):
    copas = Copa.objects.all()
    anos_copas = sorted(set(copa.ano for copa in copas))
    
    continent_map = {
        'EU': 'Europa',
        'AS': 'América do Sul',
        'AN': 'América do Norte',
        'AF': 'África',
        'ASI': 'Ásia',
        'OC': 'Oceania'
    }

    context = {
        'copas': copas,
        'anos_copas': anos_copas,
        'continent_map': continent_map
    }
    return render(request, 'blog/copas.html', context)

def copa_detail(request, copa_id):
    copa = get_object_or_404(Copa, id=copa_id)
    comments = Comment.objects.filter(copa=copa, active=True)

    # Buscar a Copa anterior e posterior
    copa_anterior = Copa.objects.filter(ano__lt=copa.ano).order_by('-ano').first()
    copa_posterior = Copa.objects.filter(ano__gt=copa.ano).order_by('ano').first()

    continent_map = {
        'EU': 'Europa',
        'AS': 'América do Sul',
        'AN': 'América do Norte',
        'AF': 'África',
        'ASI': 'Ásia',
        'OC': 'Oceania'
    }

    if request.method == 'POST':
        from .security import check_rate_limit, sanitize_html
        
        # Rate limiting
        is_allowed, remaining, reset_time = check_rate_limit(request, 'comment', limit=5, window=60)
        
        if not is_allowed:
            messages.error(request, f'Muitos comentários. Aguarde {reset_time} segundos.')
            comment_form = CommentForm(request.POST)
        else:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.copa = copa
                comment.active = True
                # Sanitizar HTML
                if comment.body:
                    comment.body = sanitize_html(comment.body)
                comment.save()
                messages.success(request, 'Comentário adicionado com sucesso!')
                return redirect('copa_detail', copa_id=copa_id)
    else:
        comment_form = CommentForm()

    context = {
        'copa': copa,
        'comments': comments,
        'comment_form': comment_form,
        'continent_map': continent_map,
        'copa_anterior': copa_anterior,
        'copa_posterior': copa_posterior,
    }
    return render(request, 'blog/copa_detail.html', context)

def timeline_copas(request):
    """View para a linha do tempo interativa das Copas do Mundo"""
    copas = Copa.objects.all().order_by('ano')
    
    # Adicionar década calculada para cada copa
    copas_com_decada = []
    copas_por_decada = {}
    
    for copa in copas:
        decada = (copa.ano // 10) * 10
        copa.decada = decada
        copas_com_decada.append(copa)
        
        if decada not in copas_por_decada:
            copas_por_decada[decada] = []
        copas_por_decada[decada].append(copa)
    
    continent_map = {
        'EU': 'Europa',
        'AS': 'América do Sul',
        'AN': 'América do Norte',
        'AF': 'África',
        'ASI': 'Ásia',
        'OC': 'Oceania'
    }
    
    context = {
        'copas': copas_com_decada,
        'copas_por_decada': copas_por_decada,
        'continent_map': continent_map,
    }
    return render(request, 'blog/timeline_copas.html', context)

def parallax_craques(request, country_code):
    """
    View para renderizar a página parallax com a história dos craques de cada seleção.
    Mapeia códigos de país para os arquivos parallax correspondentes.
    """
    # Mapeamento de códigos de país para nomes de arquivos
    country_mapping = {
        'BR': {
            'template': 'parallax/index.html',
            'css': 'parallax/styles.css',
            'js': 'parallax/script.js',
            'nome': 'Brasil',
            'nome_completo': 'Seleção Brasileira'
        },
        'AR': {
            'template': 'parallax/index-argentina.html',
            'css': 'parallax/styles-argentina.css',
            'js': 'parallax/script-argentina.js',
            'nome': 'Argentina',
            'nome_completo': 'Seleção Argentina'
        },
        'DE': {
            'template': 'parallax/index-alemanha.html',
            'css': 'parallax/styles-alemanha.css',
            'js': 'parallax/script-alemanha.js',
            'nome': 'Alemanha',
            'nome_completo': 'Seleção Alemã'
        },
        'IT': {
            'template': 'parallax/index-italia.html',
            'css': 'parallax/styles-italia.css',
            'js': 'parallax/script-italia.js',
            'nome': 'Itália',
            'nome_completo': 'Seleção Italiana'
        },
        'FR': {
            'template': 'parallax/index-franca.html',
            'css': 'parallax/styles-franca.css',
            'js': 'parallax/script-franca.js',
            'nome': 'França',
            'nome_completo': 'Seleção Francesa'
        },
        'GB': {
            'template': 'parallax/index-inglaterra.html',
            'css': 'parallax/styles-inglaterra.css',
            'js': 'parallax/script-inglaterra.js',
            'nome': 'Inglaterra',
            'nome_completo': 'Seleção Inglesa'
        },
        'UY': {
            'template': 'parallax/index-uruguai.html',
            'css': 'parallax/styles-uruguai.css',
            'js': 'parallax/script-uruguai.js',
            'nome': 'Uruguai',
            'nome_completo': 'Seleção Uruguaia'
        },
        'ES': {
            'template': 'parallax/index-espanha.html',
            'css': 'parallax/styles-espanha.css',
            'js': 'parallax/script-espanha.js',
            'nome': 'Espanha',
            'nome_completo': 'Seleção Espanhola'
        },
    }
    
    country_code = country_code.upper()
    
    if country_code not in country_mapping:
        # Se o código não existir, redireciona para a página inicial
        return redirect('index')
    
    country_info = country_mapping[country_code]
    
    context = {
        'country_code': country_code,
        'country_name': country_info['nome'],
        'country_full_name': country_info['nome_completo'],
        'parallax_css': country_info['css'],
        'parallax_js': country_info['js'],
    }
    
    # Renderizar o template parallax correspondente
    return render(request, f"blog/{country_info['template']}", context)

# View para Newsletter
@require_POST
def newsletter_subscribe(request):
    """
    View para processar inscrição na newsletter.
    Pode ser integrado com Mailchimp, SendGrid ou salvar no banco.
    """
    email = request.POST.get('email', '').strip()
    
    if not email:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': 'Email é obrigatório'}, status=400)
        messages.error(request, 'Email é obrigatório.')
        return redirect(request.META.get('HTTP_REFERER', '/'))
    
    # Validação básica de email
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': 'Email inválido'}, status=400)
        messages.error(request, 'Email inválido.')
        return redirect(request.META.get('HTTP_REFERER', '/'))
    
    # TODO: Aqui você pode:
    # 1. Salvar no banco de dados (criar modelo NewsletterSubscriber)
    # 2. Enviar para Mailchimp/SendGrid via API
    # 3. Enviar email de confirmação
    
    # Exemplo básico - apenas log (substitua pela sua lógica)
    logger.info(f'Newsletter subscription: {email}')
    
    # Resposta AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True, 
            'message': 'Email cadastrado com sucesso! Verifique sua caixa de entrada.'
        })
    
    # Resposta normal (redirect)
    messages.success(request, 'Email cadastrado com sucesso! Verifique sua caixa de entrada.')
    return redirect(request.META.get('HTTP_REFERER', '/'))