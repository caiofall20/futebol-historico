# Como Adicionar Mais Imagens dos Times

## 📁 Localização da Pasta
```
futebol_historico/blog/static/blog/images/times/
```

## 📋 Métodos para Adicionar Imagens

### Método 1: Adicionar Manualmente na Pasta

1. **Baixe as imagens** dos times (formato: `.jpg`, `.png`, `.webp`)
2. **Coloque na pasta**: `futebol_historico/blog/static/blog/images/times/`
3. **Nomeie os arquivos** seguindo o padrão:
   - `barcelona_2009.jpg`
   - `arsenal_2004.jpg`
   - `flamengo_1981.jpg`
   - etc.

4. **Execute o script**:
   ```bash
   python3 futebol_historico/adicionar_imagens_manuais.py
   ```

### Método 2: Usar URLs do Pinterest

1. **Encontre o pin no Pinterest** (ex: "Porto 2004 team photo")
2. **Copie a URL do pin** (ex: `https://br.pinterest.com/pin/123456789/`)
3. **Adicione no arquivo** `baixar_imagens_pinterest.py`:
   ```python
   'Porto 2004': [
       'https://br.pinterest.com/pin/123456789/',
   ],
   ```
4. **Execute o script**:
   ```bash
   python3 futebol_historico/baixar_imagens_pinterest.py
   ```

### Método 3: Usar o Script Principal

1. **Coloque as imagens na pasta** com os nomes corretos
2. **Execute**:
   ```bash
   python3 futebol_historico/adicionar_imagens_times.py --forcar
   ```

## 📝 Nomes dos Times no Banco

- Ajax 1971-1973
- Ajax 1995
- Arsenal 2004
- Barcelona 2009
- Bayern de Munique 2013
- Bayern de Munique 2020
- Boca Juniors 2000
- Celtic 1967
- Flamengo 1981
- Internazionale 2010
- Manchester United 1999
- Manchester United 2008
- Marseille 1993
- Milan 1989
- Peñarol 1961
- Porto 2004
- Real Madrid 1956-1960
- River Plate 1986
- São Paulo 1992/1993

## 🔍 Verificar Status

Para ver quais times ainda precisam de imagens:
```bash
python3 futebol_historico/listar_times_sem_imagem.py
```

## 💡 Dicas

- Use imagens de **pelo menos 800px de largura**
- Prefira formato **JPG** para fotos
- Nomeie os arquivos de forma clara (ex: `porto_2004.jpg`)
- Se o nome do arquivo não corresponder automaticamente, edite `adicionar_imagens_manuais.py` e adicione no `MANUAL_MAPPING`





