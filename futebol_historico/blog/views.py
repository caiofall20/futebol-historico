# blog/views.py

import logging
from django.shortcuts import render, get_object_or_404
from .models import Jogador, Post, Comment, Selecao,Time
from .forms import CommentForm

# def index(request):
#     # Obter as 3 últimas postagens
#     recent_posts = Post.objects.order_by('-created_at')[:3]
#     return render(request, 'blog/index.html', {'recent_posts': recent_posts})

logger = logging.getLogger(__name__)

def index(request):
    jogadores = Jogador.objects.all()[:3]
    logger.info(f'Jogadores carregados: {jogadores}')
    context = {
        'jogadores': jogadores
    }
    return render(request, 'blog/index.html', context)

def selecoes(request):
    query = request.GET.get('q')
    region = request.GET.get('region')
    selecoes = Selecao.objects.all()

    if query:
        selecoes = selecoes.filter(nome__icontains=query)

    if region:
        selecoes = selecoes.filter(regiao=region)

    context = {
        'selecoes': selecoes,
    }
    return render(request, 'blog/selecoes.html', context)

def selecao_detail(request, selecao_id):
    selecao = get_object_or_404(Selecao, id=selecao_id)
    context = {
        'selecao': selecao,
    }
    return render(request, 'blog/selecao_detail.html', context)


def times(request):
    times_posts = Post.objects.filter(category='times').order_by('-created_at')
    return render(request, 'blog/times.html', {'posts': times_posts})

def jogadores(request):
    jogadores = Jogador.objects.all()
    print(jogadores)
    return render(request, 'blog/jogadores.html', {'jogadores': jogadores})

# def jogadores_index(request):
#     jogadores = Jogador.objects.all()
#     print(jogadores)  # Adicione esta linha para depurar
#     return render(request, 'blog/index.html', {'jogadores': jogadores})
def render_jogadores(request, template_name):
    jogadores = Jogador.objects.all()
    print(f"Jogadores encontrados: {jogadores}")  # Linha de depuração
    return render(request, template_name, {'jogadores': jogadores})

def jogadores_index(request):
    jogadores = Jogador.objects.all()
    print(f"Jogadores encontrados: {jogadores}")  # Linha de depuração
    return render(request, 'blog/index.html', {'jogadores': jogadores})

def jogadores_page(request):
    jogadores = Jogador.objects.all()
    print(f"Jogadores encontrados: {jogadores}")  # Linha de depuração
    return render(request, 'blog/jogadores.html', {'jogadores': jogadores})

def jogador_detail(request, pk):
    jogador = get_object_or_404(Jogador, pk=pk)
    comments = Comment.objects.filter(jogador=jogador)
    recent_posts = Post.objects.order_by('-created_at')[:5]

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.jogador = jogador
            comment.save()
    else:
        comment_form = CommentForm()

    return render(request, 'blog/jogador_detail.html', {
        'jogador': jogador,
        'comments': comments,
        'comment_form': comment_form,
        'recent_posts': recent_posts
    })


def times(request):
    query = request.GET.get('q')
    region = request.GET.get('region')
    times = Time.objects.all()

    if query:
        times = times.filter(nome__icontains=query)

    if region:
        times = times.filter(regiao=region)

    context = {
        'times': times,
    }
    return render(request, 'blog/times.html', context)

def time_detail(request, time_id):
    time = get_object_or_404(Time, id=time_id)
    context = {
        'time': time,
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
