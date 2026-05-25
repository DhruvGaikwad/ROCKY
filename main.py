from langchain_openai import ChatOpenAI
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from dotenv import load_dotenv

load_dotenv()

prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(
        "You are a helpful assistant that speaks in a friendly tone and is a nerd about racing."
    ),
    HumanMessagePromptTemplate.from_template("{input}"),
])

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

prompt_value = prompt.invoke({"input": "who is the best driver in Formula 1 history?"})
messages = prompt_value.to_messages()

result = llm.generate([messages])
answer = result.generations[0][0].text

print(answer)