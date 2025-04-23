from db.models import Message, Player, Game
from datetime import datetime
from agents import GameMasterAgent, InventoryAgent, NarrativeAgent, CharacterAgent
from agents.llm_logger import log_llm_call

class GameLoop:
    def __init__(self):
        self.player = None
        self.game = None
        self.game_master = GameMasterAgent()
        self.inventory_agent = InventoryAgent()
        self.character_agent = CharacterAgent()
        self.narrative_agent = NarrativeAgent()

    def create_game(self):
        self.game = Game.create(created_at=datetime.now())
        return self.game

    def create_player(self, player_name):
        if self.game is None:
            self.create_game()
        self.player = Player.create(name=player_name, game=self.game)
        return self.player

    def process_turn(self, player_input):
        if self.player is None:
            raise ValueError("Player must be set before processing a turn.")
        if self.game is None:
            raise ValueError("Game must be set before processing a turn.")

        Message.create(
            content=player_input,
            role=Message.ROLE_USER,
            timestamp=datetime.now(),
            player=self.player
        )

        narrative_context = self.narrative_agent.get_narrative_context(game_id=self.game.id)
        character_context = self.character_agent.get_character_context(game_id=self.game.id)
        inventory_context = self.inventory_agent.get_inventory_context(game_id=self.game.id)
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
            game_id=self.game.id
        )

        self.character_agent.update_character_context(
            game_master_message=game_master_response_text,
            player_message=player_input,
            game_id=self.game.id
        )

        self.inventory_agent.update_inventory_context(
            game_master_message=game_master_response_text,
            player_message=player_input,
            game_id=self.game.id
        )

        return game_master_response_text
