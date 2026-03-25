# Amazon S3 Vectors Examples

> **Nota:** Este é um projeto de estudo. Os exercícios aqui descritos têm fins educacionais.

## O que é o Amazon S3 Vectors?

Amazon S3 Vectors é uma funcionalidade do S3 que permite armazenar e consultar vetores diretamente em **buckets S3**, sem precisar de um banco de dados vetorial separado. Lançado em 2025, oferece uma camada de armazenamento vetorial serverless e de baixo custo, integrada ao ecossistema AWS.

Cada bucket S3 pode conter **vector indexes** — índices que armazenam embeddings com metadados e permitem busca por similaridade via API.

## Quando usar o S3 Vectors?

- Você já está no ecossistema AWS e quer minimizar o número de serviços gerenciados.
- O volume de vetores é muito grande, mas as consultas não precisam de latência ultra-baixa (ex: processamento batch).
- Quer pagar apenas pelo armazenamento e pelas queries realizadas (modelo serverless/pay-per-use).
- Precisa de uma solução durável e escalável para armazenar embeddings gerados por pipelines de dados.
- Está construindo pipelines de RAG offline onde o retrieval não é em tempo real.
- Quer integrar busca vetorial diretamente com outros serviços AWS (Lambda, Bedrock, Glue).

## Quando NÃO usar o S3 Vectors?

- Sua aplicação exige busca vetorial em tempo real com baixa latência (< 100ms).
- Precisa de filtragem avançada de metadados combinada com busca vetorial.
- O caso de uso envolve atualizações frequentes de vetores.

## Pré-requisitos

- Conta AWS com permissões para S3 e Bedrock (ou outro modelo de embedding)
- Python 3.11+
- Bibliotecas: `boto3`, `sentence-transformers`

```bash
pip install boto3 sentence-transformers
```

## Configuração de credenciais AWS

```bash
# Via AWS CLI
aws configure

# Ou via variáveis de ambiente
export AWS_ACCESS_KEY_ID="..."
export AWS_SECRET_ACCESS_KEY="..."
export AWS_DEFAULT_REGION="us-east-1"

# Ou via perfil nomeado
export AWS_PROFILE="nome-do-perfil"
```

## Conceitos-chave

| Conceito      | Equivalente             | Descrição                                                              |
|---------------|-------------------------|------------------------------------------------------------------------|
| Bucket        | Banco de dados          | Container principal do S3 que habilita o recurso de vector indexes     |
| Vector Index  | Coleção / tabela        | Índice vetorial dentro de um bucket, com configuração de dimensão      |
| Vector        | Ponto / linha           | Um embedding com chave (key), dados vetoriais e metadados opcionais    |
| Key           | ID                      | Identificador único do vetor dentro do índice                          |
| Metadata      | Payload / colunas extra | Dados JSON associados ao vetor, usados para filtragem e contexto       |

## Caminho de exercícios

### Exercício 1 — Configuração e criação do Vector Index

**Objetivo:** criar um bucket S3 habilitado para vetores e configurar o primeiro índice.

**Tarefas:**
- [ ] Configurar as credenciais AWS no ambiente local
- [ ] Criar um bucket S3 com suporte a Vector Index via console ou boto3
- [ ] Criar um Vector Index com `dimension=1536` (Titan Embeddings V2) ou `dimension=384` (MiniLM)
- [ ] Listar os índices existentes no bucket
- [ ] Verificar as configurações do índice criado

**Exemplo:**
```python
import boto3

s3vectors = boto3.client("s3vectors", region_name="us-east-1")

s3vectors.create_index(
    vectorBucketName="meu-bucket-vetorial",
    indexName="meu-indice",
    dataType="float32",
    dimension=1536,
    distanceMetric="cosine",
)
```

---

### Exercício 2 — Gerando embeddings com Amazon Bedrock

**Objetivo:** usar o Amazon Titan Embeddings como modelo de embedding integrado à AWS.

**Tarefas:**
- [ ] Configurar o cliente Bedrock Runtime
- [ ] Invocar o modelo `amazon.titan-embed-text-v2:0` para gerar embeddings
- [ ] Comparar com embeddings gerados pelo `sentence-transformers` localmente
- [ ] Criar uma função utilitária reutilizável para geração de embeddings via Bedrock

