import json
import os 
from langchain_core.messages import HumanMessage, SystemMessage, messages_to_dict,messages_from_dict



memory="permanent_memory.json"

max_memory=10

def loadmem(default_system_message):
    if os.path.exists(memory):
        with open(memory, "r") as f:
            data = json.load(f)
            return messages_from_dict(data)

    print("No memory found. Starting fresh.")
    fresh_messages = [default_system_message()]
    savemem(fresh_messages)
    return fresh_messages

def savemem(messages):
    with open(memory, "w") as f:
        json.dump(messages_to_dict(messages), f, indent=2)

def summarize_history_if_needed(messages, chat_model):
    """Compresses middle turns if history gets too long."""
    if len(messages) > max_memory:
        print("\n[System: Summarizing older conversation context...]")
        
        system_prompt = messages[0]      # Always keep original persona
        recent_messages = messages[-4:]  # Preserve last 4 turns for context continuity
        old_messages = messages[1:-4]    # Isolate middle turns to compress
        
        summary_prompt = (
            "Summarize key technical facts, decisions, and context from "
            f"this chat history briefly:\n{old_messages}"
        )
        
        summary_result = chat_model.invoke([HumanMessage(content=summary_prompt)])
        
        compressed_note = SystemMessage(
            content=f"Summary of previous interactions: {summary_result.content}"
        )
        
        # Reconstruct list: [Persona, Summary Note, Recent Messages...]
        return [system_prompt, compressed_note] + recent_messages
    
    return messages