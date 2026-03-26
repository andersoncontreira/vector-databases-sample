# pip install langchain
# pip install langchain-openai
#  pip install langchain-community
import os

from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma


load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

model = ChatOpenAI(model="gpt-5-nano")

pdf_loader = DirectoryLoader("../data/articles", glob="*.pdf", loader_cls=PyPDFLoader)  # type: ignore[arg-type]
txt_loader = DirectoryLoader("../data/texts", glob="*.txt", loader_cls=TextLoader)

txt_documents = txt_loader.load()
pdf_documents = pdf_loader.load()

# print(txt_documents)
# print(pdf_documents)

# Split texts into chunks
text_splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n"],
    chunk_size=1000, chunk_overlap=200)

texts = text_splitter.split_documents(txt_documents)

print("len of chunks: ", len(texts))

# get embeddings
embeddings = OpenAIEmbeddings(api_key=openai_api_key, model="text-embedding-3-small")
# print(embeddings)

persist_path = "../db/chroma_db_with_langchain"
vectordb = Chroma.from_documents(texts, embeddings, persist_directory=persist_path)

print(vectordb)
# vectordb.persist()

retriever = vectordb.as_retriever()


result = retriever.invoke("What is the capital of France?", k=5)
print(result)
# [Document(metadata={'source': '../data/texts/franca.txt'}, page_content='País: França\nNome oficial: República Francesa\nData de fundação: 843 d.C. (Tratado de Verdun, divisão do Império Carolíngio) / 1792 (Primeira República)\nCapital: Paris\nIdioma oficial: Francês\nMoeda: Euro (EUR)\nTotal de regiões: 18 regiões (13 metropolitanas e 5 ultramarinas)\nTotal de departamentos: 101 departamentos\nTotal de municípios (communes): aproximadamente 34.955\nPopulação estimada: aproximadamente 68 milhões de habitantes (2023)\nÁrea territorial: 551.695 km² (território metropolitano)\nRegião: Europa Ocidental\n\nHistória:'), Document(metadata={'source': '../data/texts/franca.txt'}, page_content='País: França\nNome oficial: República Francesa\nData de fundação: 843 d.C. (Tratado de Verdun, divisão do Império Carolíngio) / 1792 (Primeira República)\nCapital: Paris\nIdioma oficial: Francês\nMoeda: Euro (EUR)\nTotal de regiões: 18 regiões (13 metropolitanas e 5 ultramarinas)\nTotal de departamentos: 101 departamentos\nTotal de municípios (communes): aproximadamente 34.955\nPopulação estimada: aproximadamente 68 milhões de habitantes (2023)\nÁrea territorial: 551.695 km² (território metropolitano)\nRegião: Europa Ocidental'), Document(metadata={'source': '../data/texts/franca.txt'}, page_content='Fatos relevantes:\n- Paris é a cidade mais visitada do mundo, com mais de 100 milhões de turistas por ano.\n- A Torre Eiffel, construída em 1889 para a Exposição Universal, é o monumento mais visitado do planeta.\n- A França é o maior produtor de vinho do mundo e referência mundial em gastronomia e moda.\n- O Museu do Louvre, em Paris, é o maior museu de arte do mundo e abriga a Mona Lisa.\n- A França possui territórios ultramarinos em todos os oceanos do mundo, o que lhe garante a segunda maior zona econômica exclusiva do planeta.\n- É o país com maior número de Patrimônios da Humanidade reconhecidos pela UNESCO na Europa.'), Document(metadata={'source': '../data/texts/franca.txt'}, page_content='Fatos relevantes:\n- Paris é a cidade mais visitada do mundo, com mais de 100 milhões de turistas por ano.\n- A Torre Eiffel, construída em 1889 para a Exposição Universal, é o monumento mais visitado do planeta.\n- A França é o maior produtor de vinho do mundo e referência mundial em gastronomia e moda.\n- O Museu do Louvre, em Paris, é o maior museu de arte do mundo e abriga a Mona Lisa.\n- A França possui territórios ultramarinos em todos os oceanos do mundo, o que lhe garante a segunda maior zona econômica exclusiva do planeta.\n- É o país com maior número de Patrimônios da Humanidade reconhecidos pela UNESCO na Europa.'), Document(metadata={'source': '../data/texts/franca.txt'}, page_content="História:\nO território francês foi habitado pelos gauleses antes de ser conquistado por Júlio César entre 58 e 50 a.C., tornando-se parte do Império Romano (Gália). Com a queda de Roma, os francos dominaram a região, e Carlos Magno unificou grande parte da Europa Ocidental no século VIII. A França medieval foi palco de conflitos como a Guerra dos Cem Anos com a Inglaterra (1337-1453), durante a qual Joana d'Arc se tornou heroína nacional. A Revolução Francesa de 1789 foi um marco na história mundial, derrubando a monarquia absolutista e proclamando os princípios de liberdade, igualdade e fraternidade. Napoleão Bonaparte ascendeu ao poder no início do século XIX, criando um vasto império europeu antes de ser derrotado em 1815. A França participou das duas Guerras Mundiais e foi ocupada pela Alemanha entre 1940 e 1944. No pós-guerra, tornou-se membro fundador da União Europeia e da OTAN, e uma das cinco potências nucleares permanentes no Conselho de Segurança da ONU.\n\nFatos relevantes:")]




# print(model.invoke("Hello, how are you?"))
# # Example: content='Hi there! I’m here and ready to help with whatever you need. How can I assist you today?' additional_kwargs={'refusal': None} response_metadata={'token_usage': {'completion_tokens': 287, 'prompt_tokens': 12, 'total_tokens': 299, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 256, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_provider': 'openai', 'model_name': 'gpt-5-nano-2025-08-07', 'system_fingerprint': None, 'id': 'chatcmpl-DNgTkgtmDmquBUqJPHaWoeeRRZqSe', 'service_tier': 'default', 'finish_reason': 'stop', 'logprobs': None} id='lc_run--019d2aa8-e045-7533-9221-e371bc903fd0-0' tool_calls=[] invalid_tool_calls=[] usage_metadata={'input_tokens': 12, 'output_tokens': 287, 'total_tokens': 299, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 256}}
#
# messages = [
#     SystemMessage(content="Translate the following English text to French, Spanish and Portuguese."),
#     HumanMessage(content="Hello, how are you?"),
# ]
#
# response = model.invoke(messages)
#
# print(response)
# # Example: content='French: Bonjour, comment ça va ?\nSpanish: Hola, ¿cómo estás?\nPortuguese: Olá, como vai você?' additional_kwargs={'refusal': None} response_metadata={'token_usage': {'completion_tokens': 547, 'prompt_tokens': 28, 'total_tokens': 575, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 512, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_provider': 'openai', 'model_name': 'gpt-5-nano-2025-08-07', 'system_fingerprint': None, 'id': 'chatcmpl-DNgW7PVYVrllWLySDvYHCJhpbSQqJ', 'service_tier': 'default', 'finish_reason': 'stop', 'logprobs': None} id='lc_run--019d2aab-1e9d-79a3-aaa5-11cbe40a91a6-0' tool_calls=[] invalid_tool_calls=[] usage_metadata={'input_tokens': 28, 'output_tokens': 547, 'total_tokens': 575, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 512}}