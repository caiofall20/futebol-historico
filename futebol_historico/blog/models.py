# blog/models.py

from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField

class Post(models.Model):
    CATEGORY_CHOICES = [
        ('selecoes', 'Seleções Históricas'),
        ('times', 'Times Históricos'),
        ('jogadores', 'Jogadores Lendários'),
    ]
    
    title = models.CharField(max_length=200)
    content = RichTextField()
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='selecoes')

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
    REGIAO_CHOICES = [
        ('América do Sul', 'América do Sul'),
        ('América Central', 'América Central'),
        ('Europa', 'Europa'),
        ('África', 'África'),
        ('Ásia', 'Ásia'),
    ]
    
    nome = models.CharField(max_length=200)
    imagem = models.ImageField(upload_to='selecoes/', blank=True, null=True)
    descricao = RichTextField()
    regiao = models.CharField(max_length=20, choices=REGIAO_CHOICES)
    titulos = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome
    

class Time(models.Model):
    REGIAO_CHOICES = [
        ('América do Sul', 'América do Sul'),
        ('América Central', 'América Central'),
        ('Europa', 'Europa'),
        ('África', 'África'),
        ('Ásia', 'Ásia'),
    ]

    nome = models.CharField(max_length=200)
    imagem = models.ImageField(upload_to='times/', blank=True, null=True)
    descricao = RichTextField()
    fundacao = models.DateField(default=timezone.now)
    titulos = models.IntegerField(default=0)
    regiao = models.CharField(max_length=100, choices=REGIAO_CHOICES, default='Europa')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE, null=True, blank=True)
    jogador = models.ForeignKey(Jogador, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    selecao = models.ForeignKey(Selecao, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    time = models.ForeignKey(Time, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        if self.jogador:
            return f'Comment by {self.name} on Jogador: {self.jogador.nome}'
        elif self.selecao:
            return f'Comment by {self.name} on Seleção: {self.selecao.nome}'
        elif self.time:
            return f'Comment by {self.name} on Time: {self.time.nome}'
        return f'Comment by {self.name}'

class Estadio(models.Model):
    CONTINENTES = [
        ('EU', 'Europa'),
        ('AS', 'América do Sul'),
        ('AN', 'América do Norte'),
        ('AF', 'África'),
        ('ASI', 'Ásia'),
        ('OC', 'Oceania'),
    ]

    nome = models.CharField(max_length=200)
    cidade = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)
    continente = models.CharField(max_length=3, choices=CONTINENTES, default='EU')
    capacidade = models.IntegerField()
    descricao = RichTextField()
    imagem = models.ImageField(upload_to='estadios/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Estádio'
        verbose_name_plural = 'Estádios'
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} ({self.cidade}, {self.pais})"