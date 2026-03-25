# Weaviate Examples

> **Nota:** Este é um projeto de estudo. Os exercícios aqui descritos têm fins educacionais.

## O que é o Weaviate?

Weaviate é um banco de dados vetorial open-source **orientado a objetos e schema**. Diferente de outros vetoriais, ele armazena objetos completos (não apenas vetores e IDs), suporta consultas via **GraphQL e REST**, possui módulos integrados de embedding (textos, imagens) e oferece funcionalidades como busca híbrida (vetorial + BM25).

## Quando usar o Weaviate?

- Você precisa de busca semântica rica com schema bem definido.
- Quer usar busca híbrida (semântica + keyword) nativamente.
- Seu caso de uso envolve dados **multimodais** (textos e imagens juntos).
- Prefere GraphQL como interface de consulta.
- Quer integração nativa com modelos de embedding sem código extra (via módulos).

## Pré-requisitos

- Docker (para rodar o Weaviate localmente)
- Python 3.11+
- Biblioteca: `weaviate-client`

```bash
pip install weaviate-client
```

## Subindo o ambiente com Docker

```bash
docker run -d \
  --name weaviate \
  -p 8080:8080 \
  -e QUERY_DEFAULTS_LIMIT=25 \
  -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true \
  -e PERSISTENCE_DATA_PATH=/var/lib/weaviate \
  -e DEFAULT_VECTORIZER_MODULE=none \
  -e ENABLE_MODULES="" \
  cr.weaviate.io/semitechnologies/weaviate:latest
```

## Conceitos-chave

| Conceito   | Equivalente SQL | Descrição                                                             |
|------------|-----------------|-----------------------------------------------------------------------|
| Class      | Tabela          | Define o schema de um tipo de objeto (nome, propriedades, vectorizer) |
| Object     | Linha           | Uma instância da classe, com propriedades e vetor associado           |
| Property   | Coluna          | Campo de dados de um objeto (text, int, boolean, etc.)                |
| Tenant     | Schema/partição | Isolamento de dados por cliente (multi-tenancy)                       |
| Module     | Plugin          | Integração com modelos de embedding (text2vec, img2vec, etc.)         |

## Caminho de exercícios

### Exercício 1 — Configuração e criação de schema

**Objetivo:** conectar ao Weaviate e definir uma classe com schema.

**Tarefas:**
- [ ] Conectar ao Weaviate com `weaviate.connect_to_local()`
- [ ] Criar uma classe `Document` com propriedades `title` (text) e `content` (text)
- [ ] Verificar o schema criado via API REST (`GET /v1/schema`)
- [ ] Deletar e recriar a classe para praticar o gerenciamento de schema

**Exemplo:**
```python
import weaviate
import weaviate.classes as wvc

client = weaviate.connect_to_local()
client.collections.create(
    name="Document",
    properties=[
        wvc.config.Property(name="title", data_type=wvc.config.DataType.TEXT),
        wvc.config.Property(name="content", data_type=wvc.config.DataType.TEXT),
    ]
)
```

---

### Exercício 2 — Inserindo objetos com vetores externos

**Objetivo:** inserir objetos com embeddings gerados externamente.

**Tarefas:**
- [ ] Gerar embeddings com `sentence-transformers`
- [ ] Inserir objetos na coleção usando `collection.data.insert()` com vetor explícito
- [ ] Verificar os objetos inseridos com `collection.query.fetch_objects()`
- [ ] Usar `insert_many()` para inserção em lote

---

### Exercício 3 — Busca vetorial (near_vector / near_text)

**Objetivo:** consultar objetos por similaridade.

**Tarefas:**
- [ ] Buscar objetos similares usando `near_vector` (vetor explícito da query)
- [ ] Se usar módulo `text2vec`, experimentar `near_text` (texto direto como query)
- [ ] Limitar o número de resultados e acessar os scores de distância
- [ ] Filtrar propriedades retornadas com `return_properties`

---

### Exercício 4 — Busca híbrida (híbrida = vetorial + BM25)

**Objetivo:** explorar a busca híbrida, um diferencial do Weaviate.

**Tarefas:**
- [ ] Executar uma busca híbrida com `collection.query.hybrid(query="...", alpha=0.5)`
- [ ] Ajustar o parâmetro `alpha` (0 = BM25 puro, 1 = vetorial puro) e observar as diferenças
- [ ] Comparar resultados da busca híbrida com busca puramente vetorial
- [ ] Entender quando a busca híbrida supera cada abordagem isolada

---

### Exercício 5 — Filtros e operadores

**Objetivo:** combinar busca vetorial com filtros sobre propriedades dos objetos.

**Tarefas:**
- [ ] Adicionar propriedade `category` (text) e `published` (boolean) nos objetos
- [ ] Usar `filters=Filter.by_property("category").equal("technology")` na query
- [ ] Combinar múltiplos filtros com `Filter.all_of([...])` e `Filter.any_of([...])`
- [ ] Comparar a abordagem de filtro com a do pgvector

---

### Exercício 6 — Agrupamento e agregação

**Objetivo:** usar as capacidades analíticas do Weaviate.

**Tarefas:**
- [ ] Contar objetos por categoria com `collection.aggregate.over_all()`
- [ ] Calcular média de uma propriedade numérica
- [ ] Usar `group_by` para agregar resultados por campo
- [ ] Entender as limitações das agregações em bancos vetoriais

---

### Exercício 7 — Integração com LLM (RAG com Weaviate)

**Objetivo:** construir um pipeline RAG usando os módulos generativos do Weaviate.

**Tarefas:**
- [ ] Configurar o módulo `generative-openai` ou `generative-cohere` no Weaviate
- [ ] Usar `collection.query.near_text(..., generate=...)` para RAG direto na query
- [ ] Comparar a abordagem nativa do Weaviate com a montagem manual do prompt
- [ ] Avaliar prós e contras de delegar a geração ao banco de dados

## Referências

- Documentação oficial: https://weaviate.io/developers/weaviate
- Quickstart: https://weaviate.io/developers/weaviate/quickstart
- SDK Python v4: https://weaviate.io/developers/weaviate/client-libraries/python
- Docker Compose examples: https://github.com/weaviate/weaviate-examples