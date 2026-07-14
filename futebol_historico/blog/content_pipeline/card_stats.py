"""Calcula overall e atributos estilo carta FUT a partir dos dados do portal."""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional


POSICAO_ABREV = {
    'goleiro': 'GOL',
    'defensor': 'ZAG',
    'lateral': 'LAT',
    'volante': 'VOL',
    'meia': 'MEI',
    'meia-atacante': 'MEI',
    'meia-atacante': 'MEI',
    'atacante': 'ATA',
    'centroavante': 'ATA',
    'ponta': 'PD',
    'ponta-direita': 'PD',
    'ponta-esquerda': 'PE',
}


@dataclass
class CartaFutStats:
    overall: int = 85
    posicao: str = 'MEI'
    pac: int = 80
    sho: int = 80
    pas: int = 80
    dri: int = 80
    def_: int = 70
    phy: int = 80

    def to_dict(self) -> dict:
        return {
            'overall': self.overall,
            'posicao': self.posicao,
            'pac': self.pac,
            'sho': self.sho,
            'pas': self.pas,
            'dri': self.dri,
            'def': self.def_,
            'phy': self.phy,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'CartaFutStats':
        return cls(
            overall=int(data.get('overall', 85)),
            posicao=str(data.get('posicao', 'MEI'))[:5].upper(),
            pac=int(data.get('pac', 80)),
            sho=int(data.get('sho', 80)),
            pas=int(data.get('pas', 80)),
            dri=int(data.get('dri', 80)),
            def_=int(data.get('def', data.get('def_', 70))),
            phy=int(data.get('phy', 80)),
        )


def _clamp(v: int, lo: int = 40, hi: int = 99) -> int:
    return max(lo, min(hi, v))


def posicao_abrev(outras_posicoes: str = '') -> str:
    if not outras_posicoes:
        return 'MEI'
    first = outras_posicoes.split(',')[0].strip().lower()
    for chave, abrev in POSICAO_ABREV.items():
        if chave in first:
            return abrev
    return 'MEI'


def compute_carta_stats(
    outras_posicoes: str = '',
    titulos_champions: int = 0,
    bola_de_ouro: int = 0,
    mundial_clubes: int = 0,
    inicio_carreira=None,
    fim_carreira=None,
    perna: str = '',
) -> CartaFutStats:
    """Deriva nota geral e atributos a partir de troféus e posição."""
    pos = posicao_abrev(outras_posicoes)
    trofeus = titulos_champions + mundial_clubes
    overall = 72 + trofeus * 4 + bola_de_ouro * 5
    if inicio_carreira and fim_carreira:
        anos = max(1, fim_carreira.year - inicio_carreira.year)
        if anos >= 15:
            overall += 3
    overall = _clamp(overall)

    # Perfil por posição
    base = {
        'GOL': (58, 42, 62, 58, 88, 78),
        'ZAG': (62, 48, 68, 58, 92, 86),
        'LAT': (84, 58, 74, 78, 72, 80),
        'VOL': (68, 62, 82, 72, 86, 84),
        'MEI': (76, 78, 88, 86, 62, 74),
        'ATA': (88, 92, 78, 90, 42, 82),
        'PD': (92, 86, 80, 90, 40, 78),
        'PE': (92, 86, 80, 90, 40, 78),
    }
    pac, sho, pas, dri, def_, phy = base.get(pos, base['MEI'])

    pac = _clamp(pac + trofeus)
    sho = _clamp(sho + bola_de_ouro * 2)
    pas = _clamp(pas + trofeus)
    dri = _clamp(dri + trofeus)
    def_ = _clamp(def_ + min(3, trofeus))
    phy = _clamp(phy + min(4, trofeus))

    if perna and 'canhoto' in perna.lower():
        dri = _clamp(dri + 2)

    return CartaFutStats(
        overall=overall,
        posicao=pos,
        pac=pac,
        sho=sho,
        pas=pas,
        dri=dri,
        def_=def_,
        phy=phy,
    )


def parse_altura_metros(altura: str) -> Optional[float]:
    if not altura:
        return None
    m = re.search(r'(\d)[,.](\d{2})', altura.replace(',', '.'))
    if m:
        return float(f'{m.group(1)}.{m.group(2)}')
    m = re.search(r'(\d{3})', altura)
    if m:
        return int(m.group(1)) / 100
    return None
