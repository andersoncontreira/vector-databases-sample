# Milvus Examples

> **Nota:** Este é um projeto de estudo. Os exercícios aqui descritos têm fins educacionais.

## O que é o Milvus?

Milvus é um banco de dados vetorial open-source **distribuído e de alta escala**, desenvolvido pela Zilliz. É projetado para lidar com bilhões de vetores em produção, com suporte a múltiplos tipos de índice, armazenamento persistente, alta disponibilidade e uma arquitetura baseada em microsserviços. Existe também o **Milvus Lite**, uma versão embarcada para uso local sem Docker.

## Quando usar o Milvus?

- Você precisa de escala real: **bilhões de vetores** com alta disponibilidade.
- O sistema exige múltiplos tipos de índice (HNSW, IVF, DiskANN, SCANN) com tuning fino.
- Quer **particionamento e sharding** automático de coleções.
- Precisa de busca híbrida (vetorial + escalar) com linguagem de query rica.
- Está construindo uma plataforma de IA em produção com requisitos de SLA.
- Quer usar o **Zilliz Cloud** como versão gerenciada do Milvus.

## Quando NÃO usar o Milvus?

- Projetos pequenos ou de estudo sem necessidade de escala (use ChromaDB ou FAISS).
- Infraestrutura simples sem Kubernetes ou Docker Compose.
- Time sem experiência em sistemas distribuídos.

## Pré-requisitos

- Docker e Docker Compose (para Milvus standalone)
- Python 3.11+
- Bibliotecas: `pymilvus`, `sentence-transformers`

```bash
pip install pymilvus sentence-transformers
```

## Subindo o ambiente com Docker Compose

```bash
# Baixar o docker-compose oficial do Milvus Standalone
curl -sfL https://raw.githubusercontent.com/milvus-io/milvus/master/scripts/standalone_embed.sh -o standalone_embed.sh
bash standalone_embed.sh start
```

Ou via Docker Compose manual:
```bash
# Milvus Standalone (etcd + minio + milvus)
wget https://github.com/milvus-io/milvus/releases/download/v2.4.0/milvus-standalone-docker-compose.yml -O docker-compose.yml
docker compose up -d
```

Verificar se está rodando:
```bash
# Porta padrão: 19530 (gRPC) e 9091 (HTTP/healthcheck)
curl http://localhost:9091/healthz
```

## Milvus Lite (sem Docker)

Para estudo local sem Docker:
```python
from pymilvus import MilvusClient

client = MilvusClient("./milvus_lite.db")  # arquivo local, sem servidor
```

## Conceitos-chave

| Conceito    | Equivalente SQL    | Descrição                                                                    |
|-------------|--------------------|------------------------------------------------------------------------------|
| Collection  | Tabela             | Agrupa entidades com o mesmo schema (campos + vetores)                       |
| Entity      | Linha              | Um registro com campos escalares e vetor(es)                                 |
| Field       | Coluna             | Atributo de uma entidade: `INT64`, `VARCHAR`, `FLOAT_VECTOR`, etc.           |
| Schema      | DDL                | Define os campos e tipos da coleção                                          |
| Index       | Índice             | Estrutura de busca sobre o campo vetorial (HNSW, IVF_FLAT, SCANN, etc.)     |
| Partition   | Partição           | Divisão lógica de uma coleção para otimizar queries filtradas                |
| Alias       | View / sinônimo    | Nome alternativo para uma coleção                                            |

## Tipos de índice principais

| Índice      | Tipo      | Melhor para                                         |
|-------------|-----------|-----------------------------------------------------|
| `FLAT`      | Exato     | Precisão máxima, datasets pequenos                  |
| `IVF_FLAT`  | Aproximado| Datasets médios, boa precisão                       |
| `IVF_SQ8`   | Aproximado| Economia de memória com compressão                  |
| `IVF_PQ`    | Aproximado| Datasets muito grandes com compressão agressiva     |
| `HNSW`      | Aproximado| Melhor trade-off velocidade/precisão                |
| `SCANN`     | Aproximado| Alta performance com Google ScaNN                   |
| `DiskANN`   | Disk-based| Datasets que não cabem em RAM                       |

## Caminho de exercícios

### Exercício 1 — Conectar e criar coleção

**Objetivo:** conectar ao Milvus e criar a primeira coleção com schema explícito.

**Tarefas:**
- [ ] Conectar com `MilvusClient` (Lite local ou servidor Docker)
- [ ] Criar uma coleção com `client.create_collection()` passando `dimension`
- [ ] Listar coleções existentes com `client.list_collections()`
- [ ] Descrever o schema da coleção com `client.describe_collection()`

**Exemplo (Milvus Lite):**
```python
from pymilvus import MilvusClient

client = MilvusClient("./milvus_lite.db")

client.create_collection(
    collection_name="documents",
    dimension=384,
)
```

---

### Exercício 2 — Schema explícito com múltiplos campos

**Objetivo:** criar uma coleção com schema completo (campos escalares + vetor).

