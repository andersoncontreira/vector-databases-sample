# openai
# pip install openai
# pip install python-dotenv
import os
import openai
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# openai.api_key = os.getenv("OPENAI_API_KEY")
# print(openai.api_key)
# exit()
# client = OpenAI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# response = client.embeddings.create(input=["This is a test"], model="text-embedding-ada-002")
response = client.embeddings.create(input=["This is a test"], model="text-embedding-3-small")

print (response.data[0].embedding)
print (response.usage)

