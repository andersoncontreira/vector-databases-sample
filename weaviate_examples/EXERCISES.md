# Exercícios — Weaviate

> Sugestões de exercícios para aprofundar os conceitos do Weaviate, organizados por nível de complexidade.

---

## Nível 1 — Fundamentos

### Exercício 1.1 — Criar e explorar schema
Crie uma classe `Country` com propriedades `name` (text), `capital` (text), `continent` (text) e `population` (int). Inspecione o schema via REST (`GET /v1/schema`) e pela interface gráfica do Weaviate.

### Exercício 1.2 — CRUD básico
Insira um objeto, recupere-o pelo UUID, atualize a propriedade `capital` com `collection.data.update()` e delete com `collection.data.delete_by_id()`. Confirme cada operação com um `fetch_objects`.

### Exercício 1.3 — Inserção em lote
Use `collection.data.insert_many()` para inserir todos os países de uma vez. Compare o tempo com inserções individuais em loop.

### Exercício 1.4 — Filtros escalares básicos
Use `Filter.by_property("continent").equal("América do Sul")` para recuperar apenas países de um continente. Experimente também `like` (match parcial) e `contains_any`.

---

## Nível 2 — Busca vetorial

### Exercício 2.1 — near_vector com embedding externo
Gere um embedding com `sentence-transformers` e use `collection.query.near_vector()` para buscar objetos similares. Exiba os campos `certainty` ou `distance` de cada resultado.

### Exercício 2.2 — Limite de distância
Use o parâmetro `distance=0.3` na query `near_vector` para retornar apenas objetos com distância menor que o threshold. Observe como o número de resultados varia com diferentes thresholds.

### Exercício 2.3 — return_properties seletivo
Execute uma busca retornando apenas os campos `name` e `capital`, sem o embedding. Compare o tamanho da resposta com e sem `include_vector=True`.

### Exercício 2.4 — near_object
Use `collection.query.near_object(near_object=uuid)` para encontrar objetos similares a um objeto já indexado, sem precisar gerar um novo embedding.

---

## Nível 3 — Busca híbrida

### Exercício 3.1 — Hybrid search básica
Execute `collection.query.hybrid(query="tropical rainforest", alpha=0.5, limit=5)`. Inspecione os scores e compare com os resultados de `near_vector` pura.

### Exercício 3.2 — Ajustar alpha
Execute a mesma query com `alpha=0.0` (BM25 puro), `alpha=0.5` (híbrido) e `alpha=1.0` (vetorial puro). Tabule os documentos retornados em cada caso e identifique quando cada abordagem é melhor.

### Exercício 3.3 — Hybrid com filtro
Combine hybrid search com `Filter.by_property("continent").equal("Europa")`. Verifique que os resultados são filtrados antes do ranqueamento híbrido.

### Exercício 3.4 — Fusion ranking
O Weaviate suporta dois algoritmos de fusion: `rankedFusion` e `relativeScoreFusion`. Compare os resultados de ambos para queries onde os resultados BM25 e vetorial divergem.

---

## Nível 4 — Aggregations e análise

### Exercício 4.1 — Count por grupo
Use `collection.aggregate.over_all(group_by=GroupByAggregate(prop="continent"))` para contar países por continente.

### Exercício 4.2 — Média e soma
Adicione a propriedade `area_km2` (number) aos objetos. Calcule a área média e a soma por continente usando `MetaCount`, `Mean` e `Sum` nas aggregations.

### Exercício 4.3 — Aggregation com near_vector
Execute uma aggregation apenas sobre os objetos mais similares a uma query: use `near_vector` combinado com `object_limit` nas aggregations para analisar apenas os N objetos mais relevantes.

---

## Nível 5 — Projetos integradores

### Projeto 5.1 — Enciclopédia de países com busca híbrida
Indexe os arquivos `data/texts/*.txt` com schema rico. Implemente uma CLI que:
- Aceita queries em linguagem natural
- Usa busca híbrida (alpha=0.6)
- Filtra por continente se mencionado na query
- Exibe o país de origem de cada resultado

### Projeto 5.2 — Comparativo Weaviate vs ChromaDB
Indexe o mesmo conjunto de documentos nos dois sistemas. Para 20 queries, compare: resultados retornados, scores, latência e facilidade da API. Documente as diferenças em um relatório.

### Projeto 5.3 — Multi-tenancy
Configure multi-tenancy na coleção `Country`. Crie três tenants (`tenant_a`, `tenant_b`, `tenant_c`) e insira conjuntos diferentes de países em cada um. Verifique que queries de um tenant não retornam dados de outro.
