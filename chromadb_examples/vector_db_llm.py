import os
from fileinput import close

from dotenv import load_dotenv
import chromadb
from openai import OpenAI
from chromadb.utils import embedding_functions

from chromadb_examples.data_utils import split_text, get_openai_embedding
from data_utils import load_data_from_directory

# pip install pypdf

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
openai_client = OpenAI(api_key=openai_api_key)
openai_ef = embedding_functions.OpenAIEmbeddingFunction(api_key=openai_api_key, model_name="text-embedding-3-small")

client = chromadb.PersistentClient(path="./db/chroma_db_llm_sample")
collection_name = "articles"

collection = client.get_or_create_collection(name=collection_name, embedding_function=openai_ef)

documents = load_data_from_directory("./data/articles")
# print(documents)
print (f"Number of documents: {len(documents)}")

print("Chunking documents...")
chunked_documents = []
for doc in documents:
    chunks = split_text(doc["text"])

    for i, chunk in enumerate(chunks):
        chunked_documents.append({"id": doc["id"], "text": chunk, "chunk_id": i})

print("Number of chunked documents: ", len(chunked_documents))

print("Getting embeddings for chunked documents...")
for doc in chunked_documents:
    text = doc["text"]
    embedding = get_openai_embedding(text, open_ai_client=openai_client, model="text-embedding-3-small")
    doc["embedding"] = embedding

print("Upserting chunked documents...")
for doc in chunked_documents:
    collection.upsert(documents=[doc["text"]], ids=[doc["id"]], embeddings=[doc["embedding"]])


query = "Carreira de Desenvolvedor"
query_text = f"Find information about {query}"

results = collection.query(query_texts=[query_text], n_results=3)

for doc in results['documents'][0]:
    print(f"doc: {doc}")
