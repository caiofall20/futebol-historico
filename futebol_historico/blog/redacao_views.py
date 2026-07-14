import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import OuterRef, Q, Subquery
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from .content_pipeline.async_jobs import start_background_generation
from .content_pipeline.card_stats import CartaFutStats, compute_carta_stats
from .content_pipeline.llm_enhancer import is_llm_enabled
from .content_pipeline.card_crests import FIFAROSTERS_BASE, lookup_crests, resolve_club_crest_url
from .content_pipeline.card_design import (
    CARD_TEMPLATES,
    default_card_design,
    fifarosters_assets_imported,
    load_fifarosters_styles,
)
from .content_pipeline.services import (
    ensure_rascunho_from_jogador,
    publish_rascunho,
    save_carta_from_design,
    save_carta_from_stats,
    sync_published_jogador_from_rascunho,
)
from .models import Jogador, JogadorRascunho
from .redacao_forms import NovoJogadorForm, REVISAR_DADOS_JOGADOR_FIELDS, RevisarJogadorForm


def _is_staff(user):
    return user.is_authenticated and user.is_staff


staff_required = user_passes_test(_is_staff, login_url='/admin/login/')


def _get_rascunho(pk: int) -> JogadorRascunho:
    """Staff pode editar qualquer rascunho (não só os criados por si)."""
    return get_object_or_404(JogadorRascunho, pk=pk)


def _rascunho_json(rascunho: JogadorRascunho) -> dict:
    data = {
        'ok': True,
        'pk': rascunho.pk,
        'status': rascunho.status,
        'nome': rascunho.nome,
        'mensagem_erro': rascunho.mensagem_erro or '',
        'llm_ativo': is_llm_enabled(),
    }
    if rascunho.status in ('rascunho', 'erro'):
        data['redirect_url'] = reverse('redacao_revisar', kwargs={'pk': rascunho.pk})
    return data


def _carta_save_response(rascunho: JogadorRascunho) -> dict:
    rascunho.refresh_from_db()
    jogador = rascunho.jogador_publicado
    resp = {
        'ok': True,
        'carta_url': rascunho.carta.url if rascunho.carta else '',
        'portal_atualizado': bool(jogador and jogador.carta),
    }
    if jogador and jogador.carta:
        resp['portal_carta_url'] = jogador.carta.url
    return resp


@login_required(login_url='/admin/login/')
@staff_required
def redacao_home(request):
    busca = (request.GET.get('q') or '').strip()
    try:
        page_num = max(1, int(request.GET.get('page', 1)))
    except (TypeError, ValueError):
        page_num = 1

    latest_rascunho_pk = (
        JogadorRascunho.objects.filter(jogador_publicado_id=OuterRef('pk'))
        .order_by('-atualizado_em')
        .values('pk')[:1]
    )

    jogadores_qs = Jogador.objects.annotate(
        rascunho_pk=Subquery(latest_rascunho_pk),
    ).order_by('nome')

    if busca:
        jogadores_qs = jogadores_qs.filter(
            Q(nome__icontains=busca) | Q(nacionalidade__icontains=busca)
        )

    paginator = Paginator(jogadores_qs, 40)
    jogadores_page = paginator.get_page(page_num)

    rascunhos_avulsos = (
        JogadorRascunho.objects.filter(jogador_publicado__isnull=True)
        .order_by('-atualizado_em')
    )
    if busca:
        rascunhos_avulsos = rascunhos_avulsos.filter(nome__icontains=busca)

    total_portal = Jogador.objects.count()
    total_rascunhos = JogadorRascunho.objects.count()

    return render(request, 'blog/redacao/home.html', {
        'jogadores_page': jogadores_page,
        'rascunhos_avulsos': rascunhos_avulsos,
        'busca': busca,
        'total_portal': total_portal,
        'total_rascunhos': total_rascunhos,
        'llm_ativo': is_llm_enabled(),
    })


@login_required(login_url='/admin/login/')
@staff_required
@require_GET
def redacao_abrir_jogador(request, jogador_pk):
    """Abre (ou cria) rascunho a partir de um Jogador já publicado no portal."""
    jogador = get_object_or_404(Jogador, pk=jogador_pk)
    rascunho = ensure_rascunho_from_jogador(jogador, request.user)
    return redirect('redacao_revisar', pk=rascunho.pk)


@login_required(login_url='/admin/login/')
@staff_required
@require_http_methods(['GET'])
def redacao_criar(request):
    return render(request, 'blog/redacao/criar.html', {
        'form': NovoJogadorForm(),
        'llm_ativo': is_llm_enabled(),
    })


