from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os 

load_dotenv() # this is the perfect barebones eg of openAI model 

api=os.getenv("OPENAI_API_KEY")

chat = ChatOpenAI(openai_api_key=api)

result=chat.invoke("best driver in Formula 1 history?")

print(result.content)