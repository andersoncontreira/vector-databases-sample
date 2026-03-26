# ChromaDB Examples

> **Nota:** Este é um projeto de estudo. Os exemplos aqui presentes têm fins educacionais e exploratórios, demonstrando as funcionalidades básicas do ChromaDB como banco de dados vetorial.

## O que é o ChromaDB?

ChromaDB é um banco de dados vetorial open-source, leve e fácil de usar, projetado para armazenar, indexar e consultar embeddings de forma eficiente. É muito utilizado em aplicações que envolvem processamento de linguagem natural (NLP) e inteligência artificial.

## Quando usar o ChromaDB?

O ChromaDB é recomendado nos seguintes cenários:

### Casos de uso ideais

- **Busca semântica**: quando você precisa encontrar documentos ou textos com significado similar, e não apenas correspondência exata de palavras-chave.
- **Sistemas RAG (Retrieval-Augmented Generation)**: para recuperar contexto relevante antes de gerar respostas com LLMs (ex: ChatGPT, Claude, LLaMA).
- **Recomendação de conteúdo**: encontrar itens semelhantes com base em representações vetoriais (textos, imagens, produtos).
- **Detecção de duplicatas**: identificar documentos semanticamente duplicados ou muito parecidos.
- **Classificação e agrupamento (clustering)**: organizar grandes volumes de dados não estruturados por similaridade.
- **Prototipagem e experimentos locais**: graças ao suporte a modo in-memory e persistência em disco, é ideal para desenvolvimento e estudos sem necessidade de infraestrutura adicional.

### Quando o ChromaDB se destaca em relação a alternativas

| Cenário                             | ChromaDB  | Alternativas                       |
|-------------------------------------|-----------|------------------------------------|
| Projetos pequenos/médios            | Excelente | Overkill com Pinecone/Weaviate     |
| Uso local / offline                 | Excelente | Requer servidor externo (Pinecone) |
| Integração com LangChain/LlamaIndex | Nativa    | Variável                           |
| Alta escala (bilhões de vetores)    | Limitado  | Prefira Pinecone ou Weaviate       |
| Deploy em produção gerenciado       | Limitado  | Prefira soluções cloud             |

## Estrutura dos exercícios

Os arquivos seguem a convenção `exNN_descricao.py`, ordenados pela progressão natural do estudo.

```
chromadb_examples/
├── ex01_in_memory_basic.py          # ChromaDB in-memory: coleção, upsert e busca simples
├── ex02_embedding_visualization.py  # Visualizar o vetor gerado pelo DefaultEmbeddingFunction
├── ex03_in_memory_explicit_ef.py    # In-memory com EmbeddingFunction explícita
├── ex04_persistent_client.py        # PersistentClient: dados salvos em disco
├── ex05_raw_openai_embedding.py     # Gerar embedding direto pela API OpenAI (sem ChromaDB)
├── ex06_persistent_openai_ef.py     # ChromaDB persistente com OpenAI como embedding function
├── ex07_persistent_bedrock_ef.py    # ChromaDB persistente com Amazon Bedrock como embedding function
├── ex08_rag_indexing.py             # Pipeline RAG: leitura de PDFs, chunking e indexação
├── ex09_rag_query.py                # Consulta sobre a coleção criada no ex08
├── ex10_rag_with_llm_response.py    # RAG completo: retrieval + resposta gerada pela LLM
├── data_utils.py                    # Utilitários: leitura de PDF, chunking, embeddings, geração de resposta
└── scripts/
    └── init.sh                      # Script de inicialização do ambiente virtual e dependências
```

## Coleções (Collections)

No ChromaDB, o conceito equivalente a uma "tabela" de banco de dados relacional é a **Collection**. Cada coleção armazena documentos junto com seus embeddings vetoriais e metadados opcionais.

### Estrutura interna de uma Collection

Cada registro dentro de uma coleção é composto pelos seguintes campos:

