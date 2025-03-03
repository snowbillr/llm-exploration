from ..base_agent import BaseAgent
from .system_prompt import SYSTEM_PROMPT

class GameMasterAgent(BaseAgent):
  def __init__(self):
    super().__init__(name='game_master', system_prompt=SYSTEM_PROMPT)
