import os
from django.conf import settings
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'futebol_historico.settings')
application = get_wsgi_application()

from blog.models import Estadio

# Caminho para a pasta de imagens
image_directory = os.path.join(settings.MEDIA_ROOT, 'estadios')

# Atualizar imagens dos estádios
for estadio in Estadio.objects.all():
    image_path = os.path.join(image_directory, f"{estadio.nome.lower().replace(' ', '_')}.jpg")
    if os.path.exists(image_path):
        estadio.imagem.name = f"estadios/{os.path.basename(image_path)}"
        estadio.save()
        print(f"Imagem atualizada para {estadio.nome}")
    else:
        print(f"Imagem não encontrada para {estadio.nome}")
