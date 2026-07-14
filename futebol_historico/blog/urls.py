from django.urls import path
from django.views.generic import TemplateView
from . import views
from . import api_views

urlpatterns = [
    path('', views.index, name='index'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('selecoes/', views.selecoes, name='selecoes'),
    path('selecao/<int:selecao_id>/', views.selecao_detail, name='selecao_detail'),
    path('times/', views.times, name='times'),
    path('time/<int:time_id>/', views.time_detail, name='time_detail'),
    path('jogadores/<int:pk>/', views.jogador_detail, name='jogador_detail'),
    path('jogadores/', views.jogadores_page, name='jogadores_page'),
    path('estadios/', views.estadio_list, name='estadio_list'),
    path('estadio/<int:estadio_id>/', views.estadio_detail, name='estadio_detail'),
    path('copas/', views.copas, name='copas'),
    path('copa/<int:copa_id>/', views.copa_detail, name='copa_detail'),
    path('timeline-copas/', views.timeline_copas, name='timeline_copas'),
    path('parallax-craques/<str:country_code>/', views.parallax_craques, name='parallax_craques'),
    
    # SEO
    path('robots.txt', TemplateView.as_view(template_name='blog/robots.txt', content_type='text/plain'), name='robots'),
    
    # Legal
    path('politica-privacidade/', TemplateView.as_view(template_name='blog/politica_privacidade.html'), name='politica_privacidade'),
    path('termos-servico/', TemplateView.as_view(template_name='blog/termos_servico.html'), name='termos_servico'),
    
    # Newsletter
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    
    # API Endpoints
    path('api/jogadores/', api_views.jogadores_api, name='jogadores_api'),
]