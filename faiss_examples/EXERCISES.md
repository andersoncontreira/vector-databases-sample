# Exercícios — FAISS

> Sugestões de exercícios para aprofundar os conceitos do FAISS, organizados por nível de complexidade.

---

## Nível 1 — Fundamentos

### Exercício 1.1 — Primeiro índice flat
Crie um `IndexFlatL2` com vetores aleatórios gerados por `numpy`. Adicione 1.000 vetores e faça uma busca retornando os 5 mais próximos. Inspecione os arrays `D` (distâncias) e `I` (índices) retornados.

### Exercício 1.2 — Dimensões diferentes
Experimente criar índices com dimensões 64, 128, 384 e 1536. Observe como o tempo de busca escala com a dimensão usando `time.perf_counter()`.

### Exercício 1.3 — Normalização e cosseno
Gere embeddings com `sentence-transformers`, normalize com `faiss.normalize_L2()` e use `IndexFlatIP`. Compare os rankings com um `IndexFlatL2` sem normalização para as mesmas queries.

### Exercício 1.4 — IDs customizados
Use `IndexIDMap` para associar IDs int64 arbitrários aos vetores. Mapeie os IDs para um dicionário Python com os textos originais. Verifique que a busca retorna os IDs corretos.

---

## Nível 2 — Índices aproximados

### Exercício 2.1 — IVF: treinamento obrigatório
Crie um `IndexIVFFlat` com `nlist=10`. Tente adicionar vetores sem treinar primeiro e observe o erro. Depois treine corretamente e adicione os vetores.

### Exercício 2.2 — Impacto do nprobe
Com um `IndexIVFFlat` populado com 10.000 vetores, execute a mesma query com `nprobe` variando de 1 a 50. Meça o tempo de busca e o recall (comparando com `IndexFlatL2`) para cada valor.

### Exercício 2.3 — HNSW vs IVF
Crie os dois índices com o mesmo dataset (50.000 vetores). Compare:
- Tempo de inserção
- Tempo de busca (top-10)
- Uso de memória (`index.ntotal * d * 4` bytes para flat)
- Facilidade de uso (HNSW não precisa de treinamento)

### Exercício 2.4 — Product Quantization
Use `IndexIVFPQ` com `nlist=100`, `M=8` subquantizadores e `nbits=8`. Compare o tamanho do índice salvo em disco com o de um `IndexIVFFlat` equivalente.

---

## Nível 3 — Persistência e metadados

### Exercício 3.1 — Save e load
Treine e popule um `IndexIVFFlat`. Salve com `faiss.write_index()`, carregue com `faiss.read_index()` e verifique que os resultados de busca são idênticos antes e depois.

### Exercício 3.2 — Metadados com JSON
Como o FAISS não suporta metadados nativos, salve um arquivo `index_metadata.json` paralelo ao `index.faiss`, mapeando o índice inteiro (posição no array) para o texto e metadados do documento. Implemente busca completa: FAISS retorna índices → JSON resolve os textos.

### Exercício 3.3 — Metadados com SQLite
Substitua o JSON do exercício anterior por uma tabela SQLite. Avalie a diferença de performance para 100.000 documentos ao resolver os metadados após o FAISS retornar os IDs.

### Exercício 3.4 — Atualização incremental
O FAISS não suporta deleção eficiente. Implemente uma estratégia de "soft delete": mantenha um `set` de IDs deletados em memória e filtre os resultados da busca para excluir os IDs marcados.

---

## Nível 4 — Performance e benchmarking

### Exercício 4.1 — Escala: 1M de vetores
Gere 1 milhão de vetores de dimensão 128. Compare o tempo de busca entre `IndexFlatL2`, `IndexIVFFlat` e `IndexHNSWFlat`. Use `time.perf_counter()` para medir com precisão.

### Exercício 4.2 — Batch search
Em vez de fazer queries uma a uma, use o suporte nativo de batch do FAISS: passe uma matriz `(n_queries, d)` para `index.search()`. Meça o speedup em relação a `n` chamadas individuais.

### Exercício 4.3 — GPU (opcional)
Se tiver GPU disponível, instale `faiss-gpu` e compare o tempo de busca de um `IndexFlatL2` em CPU vs GPU para 1M de vetores.

### Exercício 4.4 — Comparativo FAISS vs ChromaDB vs Qdrant
Para datasets de 10K, 100K e 1M vetores, meça e tabele: tempo de inserção, tempo de busca top-10, uso de memória e recall@10.

---

## Nível 5 — Projetos integradores

### Projeto 5.1 — Motor de busca semântica local
Construa um script que indexa todos os arquivos `data/texts/*.txt` em um `IndexHNSWFlat` persistido em disco. Implemente uma CLI que recebe uma query e exibe os trechos mais relevantes com o nome do arquivo de origem.

### Projeto 5.2 — Detector de duplicatas
Indexe um conjunto de frases com algumas duplicatas ligeiramente modificadas. Use FAISS para encontrar pares com distância < threshold. Liste os pares detectados como potenciais duplicatas.

### Projeto 5.3 — Integração com LangChain
Use `FAISS.from_documents()` do LangChain para indexar os PDFs de `data/articles/`. Monte um pipeline RAG completo e compare com o pipeline usando Chroma do `langchain_examples/ex03`.
