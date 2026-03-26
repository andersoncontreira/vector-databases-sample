import chromadb

from chromadb.utils import embedding_functions

default_ef = embedding_functions.DefaultEmbeddingFunction()

chromadb_client = chromadb.PersistentClient(path="../db/chroma_db_sample")

collection = chromadb_client.get_or_create_collection(name="my_store", embedding_function=default_ef)


# documents
documents = [
    {"id": "doc1", "text": "This is the first document."},
    {"id": "doc2", "text":"This document is the second document."},
    {"id": "doc3", "text":"And this is the third one."},
    {"id": "doc4", "text":"Is this the first document?"}
]

#collection.upsert(ids=[doc["id"] for doc in documents], documents=[doc["text"] for doc in documents])
for doc in documents:
    collection.upsert(documents=[doc["text"]], ids=[doc["id"]])

query_text = "first document"

results = collection.query(query_texts=[query_text], n_results=3)

for doc in results['documents'][0]:
    print(f"doc: {doc}")