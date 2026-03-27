# Exercícios — Amazon S3 Vectors

> Sugestões de exercícios para aprofundar os conceitos do Amazon S3 Vectors, organizados por nível de complexidade.

---

## Nível 1 — Fundamentos

### Exercício 1.1 — Criar o primeiro índice
Configure as credenciais AWS e crie um Vector Index com `dimension=1536` e `distanceMetric="cosine"`. Inspecione o índice criado com `s3vectors.describe_index()`.

### Exercício 1.2 — Listar índices
Use `s3vectors.list_indexes(vectorBucketName="...")` para listar todos os índices do bucket. Implemente uma função que exibe nome, dimensão e métrica de cada índice.

### Exercício 1.3 — Credenciais e perfis AWS
Teste a conexão usando três métodos de autenticação:
- Variáveis de ambiente (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`)
- Perfil nomeado (`boto3.Session(profile_name="...")`)
- IAM Role (se disponível em ambiente EC2/Lambda)

### Exercício 1.4 — Deletar e recriar índice
Delete o índice com `s3vectors.delete_index()` e recrie com configurações diferentes (ex: `distanceMetric="euclidean"`). Verifique que o índice anterior foi removido antes da recriação.

---

## Nível 2 — Inserção e busca

### Exercício 2.1 — Upsert com Titan Embeddings
Use o Amazon Titan Embeddings V2 (`amazon.titan-embed-text-v2:0`) para gerar embeddings dos arquivos `data/texts/*.txt`. Insira os vetores com metadados ricos.

### Exercício 2.2 — Upsert em batch
Compare o tempo de inserção de 100 vetores usando:
- Um vetor por chamada `put_vectors()`
- 10 vetores por chamada (batch de 10)
- 100 vetores em uma única chamada

### Exercício 2.3 — Query básica
Execute `query_vectors()` com `topK=5` e `returnMetadata=True`. Inspecione os campos `key`, `score` e `metadata` de cada resultado.

### Exercício 2.4 — Comparar modelos de embedding
Indexe os mesmos documentos com dois modelos:
- `amazon.titan-embed-text-v2:0` (1536 dims)
- `sentence-transformers/all-MiniLM-L6-v2` local (384 dims, em índice separado)

Compare a qualidade dos resultados de busca para as mesmas queries.

---

## Nível 3 — Metadados e filtragem

### Exercício 3.1 — Metadados estruturados
Insira vetores com metadados como `{"country": "Brasil", "continent": "América do Sul", "language": "pt", "population": 215}`. Use `returnMetadata=True` para recuperá-los nas queries.

### Exercício 3.2 — Filtro por metadados
Execute queries com filtros de metadados (sintaxe disponível na versão atual da API). Filtre por `country` e `continent` e compare com queries sem filtro.

### Exercício 3.3 — Get e delete por chave
Use `get_vectors(keys=["doc1", "doc2"])` para recuperar vetores específicos. Delete vetores individuais com `delete_vectors(keys=[...])`. Confirme com uma query que os deletados não aparecem mais.

---

## Nível 4 — Integração AWS

### Exercício 4.1 — Pipeline com S3 + S3 Vectors
Crie um pipeline que:
1. Lê arquivos TXT de um bucket S3 comum
2. Gera embeddings com Titan via Bedrock
3. Insere no S3 Vectors
4. Executa uma query de busca

### Exercício 4.2 — Lambda de indexação
Implemente uma AWS Lambda que é acionada quando um novo arquivo é adicionado ao S3 (evento `s3:ObjectCreated`). A Lambda deve gerar o embedding e fazer upsert no S3 Vectors automaticamente.

### Exercício 4.3 — Custos
Use o AWS Cost Explorer para monitorar o custo do S3 Vectors após os exercícios. Compare o custo estimado com Pinecone serverless para o mesmo volume de vetores e queries.

### Exercício 4.4 — IAM Policies
Crie uma IAM Policy mínima com apenas as permissões necessárias para S3 Vectors (`s3vectors:PutVectors`, `s3vectors:QueryVectors`, etc.). Aplique o princípio do least privilege.

---

## Nível 5 — Projetos integradores

### Projeto 5.1 — Pipeline RAG serverless
Construa um pipeline RAG 100% serverless na AWS:
- **S3** → armazena os documentos originais
- **Lambda** → processa e indexa automaticamente novos documentos
- **Bedrock (Titan Embeddings)** → gera embeddings
- **S3 Vectors** → armazena e consulta vetores
- **Bedrock (Claude)** → gera respostas

### Projeto 5.2 — Comparativo S3 Vectors vs Pinecone
Para o mesmo dataset e as mesmas queries, compare:
- Latência de upsert e query
- Custo estimado por 1M de vetores e 100K queries/mês
- Facilidade de configuração e operação
- Limitações de filtragem por metadados

### Projeto 5.3 — Indexação de documentos de países
Indexe os arquivos `data/texts/*.txt` no S3 Vectors usando Titan Embeddings. Implemente um script de query que responde perguntas sobre os países, exibindo o score de similaridade e o trecho recuperado.
