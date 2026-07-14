# blog/security.py
"""
Utilitários de segurança: rate limiting, validação de uploads, sanitização
"""
import logging
from django.core.cache import cache
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from PIL import Image
import os

logger = logging.getLogger(__name__)


def check_rate_limit(request, action='comment', limit=5, window=60):
    """
    Verifica rate limiting para ações do usuário.
    
    Args:
        request: HttpRequest object
        action: Tipo de ação ('comment', 'api_call', etc)
        limit: Número máximo de ações permitidas
        window: Janela de tempo em segundos
    
    Returns:
        tuple: (is_allowed: bool, remaining: int, reset_time: int)
    """
    # Identificar usuário (autenticado ou IP)
    if request.user.is_authenticated:
        identifier = f"user_{request.user.id}"
    else:
        identifier = f"ip_{request.META.get('REMOTE_ADDR', 'unknown')}"
    
    cache_key = f"rate_limit_{action}_{identifier}"
    
    # Obter contador atual
    current_count = cache.get(cache_key, 0)
    
    if current_count >= limit:
        # Calcular tempo de reset
        reset_time = cache.ttl(cache_key) or window
        return False, 0, reset_time
    
    # Incrementar contador
    cache.set(cache_key, current_count + 1, window)
    remaining = limit - (current_count + 1)
    
    return True, remaining, window


def validate_image_upload(file, max_size_mb=5, allowed_formats=None):
    """
    Valida upload de imagem.
    
    Args:
        file: Arquivo enviado
        max_size_mb: Tamanho máximo em MB
        allowed_formats: Lista de formatos permitidos (default: ['JPEG', 'PNG', 'WEBP'])
    
    Returns:
        tuple: (is_valid: bool, error_message: str)
    """
    if allowed_formats is None:
        allowed_formats = ['JPEG', 'PNG', 'WEBP']
    
    # Verificar tamanho
    max_size_bytes = max_size_mb * 1024 * 1024
    if file.size > max_size_bytes:
        return False, f"Arquivo muito grande. Tamanho máximo: {max_size_mb}MB"
    
    # Verificar extensão
    ext = os.path.splitext(file.name)[1].lower()
    valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
    if ext not in valid_extensions:
        return False, f"Formato não permitido. Use: {', '.join(valid_extensions)}"
    
    # Verificar conteúdo real do arquivo (não confiar apenas na extensão)
    try:
        img = Image.open(file)
        img.verify()  # Verificar se é uma imagem válida
        
        # Verificar formato
        if img.format not in allowed_formats:
            return False, f"Formato de imagem não permitido. Use: {', '.join(allowed_formats)}"
        
        # Verificar dimensões (opcional - prevenir imagens muito grandes)
        width, height = img.size
        if width > 5000 or height > 5000:
            return False, "Dimensões da imagem muito grandes. Máximo: 5000x5000px"
        
        return True, None
        
    except Exception as e:
        logger.warning(f"Erro ao validar imagem: {e}")
        return False, "Arquivo não é uma imagem válida"


def sanitize_html(text):
    """
    Sanitiza HTML removendo tags e atributos perigosos.
    Usa bleach ou implementação simples.
    
    Args:
        text: Texto HTML a ser sanitizado
    
    Returns:
        str: Texto sanitizado
    """
    try:
        # Tentar usar bleach se disponível
        import bleach
        from bleach.css_sanitizer import CSSSanitizer
        
        allowed_tags = ['p', 'br', 'strong', 'em', 'u', 'a', 'ul', 'ol', 'li']
        allowed_attributes = {
            'a': ['href', 'title'],
        }
        
        css_sanitizer = CSSSanitizer(allowed_css_properties=[])
        
        return bleach.clean(
            text,
            tags=allowed_tags,
            attributes=allowed_attributes,
            css_sanitizer=css_sanitizer,
            strip=True
        )
    except ImportError:
        # Fallback: remover todas as tags HTML
        import re
        # Remover tags HTML
        text = re.sub(r'<[^>]+>', '', text)
        # Escapar caracteres especiais
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        text = text.replace('"', '&quot;')
        text = text.replace("'", '&#x27;')
        return text


def get_client_ip(request):
    """
    Obtém o IP real do cliente, considerando proxies.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip





