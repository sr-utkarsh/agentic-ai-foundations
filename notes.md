# Agentic AI Notes

## Tool Definition Pattern

```python
from json import tool


@tool  # decorator to register the function as a tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers."""  # docstring to describe the function
    return a + b
```

### What this does

- The `@tool` decorator registers the function as a tool for an agent.
- The function is converted into a JSON schema by the framework.
- That schema helps the LLM understand:
  - the function's purpose
  - the expected inputs
  - how to call it correctly

This allows the model to discover and use the function as part of an agent workflow.

---

## How a User Request Flows Through an Agent

1. The user calls the agent.
2. The agent invokes `agent.invoke()`.
3. The framework sends a request to the LLM.
4. The Python code prepares:
   - the prompt
   - tool definitions
   - conversation context
5. The request is sent to the model API.

The user does not communicate directly with the model API. Instead, they interact with the LangChain framework, which handles the communication for them.

---

## How Tools Are Sent to the Model

When LangChain calls the model API, it sends:

- a list of messages
- a list of available tools

The model can then decide whether it needs to call one of those tools.

### Tool-call structure returned by the model

The model returns a structured tool call request that includes:

- `content` (often empty when the model wants to call a tool)
- `call_id`
- `tool_name`
- `arguments`

This is a structured response, not a direct Python execution.

---

## How LangChain Handles Tool Calls

When LangChain receives the model response, it checks for two things:

- whether `content` is empty or not
- whether a tool call is present

If the content is empty and a tool call exists, LangChain understands that the model is not done yet and wants to execute a tool.

It then:

1. extracts the `call_id`, `tool_name`, and `arguments`
2. looks up the function reference in a registry
3. matches the tool name to the Python function
4. executes the Python function
5. returns the result back to the model with:
   - the tool result as content
   - the original `tool_call_id` so the result can be mapped correctly

---

## Important Note

The full conversation history is sent every time because LLMs are stateless. This means the model does not remember previous interactions unless that context is included in the current request.

---

## Summary

LangChain acts as the bridge between:

- the user
- the Python code
- the LLM API
- the available tools

The model decides when to use a tool, LangChain executes the matching Python function, and the result is sent back into the conversation so the agent can continue reasoning.
