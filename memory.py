import json
import os 
from langchain_core.messages import HumanMessage, SystemMessage, messages_to_dict,messages_from_dict



memory="permanent_memory.json"

max_memory=12

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

def summarize_history_if_needed(messages, chat_model=None):
    if len(messages) > max_memory:
        system_prompt = messages[0]
        recent_messages = messages[-max_memory:]
        return [system_prompt] + recent_messages
    
    return messages