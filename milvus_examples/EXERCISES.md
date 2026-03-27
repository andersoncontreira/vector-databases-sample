# Exercícios — Milvus

> Sugestões de exercícios para aprofundar os conceitos do Milvus, organizados por nível de complexidade.

---

## Nível 1 — Fundamentos

### Exercício 1.1 — Milvus Lite local
Crie um `MilvusClient` com `uri="./milvus_study.db"`. Crie uma coleção, insira 10 entidades e execute uma busca. Confirme que o arquivo `.db` foi criado em disco.

### Exercício 1.2 — Schema automático vs explícito
Crie duas coleções: uma com schema automático (`dimension=384`) e outra com schema explícito definindo cada campo. Compare a flexibilidade e as limitações de cada abordagem.

### Exercício 1.3 — Lifecycle: load e release
Após criar o índice, experimente fazer `search` antes e depois de `load_collection`. Observe o erro sem o load. Depois faça `release_collection` e tente buscar novamente.

### Exercício 1.4 — Listar e descrever
Use `client.list_collections()`, `client.describe_collection()` e `client.get_collection_stats()` para inspecionar as coleções. Entenda cada campo retornado.

---

## Nível 2 — Inserção e busca

### Exercício 2.1 — Indexar países
Gere embeddings dos arquivos `data/texts/*.txt` com `sentence-transformers`. Insira os chunks no Milvus com payload rico (`text`, `source`, `country`). Execute queries sobre os dados indexados.

### Exercício 2.2 — output_fields
Execute `client.search()` com `output_fields=["text", "country"]` e sem `output_fields`. Compare as respostas e entenda o impacto de retornar campos extras no tempo de resposta.

### Exercício 2.3 — Upsert vs insert
Insira a mesma entidade duas vezes com `insert()` (observe IDs duplicados) e depois com `upsert()` (atualiza o existente). Verifique a contagem antes e depois de cada operação.

### Exercício 2.4 — Métricas de distância
Crie coleções com `COSINE`, `L2` e `IP`. Insira os mesmos vetores e compare os scores retornados. Entenda quando usar cada métrica.

---

## Nível 3 — Índices e performance

### Exercício 3.1 — Comparar tipos de índice
Crie quatro coleções idênticas com índices `FLAT`, `IVF_FLAT`, `HNSW` e `IVF_SQ8`. Para cada uma, meça:
- Tempo de criação do índice
- Tempo de busca top-10
- Tamanho em disco

### Exercício 3.2 — Parâmetros do HNSW
Varie `M` (8, 16, 32) e `efConstruction` (64, 128). Use `ef` no `search_params` para ajustar o recall em tempo de query. Tabele os resultados.

### Exercício 3.3 — IVF: nlist e nprobe
Crie um índice `IVF_FLAT` com `nlist=50`. Durante a busca, varie `nprobe` de 1 a 50 e meça o impacto no tempo de resposta e no recall comparado a `FLAT`.

---

## Nível 4 — Recursos avançados

### Exercício 4.1 — Filtros escalares
Insira entidades com campos `category` (VARCHAR) e `year` (INT64). Execute buscas combinando vetor com filtros como `'category == "geography" and year >= 2020'`.

### Exercício 4.2 — Partições
Crie partições por continente (`americas`, `europe`, `asia`). Insira países em suas respectivas partições. Execute buscas limitadas a uma ou mais partições com `partition_names`.

### Exercício 4.3 — Múltiplos vetores
Crie uma coleção com dois campos vetoriais: `title_embedding` (dim 384) e `body_embedding` (dim 384). Insira documentos e busque usando cada campo separadamente.

### Exercício 4.4 — Delete e compactação
Insira 10.000 entidades, delete 5.000 por filtro e observe que o espaço não é imediatamente liberado. Execute `client.compact()` e compare o tamanho antes e depois.

---

## Nível 5 — Projetos integradores

### Projeto 5.1 — Pipeline RAG com Milvus Lite
Construa um pipeline RAG completo usando Milvus Lite como vector store. Indexe os PDFs de `data/articles/`, implemente retrieval com filtro por fonte e gere respostas com OpenAI. Compare com o pipeline usando ChromaDB.

### Projeto 5.2 — Integração com LangChain
Use `langchain-milvus` para montar o mesmo pipeline do `langchain_examples/ex05`. Substitua o Pinecone pelo Milvus Lite e valide que os resultados são equivalentes.

### Projeto 5.3 — Benchmark Milvus vs Qdrant
Para datasets de 10K e 100K vetores, compare os dois sistemas em:
- Tempo de inserção em batch
- Tempo de busca com e sem filtro
- Facilidade de filtragem por metadados
- Escalabilidade da configuração local

### Projeto 5.4 — Milvus distribuído (avançado)
Suba o Milvus em modo cluster com Docker Compose. Crie uma coleção com 3 shards. Insira 1 milhão de vetores e observe a distribuição entre os nós via Attu (interface gráfica do Milvus).
