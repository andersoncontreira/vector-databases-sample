# Vector Databases Sample

> **Nota:** Este é um projeto de estudo sobre bancos de dados vetoriais. O objetivo é explorar diferentes soluções disponíveis no mercado, entender suas características, casos de uso e como integrá-las em aplicações Python.

## O que são bancos de dados vetoriais?

Bancos de dados vetoriais são sistemas especializados em armazenar e consultar **embeddings** — representações numéricas de dados (textos, imagens, áudio) em espaços de alta dimensão. Em vez de buscas exatas por igualdade, eles realizam **busca por similaridade** (nearest neighbor search), retornando os itens semanticamente mais próximos de uma consulta.

São a espinha dorsal de aplicações modernas como:
- Sistemas RAG (Retrieval-Augmented Generation) com LLMs
- Motores de busca semântica
- Sistemas de recomendação
- Detecção de duplicatas e anomalias

## Bancos de dados estudados

| Banco de dados       | Tipo               | Status    | Pasta                  |
|----------------------|--------------------|-----------|------------------------|
| ChromaDB             | Embarcado / local  | Concluído | `chromadb_examples/`   |
| PostgreSQL+pgvector  | Relacional+vetor   | A estudar | `pgvector_examples/`   |
| Pinecone             | Cloud gerenciado   | A estudar | `pinecone_examples/`   |
| Weaviate             | Distribuído        | A estudar | `weaviate_examples/`   |
| Qdrant               | Distribuído        | A estudar | `qdrant_examples/`     |

## Comparativo geral

| Banco de dados      | Hospedagem          | Escala        | Ideal para                                             |
|---------------------|---------------------|---------------|--------------------------------------------------------|
| ChromaDB            | Local / self-hosted | Pequena/média | Prototipagem, uso local, projetos acadêmicos           |
| PostgreSQL+pgvector | Self-hosted / cloud | Média/grande  | Quem já usa Postgres e quer evitar nova infraestrutura |
| Pinecone            | Cloud gerenciado    | Grande        | Produção sem ops, alta disponibilidade                 |
| Weaviate            | Self-hosted / cloud | Grande        | Busca semântica rica, GraphQL, multimodal              |
| Qdrant              | Self-hosted / cloud | Grande        | Alta performance, filtragem avançada, Rust-based       |

## Estrutura do projeto

```
vector-databases-sample/
├── README.md                  # Este arquivo
├── chromadb_examples/         # Exemplos com ChromaDB (concluído)
├── pgvector_examples/         # Exemplos com PostgreSQL + pgvector
├── pinecone_examples/         # Exemplos com Pinecone
├── weaviate_examples/         # Exemplos com Weaviate
├── qdrant_examples/           # Exemplos com Qdrant
└── scripts/                   # Scripts utilitários gerais
```

## Caminho de estudo sugerido

A ordem abaixo foi pensada para ir do mais simples ao mais complexo, construindo conhecimento progressivamente:

```
1. ChromaDB        → conceitos base, API simples, uso local
2. pgvector        → integração com SQL, extensão do Postgres
3. Qdrant          → performance, filtros avançados, client REST/gRPC
4. Weaviate        → busca semântica avançada, schema, GraphQL
5. Pinecone        → produção em nuvem, serverless, alta escala
```

## Pré-requisitos gerais

- Python 3.11+
- Docker (para pgvector, Qdrant e Weaviate)
- Conta na Pinecone (gratuita para estudo)
- Familiaridade básica com o conceito de embeddings