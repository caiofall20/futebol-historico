# Área de redação — criar jogadores

Interface para jornalistas (`is_staff`) criarem fichas de jogadores com apoio do Wikidata e da Wikipedia.

## Acesso

1. Crie um usuário no Django Admin (`/admin/`) com **Staff status** ativo.
2. Faça login em `/admin/login/`.
3. Abra **`/redacao/`**.

## Fluxo

1. **Novo jogador** — digite o nome (ex.: `Shunsuke Nakamura`) e clique em *Gerar conteúdo*.
2. **Revisar** — confira biografia, carreira, datas, troféus, foto e carta. Edite o que precisar.
3. **Publicar no portal** — o jogador passa a aparecer em `/jogadores/` e na página de detalhe.

## Fontes automáticas

- [Wikidata](https://www.wikidata.org/) — nacionalidade, clubes, altura, posição, datas, foto (Commons)
- [Wikipedia](https://pt.wikipedia.org/) — texto base da biografia (revise antes de publicar)
- **IA (opcional)** — reescreve biografia e carreira com tom jornalístico, **somente** a partir dos fatos acima

Títulos (Champions, Bola de Ouro, Mundial de Clubes) começam em **0** — ajuste na revisão.

## Geração com AJAX

Ao clicar em *Gerar conteúdo*, a página mostra **“Gerando…”** e consulta o servidor a cada 2 segundos. Não é preciso esperar com a aba travada — ao terminar, abre a tela de revisão automaticamente.

## IA é opcional (e pode ser gratuita)

**Sem nenhuma chave de IA**, o fluxo já funciona: Wikidata + Wikipedia + carta gerada. A redação só perde o texto “mais narrativo” — o jornalista edita na revisão.

A API da **OpenAI é paga** por uso (centavos por jogador, conforme o modelo). Não é obrigatória.

### Alternativas gratuitas ou mais baratas

| Opção | Custo | Como usar com este projeto |
|--------|--------|----------------------------|
| **Nenhuma IA** | Grátis | Não configure `OPENAI_API_KEY` |
| **[Groq](https://console.groq.com/)** | Plano gratuito com limite diário | API compatível com OpenAI — veja exemplo abaixo |
| **[Ollama](https://ollama.com/)** (local) | Grátis no seu PC/servidor | Rode `ollama run llama3.2` e aponte `OPENAI_API_BASE` para `http://localhost:11434/v1` |
| **Google Gemini** | Cota gratuita no Google AI Studio | Requer adaptador extra (não configurado por padrão) |

### Exemplo: Groq (grátis para começar)

1. Crie conta em [console.groq.com](https://console.groq.com/) e gere uma API key.
2. No `.env`:

```env
OPENAI_API_KEY=gsk_sua_chave_groq
OPENAI_API_BASE=https://api.groq.com/openai/v1
OPENAI_MODEL=llama-3.3-70b-versatile
CONTENT_LLM_ENABLED=true
```

### Exemplo: OpenAI (paga)

```env
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
OPENAI_API_BASE=https://api.openai.com/v1
CONTENT_LLM_ENABLED=true
```

Para desligar a IA mesmo com chave configurada: `CONTENT_LLM_ENABLED=false`.

## Comandos úteis

```bash
cd futebol_historico
pip install -r ../requirements.txt
python manage.py migrate
python manage.py runserver
```

## Regenerar

Na tela de revisão, use *Gerar de novo* para buscar de novo as fontes (substitui textos e imagens geradas).

**Importante:** use o **nome completo** do jogador. Só "Nakata" pode pegar a pessoa errada no Wikidata; use "Hidetoshi Nakata".

## Editor completo de carta FUT

Na revisão, clique em **Abrir editor completo da carta** (`/redacao/jogadores/<id>/carta/`).

Recursos (inspirado no [FifaRosters Card Creator](https://www.fifarosters.com/create-card)):

- **Estilo da carta:** Ícone/Ouro, TOTY, TOTS, TOTW, Hero, Flashback, etc.
- **Modelo da carta (FIFA 26):** ~98 fundos oficiais importados do FifaRosters (Rare Gold, TOTY, Icon, etc.); atributos renderizados **dentro** da carta, abaixo do nome
- **Importar/atualizar modelos:** na pasta do projeto Django (`futebol_historico/`):

  ```bash
  python3 manage.py importar_assets_fifarosters
  ```

  Os PNGs ficam em `blog/static/blog/card_assets/fifarosters/fifa26/` e o catálogo em `manifest.json`. Use `--no-download` para só regenerar o manifesto sem baixar imagens.

  **Aviso legal:** esses fundos são arte do EA/FifaRosters; use apenas em ambiente interno de redação até validar direitos para produção.
- **Foto:** foto do rascunho, upload ou URL; posição, tamanho, brilho, contraste, P&B
- **Dados:** nome, overall, posição, nacionalidade, clube, liga
- **Atributos:** PAC, SHO, PAS, DRI, DEF, PHY
- **Extras:** skill, pé fraco, workrate, química
- **Salvar:** gera PNG em alta resolução e volta à revisão

O design fica salvo em `carta_design` no banco para reeditar depois.

## Campos vazios?

Se nacionalidade ou datas aparecerem como "Desconhecida" ou 1900/2000:

1. Confira o bloco **Dados do jogador (gerados)** no topo da revisão
2. Preencha manualmente ou regenere com o nome completo
3. O aviso amarelo indica dados incompletos do Wikidata
