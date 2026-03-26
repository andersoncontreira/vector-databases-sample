import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

pinecone = Pinecone(api_key=PINECONE_API_KEY)


# If you are using:
# 	•	OpenAI text-embedding-3-small → 1536 dimensions
# 	•	OpenAI text-embedding-3-large → 3072 dimensions
# Then your Pinecone index must match:
# create a serverless index
# metric="cosine", "euclidean", "dotproduct"


indexes = [idx.name for idx in pinecone.list_indexes()]

# check if existing indexes have the same metric
if "quickstart" not in indexes:
    index = pinecone.create_index(name="quickstart",
                                  dimension=1536,
                                  metric="euclidean",
                                  spec=ServerlessSpec(
                                    cloud="aws",
                                    region="us-east-1"
                                  ))

if "quickstart-1024" not in indexes:
    index1024 = pinecone.create_index(name="quickstart-1024",
                                  dimension=1024,
                                  metric="cosine",
                                  spec=ServerlessSpec(
                                    cloud="aws",
                                    region="us-east-1"
                                  ))


# embedding = pinecone.embeddings.create(
#     model="text-embedding-3-small",
#     input="hello world"
# )
#
# len(embedding.data[0].embedding)  # → 1536