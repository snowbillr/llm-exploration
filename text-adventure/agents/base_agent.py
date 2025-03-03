from ollama import chat, ChatResponse, create

class BaseAgent:
  def __init__(self, name: str, system_prompt: str):
    self.model_name = name
    self.model = create(model=name, system=system_prompt, from_='llama3.2')

  def chat(self, messages):
    return chat(model=self.model_name, messages=messages)
