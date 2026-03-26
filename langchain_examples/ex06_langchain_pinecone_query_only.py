import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel, RunnableLambda
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone

load_dotenv()

pinecone_key = os.getenv("PINECONE_API_KEY")
openai_key = os.getenv("OPENAI_API_KEY")

model = ChatOpenAI(model="gpt-5-nano")
embeddings = OpenAIEmbeddings(api_key=openai_key, model="text-embedding-3-small")

# Instancia o client Pinecone explicitamente e conecta ao índice existente
pc = Pinecone(api_key=pinecone_key)
index = pc.Index("quickstart")

doc_search = PineconeVectorStore(
    index=index,
    embedding=embeddings,
)


retriever = doc_search.as_retriever()

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


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


chain = (
    RunnableParallel({"context": retriever | RunnableLambda(format_docs), "input": RunnablePassthrough()})
    | prompt
    | model
    | StrOutputParser()
)

question = "Tell me about the articles author"
response = chain.invoke(question)
print(response)
