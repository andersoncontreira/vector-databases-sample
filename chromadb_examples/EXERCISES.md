# Exercícios — ChromaDB

> Sugestões de exercícios para aprofundar os conceitos do ChromaDB, organizados por nível de complexidade.

---

## Nível 1 — Fundamentos

### Exercício 1.1 — Explorar metadados
Adicione metadados ricos aos documentos do `ex01` (ex: `{"author": "...", "year": 2024, "topic": "tech"}`). Após a inserção, use `collection.get()` para inspecionar os metadados armazenados.

### Exercício 1.2 — Filtro por metadados
Use o parâmetro `where` na query para filtrar documentos por metadados antes da busca vetorial. Exemplo: retornar apenas documentos de um determinado `topic`.

### Exercício 1.3 — Comparar métricas de distância
Crie três coleções idênticas, cada uma configurada com uma métrica diferente (`l2`, `cosine`, `ip`). Insira os mesmos documentos e compare os scores retornados para a mesma query.

### Exercício 1.4 — Listar e inspecionar coleções
Use `client.list_collections()` e `collection.count()` para inspecionar o estado do banco. Pratique `collection.get(ids=[...])` para recuperar documentos específicos por ID.

---

## Nível 2 — Embeddings

### Exercício 2.1 — Visualizar embeddings
Pegue o vetor gerado pelo `ex02` e use `numpy` para calcular a norma (`np.linalg.norm`) e a similaridade cosseno manualmente entre dois textos diferentes.

### Exercício 2.2 — Comparar embedding functions
Crie duas coleções com a mesma lista de documentos, uma usando `DefaultEmbeddingFunction` e outra usando `OpenAIEmbeddingFunction`. Compare os resultados de busca para a mesma query.

### Exercício 2.3 — Modelo multilíngue
Substitua o modelo padrão pelo `paraphrase-multilingual-MiniLM-L12-v2` (suporte a português). Indexe os arquivos de países de `data/texts/` e faça queries em português. Compare com os resultados do modelo em inglês.

---

## Nível 3 — Persistência e Gerenciamento

### Exercício 3.1 — Persistência com upsert idempotente
Rode o `ex04` duas vezes seguidas. Verifique com `collection.count()` que os documentos não foram duplicados (o `upsert` com IDs estáveis deve ser idempotente).

### Exercício 3.2 — Deleção seletiva
Após indexar os documentos do `ex04`, delete um subconjunto deles por ID com `collection.delete(ids=[...])`. Verifique a contagem antes e depois.

### Exercício 3.3 — Atualização de documentos
Modifique o texto de um documento existente fazendo `upsert` com o mesmo ID mas conteúdo diferente. Verifique que a busca retorna o novo conteúdo.

### Exercício 3.4 — Múltiplas coleções
Crie coleções separadas para diferentes domínios (`"articles"`, `"countries"`, `"products"`). Implemente uma função de busca que consulta todas as coleções e agrega os resultados.

---

## Nível 4 — RAG

### Exercício 4.1 — RAG com arquivos de países
Use o `ex08` como base para indexar os arquivos `data/texts/*.txt` dos países. Implemente perguntas como:
- "Qual é a capital do Brasil?"
- "Quais países têm costa no oceano Pacífico?"
- "Qual é o maior país da América do Sul?"

### Exercício 4.2 — Chunking estratégico
Compare o comportamento do RAG com chunks de tamanho 500 e 2000 caracteres. Avalie como o tamanho do chunk afeta a precisão das respostas para perguntas que requerem contexto longo.

### Exercício 4.3 — Retrieval com n_results variável
Experimente valores de `n_results` entre 1 e 10 no pipeline RAG. Observe como mais contexto nem sempre melhora a resposta (problema de "needle in a haystack").

### Exercício 4.4 — Fontes na resposta
Modifique o pipeline do `ex08` para que a resposta inclua as fontes dos documentos recuperados (arquivo de origem e trecho utilizado).

---

## Nível 5 — Projetos integradores

### Projeto 5.1 — Motor de busca de países
Construa uma interface de linha de comando que receba uma pergunta do usuário, busque nos documentos de países e exiba a resposta com o nome do país de origem da informação.

### Projeto 5.2 — Indexador com deduplicação
Crie um script que gera IDs estáveis baseados no hash do conteúdo (`hashlib.md5`). Rode o indexador múltiplas vezes e confirme que não há duplicatas, mesmo adicionando novos documentos incrementalmente.

### Projeto 5.3 — Comparativo ChromaDB vs FAISS
Indexe o mesmo conjunto de documentos em ChromaDB e FAISS. Para 100 queries aleatórias, compare: tempo de busca, recall@5 e facilidade de uso da API.
