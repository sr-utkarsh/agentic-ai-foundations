from pathlib import Path

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool

script_dir = Path(__file__).resolve().parent
print (script_dir)
env_path = script_dir/".env"
# print(env_path)
load_dotenv(dotenv_path=env_path)

#initializing the chat model
modemodel = init_chat_model("openai:gpt-5")

@tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b
@tool
def subtract_numbers(a: int, b: int) -> int:    
    """Subtract two numbers."""
    return a - b
@tool
def multiply_numbers(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b
@tool
def divide_numbers(a: int, b: int) -> float | str:
    """Divide two numbers."""
    if b == 0:
        return "Error: Division by zero is not allowed."
    return a / b

agent = create_agent(modemodel, [add_numbers, subtract_numbers, multiply_numbers, divide_numbers])

result = agent.invoke({"messages": [{"role": "user", "content": "What is the sum of 5 and 3?"}]})
print(result["messages"][-1].content)
result2 = agent.invoke({"messages": [{"role": "user", "content": "What is the division of 10 and 4?"}]})
print(result2["messages"][-1].content)