**Tarefas:**
- [ ] Definir um schema com `MilvusClient.create_schema()`
- [ ] Adicionar campos: `id` (INT64, primary key), `text` (VARCHAR), `category` (VARCHAR), `embedding` (FLOAT_VECTOR)
- [ ] Criar a coleção com o schema definido
- [ ] Entender a diferença entre schema automático e schema explícito

---

### Exercício 3 — Inserindo entidades

**Objetivo:** gerar embeddings e inserir entidades no Milvus.

**Tarefas:**
- [ ] Gerar embeddings com `sentence-transformers`
- [ ] Inserir entidades com `client.insert()` em formato de lista de dicionários
- [ ] Usar `upsert()` para atualizar entidades existentes
- [ ] Verificar a contagem com `client.get_collection_stats()`

---

### Exercício 4 — Criando índice e carregando coleção

**Objetivo:** entender o ciclo de vida de uma coleção no Milvus.

**Tarefas:**
- [ ] Criar um índice HNSW com `client.create_index()`
- [ ] Carregar a coleção em memória com `client.load_collection()` (obrigatório antes de buscar)
- [ ] Verificar o estado do índice com `client.describe_index()`
- [ ] Liberar a coleção da memória com `client.release_collection()`

**Exemplo:**
```python
client.create_index(
    collection_name="documents",
    index_params=client.prepare_index_params().add_index(
        field_name="embedding",
        metric_type="COSINE",
        index_type="HNSW",
        params={"M": 16, "efConstruction": 64},
    ),
)
client.load_collection("documents")
```

---

### Exercício 5 — Busca por similaridade

**Objetivo:** executar buscas vetoriais e interpretar os resultados.

**Tarefas:**
- [ ] Gerar o embedding da query e executar `client.search()`
- [ ] Acessar `id`, `distance` e campos de output de cada resultado
- [ ] Usar `output_fields` para retornar campos escalares junto com o vetor
- [ ] Comparar métricas: `COSINE`, `L2`, `IP`

**Exemplo:**
```python
results = client.search(
    collection_name="documents",
    data=[query_embedding],
    limit=5,
    output_fields=["text", "category"],
)
for r in results[0]:
    print(r["distance"], r["entity"]["text"])
```

---

### Exercício 6 — Filtragem escalar (query híbrida)

**Objetivo:** combinar busca vetorial com filtros sobre campos escalares.

**Tarefas:**
- [ ] Usar `filter='category == "technology"'` na busca vetorial
- [ ] Experimentar operadores: `==`, `!=`, `in`, `like`, `and`, `or`
- [ ] Usar `client.query()` para busca puramente escalar (sem vetor)
- [ ] Comparar a expressividade do Milvus Filter Expression com outros bancos

---

### Exercício 7 — Partições

**Objetivo:** usar partições para organizar e otimizar queries em grandes coleções.

**Tarefas:**
- [ ] Criar partições por categoria (`client.create_partition()`)
- [ ] Inserir entidades em partições específicas
- [ ] Executar buscas limitadas a uma ou mais partições com `partition_names`
- [ ] Entender quando partições melhoram (ou não) a performance

---

### Exercício 8 — Deleção e gerenciamento

**Objetivo:** dominar as operações de manutenção de dados no Milvus.

**Tarefas:**
- [ ] Deletar entidades por ID com `client.delete()`
- [ ] Deletar entidades por filtro: `client.delete(filter='category == "old"')`
- [ ] Compactar a coleção com `client.compact()` após deleções massivas
- [ ] Fazer backup lógico exportando os dados com `client.query()` + reinsert

---

### Exercício 9 — Integração com LangChain

**Objetivo:** usar o Milvus como vector store dentro de um pipeline LangChain.

**Tarefas:**
- [ ] Instalar `langchain-milvus` e usar `Milvus.from_documents()`
- [ ] Configurar a conexão com URI do Milvus Lite ou servidor
- [ ] Criar retriever e montar uma chain RAG completa
- [ ] Comparar com a integração FAISS + LangChain

**Exemplo:**
```python
from langchain_milvus import Milvus
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Milvus.from_documents(
    documents,
    embeddings,
    connection_args={"uri": "./milvus_lite.db"},
)
retriever = vectorstore.as_retriever()
```

---

### Exercício 10 — Milvus em modo distribuído (avançado)

**Objetivo:** explorar a arquitetura distribuída do Milvus para alta escala.

**Tarefas:**
- [ ] Subir o Milvus em modo cluster com Docker Compose (etcd + MinIO + múltiplos nós)
- [ ] Entender os componentes: Root Coord, Query Coord, Data Coord, Index Coord
- [ ] Criar uma coleção com múltiplos shards
- [ ] Observar como o Milvus distribui os dados entre os nós

## Referências

- Documentação oficial: https://milvus.io/docs
- Milvus Lite (sem Docker): https://milvus.io/docs/milvus_lite.md
- SDK Python (pymilvus): https://pymilvus.readthedocs.io/
- Integração LangChain: https://python.langchain.com/docs/integrations/vectorstores/milvus/
- Zilliz Cloud (gerenciado): https://zilliz.com/cloud
