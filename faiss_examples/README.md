# FAISS Examples

> **Nota:** Este é um projeto de estudo. Os exercícios aqui descritos têm fins educacionais.

## O que é o FAISS?

FAISS (Facebook AI Similarity Search) é uma **biblioteca** open-source desenvolvida pelo Meta AI para busca eficiente de vizinhos mais próximos em espaços de alta dimensão. Diferente dos outros bancos de dados vetoriais, o FAISS **não é um servidor** — é uma biblioteca Python/C++ que roda inteiramente em memória (ou em disco com índices especiais), sem processos externos, sem API REST, sem persistência nativa.

É amplamente usado como motor de busca vetorial embutido em outros sistemas e como referência de performance em benchmarks.

## Quando usar o FAISS?

- Você precisa de busca vetorial **máxima performance** em um único processo Python.
- O dataset cabe em memória (ou você quer usar índices on-disk como `IndexIVFFlat` com mmap).
- Quer controle total sobre o índice, sem overhead de rede ou serialização.
- Está construindo uma biblioteca ou serviço próprio e quer embutir a busca vetorial.
- Precisa fazer benchmarks ou comparar algoritmos de busca aproximada (ANN).
- Integração com pipelines de ML/data science onde tudo já está em Python/NumPy.

## Quando NÃO usar o FAISS?

- Precisa de persistência nativa com atualizações incrementais frequentes (FAISS não suporta deleção eficiente).
- Necessita de filtragem por metadados combinada com busca vetorial.
- Quer um servidor com API para múltiplos clientes simultâneos.
- O dataset não cabe em memória RAM disponível.

## Pré-requisitos

- Python 3.11+
- Bibliotecas: `faiss-cpu` (ou `faiss-gpu` se tiver GPU), `sentence-transformers`, `numpy`

```bash
# CPU (maioria dos casos)
pip install faiss-cpu sentence-transformers numpy

# GPU (requer CUDA)
pip install faiss-gpu sentence-transformers numpy
```

> Não é necessário Docker — o FAISS roda inteiramente como biblioteca Python.

## Conceitos-chave

| Conceito       | Descrição                                                                        |
|----------------|----------------------------------------------------------------------------------|
| Index          | Estrutura que armazena e indexa os vetores para busca                            |
| `d`            | Dimensão dos vetores (deve ser consistente em todo o índice)                     |
| `nlist`        | Número de clusters do IVF — trade-off entre velocidade e precisão                |
| `nprobe`       | Quantos clusters verificar na busca — maior = mais preciso, mais lento           |
| `add()`        | Adiciona vetores ao índice                                                       |
| `search()`     | Retorna os K vizinhos mais próximos de um vetor de query                         |
| `write_index()`| Salva o índice em disco                                                          |
| `read_index()` | Carrega o índice do disco                                                        |

## Tipos de índice principais

| Índice              | Descrição                                        | Melhor para                          |
|---------------------|--------------------------------------------------|--------------------------------------|
| `IndexFlatL2`       | Busca exata por distância L2                     | Precisão máxima, datasets pequenos   |
| `IndexFlatIP`       | Busca exata por produto interno (cosine com norm)| Embeddings normalizados              |
| `IndexIVFFlat`      | IVF com busca aproximada                         | Datasets médios/grandes em memória   |
| `IndexIVFSQ8`       | IVF com quantização escalar (compressão 4x)      | Economia de memória                  |
| `IndexIVFPQ`        | IVF com Product Quantization (compressão maior)  | Datasets muito grandes               |
| `IndexHNSWFlat`     | HNSW — alta velocidade e boa precisão            | Melhor trade-off para produção       |
| `IndexIDMap`        | Wrapper para usar IDs customizados               | Quando precisar de IDs não sequenciais|

## Caminho de exercícios

### Exercício 1 — Índice flat (busca exata)

**Objetivo:** criar o índice mais simples do FAISS e entender o fluxo básico.

**Tarefas:**
- [ ] Criar um `IndexFlatL2` com a dimensão correta
- [ ] Gerar embeddings com `sentence-transformers` e converter para `numpy float32`
- [ ] Adicionar vetores ao índice com `index.add()`
- [ ] Executar uma busca com `index.search()` e interpretar os arrays `D` (distâncias) e `I` (índices)

**Exemplo:**
```python
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
sentences = ["Paris is the capital of France.", "Brazil has 26 states."]

embeddings = model.encode(sentences).astype("float32")

index = faiss.IndexFlatL2(embeddings.shape[1])  # d = 384
index.add(embeddings)

query = model.encode(["What is the capital of France?"]).astype("float32")
D, I = index.search(query, k=2)
# D = distâncias, I = índices dos resultados
```

---

### Exercício 2 — Normalização e distância cosseno

**Objetivo:** usar produto interno como proxy para similaridade cosseno.

