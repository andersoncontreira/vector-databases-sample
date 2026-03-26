Claude e Bedrock no Chroma.

Combinacoes de cenario de arquivos com embeddings com bedrock + exercicio com Claude.

Sim — são duas decisões separadas:
	1.	quem gera os embeddings
	2.	quem gera a resposta final

O Chroma só precisa que os embeddings de indexação e de busca sejam gerados de forma consistente. Claude entra na síntese da resposta, não na parte de embeddings. A API do Claude é baseada no endpoint de Messages, enquanto embeddings no seu exemplo atual vêm da OpenAI; no lado AWS, o Titan Text Embeddings é um modelo de embeddings do Bedrock e pode ser invocado via InvokeModel.  ￼

Então, respondendo à sua dúvida principal:
	•	Não, você não precisa usar o arquivo do Bedrock só porque vai usar Claude.
	•	Você só precisa mudar para aquele arquivo do Bedrock se quiser que os embeddings também saiam do Bedrock, como Titan.  ￼

Na prática, você tem três combinações válidas.

Opção 1 — manter OpenAI para embeddings e usar Claude para resposta

Essa é a mudança mínima. Você mantém:
	•	OpenAIEmbeddingFunction(...)
	•	a mesma collection do Chroma já indexada com OpenAI embeddings

E troca apenas a função de geração da resposta para usar Claude. Isso funciona porque embeddings e geração são camadas diferentes.  ￼

Opção 2 — usar Titan para embeddings e Claude para resposta

Aí sim você usa sua BedrockEmbeddingFunction(...) para indexar e consultar no Chroma, e usa Claude só na hora de responder. O detalhe importante é que, se sua collection foi criada/indexada com OpenAI embeddings, você não deve só trocar a função de embedding e continuar usando a mesma base; precisa criar outra collection ou reindexar, porque os vetores precisam vir do mesmo modelo/família para indexação e consulta. O Titan Text Embeddings é um modelo próprio do Bedrock, com IDs e características próprias.  ￼

Opção 3 — usar Bedrock para tudo

Você pode usar:
	•	Titan para embeddings
	•	Claude via Bedrock para resposta

Isso faz sentido quando você quer concentrar tudo em AWS. O Bedrock suporta inferência por InvokeModel, e Titan é parte da família de modelos do Amazon Titan.  ￼

O ponto mais importante no seu código

Hoje seu fluxo é este:
	•	PDFs/artigos
	•	embeddings com OpenAI
	•	Chroma
	•	gpt-5-nano para sintetizar

Se você quiser trocar só o modelo de resposta para Claude, seu código de embeddings pode ficar igual. Você só troca esta parte:

response = generate_model_response(relevant_chunks, query, openai_client, model="gpt-5-nano")

por algo que use o cliente da Anthropic.

Exemplo: OpenAI embeddings + Claude para resposta

import os
import chromadb
from dotenv import load_dotenv
from chromadb.utils import embedding_functions
import anthropic

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=openai_api_key,
    model_name="text-embedding-3-small"
)

anthropic_client = anthropic.Anthropic(api_key=anthropic_api_key)

client = chromadb.PersistentClient(path="./db/chroma_db_llm_sample")
collection = client.get_or_create_collection(
    name="articles",
    embedding_function=openai_ef
)

def query_documents(query_text):
    return collection.query(query_texts=[query_text], n_results=3)

def generate_claude_response(relevant_chunks, query, anthropic_client, model="claude-sonnet-4-5"):
    context = "\n\n".join(relevant_chunks[:5]).strip()

    if not context:
        return "I don't know based on the retrieved documents."

    system_prompt = (
        "You are a helpful assistant that answers questions only using the provided context. "
        "Do not invent facts. "
        "If the answer is not clearly supported by the context, say: "
        "'I don't know based on the retrieved documents.' "
        "Keep the answer concise, with a maximum of 3 sentences."
    )

    user_prompt = (
        f"Question:\n{query}\n\n"
        f"Context:\n{context}\n\n"
        "Answer using only the context above."
    )

    response = anthropic_client.messages.create(
        model=model,
        max_tokens=300,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_prompt}
        ]
    )

    return "".join(
        block.text for block in response.content if block.type == "text"
    )

query = "Plano de carreira"
results = query_documents(query)
relevant_chunks = results["documents"][0]

response = generate_claude_response(relevant_chunks, query, anthropic_client)
print(response)

Isso segue o padrão da Messages API do Claude, em que você envia system, messages e recebe blocos de conteúdo textual na resposta.  ￼

Quando você precisa usar o arquivo com Bedrock embeddings

Você usa sua BedrockEmbeddingFunction quando quiser algo assim:
	•	indexar com amazon.titan-embed-text-v1 ou v2
	•	consultar o Chroma também com Titan
	•	manter embeddings no ecossistema AWS

Exemplo de raciocínio:

bedrock_ef = BedrockEmbeddingFunction(
    model_id="amazon.titan-embed-text-v1",
    region_name="us-east-1",
    profile_name="newstacktrace-dev"
)

collection = chromadb_client.get_or_create_collection(
    name="articles_bedrock",
    embedding_function=bedrock_ef
)

Mas repare no nome novo da collection: eu faria isso de propósito para não misturar uma base indexada com OpenAI com outra baseada em Titan. O Titan v2 e v1 têm especificações e limites próprios, e a AWS recomenda chunking lógico dos documentos.  ￼

Arquitetura correta para pensar

Pensa assim:

[artigos/PDFs]
   -> [embedding model]
   -> [ChromaDB]
   -> [top-k chunks]
   -> [LLM de resposta]

Você pode combinar assim:
	•	OpenAI embeddings + GPT
	•	OpenAI embeddings + Claude
	•	Titan embeddings + GPT
	•	Titan embeddings + Claude

Tudo isso é válido, desde que a etapa de embeddings seja consistente entre ingestão e query.  ￼

Minha recomendação para o seu caso

Para estudo e simplicidade:
	•	mantenha OpenAI embeddings
	•	troque só a função de resposta para Claude

Para ficar mais próximo do ambiente da empresa:
	•	crie uma segunda collection
	•	use Titan embeddings
	•	depois escolha GPT ou Claude para a resposta

O que eu faria no seu projeto agora

Eu criaria uma abstração simples:

class AnswerGenerator:
    def generate(self, relevant_chunks, query):
        raise NotImplementedError

e duas implementações:
	•	OpenAIAnswerGenerator
	•	ClaudeAnswerGenerator

E, separadamente:
	•	OpenAIEmbeddingProvider
	•	BedrockEmbeddingProvider

Assim você consegue testar combinações sem reescrever tudo.

O resumo é este: Claude não obriga Bedrock embeddings. Você só usa aquele segundo arquivo se também quiser trocar a camada de embeddings para Titan. Se quiser, eu posso te devolver isso já organizado em dois arquivos, por exemplo embedding_provider.py e answer_generator.py, com exemplo para OpenAI, Bedrock e Claude.