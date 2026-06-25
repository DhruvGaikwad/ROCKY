from langchain_ollama import ChatOllama 

chat = ChatOllama(
    model="qwen3:0.6b",
    keep_alive="30m",
    num_predict = 700
            )

user=input("what is your question?")

result = chat.invoke(user)

print(result.content)