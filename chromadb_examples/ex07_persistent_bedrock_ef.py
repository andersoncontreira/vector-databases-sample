import os

import chromadb
from dotenv import load_dotenv
import boto3
import json

# pip install boto3
load_dotenv()

# Função customizada para gerar embeddings usando Bedrock
class BedrockEmbeddingFunction:
    def __init__(self, model_id, region_name, profile_name=None):
        self.model_id = model_id
        self.region_name = region_name
        if profile_name:
            session = boto3.Session(profile_name=profile_name, region_name=region_name)
            self.client = session.client("bedrock-runtime")
        else:
            self.client = boto3.client("bedrock-runtime", region_name=region_name)

    def __call__(self, input):
        if isinstance(input, str):
            input = [input]
        embeddings = []
        for text in input:
            body = json.dumps({"inputText": text})
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=body,
                contentType="application/json",
                accept="application/json"
            )
            response_body = json.loads(response["body"].read())
            embeddings.append(response_body["embedding"])
        return embeddings

    def embed_documents(self, input):
        return self.__call__(input)

    def embed_query(self, input):
        return self.__call__(input)

    def name(self):
        return "bedrock"

# Parâmetros do Bedrock
bedrock_model_id = os.getenv("BEDROCK_MODEL_ID", "amazon.titan-embed-text-v1")
bedrock_region = os.getenv("BEDROCK_REGION", "us-east-1")
bedrock_profile = os.getenv("BEDROCK_PROFILE", "newstacktrace-dev")

bedrock_ef = BedrockEmbeddingFunction(model_id=bedrock_model_id, region_name=bedrock_region, profile_name=bedrock_profile)

chromadb_client = chromadb.PersistentClient(path="../db/chroma_db_bedrock_sample")

# Ajustar a tipagem para ignorar o warning do tipo customizado
collection = chromadb_client.get_or_create_collection(name="my_store", embedding_function=bedrock_ef)  # type: ignore

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
