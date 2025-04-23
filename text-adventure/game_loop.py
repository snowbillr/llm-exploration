from db.models import Message, Player
from datetime import datetime
from agents import GameMasterAgent, InventoryAgent, NarrativeAgent, CharacterAgent
from agents.llm_logger import log_llm_call

class GameLoop:
    def __init__(self):
        self.game_master = GameMasterAgent()
        self.inventory_agent = InventoryAgent()
        self.character_agent = CharacterAgent()
        self.narrative_agent = NarrativeAgent()
        self.player = None

    def create_player(self, player_name):
        self.player = Player.create(name=player_name)
        return self.player

    def process_turn(self, player_input, player=None):
        if player is not None:
            self.player = player
        if self.player is None:
            raise ValueError("Player must be set before processing a turn.")

        Message.create(
            content=player_input,
            role=Message.ROLE_USER,
            timestamp=datetime.now(),
            player=self.player
        )

        narrative_context = self.narrative_agent.get_narrative_context(player_id=self.player.id)
        character_context = self.character_agent.get_character_context(player_id=self.player.id)
        inventory_context = self.inventory_agent.get_inventory_context(player_id=self.player.id)
        last_messages = [
            f"{message.role}: {message.content}"
            for message in Message.select().where(Message.player == self.player.id).order_by(Message.timestamp.asc()).limit(4)
        ]
        message = f"""
NARRATIVE_CONTEXT:
- {'\n- '.join(narrative_context)}

CHARACTER_CONTEXT:
{character_context}

INVENTORY_CONTEXT:
{inventory_context}

LAST_MESSAGES:
- {'\n- '.join(last_messages)}
"""

        game_master_response_text = self.game_master.chat([
            { "role": "assistant", "content": message },
            { "role": "user", "content": player_input }
        ])['message']['content']

        log_llm_call("GameMasterAgent", message, game_master_response_text)    

        Message.create(
            content=game_master_response_text,
            role=Message.ROLE_ASSISTANT,
            timestamp=datetime.now(),
            player=self.player
        )

        self.narrative_agent.update_narrative_context(
            game_master_message=game_master_response_text,
            player_message=player_input,
            player_id=self.player.id
        )

        self.character_agent.update_character_context(
            game_master_message=game_master_response_text,
            player_message=player_input,
            player_id=self.player.id
        )

        self.inventory_agent.update_inventory_context(
            game_master_message=game_master_response_text,
            player_message=player_input,
            player_id=self.player.id
        )

        return game_master_response_text