**Exemplo:**
```python
import boto3
import json

bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

def get_embedding(text):
    response = bedrock.invoke_model(
        modelId="amazon.titan-embed-text-v2:0",
        body=json.dumps({"inputText": text}),
        contentType="application/json",
        accept="application/json",
    )
    return json.loads(response["body"].read())["embedding"]
```

---

### Exercício 3 — Inserindo vetores no S3 Vectors

**Objetivo:** popular o índice com documentos e seus embeddings.

**Tarefas:**
- [ ] Gerar embeddings para uma lista de documentos
- [ ] Inserir vetores com `put_vectors()`, incluindo `key`, `data` e `metadata`
- [ ] Inserir em lote para otimizar o número de chamadas à API
- [ ] Verificar a contagem de vetores no índice

**Exemplo:**
```python
s3vectors.put_vectors(
    vectorBucketName="meu-bucket-vetorial",
    indexName="meu-indice",
    vectors=[
        {
            "key": "doc1",
            "data": {"float32": embedding},
            "metadata": {"text": "conteúdo do documento", "category": "tecnologia"},
        }
    ],
)
```

---

### Exercício 4 — Busca por similaridade

**Objetivo:** consultar os vetores mais similares a uma query.

**Tarefas:**
- [ ] Gerar o embedding do texto de consulta
- [ ] Executar `query_vectors()` com `topK` e o vetor de query
- [ ] Acessar `key`, `score` e `metadata` de cada resultado
- [ ] Comparar resultados com diferentes métricas: `cosine`, `euclidean`, `dot_product`

**Exemplo:**
```python
query_embedding = get_embedding("Como funciona machine learning?")

results = s3vectors.query_vectors(
    vectorBucketName="meu-bucket-vetorial",
    indexName="meu-indice",
    queryVector={"float32": query_embedding},
    topK=5,
    returnMetadata=True,
)

for r in results["vectors"]:
    print(r["key"], r["score"], r["metadata"])
```

---

### Exercício 5 — Filtragem por metadados

**Objetivo:** combinar busca vetorial com filtros sobre os metadados dos vetores.

**Tarefas:**
- [ ] Inserir vetores com metadados variados (ex: `category`, `language`, `year`)
- [ ] Executar queries com filtro de metadados usando a sintaxe do S3 Vectors
- [ ] Comparar performance com e sem filtros
- [ ] Entender as limitações de filtragem em relação ao Qdrant e pgvector

---

### Exercício 6 — Pipeline RAG com S3 Vectors + Bedrock

**Objetivo:** construir um pipeline RAG completo usando apenas serviços AWS.

**Tarefas:**
- [ ] Indexar documentos com embeddings gerados pelo Titan Embeddings
- [ ] Dado uma pergunta, buscar os trechos mais relevantes no S3 Vectors
- [ ] Montar o prompt com o contexto e enviar para o Claude (via Bedrock) ou outro modelo
- [ ] Avaliar a qualidade das respostas e o custo do pipeline

**Arquitetura:**
```
Pergunta do usuário
       ↓
Titan Embeddings (gera vetor da query)
       ↓
S3 Vectors (busca top-K documentos relevantes)
       ↓
Contexto recuperado → Prompt montado
       ↓
Claude / Titan Text (Bedrock) → Resposta final
```

---

### Exercício 7 — Gerenciamento de vetores

**Objetivo:** dominar as operações de manutenção do índice.

**Tarefas:**
- [ ] Buscar um vetor por chave com `get_vectors()`
- [ ] Deletar vetores por chave com `delete_vectors()`
- [ ] Listar vetores do índice com paginação
- [ ] Excluir e recriar o índice para um novo ciclo de testes
- [ ] Monitorar o custo via AWS Cost Explorer

## Referências

- Documentação oficial: https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors.html
- Amazon Titan Embeddings: https://docs.aws.amazon.com/bedrock/latest/userguide/titan-embedding-models.html
- Boto3 S3 Vectors API: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3vectors.html