import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel, RunnableLambda
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_redis import RedisVectorStore
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


#  Criado. Para rodar, suba o Redis com Docker e instale a lib:
#
#   # Redis com suporte a vetores (RediSearch)
#   docker run -d --name redis -p 6379:6379 redis/redis-stack:latest
#
#   # Dependência
#   pip install langchain-redis redis
#
#   O exemplo:
#   - Indexa os arquivos de países de data/texts/ no Redis sob o índice countries-index
#   - Faz uma busca direta com similarity_search
#   - Monta o mesmo pipeline RAG do ex06 usando o Redis como retriever
#
#   A estrutura é idêntica ao ex06, só trocando PineconeVectorStore por RedisVectorStore — boa para comparar as duas abordagens lado a lado.

# pip install langchain-redis redis

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")

model = ChatOpenAI(model="gpt-5-nano")
embeddings = OpenAIEmbeddings(api_key=openai_key, model="text-embedding-3-small")

INDEX_NAME = "countries-index"

# --- Indexação ---
# Carrega e indexa os documentos de texto (países)
txt_loader = DirectoryLoader("../data/texts", glob="*.txt", loader_cls=TextLoader)
documents = txt_loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(documents)
print(f"Number of chunks: {len(chunks)}")

vector_store = RedisVectorStore.from_documents(
    documents=chunks,
    embedding=embeddings,
    index_name=INDEX_NAME,
    redis_url=redis_url,
)
print(f"Index '{INDEX_NAME}' criado e populado.")

# --- Query direta ---
results = vector_store.similarity_search("What is the capital of France?", k=3)
print("\n--- Similarity Search Results ---")
for doc in results:
    print(doc.page_content[:200])
    print("---")

# --- RAG com retriever ---
retriever = vector_store.as_retriever()

system_prompt = (
    "You are an assistant for question-answering. "
    "Use the following pieces of context to answer the question at the end. "
    "If you don't know the answer, just say that you don't know, don't try to make up an answer. "
    "Context: {context}"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


chain = (
    RunnableParallel({"context": retriever | RunnableLambda(format_docs), "input": RunnablePassthrough()})
    | prompt
    | model
    | StrOutputParser()
)

question = "How many states does Brazil have?"
response = chain.invoke(question)
print(f"\n--- RAG Response ---\n{response}")
