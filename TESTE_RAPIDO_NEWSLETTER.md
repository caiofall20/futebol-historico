# 🧪 Teste Rápido - Newsletter Popup

## ⚡ Ativar e Testar em 2 Minutos

### Passo 1: Ativar o Template

Edite o arquivo: `futebol_historico/blog/templates/blog/base.html`

**Encontre as linhas 382-385:**
```django
<!-- Newsletter Popup (opcional - descomente para ativar) -->
{% comment %}
{% include 'blog/newsletter_popup.html' %}
{% endcomment %}
```

**Mude para:**
```django
<!-- Newsletter Popup -->
{% include 'blog/newsletter_popup.html' %}
```

### Passo 2: Iniciar Servidor

```bash
cd futebol_historico
python manage.py runserver
```

### Passo 3: Testar

1. **Acesse:** http://localhost:8000/jogadores/
2. **Clique em 3 jogadores diferentes** (ou abra 3 páginas de jogadores)
3. **Aguarde 2 segundos** após a terceira visualização
4. **O popup aparecerá automaticamente!** 🎉

### Como Resetar o Teste

Se quiser testar novamente, abra o Console do navegador (F12) e digite:
```javascript
localStorage.removeItem('newsletterShown');
localStorage.setItem('viewedPlayers', '3');
location.reload();
```

---

## 🎨 O que você verá:

- **Fundo:** Escuro com blur
- **Card central:** Gradiente azul escuro
- **Ícone:** 📧
- **Título:** "Receba Curiosidades Diárias!"
- **Campo de email:** Com placeholder
- **Botão:** "Receber Grátis" (azul)
- **Botão X:** No canto superior direito para fechar

---

## ✅ Funcionalidades:

- ✅ Aparece após ver 3 jogadores
- ✅ Só aparece uma vez (salva no navegador)
- ✅ Pode fechar clicando no X
- ✅ Pode fechar clicando fora do popup
- ✅ Envio via AJAX (sem recarregar página)
- ✅ Validação de email
- ✅ Mensagem de sucesso/erro
- ✅ Design responsivo (mobile-friendly)

---

**Teste agora e veja funcionando!** 🚀