@login_required(login_url='/admin/login/')
@staff_required
@require_POST
def api_iniciar_geracao(request):
    form = NovoJogadorForm(request.POST)
    if not form.is_valid():
        return JsonResponse({'ok': False, 'errors': form.errors}, status=400)

    nome = form.cleaned_data['nome'].strip()
    rascunho = JogadorRascunho.objects.create(
        criado_por=request.user,
        nome=nome,
        status='gerando',
    )
    started = start_background_generation(rascunho.pk, nome)
    if not started:
        rascunho.status = 'erro'
        rascunho.mensagem_erro = 'Geração já em andamento para este rascunho.'
        rascunho.save()
        return JsonResponse(_rascunho_json(rascunho), status=409)

    return JsonResponse(_rascunho_json(rascunho))


@login_required(login_url='/admin/login/')
@staff_required
@require_GET
def api_status_geracao(request, pk):
    rascunho = _get_rascunho(pk)
    return JsonResponse(_rascunho_json(rascunho))


@login_required(login_url='/admin/login/')
@staff_required
@require_POST
def api_regenerar(request, pk):
    rascunho = _get_rascunho(pk)
    if rascunho.status == 'gerando':
        return JsonResponse({
            'ok': False,
            'error': 'Aguarde a geração atual terminar.',
        }, status=409)

    nome = request.POST.get('nome_busca', rascunho.nome).strip()
    rascunho.status = 'gerando'
    rascunho.mensagem_erro = ''
    rascunho.save(update_fields=['status', 'mensagem_erro', 'atualizado_em'])

    started = start_background_generation(rascunho.pk, nome)
    if not started:
        return JsonResponse({'ok': False, 'error': 'Geração já em andamento.'}, status=409)

    return JsonResponse(_rascunho_json(rascunho))


def _carta_stats_for_rascunho(rascunho: JogadorRascunho) -> dict:
    if rascunho.carta_stats:
        return rascunho.carta_stats
    return compute_carta_stats(
        outras_posicoes=rascunho.outras_posicoes or '',
        titulos_champions=rascunho.titulos_champions,
        bola_de_ouro=rascunho.bola_de_ouro,
        mundial_clubes=rascunho.mundial_clubes,
        inicio_carreira=rascunho.inicio_carreira,
        fim_carreira=rascunho.fim_carreira,
        perna=rascunho.perna or '',
    ).to_dict()


@login_required(login_url='/admin/login/')
@staff_required
@require_http_methods(['GET', 'POST'])
def redacao_revisar(request, pk):
    rascunho = _get_rascunho(pk)
    rascunho.refresh_from_db()

    if request.method == 'POST':
        action = request.POST.get('action', 'salvar')

        if action == 'regenerar':
            nome = request.POST.get('nome_busca', rascunho.nome)
            if rascunho.status != 'gerando':
                rascunho.status = 'gerando'
                rascunho.save(update_fields=['status', 'atualizado_em'])
                start_background_generation(rascunho.pk, nome)
            messages.info(request, 'Geração iniciada. A página será atualizada automaticamente.')
            return redirect('redacao_revisar', pk=pk)

        form = RevisarJogadorForm(request.POST, request.FILES, instance=rascunho)
        if form.is_valid():
            ja_publicado = (
                rascunho.status == 'publicado' or bool(rascunho.jogador_publicado_id)
            )
            rascunho = form.save(commit=False)
            rascunho.status = 'publicado' if ja_publicado else 'rascunho'
            rascunho.save()
            sync_published_jogador_from_rascunho(rascunho)

            if action == 'publicar':
                jogador = publish_rascunho(rascunho)
                messages.success(
                    request,
                    'Jogador publicado! Já está visível no portal.',
                )
                return redirect('jogador_detail', pk=jogador.pk)

            messages.success(request, 'Rascunho salvo.')
            return redirect('redacao_revisar', pk=pk)
    else:
        form = RevisarJogadorForm(instance=rascunho)

    dados_incompletos = (
        rascunho.nacionalidade in ('', 'Desconhecida')
        or rascunho.inicio_carreira.year <= 1901
    )

    return render(request, 'blog/redacao/revisar.html', {
        'form': form,
        'rascunho': rascunho,
        'dados_jogador_fields': [form[name] for name in REVISAR_DADOS_JOGADOR_FIELDS],
        'llm_ativo': is_llm_enabled(),
        'dados_incompletos': dados_incompletos,
        'preview_url': reverse('jogador_detail', kwargs={'pk': rascunho.jogador_publicado_id})
        if rascunho.jogador_publicado_id else None,
    })


