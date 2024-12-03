# blog/forms.py

from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    name = forms.CharField(
        label='Nome',
        widget=forms.TextInput(attrs={
            'placeholder': 'Seu nome',
            'class': 'form-control'
        })
    )
    email = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(attrs={
            'placeholder': 'seu@email.com',
            'class': 'form-control'
        })
    )
    body = forms.CharField(
        label='Comentário',
        widget=forms.Textarea(attrs={
            'placeholder': 'Digite seu comentário aqui...',
            'class': 'form-control',
            'rows': 4
        })
    )

    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']
