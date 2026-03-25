import chromadb

chromadb_client = chromadb.Client()

colection_name = "test_collection"

collection = chromadb_client.get_or_create_collection(name=colection_name)
print(f"Collection '{colection_name}' is ready for use.")

documents = [
    {"id": "doc1", "text": "This is the first document."},
    {"id": "doc2", "text":"This document is the second document."},
    {"id": "doc3", "text":"And this is the third one."},
    {"id": "doc4", "text":"Is this the first document?"}
]

for doc in documents:
    collection.upsert(documents=[doc["text"]], ids=[doc["id"]])

query_text = "first document"

results = collection.query(query_texts=[query_text], n_results=3)
print("Query Results:")
# print(results)
# for result in results['documents'][0]:
#     print(result)

for index, document in enumerate(results['documents'][0]):
    # print(f"Result {index + 1}: {doc}")
    doc_id = results['ids'][0][index]
    distance = results['distances'][0][index]
    print(f"Result {index + 1}: Document ID: {doc_id}, Distance: {distance} => {document}")
