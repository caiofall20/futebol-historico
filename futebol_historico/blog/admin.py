# blog/admin.py

from django.contrib import admin
from .models import Jogador, JogadorRascunho, Post, Image, Comment, Selecao, Time, Estadio, Copa, TimelineEvento
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'

class ImageInline(admin.TabularInline):
    model = Image
    extra = 1

class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    inlines = [ImageInline]

class SelecaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'regiao', 'titulos')
    list_filter = ('regiao',)
    search_fields = ('nome',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)

class TimelineEventoInline(admin.TabularInline):
    model = TimelineEvento
    extra = 1
    fields = ('ano', 'titulo', 'tipo_evento', 'imagem', 'ordem')
    ordering = ('ano', 'ordem')

class TimeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'regiao', 'fundacao', 'titulos', 'created_at')
    list_filter = ('regiao',)
    search_fields = ('nome',)
    readonly_fields = ('created_at',)
    date_hierarchy = 'fundacao'
    inlines = [TimelineEventoInline]
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'imagem', 'descricao', 'fundacao', 'titulos', 'regiao')
        }),
        ('Pilar 1', {
            'fields': ('pilar1_nome', 'pilar1_imagem', 'pilar1_descricao'),
            'classes': ('collapse',)
        }),
        ('Pilar 2', {
            'fields': ('pilar2_nome', 'pilar2_imagem', 'pilar2_descricao'),
            'classes': ('collapse',)
        }),
        ('Pilar 3', {
            'fields': ('pilar3_nome', 'pilar3_imagem', 'pilar3_descricao'),
            'classes': ('collapse',)
        }),
        ('Conteúdo Adicional', {
            'fields': ('momentos_historicos', 'curiosidades', 'legado', 'voce_sabia'),
            'classes': ('collapse',)
        }),
        ('Metadados', {
            'fields': ('created_at',)
        }),
    )

@admin.register(Estadio)
class EstadioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cidade', 'pais', 'continente', 'capacidade')
    list_filter = ('continente', 'pais')
    search_fields = ('nome', 'cidade', 'pais')
    ordering = ('nome',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Copa)
class CopaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ano', 'pais', 'continente', 'campeao')
    list_filter = ('ano', 'continente', 'pais')
    search_fields = ('nome', 'campeao', 'vice_campeao', 'terceiro_lugar')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'data_copa'

@admin.register(TimelineEvento)
class TimelineEventoAdmin(admin.ModelAdmin):
    list_display = ('time', 'ano', 'titulo', 'tipo_evento', 'ordem')
    list_filter = ('tipo_evento', 'ano')
    search_fields = ('titulo', 'time__nome')
    ordering = ('time', 'ano', 'ordem')

admin.site.register(Post, PostAdmin)
admin.site.register(Image)
admin.site.register(Comment, CommentAdmin)
@admin.register(JogadorRascunho)
class JogadorRascunhoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'status', 'criado_por', 'criado_em', 'jogador_publicado')
    list_filter = ('status',)
    search_fields = ('nome',)
    readonly_fields = ('wikidata_id', 'fontes', 'criado_em', 'atualizado_em')

admin.site.register(Jogador)
admin.site.register(Selecao, SelecaoAdmin)
admin.site.register(Time, TimeAdmin)
