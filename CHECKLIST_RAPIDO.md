# ✅ Checklist Rápido - Próximos Passos

## 🚨 URGENTE (Fazer AGORA - 10 minutos)

- [ ] **Criar arquivo .env**
  ```bash
  cd futebol_historico
  cp ../env.example .env
  ```

- [ ] **Gerar SECRET_KEY**
  ```bash
  python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  ```
  Copie o resultado e cole no .env

- [ ] **Editar .env (mínimo)**
  ```
  SECRET_KEY=sua-chave-gerada
  DEBUG=True
  ALLOWED_HOSTS=
  ```

- [ ] **Instalar dependências**
  ```bash
  pip install python-dotenv
  ```

- [ ] **Testar**
  ```bash
  python manage.py check
  python manage.py runserver
  ```

---

## 📅 ESTA SEMANA (2-3 horas)

### SEO
- [ ] Atualizar robots.txt (substituir `seudominio.com` pelo seu domínio)
- [ ] Testar sitemap.xml (acessar `/sitemap.xml`)
- [ ] Aplicar para Google Search Console
- [ ] Enviar sitemap para Google

### Monetização
- [ ] **Aplicar para Google AdSense** (pode levar 1-2 semanas para aprovação)
  - Acesse: https://www.google.com/adsense
  - Crie conta
  - Adicione seu site
  - Aguarde aprovação

- [ ] **Configurar Google Analytics**
  - Acesse: https://analytics.google.com
  - Crie propriedade
  - Obtenha Measurement ID (G-XXXXXXXXXX)
  - Adicione no .env: `GOOGLE_ANALYTICS_ID=G-XXXXXXXXXX`

- [ ] **Ativar Newsletter** (opcional por enquanto)
  - Descomente no base.html: `{% include 'blog/newsletter_popup.html' %}`
  - A view já está criada e funcionando!

---

## 🚀 PRÓXIMAS 2 SEMANAS

### Deploy
- [ ] Escolher plataforma (Railway/Render recomendado)
- [ ] Configurar .env em produção
- [ ] Deploy
- [ ] Testar tudo em produção
- [ ] Configurar domínio e SSL

### Pós-Deploy
- [ ] Verificar HTTPS
- [ ] Testar todas as páginas
- [ ] Configurar monitoramento (UptimeRobot - grátis)
- [ ] Enviar sitemap para Google (domínio real)

---

## 💰 MONETIZAÇÃO (Após aprovação AdSense)

- [ ] Adicionar Client ID no .env: `ADSENSE_CLIENT_ID=ca-pub-XXXXXXXXXX`
- [ ] Reiniciar servidor
- [ ] Verificar se anúncios aparecem
- [ ] Configurar posicionamento (já implementado)

---

## 📊 MONITORAMENTO

- [ ] Google Analytics funcionando
- [ ] Google Search Console configurado
- [ ] UptimeRobot configurado (monitoramento de uptime)

---

## ✅ STATUS ATUAL

### Implementado ✅
- [x] Segurança básica
- [x] SEO (sitemap, robots.txt)
- [x] Templates de monetização
- [x] View de newsletter
- [x] Google Analytics preparado
- [x] AdSense preparado

### Pendente ⏳
- [ ] Criar .env (você precisa fazer)
- [ ] Aplicar para AdSense
- [ ] Configurar Analytics
- [ ] Deploy em produção

---

## 🎯 PRIORIDADE

1. **HOJE:** Criar .env e testar localmente
2. **ESTA SEMANA:** Aplicar para AdSense e Analytics
3. **PRÓXIMAS 2 SEMANAS:** Deploy em produção
4. **PRÓXIMO MÊS:** Marketing e crescimento

---

**Tempo total estimado para estar no ar:** 2-3 semanas (incluindo aprovação AdSense)


