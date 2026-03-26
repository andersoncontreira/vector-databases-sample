import os
from dotenv import load_dotenv
from pinecone import Pinecone
from openai import OpenAI

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

pc = Pinecone(api_key=PINECONE_API_KEY)
openai_client = OpenAI(api_key=OPENAI_API_KEY)

EMBEDDING_MODEL = "text-embedding-3-small"  # dimension = 1536


def get_embedding(text: str) -> list[float]:
    result = openai_client.embeddings.create(input=[text], model=EMBEDDING_MODEL)
    return result.data[0].embedding


index = pc.Index(name="quickstart")

documents = [
    {"id": "1", "text": "The movie was a gripping drama about loss and redemption.", "metadata": {"genre": "drama"}},
    {"id": "2", "text": "A hilarious comedy that will make you laugh from start to finish.", "metadata": {"genre": "comedy"}},
    {"id": "3", "text": "An action-packed thriller with stunning visual effects.", "metadata": {"genre": "action"}},
]

data = [
    {"id": doc["id"], "values": get_embedding(doc["text"]), "metadata": doc["metadata"]}
    for doc in documents
]

index.upsert(vectors=data, namespace="default")
print("Upsert concluído.")

query_text = "emotional story about grief"
query_vector = get_embedding(query_text)

response = index.query(
    vector=query_vector,
    top_k=3,
    include_values=False,
    include_metadata=True,
    namespace="default",
    filter={"genre": {"$eq": "drama"}},
)

print(response)
