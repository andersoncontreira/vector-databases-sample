import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel, RunnableLambda
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
#query = "Tell me about Anderson Contreira"

# pass to llm
retriever = doc_search.as_retriever()

# question  = "Tell me about Anderson Contreira"
question = "Tell me about the articles author"
system_prompt = (
    "You are an assistant for question-answering. "
    "Use the following pieces of context to answer the question at the end. "
    "If you don't know the answer, just say that you don't know, don't try to make up an answer. "
    "Context: {context}"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

# question_answer_chain = create_stuff_documents_chain(
#     llm=model,
#     prompt=prompt,
#     document_variable_name="context",
# )

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


chain = (
    RunnableParallel({"context": retriever | RunnableLambda(format_docs), "input": RunnablePassthrough()})
    | prompt
    | model
    | StrOutputParser()
)

response = chain.invoke(question)
print(response)

# Here’s a concise profile based on the provided information:
#
# - Name: Anderson Contreira
# - Role: Solutions Architect
# - Experience: IT professional since 2008 with more than 6 years of leadership experience
# - Specialties: Distributed architecture, microservices, cloud (AWS/GCP), DevOps, and full-stack development
# - Location: Brazil
# - Education: Distributed Software Architecture at PUC Minas
# - Current job: Cloud Software Architect at Caylent (joined Oct 31, 2025)
# - Additional activity: Contributor on DEV Community, with posts on topics like career building in tech and warnings about technical test scams
#
# If you want, I can summarize a few of his specific articles or provide links (if available).


# Based on the snippet, the article on DEV Community is authored by Anderson Contreira (the URL slug is andersoncontreira). The post is titled “WARNING TO DEVELOPERS: A new wave of ‘technical test scams’ is targeting devs” and discusses scammers sending fake technical tests to developers, including patterns seen in Web3 communities.
#
# If you meant a different article in the snippet, please specify which one. I can also summarize the article or provide more about the author if you’d like.
#
# Process finished with exit code 0



# answer = response[0].content
# print(answer)
