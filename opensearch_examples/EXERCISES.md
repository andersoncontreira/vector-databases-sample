# Exercícios — Amazon OpenSearch (Vector Search)

> Sugestões de exercícios para aprofundar os conceitos de busca vetorial com OpenSearch, organizados por nível de complexidade.

---

## Nível 1 — Fundamentos

### Exercício 1.1 — Criar índice k-NN
Crie um índice com `"index.knn": true` e um campo `embedding` do tipo `knn_vector` com `dimension=384`. Verifique o mapping com `GET /nome-do-indice/_mapping`.

### Exercício 1.2 — Index settings
Explore as configurações do índice com `GET /nome-do-indice/_settings`. Entenda os parâmetros `knn.algo_param.ef_search`, `knn.space_type` e `knn.engine`.

### Exercício 1.3 — CRUD de documentos
Insira um documento com `POST /nome-do-indice/_doc`, recupere-o pelo `_id`, atualize com `POST /nome-do-indice/_update/{id}` e delete com `DELETE /nome-do-indice/_doc/{id}`.

### Exercício 1.4 — Count e stats
Use `GET /nome-do-indice/_count` e `GET /nome-do-indice/_stats` para monitorar o índice. Entenda os campos `_shards`, `docs.count` e `store.size_in_bytes`.

---

## Nível 2 — Busca vetorial

### Exercício 2.1 — k-NN query básica
Indexe os arquivos `data/texts/*.txt` com embeddings de `sentence-transformers`. Execute uma k-NN query e interprete os campos `_score`, `_id` e `_source` da resposta.

### Exercício 2.2 — Comparar space_type
Crie três índices com `space_type` diferente: `cosinesimil`, `l2` e `innerproduct`. Indexe os mesmos documentos e compare os rankings de resultados para a mesma query.

### Exercício 2.3 — Número de resultados
Varie `k` entre 1 e 20 na k-NN query. Observe como o tempo de resposta escala e se há degradação de qualidade com k muito alto.

### Exercício 2.4 — Efficient filter
Use `efficient_filter` na k-NN query para filtrar por `category` antes do ranking vetorial. Compare com um post-filter usando `bool + filter` e analise a diferença no recall.

---

## Nível 3 — Busca híbrida

### Exercício 3.1 — Bool query com boost
Combine k-NN com `match` usando `bool/should` e diferentes valores de `boost`. Ajuste os boosts até encontrar um balanceamento que melhore os resultados em relação a cada abordagem isolada.

### Exercício 3.2 — Search pipeline com normalização
Configure um `search_pipeline` com `normalization-processor` (técnica: `min_max` ou `z_score`) e `combination-processor` (técnica: `arithmetic_mean`). Execute uma hybrid query e observe os scores normalizados.

### Exercício 3.3 — Pesos na combinação
No `combination-processor`, ajuste os pesos da combinação (ex: `[0.3, 0.7]` para BM25 e k-NN). Compare os resultados com pesos iguais `[0.5, 0.5]` para queries de diferentes naturezas.

### Exercício 3.4 — Avaliar hybrid vs puro
Para 20 queries sobre os países, compare os top-5 resultados de: BM25 puro, k-NN puro e hybrid. Identifique casos onde a busca híbrida supera as abordagens individuais.

---

## Nível 4 — Aggregations e análise

### Exercício 4.1 — Terms aggregation
Adicione um campo `continent` (keyword) aos documentos. Use `terms` aggregation para contar documentos por continente nos resultados de uma k-NN query.

### Exercício 4.2 — Range aggregation
Adicione um campo `population` (integer). Use `range` aggregation para agrupar países por faixa de população (< 10M, 10M–100M, > 100M).

### Exercício 4.3 — Highlight
Use o parâmetro `highlight` na busca para destacar os trechos relevantes do campo `content` que contribuíram para o score BM25. Compare com os trechos recuperados pela k-NN.

---

## Nível 5 — AWS e produção

### Exercício 5.1 — OpenSearch Service na AWS
Provisione um domínio OpenSearch Service no console AWS. Configure fine-grained access control com usuário e senha. Conecte via `opensearch-py` e execute os mesmos exercícios do ambiente Docker.

### Exercício 5.2 — Autenticação com IAM
Configure uma IAM role com permissão `es:ESHttpPost` e `es:ESHttpGet`. Use `requests-aws4auth` para assinar as requisições. Verifique que requisições sem assinatura são rejeitadas.

### Exercício 5.3 — Ingestão com ML Commons
Configure o `text_embedding` processor em um ingest pipeline usando um modelo de embedding hospedado no OpenSearch ML Commons. Indexe documentos sem gerar embeddings na aplicação — o OpenSearch fará isso automaticamente.

### Projeto 5.4 — Pipeline RAG com OpenSearch
Construa um pipeline RAG completo com busca híbrida. Indexe os PDFs de `data/articles/`, implemente retrieval com hybrid search e gere respostas com OpenAI. Compare a qualidade das respostas com RAG usando k-NN puro.
