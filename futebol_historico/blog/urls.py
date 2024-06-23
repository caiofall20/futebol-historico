# blog/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('selecoes/', views.selecoes, name='selecoes'),
    path('selecao/<int:selecao_id>/', views.selecao_detail, name='selecao_detail'),
    path('times/', views.times, name='times'),
    path('time/<int:time_id>/', views.time_detail, name='time_detail'),
    path('jogadores/', views.jogadores, name='jogadores'),
    path('jogadores/', views.jogadores, name='jogadores'),
    path('jogadores/<int:jogador_id>/', views.jogador_detail, name='jogador_detail'),
]