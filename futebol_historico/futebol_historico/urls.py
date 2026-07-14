# historico_futebol/urls.py

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.views.i18n import set_language
from filebrowser.sites import site
from blog.sitemaps import (
    JogadorSitemap, SelecaoSitemap, TimeSitemap, 
    CopaSitemap, EstadioSitemap, StaticViewSitemap
)

# Sitemaps
sitemaps = {
    'jogadores': JogadorSitemap,
    'selecoes': SelecaoSitemap,
    'times': TimeSitemap,
    'copas': CopaSitemap,
    'estadios': EstadioSitemap,
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('grappelli/', include('grappelli.urls')),  # grappelli URLS
    path('admin/filebrowser/', site.urls),  # filebrowser URLs
    path('i18n/setlang/', set_language, name='set_language'),  # Mudança de idioma
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('redacao/', include('blog.redacao_urls')),
    path('', include('blog.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
