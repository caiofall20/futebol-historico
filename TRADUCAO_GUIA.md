# 🌍 Guia de Tradução - Futebol Histórico

## ✅ **IMPLEMENTADO**

A tradução multi-idioma foi implementada com sucesso! O site agora suporta:
- 🇧🇷 **Português (Brasil)** - Idioma padrão
- 🇺🇸 **English** - Inglês
- 🇪🇸 **Español** - Espanhol

## 📋 Como Funciona

### 1. **Seletor de Idiomas**
O usuário pode mudar o idioma através do dropdown no canto superior direito do header. A mudança é salva em cookie e persiste durante a navegação.

### 2. **Configuração**
- **LocaleMiddleware** ativado no `settings.py`
- **i18n context processor** adicionado
- **LANGUAGES** configurado com pt-br, en, es
- **LOCALE_PATHS** apontando para `/locale`

### 3. **Arquivos de Tradução**
- `locale/en/LC_MESSAGES/django.po` - Traduções em inglês
- `locale/es/LC_MESSAGES/django.po` - Traduções em espanhol
- Arquivos `.mo` compilados automaticamente

## 🔧 Como Adicionar Novas Traduções

### Passo 1: Marcar strings no template
```django
{% load i18n %}

<!-- Antes -->
<a href="/jogadores/">Jogadores</a>

<!-- Depois -->
<a href="/jogadores/">{% trans "Jogadores" %}</a>
```

### Passo 2: Gerar/Atualizar arquivos .po
```bash
cd futebol_historico
python3 manage.py makemessages -l en -l es
```

### Passo 3: Traduzir os textos
Edite os arquivos `.po` em:
- `locale/en/LC_MESSAGES/django.po`
- `locale/es/LC_MESSAGES/django.po`

Preencha as traduções após `msgstr ""`:
```po
msgid "Jogadores"
msgstr "Players"  # Para inglês
```

### Passo 4: Compilar traduções
```bash
python3 manage.py compilemessages
```

### Passo 5: Reiniciar servidor
```bash
python3 manage.py runserver
```

## 📝 Strings Já Traduzidas

### Menu Principal
- Início → Home / Inicio
- Copas → World Cups / Copas del Mundo
- Seleções → National Teams / Selecciones
- Times → Clubs / Clubes
- Jogadores → Players / Jugadores
- Estádios → Stadiums / Estadios

### Footer
- Universo da Bola → Football Universe / Universo del Fútbol
- Todos os direitos reservados → All rights reserved / Todos los derechos reservados

### Acessibilidade
- Pular para conteúdo principal → Skip to main content / Saltar al contenido principal

## 🎯 Próximos Passos

Para traduzir mais conteúdo:

1. **Templates**: Adicione `{% trans "texto" %}` nos templates
2. **Views**: Use `from django.utils.translation import gettext as _` e `_("texto")`
3. **Models**: Adicione `verbose_name` e `help_text` com `_()` para traduzir labels do admin

### Exemplo em Views:
```python
from django.utils.translation import gettext as _

def minha_view(request):
    mensagem = _("Bem-vindo ao site!")
    return render(request, 'template.html', {'mensagem': mensagem})
```

### Exemplo em Models:
```python
from django.utils.translation import gettext_lazy as _

class Jogador(models.Model):
    nome = models.CharField(_("Nome do Jogador"), max_length=200)
```

## 🔍 Verificar Traduções

Para verificar se todas as strings estão traduzidas:
```bash
python3 manage.py makemessages -l en -l es
# Verifique se há strings vazias (msgstr "")
```

## ⚠️ Notas Importantes

1. **Recompilar sempre**: Após editar `.po`, execute `compilemessages`
2. **Formato correto**: Mantenha o formato UTF-8 nos arquivos `.po`
3. **Pluralização**: Alguns idiomas têm regras de plural diferentes (configurado automaticamente)
4. **Cache**: Em produção, limpe o cache após atualizar traduções

## 📚 Recursos

- [Django i18n Documentation](https://docs.djangoproject.com/en/5.0/topics/i18n/)
- [Translation Template Tags](https://docs.djangoproject.com/en/5.0/topics/i18n/translation/#template-tags)

---

**Última atualização:** 2026-02-20
**Idiomas suportados:** pt-br, en, es





