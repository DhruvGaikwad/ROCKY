import subprocess
import os
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
    temperature=0.7 
)

# PERMANENT MEMORY
memory = "permanent_memory.json"
messages = loadmem(get_ev_system_message)

exit_keywords = ["exit", "quit", "close", "bye", "goodbye"]
console.print("[bold green]Model Loaded Successfully. EV diagnostic & audio link active.[/bold green]")

def speak_with_piper(text):
    """
    Sends text to the local Piper binary via stdin, generates a .wav audio file,
    and plays it using Linux ALSA (aplay).
    """
    output_audio = "ev_output.wav"
    
    # Path to your local piper binary and voice model inside your 'piper' folder
    piper_executable = "./piper/piper"
    model_path = "./piper/glados.onnx"
    
    try:
        # 1. Run piper securely via stdin pipe to prevent shell escaping/quoting issues
        process = subprocess.Popen(
            [piper_executable, "--model", model_path, "--output_file", output_audio],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        process.communicate(input=text.encode("utf-8"))
        
        # 2. Play the audio file using Linux 'aplay'
        if os.path.exists(output_audio):
            subprocess.run(["aplay", "-q", output_audio], check=True)
            
    except Exception as e:
        console.print(f"[bold red][System Error: Audio generation failed - {e}][/bold red]")

while True:
    user = input("\nwhat is your question? ").lower()

    if user in exit_keywords: 
        byebye="Logging off. Don't let the magic smoke out."
        console.print("[bold yellow]Logging off. Don't let the magic smoke out.[/bold yellow]")
        speak_with_piper(byebye)
        savemem(messages)
        break

    

    result = chat.invoke([*messages, HumanMessage(content=user)])

    messages.append(HumanMessage(content=user))
    messages = summarize_history_if_needed(messages, chat)
    messages.append(result)

    # Render inside Rich Panel with EV styling
    console.print(Panel(
        result.content,
        title="EV",
        subtitle="EV_1.2",
        style="bold magenta",
        title_align="left",
    ))

    # Trigger Piper speech output
    speak_with_piper(result.content)