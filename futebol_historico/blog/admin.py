# blog/admin.py

from django.contrib import admin
from .models import Jogador, Post, Image, Comment, Selecao, Time, Estadio
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
    list_display = ('nome', 'regiao', 'titulos', 'created_at')
    list_filter = ('regiao',)
    search_fields = ('nome',)
    readonly_fields = ('created_at',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)

class TimeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'regiao', 'fundacao', 'titulos', 'created_at')
    list_filter = ('regiao',)
    search_fields = ('nome',)
    readonly_fields = ('created_at',)
    date_hierarchy = 'fundacao'

@admin.register(Estadio)
class EstadioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cidade', 'pais', 'continente', 'capacidade')
    list_filter = ('continente', 'pais')
    search_fields = ('nome', 'cidade', 'pais')
    ordering = ('nome',)
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Post, PostAdmin)
admin.site.register(Image)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Jogador)
admin.site.register(Selecao, SelecaoAdmin)
admin.site.register(Time, TimeAdmin)
