# Amazon OpenSearch (Vector Search) Examples

> **Nota:** Este é um projeto de estudo. Os exercícios aqui descritos têm fins educacionais, baseados em cenários reais de uso do OpenSearch com busca vetorial.

## O que é o OpenSearch?

Amazon OpenSearch Service é um serviço gerenciado baseado no **OpenSearch** (fork open-source do Elasticsearch). Além de buscas full-text tradicionais, suporta **busca vetorial por similaridade** via o engine k-NN (k-Nearest Neighbors), tornando-o uma solução híbrida que combina busca clássica e semântica em um único serviço.

Pode ser usado como serviço gerenciado na AWS (Amazon OpenSearch Service) ou self-hosted via Docker.

## Quando usar o OpenSearch para busca vetorial?

- Você já usa OpenSearch/Elasticsearch para busca full-text e quer adicionar busca semântica sem introduzir um novo serviço.
- Seu caso de uso exige **busca híbrida** (keyword + semântica) com scoring combinado.
- Precisa de **análise de logs e dados + busca vetorial** no mesmo cluster.
- Está em um ambiente AWS e já tem OpenSearch Service provisionado.
- Precisa de funcionalidades avançadas de busca (facets, highlight, aggregations) junto com similaridade vetorial.
- O time já tem familiaridade com a API do Elasticsearch/OpenSearch.

## Pré-requisitos

- Docker (para rodar OpenSearch localmente)
- Python 3.11+
- Bibliotecas: `opensearch-py`, `sentence-transformers`

```bash
pip install opensearch-py sentence-transformers
```

## Subindo o ambiente com Docker

```bash
docker run -d \
  --name opensearch \
  -p 9200:9200 \
  -p 9600:9600 \
  -e "discovery.type=single-node" \
  -e "OPENSEARCH_INITIAL_ADMIN_PASSWORD=Admin@1234!" \
  opensearchproject/opensearch:latest
```

Verificar se está rodando:
```bash
curl -ku admin:Admin@1234! https://localhost:9200
```

## Conceitos-chave

| Conceito    | Equivalente SQL     | Descrição                                                                   |
|-------------|---------------------|-----------------------------------------------------------------------------|
| Index       | Tabela              | Agrupa documentos com o mesmo schema (mapping)                              |
| Document    | Linha               | Um objeto JSON indexado, com campos e vetor k-NN                            |
| Mapping     | Schema / DDL        | Define os tipos de cada campo, incluindo campos `knn_vector`                |
| Field       | Coluna              | Um atributo de um documento (text, keyword, integer, knn_vector, etc.)      |
| Query DSL   | SQL                 | Linguagem de consulta JSON do OpenSearch                                    |
| Pipeline    | ETL / trigger       | Processamento automático de documentos na ingestão (ex: gerar embeddings)   |

## Caminho de exercícios

### Exercício 1 — Configuração e criação do índice k-NN

**Objetivo:** criar um índice OpenSearch com suporte a vetores k-NN.

**Tarefas:**
- [ ] Conectar ao OpenSearch com `opensearch-py`
- [ ] Criar um índice com `"index.knn": true` e um campo do tipo `knn_vector`
- [ ] Definir `dimension`, `method` (HNSW) e `space_type` (cosinesimil, l2, innerproduct)
- [ ] Verificar o mapping criado com `GET /nome-do-indice/_mapping`

**Exemplo de mapping:**
```python
from opensearchpy import OpenSearch

client = OpenSearch(
    hosts=[{"host": "localhost", "port": 9200}],
    http_auth=("admin", "Admin@1234!"),
    use_ssl=True,
    verify_certs=False,
)

mapping = {
    "settings": {"index": {"knn": True}},
    "mappings": {
        "properties": {
            "content": {"type": "text"},
            "category": {"type": "keyword"},
            "embedding": {
                "type": "knn_vector",
                "dimension": 384,
                "method": {
                    "name": "hnsw",
                    "space_type": "cosinesimil",
                    "engine": "nmslib",
                },
            },
        }
    },
}

client.indices.create(index="documents", body=mapping)
```

---

### Exercício 2 — Inserindo documentos com embeddings

**Objetivo:** indexar documentos com seus vetores gerados externamente.

**Tarefas:**
- [ ] Gerar embeddings com `sentence-transformers`
- [ ] Indexar documentos com `client.index()` incluindo texto, metadados e embedding
- [ ] Usar `bulk()` para inserção em lote de grandes volumes
- [ ] Verificar a contagem de documentos com `GET /nome-do-indice/_count`

---

### Exercício 3 — Busca vetorial (k-NN query)

**Objetivo:** realizar busca por similaridade semântica com k-NN.

**Tarefas:**
- [ ] Gerar o embedding do texto de consulta
- [ ] Executar uma `knn` query com o vetor e `k` resultados desejados
- [ ] Acessar `_id`, `_score` e `_source` de cada resultado
- [ ] Comparar `space_type`: `cosinesimil` vs `l2` vs `innerproduct`

