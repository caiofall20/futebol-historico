from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Jogador, Selecao, Time, Copa, Estadio

class JogadorSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8
    
    def items(self):
        return Jogador.objects.all()
    
    def lastmod(self, obj):
        return obj.updated_at if hasattr(obj, 'updated_at') else None

class SelecaoSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7
    
    def items(self):
        return Selecao.objects.all()

class TimeSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.7
    
    def items(self):
        return Time.objects.all()

class CopaSitemap(Sitemap):
    changefreq = 'yearly'
    priority = 0.9
    
    def items(self):
        return Copa.objects.all()

class EstadioSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6
    
    def items(self):
        return Estadio.objects.all()

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return ['index', 'jogadores_page', 'selecoes', 'times', 'timeline_copas', 'estadio_list']

    def location(self, item):
        return reverse(item)


