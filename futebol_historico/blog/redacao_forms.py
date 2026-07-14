from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .content_pipeline.card_stats import CartaFutStats, compute_carta_stats
from .models import JogadorRascunho


class NovoJogadorForm(forms.Form):
    nome = forms.CharField(
        label='Nome do jogador',
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'redacao-input',
            'placeholder': 'Ex.: Hidetoshi Nakata',
            'autocomplete': 'off',
        }),
        help_text='Use o nome completo (evite só o sobrenome). Ex.: "Hidetoshi Nakata", não só "Nakata".',
    )


# Campos exibidos na seção "Dados do jogador" na revisão
REVISAR_DADOS_JOGADOR_FIELDS = (
    'nome',
    'nacionalidade',
    'inicio_carreira',
    'fim_carreira',
    'altura',
    'perna',
    'outras_posicoes',
    'titulos_champions',
    'bola_de_ouro',
    'mundial_clubes',
)


class RevisarJogadorForm(forms.ModelForm):
    biografia = forms.CharField(
        required=False,
        widget=CKEditorUploadingWidget(config_name='default'),
    )
    carreira = forms.CharField(
        required=False,
        widget=CKEditorUploadingWidget(config_name='default'),
    )

    class Meta:
        model = JogadorRascunho
        fields = [
            *REVISAR_DADOS_JOGADOR_FIELDS,
            'biografia',
            'carreira',
            'imagem',
            'carta',
        ]
        labels = {
            'nome': 'Nome',
            'nacionalidade': 'Nacionalidade',
            'inicio_carreira': 'Início da carreira',
            'fim_carreira': 'Fim da carreira / aposentadoria',
            'altura': 'Altura',
            'perna': 'Pé dominante',
            'outras_posicoes': 'Posições',
            'titulos_champions': 'Títulos Champions League',
            'bola_de_ouro': 'Bola de Ouro',
            'mundial_clubes': 'Mundial de Clubes',
            'imagem': 'Foto do jogador (detalhe / editor de carta)',
            'carta': 'Carta FUT (PNG para listagem)',
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'redacao-input'}),
            'nacionalidade': forms.TextInput(attrs={'class': 'redacao-input'}),
            'altura': forms.TextInput(attrs={'class': 'redacao-input', 'placeholder': '1,78 m'}),
            'perna': forms.TextInput(attrs={'class': 'redacao-input', 'placeholder': 'Destro, canhoto…'}),
            'outras_posicoes': forms.TextInput(attrs={'class': 'redacao-input', 'placeholder': 'Ex.: MEI, ATA'}),
            'titulos_champions': forms.NumberInput(attrs={'class': 'redacao-input', 'min': 0}),
            'bola_de_ouro': forms.NumberInput(attrs={'class': 'redacao-input', 'min': 0}),
            'mundial_clubes': forms.NumberInput(attrs={'class': 'redacao-input', 'min': 0}),
            'imagem': forms.ClearableFileInput(attrs={
                'class': 'redacao-file-input',
                'accept': 'image/png,image/jpeg,image/webp',
            }),
            'carta': forms.ClearableFileInput(attrs={
                'class': 'redacao-file-input',
                'accept': 'image/png,image/jpeg,image/webp',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        date_widget = forms.DateInput(
            format='%Y-%m-%d',
            attrs={'class': 'redacao-input', 'type': 'date'},
        )
        for dname in ('inicio_carreira', 'fim_carreira'):
            self.fields[dname].widget = date_widget
            self.fields[dname].input_formats = ['%Y-%m-%d']
            if self.instance and self.instance.pk:
                dval = getattr(self.instance, dname, None)
                if dval:
                    self.fields[dname].initial = dval.strftime('%Y-%m-%d')


class CartaFutForm(forms.Form):
    _wi = {'class': 'redacao-input'}
    overall = forms.IntegerField(min_value=40, max_value=99, label='Overall', widget=forms.NumberInput(attrs=_wi))
    posicao = forms.CharField(max_length=5, label='Posição', widget=forms.TextInput(attrs=_wi))
    pac = forms.IntegerField(min_value=40, max_value=99, label='PAC', widget=forms.NumberInput(attrs=_wi))
    sho = forms.IntegerField(min_value=40, max_value=99, label='SHO', widget=forms.NumberInput(attrs=_wi))
    pas = forms.IntegerField(min_value=40, max_value=99, label='PAS', widget=forms.NumberInput(attrs=_wi))
    dri = forms.IntegerField(min_value=40, max_value=99, label='DRI', widget=forms.NumberInput(attrs=_wi))
    def_stat = forms.IntegerField(min_value=40, max_value=99, label='DEF', widget=forms.NumberInput(attrs=_wi))
    phy = forms.IntegerField(min_value=40, max_value=99, label='PHY', widget=forms.NumberInput(attrs=_wi))

    def __init__(self, *args, rascunho=None, **kwargs):
        super().__init__(*args, **kwargs)
        stats = None
        if rascunho:
            if rascunho.carta_stats:
                stats = CartaFutStats.from_dict(rascunho.carta_stats)
            else:
                stats = compute_carta_stats(
                    outras_posicoes=rascunho.outras_posicoes or '',
                    titulos_champions=rascunho.titulos_champions,
                    bola_de_ouro=rascunho.bola_de_ouro,
                    mundial_clubes=rascunho.mundial_clubes,
                    inicio_carreira=rascunho.inicio_carreira,
                    fim_carreira=rascunho.fim_carreira,
                    perna=rascunho.perna or '',
                )
        if stats:
            self.fields['overall'].initial = stats.overall
            self.fields['posicao'].initial = stats.posicao
            self.fields['pac'].initial = stats.pac
            self.fields['sho'].initial = stats.sho
            self.fields['pas'].initial = stats.pas
            self.fields['dri'].initial = stats.dri
            self.fields['def_stat'].initial = stats.def_
            self.fields['phy'].initial = stats.phy

    def to_stats_dict(self) -> dict:
        cd = self.cleaned_data
        return {
            'overall': cd['overall'],
            'posicao': cd['posicao'].upper()[:5],
            'pac': cd['pac'],
            'sho': cd['sho'],
            'pas': cd['pas'],
            'dri': cd['dri'],
            'def': cd['def_stat'],
            'phy': cd['phy'],
        }