**Exemplo:**
```python
query = {
    "query": {
        "knn": {
            "embedding": {
                "vector": query_embedding,
                "k": 5,
            }
        }
    }
}

response = client.search(index="documents", body=query)
for hit in response["hits"]["hits"]:
    print(hit["_score"], hit["_source"]["content"])
```

---

### Exercício 4 — Busca híbrida (semântica + full-text)

**Objetivo:** combinar k-NN com busca full-text usando BM25, o maior diferencial do OpenSearch.

**Tarefas:**
- [ ] Executar uma busca com `bool` query combinando `knn` e `match`
- [ ] Usar `hybrid` query (disponível no OpenSearch 2.10+) com normalização de scores
- [ ] Configurar um `search_pipeline` com `normalization-processor` e `combination-processor`
- [ ] Ajustar os pesos da combinação e comparar a qualidade dos resultados

**Exemplo de busca híbrida:**
```python
query = {
    "query": {
        "bool": {
            "should": [
                {"match": {"content": {"query": query_text, "boost": 0.3}}},
                {"knn": {"embedding": {"vector": query_embedding, "k": 5, "boost": 0.7}}},
            ]
        }
    }
}
```

---

### Exercício 5 — Filtragem com pre-filter e post-filter

**Objetivo:** combinar busca vetorial com filtros de metadados.

**Tarefas:**
- [ ] Aplicar filtro por `category` usando `filter` dentro da `bool` query
- [ ] Entender a diferença entre pre-filter (filtra antes do k-NN) e post-filter (filtra após)
- [ ] Comparar os resultados e o impacto no recall e na performance
- [ ] Usar `efficient_filter` para melhorar a performance de pre-filter em índices grandes

---

### Exercício 6 — Aggregations e análise de dados

**Objetivo:** explorar as funcionalidades analíticas do OpenSearch além da busca vetorial.

**Tarefas:**
- [ ] Contar documentos por `category` com `terms` aggregation
- [ ] Calcular média de um campo numérico com `avg` aggregation
- [ ] Combinar uma `knn` query com aggregations sobre os resultados
- [ ] Entender por que essa capacidade é um diferencial frente a vetoriais puros

---

### Exercício 7 — Ingestão com pipeline de ML (Neural Search)

**Objetivo:** usar o OpenSearch ML Commons para gerar embeddings automaticamente na ingestão.

**Tarefas:**
- [ ] Configurar um modelo de embedding no OpenSearch via ML Commons
- [ ] Criar um `ingest pipeline` com o processador `text_embedding`
- [ ] Indexar documentos sem precisar gerar embeddings na aplicação — o OpenSearch faz isso
- [ ] Executar `neural` queries que geram o embedding da query automaticamente

---

### Exercício 8 — Integração com LLM (RAG com OpenSearch)

**Objetivo:** construir um pipeline RAG usando OpenSearch como retriever híbrido.

**Tarefas:**
- [ ] Indexar um corpus de documentos com embeddings e campos de texto
- [ ] Implementar retrieval híbrido: dada uma pergunta, buscar com k-NN + BM25
- [ ] Montar o prompt com os trechos recuperados e enviar para uma LLM
- [ ] Comparar a qualidade do RAG com busca puramente vetorial vs. híbrida

**Arquitetura:**
```
Pergunta do usuário
       ↓
Geração do embedding da query (sentence-transformers ou Bedrock)
       ↓
OpenSearch: busca híbrida (k-NN + BM25)
       ↓
Top-K documentos relevantes → Prompt montado
       ↓
LLM (Claude, GPT-4, etc.) → Resposta final
```

---

### Exercício 9 — Amazon OpenSearch Service (AWS gerenciado)

**Objetivo:** migrar do ambiente local para o OpenSearch Service na AWS.

**Tarefas:**
- [ ] Provisionar um domínio OpenSearch Service via console AWS ou Terraform
- [ ] Configurar autenticação via IAM ou usuário fine-grained access control
- [ ] Conectar via `opensearch-py` com autenticação AWS4 (Signature V4)
- [ ] Executar os mesmos exercícios anteriores no ambiente gerenciado
- [ ] Avaliar diferenças de performance, custo e operação vs. self-hosted

**Exemplo de conexão com IAM:**
```python
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import boto3

credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(
    credentials.access_key,
    credentials.secret_key,
    "us-east-1",
    "es",
    session_token=credentials.token,
)

client = OpenSearch(
    hosts=[{"host": "seu-dominio.us-east-1.es.amazonaws.com", "port": 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection,
)
```

## Referências

- Documentação k-NN: https://opensearch.org/docs/latest/search-plugins/knn/index/
- Neural Search (ML Commons): https://opensearch.org/docs/latest/search-plugins/neural-search/
- Busca híbrida: https://opensearch.org/docs/latest/search-plugins/hybrid-search/
- SDK Python: https://opensearch-project.github.io/opensearch-py/
- Amazon OpenSearch Service: https://docs.aws.amazon.com/opensearch-service/latest/developerguide/
