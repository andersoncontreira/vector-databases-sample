# Exercícios — Qdrant

> Sugestões de exercícios para aprofundar os conceitos do Qdrant, organizados por nível de complexidade.

---

## Nível 1 — Fundamentos

### Exercício 1.1 — Web UI
Suba o Qdrant com Docker e acesse `http://localhost:6333/dashboard`. Explore a interface: crie uma coleção manualmente, inspecione os pontos inseridos e execute uma busca visual.

### Exercício 1.2 — Criar coleção com métricas diferentes
Crie três coleções com `Distance.COSINE`, `Distance.EUCLID` e `Distance.DOT`. Insira os mesmos vetores e compare os scores retornados para a mesma query.

### Exercício 1.3 — Fetch por ID
Após o upsert, use `client.retrieve(collection_name, ids=[1, 2])` para recuperar pontos específicos com payload. Verifique os campos retornados.

### Exercício 1.4 — Count e scroll
Use `client.count()` para contar pontos e `client.scroll()` para paginar todos os pontos de uma coleção. Implemente um loop que percorre todos os pontos em páginas de 10.

---

## Nível 2 — Payload e filtragem

### Exercício 2.1 — Filtros básicos
Insira pontos com payload `{"category": "geography", "language": "pt", "year": 2024}`. Execute buscas com filtros:
- `MatchValue` para igualdade
- `Range` para intervalo numérico
- `MatchAny` para lista de valores

### Exercício 2.2 — Filtros compostos
Combine filtros com `must`, `should` e `must_not`. Implemente uma query que retorna documentos de `category = "geography"` OU `year >= 2023`, excluindo `language = "en"`.

### Exercício 2.3 — Índice de payload
Crie um índice de payload sobre o campo `category` com `client.create_payload_index()`. Use `EXPLAIN` (via REST API) para verificar se o índice está sendo usado nas queries filtradas.

### Exercício 2.4 — Busca sem vetor (scroll com filtro)
Use `client.scroll()` com um filtro de payload para recuperar todos os pontos de uma categoria específica sem usar o campo vetorial. Compare com uma busca vetorial na mesma categoria.

---

## Nível 3 — Índices e performance

### Exercício 3.1 — Parâmetros HNSW
Crie coleções com diferentes valores de `m` (8, 16, 32) e `ef_construct` (64, 128). Para cada configuração, meça o tempo de inserção de 10.000 pontos e o recall@10 comparando com busca exata.

### Exercício 3.2 — ef no tempo de busca
Ajuste `search_params=SearchParams(hnsw_ef=50)` e `hnsw_ef=200` na query. Compare latência e recall para cada valor.

### Exercício 3.3 — Quantização escalar
Crie uma coleção com `ScalarQuantization` habilitado. Compare o tamanho em memória (via REST `GET /collections/{name}`) e a latência de busca com a versão sem quantização.

---

## Nível 4 — Recursos avançados

### Exercício 4.1 — Múltiplos vetores
Crie uma coleção com dois vetores nomeados: `"title"` (dim 384) e `"body"` (dim 384). Insira documentos com ambos os vetores. Execute buscas usando cada vetor separadamente e compare os resultados.

### Exercício 4.2 — Busca por vetor esparso (sparse)
Se disponível na sua versão, experimente criar uma coleção com vetor esparso (BM25). Compare a busca esparsa com a busca densa para queries com palavras-chave exatas.

### Exercício 4.3 — Recomendação por exemplos positivos/negativos
Use `client.recommend()` passando IDs de pontos como exemplos positivos e negativos. Implemente um sistema de recomendação de países similares (positivo: Brasil) e dissimilares (negativo: Dinamarca).

### Exercício 4.4 — Upload em batch
Compare o tempo de upsert de 10.000 pontos usando:
- `client.upsert()` com lista completa
- `client.upload_points()` com batch iterator
- `client.upload_collection()` com gerador

---

## Nível 5 — Projetos integradores

### Projeto 5.1 — Motor de busca de países
Indexe os arquivos `data/texts/*.txt` com payload rico (`{"name": "Brasil", "continent": "América do Sul", "language": "pt"}`). Implemente uma CLI que filtra por continente E busca por similaridade semântica.

### Projeto 5.2 — Sistema de deduplicação
Indexe documentos com alguns textos duplicados levemente modificados. Use `client.search()` com threshold de distância para detectar e reportar duplicatas potenciais.

### Projeto 5.3 — API REST com FastAPI + Qdrant
Construa uma API com:
- `POST /index` — indexa um texto com payload
- `POST /search` — busca por similaridade com filtros opcionais de payload
- `DELETE /points/{id}` — remove um ponto por ID
