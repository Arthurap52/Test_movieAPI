# Análise e Recomendação de Filmes usando a API TMDB

Este projeto consiste em dois scripts em Python que utilizam a API do The Movie Database (TMDB) para:

1. Analisar dados de filmes e gerar estatísticas
2. Recomendar filmes com base em um filme de entrada

## Pré-requisitos

- Python 3.6 ou superior
- Bibliotecas listadas em `requirements.txt`

## Instalação

1. Clone este repositório:

    ```bash
    git clone https://github.com/seu-usuario/Test_movieAPI.git
    cd Test_movieAPI
    ```

2. Instale as dependências:

    ```bash
    pip install -r requirements.txt
    ```

3. Configure sua própria chave de API:

   -Crie uma conta no [TMDB](https://www.themoviedb.org/)
   -Solicite uma chave de API em suas configurações
   -Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

   ```bash
   TMDB_API_KEY=sua_chave_api_aqui
   ```

## Uso

### Teste 1: Análise de Dados de Filmes

Este script analisa uma lista de filmes e gera estatísticas sobre atores, gêneros e bilheteria.

```bash
python teste_1.py [id1 id2 id3 ...]
```

Onde `id1`, `id2`, etc., são IDs de filmes do TMDB. Se nenhum ID for fornecido, uma lista padrão será usada.

**Exemplo:**

```bash
python teste_1.py 550 680 11 24428 299536
```

**Saída:**
O script exibirá:

- Participação por Ator: quantas vezes cada ator aparece nos filmes analisados
- Frequência de Gêneros: contagem de cada gênero presente nos filmes
- Top 5 Atores com Maior Bilheteria: ranking dos atores com maior faturamento nos filmes

### Teste 2: Sistema de Recomendação de Filmes

Este script recebe um filme como entrada e retorna 5 recomendações baseadas nesse filme.

```bash
# Usando o título do filme
python teste_2.py "Nome do Filme"

# Usando o ID do TMDB
python teste_2.py --id 550
```

**Exemplos:**

```bash
python teste_2.py "Clube da Luta"
python teste_2.py --id 550
```

**Saída:**
O script exibirá uma lista de até 5 filmes recomendados com base no filme escolhido, incluindo título, ano de lançamento, avaliação e uma breve descrição.

## Estrutura do Projeto

- `teste_1.py`: Análise de dados de filmes
- `teste_2.py`: Sistema de recomendação de filmes
- `tmdb_api.py`: Módulo de interface com a API do TMDB
- `requirements.txt`: Dependências do projeto
- `README.md`: Este arquivo

## Explicação dos Critérios de Recomendação

Para o sistema de recomendação (teste_2.py), são utilizados dois critérios principais:

1. **Recomendações diretas da API**: O TMDB possui um algoritmo próprio que considera fatores como gênero, equipe de produção, palavras-chave e popularidade.

2. **Filmes similares**: Como complemento, usamos filmes similares em caso de poucas recomendações diretas, que são calculados com base em metadados como gênero, palavras-chave e popularidade.

## Limitações

- A API TMDB tem limites de taxa de requisições (rate limits)
- Algumas informações podem estar incompletas ou ausentes na base de dados do TMDB
