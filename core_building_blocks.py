import os
from pathlib import Path
from pyexpat.errors import messages
from dotenv import load_dotenv


script_dir = Path(__file__).resolve().parent
print (script_dir)
env_path = script_dir/".env"
# print(env_path)
load_dotenv(dotenv_path=env_path)
# print(os.getenv("OPEN_API_KEY"))

from langchain.chat_models import init_chat_model

model = init_chat_model("openai:gpt-5")

response = model.invoke("What is Langchain in one sentence")
print(response.content)

#-------------------------------------------------------------------------------------------------------------------------------------------------------

from langchain_core.prompts import PromptTemplate,ChatPromptTemplate

simple_template = PromptTemplate(
    input_variables=["topic"],
    template="What is {topic}? explain in one sentence"
)

print(simple_template.format(topic="Merge Sort Algorithm"))

chat_template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful coding tutor. Keep answers concise and to the point."),
        ("user", "Explain {topic}? with one example"),
    ]
)

messages = chat_template.format_messages(topic="Merge Sort Algorithm")
for message in messages:
    print(f"{message.type}: {message.content}")


#-------------------------------------------------------------------------------------------------------------------------------------------------------
from langchain_core.output_parsers import StrOutputParser

chain = chat_template | model | StrOutputParser()

result = chain.invoke({"topic": "Merge Sort Algorithm"})
print(result)