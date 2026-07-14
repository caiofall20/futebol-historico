from django.urls import path

from . import redacao_views

urlpatterns = [
    path('', redacao_views.redacao_home, name='redacao_home'),
    path('jogadores/novo/', redacao_views.redacao_criar, name='redacao_criar'),
    path('portal/<int:jogador_pk>/editar/', redacao_views.redacao_abrir_jogador, name='redacao_abrir_jogador'),
    path('api/gerar/', redacao_views.api_iniciar_geracao, name='redacao_api_gerar'),
    path('api/rascunho/<int:pk>/status/', redacao_views.api_status_geracao, name='redacao_api_status'),
    path('api/rascunho/<int:pk>/regenerar/', redacao_views.api_regenerar, name='redacao_api_regenerar'),
    path('api/rascunho/<int:pk>/carta/', redacao_views.api_gerar_carta, name='redacao_api_carta'),
    path('api/crest-lookup/', redacao_views.api_crest_lookup, name='redacao_api_crest_lookup'),
    path('api/crest-resolve-club/', redacao_views.api_crest_resolve_club, name='redacao_api_crest_resolve_club'),
    path('api/crest-proxy/', redacao_views.api_crest_proxy, name='redacao_api_crest_proxy'),
    path('jogadores/<int:pk>/carta/', redacao_views.redacao_carta_editor, name='redacao_carta_editor'),
    path('jogadores/<int:pk>/revisar/', redacao_views.redacao_revisar, name='redacao_revisar'),
    path('jogadores/<int:pk>/excluir/', redacao_views.redacao_excluir, name='redacao_excluir'),
]
