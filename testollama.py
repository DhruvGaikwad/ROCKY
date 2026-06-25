from langchain_ollama import ChatOllama 

chat = ChatOllama(
    model="qwen3:0.6b",
    keep_alive="30m",
    num_predict = 700
            )

print("Model Loaded Successfully")

while True:
    
    user=input("what is your question?").lower()

    if user == "exit":
        break
    
    result = chat.invoke(user)
    
    print(result.content)