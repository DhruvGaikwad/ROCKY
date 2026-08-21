
from langchain_ollama import ChatOllama 
from langchain_core.messages import HumanMessage

from personality import get_ev_system_message
from memory import loadmem, savemem, summarize_history_if_needed

from rich.console import Console
from rich.panel import Panel

console = Console()


chat = ChatOllama(
    model="llama3.2:3b",
    keep_alive="30m",
    num_predict = 700,
    temperature=0.7 #controls randomness of output. 
            )

#PERMANENT MEMORY

memory="permanent_memory.json"

messages = loadmem(get_ev_system_message)



exit = ["exit", "quit", "close", "bye", "goodbye"]
console.print("[bold green]Model Loaded Successfully[/bold green]")

while True:
    
    user=input("what is your question?").lower()

    if user in exit : 
        console.print("[bold yellow]You leave now. I wait. Happy return later[/bold yellow]")
        savemem(messages)
        break



    result = chat.invoke([*messages, HumanMessage(content=user)])

    messages.append(HumanMessage(content=user))#human message comes before AI message or else it stores the messages incorrectly sequentially 
    messages = summarize_history_if_needed(messages, chat)
    messages.append(result)
    savemem(messages)

    console.print(Panel(
        result.content,
        title="EV",
        subtitle="Llama3.2:3b",
        style="bold green",
        title_align="left",
    ))



