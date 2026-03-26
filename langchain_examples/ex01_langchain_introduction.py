# pip install langchain
# pip install langchain-openai

from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI

load_dotenv()

model = ChatOpenAI(model="gpt-5-nano")

print(model.invoke("Hello, how are you?"))
# Example: content='Hi there! I’m here and ready to help with whatever you need. How can I assist you today?' additional_kwargs={'refusal': None} response_metadata={'token_usage': {'completion_tokens': 287, 'prompt_tokens': 12, 'total_tokens': 299, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 256, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_provider': 'openai', 'model_name': 'gpt-5-nano-2025-08-07', 'system_fingerprint': None, 'id': 'chatcmpl-DNgTkgtmDmquBUqJPHaWoeeRRZqSe', 'service_tier': 'default', 'finish_reason': 'stop', 'logprobs': None} id='lc_run--019d2aa8-e045-7533-9221-e371bc903fd0-0' tool_calls=[] invalid_tool_calls=[] usage_metadata={'input_tokens': 12, 'output_tokens': 287, 'total_tokens': 299, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 256}}

messages = [
    SystemMessage(content="Translate the following English text to French, Spanish and Portuguese."),
    HumanMessage(content="Hello, how are you?"),
]

response = model.invoke(messages)

print(response)
# Example: content='French: Bonjour, comment ça va ?\nSpanish: Hola, ¿cómo estás?\nPortuguese: Olá, como vai você?' additional_kwargs={'refusal': None} response_metadata={'token_usage': {'completion_tokens': 547, 'prompt_tokens': 28, 'total_tokens': 575, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 512, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_provider': 'openai', 'model_name': 'gpt-5-nano-2025-08-07', 'system_fingerprint': None, 'id': 'chatcmpl-DNgW7PVYVrllWLySDvYHCJhpbSQqJ', 'service_tier': 'default', 'finish_reason': 'stop', 'logprobs': None} id='lc_run--019d2aab-1e9d-79a3-aaa5-11cbe40a91a6-0' tool_calls=[] invalid_tool_calls=[] usage_metadata={'input_tokens': 28, 'output_tokens': 547, 'total_tokens': 575, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 512}}