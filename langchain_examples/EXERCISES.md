# Exercícios — LangChain

> Sugestões de exercícios para aprofundar os conceitos do framework LangChain, organizados por nível de complexidade.

---

## Nível 1 — Fundamentos

### Exercício 1.1 — Troca de modelo
Modifique o `ex01` para usar um modelo diferente do `gpt-5-nano`, como `gpt-4o-mini` ou `gpt-4o`. Compare as respostas e observe as diferenças de qualidade e latência.

### Exercício 1.2 — Prompt com variáveis
Crie um `ChatPromptTemplate` com as variáveis `{language}` e `{text}`, e use-o para traduzir dinamicamente textos para idiomas diferentes sem alterar o código.

### Exercício 1.3 — Output Parser customizado
Implemente um `PydanticOutputParser` que force o modelo a responder sempre em formato JSON com os campos `answer` (string) e `confidence` (float entre 0 e 1).

### Exercício 1.4 — Histórico de conversa
Use `ChatMessageHistory` e `RunnableWithMessageHistory` para criar um chatbot simples que lembre das mensagens anteriores da sessão.

---

## Nível 2 — Document Loaders e Chunking

### Exercício 2.1 — Loader de URLs
Use `WebBaseLoader` para carregar o conteúdo de uma página web e indexar no Chroma. Faça perguntas sobre o conteúdo da página.

### Exercício 2.2 — Estratégias de chunking
Com os arquivos de países de `data/texts/`, experimente diferentes configurações de `RecursiveCharacterTextSplitter`:
- `chunk_size=500, chunk_overlap=50`
- `chunk_size=2000, chunk_overlap=400`

Compare como o tamanho do chunk afeta a qualidade das respostas RAG.

### Exercício 2.3 — Metadata nos documentos
Ao carregar os arquivos de países, adicione metadados como `{"source": "countries", "language": "pt"}` a cada documento. Use esses metadados para filtrar a busca por similaridade.

### Exercício 2.4 — Loader de CSV
Use `CSVLoader` para carregar um arquivo CSV de dados tabulares e indexar no Chroma. Experimente perguntas que exijam agregação de informações de múltiplas linhas.

---

## Nível 3 — Chains e RAG

### Exercício 3.1 — RAG com score de relevância
Modifique o pipeline RAG para usar `similarity_search_with_score()` em vez de `similarity_search()`. Exiba o score de cada documento recuperado junto com a resposta.

### Exercício 3.2 — Chain com múltiplos retrievers
Crie uma chain que consulta dois retrievers diferentes (ex: um com documentos de países e outro com artigos) e combina os contextos antes de enviar ao modelo.

### Exercício 3.3 — Reranking
Após o retrieval, implemente um passo de reranking simples que ordena os documentos recuperados por relevância usando o próprio modelo (LLM-as-a-judge) antes de montar o contexto.

### Exercício 3.4 — Chain condicional
Use `RunnableBranch` para criar uma chain que decide automaticamente se a pergunta deve ser respondida com RAG (quando envolve dados dos documentos) ou diretamente pelo modelo (conhecimento geral).

---

## Nível 4 — Vector Stores

### Exercício 4.1 — Chroma persistente
Modifique o `ex02` para usar `PersistentClient` do Chroma, salvando o índice em `../db/chroma_langchain`. Rode o script duas vezes e verifique que os documentos não são duplicados (use `upsert` com IDs estáveis).

### Exercício 4.2 — FAISS com LangChain
Substitua o Chroma pelo FAISS no pipeline do `ex02`. Use `FAISS.from_documents()` e `FAISS.save_local()`. Compare a velocidade de indexação e busca.

### Exercício 4.3 — Pinecone com namespace
Modifique o `ex04` para indexar documentos em namespaces separados por tipo: `"articles"` para PDFs e `"countries"` para TXTs. Faça queries em cada namespace individualmente.

### Exercício 4.4 — Redis com TTL
No `ex07`, configure um TTL (time-to-live) nos documentos indexados no Redis. Verifique que os documentos expiram após o tempo configurado e que novas consultas retornam resultados vazios.

---

## Nível 5 — Agents e Tools

### Exercício 5.1 — Agent com tool de busca
Crie um agent com `AgentExecutor` que tenha acesso a duas tools:
- `search_countries`: busca nos documentos de países indexados no Chroma
- `calculator`: avalia expressões matemáticas simples

Faça perguntas que exijam o uso de uma ou ambas as tools.

### Exercício 5.2 — Tool de acesso a banco de dados
Implemente uma tool que executa queries SQL em um banco SQLite. Integre ao agent para responder perguntas sobre dados estruturados combinando SQL com LLM.

### Exercício 5.3 — ReAct Agent
Implemente o padrão ReAct (Reasoning + Acting) usando `create_react_agent`. Observe o processo de raciocínio passo a passo (Thought → Action → Observation → Answer).

---

## Nível 6 — Avaliação e Observabilidade

### Exercício 6.1 — Avaliação de RAG com RAGAS
Instale `ragas` e avalie o pipeline RAG do `ex05` com as métricas:
- `faithfulness`: a resposta é suportada pelo contexto?
- `answer_relevancy`: a resposta é relevante para a pergunta?
- `context_recall`: o contexto recuperado contém a informação necessária?

### Exercício 6.2 — Tracing com LangSmith
Configure o LangSmith (`LANGCHAIN_TRACING_V2=true`) e execute os exemplos. Observe o trace completo de cada chain no dashboard, identificando latência por etapa e tokens consumidos.

### Exercício 6.3 — Comparação de modelos
Monte um pipeline de avaliação que faz as mesmas 10 perguntas sobre os documentos de países usando `gpt-5-nano`, `gpt-4o-mini` e `gpt-4o`. Compare custo, latência e qualidade das respostas.

---

## Nível 7 — Projetos integradores

### Projeto 7.1 — Assistente de países
Construa um chatbot com memória conversacional que responde perguntas sobre os 7 países indexados nos arquivos TXT. O assistente deve:
- Lembrar o contexto da conversa
- Buscar informações relevantes nos documentos
- Indicar quando não tem informação suficiente

### Projeto 7.2 — Pipeline RAG multi-vector-store
Implemente um pipeline que indexa os mesmos documentos em três vector stores diferentes (Chroma, FAISS e Redis) e compara automaticamente os resultados de retrieval para a mesma query. Exiba os top-3 documentos de cada store lado a lado.

### Projeto 7.3 — Indexador incremental
Crie um script que monitora a pasta `data/` e, quando um novo arquivo for adicionado, automaticamente:
1. Carrega e processa o documento
2. Gera embeddings
3. Faz upsert no Pinecone com namespace baseado na pasta de origem
4. Registra o arquivo processado em um arquivo de controle para evitar re-indexações

### Projeto 7.4 — API REST de RAG
Construa uma API REST com FastAPI que expõe dois endpoints:
- `POST /index` — recebe um arquivo, processa e indexa no Chroma
- `POST /query` — recebe uma pergunta e retorna a resposta RAG com as fontes utilizadas
