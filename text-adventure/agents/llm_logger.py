from llm_event_bus import LLMEventBus
from llm_event_types import LLMEvent

def log_llm_call(agent_name, input_data, output_data):
    event = LLMEvent(agent=agent_name, input_data=input_data, output_data=output_data)
    LLMEventBus.put_event(event)