**Tarefas:**
- [ ] Normalizar os vetores com `faiss.normalize_L2()`
- [ ] Usar `IndexFlatIP` (inner product) em vez de `IndexFlatL2`
- [ ] Comparar os resultados com L2 vs. cosseno no mesmo dataset
- [ ] Entender por que a normalização é necessária para IP equivaler ao cosseno

---

### Exercício 3 — IDs customizados com IndexIDMap

**Objetivo:** associar IDs arbitrários (não sequenciais) aos vetores.

**Tarefas:**
- [ ] Criar um `IndexIDMap` wrapping um `IndexFlatL2`
- [ ] Inserir vetores com `index.add_with_ids()` passando um array de IDs int64
- [ ] Buscar e mapear os IDs retornados para os documentos originais
- [ ] Entender a limitação: IDs precisam ser int64

---

### Exercício 4 — Índice IVF (busca aproximada)

**Objetivo:** melhorar a performance de busca em datasets maiores com IVF.

**Tarefas:**
- [ ] Criar um `IndexIVFFlat` com `nlist=100` clusters
- [ ] **Treinar** o índice com `index.train(embeddings)` antes de adicionar vetores
- [ ] Adicionar os vetores e executar buscas com diferentes valores de `nprobe`
- [ ] Medir o trade-off entre velocidade e recall ao variar `nprobe`

**Exemplo:**
```python
quantizer = faiss.IndexFlatL2(d)
index = faiss.IndexIVFFlat(quantizer, d, nlist=100)
index.train(embeddings)  # obrigatório antes do add
index.add(embeddings)
index.nprobe = 10        # quantos clusters verificar na busca
D, I = index.search(query, k=5)
```

---

### Exercício 5 — Persistência em disco

**Objetivo:** salvar e carregar índices FAISS do disco.

**Tarefas:**
- [ ] Salvar o índice com `faiss.write_index(index, "index.faiss")`
- [ ] Carregar o índice com `faiss.read_index("index.faiss")`
- [ ] Verificar que os resultados de busca são idênticos antes e depois do save/load
- [ ] Entender como combinar o índice FAISS com um dicionário JSON/SQLite para armazenar metadados

---

### Exercício 6 — HNSW no FAISS

**Objetivo:** usar o índice HNSW do FAISS, que oferece o melhor trade-off velocidade/precisão.

**Tarefas:**
- [ ] Criar um `IndexHNSWFlat` com `M=16` (conexões por nó)
- [ ] Adicionar vetores (HNSW não requer treinamento)
- [ ] Comparar a velocidade de busca com `IndexFlatL2` e `IndexIVFFlat`
- [ ] Ajustar `efSearch` para controlar o trade-off velocidade vs. recall

---

### Exercício 7 — Metadados externos com SQLite

**Objetivo:** superar a limitação do FAISS (sem metadados nativos) usando um store externo.

**Tarefas:**
- [ ] Criar uma tabela SQLite com `id`, `text`, `source` e outros metadados
- [ ] Usar o índice inteiro (posição no array) como chave para mapear ao registro SQLite
- [ ] Implementar busca: FAISS retorna índices → consultar SQLite pelos IDs → retornar texto
- [ ] Entender por que essa é a abordagem mais comum ao usar FAISS em produção

---

### Exercício 8 — Integração com LangChain

**Objetivo:** usar o FAISS como vector store dentro de um pipeline LangChain.

**Tarefas:**
- [ ] Instalar `langchain-community` e usar `FAISS.from_documents()`
- [ ] Salvar e carregar o vector store com `vectorstore.save_local()` e `FAISS.load_local()`
- [ ] Criar um retriever com `vectorstore.as_retriever()`
- [ ] Montar uma chain RAG completa com o FAISS como retriever

**Exemplo:**
```python
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = FAISS.from_documents(documents, embeddings)
vectorstore.save_local("../db/faiss_index")

# Em outra sessão:
vectorstore = FAISS.load_local("../db/faiss_index", embeddings, allow_dangerous_deserialization=True)
retriever = vectorstore.as_retriever()
```

---

### Exercício 9 — Benchmarking: FAISS vs. ChromaDB vs. Qdrant

**Objetivo:** comparar a performance de busca entre as principais bibliotecas.

**Tarefas:**
- [ ] Gerar um dataset sintético de 10.000, 100.000 e 1.000.000 vetores
- [ ] Medir o tempo de inserção e de busca (top-10) em cada solução
- [ ] Comparar uso de memória e precisão (recall@10)
- [ ] Documentar os resultados e as conclusões sobre quando usar cada solução

## Referências

- Repositório oficial: https://github.com/facebookresearch/faiss
- Documentação: https://faiss.ai/
- Wiki de índices: https://github.com/facebookresearch/faiss/wiki/Faiss-indexes
- Integração com LangChain: https://python.langchain.com/docs/integrations/vectorstores/faiss/
