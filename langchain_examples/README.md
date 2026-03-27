# LangChain Examples

> **Nota:** Este é um projeto de estudo. Os exemplos e exercícios têm fins educacionais, explorando o framework LangChain integrado a diferentes modelos e bancos de dados vetoriais.

## O que é o LangChain?

LangChain é um framework open-source para construção de aplicações com **LLMs (Large Language Models)**. Ele fornece abstrações para encadear chamadas a modelos de linguagem, recuperadores de documentos, ferramentas externas e memória, permitindo construir desde chatbots simples até pipelines RAG complexos de forma modular e reutilizável.

## Quando usar o LangChain?

- Você quer construir pipelines RAG sem gerenciar manualmente embeddings, retrieval e prompts.
- Precisa de abstrações portáteis entre diferentes LLMs (OpenAI, Anthropic, Bedrock, etc.) e vector stores (Chroma, Pinecone, Redis, Weaviate, etc.).
- Quer usar **LCEL (LangChain Expression Language)** para compor chains declarativas e legíveis.
- Seu projeto envolve agents, tools ou memória conversacional.

## Estrutura dos exemplos

Os arquivos seguem a convenção `exNN_descricao.py`, ordenados pela progressão natural do estudo.

```
langchain_examples/
├── ex01_langchain_introduction.py       # Primeira chamada a um LLM com ChatOpenAI
├── ex02_langchain_document_loaders.py   # Carregar PDFs e TXTs, chunking, embeddings e Chroma
├── ex03_langchain_chains.py             # Pipeline RAG com create_retrieval_chain (abordagem clássica)
├── ex04_langchain_pinecone.py           # Indexar documentos no Pinecone via LangChain
├── ex05_langchain_pinecone_retriever.py # RAG com Pinecone usando LCEL (RunnableParallel)
├── ex06_langchain_pinecone_query_only.py# Consultar índice Pinecone existente sem re-indexar
├── ex07_langchain_redis.py              # Indexar e consultar com Redis como vector store
├── EXERCISES.md                         # Sugestões de exercícios para aprofundar os conceitos
└── requirements.txt                     # Dependências do projeto
```

## Progressão dos exemplos

```
ex01  →  Conceitos base: LLM, mensagens, invoke
ex02  →  Document loaders, chunking, embeddings, Chroma local
ex03  →  RAG clássico com create_retrieval_chain + create_stuff_documents_chain
ex04  →  Pinecone: indexação de documentos reais (PDFs)
ex05  →  Pinecone: RAG com LCEL (RunnableParallel + RunnableLambda)
ex06  →  Pinecone: query-only, sem re-indexação
ex07  →  Redis como vector store alternativo
```

## Conceitos-chave do LangChain

| Conceito               | Descrição                                                                      |
|------------------------|--------------------------------------------------------------------------------|
| `ChatModel`            | Abstração sobre LLMs que aceitam mensagens (system, human, ai)                 |
| `PromptTemplate`       | Template reutilizável com variáveis para montar prompts dinâmicos              |
| `DocumentLoader`       | Carrega documentos de diversas fontes (PDF, TXT, Web, banco de dados)          |
| `TextSplitter`         | Divide documentos longos em chunks menores para indexação                      |
| `Embeddings`           | Gera representações vetoriais dos textos                                       |
| `VectorStore`          | Armazena e consulta embeddings (Chroma, Pinecone, Redis, FAISS, etc.)          |
| `Retriever`            | Interface para buscar documentos relevantes dado uma query                     |
| `Chain`                | Composição de passos: prompt → model → parser                                 |
| `LCEL`                 | LangChain Expression Language: sintaxe `a \| b \| c` para compor Runnables    |
| `RunnableParallel`     | Executa múltiplos Runnables em paralelo e combina os resultados                |
| `OutputParser`         | Transforma a saída do modelo (ex: `StrOutputParser`, `JsonOutputParser`)       |

## Pré-requisitos

- Python 3.11+
- Chave de API da OpenAI (`OPENAI_API_KEY` no `.env`)
- Chave de API do Pinecone (`PINECONE_API_KEY` no `.env`) para os exemplos ex04–ex06
- Docker com `redis/redis-stack` para o ex07

## Instalação

```bash
pip install -r requirements.txt
```

## Variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
OPENAI_API_KEY=sk-...
PINECONE_API_KEY=pcsk_...
REDIS_URL=redis://localhost:6379
```
