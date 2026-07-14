# 🚀 Guia Rápido: Colocando o Portal no Ar

## ⚡ Checklist Rápido (30 minutos)

### 1. Segurança Básica (10 min)
```bash
# 1. Gerar nova SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# 2. Criar arquivo .env
cat > .env << EOF
SECRET_KEY=sua-nova-chave-aqui
DEBUG=False
ALLOWED_HOSTS=seudominio.com,www.seudominio.com
DB_NAME=futebol_historico
DB_USER=postgres
DB_PASSWORD=senha_segura
DB_HOST=localhost
DB_PORT=5432
REDIS_URL=redis://localhost:6379/1
EOF

# 3. Instalar python-dotenv
pip install python-dotenv
```

### 2. Atualizar settings.py (5 min)
```python
# Adicionar no início do settings.py
from dotenv import load_dotenv
load_dotenv()

# Substituir:
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')
```

### 3. Preparar para Deploy (15 min)

#### Opção A: Railway (Mais Fácil)
1. Criar conta em https://railway.app
2. Conectar repositório GitHub
3. Adicionar variáveis de ambiente
4. Deploy automático!

#### Opção B: Render
1. Criar conta em https://render.com
2. New Web Service
3. Conectar repositório
4. Configurar:
   - Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - Start Command: `gunicorn futebol_historico.wsgi:application`

## 📦 Dependências Adicionais

```bash
# Adicionar ao requirements.txt
python-dotenv==1.0.0
gunicorn==21.2.0
psycopg2-binary==2.9.9
django-redis==5.4.0
whitenoise==6.6.0  # Para servir static files
```

## 🔧 Comandos Úteis

```bash
# Coletar static files
python manage.py collectstatic --noinput

# Migrar banco de dados
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Verificar configurações
python manage.py check --deploy
```

## 🎯 Próximos Passos

1. ✅ Segurança básica
2. ✅ Deploy
3. ⏭️ Google AdSense
4. ⏭️ Newsletter
5. ⏭️ Analytics

---

**Tempo total estimado:** 30-60 minutos para deploy básico


