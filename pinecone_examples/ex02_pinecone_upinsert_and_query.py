import os
from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

pc = Pinecone(api_key=PINECONE_API_KEY)

# Modelo hospedado pelo Pinecone — dimension = 1024
# Atenção: o índice "quickstart" deve ter sido criado com dimension=1024
# Modelos disponíveis: https://docs.pinecone.io/guides/inference/understanding-inference#embedding-models
EMBEDDING_MODEL = "multilingual-e5-large"


def get_embedding(text: str) -> list[float]:
    res = pc.inference.embed(
        model=EMBEDDING_MODEL,
        inputs=[text],
        parameters={"input_type": "passage"},
    )
    return res.data[0].values


index = pc.Index(name="quickstart-1024")

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
