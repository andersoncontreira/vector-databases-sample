# Qdrant Examples

> **Nota:** Este é um projeto de estudo. Os exercícios aqui descritos têm fins educacionais.

## O que é o Qdrant?

Qdrant (pronuncia-se "quadrant") é um banco de dados vetorial open-source de alta performance, escrito em **Rust**. Oferece API REST e gRPC, suporte a filtragem avançada de metadados, múltiplos vetores por ponto e é conhecido por ser uma das opções mais rápidas disponíveis. Pode ser usado localmente, via Docker ou como serviço gerenciado na Qdrant Cloud.

## Quando usar o Qdrant?

- Você precisa de **alta performance** e baixa latência em buscas vetoriais.
- Seu caso de uso exige **filtros complexos sobre metadados** combinados com busca vetorial.
- Quer rodar localmente com Docker sem depender de cloud.
- Precisa armazenar **múltiplos vetores por objeto** (ex: embedding de título + embedding de corpo).
- Quer uma solução com API bem documentada e cliente oficial para Python.

## Pré-requisitos

- Docker (para rodar o Qdrant localmente)
- Python 3.11+
- Biblioteca: `qdrant-client`, `sentence-transformers`

```bash
pip install qdrant-client sentence-transformers
```

## Subindo o ambiente com Docker

```bash
docker run -d \
  --name qdrant \
  -p 6333:6333 \
  -p 6334:6334 \
  -v $(pwd)/qdrant_storage:/qdrant/storage \
  qdrant/qdrant
```

- Porta `6333`: REST API + Web UI (`http://localhost:6333/dashboard`)
- Porta `6334`: gRPC

## Conceitos-chave

| Conceito    | Equivalente SQL | Descrição                                                              |
|-------------|-----------------|------------------------------------------------------------------------|
| Collection  | Tabela          | Agrupa pontos com a mesma configuração de vetor                        |
| Point       | Linha           | Um vetor com ID, payload e vetor(es) associado(s)                      |
| Payload     | Colunas extras  | Dados JSON arbitrários associados ao ponto, usados para filtragem      |
| Vector      | —               | O embedding numérico do ponto (pode haver múltiplos por ponto)         |
| Segment     | Partição interna| Divisão interna da coleção para otimização de I/O                      |

## Caminho de exercícios

### Exercício 1 — Configuração e criação de coleção

**Objetivo:** conectar ao Qdrant e criar a primeira coleção.

**Tarefas:**
- [ ] Conectar com `QdrantClient(host="localhost", port=6333)`
- [ ] Criar uma coleção com `vectors_config=VectorParams(size=384, distance=Distance.COSINE)`
- [ ] Listar coleções existentes com `client.get_collections()`
- [ ] Acessar a Web UI em `http://localhost:6333/dashboard` e visualizar a coleção

**Exemplo:**
```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

client = QdrantClient(host="localhost", port=6333)
client.create_collection(
    collection_name="documents",
    vectors_config=VectorParams(size=384, distance=Distance.COSINE),
)
```

---

### Exercício 2 — Inserindo pontos (upsert)

**Objetivo:** gerar embeddings e inserir pontos com payload no Qdrant.

**Tarefas:**
- [ ] Gerar embeddings com `sentence-transformers`
- [ ] Inserir pontos com `client.upsert()` incluindo payload rico (ex: `{"text": "...", "category": "...", "score": 4.5}`)
- [ ] Usar IDs numéricos e UUIDs — entender as diferenças
- [ ] Inserir em lote usando uma lista de `PointStruct`

---

### Exercício 3 — Busca por similaridade

**Objetivo:** executar buscas vetoriais e interpretar os resultados.

**Tarefas:**
- [ ] Gerar o embedding da query e executar `client.search()`
- [ ] Controlar o número de resultados com `limit`
- [ ] Acessar o `score` e o `payload` de cada resultado
- [ ] Comparar distâncias: `COSINE`, `EUCLID` e `DOT`

**Exemplo:**
```python
results = client.search(
    collection_name="documents",
    query_vector=query_embedding,
    limit=5,
)
for r in results:
    print(r.score, r.payload)
```

---

### Exercício 4 — Filtragem avançada com payload

**Objetivo:** explorar o sistema de filtros do Qdrant, um de seus maiores diferenciais.

**Tarefas:**
- [ ] Filtrar por igualdade: `FieldCondition(key="category", match=MatchValue(value="tech"))`
- [ ] Filtrar por intervalo numérico: `FieldCondition(key="score", range=Range(gte=4.0))`
- [ ] Combinar filtros com `Filter(must=[...])`, `Filter(should=[...])`, `Filter(must_not=[...])`
- [ ] Criar índice de payload para melhorar a performance dos filtros

---

### Exercício 5 — Indexação e otimização

**Objetivo:** entender como o Qdrant indexa vetores e como otimizar a performance.

**Tarefas:**
- [ ] Criar índice HNSW e ajustar os parâmetros `m` e `ef_construct`
- [ ] Criar índice de payload para campos usados em filtros frequentes
- [ ] Usar `client.optimize_collection()` e verificar o impacto
- [ ] Comparar tempo de busca com e sem índice em uma coleção maior

---

### Exercício 6 — Múltiplos vetores por ponto

**Objetivo:** explorar o suporte a múltiplos vetores, exclusividade do Qdrant.

**Tarefas:**
- [ ] Criar uma coleção com dois vetores nomeados: `"title"` e `"body"` (dimensões diferentes)
- [ ] Inserir pontos com ambos os vetores
- [ ] Executar busca usando apenas um dos vetores nomeados
- [ ] Entender casos de uso: busca por título vs. busca por conteúdo completo

---

### Exercício 7 — Integração com LLM (RAG com Qdrant)

**Objetivo:** construir um pipeline RAG usando o Qdrant como retriever.

**Tarefas:**
- [ ] Indexar um conjunto de documentos com embeddings e payload completo
- [ ] Implementar retrieval com filtro por contexto (ex: apenas documentos de uma categoria)
- [ ] Montar o prompt com os trechos recuperados e enviar para uma LLM
- [ ] Comparar a qualidade do retrieval com e sem filtros de payload

---

### Exercício 8 — Scroll, contagem e deleção

**Objetivo:** dominar as operações de gerenciamento de dados no Qdrant.

**Tarefas:**
- [ ] Usar `client.scroll()` para paginar todos os pontos de uma coleção
- [ ] Contar pontos com `client.count()`
- [ ] Deletar pontos por ID e por filtro de payload
- [ ] Limpar e recriar a coleção para um novo ciclo de testes

## Referências

- Documentação oficial: https://qdrant.tech/documentation
- Quickstart: https://qdrant.tech/documentation/quickstart
- SDK Python: https://github.com/qdrant/qdrant-client
- Web UI: `http://localhost:6333/dashboard` (após subir o Docker)