from django.contrib import admin
from django import forms
from .models import Post, Jogador, Selecao, Time

# Formulário personalizado para Post
class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
    capa = forms.ImageField(required=False)
    def __init__(self, *args, **kwargs):
        super(PostAdminForm, self).__init__(*args, **kwargs)

        # Adiciona a lógica para exibir o inline correto com base na categoria
        if self.instance and self.instance.category:
            if self.instance.category == 'jogadores':
                self.fields['jogador'].widget = forms.Select()
            elif self.instance.category == 'selecoes':
                self.fields['selecao'].widget = forms.Select()
            elif self.instance.category == 'times':
                self.fields['time'].widget = forms.Select()

# Inline para Jogador
class JogadorInline(admin.StackedInline):
    model = Jogador
    extra = 1
    max_num = 1

# Inline para Selecao
class SelecaoInline(admin.StackedInline):
    model = Selecao
    extra = 1
    max_num = 1

# Inline para Time
class TimeInline(admin.StackedInline):
    model = Time
    extra = 1
    max_num = 1

# Registro no admin com o formulário personalizado e inlines dinâmicos
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ('title', 'category', 'created_at')

    # Condicionalmente mostrar o inline com base na categoria
    def get_inlines(self, request, obj):
        if obj and obj.category == 'jogadores':
            return [JogadorInline]
        elif obj and obj.category == 'selecoes':
            return [SelecaoInline]
        elif obj and obj.category == 'times':
            return [TimeInline]
        return []

admin.site.register(Post, PostAdmin)
admin.site.register(Jogador)
admin.site.register(Selecao)
admin.site.register(Time)
