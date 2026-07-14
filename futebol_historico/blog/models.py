# blog/models.py

from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

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
    image = models.ImageField(upload_to='uploads/')

    
    def __str__(self):
        return f"Image for post: {self.post.title}"

class Jogador(models.Model):
    """
    Modelo para representar jogadores de futebol.
    
    Campos de imagem (INDEPENDENTES - não se sobrescrevem):
    - imagem_carrossel: Imagem para o carrossel da página inicial - salva em 'carrossel_jogadores/'
    - imagem: Foto do jogador para página de detalhes - salva em 'jogadores/'
    - carta: Carta/card do jogador para página de listagem (jogadores.html) - salva em 'cartas_jogadores/'
    
    IMPORTANTE:
    - Carrossel (index.html): usa APENAS 'imagem_carrossel' dos jogadores
    - Página de detalhes (jogador_detail.html): usa 'imagem' primeiro, 'carta' como fallback
    - Página de listagem (jogadores.html): usa 'carta' primeiro, 'imagem' como fallback
    """
    nome = models.CharField(max_length=200, verbose_name="Nome do Jogador")
    imagem_carrossel = models.ImageField(
        upload_to='carrossel_jogadores/', 
        blank=True, 
        null=True,
        verbose_name="Imagem do Carrossel",
        help_text="Imagem para exibir no carrossel da página inicial (diretório: carrossel_jogadores/)"
    )
    imagem = models.ImageField(
        upload_to='jogadores/', 
        blank=True, 
        null=True,
        verbose_name="Imagem do Jogador",
        help_text="Foto do jogador para página de detalhes (diretório: jogadores/)"
    )
    biografia = RichTextUploadingField(blank=True, null=True, verbose_name="Biografia")
    carta = models.ImageField(
        upload_to='cartas_jogadores/', 
        blank=True, 
        null=True,
        verbose_name="Carta do Jogador",
        help_text="Carta/card do jogador para página de listagem (jogadores.html) (diretório: cartas_jogadores/)"
    )
    nacionalidade = models.CharField(max_length=100, default='Desconhecida', verbose_name="Nacionalidade")
    inicio_carreira = models.DateField(default='1900-01-01', verbose_name="Início da Carreira")
    fim_carreira = models.DateField(default='2000-01-01', verbose_name="Fim da Carreira")
    # Campos adicionais para página de detalhes
    carreira = RichTextUploadingField(
        blank=True, 
        null=True, 
        verbose_name="Histórico da Carreira",
        help_text="Histórico formatado do jogador (clubes/anos)"
    )
    altura = models.CharField(
        max_length=20, 
        blank=True, 
        null=True, 
        verbose_name="Altura",
        help_text="Ex.: 1,77 m"
    )
    perna = models.CharField(
        max_length=30, 
        blank=True, 
        null=True, 
        verbose_name="Pé Dominante",
        help_text="Destro, Canhoto, Ambidestro"
    )
    outras_posicoes = models.CharField(
        max_length=200, 
        blank=True, 
        null=True,
        verbose_name="Outras Posições"
    )
    titulos_champions = models.PositiveIntegerField(
        default=0,
        verbose_name="Títulos da Champions League"
    )
    bola_de_ouro = models.PositiveIntegerField(
        default=0,
        verbose_name="Bolas de Ouro"
    )
    mundial_clubes = models.PositiveIntegerField(
        default=0,
        verbose_name="Mundiais de Clubes"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")

    @property
    def posicao(self):
        """Retorna a primeira posição de outras_posicoes ou 'Atacante' como padrão"""
        if self.outras_posicoes:
            return self.outras_posicoes.split(',')[0].strip()
        return 'Atacante'

    class Meta:
        verbose_name = "Jogador"
        verbose_name_plural = "Jogadores"
        ordering = ['nome']

    def __str__(self):
        return self.nome


class JogadorRascunho(models.Model):
    """Rascunho gerado pela redação antes de publicar no portal."""

    STATUS_CHOICES = [
        ('gerando', 'Gerando'),
        ('rascunho', 'Rascunho'),
        ('publicado', 'Publicado'),
        ('erro', 'Erro'),
    ]

    criado_por = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='rascunhos_jogador',
        verbose_name='Criado por',
    )
    nome = models.CharField(max_length=200, verbose_name='Nome do jogador')
    wikidata_id = models.CharField(max_length=32, blank=True, verbose_name='ID Wikidata')
    wikipedia_titulo = models.CharField(max_length=255, blank=True, verbose_name='Título Wikipedia')
    fontes = models.TextField(
        blank=True,
        help_text='URLs e referências usadas na geração automática',
    )
    nacionalidade = models.CharField(max_length=100, default='Desconhecida')
    inicio_carreira = models.DateField(default='1900-01-01')
    fim_carreira = models.DateField(default='2000-01-01')
    biografia = RichTextUploadingField(blank=True, null=True)
    carreira = RichTextUploadingField(blank=True, null=True)
    altura = models.CharField(max_length=20, blank=True, null=True)
    perna = models.CharField(max_length=30, blank=True, null=True)
    outras_posicoes = models.CharField(max_length=200, blank=True, null=True)
    titulos_champions = models.PositiveIntegerField(default=0)
    bola_de_ouro = models.PositiveIntegerField(default=0)
    mundial_clubes = models.PositiveIntegerField(default=0)
    carta_stats = models.JSONField(
        default=dict,
        blank=True,
        verbose_name='Atributos da carta FUT',
        help_text='Overall, posição, PAC, SHO, PAS, DRI, DEF, PHY',
    )
    carta_design = models.JSONField(
        default=dict,
        blank=True,
        verbose_name='Design completo da carta',
        help_text='Configuração do editor visual (fundo, foto, estilo, atributos)',
    )
    imagem = models.ImageField(upload_to='jogadores/rascunhos/', blank=True, null=True)
    carta = models.ImageField(upload_to='cartas_jogadores/rascunhos/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='gerando')
    mensagem_erro = models.TextField(blank=True)
    jogador_publicado = models.ForeignKey(
        Jogador,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='rascunhos_origem',
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Rascunho de jogador'
        verbose_name_plural = 'Rascunhos de jogadores'
        ordering = ['-atualizado_em']

    def __str__(self):
        return f'{self.nome} ({self.get_status_display()})'


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
    historia = RichTextUploadingField(blank=True, null=True)
    regiao = models.CharField(max_length=20, choices=REGIAO_CHOICES)
    titulos = models.PositiveIntegerField(default=0)
    destaque = models.TextField(blank=True, null=True)
    jogadores_iconicos = models.TextField(blank=True, null=True)
    imagem_time = models.ImageField(upload_to='selecoes/', blank=True, null=True)
    imagem_jogadores_iconicos = models.ImageField(upload_to='selecoes/', blank=True, null=True)
    colocacao = models.CharField(max_length=100, blank=True, null=True)
    tecnico = models.CharField(max_length=100, blank=True, null=True)


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
    
    # Pilares do Time (3 jogadores principais)
    pilar1_nome = models.CharField(max_length=200, blank=True, null=True, help_text="Nome do primeiro pilar")
    pilar1_imagem = models.ImageField(upload_to='pilares/', blank=True, null=True, help_text="Foto do primeiro pilar")
    pilar1_descricao = models.TextField(blank=True, null=True, help_text="Descrição do papel do primeiro pilar no time")
    
    pilar2_nome = models.CharField(max_length=200, blank=True, null=True, help_text="Nome do segundo pilar")
    pilar2_imagem = models.ImageField(upload_to='pilares/', blank=True, null=True, help_text="Foto do segundo pilar")
    pilar2_descricao = models.TextField(blank=True, null=True, help_text="Descrição do papel do segundo pilar no time")
    
    pilar3_nome = models.CharField(max_length=200, blank=True, null=True, help_text="Nome do terceiro pilar")
    pilar3_imagem = models.ImageField(upload_to='pilares/', blank=True, null=True, help_text="Foto do terceiro pilar")
    pilar3_descricao = models.TextField(blank=True, null=True, help_text="Descrição do papel do terceiro pilar no time")
    
    # Seções adicionais
    momentos_historicos = RichTextField(blank=True, null=True, help_text="Momentos históricos do time (formato HTML)")
    curiosidades = RichTextField(blank=True, null=True, help_text="Curiosidades sobre o time (formato HTML)")
    legado = RichTextField(blank=True, null=True, help_text="Legado e impacto do time no futebol")
    voce_sabia = models.TextField(blank=True, null=True, help_text="Fato curioso 'Você sabia?'")

    def __str__(self):
        return self.nome

class TimelineEvento(models.Model):
    """Eventos da timeline de um time"""
    time = models.ForeignKey(Time, related_name='timeline_eventos', on_delete=models.CASCADE)
    ano = models.IntegerField(help_text="Ano do evento")
    titulo = models.CharField(max_length=200, help_text="Ex: Final Champions League 2004")
    descricao = models.TextField(help_text="Descrição detalhada do evento")
    imagem = models.ImageField(upload_to='timeline_eventos/', blank=True, null=True, help_text="Foto do evento")
    tipo_evento = models.CharField(max_length=100, blank=True, null=True, help_text="Ex: Champions League, Libertadores, Campeonato")
    adversario = models.CharField(max_length=200, blank=True, null=True, help_text="Time adversário (se aplicável)")
    resultado = models.CharField(max_length=100, blank=True, null=True, help_text="Ex: 2-1, 3-0")
    ordem = models.IntegerField(default=0, help_text="Ordem de exibição na timeline")
    
    class Meta:
        ordering = ['ano', 'ordem']
        verbose_name = 'Evento da Timeline'
        verbose_name_plural = 'Eventos da Timeline'
    
    def __str__(self):
        return f"{self.time.nome} - {self.ano}: {self.titulo}"

class Copa(models.Model):
    CONTINENTES = [
        ('Europa', 'Europa'),
        ('América do Sul', 'América do Sul'),
        ('América do Norte', 'América do Norte'),
        ('África', 'África'),
        ('Ásia', 'Ásia'),
        ('Oceania', 'Oceania'),
    ]

    nome = models.CharField(max_length=200)
    ano = models.IntegerField()
    pais = models.CharField(max_length=100)
    continente = models.CharField(max_length=20, choices=CONTINENTES)
    campeao = models.CharField(max_length=100, blank=True, null=True)
    vice_campeao = models.CharField(max_length=100, blank=True, null=True)
    terceiro_lugar = models.CharField(max_length=100, blank=True, null=True)
    descricao = RichTextField(blank=True, null=True)
    imagem = models.ImageField(upload_to='copas/', blank=True, null=True)
    data_copa = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-ano']

    def __str__(self):
        return f"{self.nome} ({self.ano})"

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE, null=True, blank=True)
    jogador = models.ForeignKey('Jogador', on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    selecao = models.ForeignKey('Selecao', on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    time = models.ForeignKey('Time', on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    copa = models.ForeignKey('Copa', on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
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
        elif self.copa:
            return f'Comment by {self.name} on Copa: {self.copa.nome}'
        return f'Comment by {self.name}'

class Estadio(models.Model):
    CONTINENTES = [
        ('Europa', 'Europa'),
        ('América do Sul', 'América do Sul'),
        ('América do Norte', 'América do Norte'),
        ('África', 'África'),
        ('Ásia', 'Ásia'),
        ('Oceania', 'Oceania'),
    ]

    nome = models.CharField(max_length=200)
    cidade = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)
    continente = models.CharField(max_length=20, choices=CONTINENTES)
    capacidade = models.IntegerField(blank=True, null=True)
    descricao = RichTextField(blank=True, null=True)
    imagem = models.ImageField(upload_to='estadios/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nome} - {self.cidade}, {self.pais}"
