from langchain_ollama import ChatOllama 

chat = ChatOllama(model="llama3.2:3b")

result = chat.invoke("best driver in Formula 1 history?")

print(result.content)