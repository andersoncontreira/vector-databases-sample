import os
import chromadb
from dotenv import load_dotenv
from chromadb.utils import embedding_functions
from openai import OpenAI

load_dotenv()

from chromadb_examples.data_utils import generate_model_response
openai_api_key = os.getenv("OPENAI_API_KEY")

openai_client = OpenAI(api_key=openai_api_key)
openai_ef = embedding_functions.OpenAIEmbeddingFunction(api_key=openai_api_key, model_name="text-embedding-3-small")

client = chromadb.PersistentClient(path="./db/chroma_db_llm_sample")
collection_name = "articles"

collection = client.get_or_create_collection(name=collection_name, embedding_function=openai_ef)


def query_documents(query_text):
    return collection.query(query_texts=[query_text], n_results=3)


query = "Plano de carreira"
results = query_documents(query)

# for doc in results['documents'][0]:
#     print(f"doc: {doc}")


relevant_chunks = results["documents"][0]
response = generate_model_response(relevant_chunks, query, openai_client, model="gpt-5-nano")

print(f"Model response: {response}")