| Campo        | Tipo          | Obrigatório | Descrição                                                                 |
|--------------|---------------|-------------|---------------------------------------------------------------------------|
| `id`         | string        | Sim         | Identificador único do documento dentro da coleção                        |
| `documents`  | string        | Não*        | Texto original do documento (usado para gerar o embedding automaticamente)|
| `embeddings` | list[float]   | Não*        | Vetor numérico que representa semanticamente o documento                  |
| `metadatas`  | dict          | Não         | Dados adicionais associados ao documento (ex: autor, data, categoria)     |

> *Pelo menos um entre `documents` ou `embeddings` deve ser fornecido.

### Coleções criadas nos exemplos

#### `test_collection` — usada em `ex01_in_memory_basic.py` e `ex03_in_memory_explicit_ef.py`

Coleção criada para demonstrar inserção e busca por similaridade semântica. Armazena frases simples em inglês e permite consultar quais documentos são semanticamente mais próximos de um texto de busca.

**Documentos inseridos:**

| ID     | Texto                                  |
|--------|----------------------------------------|
| `doc1` | This is the first document.            |
| `doc2` | This document is the second document.  |
| `doc3` | And this is the third one.             |
| `doc4` | Is this the first document?            |

**Fluxo:**
1. Os textos são convertidos em embeddings pela `EmbeddingFunction` configurada.
2. Os vetores são armazenados e indexados na coleção.
3. Na consulta (`query_texts=["first document"]`), o texto de busca também é convertido em embedding.
4. O ChromaDB retorna os `n` documentos cujos vetores têm menor distância em relação ao vetor de consulta.

**Resultado esperado** (ordenado por similaridade):

```
Result 1: Document ID: doc1, Distance: <menor> => This is the first document.
Result 2: Document ID: doc4, Distance: <médio> => Is this the first document?
Result 3: Document ID: doc2, Distance: <maior> => This document is the second document.
```

### Diferença entre `ex01` e `ex03`

| Aspecto                      | `ex01_in_memory_basic.py`      | `ex03_in_memory_explicit_ef.py`             |
|------------------------------|--------------------------------|---------------------------------------------|
| Embedding function           | Implícita (padrão do ChromaDB) | Explícita (`DefaultEmbeddingFunction`)      |
| Controle sobre o modelo      | Nenhum                         | Permite trocar por outro modelo facilmente  |
| Exemplo de integração futura | —                              | Comentário com `AmazonBedrockEmbeddingFunction` |

## Como executar

### 1. Inicializar o ambiente

```bash
cd chromadb_examples
bash scripts/init.sh
source venv/bin/activate
```

### 2. Executar os exercícios

```bash
# Ex01 - ChromaDB in-memory básico
python ex01_in_memory_basic.py

# Ex02 - Visualizar embedding gerado
python ex02_embedding_visualization.py

# Ex03 - In-memory com EmbeddingFunction explícita
python ex03_in_memory_explicit_ef.py

# Ex04 - Cliente persistente (dados em disco)
python ex04_persistent_client.py

# Ex05 - Embedding raw via OpenAI API
python ex05_raw_openai_embedding.py

# Ex06 - ChromaDB persistente com OpenAI
python ex06_persistent_openai_ef.py

# Ex07 - ChromaDB persistente com Bedrock
python ex07_persistent_bedrock_ef.py

# Ex08 - RAG: indexar documentos (rode antes do ex09 e ex10)
python ex08_rag_indexing.py

# Ex09 - RAG: consultar a coleção indexada
python ex09_rag_query.py

# Ex10 - RAG completo com resposta da LLM
python ex10_rag_with_llm_response.py
```

## Dependências

- Python 3.11+
- chromadb==1.3.5

## Notas relevantes

- Os exemplos utilizam o cliente in-memory (`chromadb.Client()`), ou seja, os dados não são persistidos entre execuções. Para persistência, use `chromadb.PersistentClient(path="./chroma_data")`.
- O `DefaultEmbeddingFunction` usa o modelo `all-MiniLM-L6-v2` da biblioteca `sentence-transformers` por padrão, adequado para textos em inglês.
- Para textos em português, considere usar modelos multilíngues como `paraphrase-multilingual-MiniLM-L12-v2`.
- A distância retornada nas consultas é a distância L2 (euclidiana) por padrão. Valores menores indicam maior similaridade.
