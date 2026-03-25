# pgvector Examples

> **Nota:** Este é um projeto de estudo. Os exercícios aqui descritos têm fins educacionais.

## O que é o pgvector?

`pgvector` é uma extensão open-source para o **PostgreSQL** que adiciona suporte nativo a vetores e busca por similaridade. Diferente de soluções dedicadas, ele permite combinar dados relacionais convencionais com busca vetorial dentro do mesmo banco de dados, sem precisar de infraestrutura adicional.

## Quando usar o pgvector?

- Você já usa PostgreSQL e quer adicionar busca semântica sem introduzir um novo serviço.
- Precisa combinar queries SQL tradicionais com busca vetorial (ex: filtrar por categoria E buscar por similaridade).
- O volume de vetores é moderado (até dezenas de milhões de registros com tuning adequado).
- Quer manter simplicidade operacional — um único banco para tudo.

## Pré-requisitos

- Docker (para subir o PostgreSQL com a extensão pgvector)
- Python 3.11+
- Bibliotecas: `psycopg2`, `pgvector`, `sentence-transformers`

```bash
pip install psycopg2-binary pgvector sentence-transformers
```

## Subindo o ambiente com Docker

```bash
docker run -d \
  --name pgvector-db \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  pgvector/pgvector:pg16
```

## Caminho de exercícios

### Exercício 1 — Configuração inicial

**Objetivo:** conectar ao PostgreSQL, habilitar a extensão e criar a primeira tabela vetorial.

**Tarefas:**
- [ ] Conectar ao banco via `psycopg2`
- [ ] Executar `CREATE EXTENSION IF NOT EXISTS vector`
- [ ] Criar uma tabela com uma coluna do tipo `vector(384)` (384 dimensões, padrão do `all-MiniLM-L6-v2`)
- [ ] Verificar que a extensão está ativa

**Exemplo de schema:**
```sql
CREATE TABLE documents (
    id      SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    embedding vector(384)
);
```

---

### Exercício 2 — Inserindo embeddings

**Objetivo:** gerar embeddings com `sentence-transformers` e inserir no PostgreSQL.

**Tarefas:**
- [ ] Carregar o modelo `all-MiniLM-L6-v2`
- [ ] Gerar embeddings para uma lista de frases
- [ ] Inserir os registros na tabela com `INSERT INTO documents (content, embedding) VALUES (%s, %s)`
- [ ] Verificar os dados inseridos com um `SELECT`

---

### Exercício 3 — Busca por similaridade

**Objetivo:** consultar os documentos mais similares a um texto de entrada.

**Tarefas:**
- [ ] Gerar o embedding do texto de consulta
- [ ] Usar o operador `<->` (distância L2) para busca por similaridade
- [ ] Retornar os `N` documentos mais próximos
- [ ] Experimentar também os operadores `<#>` (produto interno) e `<=>` (cosseno)

**Exemplo de query:**
```sql
SELECT id, content, embedding <-> %s AS distance
FROM documents
ORDER BY distance
LIMIT 5;
```

---

### Exercício 4 — Indexação com HNSW

**Objetivo:** melhorar a performance de busca com índice HNSW (Hierarchical Navigable Small World).

**Tarefas:**
- [ ] Criar um índice HNSW na coluna `embedding`
- [ ] Comparar o tempo de busca com e sem índice
- [ ] Entender os parâmetros `m` e `ef_construction`

**Exemplo:**
```sql
CREATE INDEX ON documents USING hnsw (embedding vector_cosine_ops);
```

---

### Exercício 5 — Combinando SQL com busca vetorial

**Objetivo:** demonstrar a principal vantagem do pgvector: filtros relacionais + similaridade vetorial.

**Tarefas:**
- [ ] Adicionar colunas de metadados à tabela (ex: `category TEXT`, `created_at TIMESTAMP`)
- [ ] Criar query que filtra por categoria E ordena por similaridade vetorial
- [ ] Comparar com a abordagem de pós-filtro (buscar por vetor e depois filtrar)

**Exemplo:**
```sql
SELECT id, content, embedding <=> %s AS distance
FROM documents
WHERE category = 'technology'
ORDER BY distance
LIMIT 5;
```

---

### Exercício 6 — Integração com LLM (RAG simples)

**Objetivo:** construir um pipeline RAG básico usando pgvector como retriever.

**Tarefas:**
- [ ] Indexar um conjunto de documentos maiores (ex: parágrafos de um texto)
- [ ] Dado uma pergunta do usuário, buscar os trechos mais relevantes
- [ ] Montar um prompt com o contexto recuperado e enviar para uma LLM
- [ ] Avaliar a qualidade das respostas com e sem contexto

## Referências

- Repositório oficial: https://github.com/pgvector/pgvector
- Imagem Docker: https://hub.docker.com/r/pgvector/pgvector
- Documentação do operador de distância: https://github.com/pgvector/pgvector#querying