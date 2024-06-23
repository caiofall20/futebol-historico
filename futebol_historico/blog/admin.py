# blog/admin.py

from django.contrib import admin
from .models import Jogador, Post, Image, Comment, Selecao
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

admin.site.register(Post, PostAdmin)
admin.site.register(Image)
admin.site.register(Comment)
admin.site.register(Jogador)
admin.site.register(Selecao, SelecaoAdmin)
