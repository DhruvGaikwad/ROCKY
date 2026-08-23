import subprocess
import os
import speech_recognition as sr
import pyautogui as pyau
import datetime as dt 
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
screenshot_key=["clip that", "screenshot", "capture that","ev clip that","chat clip that"]

console.print("[bold green]Model Loaded Successfully. EV voice-only loop active.[/bold green]")

#ALSA LOGS SUPRESSION (THIS IS SOO ANNOYING)

def mute_stderr(): 
    """Temporarily redirects low-level C stderr to /dev/null to kill ALSA/PortAudio spam."""
    devnull = os.open(os.devnull, os.O_WRONLY)
    old_stderr = os.dup(2)
    os.dup2(devnull, 2)
    os.close(devnull)
    return old_stderr

def unmute_stderr(old_stderr):
    """Restores standard error."""
    os.dup2(old_stderr, 2)
    os.close(old_stderr)

def speak_with_piper(text):
    """Sends text to Piper via stdin and plays audio via aplay with muted logs."""
    output_audio = "ev_output.wav"
    piper_executable = "./piper/piper"
    model_path = "./piper/glados.onnx"
    
    try:
        process = subprocess.Popen(
            [piper_executable, "--model", model_path, "--output_file", output_audio],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        process.communicate(input=text.encode("utf-8"))
        
        if os.path.exists(output_audio):
            old_err = mute_stderr()
            subprocess.run(["aplay", "-q", output_audio], check=True)
            unmute_stderr(old_err)
            
    except Exception as e:
        console.print(f"[bold red][System Error: Audio generation failed - {e}][/bold red]")

def listen_to_user():
    """Captures microphone input while suppressing PortAudio/ALSA startup warnings."""
    r = sr.Recognizer()
    
    old_err = mute_stderr()
    try:
        with sr.Microphone() as source:
            unmute_stderr(old_err)
            console.print("[bold yellow] Listening... Speak your command.[/bold yellow]")
            r.adjust_for_ambient_noise(source, duration=0.5)
            
            old_err = mute_stderr()
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            unmute_stderr(old_err)
            
            console.print("[cyan]Processing speech...[/cyan]")
            text = r.recognize_google(audio)
            console.print(f"[green]You said: \"{text}\"[/green]")
            return text.lower()
            
    except sr.WaitTimeoutError:
        unmute_stderr(old_err)
        console.print("[dim red]Listening timed out. No speech detected.[/dim red]")
        return ""
    except sr.UnknownValueError:
        unmute_stderr(old_err)
        console.print("[dim red]Could not understand audio.[/dim red]")
        return ""
    except Exception as e:
        unmute_stderr(old_err)
        console.print(f"[bold red]Speech Recognition Error: {e}[/bold red]")
        return ""

while True:
    user = listen_to_user()

    if user in exit_keywords: 
        byebye = "Logging off. Don't let the magic smoke out."
        console.print(f"[bold yellow]{byebye}[/bold yellow]")
        speak_with_piper(byebye)
        savemem(messages)
        break

    if user in screenshot_key:
        screenshot_message = "screenshot taken"
        console.print(f"[bold yellow]{screenshot_message}[/bold yellow]")
        speak_with_piper(screenshot_message)
        timestamp =dt.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        filename = f"screenshot_{timestamp}.png"
        pyau.screenshot(filename)
        pyau.save(filename)

    result = chat.invoke([*messages, HumanMessage(content=user)])

    messages.append(HumanMessage(content=user))
    messages = summarize_history_if_needed(messages, chat)
    messages.append(result)

    console.print(Panel(
        result.content,
        title="EV",
        subtitle="EV_1.3",
        style="bold magenta",
        title_align="left",
    ))

    speak_with_piper(result.content)