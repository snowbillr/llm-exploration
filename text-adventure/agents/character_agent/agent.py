from ..base_agent import BaseAgent
from .system_prompt import SYSTEM_PROMPT

class CharacterAgent(BaseAgent):
    def __init__(self):
        super().__init__(name='character_agent', system_prompt=SYSTEM_PROMPT)
    
    def get_character_context(self, game_id):
        return ""
    
    def update_character_context(self, game_master_message, player_message, game_id):
        pass
    