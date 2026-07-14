"""
Context processors para variáveis globais nos templates
"""
from django.conf import settings

def monetization(request):
    """
    Adiciona variáveis de monetização ao context de todos os templates
    """
    return {
        'ADSENSE_CLIENT_ID': getattr(settings, 'ADSENSE_CLIENT_ID', ''),
        'GOOGLE_ANALYTICS_ID': getattr(settings, 'GOOGLE_ANALYTICS_ID', ''),
    }


