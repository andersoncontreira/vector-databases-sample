# Exercícios — pgvector

> Sugestões de exercícios para aprofundar os conceitos do pgvector, organizados por nível de complexidade.

---

## Nível 1 — Fundamentos

### Exercício 1.1 — Habilitar a extensão
Conecte ao PostgreSQL via `psycopg2`, habilite `vector` com `CREATE EXTENSION IF NOT EXISTS vector` e confirme com `SELECT * FROM pg_extension WHERE extname = 'vector'`.

### Exercício 1.2 — Criar tabela vetorial
Crie uma tabela `documents` com colunas `id SERIAL PRIMARY KEY`, `content TEXT`, `source VARCHAR(255)` e `embedding vector(384)`. Verifique o schema com `\d documents` via psql.

### Exercício 1.3 — Insert vs Upsert
Insira o mesmo documento duas vezes com `INSERT` (observe o erro de chave duplicada) e depois com `INSERT ... ON CONFLICT DO UPDATE` (upsert). Verifique a diferença de comportamento.

### Exercício 1.4 — Operadores de distância
Insira 5 documentos manualmente (com vetores fictícios de dimensão 3 para teste). Execute queries com os três operadores e compare os rankings:
- `<->` distância L2
- `<=>` distância cosseno
- `<#>` produto interno negativo

---

## Nível 2 — Embeddings e busca

### Exercício 2.1 — Indexar países
Use `sentence-transformers` com `all-MiniLM-L6-v2` para gerar embeddings dos arquivos `data/texts/*.txt`. Insira os chunks no PostgreSQL e faça queries como "Qual é a capital da França?".

### Exercício 2.2 — Retornar distância na query
Modifique a query de busca para retornar também a distância junto com o conteúdo:
```sql
SELECT content, embedding <=> %s AS distance FROM documents ORDER BY distance LIMIT 5;
```
Interprete os valores: distância cosseno próxima de 0 significa alta similaridade.

### Exercício 2.3 — Threshold de similaridade
Adicione um filtro `HAVING distance < 0.5` para retornar apenas resultados acima de um threshold de similaridade. Ajuste o valor e observe como a quantidade de resultados varia.

### Exercício 2.4 — Busca com múltiplos documentos de query
Gere embeddings para 3 queries diferentes de uma vez e use uma única chamada ao banco (via `executemany` ou batch) para recuperar os documentos mais similares de cada uma.

---

## Nível 3 — Índices e performance

### Exercício 3.1 — HNSW vs IVFFlat
Crie dois índices sobre a coluna `embedding`:
```sql
CREATE INDEX ON documents USING hnsw (embedding vector_cosine_ops);
CREATE INDEX ON documents USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
```
Use `EXPLAIN ANALYZE` para comparar os planos de execução com e sem índice.

### Exercício 3.2 — Parâmetros do HNSW
Experimente `m` (conexões por nó: 8, 16, 32) e `ef_construction` (64, 128, 256) ao criar o índice HNSW. Use `pg_stat_user_indexes` para monitorar o tamanho do índice.

### Exercício 3.3 — ef_search em runtime
Ajuste `SET hnsw.ef_search = 100` antes de executar queries e compare com o valor padrão (40). Meça o impacto no tempo de busca e no recall.

### Exercício 3.4 — Índice de payload
Adicione uma coluna `category VARCHAR(50)` e crie um índice B-tree sobre ela. Use `EXPLAIN ANALYZE` para confirmar que o índice é usado em queries com filtro por categoria.

---

## Nível 4 — SQL + vetorial

### Exercício 4.1 — Filtro relacional + similaridade
Adicione colunas `country VARCHAR(100)` e `language VARCHAR(10)` à tabela. Faça uma query que filtra por `language = 'pt'` E ordena por distância vetorial. Este é o principal diferencial do pgvector.

### Exercício 4.2 — Aggregations sobre resultados vetoriais
Crie uma query que busca os 20 documentos mais similares a uma query e depois agrupa por `category`, contando quantos documentos de cada categoria foram recuperados.

### Exercício 4.3 — JOIN com outra tabela
Crie uma tabela `sources` com `id` e `url`. Faça um JOIN entre `documents` e `sources` na query de similaridade para retornar também a URL de origem de cada resultado.

### Exercício 4.4 — Full-text + vetorial
Use `tsvector` e `tsquery` do PostgreSQL para combinar busca full-text com busca vetorial em uma única query usando `AND` ou `OR`. Compare os resultados com cada abordagem isolada.

---

## Nível 5 — Projetos integradores

### Projeto 5.1 — Pipeline RAG com PostgreSQL
Construa um pipeline RAG completo onde o PostgreSQL com pgvector é o retriever. Indexe os PDFs de `data/articles/`, faça retrieval com filtro por fonte e gere respostas com a OpenAI.

### Projeto 5.2 — Migração ChromaDB → pgvector
Exporte todos os documentos e embeddings de uma coleção ChromaDB e importe no PostgreSQL. Valide que os resultados de busca são equivalentes nos dois sistemas.

### Projeto 5.3 — API com FastAPI + pgvector
Construa uma API REST com FastAPI e dois endpoints:
- `POST /documents` — recebe texto, gera embedding e insere no PostgreSQL
- `GET /search?q=...` — recebe query, gera embedding e retorna os 5 documentos mais similares

Use `asyncpg` para conexões assíncronas.
