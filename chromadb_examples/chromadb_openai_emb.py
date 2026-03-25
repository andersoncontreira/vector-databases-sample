import os

import chromadb
from dotenv import load_dotenv
from chromadb.utils import embedding_functions

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

# default_ef = embedding_functions.DefaultEmbeddingFunction()
openai_ef = embedding_functions.OpenAIEmbeddingFunction(api_key=openai_api_key, model_name="text-embedding-3-small")

chromadb_client = chromadb.PersistentClient(path="./db/chroma_db_openai_sample")

collection = chromadb_client.get_or_create_collection(name="my_store", embedding_function=openai_ef)

documents = [
    {"id": "doc1", "text": "This is the first document."},
    {"id": "doc2", "text":"THe Microsoft is a technology company based in Redmond, Washington."},
    {"id": "doc3", "text":"The Eiffel Tower is a famous landmark located in Paris, France."},
    {"id": "doc4", "text":"The Great Wall of China is a historic fortification that stretches across northern China."},
    {"id": "doc5", "text":"The Amazon rainforest is the largest tropical rainforest in the world, covering much of South America."},
    {"id": "doc6", "text":"The Great Pyramid of Giza is a giant pyramid in Egyptian desert."},
    {"id": "doc7", "text":"The Hague is the capital city of the Netherlands."},
    {"id": "doc8", "text":"The Grand Canyon is a natural wonder located in Arizona, USA."},
    {"id": "doc9", "text":"The Taj Mahal is a mausoleum located in Agra, India."},
    {"id": "doc10", "text":"The Sydney Opera House is a famous performing arts center located in Sydney, Australia."}
]

for doc in documents:
    collection.upsert(documents=[doc["text"]], ids=[doc["id"]])

query_text = "Find text about places in the world"

results = collection.query(query_texts=[query_text], n_results=3)


for doc in results['documents'][0]:
    distance = results['distances'][0][0]
    print(f"doc: {doc}, distance: {distance}")

query_text = "Find information about companies in the world"

results = collection.query(query_texts=[query_text], n_results=3)

for doc in results['documents'][0]:
    distance = results['distances'][0][0]
    print(f"doc: {doc}, distance: {distance}")

