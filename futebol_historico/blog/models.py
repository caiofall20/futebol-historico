from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
from django.utils import timezone

class Post(models.Model):
    CATEGORY_CHOICES = [
        ('selecoes', 'Seleções Históricas'),
        ('times', 'Times Históricos'),
        ('jogadores', 'Jogadores Lendários'),
    ]

    title = models.CharField(max_length=200)
    content = RichTextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    capa = models.ImageField(upload_to='capa_posts/', blank=True, null=True)

    # Relacionamento genérico com Jogador, Selecao ou Time
    jogador = models.OneToOneField('Jogador', on_delete=models.SET_NULL, null=True, blank=True)
    selecao = models.OneToOneField('Selecao', on_delete=models.SET_NULL, null=True, blank=True)
    time = models.OneToOneField('Time', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

class Image(models.Model):
    post = models.ForeignKey(Post, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return f"Image for post: {self.post.title}"

class Jogador(models.Model):
    nome = models.CharField(max_length=200)
    imagem = models.ImageField(upload_to='jogadores/', blank=True, null=True)
    biografia = RichTextField()
    carta = models.ImageField(upload_to='cartas/', blank=True, null=True)
    nacionalidade = models.CharField(max_length=100, default='Desconhecida')
    inicio_carreira = models.DateField(default='1900-01-01')
    fim_carreira = models.DateField(default='2000-01-01')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Selecao(models.Model):
    nome = models.CharField(max_length=200)
    imagem = models.ImageField(upload_to='selecoes/', blank=True, null=True)
    descricao = RichTextField()
    regiao = models.CharField(max_length=20, choices=[
        ('América do Sul', 'América do Sul'),
        ('América Central', 'América Central'),
        ('Europa', 'Europa'),
        ('África', 'África'),
        ('Ásia', 'Ásia'),
    ])
    titulos = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Time(models.Model):
    nome = models.CharField(max_length=200)
    imagem = models.ImageField(upload_to='times/', blank=True, null=True)
    descricao = RichTextUploadingField()
    fundacao = models.DateField(default=timezone.now)
    titulos = models.IntegerField(default=0)
    regiao = models.CharField(max_length=100, choices=[
        ('América do Sul', 'América do Sul'),
        ('América Central', 'América Central'),
        ('Europa', 'Europa'),
        ('África', 'África'),
        ('Ásia', 'Ásia'),
    ], default='Europa')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    jogador = models.ForeignKey(Jogador, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
