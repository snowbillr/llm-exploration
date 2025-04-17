from dataclasses import dataclass
from typing import Any
import time

@dataclass
class LLMEvent:
    agent: str
    input_data: Any
    output_data: Any
    timestamp: float = time.time()
