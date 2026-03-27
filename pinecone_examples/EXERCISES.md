# Exercícios — Pinecone

> Sugestões de exercícios para aprofundar os conceitos do Pinecone, organizados por nível de complexidade.

---

## Nível 1 — Fundamentos

### Exercício 1.1 — Explorar o console
Acesse o console do Pinecone, navegue pelo índice `quickstart` e inspecione:
- Estatísticas do índice (`describe_index_stats`)
- Dimensão, métrica e configuração de pods/serverless
- Número de vetores por namespace

### Exercício 1.2 — Fetch por ID
Após o upsert do `ex02`, use `index.fetch(ids=["1", "2"])` para recuperar vetores específicos. Inspecione os campos `values` e `metadata` retornados.

### Exercício 1.3 — Upsert em lote
Modifique o `ex02` para fazer upsert de 100 vetores de uma vez usando uma lista. Observe a diferença de performance em relação a inserções individuais.

### Exercício 1.4 — Delete por ID e por filtro
Após o upsert, delete um vetor por ID com `index.delete(ids=["1"])`. Depois, delete todos os vetores de um namespace com `index.delete(delete_all=True, namespace="default")`. Verifique as estatísticas antes e depois.

---

## Nível 2 — Embeddings e busca

### Exercício 2.1 — Pinecone Inference vs OpenAI
Compare os resultados de busca do `ex02` (Pinecone `multilingual-e5-large`) com o `ex03` (OpenAI `text-embedding-3-small`) para as mesmas queries. Qual retorna resultados mais relevantes para textos em português?

### Exercício 2.2 — Busca sem filtro de metadados
Execute a mesma query do `ex02` sem o filtro `filter={"genre": ...}`. Compare os resultados e observe como o filtro afeta o recall.

### Exercício 2.3 — Score threshold
Filtre os resultados retornando apenas matches com `score >= 0.7`. Implemente o filtro no Python após a query (Pinecone não tem parâmetro nativo de score threshold).

### Exercício 2.4 — include_values
Execute uma query com `include_values=True` e inspecione os vetores retornados. Calcule manualmente a similaridade cosseno entre o vetor da query e o do resultado top-1.

---

## Nível 3 — Namespaces e organização

### Exercício 3.1 — Namespaces por domínio
Faça upsert dos documentos de países em um namespace `"countries"` e dos artigos em `"articles"`. Faça queries em cada namespace separadamente e compare com uma query sem namespace (busca global).

### Exercício 3.2 — Estatísticas por namespace
Use `index.describe_index_stats()` para verificar a contagem de vetores em cada namespace. Implemente uma função que exibe um relatório de uso por namespace.

### Exercício 3.3 — Migração entre namespaces
Simule uma migração: faça fetch de todos os vetores do namespace `"default"` e re-insira no namespace `"v2"`. Delete o namespace original após confirmar que a migração foi bem-sucedida.

---

## Nível 4 — Produção e escala

### Exercício 4.1 — Upsert com retry
Implemente um wrapper de upsert com retry automático usando `tenacity`. Configure 3 tentativas com backoff exponencial para tratar erros transitórios de rede.

### Exercício 4.2 — Paginação de resultados
O Pinecone retorna no máximo `top_k=10000` resultados por query. Implemente uma estratégia de paginação usando diferentes queries ou namespaces para cobrir datasets maiores.

### Exercício 4.3 — Serverless vs Pod
Crie dois índices: um serverless e um pod-based (starter). Indexe o mesmo dataset nos dois e compare latência de upsert e de query. Documente as diferenças de custo.

### Exercício 4.4 — Monitoramento
Use `index.describe_index_stats()` periodicamente para monitorar o crescimento do índice. Implemente um script que gera um relatório CSV com timestamp, total de vetores e uso por namespace.

---

## Nível 5 — Projetos integradores

### Projeto 5.1 — Sistema de FAQ semântico
Indexe um conjunto de 50 perguntas frequentes (com respostas) no Pinecone. Dado uma nova pergunta do usuário, recupere a FAQ mais similar e retorne a resposta armazenada. Se o score for baixo, encaminhe para um LLM gerar uma resposta.

### Projeto 5.2 — Motor de recomendação
Indexe descrições de filmes ou livros com metadados como `genre` e `year`. Dado um item que o usuário gostou, encontre os 10 mais similares filtrando por `genre` e `year >= 2000`.

### Projeto 5.3 — RAG multi-idioma
Indexe os arquivos de países (`data/texts/`) em português e inglês (traduza alguns manualmente ou use o modelo). Teste queries em ambos os idiomas e avalie se o `multilingual-e5-large` recupera os documentos corretos independentemente do idioma da query.
