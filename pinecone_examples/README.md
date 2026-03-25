# Pinecone Examples

> **Nota:** Este é um projeto de estudo. Os exercícios aqui descritos têm fins educacionais.

## O que é o Pinecone?

Pinecone é um banco de dados vetorial **totalmente gerenciado na nuvem** (SaaS). Ele abstrai toda a infraestrutura e oferece uma API simples para armazenar e consultar vetores em escala. É uma das soluções mais populares para aplicações de produção que utilizam embeddings.

## Quando usar o Pinecone?

- Você precisa de uma solução pronta para produção sem gerenciar servidores.
- O volume de vetores é muito grande (bilhões de registros).
- Alta disponibilidade e baixa latência são requisitos críticos.
- A equipe não tem capacidade de operar infraestrutura de banco de dados vetorial.
- Você quer focar no produto, não na plataforma.

## Pré-requisitos

- Conta gratuita no Pinecone: https://www.pinecone.io
- Python 3.11+
- Bibliotecas: `pinecone-client`, `sentence-transformers`

```bash
pip install pinecone-client sentence-transformers
```

## Configuração inicial

1. Crie uma conta em https://www.pinecone.io
2. Crie um projeto e obtenha a **API Key**
3. Crie um índice (index) com a dimensão correta para o modelo de embedding escolhido
4. Configure a variável de ambiente:

```bash
export PINECONE_API_KEY="sua-api-key-aqui"
```

## Conceitos-chave

| Conceito   | Equivalente SQL | Descrição                                                    |
|------------|-----------------|--------------------------------------------------------------|
| Index      | Banco de dados  | Unidade principal de armazenamento de vetores                |
| Namespace  | Schema          | Partição lógica dentro de um index                           |
| Vector     | Linha           | Um embedding com ID, valores e metadados opcionais           |
| Metadata   | Colunas extras  | Campos adicionais para filtragem                             |
| Query      | SELECT          | Busca pelos K vetores mais próximos                          |

## Caminho de exercícios

### Exercício 1 — Configuração e criação do índice

**Objetivo:** criar um índice Pinecone e verificar a conexão.

**Tarefas:**
- [ ] Instalar o SDK e configurar a API Key
- [ ] Criar um índice com `dimension=384` e `metric="cosine"`
- [ ] Listar os índices disponíveis na conta
- [ ] Descrever as estatísticas do índice criado (`describe_index_stats`)

**Exemplo:**
```python
import pinecone

pc = pinecone.Pinecone(api_key="sua-api-key")
pc.create_index(name="study-index", dimension=384, metric="cosine")
```

---

### Exercício 2 — Inserindo vetores (upsert)

**Objetivo:** gerar embeddings e inserir no Pinecone.

**Tarefas:**
- [ ] Gerar embeddings com `sentence-transformers`
- [ ] Inserir vetores com `upsert`, incluindo metadados (ex: `{"text": "...", "source": "..."}`)
- [ ] Usar namespaces para organizar os dados por domínio
- [ ] Verificar a contagem de vetores no índice após a inserção

---

### Exercício 3 — Busca por similaridade

**Objetivo:** consultar os vetores mais similares a uma query.

**Tarefas:**
- [ ] Gerar o embedding do texto de consulta
- [ ] Executar `index.query(vector=..., top_k=5, include_metadata=True)`
- [ ] Exibir os resultados com ID, score e metadados
- [ ] Comparar resultados com diferentes métricas (`cosine`, `dotproduct`, `euclidean`)

---

### Exercício 4 — Filtragem por metadados

**Objetivo:** combinar busca vetorial com filtros sobre metadados.

**Tarefas:**
- [ ] Inserir vetores com metadados variados (ex: `category`, `language`, `date`)
- [ ] Executar queries com filtro: `filter={"category": {"$eq": "technology"}}`
- [ ] Entender as limitações dos filtros de metadados no Pinecone
- [ ] Comparar performance com e sem filtro

---

### Exercício 5 — Deleção e atualização de vetores

**Objetivo:** gerenciar o ciclo de vida dos vetores no índice.

**Tarefas:**
- [ ] Deletar vetores por ID (`index.delete(ids=[...])`)
- [ ] Deletar todos os vetores de um namespace
- [ ] Atualizar um vetor fazendo upsert com o mesmo ID
- [ ] Verificar o impacto no `describe_index_stats`

---

### Exercício 6 — Integração com LLM (RAG com Pinecone)

**Objetivo:** construir um pipeline RAG usando Pinecone como retriever em produção.

**Tarefas:**
- [ ] Indexar um conjunto de documentos reais (ex: FAQs, artigos)
- [ ] Implementar a etapa de retrieval: dada uma pergunta, buscar os top-K trechos relevantes
- [ ] Montar o prompt com contexto e enviar para uma LLM
- [ ] Explorar o uso de namespaces para separar contextos diferentes (ex: por usuário ou produto)

---

### Exercício 7 — Serverless vs. Pod-based

**Objetivo:** entender as duas arquiteturas de deploy do Pinecone.

**Tarefas:**
- [ ] Criar um índice serverless e um pod-based (starter)
- [ ] Comparar latência, custo e limitações de cada abordagem
- [ ] Entender quando usar cada um em cenários de produção

## Referências

- Documentação oficial: https://docs.pinecone.io
- Quickstart: https://docs.pinecone.io/guides/get-started/quickstart
- SDK Python: https://github.com/pinecone-io/pinecone-python-client