@login_required(login_url='/admin/login/')
@staff_required
@require_GET
def api_crest_lookup(request):
    crest_type = (request.GET.get('type') or '').strip().lower()
    term = (request.GET.get('term') or '').strip()
    if crest_type not in ('nation', 'club', 'league'):
        return JsonResponse({'ok': False, 'error': 'type inválido'}, status=400)
    return JsonResponse({'ok': True, 'results': lookup_crests(crest_type, term)})


@login_required(login_url='/admin/login/')
@staff_required
@require_GET
def api_crest_resolve_club(request):
    """Resolve URL válida do escudo de clube (fallback fifa25 se fifa26 falhar)."""
    club_id = (request.GET.get('id') or '').strip()
    hint = (request.GET.get('url') or '').strip()
    if not club_id:
        return JsonResponse({'ok': False, 'error': 'id obrigatório'}, status=400)
    resolved = resolve_club_crest_url(club_id, hint)
    return JsonResponse({'ok': True, 'id': club_id, 'url': resolved})


@login_required(login_url='/admin/login/')
@staff_required
@require_GET
def api_crest_proxy(request):
    """Proxy de imagens FifaRosters para evitar CORS na prévia e no PNG."""
    target = (request.GET.get('url') or '').strip()
    if not target.startswith(FIFAROSTERS_BASE):
        return HttpResponse(status=400)
    try:
        from urllib.request import Request, urlopen

        req = Request(target, headers={'User-Agent': 'FutebolHistorico/1.0'})
        with urlopen(req, timeout=15) as resp:
            data = resp.read()
            ctype = resp.headers.get('Content-Type', 'image/png')
        return HttpResponse(data, content_type=ctype)
    except Exception:
        return HttpResponse(status=502)


@login_required(login_url='/admin/login/')
@staff_required
@require_http_methods(['GET'])
def redacao_carta_editor(request, pk):
    rascunho = _get_rascunho(pk)
    design = default_card_design(rascunho)
    fifa_styles = load_fifarosters_styles()
    return render(request, 'blog/redacao/carta_editor.html', {
        'rascunho': rascunho,
        'design_json': json.dumps(design, ensure_ascii=False),
        'card_templates': CARD_TEMPLATES,
        'fifa_card_styles': fifa_styles,
        'fifarosters_imported': fifarosters_assets_imported(),
        'revisar_url': reverse('redacao_revisar', kwargs={'pk': pk}),
        'crest_lookup_url': reverse('redacao_api_crest_lookup'),
        'crest_proxy_url': reverse('redacao_api_crest_proxy'),
    })


@login_required(login_url='/admin/login/')
@staff_required
@require_POST
def api_gerar_carta(request, pk):
    rascunho = _get_rascunho(pk)

    if request.content_type and 'multipart/form-data' in request.content_type:
        design_raw = request.POST.get('design', '{}')
        try:
            design = json.loads(design_raw)
        except json.JSONDecodeError:
            return JsonResponse({'ok': False, 'error': 'JSON inválido'}, status=400)
        png_bytes = None
        if 'carta_png' in request.FILES:
            png_bytes = request.FILES['carta_png'].read()
        try:
            save_carta_from_design(rascunho, design, png_bytes=png_bytes)
            return JsonResponse(_carta_save_response(rascunho))
        except Exception as e:
            return JsonResponse({'ok': False, 'error': str(e)}, status=400)

    try:
        payload = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'ok': False, 'error': 'JSON inválido'}, status=400)

    if payload.get('version') == 2 or 'template' in payload:
        try:
            save_carta_from_design(rascunho, payload)
            return JsonResponse(_carta_save_response(rascunho))
        except Exception as e:
            return JsonResponse({'ok': False, 'error': str(e)}, status=400)

    try:
        stats = CartaFutStats.from_dict(payload)
        save_carta_from_stats(rascunho, stats.to_dict())
        rascunho.refresh_from_db()
        resp = _carta_save_response(rascunho)
        resp['stats'] = stats.to_dict()
        return JsonResponse(resp)
    except (TypeError, ValueError) as e:
        return JsonResponse({'ok': False, 'error': str(e)}, status=400)


@login_required(login_url='/admin/login/')
@staff_required
@require_POST
def redacao_excluir(request, pk):
    rascunho = _get_rascunho(pk)
    rascunho.delete()
    messages.info(request, 'Rascunho excluído.')
    return redirect('redacao_home')
