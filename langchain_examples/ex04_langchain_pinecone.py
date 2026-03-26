import os

from dotenv import load_dotenv
# from langchain_community.vectorstores import Pinecone
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore

load_dotenv()

model = ChatOpenAI(model="gpt-5-nano")

pinecone_key = os.getenv("PINECONE_API_KEY")
openai_key = os.getenv("OPENAI_API_KEY")

# loader
# txt_loader = DirectoryLoader("../data/texts", glob="*.txt", loader_cls=TextLoader)
pdf_loader = DirectoryLoader("../data/articles", glob="*.pdf", loader_cls=PyPDFLoader)  # type: ignore[arg-type]
pdfs = pdf_loader.load()


text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

documents = text_splitter.split_documents(pdfs)
print(f"Number of documents: {len(documents)}")

embeddings = OpenAIEmbeddings(api_key=openai_key, model="text-embedding-3-small")


pc = Pinecone(api_key=pinecone_key)

# PineconeVectorStore.from_documents gera os embeddings e faz o upsert automaticamente
# O índice "quickstart" deve ter dimension=1536 (text-embedding-3-small)
doc_search = PineconeVectorStore.from_documents(
    documents=documents,
    embedding=embeddings,
    index_name="quickstart",
    pinecone_api_key=pinecone_key,
)

# query = "Tell me about the articles author"
query = "Tell me about Anderson Contreira"

retrieved_docs = doc_search.similarity_search(query, k=5)

print(retrieved_docs)
print(retrieved_docs[0].page_content)
print(retrieved_docs[0].metadata)