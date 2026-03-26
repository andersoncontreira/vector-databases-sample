import os
from fileinput import close

from dotenv import load_dotenv
import chromadb
from openai import OpenAI
from chromadb.utils import embedding_functions

from data_utils import split_text, get_openai_embedding, load_data_from_directory

# pip install pypdf

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
openai_client = OpenAI(api_key=openai_api_key)
openai_ef = embedding_functions.OpenAIEmbeddingFunction(api_key=openai_api_key, model_name="text-embedding-3-small")

client = chromadb.PersistentClient(path="./db/chroma_db_llm_sample")
collection_name = "articles"

collection = client.get_or_create_collection(name=collection_name, embedding_function=openai_ef)


def query_documents(query):
    query_text = f"Find information about {query}"
    return collection.query(query_texts=[query_text], n_results=3)


results = query_documents("Carreira de Desenvolvedor")

for doc in results['documents'][0]:
    print(f"doc: {doc}")


results = query_documents("Plano de carreira")

for doc in results['documents'][0]:
    print(f"doc: {doc}")