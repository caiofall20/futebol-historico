from django import template

register = template.Library()

# Mapeamento de nacionalidades para códigos de bandeira (flag-icon-css)
# Baseado em nomes comuns e variações
NATIONALITY_TO_FLAG = {
    # América do Sul
    'brasil': 'br',
    'brazil': 'br',
    'argentina': 'ar',
    'uruguai': 'uy',
    'uruguay': 'uy',
    'paraguai': 'py',
    'paraguay': 'py',
    'chile': 'cl',
    'colombia': 'co',
    'equador': 'ec',
    'ecuador': 'ec',
    'peru': 'pe',
    'venezuela': 've',
    'bolivia': 'bo',
    
    # Europa
    'italia': 'it',
    'italy': 'it',
    'itália': 'it',
    'franca': 'fr',
    'france': 'fr',
    'frança': 'fr',
    'espanha': 'es',
    'spain': 'es',
    'alemanha': 'de',
    'germany': 'de',
    'holanda': 'nl',
    'netherlands': 'nl',
    'países baixos': 'nl',
    'inglaterra': 'gb',
    'england': 'gb',
    'portugal': 'pt',
    'belgica': 'be',
    'belgium': 'be',
    'bélgica': 'be',
    'croacia': 'hr',
    'croatia': 'hr',
    'croácia': 'hr',
    'republica tcheca': 'cz',
    'república tcheca': 'cz',
    'czech republic': 'cz',
    'tchequia': 'cz',
    'polonia': 'pl',
    'poland': 'pl',
    'polônia': 'pl',
    'russia': 'ru',
    'rússia': 'ru',
    'russia': 'ru',
    'grecia': 'gr',
    'greece': 'gr',
    'grécia': 'gr',
    'turquia': 'tr',
    'turkey': 'tr',
    'suecia': 'se',
    'sweden': 'se',
    'suécia': 'se',
    'dinamarca': 'dk',
    'denmark': 'dk',
    'noruega': 'no',
    'norway': 'no',
    'finlandia': 'fi',
    'finland': 'fi',
    'finlândia': 'fi',
    'suica': 'ch',
    'switzerland': 'ch',
    'suíça': 'ch',
    'austria': 'at',
    'áustria': 'at',
    'irlanda': 'ie',
    'ireland': 'ie',
    'escocia': 'gb-sct',
    'scotland': 'gb-sct',
    'escócia': 'gb-sct',
    'gales': 'gb-wls',
    'wales': 'gb-wls',
    'país de gales': 'gb-wls',
    'pais de gales': 'gb-wls',
    
    # África
    'camaroes': 'cm',
    'camarões': 'cm',
    'cameroon': 'cm',
    'costa do marfim': 'ci',
    'ivory coast': 'ci',
    'côte d\'ivoire': 'ci',
    'nigeria': 'ng',
    'nigéria': 'ng',
    'senegal': 'sn',
    'senegal': 'sn',
    'ghana': 'gh',
    'egito': 'eg',
    'egypt': 'eg',
    'egito': 'eg',
    'marrocos': 'ma',
    'morocco': 'ma',
    'argelia': 'dz',
    'algeria': 'dz',
    'argélia': 'dz',
    'tunisia': 'tn',
    'tunísia': 'tn',
    'africa do sul': 'za',
    'south africa': 'za',
    'áfrica do sul': 'za',
    
    # Ásia
    'japao': 'jp',
    'japão': 'jp',
    'japan': 'jp',
    'coreia do sul': 'kr',
    'south korea': 'kr',
    'coréia do sul': 'kr',
    'coreia do norte': 'kp',
    'north korea': 'kp',
    'coréia do norte': 'kp',
    'china': 'cn',
    'índia': 'in',
    'india': 'in',
    'ira': 'ir',
    'iran': 'ir',
    'ira': 'ir',
    'arabia saudita': 'sa',
    'saudi arabia': 'sa',
    'arábia saudita': 'sa',
    'catar': 'qa',
    'qatar': 'qa',
    'catar': 'qa',
    'emirates': 'ae',
    'emirados árabes': 'ae',
    'united arab emirates': 'ae',
    'australia': 'au',
    'austrália': 'au',
    
    # América do Norte e Central
    'estados unidos': 'us',
    'united states': 'us',
    'usa': 'us',
    'mexico': 'mx',
    'méxico': 'mx',
    'canada': 'ca',
    'canadá': 'ca',
    'costa rica': 'cr',
    'panama': 'pa',
    'panamá': 'pa',
    'jamaica': 'jm',
    'trinidad e tobago': 'tt',
    'trinidad and tobago': 'tt',
}

def normalize_nationality(nacionalidade):
    """Normaliza o nome da nacionalidade para busca no mapeamento"""
    if not nacionalidade:
        return None
    
    # Converter para minúsculas e remover espaços extras
    normalized = nacionalidade.lower().strip()
    
    # Remover acentos comuns (simplificado)
    replacements = {
        'á': 'a', 'à': 'a', 'â': 'a', 'ã': 'a',
        'é': 'e', 'è': 'e', 'ê': 'e',
        'í': 'i', 'ì': 'i', 'î': 'i',
        'ó': 'o', 'ò': 'o', 'ô': 'o', 'õ': 'o',
        'ú': 'u', 'ù': 'u', 'û': 'u',
        'ç': 'c',
    }
    
    for old, new in replacements.items():
        normalized = normalized.replace(old, new)
    
    return normalized

def get_flag_code(nacionalidade):
    """
    Retorna o código da bandeira para uma nacionalidade.
    """
    if not nacionalidade:
        return None
    
    normalized = normalize_nationality(nacionalidade)
    
    # Buscar correspondência exata primeiro
    if normalized in NATIONALITY_TO_FLAG:
        return NATIONALITY_TO_FLAG[normalized]
    
    # Buscar correspondência parcial (palavras-chave)
    # Ordenar por tamanho da chave (maior primeiro) para pegar correspondências mais específicas
    sorted_keys = sorted(NATIONALITY_TO_FLAG.keys(), key=len, reverse=True)
    
    for key in sorted_keys:
        # Verificar se a chave está contida na nacionalidade normalizada
        if key in normalized:
            return NATIONALITY_TO_FLAG[key]
        # Verificar se a nacionalidade está contida na chave (para casos como "República Tcheca")
        if normalized in key:
            return NATIONALITY_TO_FLAG[key]
    
    # Tentar buscar por palavras individuais (útil para "País de Gales", "Costa do Marfim", etc)
    words = normalized.split()
    for word in words:
        if word in NATIONALITY_TO_FLAG:
            return NATIONALITY_TO_FLAG[word]
        # Buscar parcialmente
        for key in sorted_keys:
            if word in key or key in word:
                return NATIONALITY_TO_FLAG[key]
    
    # Se não encontrou, retornar None (será usado fallback)
    return None

@register.filter
def flag_code(nacionalidade):
    """
    Retorna o código da bandeira para uma nacionalidade.
    Uso: {{ jogador.nacionalidade|flag_code }}
    """
    return get_flag_code(nacionalidade)

